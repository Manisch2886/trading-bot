# Übergabe: Übergabeprotokoll und CLAUDE.md nachgezogen

**Für die Review-Sitzung.** Reine Dokumentationsaufgabe — kein Produktivcode,
keine Tests, kein Bot-Ordner angefasst.

Branch `claude/new-session-uqjk8h` (frisch von `origin/main` aufgesetzt, nachdem
PR #73 gemergt wurde), Basis `origin/main` (`5e3fb27`).

Geändert wurden **genau zwei Dateien**: `CLAUDE.md` und
`docs/UEBERGABEPROTOKOLL.md`. Nachweis: `git diff origin/main HEAD --name-only`.

---

## 1. Warum das dringend war

`docs/UEBERGABEPROTOKOLL.md` stammte vom 2026-09-09 (PR #63) und hinkte den
Merges **#64 bis #73** hinterher. Zwei Stellen waren dabei nicht bloß
unvollständig, sondern **falsch** — und zwar an der gefährlichsten Stelle, die
dieses Dokument hat:

> „ein Telegram-Bot und ein Web-Dashboard, **beide rein lesend**" (Abschnitt 1)
>
> „Beide lesen ausschliesslich; **keiner von beiden verändert einen Bot, eine
> Datenbank oder einen Parameter.**" (Abschnitt 4.3)
>
> „**Im aktuellen `main`-Stand existiert diese Funktion nicht** — Telegram und
> Dashboard sind dort rein lesend." (Abschnitt 9, Punkt 7)

Das Dashboard schreibt seit PR #62 in die Live-Datenbanken aller neun Bots und
seit PR #71 sogar **zeitversetzt ohne erneute Rückfrage**. Eine Sitzung, die
sich auf diese Sätze verlässt, hält einen Schreibpfad für eine Leseansicht.

`CLAUDE.md` erwähnte `broker/` mit **keinem Wort**. Eine künftige Sitzung wusste
damit nicht, dass es im Projekt einen Weg gibt, der Orders an echte Gegenstellen
schickt.

---

## 2. Was in `CLAUDE.md` steht (neu)

Ein eigener, hervorgehobener Abschnitt **„⚠️ `broker/` — echte Orders an echte
Gegenstellen"** direkt nach dem Kurzüberblick, mit:

- der Tabelle beider Brücken samt Stand (Binance-Testnet produktiv; IBKR-Paper
  gemergt, aber nie gegen eine echte TWS gelaufen),
- der Regel **„`--echt` wird NIE ohne ausdrückliche Zustimmung des Nutzers
  aufgerufen"**, ausdrücklich auch dann nicht, wenn eine Aufgabe es nahezulegen
  scheint,
- der Notbremse auf drei Ebenen und ihren beiden Dateien,
- der bekannten Einschränkung: `ib_async` verlangt Python 3.10+, der Rechner des
  Nutzers läuft auf 3.9.6 — die IBKR-Brücke ist dort **nicht lauffähig**.

Dazu in den Grundregeln: das Dashboard ist **nicht mehr rein lesend**, der
Telegram-Bot schon; und `requirements.txt` als Ort der Abhängigkeiten.

---

## 3. Was im Übergabeprotokoll steht (neu oder korrigiert)

| Abschnitt | Was |
|---|---|
| **Kopf** | Stand 2026-09-09 → **2026-09-11**, mit der Angabe, welche Merges nachgezogen wurden |
| **1** | „beide rein lesend" korrigiert; die beiden Broker-Brücken ergänzt |
| **4.1** *(neu)* | Überschrift für die Ordnerstruktur — siehe Befund B1 unten |
| **4.1** | Baum ergänzt: `broker/`, `system/`, `requirements.txt`, `manual_close.py`, `boersenkalender.py`, `warteauftraege.py`, `schliessen.py`, `warteauftraege_ausfuehren.py`, `pruefe_warteauftraege_kopie.py`, die Testdateien, die `.plist`-Vorlagen, `docs/UEBERGABE_*.md` |
| **4.2** *(neu)* | Überschrift für die Sync-Reihe — siehe Befund B1 |
| **4.3** | **Die falsche Einleitung korrigiert**, samt Tabelle wer liest und wer schreibt. Die drei Schliess-Wege, die eine schreibende Kernfunktion, die Warteaufträge mit ihren drei Zuständen und der Hinweis, dass **ohne Cronjob nichts passiert** |
| **4.4** *(neu)* | Beide Broker-Brücken: Gegenstellen, Wege, Notbremse auf drei Ebenen, was sie **nicht** sind, und die zwei Einschränkungen (nie gegen echte TWS; Python 3.9) |
| **4.5** *(neu)* | Die drei launchd-Dienste, der Schlaf-Vorfall vom 11.09.2026 samt Ausfällen, die gewählten Flags und die **vier dokumentierten Grenzen** |
| **5** | `quarterly_review.py` und `agent_optimise.py` als **nicht** bei allen neun vorhanden gekennzeichnet — siehe Befund B2 |
| **6.4** | Der Satz, die Cronjob-Frage sei „mit sechs weiteren Bots grösser geworden", korrigiert — siehe Befund B2 |
| **8** | Acht neue Zeilen: Dashboard-Weg gemergt / Telegram-Weg geschlossen, alle neun Bots freigeschaltet, **zeitversetzte Ausführung ohne erneute Bestätigung**, „unbekannt → weder noch", die beiden Broker-Brücken, **die dreistufige Notbremse samt Begründung des Rückgabewerts**, die Positionsanzahl je Bot, `caffeinate` als Dienst |
| **9** | Punkt 7 von Grund auf richtiggestellt; Punkt 8 zusammengeführt; **drei neue Punkte 10–12** (Warteauftrags-Cronjob, IBKR nicht lauffähig, Dauerbetrieb ungeprüft); die doppelte Nummer 7 beseitigt — siehe Befund B3 |
| **10** | „Wo wir stehen" um den Charakterwechsel ergänzt; zweite PR-Reihe #62–#73 als Tabelle; „Was als Nächstes" neu sortiert; zwei neue Punkte in der Kontext-Liste (`broker/` sendet echt; das Dashboard schreibt) |

Die Abschnittsnummerierung bleibt vollständig erhalten — Verweise aus älteren
Dokumenten auf „Abschnitt 4.3", „Abschnitt 8" oder „Abschnitt 9, Punkt 7" gehen
weiterhin auf, und Punkt 7 beschreibt weiterhin dasselbe Thema, nur jetzt
richtig.

---

## 4. Teil B — zusätzlich gefundene Abweichungen

Das waren die Funde **jenseits** der vier bekannten Lücken. Korrigiert wurde
nur, was eindeutig ist; alles andere steht hier zur Entscheidung.

### Korrigiert (eindeutig)

**B1 — Zwei Querverweise zeigten ins Leere.** Abschnitt 4 hatte Unterabschnitte
`4.3`, aber **keine** `4.1` und `4.2`. Gleichzeitig verwiesen zwei Stellen
(Methodik-Grundsatz 11 und Abschnitt 10.1) auf „Abschnitt 4.2". Die
Überschriften **4.1 Ordnerstruktur und Pfad-Auflösung** und **4.2 Ein Wert, eine
Quelle** wurden über den bereits vorhandenen Text gesetzt. Kein Text verschoben,
keine Nummer geändert — die Verweise stimmen jetzt.

**B2 — `quarterly_review.py` und `agent_optimise.py` gibt es nur bei drei von
neun Bots.** Abschnitt 5 führte beide im „gemeinsamen Muster in jedem der neun
`strategies/<name>/`-Ordner". Tatsächlich liegen sie nur bei `elliott_wave`,
`elliott_wave_stocks` und `t3_supertrend`. Das hat eine Folge für Abschnitt 9,
Punkt 2 und Abschnitt 6.4: dort stand, die Frage nach den Quartals-Cronjobs sei
„mit sechs weiteren Bots grösser geworden". Sie ist **kleiner**, als sie aussah
— für sechs Bots kann es gar keinen Eintrag geben. Beide Stellen sind
entsprechend eingegrenzt; ob das Quartals-Review auf die sechs Prototypen
ausgeweitet werden soll, ist als **offene Entscheidung des Nutzers** benannt,
nicht als vergessene Einrichtung.

**B3 — Abschnitt 9 hatte zweimal die Nummer 7.** Am Ende der Liste stand ein
zweiter, wortreicherer Punkt „7" zum iOS-Safari-Thema, das Punkt 8 bereits
kürzer behandelte. Der Inhalt beider ist jetzt vollständig in Punkt 8
zusammengeführt; die Liste läuft durchgehend von 1 bis 12.

**B4 — PR #61 ist nicht „offen", sondern geschlossen.** Das Protokoll führte PR
#61 und #62 gemeinsam als „zwei offene Pull Requests". #62 ist gemergt, **#61
wurde am 2026-09-10 ohne Merge geschlossen** (per GitHub-API geprüft). Der
Telegram-Bot bleibt dauerhaft rein lesend; im Quelltext von `telegram_bot.py`
steht das ausdrücklich so. Die Kernfunktion `manual_close.py` stammt allerdings
aus #61 und ist in Betrieb — das ist in Abschnitt 4.3 und 8 festgehalten, damit
niemand sie für verworfen hält.

**B5 — Freigeschaltet sind alle neun Bots, nicht nur `t3_supertrend`.** Das
Protokoll sagte „beide nur für `t3_supertrend`". `SCHLIESSBARE_BOTS` enthält
heute alle neun (im Repo nachgezählt).

**B6 — Zwei gitignorete Dateien standen ohne Kennzeichnung im Baum.**
`shared/fetch_binance_data.py` und `config/email_config.py` sind in
`.gitignore` und liegen nur auf dem Rechner des Nutzers. Im Baum stand das
nicht dabei — für eine Sitzung, die im Repo nachsieht, sind sie schlicht
abwesend. Jetzt gekennzeichnet.

**B7 — Kleinere Lücken im Baum.** `config/` enthält zusätzlich
`sp500_top50.txt` und `sp500_top25.txt`, `shared/` zusätzlich
`test_empfehlung_format.py`. Ergänzt.

### Geprüft und in Ordnung

- **`research/` = 17 Ordner** ✅ (Angabe stimmt), die vier namentlich genannten
  existieren alle.
- **„alle 13 Versandstellen"** für `empfehlung_format.py` ✅ — 9×
  `daily_summary_email.py` + 3× `quarterly_review.py` + 1×
  `weekly_portfolio_email.py`. Die beiden Agenten, die den Text *bauen* statt
  ihn zu versenden, sind zu Recht nicht mitgezählt.
- **`oos_equity_simulation.py` bei `elliott_wave` und `elliott_wave_stocks`** ✅
  — die Zeile war bereits korrekt eingeschränkt.
- **Neun `strategies/*/live_params.py`** vorhanden ✅, Bot-Tabelle unverändert
  richtig — es kam kein Bot hinzu. (Inhalte wurden auftragsgemäß **nicht**
  gelesen oder interpretiert.)
- **Testzahlen:** das Protokoll nennt keine, es war also nichts zu korrigieren.

### Benannt, nicht entschieden — bitte ansehen

**E1 — Die in der Aufgabe genannten Quelldokumente
`docs/ZUSAMMENFASSUNG_PR68_Binance_Testnet.md` und
`docs/ZUSAMMENFASSUNG_PR70_IBKR_Paper.md` existieren im Repo nicht.**
Unter `docs/` liegen nur `UEBERGABEPROTOKOLL.md`, `UEBERGABE_PR71_WARTEAUFTRAEGE.md`
und die drei Dokumente zu PR #73. Als Quelle für Abschnitt 4.4 habe ich deshalb
`broker/README.md` und `broker/README_IBKR.md` benutzt — beide sind in der
Aufgabe ebenfalls als Quelle genannt und decken den Stoff ab. **Falls es die
beiden Zusammenfassungen gibt** (lokal, in einem geschlossenen Branch, oder als
Chat-Text), lohnt ein Abgleich: sie könnten Entscheidungsgründe enthalten, die
in den READMEs nicht stehen.

**E2 — `broker/README_IBKR.md` nennt eine veraltete Testzahl.** Dort steht
„`broker/test_ibkr.py` | 183 Prüfungen"; tatsächlich sind es seit PR #73
**200** (mit `ib_async`) bzw. **168** (ohne). Nicht korrigiert, weil der Auftrag
Änderungen auf `docs/` und `CLAUDE.md` beschränkt. Eine Zeile in einem separaten
PR, wenn gewünscht.

**E3 — Die Cron-Angaben der Bot-Tabelle (Abschnitt 2) sind aus dem Repo nicht
überprüfbar.** Die Crontab liegt auf dem Mac. Belegbar waren nur die beiden
Brücken (die Binance-Zeile taucht als „12:05-Lauf" im Vorfallsbericht auf) und
der Warteauftrags-Eintrag aus der Testanleitung. Die Bot-Zeilen habe ich
unverändert gelassen, statt sie zu bestätigen. Ein `crontab -l` klärt das in
einer Minute — es steht als Punkt 1 in Abschnitt 10.4.

**E4 — Der Vorfall vom 11.09.2026 ist im Protokoll jetzt beschrieben, aber die
Folge ist nicht aufgearbeitet.** Zwischen 08:50 und 12:06 fielen Läufe aus; die
betroffenen `elliott_wave`-Forward-Tests und der 12:05-Lauf der Binance-Brücke
sind **nicht** nachgeholt worden (Cron holt nicht nach). Die Paper-Trading-Zahlen
dieses Tages beschreiben also eine Strategie, die so nicht gelaufen ist. Ob das
in den Auswertungen vermerkt werden soll — etwa als Lücke in den Ergebnis-CSVs
oder als Fussnote im Quartals-Review — ist eine offene Frage, die ich nicht
selbst entschieden habe.

---

## 5. Was nicht angefasst wurde

`git diff origin/main HEAD --name-only` listet **ausschliesslich** `CLAUDE.md`
und `docs/UEBERGABEPROTOKOLL.md` (plus die beiden neuen Dokumente unter
`docs/`). Kein Produktivcode, keine Testdatei, kein `strategies/`-Ordner, keine
`live_params.py`, keine `forward_test.py`, keine `equity_simulation.py`, keine
Crontab, keine launchd-Vorlage.

Es wurden keine Zugangsdaten in die Dokumentation übernommen. `.env`,
`config/email_config.py` und `shared/fetch_binance_data.py` sind nur **als
Dateinamen** erwähnt; ihr Inhalt wurde nicht gelesen.

## 6. Empfehlung für die Review

Die drei Stellen, die inhaltlich eine Entscheidung brauchen, sind **E1**
(fehlende Quelldokumente), **E2** (veraltete Zahl in einer Datei ausserhalb des
Auftragsumfangs) und **E4** (Umgang mit den ausgefallenen Läufen). Alles andere
ist belegt und kann so stehen bleiben.
