# TB-46b — Was tun die neun Bots mit offenen Positionen, wenn Kursdaten fehlen?

**Ergebnis einer autonomen Cloud-Sitzung, 17.09.2026.**
Vorgänger: TB-45 (Messung) · TB-46 (gemergt `135c306`) · Zweig `claude/new-session-ql406l`
Werkzeug: [`research/ausstiegspfade/probe.py`](../research/ausstiegspfade/probe.py) ·
Rohdaten: `research/ausstiegspfade/ergebnisse/probe.json` ·
Untersuchungsbericht: [`research/ausstiegspfade/BERICHT.md`](../research/ausstiegspfade/BERICHT.md)

---

## Die Frage, in einem Satz

> ⚠️ **Gibt es bei irgendeinem der neun Bots einen Weg, auf dem fehlende oder
> veraltete Kursdaten eine offene Position SCHLIESSEN?**

## Die Antwort, in einem Satz

> **Nein — bei keinem der neun. Aber ein VERALTETER Rahmen aus der zweiten
> Quelle wird ohne Frischeprüfung verwendet, und darauf wird wirklich
> geschlossen: gemessen an einem Stop-Loss, gebucht auf einem Kurs von vor
> 6,85 bis 7,85 Tagen.**

Die Zahl „Offene Papier-Positionen: 0" aus TB-45 ist also **Lesart (a)**:
keine **neuen** Positionen. Kein Parsing-Fehler macht einen Trade. Der
Sicherheitsbefund, den die Frage vermutet hat, liegt woanders — eine Ebene
tiefer und für alle neun an derselben Stelle.

---

## Inhalt

1. [Teil 1 — Der Ausstiegspfad, je Bot gelesen](#teil-1--der-ausstiegspfad-je-bot-gelesen)
2. [Teil 2 — Der Nachweis am Verhalten](#teil-2--der-nachweis-am-verhalten)
3. [Teil 3 — Zwei Gegenproben, die aufgehört hatten zu prüfen](#teil-3--zwei-gegenproben-die-aufgehört-hatten-zu-prüfen)
4. [Teil 4 — Kein-Entscheid-Tag: Vorschlag, keine Umsetzung](#teil-4--kein-entscheid-tag-vorschlag-keine-umsetzung)
5. [Umgebung — was vorgefunden wurde](#umgebung--was-vorgefunden-wurde)
6. [Basislauf, Datenstand, `git status`](#basislauf-datenstand-git-status)
7. [Was ausdrücklich nicht passiert ist](#was-ausdrücklich-nicht-passiert-ist)
8. [Offene Punkte und Vorschläge](#offene-punkte-und-vorschläge)
9. [In einfacher Sprache](#in-einfacher-sprache)

---

## Teil 1 — Der Ausstiegspfad, je Bot gelesen

⚠️ Gelesen, nichts geändert. Zeilennummern gelten für den Stand dieses
Zweiges (`forward_test.py` ist unverändert).

### Der gemeinsame Bauplan

Alle neun Bots sind an dieser Stelle **gleich gebaut**, und das ist der
Grund, warum die Antwort neunmal dieselbe ist:

```
__main__          für jedes Symbol:  df = entscheidungskerze.lade(...)
                                     → in price_data / indicator_data
                  alles in einem try/except Exception je Symbol

check_open_trades  für jeden offenen Trade:
                     if symbol not in <daten>:  continue     ← die Tür
                     future = df[df["open_time"] > entry_time]
                     Balken für Balken: Stop / Ziel / Zeit
                     nur bei Treffer:  UPDATE ... status='closed'
```

**Es gibt keinen `else`-Zweig.** Die Schliessung steht ausschliesslich hinter
einem Treffer auf einem vorhandenen Kursbalken. Ein Symbol ohne Kurse
erreicht die `UPDATE`-Zeile strukturell nicht.

### Die Tabelle

| Bot | Positionsprüfung | Kursquelle | **Symbol FEHLT** | **Rahmen LEER** | **Rahmen VERALTET** | Einstufung |
|---|---|---|---|---|---|---|
| `elliott_wave` | `forward_test.py:105` `check_open_trades` | `price_data` (aus `entscheidungskerze.lade`) | `:113` `if symbol not in price_data: continue` | `:239` `if df is None or df.empty` → `Ladeprotokoll.ohne_kursrahmen`, **gemeldet** | `data/` wird verworfen; Abruf **ungeprüft** übernommen | **sicher** ¹ |
| `t3_supertrend` | `:89` | `indicator_data` | `:97` `if symbol not in indicator_data: continue` | ⚠️ **keine Prüfung** (`:212`) — `compute_indicators` wirft `IndexError`, `:216 except Exception` fängt ihn | wie oben | **sicher, aber aus Versehen** ² |
| `rsi2_crypto` | `:108` | `indicator_data` | `:118` | `:248` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |
| `turtle_soup_crypto` | `:106` | `indicator_data` | `:117` | `:253` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |
| `volatility_breakout_crypto` | `:113` | `indicator_data` | `:124` | `:261` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |
| `elliott_wave_stocks` | `:106` | `price_data` | `:114` | `:275` `if df is None or df.empty` → `Ladeprotokoll`, **gemeldet** | wie oben | **sicher** ¹ |
| `rsi2_mean_reversion` | `:108` | `indicator_data` | `:119` | `:260` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |
| `turtle_soup_stocks` | `:99` | `indicator_data` | `:109` | `:256` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |
| `volatility_breakout` | `:100` | `indicator_data` | `:110` | `:253` `if df.empty: continue` — **still** | wie oben | **sicher** ¹ |

¹ **sicher** heisst hier: *fehlende Kursdaten schliessen nichts.* Der
Vorbehalt zum veralteten Rahmen (nächster Abschnitt) gilt für **alle neun**
und ist kein Unterschied zwischen ihnen.

² **aus Versehen**: `t3_supertrend` ist der einzige Bot ohne `if df.empty`.
Er ist trotzdem geschützt — aber durch einen `IndexError`, den ein breites
`except Exception` eine Zeile später einfängt. Das ist **dieselbe
Fehlerfamilie wie TB-45**: dort lag der `IndexError` (in `calculate_zigzag`)
**ausserhalb** des `try` und beendete den ganzen Lauf. Hier liegt er
innerhalb. Der Unterschied zwischen „harmlos" und „der Bot handelt heute
gar nicht" ist eine Einrückungsebene. Er steht nirgends geschrieben und ist
nicht geprüft — deshalb die Einstufung.

### ⚠️ Die Unterscheidung, auf die es ankommt

Der Auftrag verlangt, „gar nicht erst geladen" und „Kursrahmen leer"
getrennt zu prüfen. Sie sind getrennt geprüft — und sie nehmen wirklich
verschiedene Wege:

| | Weg | Ergebnis |
|---|---|---|
| **gar nicht geladen** | `lade()` wirft (Abruf gescheitert) → `except Exception` in der Ladeschleife → Symbol steht **nicht** im Wörterbuch → `if symbol not in …: continue` | Position unberührt |
| **leerer Rahmen** | `lade()` gibt einen leeren Rahmen zurück → je Bot einer von drei Wegen (siehe Tabelle) → Symbol steht **nicht** im Wörterbuch | Position unberührt |

Beide enden gleich, aber über verschiedene Zeilen — und nur bei drei von
neun Bots hinterlässt der zweite Weg überhaupt eine Zeile im Protokoll.

### ⚠️ Der Pfad, auf dem ein ALTER Kurs verwendet wird

Er liegt nicht in den Bots, sondern in der gemeinsamen Ladeschicht.
`shared/entscheidungskerze.py`, `lade()`:

```python
658    if art is not None:                       # data/ fehlt, veraltet oder unklar
659        sammler.erfasse(symbol, art, grund)
660        if melden: …
663        df = abruf()                          # ← die zweite Quelle
664        df, _gestrichen = entferne_unvollstaendige(df, …)
665
667    gefiltert, _verworfen, hinweis = nur_entscheidbar(df, …)
671    return gefiltert
```

Für `data/` fragt `_aus_datei()` `ist_frisch()` (Zeile 690). **Für das
Ergebnis von `abruf()` fragt es niemand.** `nur_entscheidbar` schneidet nur
ab, was *zu neu* ist — gegen *zu alt* schneidet es nicht.

Folge: Liefert die Gegenstelle (Binance, yfinance) einen verspäteten Stand,
rechnen alle neun Bots darauf, ohne dass irgendwo eine Zeile steht. Ein Stop,
der auf dem Kurs von vorgestern auslöst, ist derselbe Fehler in langsam — und
er ist auf diesem Weg erreichbar. **Gemessen in Lage C2** (siehe Teil 2).

Zwei Dinge dämpfen ihn, keines behebt ihn:

* Der `Sammler` **erfasst** den Rückfall (`VERALTET`) und `melde()` schickt
  ihn über die Telegram-Leitung — aber er meldet, dass `data/` alt war, nicht,
  dass der **Ersatz** alt war.
* `find_new_signals` würde auf altem Stand auch ein **Einstiegs**signal
  erzeugen. Das ist derselbe Weg, nur in die andere Richtung.

### Wer sonst noch `status='closed'` schreibt

Vollständig, über das ganze Repo (ohne Selbsttests):

| Stelle | Auslöser |
|---|---|
| die neun `forward_test.py` | Kursbalken (dieser Bericht) |
| `notifications/manual_close.py:630` | **Mensch** im Dashboard, doppelte Bestätigung, `result='manual_close'` |
| `dashboard/pruefe_warteauftraege_kopie.py:211` | **Mensch** hat vorgemerkt, Cronjob führt aus |

Keine dieser Stellen reagiert auf fehlende Kursdaten. Damit ist die Liste
der datengetriebenen Schliessungen die Liste der neun Bots — und die ist
durchgemessen.

---

## Teil 2 — Der Nachweis am Verhalten

⚠️ Lesen genügt nicht. Ein Weg, den man im Quelltext für unerreichbar hält,
ist in diesem Projekt schon zweimal erreichbar gewesen.

**Werkzeug:** `research/ausstiegspfade/probe.py` — 9 Bots × 5 Lagen = **45
Läufe**, jeder in einem eigenen Prozess in einem eigenen Wegwerf-Verzeichnis
ausserhalb des Arbeitsbaums. Aufbau, Begründungen und die Gründe für jede
Bauentscheidung stehen im Modulkopf und in
[`research/ausstiegspfade/BERICHT.md`](../research/ausstiegspfade/BERICHT.md).

### Zwei Positionen statt einer — und warum

| | Stop | Zweck |
|---|---|---|
| **P1** | unerreichbar tief | **muss in jeder Lage offen bleiben** |
| **P2** | genau auf dem Einstiegskurs | **muss in Lage D schliessen** |

⚠️ **Lage D ist nicht optional** — und eine Kontrolle mit nur P1 wäre es
beinahe gewesen. Bliebe in Lage A alles unverändert, weil der Bot gar nicht
bis zur Positionsprüfung kommt, sähe das genauso aus wie „richtig
entschieden". **P2 beweist, dass der Bot die Stelle erreicht und schliessen
KANN.** Erst mit beiden zusammen misst die Probe den Ausstiegspfad und nicht
die Frage, ob der Bot überhaupt läuft.

### Die fünf Lagen

| | Kursdatei in `data/` | Live-Abruf |
|---|---|---|
| **A** | fehlt ganz | scheitert (403, wie in der Cloud wirklich) |
| **B** | vorhanden, **leerer** Rahmen | liefert einen leeren Rahmen |
| **C1** | vorhanden, **veraltet** (7 Tage) | scheitert |
| **C2** | vorhanden, **veraltet** | liefert denselben veralteten Rahmen |
| **D** | in Ordnung, frisch | wird nicht gerufen |

⚠️ **C2 steht nicht im Auftrag.** Sie ist ergänzt worden, weil die Frage des
Auftrags („ein Pfad, auf dem ein ALTER Kurs verwendet wird") mit den vier
vorgegebenen Lagen **nicht beantwortbar** ist: `lade()` verwirft eine
veraltete `data/`-Datei vollständig und ruft `abruf()`. Ein veralteter
Rahmen aus `data/` erreicht den Bot **nie**. Lage C1 misst das und ist
deshalb grün; erst C2 misst die Frage.

### Das Ergebnis — neunmal dasselbe Bild

| Lage | offen vorher → nachher | Datenbank |
|---|---|---|
| **A** | 2 → 2 | ⚠️ **byteweise unverändert** (sha256 identisch) |
| **B** | 2 → 2 | **byteweise unverändert** |
| **C1** | 2 → 2 | **byteweise unverändert** |
| **C2** | 2 → 1 | P2 geschlossen, `result='stop_loss'`, **Ausstiegskurs 6,85–7,85 Tage alt** |
| **D** | 2 → 1 | P2 geschlossen, P1 offen — die Kontrolle greift |

* Rückgabewert **0** in allen 45 Läufen. Kein Lauf lief in die Zeitgrenze.
* „Prüfe offene Positionen…" **und** die Zusammenfassung wurden in **allen**
  45 Läufen erreicht — kein Bot bricht in irgendeiner Lage vorher ab.
* Für die drei unauffälligen Lagen ist nicht bloss die Zahl gleich: der
  **sha256 der Datenbankdatei** ist vor und nach dem Lauf identisch.

### Die eine Zeile, die den Befund trägt

`research/ausstiegspfade/ergebnisse/probe.json`, Lage C2, je Bot:

```
elliott_wave   [GESCHLOSSEN] BTCUSDT: stop_loss, PnL -0.30%
               exit_time = 2026-09-10 20:00:00     (Lauf: 2026-09-17)
               alter_des_ausstiegskurses_in_tagen = 7.01
```

Und daneben, damit klar ist, dass es nicht am Aufbau liegt — dieselbe
Position, dieselbe Reihe, nur mit frischen Daten (Lage D):

```
elliott_wave   exit_time = 2026-09-17 17:00:00     alter = 0.14
```

### Nachweis, dass am Bot nichts geändert wurde

Die Probe vergleicht je Lauf den sha256 von `forward_test.py`,
`live_params.py`, `indicators.py`, `equity_simulation.py` und der
gemeinsamen `shared/`-Module zwischen Repo und Wegwerf-Kopie: **18 bis 26
Dateien je Bot, alle `true`** (Feld `bot_dateien_unveraendert`).

Ausgetauscht ist ausschliesslich die **Gegenstelle**: an
`shared/fetch_binance_data.py` bzw. `strategies/<bot>/fetch_stock_data.py`
wird in der Kopie ein Block **angehängt**, der `fetch_historical_data` neu
belegt. Ohne ihn wäre jede Lage dieselbe Lage — „Abruf gescheitert" —, weil
Binance und yfinance aus der Cloud mit 403 antworten. Der Block steht nur in
der Wegwerf-Kopie, nie im Repo, und ist im JSON namentlich aufgeführt
(`gegenstelle_ersetzt_in`).

### Drei Wege, ein leeres Symbol auszulassen — gemessen, nicht geschlossen

Lage B, an den Zeilen, die der Lauf zu dem Symbol geschrieben hat:

| Weg | Bots | Zeile |
|---|---|---|
| **gemeldet** | `elliott_wave`, `elliott_wave_stocks` | `Hinweis: BTCUSDT hat keinen Kursrahmen geliefert (data/ und Live-Abruf), wird uebersprungen.` |
| **gemeldet, aber aus Versehen** | `t3_supertrend` | `Fehler bei BTCUSDT: index 0 is out of bounds for axis 0 with size 0` |
| ⚠️ **still** | die übrigen **sechs** | *(keine einzige Zeile)* |

⚠️ Und: `elliott_wave`/`elliott_wave_stocks` legen ein `Ladeprotokoll` an
(`:233` bzw. `:268`), rufen aber **nie `_prot.melde(price_data)`**. Die
**Summenzeile** — „Geladen: n von m Symbolen", die die Frage *„hat dieser
Lauf überhaupt vollständig geladen?"* ohne Zählen beantwortet und die
`shared/ladeprotokoll.py` ausdrücklich als „den eigentlichen Gewinn"
beschreibt — steht im **Papierpfad bei keinem der neun Bots**. Nur die
Backtest-Lader (`multi_symbol_optimise.py`) rufen sie.

Das ist die direkte Vorarbeit für Teil 4.

### Nebenbefund (festgehalten, nicht repariert)

`strategies/elliott_wave/forward_test.py:129`

```python
if row["high"] >= trade["target_price"]:
```

ohne None-Absicherung. Ein Trade mit `target_price = NULL` bringt
`check_open_trades` mit `TypeError` zu Fall — **ausserhalb** des `try` der
Ladeschleife, also den ganzen Lauf. Der Bot selbst schreibt immer beide
Werte; aus eigener Kraft kann der Fall nicht entstehen. Aufgefallen ist er,
weil die erste Fassung der Probe `NULL` gesetzt hatte. **Befund, keine
Reparatur** — `forward_test.py` ist für TB-46b gesperrt.

---

## Teil 3 — Zwei Gegenproben, die aufgehört hatten zu prüfen

> ⚠️ Eine Gegenprobe, die gegen einen wandernden Bezugspunkt prüft, wird
> nicht falsch — sie wird wirkungslos, und zwar still.

Beide Dateien verglichen gegen `origin/main`. Seit dem TB-45-Merge trägt
`origin/main` die Reparatur selbst: die „alte Fassung", die abbrechen soll,
**war die neue**.

### Vorher gemessen

| Datei | vorher | Ursache |
|---|---|---|
| `shared/test_leeres_symbol.py` | **43/45** | zweimal: *„auf echten Daten bricht die ALTE Fassung bei einem leeren Rahmen ab"* — sie tut es nicht mehr, sie ist repariert |
| `shared/test_stille_ausfaelle.py` | **23/24** | `teil_2` warf `RuntimeError: git commit -q -m alte Fassung:` — leere stderr, weil *„nothing to commit"* auf stdout geht |

### Was geändert wurde

**1. Der Bezugspunkt ist festgeschrieben.** In beiden Dateien steht jetzt

```python
BEZUGSCOMMIT = "97aea8878c9fae5e1f12d30e2ea0318dd20aadc5"
BEZUGSCOMMIT_KURZ = "97aea88"
```

mit einer ausgeschriebenen Begründung im Kommentar. `97aea88` ist das
**Elternteil** von `55b991d` (*„TB-45: stille Ausfaelle …"*), also der Stand
**unmittelbar vor** der Reparatur. Ermittelt, nicht angenommen:
`git log -- strategies/*/zigzag_indicator.py shared/test_kursdaten.py
dashboard/test_portfolio_sicht.py` nennt für alle drei Prüflinge denselben
Reparatur-Commit.
⚠️ **Nicht `origin/main`, nicht `HEAD~n`** — beide wandern.

**2. Der leere Commit ist abgefangen.** `test_stille_ausfaelle.teil_2`
committet mit `--allow-empty`, und der Zweig „die Fassung ist bereits
repariert" steht jetzt **vor** dem Commit statt danach.

**3. Die Lehre ist eingebaut.** Findet git den Bezugscommit nicht — flache
Kopie, fremder Klon —, ist der Test **ROT** mit dem Vermerk
`NICHT PRUEFBAR`. Nie grün, nie übersprungen. Dasselbe, wenn die Fassung aus
dem Bezugscommit die Reparatur wider Erwarten schon trägt: dann liegt der
Bezugspunkt falsch, und das ist ein Befund über den Test, kein grüner Haken.

### Nachher gemessen

| Datei | nachher |
|---|---|
| `shared/test_leeres_symbol.py` | **45/45 grün** |
| `shared/test_stille_ausfaelle.py` | **27/27 grün** (drei Prüfungen mehr: `teil_2` läuft jetzt wirklich durch) |

### Und die Gegenprobe zur Reparatur selbst

Weil eine Wache, die man repariert, ohne zu prüfen, ob sie noch beisst, genau
der Fehler ist, um den es hier geht — beide Zweige wurden künstlich ausgelöst
(Bezugscommit auf `0000…0` bzw. auf `origin/main` gesetzt, jeweils ohne die
Dateien zu ändern):

```
test_leeres_symbol.teil_1,   Bezugscommit unauffindbar   → 2 ROT, 8 grün
test_stille_ausfaelle.teil_2, Bezugscommit unauffindbar  → 2 ROT, 0 grün
test_stille_ausfaelle.teil_2, Bezugscommit = origin/main → 2 ROT
     „die Fassung aus 66530f4 trägt die Wache bereits,
      der Bezugspunkt liegt also falsch"
```

⚠️ **Nur diese beiden Dateien wurden angefasst.** Keine andere Testdatei.

---

## Teil 4 — Kein-Entscheid-Tag: Vorschlag, keine Umsetzung

⚠️ **Dieser Teil schlägt vor. Er setzt nichts um.** Kein Registertext ist
geändert worden.

### Wo müsste der Lauf-Datensatz geschrieben werden?

**Vorschlag: `shared/entscheidungskerze.melde()` — und nur dort.**

Die Begründung ist nicht Bequemlichkeit, sondern dass dort bereits alles
vorliegt und alle neun vorbeikommen:

| Was gebraucht wird | Wo es heute schon steht |
|---|---|
| **welcher Bot** | `_botname()` (`entscheidungskerze.py:779`) — aus dem Ordner des Hauptskripts, derselbe Name wie in `strategy_paths` |
| **welche Symbole, mit welchem Grund** | `Sammler.je_symbol` (`:580`) — `symbol → (art, grund)` mit `FEHLT` / `VERALTET` / `UNKLAR` |
| **genau einmal je Lauf** | `melde()` steht in **allen neun** `forward_test.py` als vorletzte Zeile vor `print_summary` |
| **bricht den Lauf nie** | `melde()` ist vollständig in `try` gekapselt (`:768`) — Grundsatz „melden, nicht stoppen" |

**Passt das Muster von `shared/ladeprotokoll.py`?** — Für den **Wortlaut**
ja, für den **Datensatz** nein.

* ✅ Der Wortlaut gehört dorthin: `Ladeprotokoll` führt die Sätze für
  ausgelassene Symbole schon zentral, und ein sechster Grund („kein
  Entscheid") wäre dort eine Zeile.
* ❌ Der Datensatz kann nicht dorthin: `Ladeprotokoll` ist **pro Ladevorgang**
  gebaut und **kennt den Bot nicht**. Es hat kein Gedächtnis über den Lauf
  hinaus und keine Datenbank.
* ⚠️ Und: **im Papierpfad läuft `Ladeprotokoll` heute fast nicht.** Nur
  `elliott_wave` und `elliott_wave_stocks` legen eines an, und **keiner von
  beiden ruft `melde()`** — die Summenzeile, also genau die Zeile, aus der man
  einen Kein-Entscheid-Tag ablesen könnte, entsteht im Papierpfad **nie**
  (gemessen, Teil 2). Ein Register auf `Ladeprotokoll` aufzusetzen hiesse,
  zuerst sechs Bots umzubauen — und `forward_test.py` ist gesperrt.

⚠️ Das ist zugleich ein **Befund für sich**: die Ladeprotokoll-Reparatur aus
TB-42/TB-45 ist im Papierpfad nur halb angekommen.

### Wohin der Datensatz — Datei oder Datenbank?

**Vorschlag: eine eigene, gemeinsame Datenbank für alle neun.** Das Muster
existiert im Projekt bereits und hat sich bewährt:

`notifications/schliess_benachrichtigung.py:177` führt
`benachrichtigungen_schliessung.db` — **eine** Datei für alle neun Bots, mit
`bot` als Spalte und `UNIQUE(bot, trade_id)` als struktureller Sperre.
Analog:

```sql
CREATE TABLE IF NOT EXISTS laeufe (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    bot          TEXT NOT NULL,
    startzeit    TEXT NOT NULL,   -- entscheidungskerze.laufbeginn(), ISO-8601
    handelstag   TEXT NOT NULL,   -- Datum der Entscheidungskerze
    symbole_ganz INTEGER NOT NULL,
    symbole_ok   INTEGER NOT NULL,
    entscheid    TEXT NOT NULL,   -- 'ja' | 'kein_entscheid' | 'teilweise'
    grund        TEXT,            -- NULL bei 'ja'
    UNIQUE(bot, startzeit)
);
```

⚠️ **Nicht in die neun `paper_trading_*.db`.** Drei Gründe, jeder für sich
ausreichend:

1. Die neun Bot-Datenbanken sind die **einzige OOS-Evidenz** des Projekts und
   nicht neu berechenbar (CLAUDE.md). Wer dort eine Tabelle anlegt, schreibt
   in sie.
2. Sie haben heute **genau eine** Tabelle (`trades`). Das ist eine
   Eigenschaft, auf die `broker/bot_db.py` (schreibgeschützt, `mode=ro`),
   `manual_close.py` und das Dashboard aufbauen.
3. Eine gemeinsame Tabelle beantwortet „an welchem Tag hatten **mehrere**
   Bots keinen Entscheid?" mit einer Zeile SQL. Neun Tabellen brauchen dafür
   neun Abfragen und einen Join.

### Wie unterscheidet die Auswertung später Kein-Entscheid von Kein-Signal?

**Heute: gar nicht.** Das ist der Kern.

Die Datenbanken der neun Bots kennen **nur `trades`**. Es gibt keine Zeile,
die einen Lauf beschreibt — nur Zeilen, die Trades beschreiben. Ein Tag ohne
neue Zeile ist deshalb heute ununterscheidbar:

* der Bot lief und fand kein Signal,
* der Bot lief und konnte nicht entscheiden,
* der Bot lief gar nicht (Cron fiel aus — `docs/DATENLUECKEN.md`).

⚠️ Alle drei sehen in jeder Auswertung gleich aus: **eine Lücke sieht in den
Zahlen genauso aus wie „kein Signal"** (CLAUDE.md).

**Mit dem Vorschlag:** die Auswertung liest `laeufe` und unterscheidet über
**eine Spalte**:

| Frage | Abfrage |
|---|---|
| Kein-Entscheid-Tag? | `entscheid = 'kein_entscheid'` |
| Kein Signal? | `entscheid = 'ja'` **und** keine `trades`-Zeile mit diesem `handelstag` |
| Lauf ausgefallen? | **keine** `laeufe`-Zeile für diesen `bot`/`handelstag` |

Die dritte Zeile ist der eigentliche Gewinn: sie macht die Datenlücken aus
`docs/DATENLUECKEN.md` erstmals **maschinell** unterscheidbar, statt sie
nachträglich aus Cron-Logs rekonstruieren zu müssen.

**Der Schwellenwert gehört ausgeschrieben.** `teilweise` und
`kein_entscheid` müssen sich an einer Zahl trennen, die einmal irgendwo
steht — Vorschlag: `kein_entscheid`, wenn `symbole_ok == 0`; `teilweise`
sonst, solange `symbole_ok < symbole_ganz`. Eine zweite, feinere Schranke
(„weniger als die Hälfte") wäre ein eigener Parameter und gehört dann nach
dem Grundsatz aus CLAUDE.md an **genau eine** Stelle.

### ⚠️ Wie viele Kein-Entscheid-Tage seit dem Umstellungstag?

**In der Cloud nicht beantwortbar.** Nicht aus Zeitmangel, sondern
strukturell:

| Was die Antwort trüge | Zustand in der Cloud |
|---|---|
| die neun `paper_trading_*.db` | gitignoriert, **existieren hier nicht** — und sie enthielten die Antwort ohnehin nicht (nur `trades`) |
| `logs/<bot>/*.log` (Cron-Ausgabe) | `logs/` ist gitignoriert, im frischen Checkout **nicht vorhanden** |
| `notifications/rueckfall_zustand.json` | gitignoriert; enthält nur den **letzten** Fingerabdruck der Meldedämpfung, **keine Historie** |

⚠️ **Und es ist auch auf dem Mac nur teilweise beantwortbar** — das gehört
gesagt, bevor die Frage dort gestellt wird:

* Der Umstellungstag ist **2026-09-16T04:42:24Z**, also **etwa anderthalb
  Tage** vor diesem Bericht. Die Stichprobe ist entsprechend klein.
* Die Antwort müsste aus den Cron-Logs kommen, und `system/log_rotation.py`
  behält **5 Stände à 1 MB**. Für das kurze Fenster reicht das, für eine
  spätere Wiederholung der Frage nicht.
* Die Bots schreiben **keine** Zeile „kein Entscheid". Gezählt werden müsste
  über die Rückfallzeilen (`Rueckfall auf den Live-Abruf …`) und die
  Fehlerzeilen — also über eine **Textsuche im Protokoll**, nicht über einen
  Datensatz. Genau das soll der Vorschlag oben ablösen.

**Die Frage geht in den Mac-Testauftrag**, mit den Befehlen, die sie so weit
beantworten, wie sie heute beantwortbar ist — siehe
[`TESTAUFTRAG_TB-46b_ausstiegspfade.md`](TESTAUFTRAG_TB-46b_ausstiegspfade.md),
Schritt 6.

---

## Umgebung — was vorgefunden wurde

⚠️ `docs/UMGEBUNGEN.md` verlangt, Abweichungen zu **melden**. Hier sind sie.

| | `docs/UMGEBUNGEN.md` / Auftrag | **diese Sitzung** |
|---|---|---|
| Python | Cloud „3.11 oder neuer" | **3.11.15** ✅ |
| `pandas` | Mac 2.3.3, Cloud „wechselnd" | ⚠️ **gar nicht vorhanden.** Nachinstalliert; `pip install pandas` liefert **3.0.5**. Auf **2.3.3 zurückgesetzt**, um dem Betriebsrechner zu entsprechen |
| `numpy` | Mac 2.0.2 | ⚠️ **2.4.6** (Abweichung, nicht rückgesetzt: `pandas 2.3.3` läuft damit) |
| `scipy`, `binance`, `yfinance`, `fastapi`, `pandas_market_calendars`, `python-telegram-bot`, `dateparser`, `pytz` | „fehlten in TB-46 alle" | ⚠️ **fehlten wieder alle.** Alle nachinstalliert |
| `uvicorn` | im Auftrag **nicht genannt** | ⚠️ **fehlte ebenfalls** — `dashboard/test_dashboard.py` bricht ohne ihn beim Import ab. Nachinstalliert |
| `pandas_market_calendars` | `requirements.txt`: `>=4.1,<5` | ⚠️ `pip install` liefert **5.4.0**, also **ausserhalb** der eigenen Bindung des Projekts. Auf `<5` zurückgesetzt |
| `US/Eastern` | „fehlte (Minimal-tzdata)" | ⚠️ **fehlte wieder.** Mit `tzdata` nachinstalliert |
| Binance, yfinance | „gesperrt" | ✅ gesperrt (403) — die Probe rechnet damit |
| GNU `timeout` | „vorhanden" | ✅ vorhanden (`/usr/bin/timeout`), `perl` ebenfalls |
| `node` | „wechselnd" | ✅ **v22.22.2 vorhanden** (`/opt/node22/bin/node`) |

**Die Meldung an den Betreiber**, wörtlich, für `docs/UMGEBUNGEN.md`:

> Die Cloud-Sitzung beginnt mit **leerem Paketstand** — nicht mit einem
> wechselnden. In TB-45, TB-46 und TB-46b war es dreimal dasselbe Bild. Der
> Satz „wechselnd" ist freundlicher, als die Messungen es hergeben; „fehlt
> und muss nachinstalliert werden" trifft es. **Und `uvicorn` gehört in die
> Liste** — ohne ihn ist `dashboard/test_dashboard.py` rot, ohne dass
> irgendetwas kaputt ist.

