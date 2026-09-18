# Umgebungen

**Wo dieses Projekt läuft, und worin sich die Orte unterscheiden.**

> ⚠️ **Grün in der Cloud heisst strukturell nicht grün auf dem Mac.** Der Mac ist
> der Rechner, auf dem der Betrieb stattfindet — er entscheidet.
>
> ⚠️ **Und die Cloud ist nicht EINE Umgebung, sondern eine je Sitzung.** Pakete,
> `node` und erreichbare Endpunkte wechseln. *Diese Tabelle nennt den zuletzt
> gemessenen Stand, nicht eine Zusicherung — **jede Sitzung prüft selbst und
> berichtet, was sie vorgefunden hat.*** (Ergänzt 17.09.2026 nach TB-45: der
> erste Einsatz dieses Vermerks hat selbst eine falsche Angabe erzeugt.)

*Angelegt 17.09.2026 nach TB-44. Anlass: Eine Reparatur war in der Cloud auf
fünf Python-Fassungen grün und brach auf dem Mac bei zwei von neun Bots ab. Die
Ursache — verschiedene Python-Fassungen — stand bis dahin nirgends an einer
Stelle, die eine Sitzung liest.*

---

## Die beiden Orte

| | **Mac** (`~/trading-bot`) | **Cloud** (Claude-Code-Sitzung) |
|---|---|---|
| **Rolle** | **Betrieb.** Cronjobs, Live-Datenbanken, Dashboard, Broker-Brücke | **Entwicklung.** Frischer Checkout je Sitzung, nichts davon dauerhaft |
| **Betriebssystem** | **macOS 15.7.9 (Build 24G830), Darwin 24.6.0, x86_64** *(gemessen 18.09.2026)* | *nicht gemessen* |
| **Python** | **3.9.6** (`trading-env/bin/python3`; `/usr/bin/python3` ist dieselbe Fassung, hat aber weder `binance` noch `dateparser`) | **3.11 oder neuer** (zuletzt gemessen: 3.11.15) |
| ⭐ **Welcher Interpreter in Aufgaben** | ⚠️ **immer `trading-env/bin/python3`** — er ist der Betriebsinterpreter. *Der TB-45-Auftrag schrieb an mehreren Stellen `python3` vor; dort fiel alles rot aus, was `binance` braucht (Trockenlauf D5/I0, `test_leeres_symbol` 7 rot) — ohne dass irgendetwas kaputt war.* | `python3` |
| **`pandas` / `numpy`** | 2.3.3 / 2.0.2 | ⚠️ **wechselnd** — fehlte in TB-39 ganz, liess sich in TB-43 und TB-45 nachinstallieren |
| **`dateparser`** | **1.2.2** | **1.4.3** |
| **`pandas_market_calendars`** | **4.6.1** *(an der Quelle geprüft 18.09.2026)* — Registertext 5f verweist darauf | **5.4.0** (TB-49) |
| **Binance, yfinance** | erreichbar | ⚠️ **gesperrt (403)** — Abrufe gehören in den Mac-Testauftrag |
| **`node`** | vorhanden (`/usr/local/bin/node`) — `test_dashboard.py` **784/784** | ⚠️ **wechselnd** — in älteren Sitzungen fehlend (`dashboard/test_dashboard.py` 780/780), in TB-45 **vorhanden** (784/784) |
| **`scipy`** | ⚠️ **nicht vorhanden** — `research/hrp_portfolio/test_hrp_core.py` bricht am Import ab (TB-45-Maclauf) | vorhanden |
| **`gh`, Homebrew** | ⚠️ **nicht vorhanden** — Sitzungen können keinen Pull Request anlegen | — |
| **`timeout` (GNU)** | fehlt — Testschleifen als Python-Runner nachbauen | vorhanden |
| **Kursdaten `data/`** | vollständig | vollständig (im Repo) |
| **Live-Datenbanken `*.db`** | ⚠️ **nur hier** — gitignoriert, **nicht neu berechenbar** | nicht vorhanden |
| **`logs/`, `results/<bot>`** | existieren (Cron hat sie angelegt) | fehlen im frischen Checkout |

---

## Was daraus folgt

**Der Mac-Testauftrag ist kein Anhang, sondern der Nachweis.** Er wird **vor**
dem Merge angefordert, nicht danach.

⚠️ **Dreimal an einem Tag hat der Mac etwas gefunden, das die Cloud strukturell
nicht sehen konnte:**

- **TB-40/TB-41** — Ein Schreibschutz scheiterte an einem `dateparser`-Aufrufweg,
  den die neuere Cloud-Fassung gar nicht mehr nimmt. **Das Werkzeug lief auf dem
  Mac überhaupt nicht.**
- **TB-43/TB-44** — Eine Wache brach auf Python 3.9 jeden `pathlib`-Zugriff,
  **auch lesende**, und liess in der anderen Import-Reihenfolge Schreibvorgänge
  **still durch**. Ab 3.11 gibt es die betroffene Stelle nicht mehr.
- **TB-44, B2** — Eine Prüfung sucht ihren Beleg an einer Stelle, die auf dem
  Mac leer bleibt, weil der Cron die Ordner längst angelegt hat.

---

## Bekannte Unterschiede im Verhalten

| Stelle | Unterschied | Stand |
|---|---|---|
| **`pathlib._NormalAccessor`** | gibt es bis 3.10, ab 3.11 nicht mehr; auf 3.10 steht dort `io.open`, auf 3.9 `os.open` | **behoben** (TB-44) — die Wachen kommen ohne Fallunterscheidung aus |
| **`datetime.fromisoformat`** | ⚠️ **acht** Schreibweisen gehen auf 3.11 durch und scheitern auf 3.9 — von vierzehn geprüften: `Z`-Suffix, `20260916T000000`, `20260916`, `2026-W38-3`, **`2026-260` (Ordinaldatum)**, **`24:00`**, Nanosekunden, Dezimalkomma. *Die Cloud nannte sechs; der Mac-Katalog ist breiter* | **gemessen (TB-45, auf 3.9.6 selbst), kein Handlungsdruck.** In `shared/entscheidungskerze.py`, aber nur im **Aktien**-Pfad — **vier von neun** Bots; der Krypto-Pfad erreicht die Stelle nie. ⭐ **Es kommt genau ein Wert an, vom Code selbst gebaut** (`f"{tag}T00:00:00"` aus dem NYSE-Kalender); die Zeitstempel der Kursdateien liest `pandas` und kommen dort **nicht** vorbei. Das `Z`-Suffix wird vorher von Hand abgefangen. **Fiele es doch aus: kein stiller Rückfall, keine falsche Kerze, kein Abbruch** — ⭐ **auf dem Mac gemessen:** der Bot läuft durch, schreibt **je Symbol eine Fehlerzeile** (3 Symbole → 3 Zeilen) und hat **null offene Positionen**; der Krypto-Pfad läuft unberührt weiter |
| **`datetime.utcnow`** | seit 3.12 verwarnt, Entfernung angekündigt | **offen**, 34 Stellen. Ein Termin, kein Fehler |
| **C-Funktion gegen Python-Funktion** | Eine Python-Funktion ist ein Deskriptor und wird im Klassenrumpf zur gebundenen Methode; eine C-Funktion nicht. **Wer eine C-Funktion ersetzt, ändert das Bindungsverhalten mit** | **behoben** in `loaderlauf.py`. ✅ **Entwarnung (TB-45-Maclauf):** `os.fstat` ist auf 3.9.6 ein `builtin_function_or_method` und steht in **keinem** Klassenrumpf — die frühere ⚠️-Markierung zu `system/test_log_rotation.py:599` ist gegenstandslos |
| **Mindestfassung des Projekts** | ⚠️ **steht nirgends** — kein `python_requires`, keine `sys.version_info`-Prüfung | **offen** |

---

## Was ein Basislauf auf dem Mac nicht erreicht

*Gemessen im TB-45-Maclauf. Wer „alle Tests grün" schreibt, meint diese nicht.*

| Stelle | Warum |
|---|---|
| `research/drawdown_reihenfolge/test_drawdown.py` · `research/fib_score_stufen/test_stufen.py` · `research/elliott_wave_params/test_params.py` | ⚠️ **verlangen ein Bot-Argument** — ohne Argument nur die Nutzungszeile und `rc=1`. **Sie sind ungeprüft, nicht rot** |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt auf dem Mac |
| `shared/test_drawdown_beide_masse.py` | ⚠️ **läuft in die Zeitgrenze** (900 s) und **hinterlässt einen Kindprozess**, der weiterrechnet — im TB-45-Lauf rund 20 Minuten CPU, bis er von Hand beendet wurde |
| `trading-env/` | im `find` **ausschliessen** — sonst 1 312 statt 65 Testdateien *(65 gemessen 18.09.2026 im TB-49-Maclauf; die 62 stammte aus TB-45)* |
| GNU `timeout` | fehlt — Ersatz: `perl -e 'alarm 900'` (`rc=142` = Zeitgrenze) |

**Bekannt rot auf dem Mac, nicht durch einen Zweig verursacht:**
`shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) —
beide teils wegen **veralteter abgelegter Ergebniskurven**;
`system/test_log_rotation.py` — grün im Regelfall, zeitabhängig flackernd — auf
dem Mac 3 von 10 Läufen rot (gemessen 18.09.2026, TB-49). Eine Einzelmessung
belegt hier nichts, siehe `docs/PRUEFPRINZIPIEN.md` A6 ·
`research/exposure_messung/test_exposure_kern.py` (1) ·
`dashboard/test_portfolio_sicht.py` (1 — hier liegen die Live-Datenbanken).

---

## Regel für Aufgabendokumente

**Die Umgebungshinweise jeder Aufgabe nennen:**

1. **Beide Python-Fassungen**, wenn die Aufgabe Standardbibliothek oder
   Fremdpakete anfasst.
2. **Was in der Cloud nicht prüfbar ist** — und dass der Mac-Testauftrag genau
   das nachholt.
3. **Die bekannt roten Tests**, ⚠️ **mit dem Vermerk, auf welchem Rechner sie rot
   sind.** *Mehrere Listen waren falsch, weil sie unbesehen aus einer Umgebung in
   die andere übernommen wurden.*
4. ⚠️ **Und die Bitte, Abweichungen von dieser Datei zu MELDEN.** *Die Liste
   altert; eine Sitzung, die sie stillschweigend für falsch hält, hilft
   niemandem. Korrekturen aus TB-45: `node` und
   `dashboard/test_portfolio_sicht.py`.*

---

## Wenn sich etwas ändert

**Diese Datei wird gepflegt, wenn sich ein Rechner ändert** — nicht wenn sich die
Arbeitsweise ändert. *Dafür ist `docs/projektfuehrung/ARBEITSWEISE.md` da.*

⚠️ **Eine Sitzung, die eine neue Fassung misst, kann sie hier nicht selbst
eintragen** — sie berichtet den Messwert, der Betreiber trägt ihn nach.
