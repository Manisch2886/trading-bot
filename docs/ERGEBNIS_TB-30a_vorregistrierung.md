# TB-30a — Vorregistrierung der Neuselektion: Ergebnis

**14.09.2026.** Kurzfassung zum Kopieren. Einzelheiten:
[`docs/VORREGISTRIERUNG_neuselektion.md`](VORREGISTRIERUNG_neuselektion.md),
[`docs/VORREGISTRIERUNG_S-E1_nulltest.md`](VORREGISTRIERUNG_S-E1_nulltest.md),
[`research/vorregistrierung/BERICHT.md`](../research/vorregistrierung/BERICHT.md).

---

## Der Vollständigkeitstest

> *Liess sich das Auswertungsskript fertig schreiben, ohne ein einziges
> Ergebnis gesehen zu haben?*

**Ja.** `research/vorregistrierung/auswertung.py` läuft gegen erzeugte
Beispieldaten mit frei erfundenen Werten und gibt aus: Plateau-Gewinner je
Bot, Markierungen (Spitze, Kante, nicht zulässig), Bleibt-Geht-Liste nach
(a)–(d), die drei DSR-Werte, alle Kennzahlen der Beurteilung, zuletzt die
Bestätigungsperiode. **Es hat keinen Schalter**, der eine Schwelle
verschiebt, einen Bot ausnimmt oder eine Kennzahl unterdrückt.

**Fertigschreiben hiess an sieben Stellen: eine Lesart festlegen**, wo die
zwölf Festlegungen zwei zuliessen. Alle sieben stehen im Register,
Abschnitt 12. Die tragende ist die erste — `DD_Toleranz` trägt ein
Exposure-Argument, weil ein Median exposure-abhängiger Grössen selbst
exposure-abhängig ist.

---

## Ist die Drawdown-Bedingung in 2020 und 2022 erfüllbar?

**Ja, und mit Abstand.** Bei 50 % Exposure:

| Falte | `DD_Benchmark` | `1,25 ×` | `DD_Toleranz` | **erlaubt** | wer bindet |
|---|---:|---:|---:|---:|---|
| 2019 | −3,69 % | −4,61 % | −4,33 % | **−4,61 %** | relativ |
| **2020** | −18,93 % | −23,66 % | −4,33 % | **−23,66 %** | relativ |
| 2021 | −2,38 % | −2,98 % | −4,33 % | **−4,33 %** | **`DD_Toleranz`** |
| **2022** | −10,09 % | −12,61 % | −4,33 % | **−12,61 %** | relativ |
| 2023 | −4,33 % | −5,41 % | −4,33 % | **−5,41 %** | relativ |
| 2024 | −3,47 % | −4,34 % | −4,33 % | **−4,34 %** | relativ (knapp) |
| 2025 | −8,89 % | −11,11 % | −4,33 % | **−11,11 %** | relativ |

Die Krisenfalten sind die **grosszügigsten** des ganzen Plans. Gebunden wird
in den ruhigen Jahren — und dort erst oberhalb der Rauschgrenze, weil
`DD_Toleranz` 2021 die relative Grenze ablöst. Genau die Lücke, die
Festlegung 5 schliessen sollte.

---

## Was erstellt wurde

| | |
|---|---|
| **Register** | `docs/VORREGISTRIERUNG_neuselektion.md` — Rastergrenzen mit Grenzsätzen, Faltenplan, Plateau- und Kantenregel, Drawdown-Bedingung, Abbruchkriterien, DSR-Buchführung, Sperrliste, Amendment-Regel |
| **Nulltest** | `docs/VORREGISTRIERUNG_S-E1_nulltest.md` — eigener Registereintrag, beide Bedingungen eingetragen |
| **Eingefrorenes Skript** | `research/vorregistrierung/auswertung.py` — inkl. Beta-Bereinigung und Zufalls-Timing-Test |
| **Vorab-Berechnungen** | `research/vorregistrierung/ergebnisse/` — Messgrössen, Faltenplan, Benchmark-Drawdowns über die ganze Exposure-Achse |
| **Wachen** | `pruefe_grenzsaetze.py` (395 Prüfungen), `registerbericht.py --pruefen`, `herkunft.py` |
| **Tests** | `test_vorregistrierung.py` (150), `shared/test_regimewache.py` (16), `shared/test_agent2_kapitalmass.py` (34) |
| **Bug-Fix AB2/U5** | `shared/regimewache.py` — Entscheidung **abbrechen**, Mechanik fertig; Einbau an drei Stellen ist TB-30b |
| **Bug-Fix Agent 2** | `shared/param_search_agent.py` — dreistufige Zielmass-Kaskade statt fest verdrahtetem „es gilt das chronologische" |
| **Testauftrag** | `docs/TESTAUFTRAG_TB-30a_vorregistrierung.md` — inkl. GPG-Tag und OpenTimestamps |

---

## Die Zahlen

| | |
|---|---:|
| Rasterzellen dieses Laufs, neun Bots | **2 416** |
| N historisch (Versuchsregister) | 653 |
| **N nominal** | **3 069** |
| Bots mit Zweijahres-Falten | **1** — `elliott_wave`, 26,0 gefundene Trades/Jahr |
| Selektionsfalten je Aktien-Bot | **7** (2019–2025) |
| Bestätigungsperiode | 2026-01-01 bis **Go-Live-Schnitt 2026-09-01**, wächst monatlich |
| Krypto-Faltenpläne | **Platzhalter mit Regel** — hängen an TB-31 |
| Purge = Embargo | 10 bis 134 Tage, je Bot die maximale gemessene Haltedauer (TB-24) |

---

## Zwei Wachen haben angeschlagen

**1. Ein Grenzsatz nannte einen Live-Wert.** Der Satz zur Obergrenze der
T3-Längen enthielt „20-Balken-Spanne"; `t3_supertrend` führt
`ADX_THRESHOLD = 20.0`. Umformuliert zu „Zwanzig-Balken-Spanne". Die
Übereinstimmung war unschuldig — und deshalb ein guter Beleg, dass die Wache
etwas tut.

**2. Die Wache aus TB-29 war falsch gebaut.**
`research/versuchsregister/test_versuchsregister.py` prüfte, dass `git
status` nichts ausserhalb von `research/` und `docs/` meldet. Das prüft nicht
TB-29, sondern den **Arbeitsbaum** — und meldete die beauftragte Änderung an
`shared/` als TB-29-Verstoss. Umgestellt auf das, was TB-29 zugesichert hat:
*ein Lauf der Untersuchung verändert nichts* — beobachtet am Ablauf, nicht am
Zustand.

---

## Was der Betreiber noch tun muss

| | |
|---|---|
| **Signierter Tag** (GPG) | Testauftrag Schritt 8 — bindet den Zustand an einen Schlüssel statt an einen editierbaren Zeitstempel |
| **Externer Zeitanker** (OpenTimestamps) | Testauftrag Schritt 9 — für Register-Hash und Datenstand-Hash |

`python3 research/vorregistrierung/herkunft.py` meldet den Stand.

---

## Was vor dem Lauf noch fehlt (alles TB-30b)

1. **Regimewache einbauen** — drei Stellen, `regimewache.pruefe_einbau()`
   meldet den Stand. **Bis dahin darf der Lauf nicht starten.**
2. **`max_drawdown_kapital_pct`** in `evaluate_combination_multi` — dann
   schaltet Agent 2 von selbst auf das führende Mass um.
3. **Zwei Achsen durchreichen** — `SMA_TREND_PERIOD` bei
   `rsi2_mean_reversion`, `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` bei beiden
   Volatility-Breakout-Bots.
4. **TB-31 abwarten** — ohne zurückgeladene Krypto-Historie bleiben die fünf
   Krypto-Faltenpläne Platzhalter.

---

## Und der Satz, der wörtlich ins Register gehörte

> **Dieses Ergebnis ist zulässig: Es kann sein, dass kein einziger Bot die
> Schwelle erreicht.** Eine Aussage über den **Backtest**, nicht über die
> Bots. *Wer das vorher nicht aufschreibt, wird es nachher nicht
> akzeptieren.*

Er steht als Zeichenkette in `registerdaten.py` und wird am Ende **jeder**
Bleibt-Geht-Liste ausgegeben — auch dann, wenn kein Bot ausscheidet.
