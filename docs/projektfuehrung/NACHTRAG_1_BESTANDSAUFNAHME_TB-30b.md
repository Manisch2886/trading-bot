# Nachtrag 1 zur Bestandsaufnahme TB-30b — die Aussicht ist ein Befund: `auswertung.py` folgt Verfahren B

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53) · **Nr. 2 von 3**
(Vorgänger: `BESTANDSAUFNAHME_TB-30b.md`; Nachfolger: `NACHTRAG_2_…`)
**Abgelegt:** 21.09.2026, 23:33 Ortszeit · **HEAD zur Messzeit:** `6071f32`
(= `origin/main`; jünger als `a0c6eb0`)
**Art:** lesende Messung. ⛔ **Kein Byte geändert.** Keine Freigabe verbraucht.

> ⚠️ **Berichtigung, 21.09.2026 nach Fable 21l Punkt 3:** Herkunftszeile und
> HEAD-Ordnung nachgetragen. Die Uhrzeit 23:32 war **gemessen** (`current_time`)
> und ist richtig; abgelegt wurde die Datei um 23:33. **Am Inhalt ist nichts
> geändert.**
**Bezug:** `BESTANDSAUFNAHME_TB-30b.md`, Abschnitt 4 — dort als *„Aussicht, kein
Befund"* stehengelassen, mit ausdrücklicher Nennung dessen, was fehlte.

⭐⭐ **Die Reihenfolge hat gehalten, und sie ist hier der Punkt:** Die
Bestandsaufnahme hat die Frage gestellt **und die Grenze der Messung benannt**,
bevor gemessen wurde (*„Gemessen ist die Schnittstelle zum Faltenplan, nicht die
Auswertungslogik selbst"*). Die Messung kann die Frage also nicht gewählt haben
— **Bauart 24.3.**

---

## 1. Das Kriterium, vor der Messung festgelegt

**Registertext 0 (15.2), wörtlich:**

> *„Die Selektion ist eine einmalige Auswahl über das vollständige Raster. Jeder
> Rasterpunkt wird auf jeder Selektionsfalte ausgewertet; Selektionsstatistik
> ist der Median der Falten-Sharpes; Gewinner nach Plateau-Regel. Es gibt kein
> Trainingsfenster und keine faltenweise Auswahl."*

**Und die Unterscheidung aus 15.1:**

| | Verfahren A (Walk-Forward) | **Verfahren B (gilt)** |
|---|---|---|
| Auswahl | **je Falte ein Gewinner** | **einmalig über das ganze Raster** |
| Out-of-Sample | die Testfalten | **allein die Bestätigungsperiode** |

⇒ **Das prüfbare Merkmal:** Verfahren A gruppiert **je Falte** und wählt darin;
Verfahren B gruppiert **je Rasterpunkt (Zelle)** und nimmt den Median **über**
die Falten.

---

## 2. ⭐⭐ Die Messung — `auswertung.py`, 678 Zeilen, 21.09.2026

### (a) Die Selektionsstatistik, wörtlich (Zeilen 225–228)

```python
def selektionsstatistik(df: pd.DataFrame, selektionsfalten: list) -> pd.Series:
    """Festlegung 2: Median des Netto-Sharpe ueber die Selektionsfalten."""
    teil = df[df["falte"].isin(selektionsfalten)]
    return teil.groupby("zelle_id")["netto_sharpe"].median()
```

⇒ ⭐ **Die Falten werden gefiltert, dann wird über ZELLEN gruppiert und der
Median über die Falten gebildet.** Das ist Registertext 0, Satz für Satz.

### (b) ⭐ Die Gegenprobe: jedes `groupby` im ganzen Skript

| Zeile | Gruppierung |
|---:|---|
| 178 | `df.groupby("zelle_id")` |
| 228 | `teil.groupby("zelle_id")` |
| 471 | `zul.groupby("zelle_id")` |

⇒ ⭐⭐ **Alle drei auf `zelle_id`. Keines auf `falte`.** Eine faltenweise
Auswahl — das definierende Merkmal von Verfahren A — **existiert nicht**.

### (c) Die Wortprobe

| Suchwort | Treffer | |
|---|---:|---|
| `walk_forward` / `walkforward` | **0** / **0** | — |
| `faltenweise` | **0** | — |
| `je_falte` | **0** | — |
| `training` / `embargo` / `purge` | **0** / **0** / **0** | (aus Abschnitt 4 der Bestandsaufnahme) |
| `median` | 7 | ⭐ Verfahren B |
| `plateau` | 14 | ⭐ Verfahren B, `plateau()` Z. 271, Gewinner = höchstes Plateau-Mittel Z. 295 |
| `bestaetigung` | 11 | ⭐ Verfahren B — OOS allein die Bestätigungsperiode |

---

## 3. ⭐⭐⭐ Die Folge: alle drei Gründe aus 15.8 Nr. 3 sind überholt

**15.8 Nr. 3 (16.09.2026) nennt drei Gründe**, warum `auswertung.py` in TB-30b
umgebaut werden müsse:

| # | Grund, wörtlich | Stand 21.09.2026 | erledigt durch |
|---:|---|---|---|
| 1 | *„es liest `faltenplan.py` mit Trainingsfenstern, Purge und Embargo zwischen den Falten"* | ⭐ **Überholt.** `auswertung.py` bezieht den Plan über **einen** Aufruf (Z. 589) und liest **vier Felder**; keines davon ist Training, Purge oder Embargo. `faltenplan.py` selbst rechnet seit **TB-80** gegen den Horizontbeginn | TB-80 (21.09.) |
| 2 | *„es kennt für Krypto nur Platzhalter"* | ⭐ **Überholt.** Genau **eine** `status`-Zuweisung im ganzen `faltenplan.py` (`"endgueltig"`, Z. 310, gemeinsame Funktion `_plan`); `plan_krypto` ruft dieselbe Funktion. Die drei Platzhalter-Wachen greifen bei **keinem** der neun Bots | TB-61 (20.09.) |
| 3 | *„rechnet ohnehin nach Verfahren A"* | ⭐⭐ **Überholt — das ist die Messung dieses Nachtrags.** Kein `groupby("falte")`, kein Walk-Forward-Wort, Median über Falten je Zelle, Plateau-Regel, OOS = Bestätigungsperiode | war offenbar **nie** der Fall |

⇒ ⭐⭐⭐ **`auswertung.py` muss für TB-30b nicht geöffnet werden.** Das
Einfrieren aus Abschnitt 0 (*„vor dem Lauf geschrieben und eingefroren"*) und die
Sperrlistenpunkte 3, 5 und 14 bleiben unberührt — **und der Widerspruch, den die
Bestandsaufnahme in Abschnitt 4 benannt hat, löst sich auf.**

### ⚠️ Was das ausdrücklich NICHT heisst

| ⛔ | |
|---|---|
| ⛔ | **Kein Lauf.** Dies ist eine statische Messung an Fundstellen und drei Codezeilen. Dass `auswertung.py` gegen `beispieldaten.py` durchläuft, sagt erst ein Lauf; `test_vorregistrierung.py` (150 Prüfungen) ist **nicht** ausgeführt worden |
| ⛔ | **Posten 6 der Bestandsaufnahme ist damit nicht komplett erledigt.** Registertext **2d** (Embargo als Bedingung am Bestand) und **3b (a)–(e)** (Loader entscheidet, Benchmark auf geladenen Symbolen, Faltenkohärenz) bleiben **eigene** Fragen. Die Tabellenzeile 2080 nennt `auswertung.py` als Ort — ⚠️ **ob das nach dieser Messung noch stimmt, ist ungeprüft** |
| ⛔ | **Der Registertext wird hier nicht geändert.** 15.8 Nr. 3 ist Registertext und bleibt zeichengleich stehen; dieser Nachtrag ist eine **Messung**, die ihr Ergebnis daneben legt — **wo sie eingetragen wird, entscheidet der Betreiber, und ob sie Fable vorzulegen ist, ebenfalls** |

---

## 4. ⚠️ Ein achter Posten, in der Bestandsaufnahme noch nicht enthalten

**15.1 sagt, wörtlich:**

> *„die **sechs** bot-eigenen Walk-Forward-Rechner werden später **ersetzt**, nicht umgestellt — das ist **TB-30b**"*

**Gemessen 21.09.2026:** Es gibt **neun** `strategies/*/multi_symbol_walk_forward.py`,
einen je Bot, und **keiner ist ein Stub**:

| Bot | Zeilen | Bot | Zeilen |
|---|---:|---|---:|
| `elliott_wave` | 107 | `turtle_soup_crypto` | 138 |
| `elliott_wave_stocks` | 109 | `turtle_soup_stocks` | 138 |
| `rsi2_crypto` | 157 | `volatility_breakout` | 153 |
| `rsi2_mean_reversion` | 168 | `volatility_breakout_crypto` | 142 |
| `t3_supertrend` | 90 | | |

⚠️ **Das wird hier als Abweichung gemeldet, nicht als Fehler behauptet.** Die
Zahl „sechs" kann sich auf einen früheren Bestand beziehen oder auf sechs Bots,
deren Rechner tatsächlich im Einsatz sind — **beides ist hier nicht gemessen**.

⇒ **Posten 8 für TB-30b:** *neun* Walk-Forward-Rechner **ersetzen** (nicht
umstellen), und vorher klären, worauf sich „sechs" bezog.

⭐ **Der Posten ist nicht dringlich für den Tag:** Verfahren B braucht keinen
Walk-Forward-Rechner. Dringlich ist nur, dass die neun **nicht** benutzt werden,
solange sie Verfahren A rechnen — und das ist eine Wache, kein Umbau.

---

## In einfacher Sprache

Die Bestandsaufnahme von vorhin endete mit einer Hoffnung und dem ausdrücklichen
Hinweis, dass sie noch nicht nachgemessen ist. **Jetzt ist sie nachgemessen, und
sie stimmt.**

Im Regelwerk steht seit dem 16. September, das zentrale Auswertungsskript müsse
vor dem grossen Tag umgebaut werden — und ausgerechnet dieses Skript soll
eigentlich **unantastbar** sein. Genannt waren drei Gründe. **Alle drei treffen
heute nicht mehr zu:** Zwei wurden am 20. und 21. September durch andere
Arbeiten erledigt; der dritte — das Skript rechne noch nach dem alten Verfahren
— war, soweit die Messung reicht, **offenbar nie richtig**.

Der Beleg ist schlicht: Das alte Verfahren sucht **pro Zeitabschnitt einen
Gewinner**. Das neue sucht **einen Gewinner über alles**. Im Skript kommt die
Gruppierung „pro Zeitabschnitt" an **keiner einzigen Stelle** vor — es gruppiert
dreimal, und jedes Mal pro Parametersatz.

⚠️ **Zwei Einschränkungen, die dazugehören:** Ich habe **gelesen, nicht laufen
lassen** — das Skript wurde nicht ausgeführt. Und eine kleinere Teilfrage (das
Embargo als Zusatzbedingung) bleibt offen.

**Und ein neuer Punkt:** Das Regelwerk spricht von „sechs" alten
Auswertungsrechnern in den Bots. **Gemessen sind es neun.** Das ist gemeldet,
nicht bewertet — wichtig ist nur, dass keiner von ihnen für den grossen Lauf
benutzt wird.
