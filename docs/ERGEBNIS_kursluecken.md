# Ergebnis — Kurslücken im Trade-Pfad (APH-Befund)

**PR #81** · Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`94e0d7f`, nach Merge von #80).

---

## Zuerst: keine Live-Zahl ändert sich

Über alle 147 Aktien-Symbole, mit der Live-Kombination von
`elliott_wave_stocks`: 510 Trades, 31,57 % Trefferquote, 1,3505 % Ø Rendite,
688,77 % Summe, 17.197,86 Endkapital — **vorher wie nachher identisch**.

Der vergiftete Trade entsteht nur bei Parametern, die nicht live sind. Keine
Aktivierungsentscheidung ist betroffen.

---

## Was gefunden wurde

| Frage | Antwort |
|---|---|
| Wo entsteht das NaN? | `backtest_elliott.py:110`, Zeitausstieg: `exit_price = last_row["close"]` |
| Wie viele Symbole? | **1 von 150** Aktien (`APH`), genau **1** Zeile — die letzte, `2026-09-01`. Krypto: 0 von 24 |
| Welche Bots in der Praxis? | `elliott_wave_stocks`: **24 von 48** Rasterkombinationen. Die drei anderen Aktien-Bots heute 0 |
| Wo verschwindet es? | `.mean()` und `.sum()` überspringen NaN — und `(pnl > 0)` zählt es als **Verlierer** |

**Der Schaden reicht weiter als der Bericht sagte.** In
`simulate_portfolio` fliesst `pnl_pct` in `capital`; ein NaN vererbt sich damit
auf **jeden folgenden Trade**. Gemessen: ein kaputter Trade in der Mitte macht
2 von 3 Kapitalzeilen unbrauchbar, `final_capital` wird `nan` — und
`num_executed` zählt ihn trotzdem als ausgeführt.

**Die Trefferquote wird nicht nur verschwiegen, sondern verfälscht**, weil
`NaN > 0` in Python `False` ergibt. Real gemessen: 55,35 % → 55,08 %.

---

## Was gebaut wurde

`shared/kursdaten.py` — eine Stelle, die definiert, was eine unvollständige
Kerze ist und was mit ihr geschieht: **streichen und zählen**, wie es
`buy_and_hold_benchmark.py` im Projekt längst richtig macht.

Eingebaut an den zwei Stellen, an denen Kursdaten hereinkommen:

1. **`fetch_stock_data.fetch_historical_data`** (4 Aktien-Bots, byte-identisch).
   Diese Funktion schreibt die CSVs **und** versorgt `forward_test.py` live —
   die Absicherung dort behebt den Live-Pfad, **ohne `forward_test.py`
   anzufassen**.
2. **`multi_symbol_optimise.load_all_symbol_data`** (alle 9 Bots), direkt nach
   `pd.read_csv`, für die vorhandenen CSVs.

`equity_simulation.py` ist **unverändert**: dort schlägt der Fehler zu, dort
entsteht er nicht. Eine Wache an der Wirkung käme zu spät (die Trefferquote wäre
schon verfälscht) und müsste in neun gleichnamigen Dateien stehen.

---

## Dass es auffällt — der eigentliche Punkt

Der Schaden war nicht die Lücke, sondern dass niemand sie bemerkt hat. Drei
Wege:

1. **Beim Laden**: `Datenqualitaet: insgesamt 1 unvollstaendige Kerze(n) in 1
   Symbol(en) gestrichen - APH (1). Diese Kerzen gehen in KEINE Kennzahl ein.`
2. **Beim Holen**: eine Zeile je Symbol — erscheint damit auch im Cronjob-Log.
3. **Als Werkzeug**: `python3 shared/kursdaten.py` durchsucht alle Kursdateien,
   **Rückgabewert 1 bei Befund**, damit ein Cronjob es sichtbar macht.

---

## Was sich ändert

| Kombination | vorher | nachher |
|---|---|---|
| **LIVE** (5,0 / 3,0) | — | **unverändert** |
| Befund (6,0 / 16,0, ohne Ziel) | Endkapital `nan` | **59.939,87** |
| Nachbar (3,0 / 3,0) | Endkapital `nan` | **17.682,96** |

Die Trade-Zahl bleibt überall gleich — der Trade verschwindet nicht, er endet
eine Kerze früher und bekommt ein echtes Ergebnis (+26,87 % statt NaN).

**Ein Nebeneffekt, der benannt gehört:** die Zeilenzahl von `APH` bleibt bei
2513, nicht 2512. Der 10-Jahres-Filter richtet sein Fenster am letzten Datum
aus; fällt die leere Kerze weg, beginnt es einen Tag früher und nimmt vorn eine
Zeile auf. Sauberer so — aber eine Prüfung auf „eine Zeile weniger" wäre grün
gewesen, ohne etwas zu zeigen.

---

## Wohin der Befund gehört

**Nicht** in `docs/DATENLUECKEN.md`. Dort stehen Ausfälle, bei denen ein Bot
**gar nicht lief**. Hier lief alles, die **Kursdaten** waren löchrig. Andere
Fehlerklasse, andere Abhilfe. In `DATENLUECKEN.md` steht jetzt genau diese
Abgrenzung mit Verweis auf `shared/kursdaten.py` — und nur die.

---

## Tests

`python3 shared/test_kursdaten.py` — **83 von 83**, 10 Abschnitte.

Der NaN-Fall wird **erzeugt**: der echte Bot-Loader läuft einmal mit und einmal
ohne Absicherung, in getrennten Prozessen. Ohne: **8** NaN-Trades. Mit: **0**.
Die Gegenprobe an einem Symbol ohne Lücke (`AAPL`) vergleicht die Trades über
alle Kombinationen Fingerabdruck für Fingerabdruck — identisch.

**14 Mutationsproben, alle 14 erkannt.** M14 (Absicherung wird aufgerufen, ihr
Ergebnis aber verworfen) fällt **nur** der Verhaltensprüfung mit
yfinance-Attrappe auf — eine Textsuche hätte sie durchgelassen.

Keine Regression: Dashboard 784/784, Portfolio-Sicht 90/90,
Schliess-Benachrichtigung 99/99, Log-Rotation 117/117, Broker 163 und 200,
Empfehlungsformat 70/70, caffeinate 52/52, manual_close alle.

---

## Was du noch tun musst

**Nichts.** Die Absicherung greift beim nächsten Backtest- oder
Optimierungslauf von selbst, und der nächste `fetch_stock_data.py`-Lauf
schreibt saubere CSVs.

Zwei Dinge, die du wissen solltest:

1. **`data/APH_1d.csv` behält seine leere Zeile.** Absichtlich: damit das Repo
   ein echtes Beispiel des Fehlers enthält, an dem sich die Absicherung prüfen
   lässt. Sie richtet keinen Schaden mehr an.
2. **Prüf einmal selbst nach:** `python3 shared/kursdaten.py`. Sind auf deinem
   Rechner mehr Symbole betroffen als das eine hier, ist `APH` kein Einzelfall,
   sondern ein Muster — das wäre der interessanteste Befund.

Der vollständige Ablauf steht in `docs/TESTAUFTRAG_kursluecken.md`; **Schritt 4**
(ändert sich eine Live-Kennzahl?) ist die wichtigste Prüfung.

---

## Offene Punkte

* **Die Ursache liegt bei yfinance** — die Zeile kam mit Datum und Volumen, aber
  ohne Kurse. Ob das wiederkehrt, macht das Werkzeug künftig messbar.
* **`simulate_portfolio` toleriert ein NaN weiterhin.** Käme je eines aus einer
  anderen Richtung — etwa aus einer Live-Datenbank —, wäre die Kapitalkurve
  wieder hin, und seit PR #80 zeigt das Dashboard sie an. Bewusst nicht
  geändert, als Entscheidung weitergereicht.
* **Die drei anderen Aktien-Bots schützt heute nur ihr `entry_cutoff`**, nicht
  ihr eigener Ausstiegspfad. Die Datenabsicherung deckt das ab; ändert jemand
  den Cutoff, bleibt sie die einzige Wache.

## Geänderte Dateien

```
shared/kursdaten.py                          (neu)
shared/test_kursdaten.py                     (neu, 83 Prüfungen)
docs/UEBERGABE_kursluecken.md                (neu)
docs/TESTAUFTRAG_kursluecken.md              (neu)
docs/ERGEBNIS_kursluecken.md                 (neu, dieses Dokument)
strategies/*/fetch_stock_data.py             (4 Aktien-Bots)
strategies/*/multi_symbol_optimise.py        (alle 9 Bots)
docs/DATENLUECKEN.md                         (Abgrenzung)
research/elliott_wave_params/BERICHT.md      (datierter Nachtrag zu Punkt 2)
```

Nicht angefasst: keine `live_params.py`, keine `forward_test.py`, keine
`equity_simulation.py`, nichts unter `broker/`, keine Crontab, keine
launchd-Vorlage, **keine Kursdatei**, kein Backtest-Ergebnis. Alles per
`git diff` gegen `origin/main` im Selbsttest geprüft.
