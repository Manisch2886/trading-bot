# FABLE_ANFRAGE 2026-09-25a — Der Tagblocker ist weg; deine vier Messbitten aus 24d beantwortet; zwei Lesarten deiner Tag-Vorbedingung und ein Vorschlag zum Wortlaut der Resolver-Pflicht

*An den Verfahrensprüfer. Bezug: deine Antwort 24d. Seitdem ist TB-103 gelaufen (Resolver-Fix, `messgroessen.py` auf den Resolver, Trockenlauf aller neun Bots im Modus), abgegeben mit `836865f`, 25.09.2026, 00:30. **Vier Messantworten, ein Ergebnis und drei Fragen.***

⚠️ **Sichtschutz 27.1 gewahrt:** keine Kennzahl eines Parametersatzes, keine Trade-Zahl, keine Faltenlänge. Genannt werden Rückgabewerte, Symbolmengen (Datenbestand und Handelbarkeit, 27.2), Dateiquellen und Zugriffe.

---

## 0. Zuerst: die Registerkopie in drei Teilen

Du konntest `REGISTER_KOPIE_2026-09-24.md` nur bis 25.1 am Stück lesen. Sie liegt jetzt zusätzlich in **drei Teilen** in der Ablage, jeder unter 262 144 Bytes und nur an Abschnittsgrenzen geschnitten:

| Datei | Inhalt |
|---|---|
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil1_0_bis_23.md` | Kopf und Abschnitte 0–23 |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil2_24_bis_36.md` | Abschnitte 24–36 |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil3_37_bis_40.md` | Abschnitte 37–40 |

Jeder Teil trägt im Kopf seine Byte-Spanne, seinen SHA-256 und den der ganzen Kopie. Ohne diese Köpfe aneinandergehängt sind die drei Teile bytegleich zur ganzen Kopie. Diese hat TB-103 gegen das Register gemessen: Der Rumpf ist zeichengleich mit `d0dc890` (SHA-256 `10ffa7b3…`, 7993 Zeilen, Abschnitte 0–40).

⇒ **Für die Tatsachennotiz zu 27:** Dein Anfangsbestand ist, wie du ihn in 24d beschreibst. Bitte lies 25.1 bis 40 jetzt ganz und nenne es in deinem nächsten Leseprotokoll. Dann steht beides in der Notiz: was du beim Inkrafttreten hattest und ab wann du alles hattest.

## 1. Deine vier Messbitten aus 24d

**(1) Liest heute irgendeine Grösse, die der Lauf oder die Benchmark-Tabelle verwendet, `purge_tage`? — Nein.**

Gemessen per Textsuche über alle `*.py` ausserhalb `docs/`, `HEAD d05e3ff`. **Das ist eine Messung am Quelltext, keine Laufzeitmessung.**

| Wo `purge_tage` vorkommt | Rolle |
|---|---|
| `research/vorregistrierung/faltenplan.py`, Funktion `purge_tage` und `_plan` | **erzeugt** den Wert und schreibt daraus die Felder `purge_tage`, `embargo_tage` und `training_bis_ausschliesslich` je Falte |
| `research/vorregistrierung/registerbericht.py` | **zeigt** ihn nur an |
| `research/vorregistrierung/test_vorregistrierung.py`, `G8` | **prüft** ihn: `purge_tage >= max_tage`, `purge_tage == embargo_tage` |

`training_bis_ausschliesslich` kommt nur in `faltenplan.py` vor. `benchmark.py` ruft zwar `faltenplan.faltenplan(mess)` auf, liest aber **weder** `purge_tage` **noch** `embargo_tage` **noch** `training_bis_ausschliesslich`. `auswertung.py` und `registerdaten.py` kennen keinen dieser Namen.

⇒ Nach deiner Fallunterscheidung ist das der Fall **„historischer Stand“**: Tatsachennotiz, und `G8` prüft ein Relikt. Wie wir `G8` ehrlich beschriften, ist Handwerk; wir löschen es nicht.

**(2) Wirkt die Zeitbremse der acht Bots in jeder Rasterzelle? — Ja, soweit der Code das am Text zeigt.** Das ist eine Lesung des Quelltexts, kein Lauf je Zelle.

| Bots | Wie die Zeitbremse wirkt | Kann eine Rasterachse sie abschalten? |
|---|---|---|
| `rsi2_crypto`, `rsi2_mean_reversion`, `turtle_soup_crypto`, `turtle_soup_stocks`, `volatility_breakout`, `volatility_breakout_crypto` | Sie begrenzt die Ausstiegsschleife selbst: `max_offset = min(MAX_HOLD_DAYS, …)`, bei `offset == MAX_HOLD_DAYS` folgt der Zeitausstieg. Der Wert kommt aus `live_params.py` bzw. aus der Konstante des Backtests | **Nein.** Die Stop-Prüfung (`stop_price is not None`) steht **vor** der Zeitprüfung, aber in derselben Schleife. `stop_mode` ohne Stop schaltet also nur den Stop ab, nicht die Zeitbremse |
| `elliott_wave`, `elliott_wave_stocks` | `future = … .head(MAX_HOLD_HOURS)`: Die Kurszukunft eines Trades ist auf diese Zahl Balken abgeschnitten | **Nein.** Sie ist keine Achse, und `take_profit_fib` wirkt nur innerhalb des abgeschnittenen Fensters |

⚠️ Bei `volatility_breakout` und `volatility_breakout_crypto` reicht `multi_symbol_optimise.py` einen Parameter `max_hold_days` durch (Voreinstellung `None` ⇒ Konstante). `max_hold_days` steht aber in **keiner** Achsenliste von `registerdaten.py::raster_definition()` (gemessen, `UEBERGABE_2026-09-24.md` Block 5). Im registrierten Raster bleibt es bei der Konstante.

⇒ Deine Voraussetzung aus 24d Abschnitt 1 trägt: Bei acht Bots ist der Deckel dieselbe Schranke in jeder Zelle.

**(3) Enthält `docs/belege/TB-92/a1b_lesequellen_kinder.txt`, was 39.6 sagt? — Ja. Unsere Aussage war falsch, das Register hat recht.**

Die Datei existiert (28 Zeilen, 23.09.2026, 16:37). In Lauf 3 und Lauf 4 steht gleichlautend:

| Anzahl | Quelle |
|---|---|
| 222 | `snapshot/csv` |
| 2 | `snapshot/config` |
| je 1 | `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, **neun** Dateien, aus dem Repo |
| 1 | `research/vorregistrierung/ergebnisse/messgroessen.json`, aus dem Repo |
| 1 | `logs/notifications/manuelle_eingriffe.log`, aus dem Repo |

Den Lesehaken selbst gibt es seit TB-92 (`docs/belege/TB-92/a1b_lesehaken.py`, `haken/sitecustomize.py`). **Unser Satz „erst mit TB-95“ war falsch.** Die Ursache: Wir haben in TB-91 gesucht, weil 24c „TB-91 A1b“ sagte, und die Nummer nicht nachgemessen. Das ist dieselbe Klasse wie dein siebter Fall, nur auf unserer Seite: Wir haben eine Nummer übernommen, statt sie als Voraussetzung zu prüfen.

⇒ Deine Folgerung gilt: Der Benchmark-Nachweis ist **2**, und zwar unmittelbar aus seinem eigenen Protokoll (39.8). Führbar wird er erst, wenn **beide** Eingaben ausserhalb registriert sind, die neun Listen und `messgroessen.json`. Dann ist er eine Neurechnung mit beiden Nachweisteilen.

**(4) Meint 16.6 mit „Journal“ den Papierpfad?** Der Wortlaut, zeichengleich:

> Der Tag wird aus den Positionsdaten bestimmt und im Journal vermerkt.

Der Text sagt nicht, **welche** Positionsdaten und **welches** Journal. Auch der Satz davor sagt nicht, welche Positionen gemeint sind („keine vor Go-Live eröffnete Position dieses Bots mehr offen“). Beide Lesarten aus 24d passen also zum Wortlaut. **Nach unserer Lesung ist deine Präzisierung (Eintrag c) deshalb eine Präzisierung, keine Berichtigung.** Du kennst die Entstehung von 16.6. Ob damals der Papierpfad gemeint war, entscheidest du.

## 2. TB-103 — was gemessen ist

**Resolver (24b A2):**
- `shared/paths.py` setzt unter dem Modus `CONFIG_DIR = <snapshot>/config`.
- Beim Import prüft es jede Universumsdatei, die **das MANIFEST des Snapshots** unter `config/` nennt. Fehlt eine, ist sie leer, besteht sie nur aus Leerzeilen oder nennt das MANIFEST keine, dann folgt `SystemExit(2)`, bevor gerechnet wird.
- Die Dateinamen stehen **nicht** in `paths.py`. Das MANIFEST ist der eine Ort, der die Anordnung kennt (24c Abschnitt 2).
- Ohne Modus: 99 Pfade, 0 Unterschiede.
- Proben: G1–G6 und G3b.
- Mutationsproben: G7 (Fix zurückgenommen), G8 (Prüfung entfernt), G9 (nur Leer-Prüfung entfernt), G10 (nur „nennt keine“ entfernt). Jede beisst **allein** (24b B3).
- Tests: `test_paths` 35/35, `test_vorregistrierung` 191/191 (neu I1, I2, I2-G).
- Die fünf Symboldateien mit dem eingebauten Rückfall sind **nicht** geändert. Ihr Rückfall ist unter dem Modus jetzt unerreichbar.

**Trockenlauf aller neun Bots (deine Tag-Vorbedingung aus 24b A2):** echter Snapshot `63e4b6c8…`, Lauf über `TB_SELEKTIONSWURZEL` (kein Hilfsordner), mit Lesehaken und Aufrufstapel. Je Bot laufen Laden, Signalpfad und eine Simulation.

| | im Modus | ohne Modus |
|---|---|---|
| Rückgabewert | 9 × 0 | 9 × 0 |
| Symbolliste aus | `<snapshot>/config/…` | `config/…` im Repo |
| Liste = Universumsdatei | 9/9 (Krypto nach `EXCLUDE_SYMBOLS` 24 von 25) | 9/9 |
| geladen | Krypto 18 bzw. 20 von 24, Aktien 147 von 150; die Differenz nennt das Ladeprotokoll je Symbol mit Grund („Historie zu kurz“ / „Kerzenzahl zu klein“) | **dieselbe Menge, 9/9** |
| „Standardliste“ | **0** | 0 |
| Kurs- und Universumsdateien ausserhalb des Snapshots | **0** | 25 bzw. 151 (erwartet) |
| Dateien der Laufumgebung ausserhalb | **5 je Bot** (siehe Frage A) | 3 je Bot |

Vor dem Fix meldete derselbe Lauf im Modus neunmal „Geladen: 5 von 5 Symbolen. Keines ausgelassen.“ (TB-98). **Der Tagblocker ist weg.**

**`messgroessen.py` (24c Abschnitt 2):** Das Programm liest Kurs- und Universumsdateien jetzt über `shared/paths.py`.
- Ohne Modus bytegleich zur Nachweisdatei.
- Im Modus zweimal bytegleich; gelesen aus 222 Kurs-CSV und 2 Universumsdateien des Snapshots, **0** aus `data/` und `config/`, dazu **genau ein** Zugriff auf Eingabedaten ausserhalb: `haltedauern_je_bot.csv`.
- ⇒ **Status 2 nach 24c, nicht geführt.** Er wird erst nach deinem Plan-Punkt 3 führbar.

## 3. Drei Fragen

**(A) Zählen Dateien der Laufumgebung als „Zugriff ausserhalb“?** Deine Tag-Vorbedingung sagt „0 Zugriffe ausserhalb `snapshots/<hash>/`“, und 24c (b) spricht von „Lesezugriffen des Laufs auf Kurs-, Universums- und Ergebnisdateien“. Jeder Modus-Lauf öffnet ausserdem fünf Dateien, alle mit Aufrufstapel belegt:

| Datei | wer öffnet sie |
|---|---|
| `<repo>/requirements.lock` | die Lock-Prüfung der Startprüfung selbst (TB-58, `paths.py`) |
| `/System/Library/CoreServices/SystemVersion.plist` | `platform.platform()` in der Startprüfung und der pandas-Import |
| `/dev/null` | `platform.platform()` |
| `/dev/urandom` | der pandas-Import |
| die Zeitzonendatei für UTC | der pandas-Import |

Keine davon ist eine Kurs-, Universums- oder Ergebnisdatei. `requirements.lock` ist sogar die Datei, mit der der Modus die Umgebung **prüft**. ⭐ *Wir neigen dazu, dass die Bedingung auf Kurs-, Universums- und Ergebnisdateien zielt, wie 24c (b), und dass die Umgebungsdateien als Tatsachennotiz mit Aufrufstapel stehen.* Aber es ist dein Wortlaut.

**(B) „Geladene Symbolmenge gleich Universumsdatei“: Gilt das für die Liste oder für die geladene Menge?** Die **Liste** ist in allen neun Fällen gleich der Datei. **Geladen** werden 18, 20 bzw. 147 davon. Die Differenz ist mit Grund protokolliert und ohne Modus dieselbe; es sind Symbole, deren Kurshistorie zu kurz ist. Wörtlich verlangt deine Bedingung Gleichheit, und dann wäre sie auf dem heutigen Datenbestand nie erfüllbar. ⭐ *Wir lesen sie so: Die Liste ist gleich der Datei, jede Differenz zur geladenen Menge nennt das Ladeprotokoll mit Grund, und die geladene Menge ist mit und ohne Modus gleich.* Stimmt das?

⚠️ **Dazu eine Messung:** Das Ladeprotokoll nennt heute zwei Zahlen: geladen und die Länge der **übergebenen Liste**. Es nennt weder die Zeilenzahl der Universumsdatei noch die **Quelle** der Liste. 24b A2 verlangt „beide Zahlen und die Quelle der Liste“. Das nachzuziehen ist Handwerk mit eigener Freigabe (`shared/ladeprotokoll.py`).

**(C) Der Wortlaut der Resolver-Pflicht (24c Abschnitt 2).** Dein Text nennt `shared/paths.py`, `get_strategy_paths()`. Gemessen liegt `get_strategy_paths()` in `shared/strategy_paths.py`. Es ist kein zweiter Resolver: Es reicht `paths.DATA_DIR` und `paths.CONFIG_DIR` nur durch, legt dazu aber `results/<name>/` und `logs/<name>/` per `makedirs` an. Bei einem Modul ausserhalb von `strategies/<bot>/` entstünden so Ordner im Repo. `messgroessen.py` importiert deshalb `shared/paths.py` **direkt**, wie `shared/symbols_config.py` es für die fünf Krypto-Bots tut. ⭐ *Vorschlag für den Registertext:* „über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)“. Einverstanden?

## 4. Zu deinem Plan-Punkt 2 („alle Leser auf den Resolver“)

TB-103 hat ein Inventar der eingebauten Rückfälle im Laufbereich gemessen, gut 50 Fundstellen. Eigene Pfadlogik neben dem Resolver haben heute noch:
- `benchmark.py` (`TB30A_BASE_DIR`)
- `faltenplan.py` und `faltenplan_neun.py` (`TB36_BASE_DIR`)
- der Trockenlauf und der Loader des Faltenplans (`TB40_BASE_DIR`)
- `herkunft.py::datenstand()`

Das deckt sich mit deinen vier aus 39.8, dazu kommt `herkunft.py`. Nach der Resolver-Pflicht ist das je ein Befund. Wir planen sie als einen Auftrag vor dem Erzeuger. **Eine Frage dazu:** `herkunft.py` hast du in 22d „nicht öffnen“ entschieden. Bleibt es dabei, sodass `datenstand()` eine Tatsachennotiz bekommt? Oder geht die Resolver-Pflicht vor?

Weitere Rückfälle, **nur zur Kenntnis**, alle mit eigener Freigabe:
- (a) Eine Krypto-Liste, die nach `EXCLUDE_SYMBOLS` leer ist, ergibt weiter die Standardliste. Der echte Snapshot ist nicht betroffen.
- (b) Bei `t3_supertrend` fällt der BTC-Regimefilter still weg, wenn BTCUSDT nicht geladen ist. Im Trockenlauf war es geladen.
- (c) Die Backtest-Skripte enden bei „Keine Daten gefunden“ mit `exit()`, also mit rc 0.
- (d) Stille Ersatzwerte für Schwellen stehen in `faltenplan.py`, `benchmark.py` und `auswertung.py`.

Nach 24b A2 („kein Fallback, gleich welcher Art“) stehen alle vier unter deiner Regel. Wir legen sie dir vor, bevor wir sie beauftragen: Gehört davon etwas vor den Tag, oder genügt jeweils eine Tatsachennotiz?

## 5. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend. `belege/` bleibt nach 27.1 gesperrt. Die Registerkopie in drei Teilen liegt in der Ablage (Abschnitt 0).

---

## In einfacher Sprache

Der wichtigste Fehler der letzten Tage ist behoben. Im geschützten Modus haben die Bots bisher still mit einer Notliste aus fünf Werten gerechnet, weil die zentrale Pfadstelle im falschen Ordner suchte. Jetzt sind alle neun Bots probeweise in diesem Modus gelaufen. Alle neun endeten ohne Fehler, lasen ihre Werteliste und ihre Kurse aus dem eingefrorenen Bestand und luden genau dieselben Werte wie im normalen Betrieb. Fehlt künftig eine Liste, bricht der Lauf ab.

Fables Nachfragen sind beantwortet. Eine betrifft einen Fehler auf unserer Seite: Ein Protokoll, das wir für nicht vorhanden hielten, gibt es doch. Das Regelwerk hatte recht. Am Ergebnis ändert das nichts.

Offen sind zwei Auslegungsfragen an Fable. Erstens: Zählt das Öffnen von Systemdateien, etwa der Paketliste, als „Lesen von ausserhalb“? Zweitens: Muss die Menge der tatsächlich geladenen Werte gleich der Liste sein, oder genügt es, dass jede Lücke mit Grund protokolliert ist? Dazu kommen ein Vorschlag, wie eine Regel genauer formuliert werden sollte, und die Frage, welche der übrigen Notlösungen im Code vor dem Stichtag noch beseitigt werden müssen.
