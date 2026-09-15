# TB-33 — Nulltest S-E1 Turn-of-Month

**Gegenstand ist nicht die Strategie, sondern der Weg.** Register →
Backtest → Forward-Test ohne Live-Status → Bestätigungsperiode → Bericht,
**ohne dass unterwegs jemand eine Wahl hat.**

Diese Untersuchung fasst **keinen** Bot-Code an: keine `live_params.py`,
keine `forward_test.py`, keine `equity_simulation.py`, keine
`multi_symbol_*.py`, keine Datenbank, keine `results/*.csv`.

---

## Die beiden Register

Beide **vor** dem Lauf eingefroren, beide im Herkunfts-Hash:

| Datei | Inhalt |
|---|---|
| [`docs/VORREGISTRIERUNG_S-E1_strategiekriterien.md`](../../docs/VORREGISTRIERUNG_S-E1_strategiekriterien.md) | Was gerechnet wird: Instrument, Fenster, Kosten, Bootstrap, Schwellen, Sweep-Regel |
| [`docs/VORREGISTRIERUNG_S-E1_pfadkriterien.md`](../../docs/VORREGISTRIERUNG_S-E1_pfadkriterien.md) | Was ein **bestandener Weg** ist: die neun Pfadkriterien P1–P9 |

Sie bauen auf [`docs/VORREGISTRIERUNG_S-E1_nulltest.md`](../../docs/VORREGISTRIERUNG_S-E1_nulltest.md)
(TB-30a) auf und ersetzen es nicht.

---

## Die Dateien

| Datei | was sie tut |
|---|---|
| `register.py` | Die Festlegungen als Code. **Jede Zahl steht hier genau einmal.** |
| `handelstage.py` | Handelstage, nicht Kalendertage. Die einzige Stelle, an der aus einer Kursreihe Ereignisse werden |
| `kennzahlen.py` | Bootstrap und Platzhalter-Verteilung, beide mit festem Startwert aus dem Register. Ohne `scipy` |
| `herkunft.py` | Commit-, Datenstand- und Register-Hash; append-only-Protokoll |
| `auswertung.py` | **Das eingefrorene Auswertungsskript.** Keine Stelle, an der ein Mensch entscheidet |
| `beispieldaten.py` | Erzeugte Kursdaten — damit die Auswertung prüfbar ist, **bevor** echte Ergebnisse existieren |
| `datenlauf.py` | Holt SPY/QQQ/IWM/EFA über yfinance nach `daten/` (**Schritt für den Mac**) |
| `staging.py` | Die Staging-Ebene: läuft und protokolliert, **kein** Portfoliogewicht, **kein** Crash-Knopf |
| `test_turn_of_month.py` | Der Selbsttest. Rückgabewert 0 heisst: der Weg ist sauber gelaufen |

---

## Ablauf

```bash
# 1. Das Register zum Mitlesen
python3 research/turn_of_month/register.py

# 2. Der Selbsttest - laeuft OHNE echte Daten
python3 research/turn_of_month/test_turn_of_month.py

# 3. Die Kursdaten holen (braucht Netz und yfinance)
python3 research/turn_of_month/datenlauf.py

# 4. Der Lauf
python3 research/turn_of_month/auswertung.py \
    --json research/turn_of_month/ergebnisse/lauf.json --protokollieren

# 5. Die Herkunft nachsehen
python3 research/turn_of_month/herkunft.py
```

---

## Die Staging-Ebene

`S-E1` geht nach dem Backtest in die **Staging-Ebene, nicht ins Buch**. Kein
Portfoliogewicht, bevor Rang 3 über die neun Bots entschieden hat — *sonst
kommt ein zehnter Beta-Baustein vor die Beta-Bereinigung, nur durch die
Hintertür.*

```bash
python3 research/turn_of_month/staging.py --lauf     # ein Signal protokollieren
python3 research/turn_of_month/staging.py --status   # Frist und Kriterium
```

**Frist und Entscheidungskriterium standen beim Anlegen fest** (Abschnitt 3
der Pfadkriterien, als Code in `register.py`):

* **Frist:** 12 abgeschlossene Monatswechsel ab dem ersten Signal, spätestens
  **2027-09-30**. Was zuerst eintritt.
* **Kriterium:** S1 Rang 3 hat entschieden · S2 der Backtest hat bestanden ·
  S3 mindestens 12 Forward-Ereignisse **und** untere Bootstrap-Grenze > 0.
* Trifft eines nicht zu, wird der Eintrag **geschlossen**. Kein „vorerst
  behalten".

### ⚠️ Der Cronjob ist **nicht** eingetragen — nur ein Vorschlag

Wie bei der Log-Rotation (`30 3 * * *`) und der Portfolio-Sicht
(`40 3 * * *`) trägt der **Betreiber** die Zeile selbst ein. Ein
Forschungslauf, der sich selbst in die Crontab schreibt, hat den Unterschied
zwischen Staging und Buch schon verloren.

```cron
# TB-33 / S-E1 Staging - taeglich nach US-Boersenschluss, werktags.
# NICHT eingetragen. Vorschlag.
15 23 * * 1-5 cd ~/trading-bot && ./trading-env/bin/python3 research/turn_of_month/staging.py --lauf >> logs/s_e1_staging.log 2>&1
```

Prüfen mit `crontab -l | grep turn_of_month`. **Ohne den Eintrag passiert
nichts** — das ist ein bewusst möglicher Zwischenschritt, genau wie bei den
Warteaufträgen.

---

## Was dieser Ordner **nicht** tut

* Er legt **kein** Portfoliogewicht an und taucht in **keiner** Portfolio-Zahl
  auf. Nicht wegen einer Flagge, sondern weil er in keiner der Listen steht,
  aus denen sie gebildet werden (`shared/ergebniskurven.finde_bots()`,
  `notifications/manual_close.SCHLIESSBARE_BOTS`). Teil D des Selbsttests
  prüft das am **Verhalten**.
* Er erzeugt **keine** `paper_trading_*.db` und **keinen** Eintrag unter
  `results/`.
* Er trägt **nichts** zur DSR bei: **N = 1**. Zum Versuchsregister zählt er
  als **ein** Eintrag — *ein Versuch ohne Wahl ist trotzdem ein Versuch.*
