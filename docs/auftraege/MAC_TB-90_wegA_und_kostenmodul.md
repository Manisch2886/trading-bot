# TB-90 — Weg (A) in `faltenplan.py` und das Kostenmodul: neun Importe statt neun Kopien

**Sitzungstitel:** `TB-90`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD beim Schreiben:** `563fb54`
**Vorgänger:** TB-89 (`563fb54`), TB-88 (`ec54618`), TB-87 (`afe6192`)
**Freigabe:** Betreiber, 22.09.2026 — Punkt 3 **und** die Kosten-Importe, in einem Auftrag
**Registergrundlage:** Abschnitt **38.1** (Weg A) und **38.5** (neun Importe), seit TB-89 eingetragen

⚠️⚠️ **Dieser Auftrag ändert Code, darunter einen Sperrlistenpunkt.** Die
Berechtigungsdatei sperrt `faltenplan.py` — **du wirst dort einmal nach einer
Genehmigung gefragt. Das ist gewollt und der einzige Klick, der bleiben soll.**

⛔ **Kein neues Abbild, keine Sonde anpassen, kein Vollzug von Punkt 8, kein
Registertext.** Das Abbild kommt gebündelt nach Punkt 8 (Fable 22g).

---

## 0. Der Anlass, in zwei Sätzen

**Der Bezeichner der Bestätigungsperiode ist ein Schlüssel** (TB-88 gemessen), und
Weg (A) ist der einzige, der ihn ohne Eingriff in gesperrten Code richtigstellt.
**Die Handelskosten stehen achtzehnmal im Repo**; die neun Laufkopien sollen
verschwinden, weil ein Import eine Struktur ist und eine Sonde nur eine Prüfung
(38.5).

---

## 1. Schritt 0 — der Arbeitsbaum

Im Arbeitsbaum liegen **vier Dateien vom steuernden Chat**, alle zu committen:
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md` ·
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-23b_tb72_erfuellt_es_aber.md` ·
`docs/belege/_gemeldet/TB-89.txt` (Quittung des Boten) ·
`docs/auftraege/MAC_TB-90_wegA_und_kostenmodul.md` (dieser Auftrag) ·
`docs/auftraege/AKTUELLER_AUFTRAG.md` (geändert, Zeiger).
Danach `git status --porcelain` leer.

**Dann die drei Hashes messen** (`benchmark_drawdowns.json`, `faltenplan.json`,
`benchmark_drawdowns_vt.json`) — sie müssen am Ende **gleich** sein.
⭐ **Zusätzlich vorher:** `sha256` von `research/vorregistrierung/faltenplan.py`
und ein **lesender** Sondenlauf. *Der Hash von `faltenplan.py` ÄNDERT sich in
diesem Auftrag — das ist planmässig nach 37.3 und gehört mit altem und neuem
Wert ins Ergebnisdokument.*

---

## 2. Block A ⭐⭐ — Weg (A): die letzte Falte heisst die Spanne

**Registertext 38.1, zeichengleich:**

> Der Bezeichner der Bestätigungsperiode entsteht **an der Stelle, an der die
> letzte Falte ihren Namen bekommt** … die letzte Falte **heisst** die Spanne
> `2026-01-01/2026-09-01`.

### Was zu tun ist

In `research/vorregistrierung/faltenplan.py`, Funktion **`_plan`**, in der
Schleife, die `f["rolle"]` vergibt: Die Falte mit der Rolle `bestaetigung`
bekommt ihren Namen aus ihrer eigenen Spanne —

```python
f["name"] = "%s/%s" % (f["von"], f["bis_ausschliesslich"])
```

⭐ **Beide Werte stehen schon im Dict.** `von` ist der 1. Januar, und
`bis_ausschliesslich` ist bei der letzten Falte auf den Go-Live-Schnitt gekürzt
(`_jahresfalten`, Zweig `angeschnitten`).

| | ⛔ NICHT |
|---|---|
| ⛔ | `_jahresfalten` ändern — sie bildet **alle** Namen gleich und weiss nicht, welche Falte die letzte ist |
| ⛔ | die Zeile `"bestaetigungsperiode": falten[-1]["name"] …` ändern — sie liest nur, und unter (A) liest sie das Richtige |
| ⛔ | `auswertung.py`, `beispieldaten.py`, `registerbericht.py` anfassen (38.1: *„bleiben unberührt"*) |

### Nachweise Block A

| | |
|---|---|
| **A1** | ⭐⭐ **Bei allen NEUN Bots** `plan[bot]["bestaetigungsperiode"] == "2026-01-01/2026-09-01"` — **genau die Zahl aus 35.1**, gebildet aus 21.4 und 5.2. Weicht ein Bot ab: das ist ein Befund, kein Tippfehler |
| **A2** | ⭐ **Ausgabevergleich wie TB-86:** Plan vorher und nachher je Bot, `diff` — **alle Selektionsfalten zeichengleich**, genau **ein** String verändert. Beleg je Bot |
| **A3** | `selektionsfalten` enthält **nur Kalenderjahre** (bzw. Doppeljahre bei `elliott_wave`), **keine** Spanne — 38.1, Fables Absatz *„Zu eurem Einwand"* |
| **A4** | `embargo_nach_falten` der Selektionsfalten unverändert (die Bestätigungsfalte ist die letzte, steht also in keiner Embargo-Liste) |
| **A5** | ⭐ **`test_vorregistrierung.py` mit aktiviertem `trading-env` laufen lassen, vorher und nachher.** ⚠️ **Er stürzt weiterhin ab** — `KeyError` in `zulaessigkeit`, das ist Plan-Punkt 8 und **nicht dieser Auftrag**. Zu belegen: **dieselbe** Abbruchstelle, **keine neue** und **keine frühere**. Verschiebt sich der Absturz nach vorn: ⛔ ABBRUCH |
| **A6** | ⭐⭐ **Die TB-88-Simulation wiederholen** (`docs/belege/TB-88/m4_simulation_punkt8.sh`, Wegwerf-Kopie mit getauschter Tabelle, Repo unberührt): vorher **163 bestanden / 2 gescheitert**. **Nachher darf es nicht schlechter sein.** Wird eine dritte Prüfung rot, gehört sie namentlich ins Ergebnisdokument — *das ist genau die Prüfung, die Fable unter (A) befürchtet hat* |

---

## 3. Block B ⭐⭐ — das Kostenmodul und die neun Importe

**Registertext 38.5, zeichengleich:** *„kein Laufmodul trägt eine eigene Kopie.
Die neun `backtest_*.py` ersetzen ihre Zuweisung durch den Import aus dem neuen
Modul."*

### B1 — Das neue Modul

`shared/handelskosten.py`. Es trägt **genau zwei** Konstanten und nichts weiter:

```python
TRADING_FEE_PCT = 0.1      # je Order (Einstieg und Ausstieg je einmal)
SLIPPAGE_PCT    = 0.05     # angenommene Abweichung vom gewuenschten Preis, je Order
```

⭐ **Der Modulkopf sagt, was es ist:** der eine Ort der registrierten Kosten
(Sperrlistenpunkt 9, Registertext 37.5 und 38.5), Summe je Rundlauf
`2 × (0,1 + 0,05)` = 0,30 %. ⛔ **Keine Funktion, keine Berechnung, kein Import,
kein Seiteneffekt.** *Ein Modul, das nur Werte trägt, kann nicht heimlich etwas
anderes tun.*

⛔ **Das Modul kommt NICHT auf die Sperrliste** — das ist Registertext und ein
eigener Schritt.

### B2 — Die neun Ersetzungen

In **jeder** der neun `strategies/*/backtest_*.py`: die beiden Zuweisungen
`TRADING_FEE_PCT = 0.1` und `SLIPPAGE_PCT = 0.05` **entfernen** und durch

```python
from handelskosten import TRADING_FEE_PCT, SLIPPAGE_PCT
```

ersetzen. ⭐ **Die Kommentare, die heute an den Zuweisungen hängen, gehen nicht
verloren** — sie stehen im Kopf des neuen Moduls.

⚠️⚠️ **Acht der neun haben den `sys.path`-Block schon** (`_STRATEGY_DIR`,
`_SHARED_DIR`, `sys.path.insert`). **`strategies/t3_supertrend/backtest_trend.py`
hat ihn NICHT** — dort ist er nach dem Muster der anderen acht zu ergänzen,
zeichengleich übernommen, nicht neu erfunden.

| | ⛔ NICHT |
|---|---|
| ⛔ | `forward_test.py` — Papierpfad, Live-Code, **eigene Freigabe** (38.5). Die neun Kopien dort bleiben |
| ⛔ | `research/vorregistrierung/messgroessen.py` — eingefroren; `GEBUEHR_PCT` bleibt stehen (38.5) |
| ⛔ | `equity_simulation.py`, `multi_symbol_optimise.py`, `optimise_*.py` — sie tragen **keine** Kopie, sie rufen `run_backtest` auf. Nichts zu tun |

### Nachweise Block B

| | |
|---|---|
| **B3** | `grep -c "^TRADING_FEE_PCT\|^SLIPPAGE_PCT"` über alle neun → **0**. Und `grep -c "from handelskosten import"` → **9** |
| **B4** | Je Bot: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` aus dem importierten Modul gelesen → **0.1 / 0.05**, neunmal |
| **B5** | ⭐⭐ **Mutationsprobe.** Im neuen Modul den Wert **testweise** ändern (etwa `TRADING_FEE_PCT = 0.999`), bei allen neun nachsehen, ob sie mitziehen, **danach zurücksetzen** und `git diff` prüfen, dass die Rücknahme vollständig ist. *Das beweist die Struktur: Der Wert kann im Laufmodul nicht abweichen, weil er dort nicht steht.* ⛔ **Die Probe läuft nur im Arbeitsbaum, nie in einem Commit** |
| **B6** | ⭐ **Ein Backtest je Bot, vorher und nachher, bitidentisch.** Gleiche Eingabe, gleiche Parameter; Ergebnis byte-gleich vergleichen. Geht das für einen Bot nicht (fehlende Daten, Laufzeit), **sag das** mit Grund (`A2`) statt es zu überspringen |
| **B7** | `python3 -c "import …"` je geänderte Datei: alle neun importierbar, **auch `t3_supertrend`** mit dem neuen `sys.path`-Block |

---

## 4. Block C — zwei Messungen für Fable (rein lesend)

Fable hat in 23a die Bedingung gesetzt, welche Benchmark-Tabelle vollzogen wird.
Ein Teil seiner Messbitte braucht den gerechneten Plan und ging deshalb über die
Geräteanbindung nicht (`A2`).

| | zu messen |
|---|---|
| **C1** | ⭐ **Faltenmenge je Bot in `ergebnisse/benchmark_drawdowns_tb72.json` gegen den gerechneten Plan nach 33.2** — je Bot: Menge gleich, Übermenge, Teilmenge? ⭐ TB-88 hat das Werkzeug gebaut: `docs/belege/TB-88/m5_falten_abgleich.py` |
| **C2** | **Dieselbe Messung NACH Block A.** ⚠️ *Erwartung: Die Bestätigungszeile heisst in der Tabelle weiter `2026` (bzw. `2026-2027`), im Plan aber `2026-01-01/2026-09-01`* — genau die Abweichung, die in Anfrage 23b an Fable liegt. **Nur messen und belegen, nichts daraus folgern und nichts reparieren** |
| **C3** | Dasselbe für `benchmark_drawdowns_vt.json`, damit beide Kandidaten vergleichbar belegt sind |

⛔ **Keine der drei Tabellen wird angefasst.**

---

## 5. ⛔ Abbruchkriterien

| | |
|---|---|
| ⛔ | Einer der drei JSON-Hashes ändert sich |
| ⛔ | Eine Datei in `research/vorregistrierung/ergebnisse/` entsteht oder ändert sich |
| ⛔ | `python3 faltenplan.py` wird aufgerufen (auch nicht mit `--ziel`) |
| ⛔ | Ein Bot liefert bei **A1** nicht `2026-01-01/2026-09-01` |
| ⛔ | **A2** zeigt mehr als **einen** veränderten String je Bot |
| ⛔ | **A5**: der Absturz von `test_vorregistrierung.py` verschiebt sich nach vorn oder wird ein anderer |
| ⛔ | **B5**: die Rücknahme der Mutationsprobe ist nicht vollständig |
| ⛔ | Eine Datei ausserhalb von `research/vorregistrierung/faltenplan.py`, `shared/handelskosten.py`, den neun `strategies/*/backtest_*.py` und `docs/` ist am Ende geändert |

⭐ **Abbruchkriterium heisst ABBRUCH und Meldung — nie Rückfrage.**

---

## 6. Ins Ergebnisdokument

`docs/ERGEBNIS_TB-90_wegA_und_kostenmodul.md`, Belege in `docs/belege/TB-90/`.

1. Die drei JSON-Hashes **vorher und nachher** · der Hash von `faltenplan.py`
   **vorher und nachher** (er ändert sich — planmässig nach 37.3)
2. **A1** je Bot, **A2** je Bot (der `diff`), **A3**–**A7** einzeln
3. **B3**–**B7** einzeln, die Mutationsprobe mit Ausgabe **und** dem Nachweis der
   vollständigen Rücknahme
4. **C1**–**C3** als Tabelle je Bot
5. ⭐ Der **Sondenlauf** am Ende, lesend: Er meldet jetzt einen **zweiten** Befund
   `1` (Punkt 2, zweiter Pfad `faltenplan.py`). **Das ist planmässig nach 37.3** —
   mit altem und neuem Hash als Tatsachennotiz belegen. ⛔ **Kein neues Abbild**
6. ⚠️ **Jede Abweichung** von diesem Auftrag ausdrücklich

**Danach Commit und Push**, Journalblock nach der üblichen Form.

---

## In einfacher Sprache

Zwei Änderungen am Programmcode, beide vom Verfahrensprüfer entschieden und
gestern ins Regelwerk eingetragen.

**Erstens:** Der Bestätigungszeitraum bekommt seinen richtigen Namen — die
Datumsspanne statt einer Jahreszahl. Wichtig ist, **wo** die Änderung sitzt: an
der Stelle, wo der Name entsteht, nicht dort, wo er weitergereicht wird. Dann
stimmen alle anderen Stellen von allein, und keine geschützte Datei muss
angefasst werden. Die Probe: Am Ende muss bei allen neun Bots genau die Spanne
stehen, die im Regelwerk registriert ist — und sonst darf sich **kein einziger**
anderer Name geändert haben.

**Zweitens:** Die Handelskosten stehen bisher in achtzehn Programmdateien als
Kopie. Die neun, die der grosse Lauf benutzt, bekommen ein gemeinsames kleines
Modul und lesen den Wert von dort. Danach kann er in diesen neun Dateien gar
nicht mehr abweichen, weil er dort nicht mehr steht. Bewiesen wird das mit einer
Probe: Wert im Modul verstellen, nachsehen, ob alle neun mitziehen, dann
zurücksetzen.

**Und eine Messung für den Verfahrensprüfer:** Welche der Vergleichstabellen zum
eingetragenen Zeitplan passt — vor und nach der Umbenennung. ⚠️ **Nur messen,
nichts reparieren.** Die Entscheidung darüber liegt bei ihm und ist gestellt.
