# Übergabe TB-40 — Universum-Trockenlauf

**Branch:** `claude/new-session-06epnh` · **Base:** `main` = `ab4a358`
*(Der geforderte Commit `ab4a358` ist in `origin/main` enthalten — geprüft, bevor
irgendetwas gemessen wurde.)*

---

## Die drei Antworten, in der verlangten Reihenfolge

### 1 · Die gemessene Symbolzahl je Bot und Falte gegen die eingetragene

| Bot | eingetragen | **gemessen H** *(Registertext 3b)* | gemessen F *(Faltenbeginn)* |
|---|---|---|---|
| `elliott_wave` | 6 / 13 / 13 · B 18 | **6 / 13 / 13 · B 18** ✅ | 0 / 6 / 13 · B 13 |
| `t3_supertrend` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **3 / 6 / 9 / 13 / 13 / 13 / 17 · B 18** | 0 / 3 / 6 / 9 / 13 / 13 / 13 · B 17 |
| `rsi2_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| `turtle_soup_crypto` | dieselbe | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| `volatility_breakout_crypto` | dieselbe | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| die **vier Aktien-Bots** | 140 / 142 / 145 / 147 / 148 / 148 / 149 · B 150 | **137 / 137 / 139 / 139 / 140 / 142 / 145 · B 147** | 136 / 137 / 137 / 139 / 139 / 140 / 142 · B 145 |

**Acht der neun Reihen sind falsch, alle zu hoch.** Es kommt in **keiner** Falte
eines Bots ein Symbol hinzu: F ⊆ H ⊆ eingetragene Lesart A, ausnahmslos.
`elliott_wave` stimmt unter Lesart H exakt — bei ihm ist die Notiz richtig.

### 2 · Muss die Tatsachennotiz korrigiert werden — und wie lautet die Zeile?

**Ja, acht Zeilen.** Die vollständige korrigierte Tabelle steht zum Kopieren in
`docs/ERGEBNIS_TB-40_universum_trockenlauf.md`, Abschnitt „2." — für **beide**
Lesarten, damit sie unabhängig von der Registerentscheidung bereitliegt.

Die geänderten Zeilen unter **Lesart H**:

```
| `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |
| `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `rsi2_mean_reversion` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `turtle_soup_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `volatility_breakout` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
```

⚠️ **Eingetragen ist hier nichts.** `docs/VORREGISTRIERUNG_neuselektion.md` ist
unberührt — der Nachtrag erfolgt in einem Zug mit den übrigen offenen
Registertexten, wie in der Aufgabe vorgesehen.

⚠️ **Eine zweite Tatsachennotiz desselben Abschnitts ist ebenfalls betroffen**
und war in der Aufgabe nicht genannt: **„Symbole ohne Faltenevidenz"**. Heute
zwei Listen je Markt (krypto 6, aktien 1); gemessen sind es Listen **je Bot** —
`elliott_wave` 11, `t3_supertrend` 7, die drei Krypto-Tagesbots 6 (unverändert),
die vier Aktien-Bots 5 statt 1 (`APP`, `CEG`, `GEV`, `HOOD`, `SNDK`).

### 3 · Unterschreitet ein Bot dadurch die Mindestzahl von 3 Falten?

* **Unter Lesart H: nein.** Alle neun behalten Falten mit Symbolen —
  `elliott_wave` 3 von 3, die übrigen 7 von 7. Keine leere Falte, keine
  Ein-Symbol-Falte.
* **Unter Lesart F: ja, genau einer.** `elliott_wave` verliert seine Falte
  2019–2020 (**0 Symbole**) und steht bei **2 von 3** → Regel 4c,
  „unterbestimmt", Schatten ausserhalb des Buchs. `t3_supertrend` verliert
  ebenfalls seine Falte 2019, bleibt mit 6 von 7 aber klar darüber.

**Damit ist die Registerfrage scharf:** die Wahl zwischen H und F entscheidet, ob
`elliott_wave` selektiert wird oder nicht.

---

## Die Registerfragen, die zu klären sind *(klären, nicht entscheiden)*

1. **H oder F?** Registertext 3b sagt wörtlich „an mindestens einem Handelstag
   der Falte" (H). Die Aufgabenbeschreibung TB-40 sagt „die Schranke wird am
   Faltenbeginn geprüft" (F). Beide Zahlenreihen liegen vor. **Empfehlung zur
   Kenntnis, keine Entscheidung:** H ist der Wortlaut der Festlegung, und nur bei
   H bleibt Regel 4c unangetastet.
2. **Zählt eine Falte mit null oder einem Symbol?** Unter F gibt es zwei leere
   Falten (`elliott_wave` 2019–2020, `t3_supertrend` 2019) und je eine mit zwei
   Symbolen bei den drei Krypto-Tagesbots. Unter H ist keine Falte leer — aber
   `t3_supertrend` hat 2019 nur **drei** Symbole. Ob das noch eine Falte ist,
   sagt weder 4b noch 3b. Die Festlegung sagt dazu nichts; ausgezählt ist es.
3. **`MIN_HISTORY_DAYS` je Bot:** fünf verschiedene Werte, und bei
   `elliott_wave` heisst die Schranke **`MIN_HISTORY_HOURS` = 17520** und misst
   **Kerzenzahl**, nicht Zeitspanne. Registertext 3b spricht nur von
   `MIN_HISTORY_DAYS`; der Eintrag muss beide Namen und beide Grössen nennen.

---

## Was gebaut wurde

```
research/universum_trockenlauf/
    universum_trockenlauf.py          Trockenlauf + Vergleich gegen das Register
    loaderlauf.py                     Kindprozess: ein Bot-Loader, isoliert
    test_universum_trockenlauf.py     42 Prüfungen
    BERICHT.md
docs/ERGEBNIS_TB-40_universum_trockenlauf.md
docs/TESTAUFTRAG_TB-40_universum_trockenlauf.md
docs/UEBERGABE_TB-40_universum_trockenlauf.md   (dieses Dokument)
```

**Kein bestehender Code wurde geändert.** Der Diff besteht ausschliesslich aus
neuen Dateien.

### Entwurfsentscheidung: eigenständiges Werkzeug, aufgerufen mit `--nur-universum`

Die Festlegung nennt die Option, lässt aber offen, woran sie hängt. Entschieden
ist **eigenständig unter `research/`**, weil (a) der spätere Auswerter
`research/vorregistrierung/auswertung.py` **eingefroren** ist und in dieser
Aufgabe nicht angefasst werden darf, (b) die Zahl **vor** dem Lauf gebraucht wird
und ohne Raster erzeugbar sein muss, und (c) der Auswerter in TB-30b dieses
Werkzeug aufrufen oder `messe_bot()` importieren kann, statt die Frage ein
viertes Mal zu beantworten. Ausführlich in `research/universum_trockenlauf/BERICHT.md`,
Abschnitt 2.1.

### Der gemeldete Befund zum Import

Die Aufgabe verlangt zugleich „der Laufcode entscheidet" und „Bot-Dateien werden
gelesen, nie importiert". **Beides zusammen geht nicht** —
`load_all_symbol_data()` ist eine Funktion in einem Modul. Aufgelöst: der Import
findet statt, aber **in einem eigenen Prozess je Bot**. Kollisionen in
`sys.modules` sind damit nicht vermieden, sondern unmöglich. Nichts ist
erzwungen, nichts nachgebaut.

Am Laufcode verändert wurden genau zwei Dinge, beide an der **Eingabe**:
`pandas.read_csv` liefert die Datei nur bis zum Stichtag, und
`binance.client.Client.ping` ist stillgelegt (Nebenbefund 1). Die Schranke, der
Leerlauf-Test, die Streichung unvollständiger Kerzen und das Zehnjahresfenster
laufen unverändert.

---

## Nebenbefunde

1. **Der Import von `elliott_wave` braucht Netz.** `shared/fetch_multi_data.py:46`
   legt auf Modulebene `client = Client()` an; `python-binance` pingt im
   Konstruktor `api.binance.com`. `strategies/elliott_wave/multi_symbol_optimise.py`
   holt daraus nur die Konstante `INTERVAL`. In der Cloud 403, auf dem Mac eine
   Netzrunde pro Import. Kandidat für die nächste Aufräumrunde, **kein**
   Handlungsbedarf für TB-40.
2. **Drei Bots sortieren völlig lautlos aus.** `rsi2_mean_reversion`,
   `turtle_soup_stocks` und `volatility_breakout` melden weder eine zu kurze
   Historie noch eine fehlende Kursdatei. Der auslösende Befund war nur deshalb
   sichtbar, weil `rsi2_crypto` es meldet — bei diesen dreien wäre dieselbe Sache
   unbemerkt geblieben. Gemessen, nicht gelesen (`--stille-filter`).
3. **Die Klammer hinter der Krypto-Universumsgrösse stimmt rechnerisch nicht.**
   Register 15.5: „24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)". Die Datei
   mit dem **eingetragenen Hash** `3afc95a4…` hat **25 Zeilen**, `PAXGUSDT` steht
   nicht darin, `shared/symbols_config.py` streicht nur `XAUTUSDT`. **Ergebnis 24
   richtig, Rechenweg falsch.** Der Hash ist geprüft und identisch.

---

## Randbedingungen — eingehalten und nachgewiesen

| Randbedingung | Nachweis |
|---|---|
| Keine Datei unter `data/` verändert; Datenstand `d9449faf51bffaaa…`, 223 Dateien | vor und nach dem Lauf gemessen, identisch (Selbsttest B) |
| `docs/VORREGISTRIERUNG_neuselektion.md` unberührt | nicht im Diff |
| `research/vorregistrierung/auswertung.py` eingefroren | nicht im Diff |
| Keine `live_params.py`, `forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py` verändert | nicht im Diff — nur gelesen und ausgeführt |
| `research/faltenplan_neun/` unberührt | nicht im Diff; wird nur aufgerufen |
| Die `shared/`-Module unberührt | nicht im Diff |
| Nichts unter `broker/`, keine Crontab, kein `results/*.csv` | nicht im Diff |
| Rein lesend | Schreibschutz im Kindprozess; Mutationsprobe G zeigt, dass er greift |

---

## Tests

`python3 research/universum_trockenlauf/test_universum_trockenlauf.py` →
**42/42 Prüfungen bestanden.**

**Alle 57 Testdateien des Repos**, einmal auf unverändertem `main` (Basislauf)
und einmal mit TB-40. **Dieselben zehn Dateien rot, dieselben grün** — keine
einzige Veränderung, die TB-40 zuzuschreiben wäre:

```
dashboard/test_dashboard.py                      (ohne node: 780/780 statt 784)
dashboard/test_portfolio_sicht.py                bekannt rot
research/drawdown_reihenfolge/test_drawdown.py   vorbestehend
research/elliott_wave_params/test_params.py      vorbestehend
research/exposure_messung/test_exposure_kern.py  bekannt rot
research/fib_score_stufen/test_stufen.py         vorbestehend
shared/test_drawdown_beide_masse.py              bekannt rot (Zeitüberschreitung)
shared/test_stabile_sortierung.py                bekannt rot
shared/test_wellenauswahl.py                     bekannt rot
shared/test_zuteilung.py                         vorbestehend
```

Die einzigen beiden Unterschiede zwischen den beiden Läufen:
`research/universum_trockenlauf/test_universum_trockenlauf.py` (im Basislauf gar
nicht vorhanden → jetzt **grün**) und `shared/test_drawdown_beide_masse.py`,
dessen Rückgabewert sich nur deshalb von 124 auf 1 ändert, weil ihm im zweiten
Lauf mehr Zeit gegeben wurde — rot ist er in beiden.

*In der Cloud fehlen einige Bot-Abhängigkeiten; für den Trockenlauf wurden
`pandas`, `numpy`, `python-binance`, `yfinance` und `scipy` nachinstalliert, wie
sie auf dem Mac ohnehin vorliegen. `shared/test_kursdaten.py` und
`system/test_log_rotation.py` sind hier grün, obwohl sie als „bekannt rot"
geführt werden — beide in Basis- und Nachlauf gleich.*

**Zu den Mutationsproben.** Keine Probe biegt eine Variable im laufenden Prozess
um und fragt dieselbe Variable ab; jede kopiert das Werkzeug in ein
Wegwerf-Verzeichnis, ändert dort **eine** Zeile und startet es als eigenen
Prozess — beobachtet wird der **Ablauf**. Und weil eine zweite Wache das Fehlen
der ersten verdecken kann, sind die beiden Wachen gegen das Schreiben **einzeln**
geprüft: **G** zeigt, dass der Schreibschutz allein abbricht; **H** schaltet ihn
ab, lässt denselben Defekt klaglos durchlaufen und zeigt, dass der
Datenstand-Hash **allein** ihn findet.

---

## Offen / nächste Schritte

1. **Registerentscheidung H oder F** (Betreiber).
2. **Registernachtrag** der korrigierten Tatsachennotiz — beide Tabellen liegen
   fertig vor. In einem Zug mit den übrigen offenen Registertexten.
3. **Zweite Tatsachennotiz** „Symbole ohne Faltenevidenz" mitziehen.
4. **TB-30b** bleibt Voraussetzung des Selektionslaufs (Regimewache, Agent 2,
   Umstellung von `auswertung.py` auf Verfahren B). Dort kann der Auswerter
   `messe_bot()` importieren, statt die Universumsfrage neu zu beantworten.
5. **Mac-Bestätigung** über `docs/TESTAUFTRAG_TB-40_universum_trockenlauf.md`.

---

## In einfacher Sprache

**Was wir wissen wollten.** Im Vorab-Dokument des Projekts („Register") steht,
wie viele Handelswerte in jedem Prüfzeitraum mitgerechnet werden können. Wir
wollten wissen, ob diese Zahlen stimmen — und zwar, indem wir dasselbe Programm
fragen, das später wirklich rechnet.

**Was herauskam.** Acht von neun Zahlenreihen sind zu hoch. Es fallen überall
Werte weg und nirgends kommt einer hinzu. Nur ein Bot stimmt genau.

**Warum das so ist.** Bisher hat ein Hilfsprogramm die Frage beantwortet, und es
fragt weniger streng: „Gibt es Kursdaten?" statt „Gibt es **genug** Kursdaten?".
Junge Aktien und junge Kryptowährungen bestehen die erste Frage, die zweite
nicht.

**Was das für dich heisst.** Die korrigierten Zahlen liegen fertig zum Kopieren
bereit — eingetragen werden sie später, zusammen mit den anderen offenen Punkten.
Eine Frage musst du entscheiden: Zählt ein Wert zu einem Jahr, wenn er
*irgendwann* in diesem Jahr handelbar war, oder erst, wenn er es schon am
1. Januar war? Das ist nicht kosmetisch — bei der strengeren Antwort hat ein Bot
(`elliott_wave`) zu wenige Prüfzeiträume und dürfte nicht neu eingestellt werden.
Und: Es wurde nichts verändert. Kein Kurs, kein Programm, keine Einstellung.

---

*TB-40, 16.09.2026. Kein Selektionslauf, kein signierter Tag, keine
Parameterübernahme.*
