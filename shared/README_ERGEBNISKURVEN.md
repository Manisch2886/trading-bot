# Ergebniskurven — erzeugen und aktuell halten

`shared/ergebniskurven.py` hält die abgelegten `results/*/equity_curve.csv`
gegen die heutige Konfiguration und erzeugt sie auf Wunsch neu.

**Warum das nötig ist.** Diese Dateien sind keine Ablage, sondern eine
Aussage. Sie füllen laut Übergabeprotokoll 4.3b die **Montags-Mail**
(`shared/portfolio_overview.py`) und die **Dashboard-Portfolio-Sicht**
(`dashboard/portfolio_sicht.py`), solange ein Bot unter
`MIN_LIVE_CLOSED_TRADES = 10` geschlossenen Live-Trades liegt — und das tun
derzeit alle neun. Sie sind ausserdem die Grundlage praktisch jeder
Untersuchung unter `research/`.

Geschrieben werden sie nur, wenn jemand `python3 equity_simulation.py` von
Hand aufruft. Ändert sich in der Zwischenzeit ein Parameter, ein Filter oder
der Datenpfad, beschreibt die Datei ab diesem Moment einen Bot, den es nicht
mehr gibt — und **nichts sagt es**. Genau das ist dreimal passiert
(`hrp_portfolio` zweimal, `volatility_scaled_sizing`, `exposure_messung`).

---

## Benutzung

```bash
python3 shared/ergebniskurven.py                    # prüfen, Rückgabewert 1 bei Befund
python3 shared/ergebniskurven.py --erzeugen         # alle neun Kurven neu schreiben
python3 shared/ergebniskurven.py --bot t3_supertrend
python3 shared/ergebniskurven.py --nur-abweichung   # nur der ernste Fall zählt
python3 shared/ergebniskurven.py --json bericht.json
python3 shared/test_ergebniskurven.py               # Selbsttests (44 Prüfungen)
```

Ein vollständiger Durchlauf über alle neun Bots dauert rund **50 Sekunden**
(je ein Prozess). Das Programm hat keinen Zustand und ist beliebig oft
wiederholbar; zwei Läufe erzeugen byteweise dieselbe Datei.

### Cron-Zeile — Vorschlag, **nicht eingetragen**

```cron
50 3 * * * cd ~/trading-bot && /usr/bin/python3 shared/ergebniskurven.py --nur-abweichung >> logs/system/ergebniskurven.log 2>&1
```

Einmal täglich um 3:50 Uhr, also nach der Log-Rotation (3:30) und nach der
Portfolio-Sicht (3:40), und mit deutlichem Abstand zu den 4-Stunden-Läufen der
Bots. `--nur-abweichung` ist für den Cronjob die richtige Wahl: die Kursdaten
wachsen täglich, eine bloss verlängerte Kurve ist deshalb Alltag und kein
Alarm. Ohne diesen Schalter meldete der Cronjob **jeden Tag** etwas und wäre
binnen einer Woche nicht mehr gelesen.

Den Ordner vorher anlegen: `mkdir -p logs/system`.

> **Hinweis:** Die Crontab des Nutzers liess sich am 12.09.2026 nicht ändern
> (`crontab -` scheitert mit `Operation not permitted`, macOS-Berechtigung nach
> einem Update zurückgesetzt). Das Werkzeug ist deshalb bewusst auch **von Hand
> sinnvoll aufrufbar** — es hat keinen Zustand und braucht kein Intervall. Der
> passende Zeitpunkt von Hand ist: **vor jeder Auswertung, die `results/` liest**
> (also vor jeder neuen Untersuchung unter `research/`) und nach jedem Merge,
> der `strategies/` anfasst.

---

## Was die Prüfung vergleicht — und warum

Sie **erzeugt die Kurve neu und vergleicht sie Zeile für Zeile** mit der
abgelegten. Nicht die Zeilenzahl, nicht einen Parameter-Fingerabdruck, nicht
den Zeitstempel der Datei.

Der Grund steht im HRP-Fall. Dort war nicht die Zahl der Trades das Problem,
sondern ein **nicht angewendeter Regimefilter** — und dieser Filter ist kein
Wert in `live_params.py`, sondern eine **Aufrufstelle im `__main__`-Block** von
`volatility_breakout_crypto/equity_simulation.py` (PR #57; dort ausdrücklich so
platziert, weil drei Experiment-Skripte dieses Bots über `collect_all_trades()`
ihren *ungefilterten* Vergleichsdatensatz holen). Der `live_params.py`-Diff
jenes PRs bestand aus **einer geänderten Kommentar-Zeilennummer**.

Daraus folgt die Wahl:

| Kandidat | Warum verworfen |
|---|---|
| Zeilenzahl | Der HRP-Fall kann bei gleicher Zeilenzahl auftreten. Genau das prüft Abschnitt 3 der Selbsttests nach. |
| Fingerabdruck über `live_params.py` | Hätte PR #57 **nicht** gesehen — dort änderte sich kein Wert. |
| Fingerabdruck über den Quelltext | Hätte bei jeder Kommentaränderung gemeldet. Eine Prüfung, die grundlos anschlägt, liest bald niemand mehr. |
| Zeitstempel der Datei | Sagt, wann geschrieben wurde, nicht ob es noch stimmt. |
| **Die Kurve selbst** | Kann weder unvollständig noch verrauscht sein: sie *ist* das, worauf sich Mail, Dashboard und Berichte berufen. |

Der Preis ist Rechenzeit. Für eine nächtliche Prüfung ist das unerheblich.

### Zwei Arten von Befund

| Marke | Bedeutung | Was zu tun ist |
|---|---|---|
| `AKTUELL` | Zeile für Zeile identisch | nichts |
| `VERALTET` | Die abgelegte Kurve ist ein **exakter Anfang** der heutigen; es sind nur neue Kursdaten dazugekommen. Unvollständig, aber nicht falsch. | bei Gelegenheit `--erzeugen` |
| `ABWEICHEND` | Schon im gemeinsamen Teil laufen die Kurven auseinander, **oder** die abgelegte ist länger als der heutige Lauf. Sie beschreibt einen anderen Bot. | `--erzeugen`, **und** jede Zahl prüfen, die aus ihr abgeleitet wurde |
| `FEHLT` | Keine abgelegte Kurve. Ein solcher Bot fällt in `portfolio_overview.load_all_curves()` lautlos aus jeder Summe (Protokoll 4.3b, Befund 2). | `--erzeugen` |
| `FEHLER` | Der Lauf selbst ist gescheitert. | Meldung lesen — meist fehlen Kursdaten. |

Ohne die Trennung `VERALTET`/`ABWEICHEND` wäre die Prüfung wertlos: die
Kursdaten wachsen täglich.

---

## Was das Werkzeug nie tut

* **Es blockiert nichts.** Kein Bot ruft es auf. Es fährt nichts herunter,
  ändert keine `live_params.py`, fasst keine Bot-Datenbank an, sendet keine
  Order. Der Rückgabewert 1 ist für den Cronjob da, nicht für den Live-Betrieb.
* **Beim Prüfen schreibt es nicht nach `results/`.** Das ist strukturell
  abgesichert, nicht versprochen: `shared/kurven_lauf.py` lenkt `RESULTS_DIR`
  in einen temporären Ordner um, und nur `--erzeugen` kopiert von dort in die
  Ablage. Abschnitt 7 und 8 der Selbsttests prüfen das nach.
* **Es fasst keinen Bot-Code an.** `live_params.py`, `forward_test.py` und
  `equity_simulation.py` werden ausschliesslich **aufgerufen**.

---

## Wie die Kurve erzeugt wird

`shared/kurven_lauf.py` führt je Bot den **`__main__`-Block seiner eigenen
`equity_simulation.py`** aus (`runpy.run_path(..., run_name="__main__")`), in
einem eigenen Prozess — neun gleichnamige `equity_simulation.py` kollidieren
sonst in `sys.modules` und schieben einem Bot lautlos die Funktionen eines
anderen unter.

**Warum der `__main__`-Block und nicht die einzelnen Funktionen:**
`research/exposure_messung/bot_lauf.py` ruft `collect_all_trades()` je Bot mit
einer dort hinterlegten Argumentliste auf. Das funktioniert, führt aber eine
zweite Fassung der Frage „womit rechnet dieser Bot eigentlich" ein — genau die
Doppelführung, an der dieses Projekt schon mehrfach auseinandergelaufen ist
(Protokoll 4.2, Prinzip 7.11). Der BTC-Regimefilter oben ist der Beleg: wer
die Funktionen einzeln aufruft, muss ihn von Hand nachbilden. So steht die
Argumentzuordnung an genau **einer** Stelle, nämlich in der Datei des Bots.

**Unvollständige Kursbalken** hält `shared/kursdaten.py` fern — nicht von hier
aus, sondern dort, wo die Daten ins Programm kommen: alle neun
`multi_symbol_optimise.load_all_symbol_data()` rufen seit PR #81
`entferne_unvollstaendige()` auf, und das ist der Weg, über den jeder
`__main__`-Block seine Daten holt. Eine zweite Filterung hier wäre eine zweite
Wahrheit über dieselben Daten.

**Der Krypto-Elliott-Wave-Bot** legt seine Kurve historisch unter
`results/equity_curve.csv` ab statt unter `results/elliott_wave/`. Das Werkzeug
löst den Pfad **genauso auf wie `shared/portfolio_overview.py`** (Standardpfad
gewinnt, wenn es ihn gibt; sonst der historische) und prüft damit genau die
Datei, die Montags-Mail und Dashboard auch lesen. Die Ablage wird hier bewusst
**nicht** umgezogen — das wäre eine eigene Änderung mit eigenen Folgen.

---

## Selbsttests

```bash
python3 shared/test_ergebniskurven.py     # 44 Prüfungen
```

Der Kern ist Abschnitt 3: derselbe Bot, dieselben Dateien, dieselbe Prüfung —
vorher grün, nach einer reinen **Konfigurationsänderung** rot, **bei
unveränderter Zeilenzahl**. Die veraltete Kurve wird dabei nie von Hand
geschrieben; sie entsteht immer aus dem `equity_simulation.py` des Bots in
einem vollständigen, lauffähigen Klon des Repos.

Abschnitt 4 stellt den HRP-Fall selbst nach: der BTC-Regimefilter wird aus dem
`__main__`-Block entfernt — dieselbe Lücke, die PR #57 geschlossen hat — und
`live_params.py` bleibt dabei nachweislich unangetastet.

**Leerprobe (nachgeprüft am 12.09.2026):** Wird der Inhaltsvergleich in
`vergleiche()` entfernt und nur die Zeilenzahl verglichen, fällt Abschnitt 3
rot aus. Abschnitt 4 bliebe grün — dort ändert sich die Zeilenzahl mit, ein
Zeilenzahl-Vergleich fängt ihn also ebenfalls. Genau deshalb gibt es
Abschnitt 3: er ist der einzige Prüffall, bei dem **nur** die geprüfte
Zusicherung greifen kann.
