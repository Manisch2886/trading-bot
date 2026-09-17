# Ausstiegspfade bei fehlenden Kursdaten — Bericht

**TB-46b, 17.09.2026.** Vorgänger: TB-45 (Messung), TB-46 (`135c306`).
Werkzeug: [`probe.py`](probe.py) · Rohdaten: [`ergebnisse/probe.json`](ergebnisse/probe.json)

---

## Die Frage

TB-45 hat gemessen, was ein Bot tut, der seine Entscheidungskerze nicht
bestimmen kann: Er läuft durch, schreibt je Symbol eine Fehlerzeile, und am
Ende steht *„Offene Papier-Positionen: 0"*.

Diese Zahl hat zwei Lesarten, und an der Bildschirmausgabe sind sie nicht zu
unterscheiden:

| | |
|---|---|
| **(a)** | Der Bot eröffnet keine **neuen** Positionen — harmlos. |
| **(b)** | Der Bot **schliesst** offene, weil er sie ohne Kerze nicht bewerten kann — dann macht ein Parsing-Fehler einen Trade. |

Sichtbar wird der Unterschied nur am **Zustand der Datenbank vorher und
nachher**. Genau das misst diese Untersuchung.

---

## Die Antwort

> **Nein.** Bei **keinem** der neun Bots schliessen fehlende Kursdaten eine
> offene Position. Es ist Lesart (a).

**Aber** — und das ist der Befund, der ohne die Probe nicht aufgefallen wäre:

> Ein **veralteter** Kursrahmen, der aus der **zweiten** Quelle kommt (dem
> Live-Abruf), wird **ohne Frischeprüfung** verwendet. Alle neun Bots
> entscheiden dann auf Kerzen, die beliebig alt sein dürfen. Gemessen:
> ein Stop-Loss, gebucht auf einem Kurs von vor **6,85 bis 7,85 Tagen**.

Die tragende Stelle ist eine einzige, und sie ist gemeinsam:
`shared/entscheidungskerze.py`, `lade()`, Zeile 658–671. Für `data/` wird
`ist_frisch()` gefragt; für das Ergebnis von `abruf()` wird es **nicht**
gefragt.

---

## Aufbau der Probe

* **Ein Wegwerf-Verzeichnis je Bot**, ausserhalb des Arbeitsbaums, mit einer
  Teilkopie des Projekts. Weil `strategy_paths.get_strategy_paths()` die
  Datenbank aus dem Wurzelverzeichnis ableitet, zeigen Datenbank, Kursordner
  und Protokolle damit alle in die Kopie. **Keine echte `*.db` wird
  angefasst.**
* **Ein eigener Prozess je Bot** (TB-40). Bot-Dateien werden gelesen und
  ausgeführt, nie importiert.
* **Das Schema kommt per Syntaxbaum aus `init_db()`** der jeweiligen
  `forward_test.py` — gelesen, nicht geraten.
* **Gemessen wird die Datenbank**, Zeile für Zeile, vorher und nachher.
  Zusätzlich der sha256 der Datei.
* **Am Bot wird nichts geändert.** Die Probe weist je Lauf mit sha256 nach,
  dass `forward_test.py`, `live_params.py`, `indicators.py` und die
  gemeinsamen `shared/`-Module byteweise dem Repo entsprechen (Feld
  `bot_dateien_unveraendert`, 18–26 Dateien je Bot, alle `true`).
  Ausgetauscht wird ausschliesslich die **Gegenstelle**: an
  `fetch_binance_data.py` bzw. `fetch_stock_data.py` wird ein Block
  angehängt, der `fetch_historical_data` neu belegt. Ohne ihn wäre jede Lage
  dieselbe Lage — „Abruf gescheitert" —, weil Binance und yfinance aus der
  Cloud gesperrt sind (403).

### Zwei Positionen, nicht eine

| | Stop | Zweck |
|---|---|---|
| **P1** | unerreichbar tief | **muss in jeder Lage offen bleiben** |
| **P2** | genau auf dem Einstiegskurs | **muss in Lage D schliessen** |

P2 ist die Gegenprobe, ohne die die Probe nichts misst: Bliebe in Lage A
alles unverändert, weil der Bot gar nicht erst bis zur Positionsprüfung
kommt, sähe das genauso aus wie „der Bot hat richtig entschieden". P2 zeigt,
dass er die Stelle erreicht **und** schliessen kann.

### Die fünf Lagen

| | Kursdatei | Live-Abruf |
|---|---|---|
| **A** | fehlt ganz | scheitert |
| **B** | vorhanden, **leerer** Rahmen | liefert einen leeren Rahmen |
| **C1** | vorhanden, **veraltet** | scheitert |
| **C2** | vorhanden, **veraltet** | liefert denselben veralteten Rahmen |
| **D** | in Ordnung | wird nicht gerufen |

⚠️ **C2 steht nicht im Auftrag und ist trotzdem nötig.** Der Auftrag fragt
nach einem Pfad, „auf dem ein ALTER Kurs verwendet wird". Mit C1 allein ist
das nicht zu beantworten: `lade()` **verwirft** eine veraltete `data/`-Datei
vollständig und ruft `abruf()`. Ein veralteter Rahmen aus `data/` erreicht den
Bot also nie. Erreichbar ist er nur über die zweite Quelle — und genau die
wird nicht auf Frische geprüft.

---

## Ergebnis, alle neun Bots

| Lage | offene Positionen vorher → nachher | Datenbank |
|---|---|---|
| **A** | 2 → 2 | **byteweise unverändert** (sha256 gleich) |
| **B** | 2 → 2 | **byteweise unverändert** |
| **C1** | 2 → 2 | **byteweise unverändert** |
| **C2** | 2 → 1 | P2 geschlossen, **Ausstiegskurs 6,85–7,85 Tage alt** |
| **D** | 2 → 1 | P2 geschlossen (Kontrolle greift), P1 offen |

Neunmal dasselbe Bild, ohne eine einzige Abweichung. Rückgabewert 0 in
allen 45 Läufen; die Zeile „Prüfe offene Positionen…" und die
Zusammenfassung wurden in **allen** Lagen erreicht.

---

## Wie die Bots ein leeres Symbol auslassen — drei verschiedene Wege

Gemessen in Lage B, an den Zeilen, die der Lauf zu dem Symbol geschrieben hat:

| Weg | Bots | Zeile im Protokoll |
|---|---|---|
| **gemeldet** (`Ladeprotokoll`) | `elliott_wave`, `elliott_wave_stocks` | `Hinweis: BTCUSDT hat keinen Kursrahmen geliefert (data/ und Live-Abruf), wird uebersprungen.` |
| **gemeldet, aber aus Versehen** | `t3_supertrend` | `Fehler bei BTCUSDT: index 0 is out of bounds for axis 0 with size 0` |
| ⚠️ **still** | die übrigen **sechs** | *(keine Zeile)* |

`t3_supertrend` hat als einziger Bot **keine** `if df.empty`-Prüfung in der
Ladeschleife (Zeile 212). Geschützt ist er trotzdem — aber durch einen
`IndexError` aus `compute_indicators`, den das breite `except Exception`
eine Zeile später einfängt (Zeile 216/217). Die Meldung, die dabei entsteht,
nennt einen Array-Index statt einer fehlenden Kursquelle.

Bei den sechs übrigen steht `if df.empty: continue` **ohne Meldung** — der
stille Ausfall aus TB-40/TB-42, im Papierpfad noch vorhanden.

Und: `elliott_wave`/`elliott_wave_stocks` legen zwar ein `Ladeprotokoll` an,
rufen aber **nie `_prot.melde(price_data)`**. Die Summenzeile („Geladen: n von
m Symbolen"), die die Frage *„hat dieser Lauf überhaupt vollständig
geladen?"* ohne Zählen beantwortet, steht im Papierpfad also bei **keinem**
der neun Bots.

---

## Nebenbefund

`strategies/elliott_wave/forward_test.py`, Zeile 129:

```python
if row["high"] >= trade["target_price"]:
```

Ohne None-Absicherung. Ein Trade mit `target_price = NULL` bringt
`check_open_trades` mit einem `TypeError` zu Fall — und zwar **ausserhalb**
des `try` der Ladeschleife, also den ganzen Lauf. Der Bot selbst schreibt
immer beide Werte, der Fall kann aus eigener Kraft nicht entstehen. Er ist
hier aufgefallen, weil die erste Fassung der Probe `NULL` gesetzt hatte.
Festgehalten, nicht repariert: `forward_test.py` ist für TB-46b gesperrt.

---

## Was diese Untersuchung nicht getan hat

* Keinen Bot gegen eine echte Datenbank laufen lassen.
* Nichts unter `data/` verändert (Datenstand vorher und nachher identisch).
* Keine Zeile in `forward_test.py`, `live_params.py`, `equity_simulation.py`,
  `shared/entscheidungskerze.py` oder `shared/paths.py` geändert.
* Keinen Trade ausgelöst, keinen Broker-Endpunkt berührt, nichts abgerufen.
