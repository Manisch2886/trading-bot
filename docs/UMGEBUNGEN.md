# Umgebungen

**Wo dieses Projekt läuft, und worin sich die Orte unterscheiden.**

> ⚠️ **Grün in der Cloud heisst strukturell nicht grün auf dem Mac.** Der Mac ist
> der Rechner, auf dem der Betrieb stattfindet — er entscheidet.

*Angelegt 17.09.2026 nach TB-44. Anlass: Eine Reparatur war in der Cloud auf
fünf Python-Fassungen grün und brach auf dem Mac bei zwei von neun Bots ab. Die
Ursache — verschiedene Python-Fassungen — stand bis dahin nirgends an einer
Stelle, die eine Sitzung liest.*

---

## Die beiden Orte

| | **Mac** (`~/trading-bot`) | **Cloud** (Claude-Code-Sitzung) |
|---|---|---|
| **Rolle** | **Betrieb.** Cronjobs, Live-Datenbanken, Dashboard, Broker-Brücke | **Entwicklung.** Frischer Checkout je Sitzung, nichts davon dauerhaft |
| **Python** | **3.9.6** (`trading-env/bin/python3`; `/usr/bin/python3` ist dieselbe Fassung, hat aber weder `binance` noch `dateparser`) | **3.11 oder neuer** (zuletzt gemessen: 3.11.15) |
| **`pandas` / `numpy`** | 2.3.3 / 2.0.2 | wechselnd; fehlte zeitweise ganz, liess sich zuletzt nachinstallieren |
| **`dateparser`** | **1.2.2** | **1.4.3** |
| **Binance, yfinance** | erreichbar | ⚠️ **gesperrt (403)** — Abrufe gehören in den Mac-Testauftrag |
| **`node`** | vorhanden (`/usr/local/bin/node`) | fehlt ⇒ `dashboard/test_dashboard.py` meldet 780/780 statt 784 |
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
| ⚠️ **`datetime.fromisoformat`** | 3.11 akzeptiert **viel mehr** Schreibweisen als 3.9: `20260916T120000`, `2026-W38-3`, Nanosekunden, Dezimalkomma | ⚠️ **offen.** Betrifft `shared/entscheidungskerze.py` — **die Funktion, die alle neun Bots seit dem Umstellungstag benutzen.** Heute harmlos, weil die Kursdateien ein festes Format führen und `Z` von Hand abgefangen wird |
| **`datetime.utcnow`** | seit 3.12 verwarnt, Entfernung angekündigt | **offen**, 34 Stellen. Ein Termin, kein Fehler |
| **C-Funktion gegen Python-Funktion** | Eine Python-Funktion ist ein Deskriptor und wird im Klassenrumpf zur gebundenen Methode; eine C-Funktion nicht. **Wer eine C-Funktion ersetzt, ändert das Bindungsverhalten mit** | **behoben** in `loaderlauf.py`; ⚠️ dasselbe Muster in `system/test_log_rotation.py:599` (`os.fstat`), dort heute harmlos |
| **Mindestfassung des Projekts** | ⚠️ **steht nirgends** — kein `python_requires`, keine `sys.version_info`-Prüfung | **offen** |

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

---

## Wenn sich etwas ändert

**Diese Datei wird gepflegt, wenn sich ein Rechner ändert** — nicht wenn sich die
Arbeitsweise ändert. *Dafür ist `docs/projektfuehrung/ARBEITSWEISE.md` da.*

⚠️ **Eine Sitzung, die eine neue Fassung misst, kann sie hier nicht selbst
eintragen** — sie berichtet den Messwert, der Betreiber trägt ihn nach.
