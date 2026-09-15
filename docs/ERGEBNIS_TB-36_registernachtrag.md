# Ergebnis TB-36 — Faltenplan und Registernachtrag

**Stand: 15.09.2026. Zum Kopieren.** Keine Änderung an Bot-Code, keinem
Parameter, keiner Kursdatei. Kein Selektionslauf.

---

## Die beiden Antworten, um die gebeten wurde

### 1. Stimmt die Krypto-Gegenprobe?

**Ja, exakt.** Das neue Werkzeug liefert für alle fünf Krypto-Bots dieselben
Zahlen wie `research/krypto_historie/faltenplan.py --mindesttraining 0`:

| | |
|---|---|
| erste Falte | **2019** |
| Selektionsfalten Tagesbots (und `t3_supertrend`) | **7** — 2019 bis 2025 |
| Doppeljahr-Falten `elliott_wave` | **3** — 2019–2020, 2021–2022, 2023–2024 |
| Symbole je Falte | **6 / 9 / 13 / 13 / 13 / 17 / 18** |
| Bestätigungsperiode | **23** Symbole |

Verglichen wird nicht die Anzahl, sondern die **Symbolliste je Falte,
namentlich**; beide Werkzeuge laufen dafür als eigener Prozess auf denselben
Kursdateien.

### 2. Faltenzahl und Symbolzahl der vier Aktien-Bots

**Alle vier gleich** — sie teilen Universum (`config/sp500_top150.txt`, 150
Symbole) und Faltenplan:

| | |
|---|---|
| Selektionsfalten | **7** — 2019, 2020, 2021, 2022, 2023, 2024, 2025 |
| Bestätigungsperiode | **2026** (bis Go-Live-Schnitt 2026-09-01) |
| Symbole je Selektionsfalte | **140 / 142 / 145 / 147 / 148 / 148 / 149** |
| Symbole Bestätigungsperiode | **150 von 150** |

Betrifft `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`,
`volatility_breakout`.

---

## Der Faltenplan, vollständig

| Bot | Markt | Länge | Selektionsfalten | # | Symbole je Falte → Bestätigung |
|---|---|---:|---|---:|---|
| `elliott_wave` | krypto | 2 J | 2019–2020, 2021–2022, 2023–2024 | 3 | 6 / 13 / 13 → 18 |
| `t3_supertrend` | krypto | 1 J | 2019 … 2025 | 7 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `rsi2_crypto` | krypto | 1 J | 2019 … 2025 | 7 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `turtle_soup_crypto` | krypto | 1 J | 2019 … 2025 | 7 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `volatility_breakout_crypto` | krypto | 1 J | 2019 … 2025 | 7 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `elliott_wave_stocks` | aktien | 1 J | 2019 … 2025 | 7 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `rsi2_mean_reversion` | aktien | 1 J | 2019 … 2025 | 7 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `turtle_soup_stocks` | aktien | 1 J | 2019 … 2025 | 7 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `volatility_breakout` | aktien | 1 J | 2019 … 2025 | 7 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |

**Kein Bot ist unterbestimmt.** Der niedrigste Wert ist 3 und erreicht die
Schwelle aus Registertext 4b genau.

**Sieben Symbole haben keine Faltenevidenz** — für sie gilt der gewählte
Parametersatz live, ohne dass eine Selektionsfalte etwas über sie sagt:
Krypto `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT`;
Aktien `SNDK`.

---

## Das Embargo je Bot (Registertext 2d)

| Bot | Grundlage | Handelstage | **Embargo** |
|---|---|---:|---:|
| `elliott_wave` | `MAX_HOLD_HOURS` = 240 Stundenbalken | 10 | **11** |
| `t3_supertrend` | **keine Zeitbremse** → P95 = 11,21 Tage | 11,21 | **13** |
| `rsi2_crypto` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `turtle_soup_crypto` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `volatility_breakout_crypto` | `MAX_HOLD_DAYS` = 15 | 15 | **16** |
| `elliott_wave_stocks` | `MAX_HOLD_HOURS` = 90 Tagesbalken | 90 | **91** |
| `rsi2_mean_reversion` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `turtle_soup_stocks` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `volatility_breakout` | `MAX_HOLD_DAYS` = 15 | 15 | **16** |

Jede Zahl wird bei jedem Lauf **aus der Bot-Datei gelesen**, mit Datei und
Zeilennummer in der Ausgabe. Genau ein Bot hat keine Zeitbremse
(`t3_supertrend`) — das ist die TB-24-Messung, keine Annahme.

---

## Was eingetragen wurde

`docs/VORREGISTRIERUNG_neuselektion.md`, **Abschnitt 15** (neu):

| | |
|---|---|
| 15.1 | Verfahren B gilt — einmalige Auswahl über das ganze Raster |
| 15.2 | **Registertext 0** — Verfahren |
| 15.3 | **Registertext 1** — Bootstrap (1a, 1b neu; 1c ersetzt) |
| 15.4 | **Registertext 2** — Faltenzuordnung, mit Embargo-Tabelle |
| 15.5 | **Registertext 3** — Universum (ersetzt die frühere Fassung), mit Symbolzahlen und Hashes |
| 15.6 | **Registertext 4** — Falten (4b, 4c ersetzt), mit Faltenliste |
| 15.7 | **Registertext 5** — Datenstand |
| 15.8 | vier Befunde am Rande |
| 15.9 | was der Nachtrag nicht tut |

**Bestehender Text wurde nicht umgeschrieben.** Vier Stellen im alten Text
(Abschnitt 3 „Der Faltenplan", 5.1, 5.3, Sperrliste Nr. 8) tragen einen Verweis
auf Abschnitt 15. `git diff origin/main -- docs/VORREGISTRIERUNG_neuselektion.md`
enthält **null entfernte Zeilen**.

**Das ist kein Amendment:** Es hat kein Selektionslauf stattgefunden, und die
Sperrliste gilt laut ihrem eigenen ersten Satz erst „ab dem signierten Tag" —
der steht weiterhin als offen.

---

## Vier Befunde am Rande

Keiner ändert eine Zahl.

1. **„AF.2 Nr. 6" gibt es in diesem Repo nicht.** Gemeint und angewandt ist die
   Doppeljahr-Regel aus **Abschnitt 5.1 Nr. 6** samt Auswertung in **5.4**. Die
   Regel wurde nachgelesen und nachgerechnet; nur ihr Aktenzeichen stimmt nicht.
2. **Drei „ersetzte Fassungen" haben im Register nie gestanden** — die
   Mindestzahl 10 Trades, „mindestens 4" Falten, „behält seine heutigen
   Parameter". Sie stammen aus früheren Beratungsrunden. Die Klammerzusätze
   bleiben wörtlich, die Texte sind als **Erstfassung** eingetragen.
3. **`auswertung.py` rechnet weiterhin nach Verfahren A** — eingefroren und
   nicht angefasst. Die Umstellung ist **TB-30b**. Bis dahin beschreibt der
   Nachtrag, was gerechnet wird, und das Skript kann es noch nicht.
4. **Die Bots überspringen kurze Historien von sich aus** (`MIN_HISTORY_DAYS`).
   Betroffen: `GEV`, `SNDK`, `CEG` (Aktien) und `ENSOUSDT`, `PUMPUSDT`,
   `ZKCUSDT`, `UUSDT` (Krypto). Die Symbolzahlen sagen, wie viele Symbole
   Evidenz liefern **können**, nicht wie viele der heutige Bot-Code lädt. Auch
   das gehört in TB-30b.

---

## Die eine Lesart, die nötig war

Registertext 3a: Symbole, „für die am 1. Januar der Falte Kursdaten
**einschliesslich Indikator-Vorlauf** vorliegen". Eingetragen ist **Lesart A**
(Kursdaten liegen vor; der Vorlauf läuft in die Falte hinein und das Symbol
trägt für diese Tage 0 bei). Begründung steht im Register selbst: 3b nennt
**eine** Zahlenreihe für **alle** Krypto-Tagesbots — hinge die Zahl am Vorlauf,
hätte jeder Bot seine eigene; und der nächste Satz von 3a lässt Symbole ohne
Historie 0 beitragen statt sie auszuschliessen.

Der Preis ist gerechnet und steht im Register neben der Zahl: bei fünf der neun
Bots weicht die strenge Lesart B ab, am deutlichsten bei `rsi2_crypto`
(Falte 2021: 9 statt 13 Symbole, Bestätigung 20 statt 23).

---

## Dateien

| | |
|---|---|
| `research/faltenplan_neun/faltenplan_neun.py` | Faltenplan, alle neun Bots, reine Standardbibliothek |
| `research/faltenplan_neun/embargo_neun.py` | Embargo je Bot |
| `research/faltenplan_neun/test_faltenplan_neun.py` | 145 Prüfungen, vier Mutationsproben |
| `research/faltenplan_neun/BERICHT.md` | ausführlicher Bericht |
| `research/faltenplan_neun/daten/*.json` | Ergebnisse, maschinenlesbar |
| `docs/VORREGISTRIERUNG_neuselektion.md` | Abschnitt 15 neu, vier Verweise im alten Text |
| `docs/TESTAUFTRAG_TB-36_registernachtrag.md` | Testauftrag für den Mac |
| `docs/UEBERGABE_TB-36_registernachtrag.md` | Übergabe-Zusammenfassung |

**Datenstand unverändert:** `d9449faf51bffaaa…`, 223 Kursdateien.

---

## In einfacher Sprache

**Was wir wissen wollten.** Bevor die grosse Parametersuche beginnt, muss
schriftlich feststehen, worauf gerechnet wird: in welche Zeitabschnitte die
Vergangenheit zerlegt wird, welche Wertpapiere in jedem Abschnitt vorkommen und
wie lange nach dem Stichtag gewartet wird, bevor die Prüfperiode beginnt. Für
die Aktien-Bots stand das noch gar nicht fest.

**Was herauskam.** Acht der neun Bots bekommen sieben Abschnitte (die Jahre
2019 bis 2025), geprüft wird am Jahr 2026. Ein Bot handelt so selten, dass
seine Abschnitte doppelt so lang sein müssen; er bekommt drei. Bei den
Kryptowährungen wächst die Zahl der handelbaren Münzen von 6 auf 18, bei den
Aktien von 140 auf 149 von 150. Die Wartezeit liegt je nach Bot bei 11 bis 91
Tagen. Die Kontrollrechnung gegen die frühere Untersuchung stimmt auf jedes
einzelne Symbol.

**Warum das so ist.** Eine Münze kann erst gehandelt werden, wenn es sie gibt —
Bitcoin haben wir seit 2017, manche Münzen erst seit 2025. Die Wartezeit
richtet sich danach, wie lange ein Bot eine Position höchstens hält; bei dem
einen Bot ohne feste Obergrenze haben wir gemessen, wie lange seine längsten
5 % der Positionen dauern. Alle Zahlen sind aus vorhandenen Dateien abgelesen
oder nachgerechnet — geschätzt ist keine.

**Was das für dich heisst.** Der Registereintrag ist vollständig; die
Parametersuche kann darauf aufsetzen, ohne dass danach noch etwas entschieden
werden müsste. Am Handel hat sich nichts geändert: keine Order, kein Parameter,
keine Kursdatei. Offen bleibt bewusst eines: das Auswertungsskript rechnet noch
nach dem alten Verfahren — das ist die nächste Aufgabe.
