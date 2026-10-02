# REGISTER-KOPIE Abschnitt 16 (von 0–52) — Register-Z. 1814–2568 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

## 16. Registernachtrag (TB-41, 16.09.2026)

### 16.0 Was das ist — und was es ausdrücklich nicht ist

**Das ist kein Amendment.** Es hat **kein Selektionslauf stattgefunden**: kein
Raster gerechnet, kein Parametersatz bewertet, kein Ergebnis erzeugt — derselbe
Stand wie am Kopf dieses Dokuments und wie am Kopf von Abschnitt 15. Die
Sperrliste (Abschnitt 10) gilt laut ihrem eigenen ersten Satz **„ab dem
signierten Tag"**, und der steht in Abschnitt 13 weiterhin als *offen —
Betreiber*. Es ist deshalb nichts aufzubrechen; es wird nachgetragen, bevor
gerechnet wird.

Seit TB-36 sind **zwölf weitere Festlegungen** entstanden, und **drei der
eingetragenen Tatsachennotizen haben sich als falsch erwiesen**. Dieser
Abschnitt trägt beides **in einem Zug** nach. Danach wird nichts mehr geändert,
bevor der Snapshot gezogen und der signierte Tag gesetzt ist.

**Bestehender Text wird nicht umgeschrieben.** Die betroffenen Passagen
(15.4 Registertext 2d, 15.5 Registertext 3 mit seinen Tatsachennotizen, 15.7
Registertext 5) bleiben **vollständig stehen** und tragen nur einen eingefügten
Verweis hierher. Der Verlauf soll lesbar bleiben — das ist der Sinn eines
Registers. Am Diff dieser Arbeit sind **null Zeilen entfernt**.

**Herkunft der Zahlen.**

| | |
|---|---|
| Symbolzahl je Falte, Symbole ohne Faltenevidenz | `research/universum_trockenlauf/` (TB-40), Ergebnis in `docs/ERGEBNIS_TB-40_universum_trockenlauf.md` |
| `MIN_HISTORY_*` je Bot | `strategies/<bot>/multi_symbol_optimise.py`, **gelesen** |
| Umstellungstag der Entscheidungskerze | `docs/umstellungstag_entscheidungskerze.json` (TB-38) |
| Zeilenzahl und Hash der Universumsdatei | `config/top25_symbols.txt`, `shared/symbols_config.py` |
| Datenstand | `d9449faf51bffaaa…`, 223 Kursdateien — vor und nach dieser Arbeit identisch |
| Prüfwerkzeug dieses Nachtrags | `research/registernachtrag_tb41/` |

⚠️ **Die Zahlen sind nicht abgetippt.** `research/registernachtrag_tb41/pruefe_register.py`
vergleicht die hier eingetragenen Zahlen **maschinell** gegen ihre Quelle und
meldet jede Abweichung; auf einer Maschine mit Bot-Abhängigkeiten vergleicht es
zusätzlich gegen einen frischen Trockenlauf des Laufcodes.

---

### 16.1 Die drei falschen Tatsachennotizen — korrigiert

#### 16.1.1 Symbolzahl je Falte (Tatsachennotiz zu Registertext 3b)

**Gemessen in TB-40 durch Trockenlauf des Laufcodes** — der Loader des Bots
entscheidet, nicht ein nachgebautes Werkzeug. **Acht der neun Reihen** in der
Tabelle von 15.5 sind **zu hoch**; `elliott_wave` stimmt. **Es kommt nirgends
ein Symbol hinzu** — in keiner Falte eines Bots: die gemessenen Mengen sind
überall Teilmengen der eingetragenen (F ⊆ H ⊆ A).

> **Die Symbolzahl je Falte** (Tatsachennotiz zu 3b, **ersetzt die Fassung aus
> 15.5**; Lesart H, gemessen am Loader):
>
> | Bot | Symbolzahl je Selektionsfalte | Bestätigung | Universum |
> |---|---|---:|---:|
> | `elliott_wave` | 6 / 13 / 13 | 18 | 24 |
> | `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |
> | `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `rsi2_mean_reversion` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `turtle_soup_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `volatility_breakout` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
>
> `elliott_wave` hat Doppeljahr-Falten; seine drei Zahlen stehen für 2019–2020,
> 2021–2022 und 2023–2024. Die vier Aktien-Bots teilen eine Reihe, weil sie
> dieselbe Symbolliste und dieselbe Schranke haben.

**Was die Korrektur an den Regeln ändert — und was nicht:**

* **Regel 4b (mindestens 3 Selektionsfalten) bleibt für alle neun erfüllt.**
  Kein Bot verliert eine Falte; keine Falte ist leer. Regel 4c
  („unterbestimmt") greift weiterhin für keinen der neun.
* ⚠️ **`t3_supertrend` hat in seiner Falte 2019 nur drei Symbole.** Die Falte
  zählt — Registertext 3b (a) unten sagt das jetzt ausdrücklich —, aber sie ist
  dünn, und das gehört berichtet, nicht versteckt.
* **Die Bestätigungsperiode wird bei sechs Bots kleiner** (Krypto-Tagesbots
  23 → 20, `t3_supertrend` 23 → 18, Aktien-Bots 150 → 147). Das ist keine
  Verschlechterung der Strategie, sondern die Korrektur einer Fehlmessung.

#### 16.1.2 „Symbole ohne Faltenevidenz" sind Listen **je Bot**

Heute steht in 15.5 **eine Liste je Markt** (krypto 6, aktien 1). Das ist
falsch: was der Loader nicht lädt, liefert auch keine Evidenz — und die Loader
haben **fünf verschiedene Schranken**. Die Listen fallen deshalb je Bot
auseinander.

> **Symbole ohne Faltenevidenz** (Tatsachennotiz zu 3b, **ersetzt die Fassung
> aus 15.5**; Lesart H, je Bot):
>
> | Bot | # | Symbole ohne Faltenevidenz |
> |---|---:|---|
> | `elliott_wave` | 11 | `BMTUSDT`, `ENAUSDT`, `ENSOUSDT`, `PEPEUSDT`, `PROMUSDT`, `PUMPUSDT`, `SUIUSDT`, `TRUMPUSDT`, `UUSDT`, `WLDUSDT`, `ZKCUSDT` |
> | `t3_supertrend` | 7 | `BMTUSDT`, `ENAUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `rsi2_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `turtle_soup_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `volatility_breakout_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `elliott_wave_stocks` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `rsi2_mean_reversion` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `turtle_soup_stocks` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `volatility_breakout` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
>
> Für diese Symbole gilt der gewählte Parametersatz live **ohne
> Faltenevidenz**. Das ist keine Nachlässigkeit, sondern die Kehrseite von 3d:
> wer sie hätte, hätte ein point-in-time-Universum und damit einen anderen Lauf.

⚠️ Bei den Aktien-Bots waren es **eingetragen `SNDK` allein**, gemessen sind es
**fünf**. Die vier zusätzlichen (`APP`, `CEG`, `GEV`, `HOOD`) sind nicht neu im
Universum — sie fallen an `MIN_HISTORY_DAYS = 1825` heraus, und das war in der
alten Notiz nicht abgebildet, weil die alte Messung diese Schranke nicht kannte.

#### 16.1.3 Die Klammer in 15.5 rechnet falsch — Rechenweg korrigiert

In der Tabelle *„Die Universumsdateien"* steht für `config/top25_symbols.txt`
**„24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)"**.

**Ergebnis 24 richtig, Rechenweg falsch.** Nachgemessen an der Datei mit dem
**eingetragenen** Hash `3afc95a4…`:

* Sie hat **25** nichtleere Zeilen, nicht 26.
* **`PAXGUSDT` steht nicht darin.** `shared/symbols_config.py:23` führt beide
  Namen in `EXCLUDE_SYMBOLS`, aber nur `XAUTUSDT` kommt in der Datei vor und
  wird tatsächlich gestrichen.

> **Korrigierter Rechenweg** (**ersetzt die Klammer in der Tabelle von 15.5**,
> die dort unverändert stehen bleibt):
>
> | Markt | Datei | SHA-256 | Symbole |
> |---|---|---|---:|
> | krypto | `config/top25_symbols.txt` | `3afc95a4f6b5ebc3a8f7bb7854b5dd59c4ecc4e3d86aa7b93c08066a3fccf810` | **24 (25 Zeilen abzüglich `XAUTUSDT`)** |
> | aktien | `config/sp500_top150.txt` | `6acba892f38e998cf43ae9e5594c4707945143aba481429c44a5c6005339f607` | 150 |
>
> Der Hash ist geprüft und unverändert — es ist **dieselbe Datei**, nur die
> Beschreibung daneben stimmte nicht.

---
#### 16.1.4 Eine vierte, in dieser Arbeit gefundene: „die fünf Werte"

Die Aufgabenstellung nennt drei falsche Tatsachennotizen. Beim maschinellen
Nachzählen ist eine **vierte** aufgefallen, und sie wird hier genannt statt
stillschweigend geglättet: Registertext 3b (b) spricht von **„den fünf
Werten"** von `MIN_HISTORY_*`. **Gezählt sind es vier** — 17 520 · 730 · 500 ·
1 825 — in zwei Einheiten. Die Zahl stammt aus TB-40 und ist dort schon falsch.

**Der Wortlaut bleibt unverändert**, weil er der registrierte ist; die
Tatsachennotiz daneben (in 16.7) sagt, was gezählt wurde. Das ist derselbe
Umgang wie bei 16.1.3: **Rechenweg korrigieren, Wortlaut stehen lassen.**

---

### 16.2 Die Lesart, die gilt: **H**

**Es gilt Lesart H: „an mindestens einem Handelstag der Falte handelbar."**

⚠️ **Das ist eine Bestätigung, keine Änderung** — es ist der Wortlaut von
Registertext 3b. TB-40 hat zusätzlich die Alternative **F** („am Faltenbeginn
geprüft") gemessen, weil die TB-40-Aufgabenstellung sie verlangte. Beides gehört
ins Journal, **in dieser Reihenfolge:**

1. **H wurde behalten, weil es registriert war.** Zum Zeitpunkt der Entscheidung
   war bekannt, dass F `elliott_wave` auf **2 von 3** Falten drücken (erste
   Falte: 0 Symbole) und ihn damit nach Regel 4c „unterbestimmt" machen würde.
   *Eine Wahl nach dem Ergebnis wurde bewusst vermieden.* Die Reihenfolge ist
   der Punkt: erst gilt, was registriert war; die Sachfrage kommt danach.
2. **H ist zusätzlich in der Sache richtig.** F beschreibt eine Strategie, die
   der Bot nicht handelt: ein Symbol, das im März handelbar wird, wird ab März
   gehandelt — F würde es für das **ganze Jahr** streichen. Die Falte ist ein
   Berichtszeitraum, kein Zulassungsstichtag.

Die Zahlenreihe unter F steht vollständig in
`docs/ERGEBNIS_TB-40_universum_trockenlauf.md`. Sie ist **nicht** eingetragen
und hat keinen Weg ins Urteil.

---

### 16.3 Registertext 5 — Datenstand *(ersetzt die Fassung aus 15.7 vollständig)*

> **(a)** Es gibt **zwei Kursdatenbestände**. `data/live/` wird täglich vor den
> Bot-Läufen von einem Cron aktualisiert und auf Frische geprüft (letzte
> abgeschlossene Kerze vorhanden, keine Teilkerze); **Forward-Tests und der
> Backtester-Vergleich (Registertext 7) lesen ausschliesslich daraus**.
> `data/snapshots/<hash>/` ist eine einmal erzeugte, danach **unveränderliche**
> Kopie; **der Selektionslauf liest ausschliesslich daraus**. Kein Modul eines
> Laufs ruft Kurse über das Netz ab.
>
> ⚠️ **ERSETZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026), 17.1.**
> Registertext 5a führt dort **Bestand** und **Snapshot** als Rollen statt als
> Pfade (`data/` und `snapshots/<hash>/` nur noch als Tatsachennotiz), nennt den
> Umfang der Eingaben (⭐ neben den Kursdateien **genau zwei**:
> `config/top25_symbols.txt`, `config/sp500_top150.txt`) und trennt
> **Snapshot-Hash** und **Datenstand-Hash**. Der Kern dieses Absatzes — der
> Selektionslauf liest ausschliesslich den Snapshot, kein Modul ruft Kurse über
> das Netz ab — **bleibt unverändert gültig** und ist dort wörtlich
> übernommen. ⭐ Neu hinzu kommt die Ausnahme `rand_erste` (17.3).
>
> **(b)** **Der Registerhash bezeichnet den Snapshot.** Der Live-Bestand wird
> nicht registriert; jede Auswertung, die ihn liest, protokolliert den Hash
> dessen, was sie gelesen hat, im Ergebnis.
>
> ⚠️ **PRÄZISIERT durch Abschnitt 17, 17.9** — nicht ersetzt. Als dieser Satz
> geschrieben wurde, gab es **einen** Hash. Seit TB-47 gibt es **zwei**;
> `d9449faf…` ist der **Datenstand-Hash** (der Kursdatenteil), der
> **Snapshot-Hash** ist ein eigener Wert
> (`4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608`,
> TB-47-Maclauf). Der Satz selbst bleibt gültig; 17.9 sagt nur, **welcher**
> Hash gemeint ist.
>
> **(c)** Der Snapshot wird **am Tag des signierten Tags** aus `data/live/`
> gezogen, danach nicht mehr. **Ein zweiter Snapshot ist ein neuer Lauf.**
>
> ⚠️ **ERSETZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026), 17.2.**
> „Am Tag des signierten Tags" liess die **Reihenfolge** offen. Korrigiert
> gilt: **der Snapshot wird VOR dem signierten Tag gezogen, und der Tag
> referenziert seinen Hash.** Der zweite Satz — ein zweiter Snapshot ist ein
> neuer Lauf — bleibt unverändert.
>
> **(d)** **Alle Daten- und Bot-Cronjobs laufen in UTC** (`TZ=UTC` in der
> Crontab oder launchd mit UTC), in der Reihenfolge Datenaktualisierung →
> Frischeprüfung → Bots.

**Dazu eine Prüfung, kein Abbruchkriterium:** Der Selektionslauf auf dem
Snapshot muss **auf einer zweiten Maschine bitidentisch reproduzieren**. Tut er
das nicht, ist der Snapshot unvollständig — ein Modul liest von woanders. *Das
ist vor dem Tag zu finden, nicht danach.* Die Prüfung erzeugt kein Urteil; sie
erzeugt einen Befund.

⚠️ **Der Umbau selbst ist nicht Teil dieses Nachtrags.** Er ist eine eigene,
grosse Aufgabe: **101 Module lesen heute `data/`.** Hier wird nur der
Registertext eingetragen. Bis der Umbau erfolgt ist, **fallen Registertext und
Umsetzung auseinander** — siehe 16.11, Zeile 1.

**Die alte Fassung (15.7) bleibt gültig, soweit sie Tatsachen festhält**, die
der neue Text nicht widerruft: der Hash über Binance-Dateien ist stabil, der
über yfinance-Dateien konstruktionsbedingt nicht (`auto_adjust=True`). Genau
diese Instabilität ist der Grund, warum (a) einen unveränderlichen Snapshot
verlangt: ein Bestand, der sich bei jedem Abruf um 10⁻⁶ verschiebt, kann nicht
zugleich die Grundlage eines registrierten Laufs sein.

---

### 16.4 Registertext 6 — Budgetstufen und Zellenbudget *(neu)*

**Die Budgetstufen-Leiter stand bisher nirgends im Repo.** Das ist ein Befund
aus TB-39: eine Sitzung musste sie **nachbauen**, um mit ihr arbeiten zu können.
*Jede Aufgabe, die sie nicht vorfindet, rät sie neu — und jede rät anders.*
Dieser Registertext beendet das.

#### Die Stufen

> **(a)** Jeder Bot steht auf einer von drei Stufen: **Schatten** (läuft, kein
> Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf),
> **Grundbudget** (im Buch), **Bestätigt** (im Buch, Rang-5-Gewichtung, sobald
> Netting existiert).
>
> **(b)** Nach dem Selektionslauf steht jeder Bot, der **kein** Abbruchkriterium
> erfüllt, auf **Grundbudget**; jeder, der eines erfüllt, auf **Schatten** —
> sein Budgetanteil hält die statische Benchmark-Position in Höhe seines
> mittleren Exposures. **Die Zuweisung ist Ergebnis des eingefrorenen Skripts,
> keine Lesung.**
>
> **(c)** **Aufstieg** Grundbudget → Bestätigt, geprüft am Ende jedes
> Kalenderquartals durch dasselbe Skript, frühestens nach **30 geschlossenen
> Trades und sechs Monaten** Bestätigungsperiode: Netto-Sharpe der
> Bestätigungsperiode > 0, **und** Netto-Calmar ≥ **0,5 ×** Netto-Calmar des
> Gewinners über die Selektionsfalten, **und** Max-Drawdown der
> Bestätigungsperiode nicht tiefer als die tiefste Selektionsfalte des
> Gewinners. *(30 Trades, sechs Monate und 0,5 sind **willkürlich**; 0,5 ist
> eine fremde Faustregel, keine Messung dieses Projekts.)*
>
> **(d)** **Abstieg** auf Schatten, quartalsweise: Max-Drawdown tiefer als
> **1,25 ×** die tiefste Selektionsfalte des Gewinners, **oder** Netto-Sharpe
> < 0 nach **60** geschlossenen Trades. **Rückkehr nur über einen neuen
> registrierten Lauf.**
>
> **(e)** Zwischen den Quartalsprüfungen ändert sich keine Stufe. **Kein
> Betreiberentscheid setzt eine Stufe hinauf; der Betreiber kann einen Bot
> jederzeit auf Schatten setzen (Notbremse), aber nie hinauf.**
>
> **(f)** **D5 (Echtgeld)** setzt für jeden beteiligten Bot die Stufe
> **Bestätigt seit mindestens zwei Quartalsprüfungen in Folge** voraus.

> ⭐ **16.4 (b) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (a) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (b) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (c) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (d) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

#### Das Zellenbudget

> **(g)** **Zellen sind Quelle × Anlage.** Heute:
>
> | Zelle | Bots |
> |---|---|
> | Fortsetzung × Aktien | `volatility_breakout` |
> | Umkehr × Aktien | `rsi2_mean_reversion`, `turtle_soup_stocks`, `elliott_wave_stocks` |
> | Fortsetzung × Krypto | `t3_supertrend`, `volatility_breakout_crypto` |
> | Umkehr × Krypto | `rsi2_crypto`, `turtle_soup_crypto`, `elliott_wave` |
>
> Jeder Bot gehört zu **genau einer** Zelle; **die Zuordnung steht im Register
> und ändert sich nur mit dem Bot.**
>
> **(h)** Eine Zelle ist **aktiv**, wenn mindestens ein Bot darin auf
> Grundbudget oder Bestätigt steht. **Aktive Zellen teilen das Buch zu gleichen
> Teilen.** *Gleichteilung ist willkürlich; sie ist die einzige Aufteilung, die
> kein Ergebnis verwendet.*
>
> **(i)** Innerhalb einer Zelle teilen die Bots nach **Stufenfaktor: Schatten 0,
> Grundbudget 1, Bestätigt 2** *(Faktor 2 willkürlich)*. Anteil = eigener Faktor
> / Summe der Faktoren der Zelle.
>
> **(j)** **Aufstieg:** mehr vom **Zellenbudget**; das Zellenbudget ändert sich
> nicht. **Abstieg:** Zellenbudget **bleibt**, die übrigen teilen es nach (i).
> **Wird die Zelle inaktiv, geht ihr Budget in die statische
> Benchmark-Position ihrer Anlage — nicht an andere Zellen.**
>
> **(k)** Wird eine **neue Zelle aktiv**, steigt die Zahl aktiver Zellen und
> alle Zellenanteile sinken entsprechend. **Das ist die einzige Umverteilung
> zwischen Zellen, und sie folgt aus Zulassung, nicht aus Ergebnis.**
>
> **(l)** ⭐ **Anlageklassen-Schlüssel, Betreiberentscheid vom 16.09.2026:
> Aktien 80 / Krypto 20.** Er skaliert die Zellen einer Anlage gemeinsam und
> gilt, bis Netting (Rang 5) existiert.
>
> **(m)** **Umsetzung ohne gemeinsames Konto:** Das Leiter-Skript berechnet
> quartalsweise je Bot einen Multiplikator auf dessen heutige statische
> Positionsgrösse:
>
> `m_b = (Zellenanteil × Klassenschlüssel × Bot-Anteil in der Zelle) / (1/9)`
>
> **Die Bots lesen `m_b`; sonst ändert sich nichts.**

> ⭐ **16.4 (m) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (h) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (l) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (h) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (j) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (k) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (l) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (j) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (i) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (j) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (i) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (h) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **16.4 (g) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

#### ⭐ Das Prinzip, das (j) und (k) trägt

> **Die Leiter bewegt Bots. Sie bewegt keine Zellen.** Out-of-Sample-Evidenz
> über einen Bot ist Evidenz über eine **Implementierung**, nicht darüber, dass
> die Ertragsquelle seiner Zelle mehr Kapital verdient. Schrumpfte die Zelle
> beim Abstieg, würde ein Bot für das Versagen eines anderen bestraft — **und
> das Kapital ginge dorthin, wo es zufällig besser lief.**

#### Die Begründung des Schlüssels 80/20 — mit ihrer Messung

Gemessen über **2 271 gemeinsame Handelstage**, 2017-08-18 bis 2026-09-01:

| | Krypto | Aktien |
|---|---:|---:|
| Jahresschwankung | **74,7 %** | **19,6 %** |
| Verhältnis | **3,82 ×** | |
| Korrelation | **0,32** | |

**Bei 60/40 kämen 80 % des Risikos aus Krypto.** Gleicher Risikobeitrag läge bei
**79/21**; 80/20 ist die gerundete Fassung davon und als Betreiberentscheid
eingetragen, nicht als Rechenergebnis.

⚠️ **Der Ertrag wurde bewusst nicht gemessen.** Der Zeitraum enthält einen der
grössten Krypto-Aufschwünge; eine Ertragszahl daraus würde den Schlüssel nach
dem Ergebnis setzen, und genau das soll die Vorregistrierung verhindern.

#### Prüfung vor dem Tag

Das Leiter-Skript muss aus **jeder** möglichen Stufentabelle — **3⁹ = 19 683**,
trivial aufzählbar — einen **eindeutigen** Multiplikatorvektor erzeugen,
**ohne Eingabe des Betreibers**. *Ein Fall, in dem es fragt, ist ein Fall, in
dem das Register unvollständig ist.* Auch das ist eine Prüfung mit Befund, kein
Abbruchkriterium.

⚠️ **Das Leiter-Skript existiert noch nicht.** Siehe 16.11, Zeile 3.

> ⭐ **Evidenz der Leiter: siehe 46.4 (f); Lesarten: TB-116** (Fable 27a R13
> (f), TB-117, 26.09.2026). Die Prüfung vor dem Tag oben bleibt
> zeichengleich.

> ⭐ **16.4, „Prüfung vor dem Tag“ PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 16.5 Registertext 7 — Backtester-Prüfung *(neu)*

> Vor dem Selektionslauf wird für jeden Bot der **simulierte Kapitalpfad mit
> heutigen Parametern** gegen den **Papierpfad seit dem Umstellungstag**
> gestellt (gleiche Kerzen, gleiche Kosten). Berichtet werden: Anteil
> übereinstimmender Signale, Korrelation der Tagesrenditen, Summe der
> Abweichung. Ein Bot, dessen Signalübereinstimmung unter **95 %** liegt
> *(willkürlich)*, wird im Selektionslauf ausgewertet, aber mit dem Vermerk
> **„Backtester nicht bestätigt"**, und kann bis zur Klärung **nicht über
> Schatten hinaus**.

**Ergänzung — der Boden unter der Schwelle:**

> **Unterhalb einer Mindestzahl von Signalen wird die Übereinstimmung
> berichtet, aber nicht bewertet.** Der Bot gilt dann als **„Backtester nicht
> geprüft"**, nicht als „nicht bestätigt".
>
> *Begründung: `volatility_breakout` (Aktien) erzeugt bei 21 Tagen
> Median-Haltedauer in drei Monaten möglicherweise zwölf Signale; bei acht
> reisst ein einziger Unterschied die 95 % (8/9 = 88,9 %, 7/8 = 87,5 %). Eine
> Schwelle ohne Boden trifft nach **Handelsfrequenz** statt nach **Qualität** —
> derselbe Fehler wie die gestrichene 10-Trades-Regel (Registertext 1c).*
>
> ⚠️ **Die Mindestzahl ist vom Betreiber festzulegen und als willkürlich zu
> kennzeichnen.** Sie steht bis dahin als **offen** im Register; ohne sie ist
> Registertext 7 nicht anwendbar, sondern nur berichtsfähig.

**Die Abweichung zwischen Live- und Snapshot-Bestand:**

> Live- und Snapshot-Bestand weichen in adjustierten Aktienkursen bis **10⁻⁵**
> relativ voneinander ab; Signalabweichungen an Schwellen sind dadurch möglich
> **und werden gezählt** — nicht weggerechnet, nicht als Rauschen abgetan.

**Der Umstellungstag** ist **`2026-09-16T04:42:24Z`**, für **alle neun Bots**
derselbe, belegt in `docs/umstellungstag_entscheidungskerze.json` (TB-38).

> ⚠️ **Papierpfade vor diesem Tag gelten für den Vergleich Backtest gegen Live
> als nicht vergleichbar.** Vor dem Umstellungstag entschieden die Bots auf der
> **laufenden** Kerze (Teilkerze), danach auf der **Entscheidungskerze**. Das
> ist eine andere Regel, nicht dasselbe Verfahren mit Rauschen.

⚠️ **Der Vergleich ist heute noch nicht gebaut.** Siehe 16.11, Zeile 4.

⚠️ **ERGÄNZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026) — an drei
Stellen; dieser Registertext bleibt im Wortlaut stehen:**

| | |
|---|---|
| **17.6** | Der **Kein-Entscheid-Tag**: ein Tag ohne bestimmbare Entscheidungskerze zählt **nicht** in die Quote, offene Positionen bleiben unverändert; über **5 %** der Handelstage gilt das Fenster als „Holdout beeinträchtigt" |
| **17.7** | ⭐ **Die oben als „vom Betreiber festzulegen" offen gelassene Mindestzahl ist festgelegt: n = \|Vereinigung\| ≥ 20**, abgeleitet aus der 95-%-Schwelle als 1 / (1 − 0,95) und nachgerechnet (18/19 = 94,7 % reisst sie, 19/20 = 95,0 % nicht). Dort ist auch die **Vergleichsmenge** benannt — Ereignispaare (Symbol, Tag), Ein- und Ausstiege, Quote als \|Schnitt\| / \|Vereinigung\| — und das Urteil unterhalb der Mindestzahl heisst **„unbestimmt"** |
| **17.8** | **Drift**: weicht der Bestand zum Vergleichszeitpunkt vom protokollierten Datenstand-Hash ab, ist die Abweichung je Symbol **Drift**, keine Verfahrensabweichung. ⚠️ Die Zählregel oben (bis 10⁻⁵ zwischen Live- und Snapshot-Bestand **werden gezählt**) bleibt davon unberührt — 17.8 betrifft **denselben** Bestand zu **zwei Zeitpunkten** |

---

### 16.6 Registertext 2d — Embargo *(ersetzt die Fassung aus 15.4 vollständig)*

> Die Bestätigungsperiode eines Bots beginnt am **ersten Handelstag nach
> Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen
> ist.** Der Tag wird aus den Positionsdaten bestimmt und im Journal vermerkt.
> **Obere Schranke** ist die Zeitbremse des Bots, falls vorhanden; **für Bots
> ohne Zeitbremse das 95. Perzentil der Haltedauer plus 1** — für
> `t3_supertrend` **13 Handelstage** (P95 = 11,21).
>
> ⚠️ **Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt
> die Bestätigungsperiode trotzdem — diese Position wird in der
> Bestätigungsstatistik jedoch nicht gezählt** (Attribution je Position,
> ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).

**Was sich gegenüber 15.4 ändert:** Das Embargo war dort eine **feste Frist**
(Zeitbremse + 1, Tage im Embargo gehören zu keiner Periode). Jetzt ist es eine
**Bedingung am Bestand** mit der alten Frist als **Deckel**. Der Grund: die
feste Frist verschenkt Bestätigungstage, wenn der Bot früher flach ist, und sie
reicht nicht, wenn er es nicht ist — beides ohne Not.

**Die gemessenen Embargo-Werte aus 15.4 bleiben** als obere Schranken gültig,
soweit sie der neuen Fassung nicht widersprechen; die Tabelle dort ist
unverändert weiterzulesen.

⚠️ **`elliott_wave_stocks` = 91 Handelstage ist bestätigt.** `MAX_HOLD_HOURS =
90` wird bei diesem Bot als **90 Tagesbalken** gelesen — der Kommentar im Bot
sagt es ausdrücklich („entspricht ~90 Handelstage"), und 15.4 Anmerkung 3 hat
es an der Kursreihe nachgemessen.

> **Folge, die ins Register gehört:** Die Bestätigungsperiode beginnt für
> `elliott_wave_stocks` **rund vier Monate später als für die anderen acht**
> (91 Handelstage Deckel gegen 11 bis 16). Wer die neun Bestätigungsperioden
> nebeneinander liest, liest für diesen einen Bot einen deutlich kürzeren
> Zeitraum — das ist kein Fehler, sondern seine Haltedauer.

> ⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d,
> TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse — das 95.
> Perzentil der Haltedauer plus 1 — wird aus den **gefundenen** Trades
> gerechnet, nicht als Maximum über das Raster; er ist keine Leckschranke, das
> Leck schliesst die Attribution je Position (**41.3, C2**). (2) Die Bedingung
> („keine vor Go-Live eröffnete Position mehr offen") wird im Selektionslauf
> **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet;
> das Journal des Papierpfads ist dafür keine Quelle (**41.3, C3**). (3) Fables
> Berichtigung aus 24c, `purge_tage` als Schranke über das Raster zu bemessen,
> ist zurückgenommen und nie eingetragen worden (**41.2 B2, 41.3 C1**). Der
> Registertext oben bleibt zeichengleich.

> ⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 16.7 Registertext 3b — Ergänzungen (a) bis (e) *(neu; die Fassung in 15.5 bleibt stehen)*

> **(a)** Eine Selektionsfalte zählt, wenn der Loader des Bots in ihr
> **mindestens ein Symbol** an mindestens einem Handelstag handelbar macht. **Es
> gibt keine Mindest-Symbolzahl je Falte.**
>
> **(b)** `MIN_HISTORY_*` ist **je Bot mit seinem Namen und seiner Einheit**
> fest auf dem heutigen Wert; **die fünf Werte stehen im Register**:
>
> | Bot | Name | Wert | misst |
> |---|---|---:|---|
> | `elliott_wave` | `MIN_HISTORY_HOURS` | **17 520** | **Kerzenzahl** (`len(df)`) |
> | `t3_supertrend` | `MIN_HISTORY_DAYS` | **730** | Zeitspanne in Tagen |
> | `rsi2_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `turtle_soup_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `volatility_breakout_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `elliott_wave_stocks` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `rsi2_mean_reversion` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `turtle_soup_stocks` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `volatility_breakout` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
>
> ⚠️ **Bei Kerzenzählung hängt die Handelbarkeit eines Symbols von der
> Lückenfreiheit der Reihe ab** — eine Reihe mit derselben Zeitspanne, aber
> Lücken, fällt bei `elliott_wave` heraus und bei den anderen acht nicht (in
> TB-40 am Verhalten gemessen, Fall *luecke_gleiche_spanne*). Der Snapshot
> friert das ein, der Live-Bestand kann abweichen — **Registertext 7 zählt
> solche Fälle.**

⚠️ **Tatsachennotiz zu 3b (b) — eine vierte falsche Zahl, in TB-41 gefunden und
hier festgehalten statt stillschweigend geglättet:** Der Wortlaut sagt „die
**fünf** Werte". **Gezählt sind es über die neun Bots vier verschiedene
Zahlenwerte** — **17 520 · 730 · 500 · 1 825** — in **zwei** Einheiten
(Kerzenzahl und Zeitspanne). Die Zahl „fünf" stammt aus
`docs/ERGEBNIS_TB-40_universum_trockenlauf.md` („Fünf verschiedene Werte und
zwei verschiedene Grössen") und ist dort schon falsch; die Tabelle darunter
zeigt in beiden Dokumenten dieselben vier Werte. **Der Wortlaut bleibt
unverändert stehen, weil er der registrierte ist; massgeblich ist die
Tabelle.** `research/registernachtrag_tb41/pruefe_register.py` zählt die Werte
in den neun Bot-Dateien nach und meldet jede Abweichung von **vier Werten in
zwei Einheiten**.
>
> ⚠️ **(c) ERSETZT durch Abschnitt 23 (Berichtigung TB-66, 20.09.2026), 23.3 — der Wortlaut bleibt stehen.**
>
> **(c)** ⭐ **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3 — **wird auf den in dieser Falte geladenen
> Symbolen des Bots gerechnet, nicht auf dem vollen Universum. Bot und
> Benchmark leben in derselben Menge.**
>
> **(d)** **Berichtet je Bot und Falte, ohne dass ein Kriterium daran hängt:**
> Symbolzahl, Anteil am Universum, **Liste der ausgelassenen Symbole mit Grund**
> (Historie zu kurz / Kursdatei fehlt / Kerzenzahl zu klein), und nach dem Lauf
> die **Faltenkohärenz** — Spearman-Rangkorrelation der
> Parametersatz-Rangfolge dieser Falte gegen die Rangfolge nach dem Median der
> übrigen Falten. *Eine Falte mit Kohärenz nahe null hat als Rauschen gewirkt;
> das steht im Bericht, damit der I10-Lauf es gegen eine Zahl prüfen kann.*
>
> **(e)** Die Listen **„Symbole ohne Faltenevidenz" werden je Bot geführt**
> (Tatsachennotiz in 16.1.2).

> ⭐ **16.7 (d) ERGÄNZT durch R38 (48.6)** (Fable 29b R38, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Die Einordnung, die dazugehört:**

> Die drei Symbole der Falte 2019 von `t3_supertrend` sind **BTC, ETH und BNB**
> — die drei, die aus der 2019er-Landschaft in die heutige Liste überlebt
> haben. **Die frühen dünnen Falten sind die Stelle, an der die in Registertext
> 3c eingetragene Survivorship-Verzerrung am grössten ist** — kein neues
> Problem, sondern das bekannte in seiner sichtbarsten Form. Wer 2019 mit drei
> Symbolen rechnet, rechnet mit den drei Gewinnern von 2019.

---

### 16.8 Kandidatenregeln *(neuer Registertext)*

> **(a)** **Kandidaten werden nie gegeneinander gerankt.** Zulassung ist je
> Kandidat **absolut**, gegen die **Null** — das Buch ohne diesen Kandidaten —,
> nie gegen einen anderen Kandidaten. *Die Null ist kein Kandidat, sondern der
> Vergleich, den jeder Kandidat hat.*
>
> **(b)** **N ist die Rastergrösse. Neue Kandidaten bekommen kein Raster** — sie
> treten mit einem festen Satz aus der Literatur an (N = 1). Ein Raster
> frühestens **nach der ersten Bestätigungsperiode**, als eigener registrierter
> Lauf.
>
> **(c)** **Familienbuchführung:** Im Register werden geführt — geprüfte
> Kandidaten, zugelassene, und die erwarteten Fehlzulassungen als Summe.
>
> **(d)** Eine **Reihenfolge nach Prior** ist zulässig: Sie ist eine
> Ressourcenentscheidung, keine Schwelle. **Sie steht im Register, bevor der
> erste Kandidat läuft.**
>
> **(e)** ⭐ **Overlay-Kandidaten** — Regeln, die auf bereits selektierte Bots
> wirken — werden **erst nach dem Selektionslauf registriert**; ihre Zulassung
> hängt an der **Bestätigungsperiode**, nicht an den Falten. *Begründung:
> gestapelte Selektion — ein Overlay wird auf denselben Daten geprüft, auf denen
> die Bots gewählt wurden, und sein Ergebnis hängt von dieser Wahl ab. Die
> Falten sind für ein Overlay kein unabhängiger Boden mehr.*

---

### 16.9 Vorab-Filter *(neuer Registertext)*

> Vor jeder Methodikprüfung und vor jedem Backtest eines Kandidaten:
>
> **(a) Darf der Betreiber das überhaupt handeln?** *(Regulierung am Wohnsitz.
> Diese Klausel hat am 16.09.2026 den Funding-Carry erledigt: keine
> Binance-Derivate für Privatanleger mit Wohnsitz in Deutschland.)*
>
> **(b) Ist das konkrete Instrument für ihn zugelassen?** *(Diese Klausel hätte
> `S-B1` und `S-A2` erledigt: US-domizilierte ETFs sind für EU-Privatanleger
> wegen fehlendem PRIIPs-Basisinformationsblatt gesperrt — auch die gehebelten
> und inversen.)*
>
> **(c) Ko-Einstiegsquote** der Signale gegen jeden vorhandenen Bot derselben
> Anlage. **Über 1,5 ⇒ gleiche Zelle ⇒ Variante, kein Kandidat.**

*Warum das ein Filter und keine Kennzahl ist: (a) und (b) kosten nichts, wenn
man sie zuerst stellt, und kosten einen ganzen Lauf, wenn man sie zuletzt
stellt. Beide Beispiele sind keine Konstruktionen — sie sind an je einem
Kandidaten nachträglich aufgefallen.*

---

### 16.10 Vorbedingung für short-fähige Sleeves *(neuer Registertext)*

> **(a)** Eine Short-Position ist **nur in Indexinstrumenten** zulässig, **nie
> in Einzelaktien**. *Begründung: grösster Tagesanstieg S&P 500 rund **+12 %**
> (13.10.2008), Einzelaktien **+50 %** und mehr (Squeeze). Nur im ersten Fall
> ist der Verlust je Tag mit einer Notional-Grenze beherrschbar.*
>
> **(b)** Je Short-Position **Notional-Obergrenze 20 % des Sleeve-Budgets**
> *(willkürlich)*; der registrierte **Stress-Tagesverlust** ist Notional ×
> grösster historischer Tagesanstieg des Underlyings — **aus den Daten, nicht
> gesetzt**.
>
> **(c)** Ein **Stop liegt als Order beim Broker**, nicht im Cron; die
> Simulation nimmt den Fill **zum Stress-Sprung** an, nicht zum Stop-Kurs.
>
> **(d)** Short-Notional zählt im Netting als **Brutto-Exposure der
> Anlageklasse**.
>
> **(e)** ⭐ **Abbruch, unabhängig von jeder Kennzahl:** Ein realisierter
> Tagesverlust einer Short-Position **über dem registrierten
> Stress-Tagesverlust** setzt den Sleeve auf **Schatten**. *Das ist keine
> Leistungsprüfung, sondern die Feststellung, dass das Risikomodell verletzt
> wurde.*

⚠️ **Registertext 6 braucht dafür keine eigene Stufe.** Der Kapitalpfad ist
durch (b) und den Stress-Sprung nach unten begrenzt; eine vierte Stufe „Short"
würde eine Grenze verdoppeln, die schon steht.

---

### 16.11 Wo Registertext und Umsetzung auseinanderfallen

**Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.** Hier ist die vollständige Liste, Stand
16.09.2026:

| # | Registertext | Was der Code heute tut | Wer schliesst die Lücke |
|---:|---|---|---|
| 1 | **5 (a)–(c)** — `data/live/` und `data/snapshots/<hash>/` | Es gibt **einen** Ordner `data/`; **101 Module** lesen ihn direkt. Kein Snapshot, keine Frischeprüfung, kein Live/Snapshot-Schnitt. | eigene Aufgabe (Datenordner-Umbau) |
| 2 | **5 (d)** — alle Cronjobs in UTC | Die Crontab ist in dieser Aufgabe **nicht angefasst** worden; ob `TZ=UTC` gesetzt ist, ist hier nicht geprüft. | Betreiber, beim Umbau |
| 3 | **6 (a)–(m)** — Budgetstufen, Zellen, `m_b` | **Kein Leiter-Skript.** Kein Bot liest einen Multiplikator; alle neun rechnen mit fester Positionsgrösse (faktisch 1/9). Die 3⁹-Prüfung kann noch nicht laufen. | eigene Aufgabe (`m_b` in die `forward_test.py`) |
| 4 | **7** — Backtester-Prüfung | **Kein Vergleichswerkzeug.** Papierpfad und simulierter Pfad werden heute nirgends gegeneinander gestellt; die 95-%-Schwelle hat nichts zu messen. | eigene Aufgabe |
| 5 | **7, Mindestzahl Signale** | **Offen — Betreiber.** Bis die Zahl feststeht, ist Registertext 7 berichtsfähig, aber nicht anwendbar. | Betreiber |
| 6 | **2d** — Embargo als Bedingung am Bestand | `research/vorregistrierung/auswertung.py` kennt nur das **alte** feste Embargo (und rechnet ohnehin nach Verfahren A, 15.8 Nr. 3). Die Datei ist **eingefroren**. | TB-30b |
| 7 | **3b (a)–(e)** — Loader entscheidet, Benchmark auf geladenen Symbolen, Faltenkohärenz | Gemessen ist das nur **einmal**, im Trockenlauf von TB-40. Der spätere Auswerter tut es noch nicht; `faltenplan_neun` beantwortet dieselbe Frage weiter nach Lesart A. | TB-30b |
| 8 | **3b (d)** — Liste der ausgelassenen Symbole mit Grund | **Drei Bots sortieren lautlos aus** (`rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` melden bei zu kurzer Historie und fehlender Kursdatei **keine Zeile**, TB-40 Abschnitt 4). Die Liste liesse sich heute nicht aus den Logs erzeugen. | eigene Aufgabe (Logging-Fix, freigegeben) |
| 9 | **6, Zellenzuordnung** | Steht jetzt im Register, aber **nirgends im Code** — kein Modul kennt Zellen. | mit dem Leiter-Skript |
| 10 | **16.10** — short-fähige Sleeves | **Kein Bot kann short.** Der Registertext ist reine Vorbedingung für einen Kandidaten, den es noch nicht gibt. | wenn der erste Short-Kandidat antritt |
| 11 | **16.1.1** — die korrigierte Symbolzahl | `research/universum_trockenlauf/universum_trockenlauf.py` liest als „eingetragene" Zahl weiter die **erste** Tabelle mit der Kopfzeile „Symbolzahl je Selektionsfalte" — das ist die **historische** Fassung in 15.5. Ein erneuter Lauf meldet deshalb wieder acht Abweichungen, obwohl das Register jetzt stimmt. Das Werkzeug ist in dieser Aufgabe **unberührt** (Belegquelle). | mit TB-30b, wenn der Auswerter das Werkzeug übernimmt |

**Zwei Stellen, an denen es *nicht* auseinanderfällt** — beide geprüft, nicht
angenommen:

⚠️ **Fortschreibung (18.09.2026, TB-48 — angehängt, nichts entfernt):**
**Zeile 5 dieser Tabelle ist erledigt.** Die Mindestzahl Signale ist in
**17.7** festgelegt (n ≥ 20, als willkürlich abgeleitet aus der 95-%-Schwelle);
Registertext 7 ist damit nicht mehr „offen — Betreiber". *Die übrigen zehn
Zeilen stehen unverändert.* **Sieben weitere Lücken kommen mit Abschnitt 17
hinzu** — sie stehen in **17.10**, nicht hier, damit diese Tabelle den Stand
vom 16.09.2026 behält. ⚠️ **Die dringendste davon:** `shared/snapshot.py`
**kann den Snapshot heute nicht ziehen** — es wirft bei jedem
Teilkerzen-Befund, und es gibt 36 (17.10, Zeile 2).


* **Die fünf `MIN_HISTORY_*`-Werte** in 16.7 (b) sind aus den neun Bot-Dateien
  **gelesen** und werden maschinell dagegen geprüft.
* **Der Umstellungstag** `2026-09-16T04:42:24Z` in 16.5 stimmt für **alle neun**
  Bots mit `docs/umstellungstag_entscheidungskerze.json` überein.

---

### 16.12 Was dieser Nachtrag nicht tut

* **Kein Selektionslauf.** Es ist weiterhin kein Raster gerechnet, kein
  Parametersatz bewertet, kein Ergebnis erzeugt. **Kein Amendment.**
* **Kein Datenordner-Umbau.** `data/live/` und `data/snapshots/` sind
  **Registertext**, nicht Wirklichkeit — 101 Module lesen weiter `data/`.
* **Kein Logging-Fix** für die drei lautlos aussortierenden Bots (freigegeben,
  eigene Aufgabe).
* **Kein `m_b` in den `forward_test.py`** (freigegeben, eigene Aufgabe).
* **Keine Umstellung von `auswertung.py` auf Verfahren B** — die Datei ist
  **unberührt** und bleibt eingefroren.
* **Kein Snapshot, kein signierter Tag, kein Zeitanker.** Das ist der nächste
  Schritt und gehört dem Betreiber.
* **Keine Parameterübernahme.** `live_params.py`, `forward_test.py`,
  `equity_simulation.py`, `multi_symbol_optimise.py` und
  `multi_symbol_walk_forward.py` sind in dieser Arbeit nur **gelesen** worden.
* **Keine Kursdatei angefasst.** Der Datenstand ist unverändert
  `d9449faf51bffaaa…` bei 223 Dateien — als Test nachgewiesen.
* **`research/faltenplan_neun/`, `research/universum_trockenlauf/`,
  `research/etf_trendfolge/` unberührt** — sie sind die Belegquellen.
* **Nichts unter `broker/` oder `shared/`, keine Crontab, kein
  `results/*.csv`.**

*Nachgetragen in TB-41, 16.09.2026. Kein Amendment: kein Selektionslauf, kein
signierter Tag, keine Parameterübernahme.*

---

