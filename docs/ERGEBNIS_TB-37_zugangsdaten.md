# Ergebnis TB-37 — Zugangsdaten trennen

**Stand:** 15.09.2026 · **Basis:** `main` bei `e23e38f` (TB-36, PR #109)
**Zweig:** `claude/new-session-d2nlap`
**Ausführlich:** `research/zugangsdaten/BERICHT.md` ·
**Am Mac:** `docs/TESTAUFTRAG_TB-37_zugangsdaten.md`

---

## Das Ergebnis in vier Sätzen

`shared/fetch_binance_data.py` lag in keinem Commit, in keinem Zweig, auf
keinem Server — nur auf dem MacBook, und **neun Module hingen an ihr, fünf im
täglichen Live-Betrieb**. Ab jetzt ist der **Code** im Repo und die
**Schlüssel** sind es nicht: sie kommen aus der Umgebung, ersatzweise aus der
weiterhin gitignorierten `.env`. **Kein einziger Aufrufer musste geändert
werden** — die Signatur wurde aus den Aufrufern erschlossen, nicht gesetzt.
Der Schnitt selbst geschieht am Mac, nach einer Anleitung, in der kein Befehl
je einen Schlüssel anzeigt.

---

## 1. Die neun Module

| # | Modul | Intervall | Lookback | Ergebnis |
|---|---|---|---|---|
| 1 | `shared/fetch_multi_data.py` | `1h` | `1 Jan, 2017` | → CSV |
| 2 | `strategies/elliott_wave/forward_test.py` | `1h` | `90 day ago UTC` | **Handel** |
| 3 | `strategies/rsi2_crypto/fetch_1d_data.py` | `1d` | `1 Jan, 2017` | → CSV |
| 4 | `strategies/rsi2_crypto/forward_test.py` | `1d` | `400 day ago UTC` | **Handel** |
| 5 | `strategies/t3_supertrend/fetch_4h_data.py` | `4h` | `1 Jan, 2017` | → CSV |
| 6 | `strategies/t3_supertrend/forward_test.py` | `4h` | `120 day ago UTC` | **Handel** |
| 7 | `strategies/turtle_soup_crypto/forward_test.py` | `1d` | `400 day ago UTC` | **Handel** |
| 8 | `strategies/volatility_breakout_crypto/fetch_1d_data.py` | `1d` | `1 Jan, 2017` | → CSV |
| 9 | `strategies/volatility_breakout_crypto/forward_test.py` | `1d` | `400 day ago UTC` | **Handel** |

Alle neun rufen **identisch** auf: drei Argumente der Reihe nach, keines
benannt. Daraus die Signatur `fetch_historical_data(symbol, interval,
lookback)`. Mechanisch ermittelt über den Syntaxbaum
(`research/zugangsdaten/geruest.py`), nicht aus dem Gedächtnis — eine Liste
von Hand wäre am Tag nach der nächsten Änderung falsch, ohne dass es auffiele.

**Die Zusicherungen:** sechs Spalten `open_time, open, high, low, close,
volume` ohne `close_time`; Zeitstempel `2017-08-17 04:00:00` bzw. `2017-08-17`;
Zahlen als `float`; aufsteigend sortiert; **die laufende Kerze ist enthalten**
(`abrufschutz` schneidet sie ab, die fünf `forward_test.py` brauchen sie).

**Was nicht erschließbar war** — fünf Punkte, ausdrücklich als *unbekannt*
berichtet und nicht vermutet: Ratenbegrenzung, Wiederholversuche, Zeitzone,
ob die Schlüssel überhaupt gebraucht werden, Fehlerverhalten bei unbekanntem
Symbol. Punkte 1–3 und 5 entscheiden sich am Mac; Punkt 4 beantwortet
Schritt 7 des Testauftrags am Verhalten.

---

## 2. Die drei Entscheidungen

| Frage | Entschieden | Warum |
|---|---|---|
| Neue Datei oder Ersetzung? | **Ersetzung**, gleicher Pfad, gleicher Modulname | Die neun binden sie als Top-Level-Modul über `shared/` in `sys.path` ein. Eine zweite Datei fände keiner von ihnen — **alle neun müssten geändert werden**, und das ist ausgeschlossen. Zweitens: zwei Wege zu denselben Daten, wovon dieses Projekt schon zu viele hat. |
| Fehlende Schlüssel? | **Läuft weiter, meldet sich einmal, liefert nie still leer** | `/api/v3/klines` ist öffentlich und braucht keinen Schlüssel — für den Datenpfad löst sich die Abwägung auf. Meldung einmal je Prozess nach `stderr` (25 Symbole × 5 Bots wären Lärm). Eine leere Antwort wird als `AbrufLeer` **geworfen**, nie geliefert: ein leeres Ergebnis sieht im Bot genauso aus wie „kein Signal". |
| `.env.beispiel` ins Repo? | **Ja** | Sie beantwortet die Frage, die sonst nur die verlorene Datei beantworten konnte: wie die Namen heißen. Ohne Werte; `*.env` trifft sie nicht (mit `git check-ignore` nachgeprüft). |

> **Wichtig zur zweiten Entscheidung:** Ein `raise` allein wäre **nicht laut
> genug**. Alle neun Aufrufer fangen `except Exception` **je Symbol** ab und
> drucken „Fehler bei {symbol}". Deshalb zusätzlich die eigene Meldung nach
> `stderr` — und deshalb blockiert ein fehlender Schlüssel den Live-Betrieb
> auch nicht.

---

## 3. Berichtet, nicht entschieden: `python-binance` gegen stdlib

**Gebaut mit `python-binance`** — also so, wie es war. Das ist keine
Entscheidung gegen die stdlib, sondern die Weigerung, eine ausdrücklich zur
Berichterstattung gestellte Frage nebenbei zu entscheiden.

**Für `shared/binance_historie.py` als Unterbau:** es blättert schon in
1000er-Schritten, `als_dataframe` liefert **exakt dieselben sechs Spalten in
derselben Schreibweise**, es hat eine echte Ratenbegrenzung (Mindestpause,
`x-mbx-used-weight-1m`, `Retry-After` bei 429, Abbruch bei 418) — was
`python-binance` nicht hat — und es braucht eine Abhängigkeit weniger.

**Dagegen — und es wiegt schwer:** die **Lookback-Grammatik**. Die neun
übergeben `"400 day ago UTC"` und `"1 Jan, 2017"`; das ist die Schreibweise
von `python-binance` (über `dateparser`). `binance_historie` rechnet in
Millisekunden. Sie nachzubauen hieße, ausgerechnet die Stelle nachzubauen, an
der eine stille Abweichung teuer wird: **wie weit zurück geladen wird,
entscheidet über den Inhalt von `data/` und damit über den Datenstand-Hash der
Vorregistrierung.** Die Schreibweise ändern ließe sich nur, indem man alle
neun Aufrufer anfasst. Dazu käme eine Zweitrolle für ein Werkzeug, das für das
*Zurückladen* gebaut wurde.

**Empfehlung: nicht jetzt.** Der Schnitt Code/Schlüssel ist für sich ein
Eingriff in den Live-Pfad von fünf Bots. Den Transport im selben Zug zu
tauschen, machte zwei Änderungen ununterscheidbar, wenn danach etwas klemmt.
Wenn, dann als eigener Schritt — Schritt 7 des Testauftrags legt die Messlatte.

---

## 4. Vier Befunde

### ⚠️ 4.1 `git pull` überschreibt eine gitignorierte Datei ohne Warnung

**Nachgemessen, nicht vermutet.** Fügt ein Commit eine Datei an einem Pfad
hinzu, an dem lokal eine gitignorierte Datei liegt, überschreibt `git pull`
sie **kommentarlos** — keine Rückfrage, keine Warnung, nur `create mode
100644`.

**Folge:** Ein `git pull` des TB-37-Zweigs auf dem MacBook **löscht die
einzige Kopie der Zugangsdaten** — genau den Verlust, den TB-37 verhindern
soll. Deshalb ist Schritt 0 des Testauftrags die Sicherung, *vor jeder
git-Operation*, und Schritt 1 prüft sie nach.

### 4.2 Die Namen waren nie unbekannt — und eine Wache wird dadurch scharf

`broker/zugang.py:101` führt seit jeher `DATENABRUF_VARIABLEN =
("BINANCE_API_KEY", "BINANCE_API_SECRET")` und bezeichnet sie ausdrücklich als
die Schlüssel von `shared/fetch_binance_data.py`. Die Namen sind also die im
Repo dokumentierten, nicht geraten; der Selbsttest rechnet das nach.

**Und daran hängt mehr:** `get_zugang()` bricht ab, wenn ein **Testnet**-
Schlüssel mit einem dieser beiden übereinstimmt — eine Verwechslungssperre
gegen den schlimmsten denkbaren Fehlgriff. Sie konnte **bisher nicht
greifen**, weil die echten Schlüssel in einer Python-Datei standen und nicht in
der Umgebung. Stehen sie in der `.env`, findet die Sperre sie — und tut zum
ersten Mal, wofür sie geschrieben wurde. **`broker/` wird dafür nicht
angefasst.**

### 4.3 Der Kursabruf braucht diese Schlüssel vermutlich gar nicht

`/api/v3/klines` ist öffentlich; `shared/binance_historie.py` holt darüber die
gesamte Historie seit 2017 ohne Schlüssel; `shared/get_top_symbols.py:15` und
`shared/fetch_multi_data.py:46` bauen `Client()` **ohne** Zugangsdaten —
letzteres in derselben Datei, die `fetch_historical_data` aufruft.

**Kein Beweis**, aber stark genug: Schritt 7 des Testauftrags prüft es **am
Verhalten**. Fällt er positiv aus, kann der Betreiber erwägen, die Schlüssel
eines **echten** Kontos gar nicht erst in die `.env` zu schreiben — der
sicherste Schlüssel ist der, der nirgends liegt.

### 4.4 Woran hängt das System noch, das es nur einmal gibt?

**13 von 22** `.gitignore`-Einträgen werden von Betriebscode gelesen. Vier
wären bei Verlust nicht oder kaum zu ersetzen:

| Eintrag | | Warum |
|---|---|---|
| `*.db` | **UNERSETZLICH** | Die Handelsdatenbanken **aller neun Bots** — der gesamte Forward-Test-Verlauf. Nicht neu berechenbar: die Signale entstanden zu Zeitpunkten, die vorbei sind. **Der größte Posten — größer als der, der TB-37 ausgelöst hat.** |
| `config/email_config.py` | **UNERSETZLICH** | Zugangsdaten im Klartext, von **17 Betriebsmodulen** gelesen. Dieselbe Risikoklasse wie `fetch_binance_data.py` vor TB-37 — **derselbe Schnitt wäre möglich**. |
| `.env` | **UNERSETZLICH** | Trägt jetzt die Binance-Schlüssel — die neue einzige Kopie. Gehört zusätzlich in die Passwortverwaltung. |
| `notifications/warteauftraege.json` | **HEIKEL** | Wartende Ausstiegsaufträge, die ein Cronjob **ohne Rückfrage** ausführt. Verlust bleibt **unbemerkt**, weil „keine Warteaufträge" der Normalfall ist. |

**Wurde versehentlich etwas ausgeschlossen, das ins Repo gehört?** Geprüft
wurde die **Form**: ein Eintrag, der eine **Quelltextdatei** nennt, ist der
Geruch — Zustandsdateien entstehen neu, Quelltext nicht. Vorher **zwei** solche
Einträge, jetzt **einer** (`config/email_config.py`). Die Erweiterungen aus
TB-34 und TB-35 betreffen ausschließlich Laufzeitzustand und Sicherungen —
dort wurde nichts versehentlich ausgeschlossen. Alle 22 Muster zusätzlich mit
`git check-ignore` gegengeprüft.

---

## 5. Was gebaut wurde

| Datei | |
|---|---|
| `shared/fetch_binance_data.py` | **Neu im Repo.** Code versioniert, Schlüssel aus der Umgebung. |
| `.env.beispiel` | Die zwei Namen, ohne Werte. |
| `.gitignore` | Eintrag `shared/fetch_binance_data.py` **entfernt**; `.env` bleibt ausgeschlossen. |
| `shared/test_fetch_binance_data.py` | 77 Prüfungen, davon 5 Mutationsproben. |
| `research/zugangsdaten/geruest.py` | Was muss der versionierte Teil können? |
| `research/zugangsdaten/gitignoriert.py` | Woran hängt das System, das es nur einmal gibt? |
| `research/zugangsdaten/BERICHT.md` | Der ausführliche Bericht. |
| `docs/TESTAUFTRAG_TB-37_zugangsdaten.md` | 12 Schritte für den Mac, jeder Befehl einzeilig. |
| `CLAUDE.md`, `docs/UEBERGABEPROTOKOLL.md` | Nachgezogen. |

**Nicht angefasst:** kein `forward_test.py`, kein `live_params.py`, nichts
unter `broker/`, keine Datei unter `data/`, keine Crontab, kein
`results/*.csv`, `research/vorregistrierung/auswertung.py` eingefroren,
`docs/VORREGISTRIERUNG_neuselektion.md` unberührt, die sieben genannten
`shared/`-Module unberührt, `research/faltenplan_neun/` nicht berührt.

---

## 6. Wie geprüft wurde

`python3 shared/test_fetch_binance_data.py` → **77 von 77 Prüfungen
bestanden.**

**Ohne Netz, ohne `python-binance`.** Ersetzt wird **genau eine** Stelle — dort,
wo python-binance sein Ergebnis abliefert. Alles davor und danach läuft echt.

**Die Schreibweise wird zeichengleich geprüft:** eine erzeugte Kerze wird durch
`to_csv` geschrieben und gegen die **erste Zeile von `data/BTCUSDT_{1h,4h,1d}.csv`**
verglichen. Damit ist ausgeschlossen, dass der Datenstand-Hash sich ändert,
ohne dass ein Kurs anders wäre.

**Kein Schlüssel im Repo** — zwei unabhängige Prüfungen, beide mit einem
eingepflanzten Schlüssel gegengeprüft; die Probe dafür **entsteht zur
Laufzeit**, damit sie nicht selbst in einer Datei steht.

**Die zwei Fallen:** fünf **Mutationsproben** schalten jede Absicherung einzeln
aus; danach muss genau die zugehörige Prüfung fallen — **und die übrigen vier
stehen bleiben**. Die zweite Falle trat in dieser Sitzung real auf: eine
Prüfung lief über `git ls-files` und übersah neu hinzugekommene Dateien; ein
eingepflanzter Schlüssel wurde nur von der *zweiten* Prüfung gefunden. Behoben,
danach schlagen beide an.

**Basislauf auf unverändertem `main`** (`e23e38f`, eigener git-Arbeitsbaum)
gegen den Zweig:

| | Tests | grün |
|---|---|---|
| `main` (`e23e38f`) | 52 | 41 |
| Zweig (`e64f656`) | **53** | **42** |

**Der einzige Unterschied ist die neue Zeile** `shared/test_fetch_binance_data.py`
mit Rückgabewert `0`. Kein Test, der vorher grün war, ist rot geworden.

Die 11 roten sind auf beiden Seiten dieselben: fehlende Cloud-Abhängigkeiten
(`fastapi`, `scipy`, Zeitzone `US/Eastern`), drei Tests, die ein Argument
verlangen (`test_drawdown.py <bot>` usw.), `test_drawdown_beide_masse.py`
(Zeitüberschreitung), `test_portfolio_sicht.py` und `test_kursdaten.py`
(66/68 bzw. 62/66) sowie `test_stabile_sortierung.py` und
`test_wellenauswahl.py` (`ergebniskurven.py` meldet `9x AKTUELL`). Alle in
der Aufgabenbeschreibung als vorbestehend genannt bzw. dort erklärt.

---

## 7. Was jetzt zu tun ist

1. **Testauftrag am Mac ausführen** — `docs/TESTAUFTRAG_TB-37_zugangsdaten.md`.
   **Schritt 0 nicht überspringen.**
2. Zurückmelden: die Tabelle am Ende des Testauftrags und das ZIP aus
   `~/Downloads`.
3. Danach entscheiden (nicht Teil von TB-37):
   * `config/email_config.py` nach demselben Muster schneiden — der Weg ist
     jetzt gebaut und einmal erprobt.
   * Eine Sicherung für die **Handelsdatenbanken**. Die größere Aufgabe.
   * Ob die Schlüssel des echten Kontos überhaupt in die `.env` sollen
     (siehe Befund 4.3).
   * `python-binance` gegen stdlib — als eigener Schritt.

---

## In einfacher Sprache

**Was wir wissen wollten.**
In diesem Projekt gab es eine einzige Datei, die auf keinem Server und in
keiner Sicherung lag — nur auf dem MacBook. Fünf von neun Handels-Programmen
brauchten sie jeden Tag. Wäre das MacBook kaputtgegangen, hätten fünf
Programme gestanden, und niemand hätte die Datei wiederherstellen können. Wir
wollten wissen: Was genau muss sie können, und wie bekommen wir sie in die
Sicherung, ohne die Passwörter mit hineinzulegen, die darin stehen?

**Was herauskam.**
Der Text der Datei — das Programm — liegt jetzt im Sicherungssystem. Die
Passwörter nicht: die kommen aus einer eigenen kleinen Datei namens `.env`, die
weiterhin nur auf dem MacBook liegt. Die neun Programme merken davon nichts,
**kein einziges musste geändert werden**. Nebenbei kam heraus, dass das
Programm die Passwörter zum Kurse-Holen wahrscheinlich gar nicht braucht — die
Kurse sind öffentlich abrufbar.

**Warum das so ist.**
Ein Programm und ein Passwort sind zwei verschiedene Dinge, auch wenn sie in
derselben Datei stehen. Das Programm darf jeder sehen und soll gesichert
werden; das Passwort darf niemand sehen und darf nicht gesichert werden. Weil
beides zusammen in einer Datei lag, musste die ganze Datei ungesichert
bleiben. Jetzt sind sie getrennt, und jedes wird behandelt, wie es soll.

**Was das für dich heißt.**
Am MacBook sind ein paar Schritte nötig, und die Reihenfolge ist wichtig:
**zuerst eine Sicherheitskopie anlegen, erst danach das Update holen.** Wir
haben nachgemessen, dass das Update die alte Datei **ohne zu fragen und ohne
es zu melden** überschreibt. Wer zuerst kopiert, kann jederzeit zurück; wer es
vergisst, verliert die Passwörter. Die Anleitung führt Schritt für Schritt
durch, jeder Befehl passt in eine Zeile fürs iPhone, und kein Befehl zeigt
jemals ein Passwort an.

Zwei Dinge sind uns aufgefallen, die **nicht** zu dieser Aufgabe gehören, aber
wichtiger sein könnten: Die **Aufzeichnungen aller Test-Geschäfte** seit Beginn
liegen ebenfalls nur auf dem MacBook und lassen sich nicht neu berechnen. Und
die Datei mit den **E-Mail-Zugangsdaten** hat genau dasselbe Problem wie die,
die wir gerade repariert haben. Für beides wäre der nächste Schritt derselbe
Weg, den wir jetzt einmal gegangen sind.
