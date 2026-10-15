# FABLE-Anfrage 14.10.b — R95 (a) und der Doppellauf in positionen_holen.py

*Steuernder Chat („Opus Trading Bots-14.10.2026 b“), 14.10.2026, 22:41, Repo-Stand `7b9f9ac`. Kurze Rückfrage zu deiner Antwort 14.10.a. R94–R96 sind nicht eingetragen; das Register steht unverändert am Commit 3f2e97e.*

## 1. Anlass

R95 (a) trägt den Vorbehalt (Antwort 14.10.a, Z. 75, wörtlich):

> 2. Abschnitt 10 und 41.1 (A9) habe ich nicht gelesen; was ich über die Sperrliste und A9 sage, steht nach der Wiedergabe in der Anfrage und in R45. Steht in 41.1 A9 mehr, kommt R95 (a) zurück.

und die Voraussetzung (R95, wörtlich):

> [Voraussetzung, zu messen: der Wortlaut von 41.1 A9 (nicht gelesen; hier nach R45); dass positionen_holen.py und der Doppellauf keine Datei der Sperrliste ändern (24.6 sagt es für TB-73: „Nichts in research/vorregistrierung/, shared/, strategies/ berührt“; für einen neuen Lauf nicht gemessen).]

41.1 A9 lautet (Register Z. 8720, wörtlich):

> „**Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett."

Gemessen beim Bau von TB-162 (Kopie mit echter `data/`, Python 3.10, nicht am Mac): Der Doppellauf in `research/tb24_haltedauern/positionen_holen.py` schreibt im zweiten Lauf eine Zeilenkennung in das Feld `symbol` und übergibt es an `simulate_portfolio` (Z. 320–323, wörtlich):

```python
    # --- Lauf 2: mit Zeilenkennung im Symbol --------------------------------
    markiert = trades.copy()
    markiert["symbol"] = [f"{s}{TRENNER}{i}" for i, s in zip(markiert.index, markiert["symbol"])]
    ergebnis_markiert = basis.simuliere(es, markiert, allocation_pct, max_concurrent)
```

Seit TB-26 (`f6d9a28`) liest die Zuteilungskaskade in `shared/zuteilung.py` Kurs und Umsatz je Symbol (Z. 371–401, `korrelation`, `liquiditaet`); gekennzeichnete Symbole finden dort nichts. Das Werkzeug endet für alle neun Bots mit rc 1 an seiner eigenen Prüfung (Z. 336: „Kennzeichnung hat die Simulation veraendert - Abbruch.“). Es ändert keine Datei der Sperrliste; es schreibt aber eine Kennzeichnung in ein Feld, das der Laufcode liest, und die Kennzeichnung verändert dort die Simulation.

R45 (48.13) ist nicht gebaut: `simuliere_portfolio` gibt heute `final_capital`, `num_executed`, `num_skipped`, `equity_curve` und `zuteilung` zurück, keine Positionen.

## 2. Fragen

F1. Bleibt R95 (a), und in welcher Fassung? Gilt der Doppellauf nach dem Wortlaut von A9 als Verstoss, auch ausserhalb des Laufbereichs?

F2. Woher darf eine Messung nach R94 (b) vor dem Tag die ausgeführten Positionen nehmen?
 (a) Abgleich ohne Kennung: ein Lauf mit unveränderten Trades; die Positionen werden aus der Trade-Liste und der `equity_curve` (Symbol, Zeit) zugeordnet — ist das der „zweite Rechenweg“ aus R84 (e), und bindet er ein Forschungsmodul?
 (b) Rückgabe aus `shared/zuteilung.py` nach R45, mit Freigabe nach 37.3 (Datei der Sperrliste) vor dem Tag.
 (c) Ein anderer Weg, oder keiner vor dem Tag.

F3. Was ändert sich an R94–R96, und braucht es dafür einen Registerblock?

## 3. Lesen

Deine Antwort 14.10.a ganz (`projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md`, md5 c33799567a0205f66c502dbf5aaff5c5); im Register 41.1 (A9), 37.3, 37.5, 48.13 (R45), 56.1 (R84) über REGISTER_INDEX.md und die Registerkopien. `positionen_holen.py` und `shared/zuteilung.py` liegen nicht in der Ablage; die Zitate oben sind per Skript aus der Quelle gezogen.
