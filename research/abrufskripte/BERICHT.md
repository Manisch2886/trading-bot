# Abrufwege — wer hängt an `shared/fetch_binance_data.py`?

**Untersuchung aus TB-35. Stand 2026-09-15. Rein lesend, ändert nichts.**

Werkzeug: `research/abrufskripte/abrufwege.py` (nur Standardbibliothek,
Rückgabewert 0 — ein Bericht, kein Wächter).

```
python3 research/abrufskripte/abrufwege.py
python3 research/abrufskripte/abrufwege.py --json daten/abrufwege.json
```

---

## 1. Warum das überhaupt untersucht wurde

`shared/fetch_binance_data.py` ist **gitignoriert**. Sie enthält Zugangsdaten
und liegt nur auf dem Rechner des Betreibers. TB-34 konnte sie nicht lesen und
hat ihr Verhalten ausschliesslich am Ergebnis erschlossen; TB-35 konnte sie
ebenfalls nicht lesen und hat sie **nicht nachgebaut**.

Die Aufgabe verlangte deshalb, mechanisch festzustellen, *wer* an ihr hängt —
über den Syntaxbaum, nicht über eine Liste von Hand. Eine Liste von Hand wäre
am Tag nach der nächsten Änderung falsch, ohne dass es auffiele. Dasselbe
Vorgehen wie in `research/kursdaten_neuaufbau/datenwege.py`.

---

## 2. Das Ergebnis

**Neun Module binden sie ein.** Sie zerfallen in zwei Gruppen, und der
Unterschied zwischen ihnen ist der Unterschied zwischen *„eine CSV ist
falsch"* und *„ein Bot handelt falsch"*:

| Gruppe | Module | Was ein Fehler dort anrichtet |
|---|---|---|
| **schreiben nach `data/`** | `shared/fetch_multi_data.py`, `strategies/t3_supertrend/fetch_4h_data.py`, `strategies/rsi2_crypto/fetch_1d_data.py`, `strategies/volatility_breakout_crypto/fetch_1d_data.py` | landet **dauerhaft** in einer Kursdatei und in jeder Auswertung, die sie liest |
| **lassen eine Handelsentscheidung davon abhängen** | die fünf Krypto-`forward_test.py` (`elliott_wave`, `rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto`) | wirkt **sofort** auf den Paper-Trading-Bestand |

Die vier Abrufskripte der ersten Gruppe sind die, die TB-35 geändert hat. Die
fünf `forward_test.py` sind **nicht angefasst worden** — sie stehen auf der
Sperrliste der Aufgabe. Was dort auffiel, steht unten unter Punkt 4.

---

## 3. Die Zusicherungen, die an dieser Datei hängen

Keine davon ist im Repo nachprüfbar. Alle sind aus dem Verhalten der Aufrufer
und aus den entstandenen Kursdateien erschlossen:

| Zusicherung | Woran sie hängt |
|---|---|
| **Spalten** | `open_time/open/high/low/close/volume` — und **keine** `close_time`. Nachgerechnet an den Kursdateien selbst (`head -1 data/BTCUSDT_1h.csv`), nicht an der Quelle. |
| **Reihenfolge** | aufsteigend nach `open_time`. Jeder Aufrufer, der `df.iloc[-1]` als „die jüngste Kerze" liest, setzt das voraus — fünf tun das. |
| **Raster** | die `open_time`-Werte liegen auf dem Raster des angefragten Intervalls, ohne Doppelungen. `shared/zeitabdeckung.py` prüft das an den **fertigen Dateien** nach, nicht an der Antwort. |
| **Schreibweise** | `YYYY-MM-DD HH:MM:SS`, bei Tageskerzen `YYYY-MM-DD`. Ändert sie sich, ändert sich der Datenstand-Hash, ohne dass ein Kurs anders wäre. |
| **Vollständigkeit** | `LOOKBACK` wird als „ab diesem Zeitpunkt" gelesen und liefert alles Vorhandene, auch über die 1000-Kerzen-Grenze des Endpunkts hinaus. |
| **Laufende Kerze** | sie **ist** im Ergebnis enthalten. Genau dieser Befund hat TB-35 ausgelöst — erschlossen aus den Dateien, nicht aus der Quelle. |

**Die fehlende `close_time` ist der Grund für eine Entwurfsentscheidung in
`shared/abrufschutz.py`:** `shared/kursdaten_neuaufbau.py` liest die rohen
Kerzenfelder des Endpunkts und kann `close_time` (Feld 6) unmittelbar
auswerten. Die Abrufskripte sehen nur noch den fertigen DataFrame — dort gibt
es das Feld nicht. `abrufschutz` rechnet den Schluss deshalb aus `open_time`
und der Intervalllänge, mit **derselben Formel** wie der Neuaufbau
(`schluss = öffnung + länge − 1`, behalten bei `schluss <= Stand`).

---

## 4. Die Frage, die hier berichtet und **nicht entschieden** wird

**a) Ein zentrales Abrufmodul, das nirgends versioniert ist, existiert genau
einmal — auf einem MacBook.** Das ist dieselbe Klasse von Risiko wie G1: neun
Module hängen daran, fünf davon im täglichen Betrieb. Geht der Rechner
verloren, ist der einzige Weg zu Krypto-Kursdaten weg, und niemand kann ihn
aus dem Repo wiederherstellen.

Enthält die Datei Zugangsdaten — was sich mit `grep -c` feststellen lässt,
**ohne den Inhalt anzuzeigen** (Schritt 1 des Testdokuments) —, ist der
richtige Weg eine **Trennung in einen versionierten Codeteil und eine
unversionierte `.env`**, nicht ein Commit der ganzen Datei. Das ist eine
Entscheidung des Betreibers und keine dieser Sitzung.

**b) Nebenbefund: die fünf Krypto-`forward_test.py` handeln auf `df.iloc[-1]`
— also auf der laufenden Kerze.** Beispiel `t3_supertrend/forward_test.py`
Zeile 132/133: `row = df.iloc[-1]`, `prev = df.iloc[-2]`. Der Cronjob läuft
zur Minute 5 nach der 4h-Grenze; `row` ist dann eine fünf Minuten alte
Teilkerze einer Vier-Stunden-Strategie.

Das ist **kein Teil von TB-35** und wurde nicht angefasst: `forward_test.py`
steht ausdrücklich auf der Sperrliste, und eine Änderung daran wäre eine
Änderung am Handelsverhalten, die nach Abschnitt 7 des Übergabeprotokolls
durch Backtest, Walk-Forward und Equity-Simulation muss. Es kann auch Absicht
sein (Einstieg zum aktuellen Kurs). Hier steht nur der Befund, gemessen.

---

## In einfacher Sprache

**Was wir wissen wollten.** Es gibt im Projekt eine einzelne Datei, die die
Kurse von der Krypto-Börse holt. Sie liegt aus Sicherheitsgründen nicht im
gemeinsamen Speicher, sondern nur auf dem Rechner des Betreibers. Wir wollten
mechanisch — also durch ein Programm, das den Programmtext liest, nicht durch
Nachdenken — feststellen, welche Teile des Projekts von ihr abhängen.

**Was herauskam.** Neun Programme hängen an ihr. Vier davon schreiben Kurse in
Dateien; fünf lassen davon abhängen, ob ein Bot kauft oder verkauft. Die
Datei sagt dabei **nicht** mit, ob eine Kursperiode schon zu Ende ist — dieses
Feld geht auf dem Weg verloren.

**Warum das so ist.** Die Börse liefert zu jeder Kerze auch einen Endzeitpunkt
mit. Die nicht einsehbare Datei reicht ihn nicht weiter, sondern nur
Anfangszeit und Kurse. Wer wissen will, ob eine Kerze fertig ist, muss den
Endzeitpunkt also selbst ausrechnen: Anfang plus Länge. Genau das tut die neue
Absicherung.

**Was das für dich heisst.** Zwei Dinge. Erstens: die Absicherung funktioniert
auch ohne diese Datei, weil sie nichts von ihr braucht, was sie nicht hat.
Zweitens: dass ein so wichtiges Stück Programm nur einmal auf einem Rechner
liegt, ist ein Risiko — und es lässt sich beheben, ohne Passwörter ins Repo zu
legen, indem man den Programmteil und die Zugangsdaten trennt. Das ist deine
Entscheidung; diese Sitzung hat sie nur aufgeschrieben.
