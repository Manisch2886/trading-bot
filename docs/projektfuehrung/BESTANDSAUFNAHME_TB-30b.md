# Bestandsaufnahme TB-30b — was der Auftrag wirklich umfasst, und ein Befund, der ihn kleiner macht

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53) · **Nr. 1 von 3**
(Nachfolger: `NACHTRAG_1_…`, `NACHTRAG_2_…`)
**Abgelegt:** 21.09.2026, 23:31 Ortszeit · **HEAD zur Messzeit:** `6071f32`
(= `origin/main`; ⭐ **jünger** als `a0c6eb0`, an dem die Anfrage 21f misst —
`a0c6eb0` ist TB-81 Schritt 1, `6071f32` dessen Abschlussbeleg)
**Art:** lesende Vorarbeit. ⛔ **Kein Byte geändert** — weder in `strategies/`
noch in `research/`. Keine Betreiberfreigabe verbraucht.

> ⚠️ **Berichtigung, 21.09.2026 nach Fable 21l Punkt 3.3:** Der Kopf nannte
> zuvor *„Stand: 21.09.2026, 23:55"*. **Das war falsch** — die Uhrzeit war
> geschätzt und nicht gemessen; die Datei entstand um 23:31. ⭐ Für ein
> Dokument, das eine Reihenfolge belegen soll (Frage vor Messung), zählt das.
> Fables Beanstandung ist berichtigt, die Herkunftszeile und die HEAD-Ordnung
> sind nachgetragen (21l Punkte 3.1 und 3.2). **Am Inhalt ist nichts geändert.**
**Anlass:** TB-30b ist der nächste grosse Schritt vor dem signierten Tag und war
bisher nur als *„die vier Optimierer plus die Wache"* geführt. Das ist er nicht.

---

## 1. ⚠️ TB-30b ist ein Sammelposten aus sieben Registerstellen, nicht ein Auftrag

**Gemessen:** `grep -n "TB-30b" docs/VORREGISTRIERUNG_neuselektion.md` → 13
Fundstellen. Danach gelesen und zusammengestellt:

| # | Posten | Fundstelle | Umfang |
|---:|---|---|---|
| **1** | **Regimewache einbauen** — `t3_supertrend` überspringt seinen BTC-Regimefilter stillschweigend, wenn `BTCUSDT` fehlt | **11.1** | ⭐ **Die Wache steht fertig und geprüft** in `shared/regimewache.py` (16 Prüfungen). Einzubauen an **drei** Stellen. `regimewache.pruefe_einbau()` beantwortet maschinell, ob es geschehen ist |
| **2** | **Kapital-Drawdown nachrüsten** — `evaluate_combination_multi` liefert `max_drawdown_kapital_pct` nicht mit | **11.2** | ⭐ Agent 2 schaltet **von selbst** von Stufe 2 auf Stufe 1 der `ZIELMASS_KASKADE`, sobald das Feld da ist. Heute rechnet er auf dem Stellvertreter und **weist ihn als Stellvertreter aus** |
| **3** | **Zwei Achsen durchreichen** — `SMA_TREND_PERIOD = 200` ist Konstante statt Parameter; `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` stehen in `live_params.py`, aber nicht im Optimierer | **11.3** | betrifft `rsi2_mean_reversion`, `volatility_breakout`, `volatility_breakout_crypto` |
| **4** | **`entry_cutoff` je Bot aus dem Register** statt je Symbol aus `df["open_time"].max()` | **26.1**, Registerzeile 4446 | die vier Aktien-Optimierer. ⚠️ **Siehe Abschnitt 2 — ein Bot fällt aus der Reihe** |
| **5** | **Die Wache** *„frühester Einstieg ≥ Beginn der ersten Selektionsfalte"*, samt Mutationsprobe | **29.4** | in den vier `multi_symbol_optimise.py`, **nicht** in `auswertung.py` (Fables Rücknahme in 21b) |
| **6** | **Embargo als Bedingung am Bestand** (Registertext 2d) und **Loader/Benchmark/Faltenkohärenz** (3b (a)–(e)) | Tabelle Z. 2080/2081 | ⚠️ **beide auf `auswertung.py` verwiesen — siehe Abschnitt 4** |
| **7** | **Symbolzahl im Trockenlauf-Werkzeug** (16.1.1) und **`MIN_HISTORY_DAYS`-Angleichung** (15.8 Nr. 4) | Z. 2085, 15.8 Nr. 4 | Werkzeugpflege, *„wenn der Auswerter das Werkzeug übernimmt"* |

⭐ **Posten 1 und 2 sind Sperrbedingungen, keine Wünsche.** Sperrliste,
Schlusssatz, wörtlich: *„Der Lauf darf nicht beginnen, bevor die beiden
Bug-Fixes aus Abschnitt 11 eingebaut sind."*

---

## 2. ⚠️⚠️ Posten 4 gemessen: drei Bots sind ein Einzeiler, der vierte nicht

**Gemessen über alle neun `strategies/*/multi_symbol_optimise.py`:**

| | Befund |
|---|---|
| ⭐ | **Genau die vier Aktien-Bots** tragen `RECENT_YEARS_ONLY = 10`. Die fünf Krypto-Bots tragen es **nicht** — was zu Register 33.2 passt, wo sie „kein Horizont" haben |
| ⚠️ | Die Zeile ist bei allen vier dieselbe Bauart: `df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` — ⭐ **die Datenuhr, je Symbol**, also genau das, was TB-80 in `faltenplan.py` beseitigt hat |

**⚠️ Aber die Semantik ist nicht dieselbe:**

| Bot | Zeile | was geschieht | Folge |
|---|---:|---|---|
| `volatility_breakout` | 86–91 | `entry_cutoff` wird **als Filter weitergereicht**; `compute_indicators(df)` läuft auf der **vollen** Historie | Umstellung = **ein Wert** ändern |
| `rsi2_mean_reversion` | 91–96 | dito | dito |
| `turtle_soup_stocks` | 79–83 | dito | dito |
| ⚠️⚠️ **`elliott_wave_stocks`** | **92–98** | **kappt den DataFrame selbst**: `df = df[df["open_time"] >= cutoff]` — und die `MIN_HISTORY_DAYS`-Prüfung läuft **danach** | ⇒ Die Umstellung ändert **auch, welche Daten die Indikatoren sehen** und **welche Symbole die Handelbarkeitsprüfung überstehen** |

⇒ ⚠️ **Für `elliott_wave_stocks` ist die Umstellung keine Wertänderung, sondern
eine Änderung am Datenschnitt.** Das gehört gemessen, **bevor** es beauftragt
wird — nicht währenddessen entdeckt.

*Zweiter Unterschied, derselbe Posten:* `df["open_time"].max()` ist **je Symbol**
verschieden (ein 2022 gelistetes Symbol hat ein anderes Maximum als ein seit
2010 gelistetes); der Horizontbeginn aus 28.4 ist **ein einziges Datum für
alle**. ⛔ **Wie viele Symbole das bewegt, ist hier NICHT gemessen** — es gehört
in den Auftrag.

---

## 3. Posten 5 gemessen: heute gibt es in keinem der neun Optimierer eine Wache

**Gemessen** (`assert`/`raise`/„Wache" je Datei): **alle neun → 0.**

⇒ Die Wache aus 29.4 ist ein **Ersteinbau**, keine Änderung. ⭐ Und sie gilt der
Sache nach für alle neun Bots — die fünf Krypto-Bots haben zwar keinen Horizont,
aber sehr wohl eine **erste Selektionsfalte** (Register 33.2).

⚠️ **Das ist eine offene Frage an den Auftragszuschnitt:** 29.4 sagt *„in den
vier `multi_symbol_optimise.py`"*. Ob die fünf Krypto-Optimierer die Wache
ebenfalls bekommen, ist damit **nicht entschieden** — und die Wache wäre dort
nicht leer, weil `t3_supertrend`, `rsi2_crypto` und `elliott_wave` erste Falten
haben, die **später** liegen als ihr erster handelbarer Tag.

---

## 4. ⭐⭐ Der Befund: zwei von drei Sätzen über `auswertung.py` sind überholt

**Die Lage, wie sie im Register steht** (15.8 Nr. 3, 16.09.2026):

> *„`auswertung.py` rechnet weiterhin nach **Verfahren A** — es liest
> `faltenplan.py` mit Trainingsfenstern, Purge und Embargo zwischen den Falten,
> und es kennt für Krypto nur Platzhalter. … Die Datei ist **eingefroren** …
> Ihre Umstellung ist **TB-30b**."*

⚠️ **Das wäre der grösste Posten überhaupt** — `auswertung.py` steht **dreifach**
auf der Sperrliste (Punkte 3, 5, 14), und Registerzeile 4447 sagt: *„ein
eingefrorenes Skript, das einmal geöffnet wird, ist nicht mehr eingefroren."*

### Gemessen, 21.09.2026, an `research/vorregistrierung/auswertung.py` (678 Zeilen, 26 Funktionen)

| Suchwort | Treffer |
|---|---:|
| `training` | **0** |
| `embargo` | **0** |
| `purge` | **0** |
| `krypto` | **0** |
| `faltenplan` | 7 |

⭐ **Die Datei trägt keine einzige Verfahren-A-Grösse selbst.** Sie bezieht den
Plan über **genau einen** Aufruf — `plan = fp.faltenplan(mess)`, Zeile 589 — und
liest daraus **vier Felder**:

| Zeile | gelesen |
|---:|---|
| 177, 325 | `plan[bot]["falten"]` |
| 432 | `plan[bot]["bestaetigungsperiode"]` |
| 458 | `plan[bot]["status"]` |
| 464 | `plan[bot]["selektionsfalten"]` |

⭐ **Alle vier liefert `faltenplan.py` heute** (Zeilen 334, 336, 310, 335).

### Und die „Platzhalter" sind Wachen, kein Rest

Die drei Treffer auf „Platzhalter" (Zeilen 327, 434, 460) sind **Abbrüche**, und
der Wortlaut ist der richtige:

> *„Ohne Falten gibt es keine Selektion — und keine Zahl, die so tut als gäbe es eine."*

**Greifen sie heute?** Gemessen: **genau eine** `"status"`-Zuweisung im ganzen
`faltenplan.py` — `"endgueltig"`, Zeile 310, in der gemeinsamen Funktion
`_plan`. Und `plan_krypto` trägt im Docstring:

> *„Seit TB-61 (20.09.2026) derselbe Plan wie bei Aktien, `status` `endgueltig`. Bis dahin ein Platzhalter mit Regel, der auf TB-31 wartete; TB-31 und TB-34 sind erledigt."*

⇒ ⭐⭐ **Die Platzhalter-Wachen greifen heute bei keinem der neun Bots.**

### Was das heisst — und was ausdrücklich NICHT

| | |
|---|---|
| ⭐ | **„kennt für Krypto nur Platzhalter" ist überholt** — erledigt durch **TB-61**, nicht durch TB-30b |
| ⭐ | **„liest `faltenplan.py` mit Trainingsfenstern, Purge und Embargo" ist überholt** — `auswertung.py` liest vier Felder, keines davon; und `faltenplan.py` selbst ist durch **TB-80** auf den Horizontbeginn umgestellt, **ohne dass `auswertung.py` geöffnet wurde** |
| ⛔⛔ | **„rechnet nach Verfahren A" ist NICHT widerlegt.** Gemessen ist die **Schnittstelle** zum Faltenplan, **nicht** die Auswertungslogik selbst — Selektionsstatistik, Plateau-Regel, Spitzen-Schwelle. Ob die Verfahren A oder B folgt, ist hier **nicht** gemessen und bleibt offen |
| ⛔ | **Das ist eine statische Messung an Fundstellen, kein Lauf.** Dass `auswertung.py` gegen `beispieldaten.py` durchläuft, sagt erst ein Lauf. `test_vorregistrierung.py` (150 Prüfungen) ist hier **nicht** ausgeführt worden |

⇒ ⭐ **Die Aussicht, die das eröffnet:** Wenn die Auswertungslogik Verfahren B
schon folgt, muss `auswertung.py` für TB-30b **gar nicht geöffnet werden** — und
das Einfrieren aus Abschnitt 0 hält, statt vor dem Tag gebrochen zu werden.
⚠️ **Das ist eine Aussicht, kein Befund.** Der Posten, der sie entscheidet, ist
**Posten 6** (Registertext 2d und 3b), und er ist ungemessen.

---

## 5. Was diese Vorarbeit ausdrücklich nicht getan hat

| ⛔ | |
|---|---|
| ⛔ | **Kein Code geändert** — nicht ein Byte in `strategies/`, `research/` oder `shared/` |
| ⛔ | **Kein Test ausgeführt** — weder `test_vorregistrierung.py` noch `test_regimewache.py` |
| ⛔ | **Nicht gemessen, wie viele Symbole** die Umstellung von der Datenuhr auf den Horizontbeginn bewegt |
| ⛔ | **Nicht gemessen**, ob die Auswertungslogik Verfahren A oder B folgt (Posten 6) |
| ⛔ | **Keine Empfehlung zum Rastern, keine Kennzahl, kein Parametersatz** — Sichtschutz 27.1 unberührt |

---

## 6. ⚠️ Vorschlag zum Zuschnitt — Entscheidungsvorlage, nicht vollzogen

**Sieben Posten in einem Auftrag sind zu viel** — TB-78 bis TB-81 haben gezeigt,
dass ein Auftrag mit klarem Abbruchkriterium sauber durchläuft und ein
überladener nicht.

| Vorschlag | Inhalt | Warum zuerst |
|---|---|---|
| **TB-30b/1** | ⭐ **Posten 1 und 2** — Regimewache an drei Stellen, Kapital-Drawdown in `evaluate_combination_multi` | ⭐ **Beide sind Sperrbedingungen für den Lauf**, beide haben fertigen, geprüften Code und ein **maschinelles Abnahmekriterium** (`regimewache.pruefe_einbau()`, Stufenwechsel der Kaskade) |
| **TB-30b/2** | **Posten 4 und 5** — `entry_cutoff` aus dem Register und die Wache, samt Mutationsprobe | ⚠️ Braucht vorher eine **Messung zu `elliott_wave_stocks`** (Abschnitt 2) und eine **Entscheidung**, ob die fünf Krypto-Optimierer die Wache bekommen (Abschnitt 3) |
| **TB-30b/3** | **Posten 6** — und zwar ⭐ **zuerst als Messung**: folgt die Auswertungslogik Verfahren A oder B? | ⛔ **Erst danach** entscheidet sich, ob `auswertung.py` geöffnet werden muss. **Das Öffnen braucht eine eigene Betreiberfreigabe und eine Verfahrensfrage an Fable** |
| **TB-30b/4** | **Posten 3 und 7** — Achsen durchreichen, Werkzeugpflege | kleinster Hebel, kann zuletzt |

⚠️ **Zwei Fragen, die vor der Beauftragung beim Betreiber liegen:**

1. **Bekommen die fünf Krypto-Optimierer die Wache aus 29.4 auch?** Der Wortlaut
   sagt „die vier"; die Sache spricht für alle neun.
2. **Darf `auswertung.py` geöffnet werden, wenn Posten 6 es verlangt?** ⭐ *Erst
   messen, dann fragen* — die Messung aus TB-30b/3 kann die Frage erübrigen.

---

## In einfacher Sprache

Der nächste grosse Arbeitsschritt hiess bisher „die vier Optimierer plus eine
Wache". **Gemessen sind es sieben Posten**, verteilt über sieben Stellen im
Regelwerk — darunter **zwei, ohne die der grosse Lauf laut Regelwerk gar nicht
starten darf**. Für die ist der Code schon fertig und geprüft; er muss nur
eingebaut werden.

Zwei Dinge sind dabei aufgefallen:

**Erstens ein Stolperstein.** Drei der vier Aktien-Bots rechnen ihren Startpunkt
auf dieselbe Art; beim vierten (`elliott_wave_stocks`) ist es anders gebaut —
dort **schneidet** der Startpunkt die Kursdaten ab, statt nur die Geschäfte zu
filtern. Eine Umstellung ändert dort also mehr, als es aussieht. Besser jetzt
gemessen als mitten im Auftrag entdeckt.

**Zweitens eine gute Nachricht.** Im Regelwerk steht seit dem 16. September, das
zentrale Auswertungsskript müsse umgebaut werden — und dieses Skript ist
eigentlich **unantastbar**. Nachgemessen: **Zwei der drei Gründe sind
inzwischen erledigt**, durch Arbeiten vom 20. und 21. September. Das Skript holt
sich den Auswertungsplan über **eine einzige Zeile** und liest daraus **vier
Angaben** — von den alten Begriffen kommt keiner darin vor.

⚠️ **Der dritte Grund ist offen** und noch nicht nachgemessen. Wenn er sich
ebenso auflöst, muss das unantastbare Skript **gar nicht angefasst werden** —
und eine der grössten Sorgen vor dem grossen Tag wäre keine mehr. Das ist eine
**Aussicht, kein Ergebnis**; die Messung dazu steht noch aus.
