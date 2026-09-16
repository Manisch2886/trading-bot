# `research/etf_trendfolge/` — Vorbereitung S-B1 (TB-39)

**Status: reine Vorbereitung. KEINE Änderung an Bot-, Backtest- oder
Live-Dateien.** Alle Dateien liegen ausschliesslich unter
`research/etf_trendfolge/` und `docs/`.

> ⚠️ **Dieser Ordner rechnet keinen Backtest. Bewusst.**
> Kein Ertrag, kein Sharpe, keine Parametersuche, keine Auswahl von
> Instrumenten nach ihrem Ergebnis. `S-B1` steht auf Rang 4 der
> Reparaturkette; ihr Backtest gehört **hinter Rang 1**. Vorgezogen ist nur,
> was **nichts auswählt**: Daten beschaffen, Rastergrenzen festlegen, das
> Register schreiben.

Das Register ist
[`docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`](../../docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md).
Der Datenlauf steht in
[`docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`](../../docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md).

---

## Die Module

| Datei | was sie tut |
|---|---|
| `register.py` | **Die eingefrorenen Festlegungen als Code.** Jede Zahl steht genau hier — einmal. Alles andere importiert sie |
| `raster.py` | Baut das Raster und **zählt** N aus der Zellenliste. `--was-waere-wenn` rechnet vor, was weitere Achsen kosten würden |
| `kosten.py` | Was von den Erträgen nach **0,30 Prozentpunkten je Round Trip** bleibt — strukturell, ohne Kursdaten |
| `historie.py` | **Misst** je Kandidat das erste verfügbare Datum und prüft die **Untergrenze**. Rückgabewert **1**, wenn sie fällt |
| `datenlauf.py` | Holt die Kursdateien über yfinance. **Läuft nur am Mac** (Yahoo ist aus der Cloud gesperrt) |
| `datenstand.py` | Die **Wache über `data/`**: Hash und Ort. Rückgabewert 1 bei Abweichung |
| `beispieldaten.py` | Erzeugte Beispieldaten für die Prüfung. **Keine Marktdaten** — aus ihnen folgt keine Aussage über `S-B1` |
| `test_etf_trendfolge.py` | Selbsttest, einschliesslich Mutationsproben |

**Reine Standardbibliothek** — kein pandas, kein numpy. Einzige Ausnahme ist
`datenlauf.py`, der yfinance braucht. Dasselbe Werkzeug läuft damit in der
Cloud und auf dem Rechner des Betreibers.

---

## Der Ablauf

```bash
# 1. Die Wache, vorher
python3 research/etf_trendfolge/datenstand.py

# 2. Der Datenlauf - NUR am Mac, Yahoo ist aus der Cloud gesperrt
python3 research/etf_trendfolge/datenlauf.py

# 3. Die Messung: reicht die Historie?
python3 research/etf_trendfolge/historie.py --json research/etf_trendfolge/ergebnisse/historie.json

# 4. Die Wache, nachher - derselbe Hash wie in Schritt 1
python3 research/etf_trendfolge/datenstand.py

# 5. Der Selbsttest
python3 research/etf_trendfolge/test_etf_trendfolge.py
```

`raster.py` und `kosten.py` brauchen **keine** Daten und laufen überall:

```bash
python3 research/etf_trendfolge/raster.py --was-waere-wenn
python3 research/etf_trendfolge/kosten.py
```

---

## Die drei Regeln dieses Ordners

1. **Nichts unter `data/`.** Der Datenstand-Hash der Vorregistrierung
   (`d9449faf51bffaaa…`, 223 Dateien) ist der SHA-256 über die Dateien dort.
   Eine einzige zusätzliche Datei ändert ihn. Die ETF-Kursdateien liegen
   deshalb unter `daten/` — **gitignoriert**, damit sie auch bei keinem Merge
   dorthin wandern können.

2. **Die Kursdateien werden einmal geholt und dann eingefroren.**
   `datenlauf.py` überschreibt nicht. `--neu` vergleicht und meldet;
   übernommen wird erst mit `--uebernehmen`. Grund: `auto_adjust=True` ändert
   die ganze Historie bei jeder Ausschüttung.

3. **Keine Zahl steht zweimal.** Sie steht in `register.py` und wird
   importiert. Der Selbsttest weist das am Verhalten nach: eine geänderte
   Festlegung ändert das Ergebnis der Werkzeuge (Teil I).

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob sich eine Handelsstrategie bauen lässt, die nicht dasselbe tut wie deine
neun heutigen Programme — und nach welchen Regeln das geprüft werden soll.

**Was herauskam.**
Acht kleine Programme, die zusammen drei Dinge leisten: Sie holen die
Kursdaten (das geht nur auf deinem MacBook), sie messen, wie weit die
Kurshistorie zurückreicht, und sie rechnen aus, wie viel die Handelsgebühren
kosten. Gerechnet, wie gut die Strategie **wäre**, wurde bewusst nichts.

**Warum das so ist.**
Die Reihenfolge ist wichtig: erst die Regeln aufschreiben, dann rechnen. Wer
umgekehrt vorgeht, sucht sich hinterher die Regeln aus, die zum schönsten
Ergebnis passen — und merkt es selbst nicht.

**Was das für dich heisst.**
Du brauchst hier nichts zu tun, ausser der Anleitung in
`docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md` zu folgen. Sie holt die
Kursdaten und beantwortet die eine Frage, die aus der Cloud nicht zu
beantworten war: **Reichen die Kursdaten weit genug zurück, um die
Finanzkrise 2008 mit abzudecken?**
