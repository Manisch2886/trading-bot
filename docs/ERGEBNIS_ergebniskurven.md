# Ergebnis — Ergebniskurven erneuert und gegen Veralterung gesichert

Branch `claude/new-session-bb4yi0`, Basis `origin/main` (`317e6b9`, nach Merge
von PR #84). Zwei Commits: erst das Werkzeug, dann — getrennt — die Kurven.

---

## Zuerst: die Zahl, die Sie wöchentlich lesen, war zu gut

Montags-Mail und Dashboard-Portfolio-Sicht rechnen aus
`results/*/equity_curve.csv` — zu 100 %, weil alle neun Bots unter
`MIN_LIVE_CLOSED_TRADES = 10` liegen.

| | vorher | nachher |
|---|---:|---:|
| Vergleichsfenster | 2022-03-18 – 2026-06-27 | 2022-03-18 – **2026-08-20** |
| Rendite im Fenster | +80,52 % | **+69,68 %** |
| **Max Drawdown kombiniert** | **−6,24 %** | **−11,29 %** |

**Der kombinierte Drawdown hat sich fast verdoppelt.** Er war nie eine
Eigenschaft des Portfolios, sondern zu grossen Teilen eine Eigenschaft
veralteter Dateien.

Der kombinierte Vierer-Drawdown, die bekannte Zahl aus
`portfolio_correlation_analysis.py`: **−1,43 % → −9,34 %.** Damit ist die
Vorhersage der Exposure-Messung (−9,41 %) bestätigt; die 0,07 Punkte
Unterschied sind erklärt (siehe unten).

**Hängt daran eine getroffene Entscheidung?** Nein. Die −1,43 % waren durch
PR #84 ohnehin schon als Risikokennzahl verworfen, und die Montags-Mail-Zahlen
lösen nichts aus. Was sich ändert, ist die Grundlage **künftiger**
Entscheidungen — und die Korrektur geht durchweg in die unangenehme Richtung.

---

## Fünf von neun Kurven beschrieben einen Bot, den es nicht mehr gibt

| Bot | Zeilen alt | Zeilen neu | Rendite alt | Rendite neu | MaxDD alt | MaxDD neu |
|---|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | 144 | 130 | +84,33 % | +67,77 % | **−0,69 %** | **−10,17 %** |
| `elliott_wave_stocks` | 469 | 395 | +1500,53 % | +352,72 % | **−1,90 %** | **−22,44 %** |
| `rsi2_mean_reversion` | 2.641 | 4.232 | +29,91 % | +36,75 % | −21,82 % | −21,05 % |
| `turtle_soup_stocks` | 1.887 | 8.915 | +133,01 % | +145,59 % | −32,54 % | −29,91 % |
| `volatility_breakout` | 1.236 | 1.454 | +142,06 % | +224,41 % | −22,39 % | −23,97 % |

**„Veraltet" trifft es nicht.** Bei vier der fünf laufen die Kurven schon in
der **ersten Zeile** auseinander. Ursachen: die Look-Ahead-Korrektur (PR #26,
beide Elliott-Bots — die Drawdowns von −0,69 % und −1,90 % waren ein
Rechenfehler, keine Strategieeigenschaft), die Sync-Reihe (PR #38–#59,
Allokation 10 % → 5 % bzw. 2 %) und die Kurslückenbehandlung (PR #81).

**Unverändert, byteweise identisch neu erzeugt:** `rsi2_crypto`,
`t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto`. Das ist
die wichtigste Gegenprobe: Ein Verfahren, das alle neun Kurven verändert
hätte, hätte nichts bewiesen.

---

## Die Wiederholungssperre

```bash
python3 shared/ergebniskurven.py                    # prüfen, Rückgabewert 1 bei Befund
python3 shared/ergebniskurven.py --erzeugen         # neu schreiben
python3 shared/ergebniskurven.py --nur-abweichung   # nur der ernste Fall (Cron)
```

**Sie erzeugt die Kurve neu und vergleicht Zeile für Zeile** — nicht die
Zeilenzahl, keinen Parameter-Fingerabdruck, keinen Zeitstempel.

Der Grund ist der HRP-Fall selbst: Dort war nicht die Zahl der Trades das
Problem, sondern ein nicht angewendeter Regimefilter — und der ist **kein Wert
in `live_params.py`**, sondern eine Aufrufstelle im `__main__`-Block. Der
`live_params.py`-Diff von PR #57 bestand aus **einer geänderten
Kommentar-Zeilennummer**. Ein Parameter-Fingerabdruck hätte die Änderung nicht
gesehen; ein Quelltext-Fingerabdruck hätte bei jedem Kommentar gemeldet.

**Zwei Arten von Befund**, und die Trennung ist der eigentliche Trick:

* `VERALTET` — die abgelegte Kurve ist ein exakter **Anfang** der heutigen,
  es sind nur neue Kursdaten dazugekommen. Unvollständig, nicht falsch.
* `ABWEICHEND` — schon der gemeinsame Teil läuft auseinander. Jede Zahl aus
  dieser Datei ist neu zu prüfen.

Ohne diese Trennung meldete ein Cronjob **jeden Tag** (die Kursdaten wachsen)
und wäre binnen einer Woche nicht mehr gelesen.

**Der Live-Betrieb wird nie blockiert.** Kein Bot ruft das Werkzeug auf. Beim
Prüfen schreibt es *strukturell* nicht nach `results/`: `kurven_lauf.py` lenkt
`RESULTS_DIR` in einen temporären Ordner um, nur `--erzeugen` kopiert von dort
in die Ablage.

Dauer: rund **50 Sekunden** für alle neun Bots. Cron-Zeile steht als Vorschlag
in `shared/README_ERGEBNISKURVEN.md`, **nicht eingetragen**.

---

## Tests: 44 von 44 — und die Leerprobe

Der Kern: **derselbe Bot, dieselbe Prüfung — vorher grün, nach einer reinen
Konfigurationsänderung rot, bei nachweislich unveränderter Zeilenzahl**
(207 vorher, 207 nachher).

Beide bekannten Fallen sind umgangen:

* Die veraltete Kurve wird **nie von Hand geschrieben** — der Test ändert nur
  die Konfiguration des Bots und lässt dessen eigenes `equity_simulation.py`
  rechnen, in einem lauffähigen Klon des Repos. Beobachtet wird der Ablauf.
* Der Prüffall ändert die Zeilenzahl **nicht**, damit **nur** der
  Inhaltsvergleich ihn fangen kann. Nachgewiesen per Leerprobe: entfernt man
  den Inhaltsvergleich, fällt genau dieser Abschnitt rot aus.

Alle bestehenden Tests bestehen weiterhin (u. a. Dashboard 784/784,
Kurslücken 83/83, Broker 163/163 und 168/168). Eine **vorbestehende**
Einzelabweichung in `research/exposure_messung/test_exposure_kern.py` ist vor
und nach der Erneuerung Zeile für Zeile identisch (pandas-`pct_change`, keine
Kurve).

---

## Die drei Untersuchungen mit überholter Grundlage

| Ordner | berührt? |
|---|---|
| `hrp_portfolio` | **Die entscheidende Frage: nein.** `volatility_breakout_crypto` ist byteweise unverändert — das Vorzeichen, das dort an 0,7 % hängt, ist unangetastet, und die Kernaussage (`korrigiert_v2` gegen `v2_mit_regimefilter`) beruht auf eingefrorenen Kurven. **Aber** `nachtrag_vbc_regimefilter.py` bricht jetzt ab: sein Anker `korrigiert_v1` liest vier Kurven — darunter `elliott_wave` — weiterhin **live**. Siehe offener Punkt 1. |
| `trend_overlay` | Gleiche Bauart, gleiche Abhängigkeit. Seine `nachtrag_sync_korrektur*.py` scheitern aber **schon mit den alten Kurven** — die Erneuerung ist dort nicht die Ursache. Beide Test-Dateien bestehen vorher wie nachher. |
| `order_sensitivity` | **Nicht berührt.** Liest `results/*/equity_curve.csv` an keiner Stelle; `run_one_bot.py` rechnet alles selbst aus dem Bot-Code. |

---

## Was bewusst nicht angefasst wurde

`git diff 317e6b9..HEAD -- strategies/ broker/` ist **leer**. `live_params.py`,
`forward_test.py`, `equity_simulation.py`, `shared/portfolio_overview.py` und
`dashboard/portfolio_sicht.py` wurden ausschliesslich **aufgerufen**. Keine
Crontab, keine launchd-Vorlage. Die Ablage von `elliott_wave` bleibt unter
`results/equity_curve.csv` — ein Umzug würde stillschweigend die Quelle
wechseln, die die Montags-Mail liest.

---

## Vier offene Punkte, die aus dieser Arbeit folgen

1. **`research/hrp_portfolio/nachtrag_vbc_regimefilter.py` bricht ab.** Der
   Anker `korrigiert_v1` hängt an vier lebenden Kurven — dieselbe Bauart-Lücke,
   die Abschnitt W1 des Berichts für den Anker `original` bereits geschlossen
   hatte, eine Stufe tiefer. Abhilfe: die vier synchronen Kurven als
   `corrected_curves_v1_clean/` mit `MANIFEST.json` einfrieren. **Nicht
   behoben** — der Auftrag sagte „nicht neu rechnen". Freizugeben.
2. **`sort_values("time")` ist nicht stabil.** `portfolio_correlation_analysis.py`
   und `shared/portfolio_overview.py` verlieren dadurch bei den Aktien-Bots die
   Reihenfolge innerhalb eines Tages; `groupby(...).last()` greift dann nicht
   zwingend die chronologisch letzte Zeile ab. Gemessen: mit `kind="stable"`
   ergibt dieselbe Datei auf denselben Kurven **exakt −9,41 %** statt −9,34 %
   (und −11,41 % statt −11,29 % bei der Montags-Mail) — genau die Werte der
   Exposure-Messung. Klein, aber es ist eine Zahl, die von der
   Sortierimplementierung abhängt. Beide Dateien durften nur aufgerufen werden.
3. **Die Montags-Mail nennt weiterhin eine Backtest-Zahl „LIVE-PORTFOLIO"**
   (Protokoll 9.15, unverändert offen).
4. **Die Kurven veralten weiter** — das Werkzeug meldet es, aber nur, wenn es
   läuft. Solange die Crontab klemmt (Protokoll 9.14), hängt das an einem
   Aufruf von Hand. Der richtige Zeitpunkt: **vor jeder Auswertung, die
   `results/` liest.**

---

## Dateien

| Datei | Zweck |
|---|---|
| `shared/ergebniskurven.py` | das Werkzeug: prüfen (Rückgabewert 1) und erzeugen |
| `shared/kurven_lauf.py` | ein Prozess je Bot, führt dessen eigenen `__main__`-Block aus |
| `shared/test_ergebniskurven.py` | 44 Selbstprüfungen inkl. Mutationsproben |
| `shared/README_ERGEBNISKURVEN.md` | Benutzung, Begründung der Prüfgrösse, Cron-Vorschlag |
| `results/…/equity_curve.csv` (5 ×) | die erneuerten Kurven, eigener Commit |
| `docs/UEBERGABE_ergebniskurven.md` | ausführliche Übergabe |
| `docs/TESTAUFTRAG_ergebniskurven.md` | autonom abarbeitbarer Prüfplan |
