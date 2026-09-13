# Testauftrag: beide Drawdown-Masse in `multi_symbol_optimise.py` (TB-18)

**Stand: 2026-09-13** · Gegenstand: die Änderung aus TB-18 (Schritt M1 aus
`research/drawdown_reihenfolge/BERICHT.md`). Dieses Dokument ist **eigenständig
ausführbar**: es setzt nichts voraus ausser dem Repo, Python 3 und `pandas`.

---

## 0. Worum es geht (in drei Sätzen)

`evaluate_combination_multi` weist seit TB-18 **zusätzlich** den Drawdown auf der
**chronologischen** Reihenfolge aus — Spalte `max_drawdown_chronologisch_pct`.
Der bisherige Wert (`max_drawdown_pct`, gerechnet auf der Reihenfolge der
aneinandergehängten Symbol-Blöcke), der `robustness_score` und die **Rangfolge**
bleiben unverändert; wer heute optimiert, bekommt dieselben Parameter wie gestern.

**Das ist die Zusicherung, die zu prüfen ist.** Alles andere in diesem Dokument
dient ihr.

---

## 1. Voraussetzungen

| | |
|---|---|
| Python | 3.9+ (getestet mit 3.11) |
| Pflicht | `pandas` |
| Für Abschnitt 5 zusätzlich | die CSV-Dateien in `data/` (liegen im Repo) und die Ergebnisdateien in `research/drawdown_reihenfolge/results/` (liegen im Repo) |
| Nicht nötig | `binance`, `scipy`, `node`, Netzzugang, API-Schlüssel |

Der Test ruft **keine** Kursdaten ab. Die Abruf-Module werden durch Attrappen
ersetzt, die beim Aufruf eine Ausnahme werfen — er kann also gar nicht
unbemerkt ins Netz gehen.

---

## 2. Der eine Befehl

```bash
cd <repo>
python3 shared/test_drawdown_beide_masse.py
```

**Erwartet:** `253 von 253 Pruefungen bestanden, 0 fehlgeschlagen.` und
Rückgabewert `0` (Stand 2026-09-13; die Zahl wächst, wenn Prüfungen dazukommen —
entscheidend ist die `0` hinter „fehlgeschlagen").

Laufzeit: **etwa 6–8 Minuten**, fast vollständig verursacht von einer einzigen
Gegenprobe an echten Kursdaten (`elliott_wave`, Stundenkerzen, ~3 Minuten für
eine Rasterkombination). Ohne diesen Teil:

```bash
python3 shared/test_drawdown_beide_masse.py --ohne-kursdaten   # ca. 1 Minute
```

Einzelner Bot (nützlich beim Nachstellen eines Fehlschlags):

```bash
python3 shared/test_drawdown_beide_masse.py --bot turtle_soup_stocks
```

Erlaubte Namen: `elliott_wave`, `t3_supertrend`, `rsi2_crypto`,
`turtle_soup_crypto`, `volatility_breakout_crypto`, `elliott_wave_stocks`,
`rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`.

---

## 3. Was der Test prüft — und warum so

### Abschnitt 1 — die eigentliche Zusicherung (je Bot)

Derselbe Bot bewertet **zweimal dieselbe Trade-Menge**: einmal mit den
ursprünglichen `entry_time`-Werten, einmal mit **denselben** Zeitstempeln, nur
anders auf die Zeilen verteilt. PnL, Zeilenreihenfolge und Trade-Anzahl sind in
beiden Läufen Zeile für Zeile gleich.

Das alte Mass hat `entry_time` nie gesehen. Also **muss** gelten:

* `robustness_score`, `max_drawdown_pct` und **jede** andere Spalte: identisch;
* die Rangfolge (Reihenfolge der Zeilen): identisch;
* `max_drawdown_chronologisch_pct`: **unterschiedlich** — sonst prüfte der
  Vergleich nichts.

Geprüft wird der **Ablauf** (zwei Läufe des echten Bot-Codes), nicht der Diff
und keine von Hand hingeschriebene Zahl.

### Abschnitt 2 — der neue Wert ist wirklich der chronologische

Konstruierter Fall, von Hand nachrechenbar: zwei Symbole handeln abwechselnd,
je `+10 / −6 / −6`.

| Reihenfolge | kumuliert | Drawdown |
|---|---|---|
| Symbol-Blöcke | 10, 4, −2, 8, 2, −4 | **−14** |
| chronologisch | 10, 20, 14, 8, 2, −4 | **−24** |

Der Bot muss `max_drawdown_pct = −14.0` und
`max_drawdown_chronologisch_pct = −24.0` liefern. Zusätzlich rechnet der Test
beide Werte in **reinem Python** nach (`drawdown_referenz`, ohne
`cumsum`/`cummax`) — die Gegenprobe benutzt also nicht dieselbe Kette, die sie
prüfen soll.

### Abschnitt 3 — stabile Sortierung

`sort_values("entry_time")` **ohne** `kind="stable"` liefert bei gleichen
Zeitstempeln eine beliebige Reihenfolge — und damit einen anderen Drawdown
(offener Befund N1 der Untersuchung).

Der Prüffall: **alle** Trades auf demselben Zeitstempel. Dann muss die
chronologische Sortierung die Blockreihenfolge unverändert lassen, der neue Wert
also **exakt gleich dem alten** sein. Ein zweiter Fall mischt gleiche und
verschiedene Zeitstempel und vergleicht gegen die in reinem Python gebildete
stabile Reihenfolge. Dass die Reihenfolge innerhalb der Gleichstände überhaupt
etwas ändert, weist der Test selbst nach, statt es vorauszusetzen.

### Abschnitt 4 — Mutationsproben (9 Bots × 3 Mutationen = 27 Proben)

Jede Wache wird **einzeln entfernt** — in einer Kopie unter `/tmp`, nie im Repo —
und die zugehörige Prüfung **muss** dann anschlagen:

| Mutation | erwarteter Fehlschlag |
|---|---|
| `kind="stable"` entfernt | Abschnitt 3 |
| `robustness_score` auf den chronologischen Wert umgestellt | Abschnitt 1 |
| bestehendes Mass still chronologisch sortiert (die naive Umsetzung) | Abschnitt 1 |

Das beantwortet die Frage „prüft der Test überhaupt etwas?" am Verhalten. Es
belegt zugleich, dass die Wache in **allen neun** Dateien steht: fehlte sie in
einer, liesse sich die Mutation dort nicht anwenden — der Test meldet das als
Fehler.

### Abschnitt 5 — Gegenprobe an echten Kursdaten (je Bot ein Wert)

Die Untersuchung `research/drawdown_reihenfolge/` hat ihre Raster **vor** dieser
Änderung gerechnet und abgelegt (`results/<bot>_raster.csv`, Spalten `dd_bot`,
`score_bot`, `dd_entry`). Der Test lässt den echten Bot je eine
Rasterkombination auf den echten Kursdaten rechnen und vergleicht:

* `max_drawdown_pct` gegen `dd_bot` — **der Beleg, dass der alte Wert
  derselbe geblieben ist**;
* `robustness_score` gegen `score_bot` — dito;
* `max_drawdown_chronologisch_pct` gegen `dd_entry` — der neue Wert.

Ankerwert für `elliott_wave_stocks` (dev 5 % / Stop 3 % / kein Ziel), so wie er
im Bericht steht: **−82,50 %** (Blöcke) gegen **−259,86 %** (chronologisch).

Für Kombinationen, die den **Mindestfilter** des Bots nicht bestehen, liefert
`evaluate_combination_multi` `None`. Nur dafür setzt der Test die drei
`MIN_*`-Konstanten kurz aus (und danach zurück); **gerechnet wird unverändert**.
Der Testlauf sagt in diesem Fall „Hinweis: … Mindestfilter … kurz ausgesetzt".
Betroffen ist heute nur `elliott_wave` — dieser Bot hat keine Kombination, die
seine eigenen Mindestfilter besteht.

### Abschnitt 6 — Folgenlosigkeit

`git status --porcelain` vor und nach dem Lauf muss identisch sein — beschränkt
auf `strategies/`, `results/`, `data/`, `logs/` und die Trade-Datenbanken, also
auf das, was ein Testlauf überhaupt anfassen könnte. (Ohne diese Beschränkung
schlägt die Prüfung an, sobald während des Laufs irgendwo sonst im Repo eine
Datei entsteht — etwa ein Dokument oder ein `git commit` — und behauptete damit
etwas, das sie nicht gemessen hat.) Der Test
bindet die Bot-Dateien als **Bibliothek** ein; der `__main__`-Block, der
`results/<bot>/multi_symbol_optimisation_results.csv` überschreiben würde, läuft
nie. Die gespeicherten Ergebnisdateien sind Beweismittel früherer
Entscheidungen und bleiben unangetastet.

---

## 4. Prüfung von Hand (optional, 2 Minuten)

Wer die Spalte einmal selbst sehen will, ohne eine Ergebnisdatei zu
überschreiben:

```bash
cd <repo>
python3 - <<'EOF'
import sys, types
sys.path[:0] = ["shared", "strategies/volatility_breakout_crypto"]
for n in ("fetch_binance_data", "fetch_multi_data", "fetch_stock_data", "yfinance"):
    m = types.ModuleType(n); m.INTERVAL = "1d"; sys.modules.setdefault(n, m)
b = types.ModuleType("binance"); c = types.ModuleType("binance.client")
class K:
    KLINE_INTERVAL_1HOUR = "1h"; KLINE_INTERVAL_4HOUR = "4h"; KLINE_INTERVAL_1DAY = "1d"
c.Client = K; b.client = c; sys.modules.update({"binance": b, "binance.client": c})

import multi_symbol_optimise as mo
daten = mo.load_all_symbol_data()
print(mo.evaluate_combination_multi(daten, 5.0))
EOF
```

**Erwartet** (Stand 2026-09-13): `max_drawdown_pct: -105.65`,
`robustness_score: 0.314`, `max_drawdown_chronologisch_pct: -192.97`.
Die ersten beiden Zahlen stehen so in
`research/drawdown_reihenfolge/results/volatility_breakout_crypto_raster.csv`
(`dd_bot`, `score_bot`), die dritte als `dd_entry`.

**Wichtig:** `python3 strategies/<bot>/multi_symbol_optimise.py` **nicht** zum
Prüfen aufrufen — das schreibt
`results/<bot>/multi_symbol_optimisation_results.csv` neu.

---

## 5. Die übrigen Selbsttests des Projekts

Die Änderung berührt keinen anderen Teil des Projekts; die bestehenden Tests
müssen unverändert durchlaufen:

```bash
python3 broker/test_broker.py                       # 163/163
python3 notifications/test_manual_close.py          # 118/118
python3 notifications/test_schliess_benachrichtigung.py  # 99/99
python3 shared/test_empfehlung_format.py            # 70/70
python3 shared/test_ergebniskurven.py               # 44/44
python3 shared/test_live_params_werte.py            # 69/69
python3 system/test_caffeinate_plist.py             # 53/53
python3 system/test_log_rotation.py                 # 117/117
python3 dashboard/test_dashboard.py                 # 784/784 (780 ohne `node`)
python3 dashboard/test_portfolio_sicht.py           # 90/90 (67 davon über `node`)
python3 system/test_dienst_plists.py                # Rückgabewert 2 = 0 Fehler, 4 offen
```

**Umgebungsabhängige Fehlschläge, die nichts mit dieser Änderung zu tun haben.**
In einer Umgebung ohne `node`, ohne `fastapi`, ohne `ib_async` und ohne
Zeitzonendaten schlagen `dashboard/test_dashboard.py`,
`dashboard/test_portfolio_sicht.py` (2 von 68), `broker/test_ibkr.py` und
`shared/test_kursdaten.py` bereits **auf unverändertem `main`** fehl. Wer einen
Fehlschlag beurteilen will, macht zuerst einen Basislauf auf `main` und
vergleicht.

---

## 6. Was ein Fehlschlag bedeutet

| Fehlschlag in | Bedeutung |
|---|---|
| Abschnitt 1 | **Die zentrale Zusicherung ist verletzt** — der bestehende Wert oder die Rangfolge hängt jetzt an `entry_time`. Alle früheren Scores wären unvergleichbar geworden. Nicht übernehmen. |
| Abschnitt 2 | Der neue Wert ist nicht der chronologische Drawdown. |
| Abschnitt 3 | Gleiche Zeitstempel werden nicht stabil sortiert — der Wert schwankt zwischen Läufen (Befund N1). |
| Abschnitt 4 | Der **Test** greift nicht: eine entfernte Wache blieb unbemerkt, oder die Wache fehlt in einem der neun Bots. |
| Abschnitt 5 | Zahlen weichen von der Untersuchung ab. Erst prüfen, ob sich die Kursdaten in `data/` seither geändert haben (neue Kerzen ⇒ andere Trades); dann ist es ein echter Befund. |
| Abschnitt 6 | Der Testlauf hat Dateien im Repo verändert. |
