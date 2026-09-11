# Testergebnis — Positionsanzahl je Bot + Notbremse zu Beginn

Branch `claude/new-session-uqjk8h`, Basis `origin/main` (`c2b6995`).
Alles unten in dieser Sitzung ausgeführt, nicht geschätzt.

## Ergebnis: alles grün

| Suite | Erwartet | Ergebnis | vorher |
|---|---|---|---|
| `broker/test_broker.py` | 163 | **163 / 163** ✅ | 149 |
| `broker/test_ibkr.py` (mit `ib_async`) | 200 | **200 / 200** ✅ | 186 |
| `broker/test_ibkr.py` (ohne `ib_async`) | 168 | **168 / 168** ✅ | 154 |
| `dashboard/test_dashboard.py` | 753 | **753 / 753** ✅ | 738 |
| `dashboard/test_gewichtung.js` | 35 | **35 / 35** ✅ | 27 |

Keine Regression in den unbeteiligten Suiten:

| Suite | Ergebnis |
|---|---|
| `notifications/test_manual_close.py` | **118**, 0 fehlgeschlagen ✅ |
| `shared/test_empfehlung_format.py` | **70 / 70** ✅ |
| `system/test_caffeinate_plist.py` | **52 / 52** ✅ |
| `dashboard/test_zustandsmaschine.js` | **27 / 27** ✅ |
| `dashboard/test_zeitzone.js` | **24 / 24** ✅ |

**Keine bestehende Prüfung wurde geändert oder entfernt.**
`git diff origin/main HEAD` über die vier Testdateien entfernt **0** Zeilen —
alle Teständerungen sind Hinzufügungen (+56 Prüfungen).

## Mutationsproben: 13 von 13 erkannt

| Probe | Mutation | Erkannt von |
|---|---|---|
| M1 | Anzahl-Zeile aus `gewichtungsZeilen()` entfernt | „Der Dialog weist die Anzahl der Positionen JE BOT aus" |
| M2 | Anzahl-Zeile aus `notfallErgebnisAnzeigen()` entfernt | „Die Ergebnisanzeige weist die Anzahl je Bot ebenfalls aus" |
| M3 | `positionsanzahlZeilen()` liefert immer nichts | dito M1 |
| M4 | Anzahl als `title`-Tooltip statt sichtbarer Zeile | „Sie ist sichtbarer Text, kein title-Tooltip" |
| M5 | fehlende Anzahl wirft statt Strich | Abbruch der Suite (Ausnahme) |
| M6 | Binance: Prüfung zu Beginn entfernt | „Ohne offene Aufgabe wird die Notbremse trotzdem SICHTBAR gemeldet" |
| M7 | Binance: Prüfung **je Aufgabe** entfernt | „… der Client wird dafür nicht mehr gefragt" (2 statt 1 Order-Versuch) |
| M8 | Binance: Notbremse gilt als Fehlschlag | „Rückgabewert 0 ohne offene Aufgabe — Cron schlägt NICHT falsch Alarm" |
| M9 | Binance: offene Aufgaben verschwinden aus der Nachverfolgung | „… statt spurlos zu verschwinden" |
| M10 | Binance: Meldung in DEBUG versteckt statt WARNING | dito M6 |
| M11 | IBKR: Prüfung zu Beginn entfernt | Abbruch (TWS-Verbindung wird versucht) |
| M12 | IBKR: Prüfung **je Aufgabe** entfernt | „… die Verbindung wird dafür nicht mehr gefragt" |
| M13 | IBKR: Notbremse gilt als Fehlschlag | dito M8 |

Jede Mutation stellt die Datei danach byteweise wieder her; `git status` ist
hinterher leer. Das Skript steht in
`docs/TESTAUFTRAG_positionsanzahl_und_notbremse.md`, Schritt 5.

> **Anmerkung zu M7/M12:** beide gingen in der ersten Fassung **unentdeckt**
> durch. Ursache: unter der Prüfung je Aufgabe liegt eine dritte Ebene
> (`binance_testnet.marktorder()` / `ibkr_paper.marktorder()`), die die Bremse
> ebenfalls prüft — nimmt man die mittlere heraus, bleibt trotzdem jede Order
> aus. Die Prüfung unterscheidet die Ebenen jetzt daran, wie oft der Client
> überhaupt gefragt wurde und von welcher Ebene der Grund stammt. Seitdem:
> erkannt.

## Teil 1 — was inhaltlich geprüft wurde

* Die Anzahl je Bot erscheint in **allen vier** bot-übergreifenden Ansichten:
  `alle-schliessen` (Übersicht + Ergebnis) und `alle-bots-schliessen`
  (Übersicht + Ergebnis). ✅
* Geprüft wird **je Funktion**, nicht im ganzen Dokument — fünf Ansichten
  einzeln in `test_dashboard.py`, plus die wirklich erzeugte Ausgabe in
  `test_gewichtung.js`. ✅
* **Sichtbare Zeile**, kein `title`-Tooltip (iPhone hat kein Hover), mit
  derselben CSS-Klasse und Block-Regel wie `GEWICHTUNG_ERLAEUTERUNG`. ✅
* **Eine Quelle** in `app.js`; `bot.html` und `index.html` definieren sie
  nicht selbst. ✅
* **Blockiert den Notfallweg nicht:** fehlendes Feld, leere Liste, kaputte
  Liste, fehlende Anzahl eines Bots, fehlender Name — in keinem Fall eine
  Ausnahme, geschlossen wird trotzdem. ✅
* Erzeugte Ausgabe mit sieben Elliott- und einer fremden Position:
  `Eingegangene Positionen je Bot – Elliott Wave (Krypto): 7; Turtle Soup
  (Aktien): 1.` ✅
* **Unverändert:** Gewichtungsformel, `pnl_gewichtet`, `pnl_schnitt_pct`,
  `pnl_bestes_pct`, `pnl_schlechtestes_pct`, Ausschluss-Mechanismus.
  `dashboard/schliessen.py` ist byteweise gleich. ✅

## Teil 2 — was inhaltlich geprüft wurde

Je Brücke (`broker/STOP` und `broker/STOP_IBKR`):

* Bei **null** offenen Aufgaben erscheint die sichtbare Meldung `NOTBREMSE
  aktiv (…)` mit Pfad und dem Hinweis, dass der Lauf beendet wird. ✅
* **Testnet bzw. TWS werden gar nicht erst kontaktiert** (Binance: keine
  einzige Anfrage; IBKR: `konto is None`, weil nicht verbunden wurde). ✅
* **Rückgabewert 0** ohne offene Aufgabe, **1** mit offener Aufgabe. ✅
* Ohne gezogene Bremse steht die Zeile **nicht** da. ✅
* Offene Aufgaben stehen beim Abbruch mit Grund in der Nachverfolgung. ✅
* Die **bestehende Prüfung je Aufgabe greift weiterhin** — mit einer echt
  mitten im Lauf angelegten Datei geprüft: erste Order draußen, zweite von
  Ebene 2 gestoppt. ✅

## Begründung des Rückgabewerts (kurz)

**0** bei gezogener Bremse ohne offene Aufgaben. Die Bremse ist eine
befolgte Anweisung des Nutzers, kein Fehlschlag, und es ist nichts
liegengeblieben. Cron alarmiert über die Fehlermail; bei jedem Lauf eine zu
schicken, solange die Bremse absichtlich gezogen ist (beim 4-Stunden-Takt
sechs am Tag, tagelang), entwertet genau die Mails, auf die es ankommt. Dass
die Bremse wirkt, steht sichtbar im Protokoll — zweimal — und nicht im
Rückgabewert. **Mit** offener Aufgabe bleibt es beim bisherigen **1**: da ist
tatsächlich etwas nicht ausgeführt worden.

## Was nicht angefasst wurde

Keine `live_params.py`, keine `forward_test.py`, keine
`equity_simulation.py`, kein Schema der `trades`-Tabelle, keine
launchd-Vorlage, keine Crontab, kein `dashboard/schliessen.py`.
`git diff origin/main HEAD --name-only` listet zehn Dateien (zwei Anzeige,
zwei Brücken, zwei READMEs, vier Testdateien) plus drei Dokumente unter
`docs/`.

## Offen

Der Dialog wurde **nicht im Browser** angesehen — die Anzeige ist über die
erzeugte Ausgabe geprüft (Node, ohne Browser), nicht am iPhone. Ein Blick auf
die fertige Seite bei Gelegenheit wäre trotzdem gut, vor allem auf den
Zeilenumbruch der neuen Zeile, wenn viele Bots gleichzeitig betroffen sind.
