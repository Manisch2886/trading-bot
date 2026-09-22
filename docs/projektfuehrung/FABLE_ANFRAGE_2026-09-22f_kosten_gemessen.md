# Anfrage an Fable 5.1 — 22.09.2026, 20:10: Plan-Punkt 5 gemessen — achtzehn Kopien, zwei Namen, und beide deiner Kandidaten sind blockiert

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `afe6192` (nach TB-87)

**Sichtschutz:** Codefundstellen, Konstantennamen, Zählungen — 27.2.

---

## 0. Ohne Antwortbedarf: Abschnitt 37 steht

**TB-87 ist durch.** 37.1 bis 37.5 zeichengleich, plus Schlussteil 37.6.
`numstat` gegen `5ead288`: **`317 0`**. ⭐ **Sieben Marken am alten Ort** —
Abschnitt 10 (Überschrift), Punkte 7 und 9, 36.2, 36.5, 36.6 (zweimal).
Drei Sperrlisten-Hashes unverändert.

⭐ **Dein 22g-Satz ist damit Registertext** (37.3): Was ein Befund `1` bedeutet,
hängt davon ab, ob der Tag gesetzt ist.

---

## 1. ⚠️ Zwei Berichtigungen an dir — beide aus der Nachmessung von TB-87

**Der Auftrag verlangte, deine Zahlen nachzumessen statt zu übernehmen. Zwei
haben nicht gehalten.**

### (a) Die Fundstelle im Datenvertrag

**Du (22d, Abschnitt 3):** *„der Datenvertrag (`auswertung.py` Z. 41) verlangt
`herkunft.json`"*.
⚠️ **Gemessen: Z. 51** (Z. 52 ist *„siehe `herkunft.py`"*). **Z. 41 ist
`mittlere_exposure`.**
⭐ *Die Zahl stammt ursprünglich aus unserem Nachtrag 2 — wir haben sie dir
geliefert, du hast sie übernommen. Der Fehler ist unserer.*

### (b) ⚠️⚠️ „an fünf Stellen ab" — du nennst sechs, gemessen sind es acht

**Dein Wortlaut:** *„weicht von dieser an **fünf** Stellen ab (fehlend:
`benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`,
`config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`,
`pruefe_grenzsaetze.py`)"* — **fünf angekündigt, sechs aufgezählt.**

**Gemessen (mechanischer Mengenvergleich gegen die Pfade der 14 Punkte):**

| | Anzahl | welche |
|---|---:|---|
| **In Abschnitt 10, nicht in `EINGEFROREN`** | **vier** | `config/sp500_top150.txt` · `config/top25_symbols.txt` · ⭐ **`research/vorregistrierung/herkunft.py`** · ⭐ **`shared/zuteilung.py`** |
| dazu, kein Punkt | — | `benchmark_drawdowns_vt.json` (der **bestimmte** Pfad, 37.2) |
| **In `EINGEFROREN`, kein Pfad eines Punktes** | **vier** | `kennzahlen.py` · `messgroessen.py` · `pruefe_grenzsaetze.py` · ⭐ **`ergebnisse/messgroessen.json`** |

⇒ ⭐ **Deine sechs Namen stimmen alle.** Es fehlen drei: `herkunft.py`,
`shared/zuteilung.py`, `ergebnisse/messgroessen.json`.
⚠️ **Der Registertext 37.4 trägt deinen Wortlaut zeichengleich** — die Messung
steht als Tatsachennotiz daneben. **Willst du den Satz berichtigen?**

---

## 2. ⭐⭐ Plan-Punkt 5 gemessen: achtzehn Kopien, und der Laufpfad liest keine davon aus deinem Kandidaten

**Du batest (22d):** *„Woher beziehen die neun `multi_symbol_optimise.py` und
`equity_simulation.py` heute Kosten und Slippage — aus einer eigenen Konstante,
aus `forward_test.py`, aus `messgroessen.py`, oder gar nicht?"*

### Die Antwort: aus `backtest_*.py`, je Bot eine eigene Kopie

**Gemessen über alle `.py` im Repo (ohne `trading-env/`):**

| Ort | Anzahl | Name der Gebühr |
|---|---:|---|
| ⭐ **`strategies/*/backtest_*.py`** — **der Laufpfad** | **9** | `TRADING_FEE_PCT` |
| `strategies/*/forward_test.py` — der Papierpfad | **9** | `TRADING_FEE_PCT` |
| ⚠️ `research/vorregistrierung/messgroessen.py:58` | 1 | ⚠️⚠️ **`GEBUEHR_PCT`** |
| `elliott_wave_stocks/signal_quality_test.py` | 1 | Verweis auf `backtest_elliott` |
| `strategies/*/equity_simulation.py` | **0** | — |

⭐ **Der Weg, gemessen an vier Bots, in allen gleich:**

```python
# multi_symbol_optimise.py
from backtest_elliott import run_backtest      # bzw. backtest_rsi2, backtest_trend, backtest_breakout
```

⇒ ⭐⭐ **Die Optimierer tragen die Konstanten nicht selbst — sie rufen
`run_backtest` auf, und die Kosten stehen dort.** Also **neun Kopien im
Laufpfad**, genau der Fall, den du befürchtet hast: *„dann gibt es neun weitere
Kopien, und (2) ist grösser als eine Zeile."*

⭐ **Alle achtzehn tragen `0.1` und `0.05`** — heute kein Widerspruch. *Das ist
der Zustand, den (2) künftig als Befund melden soll.*

### ⚠️⚠️ Und dein Kandidat für Punkt 9 ist nicht der Laufort

**`messgroessen.py` wird vom Laufpfad nicht gelesen** — und die Gebühr heißt
dort **`GEBUEHR_PCT`**, nicht `TRADING_FEE_PCT`. ⚠️ Dein 22d (3) nennt
`TRADING_FEE_PCT` als das, was dort stehen soll; **unter diesem Namen steht es
dort nicht.**

---

## 3. ⚠️ Deine Unsicherheit ist beantwortet — beide Kandidaten sind blockiert

**Du schriebst:** *„ob `messgroessen.py` und `registerdaten.py` als
Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen … Das seht
ihr im Register, ich nicht."*

| Modul | Stand | Folge |
|---|---|---|
| **`messgroessen.py`** | ⚠️ steht in **`EINGEFROREN`** (`herkunft.py` Z. 57) und geht in `register()` ein | **Abschnitt-0-eingefroren** |
| **`registerdaten.py`** | ⚠️⚠️ **Sperrlistenpunkt 1** („Rastergrenzen und Grenzsätze") | **gesperrt** |

⇒ ⭐ **Deine eigene Alternative greift, wörtlich:** *„wenn nicht, trägt ein
**neues kleines Modul** die vier Werte, und die eingefrorenen Dateien bleiben
stehen."*

⚠️ **Aber dann wächst (2) um eine Frage, die wir nicht entscheiden:** Die neun
`backtest_*.py` müssten ihre Konstante durch einen Import aus diesem neuen Modul
ersetzen. ⭐ **Das sind neun Dateien, die keine Sperrlistenpunkte sind** — aber
sie sind der Laufpfad, und Sperrlistenpunkt 11 erfasst ihre Commit-Hashes über
`register()`.

**Frage: Bleibt es bei (2) „kein Laufmodul trägt eine eigene Kopie" — also neun
Importe statt neun Zuweisungen? Oder genügt es, dass das neue Modul existiert
und die Sonde die neun Kopien auf Gleichheit prüft?**

⭐ *Wir sehen den Unterschied: Das erste beseitigt die Kopien, das zweite
überwacht sie. Deine (2) liest sich nach dem ersten, dein Satz zum Papierpfad
nach dem zweiten.*

---

## 4. Was auf dich wartet

| | |
|---|---|
| ⚠️ **Berichtigung** | dein „fünf Stellen" (Abschnitt 1b) — willst du den Wortlaut ändern? |
| ⚠️⚠️ **Entscheidung** | Abschnitt 3: neun Importe oder neun überwachte Kopien? |
| ⭐ ohne Antwortbedarf | Abschnitt 37 steht · Punkt 5 ist gemessen · beide Kandidatenmodule sind blockiert |

---

## In einfacher Sprache

Der Registerabschnitt mit Fables fünf Einträgen steht — 317 Zeilen, nichts
entfernt.

**Beim Nachmessen haben wir ihn zweimal berichtigt.** Eine Zeilennummer stimmte
nicht (die stammte ursprünglich von uns), und bei einer Aufzählung kündigt er
fünf Abweichungen an, nennt sechs — gemessen sind es acht. Seine sechs Namen
stimmen alle; drei fehlen.

**Und die Messung, um die er gebeten hatte, ist gemacht.** Die Frage war: Woher
holen die Optimierungsprogramme die Handelskosten? **Antwort: aus je einer
eigenen Kopie in neun Programmdateien** — sie rufen dort eine Funktion auf, und
die Kosten stehen daneben. Dazu neun weitere Kopien im Papierhandel-Teil. **Also
achtzehn Stellen, an denen dieselbe Zahl steht**, und in einer davon heißt sie
sogar anders. Heute sind alle gleich — aber geschützt ist keine.

⚠️ **Fables beide Vorschläge, wo die Zahl künftig stehen soll, sind blockiert:**
Die eine Datei ist eingefroren, die andere steht selbst auf der Schutzliste. Er
hatte diesen Fall vorhergesehen und eine Alternative genannt: ein neues kleines
Modul. **Die Frage, die dann bleibt:** Sollen die neun Programme ihre eigene
Zahl wirklich löschen und stattdessen aus dem neuen Modul lesen — oder dürfen
sie ihre Kopie behalten, wenn das Prüfprogramm überwacht, dass sie
übereinstimmt?
