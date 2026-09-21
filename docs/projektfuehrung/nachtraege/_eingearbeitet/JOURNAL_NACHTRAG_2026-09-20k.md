# Journal-Nachtrag (k) — 20.09.2026, TB-72 Schritte 2–7: die erste Falte ist eine Konjunktion, der Plan leitet sie aus dem Trockenlauf ab, und genau ein Bot ändert sich

**Quelle:** Mac-Sitzung **TB-72 erste Falte aus Trockenlauf**, 20.09.2026,
dritter Anlauf ab 20:20 Ortszeit (Schritt 1 lag in `7b73584`, die Fable-Antwort
zur Konjunktion war da), Ausgang `7b73584` (= `origin/main` beim Start),
Interpreter `trading-env/bin/python3` 3.9.6. Commits `96cc9c7` (Schritt 0,
Betreiber-Dateien), `e7a4108` (Schritt 2, `faltenplan.py`), `edd1bce`
(Schritt 3, `faltenplan_tb72.json`), `27c58a2` (Schritt 4,
`benchmark_drawdowns_tb72.json`), dann Schritt 5 (Test), Schritt 6 (Register 25)
und Schritt 7 (dieser Nachtrag, Backlog `K4l`, Ergebnisdokument
`docs/ERGEBNIS_TB-72_erste_falte_aus_trockenlauf.md`). **Einzuarbeiten als
nächster Block nach dem höchsten vorhandenen** (am 20.09.2026 gemessen: `BT`;
`(20g)` bis `(20j)` liegen davor — die Nummer vergibt die einarbeitende Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20k.md`*
```

---

## Was der Auftrag wollte und was er bekam

Nach dem Halt aus Schritt 1 (Nachtrag `(20j)`) hat Fable seinen eigenen
Vorschlag zurückgenommen — *„hätte den Aktien-Bots 1967 gegeben … die Messung
in beide Richtungen war die richtige Reihenfolge; zurückgenommen"* — und 4a und
21.3 (b) als **Konjunktion** neu gefasst: Ein Jahr ist Selektionsfalte, wenn
**(i)** Datenhorizont und Indikator-Vorlauf am 1. Januar **und** **(ii)** der
Trockenlauf es tragen. Der Auftrag wollte daraus sechs Schritte: die Ableitung
im Code, den neuen Plan und die neue Benchmark-Tabelle **daneben**, einen Test
mit Mutation, Register 25, eine Backlog-Zeile.

**Bekommen hat er alle sechs, und die Erwartung *„genau ein Bot, genau eine
Falte"* hat gehalten** — gegen den Speicherstand vor TB-72, nicht gegen die
Datei `faltenplan.json` (TB-30a-Stand, wie in `(20j)` vorgemerkt):
`t3_supertrend` 2018 → 2019, Falte 2018 entfällt, sieben Selektionsfalten;
`DD_Toleranz` −12,89 / −24,73 / −45,16 → **−13,90 / −26,57 / −48,10** — Zahl für
Zahl die Erwartung aus TB-65 C1. Die acht anderen Bots sind gegen `_vt.json`
zeichengleich (69 Falten × 100 Stufen, `handelstage`, Symbolzahlen,
`DD_Toleranz`). Drei Sperrlisten-Hashes vorher = nachher.

---

## Vier Befunde

### 1. ⭐ Die Ableitung kostet Laufzeit — und die Form entscheidet, wie viel

Bedingung (ii) heisst: der Loader des Bots läuft im Kindprozess (TB-40,
`messe_bot`). Ein Aktien-Loader braucht rund **6 s je Kindprozess** plus
~1,7 s je weiterem Stichtag; über alle 4a-Kandidaten in einem Prozess wären das
rund 75 s je `faltenplan()`-Aufruf. Umgesetzt ist die Ableitung deshalb **Falte
für Falte**: ein Kindprozess je geprüftem Faltenende, Schluss beim ersten
`H ≥ 1` — bei acht Bots ist das die erste Kandidatenfalte, bei `t3_supertrend`
die zweite. Gemessen: `faltenplan()` **12,4 s → 37,6 s** im ersten Aufruf je
Prozess (`lru_cache` danach). ⚠️ Das zahlt jeder Prozess, der den Plan
importiert — `benchmark.py`, `registerbericht.py`, `auswertung.py` und damit
`test_vorregistrierung.py` Teil H **sechsmal** (je Wegwerf-Kopie ein eigener
Prozess). Die Schritt-1-Messung (`erste_falte_trockenlauf.py main()`) ruft
weiter `vollstaendig=True` (alle Kandidaten in einem Prozess) und bleibt
unverändert — ihr Ergebnis je Falte ist dasselbe, weil jeder Stichtag im
Kindprozess ein eigener Loader-Lauf ist.

⭐ **Regel:** *Wer eine Nachrechnung durch eine Messung ersetzt, nennt die
Laufzeit der Messung und wer sie zahlt. Eine Ableitung, die jeden Aufrufer eine
halbe Minute kostet, ist richtig — aber sie ist nicht kostenlos, und der Preis
steht dorthin, wo der nächste Aufrufer ihn sieht (Modulkopf, Test-Docstring,
Backlog).*

### 2. ⭐ Das Register war dem Code voraus — 21.4 sagte längst 2019

Register 21.4 (TB-56b, 19.09.) führt `t3_supertrend` mit *„2019, 7 Falten"*,
gemessen über die Trockenlauf-Spalte H, und sagt ausdrücklich: *„Nach (b)
bindet 3b (a); seine Zeile bleibt, wie sie war."* Der Code (`faltenplan.py`)
rechnete weiter 4a allein und schrieb 2018 in `benchmark_drawdowns_vt.json` —
eine Selektionsfalte mit 0 Symbolen, 0 Handelstagen, Drawdown 0,00. **Die
Instanz war also keine neue Registertatsache, sondern der Code hinkte der
eigenen Tatsachennotiz hinterher**, und er sagte es in seinem Modulkopf
(Z. 38–42) selbst. Der neue Test vergleicht deshalb drei Quellen: Plan,
eigener `messe_bot`-Aufruf, Register 21.4.

⭐ **Regel:** *Ein Modulkopf, der sagt „das rechnet dieses Modul nicht", ist
ein offener Befund, kein Hinweis. Er gehört in den Backlog oder in einen
Auftrag — mit der Zahl, die er kostet — und nicht nur in den Docstring.*

### 3. ⭐ Eine Gegenüberstellung muss Folgeänderungen von Änderungen trennen

Die erste Fassung der Schritt-3-Gegenüberstellung zählte **neun** geänderte
Falten bei `t3_supertrend` und meldete *„NEIN (Befund)"* gegen die Erwartung
*„genau eine Falte"*. Gemessen waren acht davon nur die Listen
`embargo_nach_falten` der Falten 2019–2026, aus denen die entfallene Falte 2018
verschwindet — eine Folge, keine eigene Änderung; Grenzen, Rollen und
`training_bis_ausschliesslich` aller acht Falten sind gleich. Die zweite Fassung
zählt beides getrennt (**1** entfallene Falte, **8** Folgeänderungen am Embargo)
und meldet *„JA"*. Beide Fassungen liegen im Beleg; die erste Meldung wäre ohne
Nachsehen als Befund ins Ergebnis gewandert.

⭐ **Regel:** *Bevor eine Gegenüberstellung „Befund" meldet, wird je Abweichung
gefragt, ob sie eine eigene Änderung ist oder die Folge einer schon gezählten.
Zählt ein Vergleich Folgen als Änderungen, widerspricht er einer richtigen
Erwartung.*

### 4. Fables Nachrechnung zu `rsi2_crypto` trifft — nachgemessen, nicht übernommen

*„150 Tagesbalken Vorlauf am 1.1.2018 bräuchten Daten ab August 2017, BTC
beginnt am 17.08.2017, das sind 137."* Gemessen aus den Kursdateien: BTC und ETH
haben bis zum 31.12.2017 **137** Balken, der 150. liegt am **2018-01-14**;
Bedingung (i) ist am 1.1.2018 nicht erfüllt, (ii) schon (`H = 2`). Konjunktion:
2019, unverändert. Der Auftrag hatte *„Miss das selbst nach, statt es zu
übernehmen"* verlangt — der Beleg liegt in
`docs/belege/TB-72/schritt2_rsi2_crypto_bedingung_i.txt`.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Schritt 3: Gegenüberstellung gegen `ergebnisse/faltenplan.json` | gegen den Speicherstand vor TB-72 (Beleg aus Schritt 0): ein Bot, eine Falte ✅; gegen die Datei: alle neun Bots — sie ist TB-30a-Stand (`K4k`) |
| Schritt 3: *„genau eine Falte"* | eine entfallene Falte **plus** acht Folgeänderungen an `embargo_nach_falten` (Befund 3) — keine zweite Änderung |
| Schritt 5: *„`test_vorregistrierung.py` oder neben `faltenschranke_messung.py`"* | **neben** `faltenschranke_messung.py` (`research/faltenplan_neun/test_erste_falte_trockenlauf.py`): `test_vorregistrierung.py` bricht im Repo in Teil A ab (gesperrte Tabelle, `KeyError: '2017'`) und erreichte die neue Prüfung nicht; der neue Test läuft allein, misst (ii) mit eigenem `messe_bot`-Aufruf und trägt seine Mutationsprobe selbst |
| Schritt 2: *„Ändere nichts anderes an `faltenplan.py`"* | der Modulkopf (Regel 2 und 3) musste mit — er sagte *„das rechnet dieses Modul nicht"*, was nach Schritt 2 falsch wäre; alter Wortlaut bleibt als ersetzt stehen. Zwei neue Felder je Bot im Plan (`erste_falte_4a`, `erste_falte_trockenlauf_H`), damit im Plan steht, **warum** er dort beginnt |
| Nachweis 3 nennt `ergebnisse/…` | Dateien liegen unter `research/vorregistrierung/ergebnisse/` (wie TB-71, TB-72 Schritt 1) |

---

## Offen

| | wer |
|---|---|
| ⛔ **Vollzug der Sperrlisten-Änderung** (Register 21.9, Betreiberfreigabe) — jetzt mit `benchmark_drawdowns_tb72.json` und `faltenplan_tb72.json`; `registerbericht.py:178` dabei nachziehen (23.5) | Betreiber |
| ⚠️ **TB-74** — Bedingung (i): *„Datenhorizont"* als `asof` minus `RECENT_YEARS_ONLY`, Datenuhr statt Wanduhr, `entry_cutoff` je Symbol gegen `fensteranker` je Markt | eigener Auftrag |
| Laufzeit von `faltenplan()` (+25 s je Prozess) — falls sie in `test_vorregistrierung.py` Teil H oder im Auswerter stört: Ergebnis je Bot cachen (Datei neben dem Plan) wäre eine Konstantenkopie durch die Hintertür und ist **nicht** vorgesehen; erst messen, ob es stört | TB-30b |
| Dieser Nachtrag ins Journal (Block nach dem höchsten vorhandenen) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): Backlog, Register 25, neues Ergebnisdokument, `AKTUELLER_AUFTRAG.md` (TB-72-Zeile auf „erledigt") | steuernder Chat / Betreiber |
