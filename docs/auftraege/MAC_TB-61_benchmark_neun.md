# TB-61 Benchmark-Tabelle für alle neun Bots — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-61 Benchmark neun Bots`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main` — kein Zweig, kein PR
(Regelweg, `ARBEITSWEISE.md` Abschnitt 5b).

⚠️ **Diese Aufgabe rechnet.** Sie braucht `trading-env` und die Kursdateien in
`data/`. Die Geräteanbindung kann sie nicht ausführen — sie liest das Repo, sie
rechnet nicht darin.

---

## 0. Warum es diese Aufgabe gibt — jede Zahl unten ist gemessen, keine geschätzt

**Gemessen am 20.09.2026 über die Geräteanbindung, rein lesend, an `79742d1`:**

`research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` ist für **alle
neun Bots** überholt — nicht nur für die fünf, die als Platzhalter markiert sind.

| Bot | `status` in der Datei | `falten` in der Datei | nach Register Abschnitt 21 |
|---|---|---|---|
| `elliott_wave` | `platzhalter` | *leer* | **2018–2019**, 4 Falten |
| `t3_supertrend` | `platzhalter` | *leer* | **2019**, 7 Falten |
| `rsi2_crypto` | `platzhalter` | *leer* | **2019**, 7 Falten |
| `turtle_soup_crypto` | `platzhalter` | *leer* | **2018**, 8 Falten |
| `volatility_breakout_crypto` | `platzhalter` | *leer* | **2018**, 8 Falten |
| `elliott_wave_stocks` | `endgueltig` | **2019**–2026 | ⚠️ **2017**, 9 Falten |
| `turtle_soup_stocks` | `endgueltig` | **2019**–2026 | ⚠️ **2017**, 9 Falten |
| `rsi2_mean_reversion` | `endgueltig` | **2019**–2026 | ⚠️ **2018**, 8 Falten |
| `volatility_breakout` | `endgueltig` | **2019**–2026 | ⚠️ **2018**, 8 Falten |

⚠️⚠️ **Der Befund, der über den Auftragsanlass hinausgeht: die vier Aktien-Bots
tragen in dieser Datei noch die Falten der entfernten Schranke `2019`.** Sie
stehen dort als `endgueltig` und sind es nicht. *Ein Zustand, der sich selbst
als fertig bezeichnet, ist gefährlicher als einer, der sich Platzhalter nennt.*

### Warum die fünf Krypto-Bots Platzhalter sind — die Ursache besteht nicht mehr

`research/vorregistrierung/faltenplan.py:216`, `plan_krypto()`, Docstring:

> `"""Platzhalter MIT REGEL - keine Jahreszahlen bis TB-31 gemeldet hat."""`

und im Rückgabewert hart `"status": "platzhalter"`. `benchmark.py:176` prüft
`if p["status"] != "endgueltig"`, schreibt den Hinweis *„der Faltenplan dieses
Marktes haengt an TB-31"* und springt mit `continue` weiter. **Deshalb ist
`dd_toleranz` bei diesen fünf leer.**

**Gemessen, dass die Bedingung erfüllt ist:**

| | |
|---|---|
| TB-31 | **erledigt**, PR #105 (Journal AJ) |
| TB-34 | **erledigt**, Kursbestand neu aufgebaut — `data/` enthält **223 Dateien**, gezählt; Datenstand `d9449faf…`/223 nach Backlog Zeile 1243 |
| Krypto-Faltenplan | **steht gemessen** in Register Abschnitt 21, gerechnet von `research/faltenplan_neun/` |

⇒ ⭐ **Der Platzhalter wartet auf ein Ereignis, das eingetreten ist.**

### Was dieser Lauf mitschliesst

⭐ **Der eine unerwartet rote Test erklärt sich damit vollständig.**
`test_vorregistrierung.py` fällt mit `KeyError: '2017'` an
`auswertung.py:237` — dort steht `falte = eintrag["falten"][z["falte"]]`. Der
Faltenplan liefert seit Abschnitt 21 die Falte `2017`; die Benchmark-Tabelle
beginnt bei `2019`. **Der Test ist nicht kaputt, er zeigt genau diesen
Widerspruch an.**

⚠️ **Nicht gemessen, sondern erschlossen:** dass er nach dem Lauf grün wird.
Das ist zu **prüfen**, nicht vorauszusetzen — siehe Nachweis 7.

---

## 1. ⛔ Die Sperre, die diese Aufgabe NICHT bricht

**Register Abschnitt 21.9, Betreiberentscheidung vom 19.09.2026, wörtlich:**

> Bis dahin bleibt
> `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` byteweise
> unverändert; die neu gerechnete Tabelle liegt als eigene Datei daneben.

⛔ **Diese Aufgabe überschreibt `benchmark_drawdowns.json` NICHT.** Sie erzeugt
`benchmark_drawdowns_neu.json` daneben.

⚠️ **Gemessen, warum das eine Code-Änderung erzwingt:** `benchmark.py::main()`
hat **keinen Ausgabeschalter**. Zeile 227 lautet

```
ziel = os.path.join(_HIER, "ergebnisse", "benchmark_drawdowns.json")
```

**Ein Lauf von `benchmark.py` in seiner heutigen Form überschreibt die gesperrte
Datei.** Deshalb ist Schritt 2 dieser Aufgabe, den Schalter einzubauen — vor
jedem Lauf.

**Gegenprobe am Ende, hart:** SHA-256 von `benchmark_drawdowns.json` muss nach
dieser Aufgabe unverändert

```
a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee
```

lauten. Das ist derselbe Wert, der in Register 21.6 eingetragen ist, und er ist
am 20.09.2026 an `79742d1` nachgemessen worden.

---

## 2. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt, bevor du anfängst.** Der Nachweis
„Arbeitsbaum sauber" wird **danach** geprüft, nicht davor. Findest du nichts,
sag es und mach weiter.

### Schritt 1 — messen, bevor du etwas änderst

Rechne `research/faltenplan_neun/faltenplan_neun.py` und halte seine neun
Faltenpläne **gegen die Tabelle in Abschnitt 0 oben**.

⚠️ **Stimmen sie nicht überein, brich ab und melde es.** Ändere nichts. Eine
Abweichung hier heisst, dass entweder das Register oder das Werkzeug nicht den
Stand hat, den ich gemessen habe — und das ist ein Befund, keine Arbeitsgrundlage.

### Schritt 2 — der Ausgabeschalter

`benchmark.py` bekommt ein `--ziel`-Argument. Ohne Angabe bleibt das heutige
Verhalten unverändert.

⛔ **Nur der Schalter. Keine Rechenlogik anfassen** — nicht
`drawdown_bei_exposure`, nicht `bh_tagesrenditen`, nicht `point_in_time`, nicht
die Medianbildung. Diese Funktionen stehen auf der Sperrliste, Punkt 4 und
Punkt 6.

**Sichern: commit und push.** *(Nicht im selben `&&`-Block wie der Commit —
siehe Abschnitt 4.)*

### Schritt 3 — `plan_krypto()` liefert den gemessenen Plan

`research/vorregistrierung/faltenplan.py`, `plan_krypto()` gibt den Faltenplan
nach derselben Regel zurück, nach der `plan_aktien()` ihn gibt, und setzt
`"status": "endgueltig"`.

⭐ **Der Docstring sagt, was ihn ablöst** (`DOKUMENTATIONSSTANDARD.md` Regel 9):
dass der Platzhalter bis TB-61 auf TB-31 wartete, dass TB-31 und TB-34 erledigt
sind, und dass der Plan jetzt aus der Datenlage kommt. **Das Abgelöste wird
entfernt, nicht danebengestellt** — der alte Docstring-Text geht raus.

Ebenso raus: der Hinweistext in `benchmark.py:177` *„haengt an TB-31"* und die
Zeile `print(f"\n{bot}: Platzhalter (TB-31)")` in `main()`, **sobald kein Bot
mehr Platzhalter ist.** Bleibt einer, bleibt auch der Zweig — dann melde, welcher.

**Sichern: commit und push.**

### Schritt 4 — der Lauf

```
trading-env/bin/python3 research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_neu.json
```

### Schritt 5 — der Vergleich, und er gehört ins Ergebnisdokument

Für **alle neun Bots** und die Exposure-Stufen **25 %, 50 %, 100 %**: alter Wert,
neuer Wert, Differenz.

⭐ **Vier davon sind in Register 21.6 vorausgesagt.** Halte sie dagegen:

| Bot | 25 % | 50 % | 100 % |
|---|---|---|---|
| `rsi2_mean_reversion` | −2,18 → **−3,35** | −4,33 → **−6,61** | −8,55 → **−12,89** |
| `volatility_breakout` | −2,18 → **−3,35** | −4,33 → **−6,61** | −8,55 → **−12,89** |
| `elliott_wave_stocks` | unverändert | unverändert | unverändert |
| `turtle_soup_stocks` | unverändert | unverändert | unverändert |

⚠️ **Weicht der Lauf davon ab, ist das ein Befund und kein Fehler des Laufs.**
Berichte die gemessene Zahl, nicht die vorausgesagte. *Eine Vorhersage, die man
zur Sollgrösse macht, misst nichts mehr* — und die Zahlen in 21.6 wurden mit
einem anderen Werkzeug gerechnet als mit diesem hier.

**Sichern: commit und push.**

### Schritt 6 — die Abgabe

`docs/ERGEBNIS_TB-61_benchmark_neun.md` mit den Nachweisen aus Abschnitt 3,
und ein Journal-Nachtrag.

**Sichern: commit und push.**

---

## 3. Die Nachweise, die diese Aufgabe schuldet

| # | Nachweis |
|---:|---|
| **1** | `git status --short` **vor** dem ersten Schreiben |
| **2** | ⭐ **SHA-256 von `benchmark_drawdowns.json` nach der Aufgabe** — muss `a163c498…36d1ee` sein. *Das ist der Nachweis, dass die Sperre gehalten hat* |
| **3** | Die neun Faltenpläne aus Schritt 1 gegen die Tabelle in Abschnitt 0 — Zeile für Zeile |
| **4** | `git diff --numstat` je geänderter Datei |
| **5** | ⭐ Der Vergleich aus Schritt 5, alle neun Bots, drei Stufen |
| **6** | `status` je Bot in der **neuen** Datei — erwartet neunmal `endgueltig`. Steht dort etwas anderes, melde **welcher Bot und warum**, und lass ihn stehen |
| **7** | ⭐ `trading-env/bin/python3 -m pytest research/vorregistrierung/` — **mit dem Ergebnis je Testdatei, nicht nur der Summe.** Insbesondere: ist der `KeyError: '2017'` weg? ⚠️ Wird er es nicht, ist das **das wichtigste Ergebnis dieser Aufgabe** und gehört an den Anfang des Ergebnisdokuments |
| **8** | Nichts ausserhalb `research/vorregistrierung/` und `docs/` geändert |

⚠️ **Zu Nachweis 7, damit es nicht untergeht:** Der Test steht in Register 21.9
als *„offen durch eigene Änderung — blockierend für den Tag"* geführt.
**Solange er rot ist, blockiert er den Tag.** Wird er grün, ist das im
Ergebnisdokument ausdrücklich zu vermerken, weil eine Registerangabe damit
überholt ist.

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **`benchmark_drawdowns.json` wird nicht überschrieben.** Nachweis 2 |
| ⛔ | **Keine Rechenlogik in `benchmark.py`.** Nur der Ausgabeschalter |
| ⭐ | **Sichern nach jedem fertigen Teil, nicht am Ende.** Vier Commits sind oben benannt. *Begründung: TB-59 und TB-60 haben ihre Arbeit fertiggestellt und nie committet — elf Stunden bzw. vierzig Minuten ungesichert, beide Male durch einen Abbruch der SSH-Verbindung* |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block.** Gemessen: verkettet zweimal nicht durchgelaufen, allein zweimal sofort erfolgreich. ⚠️ **Die Ursache ist nicht gemessen** — die Abhilfe kommt ohne sie aus |
| ⭐ | **Jede SOLL-Zahl ist gezählt, nicht geschätzt** (`K2o`). Das gilt auch für Zahlen in deinem Ergebnisdokument |
| ⭐ | **Ein Messergebnis wird gegen eine zweite, unabhängige Zählung gehalten**, bevor es als Nachweis gilt |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** TB-59 hat das an zwei Stellen getan und hatte beide Male recht. *Ein falsches SOLL in einem Auftrag ist gefährlicher als eines in einem Bericht — hier liest es jemand als Anweisung* |

---

## 5. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Die gesperrte Datei ersetzen.** Das ist das Amendment und braucht eine eigene Betreiberfreigabe — nach 21.9 und Sperrliste 10.1 |
| ⛔ | **Den Tag setzen** |
| ⛔ | **Registertexte ändern.** Berichtigungen am Register gehen über eine eigene Aufgabe; hier wird nur gerechnet und berichtet |
| ⛔ | **`MINDESTTRAINING_JAHRE` anfassen.** Siehe Abschnitt 6 — das ist eine offene Frage, keine Aufgabe |
| ⛔ | **Die zwei Code-Kopien der Faltenschranke** in `research/faltenplan_neun/faltenplan_neun.py:120` und `research/krypto_historie/faltenplan.py:64` (`T56b.6`). Eigene Aufgabe, eigener Lauf |

---

## 6. ⚠️ Ein Befund zum Melden, nicht zum Lösen

**Gemessen, zwei Stellen, die sich widersprechen:**

| Fundstelle | Wortlaut |
|---|---|
| `research/vorregistrierung/registerdaten.py:108` | `MINDESTTRAINING_JAHRE = 4  # vor der ersten Falte` — angewandt in `benchmark.py:190` als point-in-time-Schranke |
| `research/etf_trendfolge/register.py:347` | `FALTEN_MINDESTTRAINING = None  # Verfahren B kennt keines` |

⚠️ **Ob das ein Widerspruch oder zwei verschiedene Dinge sind, ist nicht
gemessen.** Möglich ist beides: „kein Trainingsfenster für die Selektion" und
„ein Symbol tritt erst nach vier Jahren Historie in eine Falte ein" können
nebeneinander gelten.

⛔ **Entscheide das nicht.** Es ist eine Verfahrensfrage vor dem Tag und geht an
den Betreiber. **Berichte nur, welchen Wert dein Lauf benutzt hat und an welcher
Zeile** — damit später niemand raten muss.

---

## In einfacher Sprache

**Was wir wissen wollen:** Die Tabelle, die für jeden Bot festlegt, wie tief er
fallen darf, bevor er ausscheidet, ist veraltet. Bei fünf Bots ist sie leer, bei
den anderen vier steht sie auf Jahren, die nicht mehr gelten. Diese Aufgabe
rechnet sie neu — **daneben, nicht darüber.**

**Warum daneben:** Die alte Tabelle darf sich erst ändern, wenn du das
ausdrücklich freigibst. Das hast du am 19.09. so entschieden, und die Aufgabe
hält sich daran. Am Ende wird geprüft, dass die alte Datei Byte für Byte
dieselbe geblieben ist.

**Was du danach bekommst:** Eine Gegenüberstellung alt gegen neu für alle neun
Bots. Für zwei davon steht die erwartete Zahl schon fest — sie werden
nachgiebiger, bei voller Positionsgrösse von −8,55 auf −12,89 Prozent. Ob die
Rechnung das bestätigt, zeigt der Lauf.

**Und ein Nebeneffekt, auf den wir hoffen:** Der eine Test, der seit Tagen rot
ist, sucht das Jahr 2017 in einer Tabelle, die erst 2019 beginnt. Nach diesem
Lauf könnte er grün werden. Falls nicht, ist das der wichtigste Satz im Bericht.
