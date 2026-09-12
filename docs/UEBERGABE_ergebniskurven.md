# Übergabe — Ergebniskurven erneuert und gegen Veralterung gesichert

Branch `claude/new-session-bb4yi0`, Basis `origin/main` (`317e6b9`, nach Merge
von PR #84). Zwei Commits: erst das Werkzeug, dann — getrennt — die Kurven.

---

## 1. Zuerst: die Zahlen, die sich verschoben haben

### Montags-Mail und Dashboard-Portfolio-Sicht

Beide rechnen mit `shared/portfolio_overview.py` und lesen laut Protokoll 4.3b
`results/*/equity_curve.csv`, solange ein Bot unter
`MIN_LIVE_CLOSED_TRADES = 10` geschlossenen Live-Trades liegt. **Alle neun
liegen darunter** — es sind also zu 100 % diese Dateien.

| Gruppe „LIVE-PORTFOLIO (alle neun)" | vorher | nachher |
|---|---:|---:|
| Vergleichsfenster | 2022-03-18 – **2026-06-27** | 2022-03-18 – **2026-08-20** |
| Rendite im Fenster | +80,52 % | **+69,68 %** |
| **Max Drawdown kombiniert** | **−6,24 %** | **−11,29 %** |
| schlechtester Einzel-Bot | −32,40 % | −32,40 % |

Die Dashboard-Portfolio-Sicht zeigt dieselben Zahlen (Gruppe `alle`); die
Gruppe `nur_echte_trades` bleibt vorher wie nachher leer, weil kein Bot die
Schwelle erreicht.

**Der kombinierte Drawdown hat sich also fast verdoppelt.** Er war nie eine
Eigenschaft des Portfolios, sondern zu grossen Teilen eine Eigenschaft
veralteter Dateien.

Je Bot, im jeweiligen gemeinsamen Fenster:

| Bot | Rendite vorher | Rendite nachher | MaxDD vorher | MaxDD nachher |
|---|---:|---:|---:|---:|
| Elliott Wave (Krypto) | +61,63 % | +58,43 % | **−0,23 %** | **−10,17 %** |
| Elliott Wave (Aktien) | +286,68 % | +113,70 % | **−1,65 %** | **−16,23 %** |
| RSI-2 (Krypto) | +29,42 % | +27,64 % | −13,11 % | −13,11 % |
| RSI-2 Mean-Reversion (Aktien) | +21,47 % | +36,75 % | −11,61 % | −8,60 % |
| T3/SuperTrend (Krypto) | +110,85 % | +96,99 % | −22,20 % | −22,20 % |
| Turtle Soup (Krypto) | +112,50 % | +122,22 % | −32,40 % | −32,40 % |
| Turtle Soup (Aktien) | +18,33 % | +71,19 % | −23,03 % | −18,67 % |
| Volatility Breakout (Aktien) | +31,15 % | +53,61 % | −22,39 % | −23,97 % |
| Volatility Breakout (Krypto) | +52,67 % | +46,64 % | −16,29 % | −16,29 % |

> **Achtung beim Lesen dieser Tabelle:** auch bei den vier Bots mit
> **unveränderter** Kurve ändert sich die Rendite. Das liegt nicht an ihnen,
> sondern am gemeinsamen Fenster: es endet jetzt zwei Monate später, weil die
> `elliott_wave`-Kurve nicht mehr am 27.06. aufhört. Der Drawdown dieser vier
> bleibt folgerichtig gleich.

### Der kombinierte Vierer-Drawdown — die −1,43 %

`strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py`, die Quelle
der Zahl:

| | vorher | nachher |
|---|---:|---:|
| Elliott Wave (Krypto) | −0,23 % | −10,17 % |
| T3/SuperTrend (Krypto) | −22,20 % | −22,20 % |
| Elliott Wave (Aktien) | −1,65 % | −21,16 % |
| RSI-2 Mean-Reversion | −12,72 % | −11,17 % |
| Rendite im Fenster | +140,92 % | +74,69 % |
| **kombiniert (25/25/25/25)** | **−1,43 %** | **−9,34 %** |

**Die Vorhersage der Exposure-Messung (−9,41 %) ist bestätigt**, mit einer
Abweichung von 0,07 Punkten — und die Abweichung ist erklärt, nicht
weggerundet:

> `portfolio_correlation_analysis.py` ruft `df.sort_values("time")` auf.
> Pandas sortiert voreingestellt mit **Quicksort, nicht stabil**; Zeilen mit
> gleichem Zeitstempel werden dabei umgeordnet. Das anschliessende
> `groupby("date")["capital_after"].last()` greift deshalb nicht zwingend die
> chronologisch letzte Zeile eines Tages ab. Nur bei den Aktien-Bots relevant
> (dort teilen sich viele Trades denselben Tagesstempel).
>
> **Nachgewiesen:** Dieselbe Datei, unverändert bis auf `kind="stable"` in
> genau dieser Zeile, ergibt auf denselben neuen Kurven **exakt −9,41 %** und
> für `rsi2_mean_reversion` **−11,73 %** — beides die Werte der
> Exposure-Messung auf die letzte Stelle. Die Probe lief auf einer Kopie
> ausserhalb des Repos; die Bot-Datei ist unverändert.

`shared/portfolio_overview.py` enthält dieselbe Zeile. Der Montags-Mail-Wert
läge mit stabiler Sortierung bei **−11,41 %** statt −11,29 %. Beide Dateien
durften laut Auftrag nur aufgerufen, nicht geändert werden — siehe die offenen
Punkte unten.

### Hängt an einer dieser Zahlen eine getroffene Entscheidung?

**Nein, nach heutigem Stand nicht.** Die −1,43 % wurden bereits durch
`research/exposure_messung` (PR #84) als Risikokennzahl verworfen; eine
Parameter- oder Aktivierungsentscheidung ist auf ihnen nie getroffen worden
(Protokoll Abschnitt 8 nennt keine). Die Montags-Mail-Zahlen sind
Beobachtungswerte ohne Automatik. **Was sich ändert, ist die Grundlage
künftiger Entscheidungen** — und die Korrektur geht durchweg in die
unangenehme Richtung: die abgelegten Zahlen waren zu gut.

---

## 2. Teil 1 — der gemessene Ist-Zustand, bevor etwas überschrieben wurde

Gemessen mit `python3 shared/ergebniskurven.py` auf dem unveränderten `main`.

| Bot | Zeilen abgelegt | Zeilen heute | Rendite abgelegt | Rendite heute | MaxDD abgelegt | MaxDD heute | Einstufung |
|---|---:|---:|---:|---:|---:|---:|---|
| `elliott_wave` | 144 | 130 | +84,33 % | +67,77 % | −0,69 % | −10,17 % | **ABWEICHEND** ab Zeile 0 |
| `elliott_wave_stocks` | 469 | 395 | +1500,53 % | +352,72 % | −1,90 % | −22,44 % | **ABWEICHEND** ab Zeile 0 |
| `rsi2_crypto` | 392 | 392 | +28,37 % | +28,37 % | −13,30 % | −13,30 % | AKTUELL |
| `rsi2_mean_reversion` | 2.641 | 4.232 | +29,91 % | +36,75 % | −21,82 % | −21,05 % | **ABWEICHEND** ab Zeile 0 |
| `t3_supertrend` | 656 | 656 | +129,64 % | +129,64 % | −22,20 % | −22,20 % | AKTUELL |
| `turtle_soup_crypto` | 1.414 | 1.414 | +177,59 % | +177,59 % | −32,40 % | −32,40 % | AKTUELL |
| `turtle_soup_stocks` | 1.887 | 8.915 | +133,01 % | +145,59 % | −32,54 % | −29,91 % | **ABWEICHEND** ab Zeile 0 |
| `volatility_breakout` | 1.236 | 1.454 | +142,06 % | +224,41 % | −22,39 % | −23,97 % | **ABWEICHEND** ab Zeile 8 |
| `volatility_breakout_crypto` | 207 | 207 | +49,03 % | +49,03 % | −16,29 % | −16,29 % | AKTUELL |

Die Zeilenzahlen stimmen mit der Aufgabenstellung und mit
`research/exposure_messung/BERICHT.md` Abschnitt 7 überein — unabhängig
reproduziert, mit einem anderen Weg (`__main__`-Block statt eigener
Argumentliste).

**„Veraltet" trifft es nicht.** Bei vier der fünf laufen die Kurven schon in
der **ersten Zeile** auseinander. Das sind keine unvollständigen, sondern
falsche Dateien.

### Wann wurde jede Datei zuletzt geschrieben

| Datei | letzter Commit |
|---|---|
| acht der neun Kurven | `54e6315`, **07.09.2026** (Merge PR #22) |
| `volatility_breakout_crypto` | `3770ca7`, **09.09.2026** (PR #57, BTC-Regimefilter) |

Seither wurden **PR #23 bis #84** gemergt. Von den Commits, die `strategies/`
oder `shared/` anfassen, erklären insbesondere:

* **PR #26** (Look-Ahead im Zigzag) — beide Elliott-Bots. Die abgelegten
  Drawdowns von −0,69 % und −1,90 % waren keine Eigenschaft der Strategie,
  sondern ein Rechenfehler.
* **Die Sync-Reihe (PR #38–#59)** — `rsi2_mean_reversion` (Allokation 10 % →
  5 %, Limit 8 → 20) und `turtle_soup_stocks` (10 % → 2 %, Limit 8 →
  unbegrenzt), sichtbar daran, dass sich die **erste** Zeile nur in
  `allocation` und `capital_after` unterscheidet. Die Sync-Reihe hat den
  **Code** in Ordnung gebracht und die daneben liegenden **Ergebnisdateien**
  nicht mit erneuert.
* **PR #81** (Kurslücken im Trade-Pfad) — `volatility_breakout` läuft erst ab
  Zeile 8 auseinander.

### Gegenprobe: sind die vier „identischen" Bots es nach PR #81 noch?

**Ja, alle vier.** `rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto` und
`volatility_breakout_crypto` wurden byteweise identisch neu erzeugt —
`--erzeugen` meldet für sie „unveraendert" und schreibt die Datei gar nicht
erst an.

Das ist zugleich die wichtigste Gegenprobe der ganzen Arbeit: **die Erzeugung
trifft den Bot und nicht etwas anderes.** Ein Verfahren, das alle neun Kurven
verändert hätte, hätte nichts bewiesen.

### Wie die alten Fassungen erhalten bleiben

Über die Git-Historie, und die Erzeugung liegt in einem **eigenen, getrennten
Commit** (`0d1693e`) — kein Werkzeugcode darin, keine Kurve im
Werkzeug-Commit. `git show 317e6b9:results/equity_curve.csv` liefert jede alte
Fassung unverändert zurück.

---

## 3. Teil 3 — die Wiederholungssperre

`shared/ergebniskurven.py`, Rückgabewert **1** bei Befund, Vorbild
`shared/kursdaten.py` (PR #81).

```bash
python3 shared/ergebniskurven.py                    # prüfen
python3 shared/ergebniskurven.py --erzeugen         # neu schreiben
python3 shared/ergebniskurven.py --nur-abweichung   # nur der ernste Fall
```

### Woran sich die Prüfung festmacht — und warum

Sie **erzeugt die Kurve neu und vergleicht sie Zeile für Zeile**. Nicht die
Zeilenzahl, nicht einen Parameter-Fingerabdruck, nicht den Dateizeitstempel.

Der Grund steht im HRP-Fall selbst: dort war nicht die Zahl der Trades das
Problem, sondern ein nicht angewendeter Regimefilter — und dieser Filter ist
**kein Wert in `live_params.py`**, sondern eine Aufrufstelle im
`__main__`-Block von `volatility_breakout_crypto/equity_simulation.py`. Der
`live_params.py`-Diff von PR #57 bestand aus **einer geänderten
Kommentar-Zeilennummer**.

| Kandidat | Warum verworfen |
|---|---|
| Zeilenzahl | Der HRP-Fall kann bei gleicher Zeilenzahl auftreten. |
| Fingerabdruck über `live_params.py` | Hätte PR #57 **nicht** gesehen. |
| Fingerabdruck über den Quelltext | Hätte bei jeder Kommentaränderung gemeldet — und eine Prüfung, die grundlos anschlägt, liest bald niemand. |
| Zeitstempel der Datei | Sagt, wann geschrieben wurde, nicht ob es noch stimmt. |
| **Die Kurve selbst** | Kann weder unvollständig noch verrauscht sein. |

Preis: rund **50 Sekunden** für alle neun Bots.

### Zwei Arten von Befund

`VERALTET` (die abgelegte Kurve ist ein exakter **Anfang** der heutigen — nur
neue Kursdaten) wird von `ABWEICHEND` (schon der gemeinsame Teil läuft
auseinander, oder die abgelegte ist **länger** als der heutige Lauf) getrennt.
Dazu `FEHLT` (Bot fällt lautlos aus jeder Summe, Protokoll 4.3b Befund 2) und
`FEHLER`.

Ohne diese Trennung wäre die Prüfung wertlos: die Kursdaten wachsen täglich,
ein Cronjob ohne sie meldete **jeden Tag** und wäre binnen einer Woche nicht
mehr gelesen. `--nur-abweichung` verengt den Rückgabewert auf den ernsten Fall
und ist deshalb die Cron-Variante.

### Der Live-Betrieb wird nie blockiert

Kein Bot ruft das Werkzeug auf. Es ändert keine `live_params.py`, fasst keine
Bot-Datenbank an, sendet keine Order. **Beim Prüfen schreibt es strukturell
nicht nach `results/`**: `shared/kurven_lauf.py` lenkt `RESULTS_DIR` in einen
temporären Ordner um, und nur `--erzeugen` kopiert von dort in die Ablage.
Abschnitt 7 und 8 der Selbsttests prüfen das am echten Repo nach.

### Wie erzeugt wird

`shared/kurven_lauf.py` führt je Bot den **`__main__`-Block seiner eigenen
`equity_simulation.py`** aus (`runpy`, ein Prozess je Bot — neun gleichnamige
Module kollidieren sonst in `sys.modules`).

Bewusst der `__main__`-Block und **nicht** die einzelnen Funktionen:
`research/exposure_messung/bot_lauf.py` führt dafür eine eigene Argumentliste
je Bot — eine zweite Fassung der Frage „womit rechnet dieser Bot". Genau
daran ist der HRP-Bericht gekippt. So steht die Argumentzuordnung an genau
**einer** Stelle: in der Datei des Bots.

`shared/kursdaten.py` (PR #81) greift über `load_all_symbol_data()` aller neun
Bots — nicht ein zweites Mal im Werkzeug. Eine zweite Filterung wäre eine
zweite Wahrheit über dieselben Daten.

### Cron

Vorschlag in `shared/README_ERGEBNISKURVEN.md`, **nicht eingetragen** (die
Crontab liess sich am 12.09.2026 nicht ändern, Protokoll 9.14):

```cron
50 3 * * * cd ~/trading-bot && /usr/bin/python3 shared/ergebniskurven.py --nur-abweichung >> logs/system/ergebniskurven.log 2>&1
```

Von Hand ist der passende Zeitpunkt: **vor jeder Auswertung, die `results/`
liest**, und nach jedem Merge, der `strategies/` anfasst.

---

## 4. Tests

`python3 shared/test_ergebniskurven.py` — **44 von 44 Prüfungen bestanden.**

Der Kern ist Abschnitt 3: **derselbe Bot, dieselben Dateien, dieselbe Prüfung —
vorher grün, nach einer reinen Konfigurationsänderung rot, bei nachweislich
unveränderter Zeilenzahl.**

Beide Fallen aus #73, #77, #78, #79 und #81 sind gezielt umgangen:

1. **Die selbstbestätigende Probe.** Die veraltete Kurve wird **nie von Hand
   geschrieben**. Der Test ändert ausschliesslich die Konfiguration des Bots
   und lässt die Kurve von dessen eigenem `equity_simulation.py` erzeugen — in
   einem vollständigen, lauffähigen Klon des Repos (`shared/`, `data/`,
   `config/` verknüpft, `strategies/<bot>/` kopiert). Beobachtet wird der
   **Ablauf**, nicht ein hergestellter Zustand.
2. **Die zweite Wache verdeckt das Fehlen der ersten.** Der Kernfall ändert die
   Zeilenzahl **nicht**: das Startkapital wird verdoppelt. In
   `simulate_portfolio()` skalieren Positionsgrösse und freies Kapital beide
   linear, die Menge der ausgeführten Trades bleibt also dieselbe — gemessen
   207 vorher, 207 nachher —, während sich jede Zeile von `allocation` und
   `capital_after` ändert. Eine reine Zeilenzahl-Wache wäre hier blind.

Abschnitt 4 stellt den HRP-Fall selbst nach: der BTC-Regimefilter wird aus dem
`__main__`-Block entfernt — dieselbe Lücke, die PR #57 geschlossen hat — und
`live_params.py` bleibt dabei nachweislich unangetastet.

**Leerprobe (nachgeprüft).** Wird der Inhaltsvergleich in `vergleiche()`
entfernt und nur die Zeilenzahl verglichen, fällt Abschnitt 3 rot aus.
Abschnitt 4 bliebe **grün** — dort ändert sich die Zeilenzahl mit, ein
Zeilenzahl-Vergleich fängt ihn also ebenfalls. Genau deshalb gibt es
Abschnitt 3: er ist der einzige Prüffall, bei dem **nur** die geprüfte
Zusicherung greifen kann.

### Alle bestehenden Tests

| Bereich | Ergebnis |
|---|---|
| `broker/test_broker.py` | 163/163 |
| `broker/test_ibkr.py` | 168/168 |
| `dashboard/test_dashboard.py` | 784/784 |
| `dashboard/test_portfolio_sicht.py` | 90/90 |
| `notifications/` (2 Dateien) | alle bestanden |
| `shared/test_kursdaten.py` | 83/83 |
| `shared/test_empfehlung_format.py` | 70/70 |
| `system/` (2 Dateien) | 52/52, 117/117 |
| 15 Test-Dateien unter `research/` | alle bestanden — **bis auf eine** |

Die eine Ausnahme ist **vorbestehend und von dieser Arbeit unabhängig**:
`research/exposure_messung/test_exposure_kern.py` meldet 1 fehlgeschlagene
Prüfung („am Tag mit nur einem gültigen Kurs zählt dieser allein"). Die
Ausgabe ist **vor und nach** der Kurvenerneuerung Zeile für Zeile identisch;
Ursache ist eine pandas-Verhaltensänderung bei `pct_change`, nicht eine Kurve.

---

## 5. Was die neuen Kurven bei den drei Untersuchungen berühren

Auftragsgemäss **nicht neu gerechnet**, nur benannt.

### `research/hrp_portfolio` — **berührt, und zwar handfest**

**Die Frage, auf die es ankam, ist unproblematisch:** Hat sich
`volatility_breakout_crypto` geändert? **Nein — byteweise identisch.** Das
Vorzeichen, das dort an 0,7 % hängt, ist unangetastet. Auch die Kernaussage
des Berichts ist es: sie hängt am Vergleich `korrigiert_v2` gegen
`v2_mit_regimefilter`, und beide Grundlagen liegen eingefroren unter
`corrected_curves_v2/` bzw. `corrected_curves_v2_regimefilter/`. Der Anker
`korrigiert_v2` bestätigt im Lauf mit den neuen Kurven weiterhin alle neun
Werte.

**Aber:** `nachtrag_vbc_regimefilter.py` läuft mit den neuen Kurven nicht mehr
durch. Gemessen — mit den alten Kurven Rückgabewert **0** („27 Referenzwerte
bestätigt, 0 abweichend"), mit den neuen Rückgabewert **1** („9 Abweichungen —
der Vergleich wäre nicht belastbar. Abbruch").

Der Grund ist genau der, den Abschnitt W1 des Berichts für erledigt erklärt
hatte („Damit hängt **keiner** der drei Anker mehr an einer lebenden Datei"):
Der Anker `korrigiert_v1` ruft `analysiere(v1_kurven, cc.SWAP_PRIMARY, …)` und
biegt damit nur die **fünf abweichenden** Bots auf den eingefrorenen Ordner
`corrected_curves/` um. Die vier als synchron geltenden Bots — darunter
`elliott_wave` — liest er weiterhin **live** aus `results/`. Und
`elliott_wave` ist der Bot, dessen lebende Kurve sich gerade von 144 auf 130
Zeilen geändert hat.

Das ist kein inhaltlicher Fehler des Berichts, sondern dieselbe Bauart-Lücke
wie beim Anker `original` vor PR #64 — eine Stufe tiefer. **Der Modulabbruch
ist in diesem Sinn die Prüfung, die funktioniert**, nur an einer Stelle, die
noch nicht eingefroren war.

**Nicht behoben** (der Auftrag sagt ausdrücklich „nicht neu rechnen"). Der
naheliegende Weg wäre derselbe wie in W1: die vier synchronen Kurven als
`corrected_curves_v1_clean/` mit `MANIFEST.json` einfrieren und
`korrigiert_v1` darauf zeigen lassen. Das ist eine eigene, freizugebende
Aufgabe.

### `research/trend_overlay` — berührt, aber der Befund ist vorbestehend

`corrected_curves.py` ist dort Zeile für Zeile dieselbe Konstruktion, also
dieselbe Abhängigkeit von vier live gelesenen Kurven. Die beiden
`nachtrag_sync_korrektur*.py` scheitern dort allerdings **schon mit den alten
Kurven** (gemessen, Rückgabewert 1) — die Erneuerung ist dort nicht die
Ursache. Beide Test-Dateien (`test_corrected_curves.py`, `test_trend_core.py`)
bestehen vorher wie nachher.

### `research/order_sensitivity` — **nicht berührt**

Der Ordner liest `results/*/equity_curve.csv` an keiner Stelle:
`run_one_bot.py` rechnet alles selbst aus dem Bot-Code, alle Pfade zeigen auf
den ordnereigenen `results/`-Unterordner. `test_order_core.py` besteht
unverändert.

> **Warnung für die nächste Sitzung:** `nachtrag_sync_korrektur*.py` in
> `hrp_portfolio/` und `trend_overlay/` sind **nicht rein lesend** — sie
> schreiben beim Lauf in ihre eigenen `corrected_curves*/`-Schnappschüsse.
> Wer sie zur Diagnose startet, muss danach `git status` prüfen und
> gegebenenfalls `git checkout -- research/` aufrufen.

---

## 6. Was bewusst nicht angefasst wurde

* `live_params.py`, `forward_test.py`, `equity_simulation.py` — nur
  **aufgerufen**. Kein Diff in `strategies/`.
* `shared/portfolio_overview.py` und `dashboard/portfolio_sicht.py` — nur
  aufgerufen. Die einzige Folge ist die von `portfolio_overview.py` selbst
  geschriebene Datei `results/portfolio_overview/portfolio_overview_curve_live.csv`,
  die aus denselben Kurven abgeleitet ist und deshalb mit erneuert wurde.
* Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage.
* Die Ablage von `elliott_wave` bleibt unter `results/equity_curve.csv`. Ein
  Umzug nach `results/elliott_wave/` würde stillschweigend die Quelle wechseln,
  die `portfolio_overview.py` liest — das ist eine eigene Änderung mit eigenen
  Folgen. Das Werkzeug löst den Pfad **genauso auf** wie `portfolio_overview`
  und prüft damit garantiert dieselbe Datei.

---

## 7. Offene Punkte, die aus dieser Arbeit folgen

1. **`research/hrp_portfolio/nachtrag_vbc_regimefilter.py` bricht ab.** Der
   Anker `korrigiert_v1` liest vier Kurven live. Abhilfe: einfrieren wie in
   W1. Die Kernaussage des Berichts ist nicht betroffen. **Freizugeben.**
2. **`sort_values("time")` ist in beiden Portfolio-Rechnungen nicht stabil.**
   `portfolio_correlation_analysis.py` und `shared/portfolio_overview.py`
   verlieren dadurch bei den Aktien-Bots die Reihenfolge innerhalb eines Tages.
   Gemessene Wirkung: −9,34 % statt −9,41 % bzw. −11,29 % statt −11,41 %. Klein,
   aber es ist eine Zahl, die von der Sortierimplementierung abhängt. Ein
   `kind="stable"` je Datei würde es beheben; an `portfolio_overview.py` hängt
   die Montags-Mail, deshalb hier **nicht** angefasst.
3. **Die Montags-Mail nennt weiterhin eine Backtest-Zahl „LIVE-PORTFOLIO"**
   (Protokoll 9.15, unverändert offen). Nach dieser Arbeit ist die Zahl
   richtiger, aber die Überschrift bleibt irreführend.
4. **Die Kurven veralten weiter.** Das Werkzeug meldet es künftig — aber nur,
   wenn es läuft. Solange die Crontab klemmt (Protokoll 9.14), hängt das an
   einem Aufruf von Hand.

---

## 8. Reproduktion

```bash
cd ~/trading-bot
python3 shared/ergebniskurven.py            # erwartet: 9x AKTUELL, Rückgabewert 0
python3 shared/test_ergebniskurven.py       # erwartet: 44 von 44
python3 shared/portfolio_overview.py        # die Zahlen aus Abschnitt 1
python3 dashboard/portfolio_sicht.py --berechnen
cd strategies/rsi2_mean_reversion && python3 portfolio_correlation_analysis.py
```

Der ausführliche, autonom abarbeitbare Prüfplan steht in
`docs/TESTAUFTRAG_ergebniskurven.md`.
