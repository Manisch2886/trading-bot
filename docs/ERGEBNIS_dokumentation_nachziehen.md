# Ergebnis — Dokumentation nachgezogen

Branch `claude/new-session-uqjk8h`, Basis `origin/main` (`5e3fb27`, nach Merge
von PR #73). Reine Dokumentationsaufgabe.

## Geändert: genau zwei Dateien

```
CLAUDE.md                    +25 Zeilen
docs/UEBERGABEPROTOKOLL.md  +213 / −30 Zeilen
```

Kein Produktivcode, keine Tests, kein `strategies/`-Ordner, keine `crontab`,
keine launchd-Vorlage. Keine Zugangsdaten übernommen.

## Die wichtigste Korrektur

Das Protokoll behauptete an **drei** Stellen, Telegram **und** Dashboard seien
rein lesend, zuletzt sogar ausdrücklich: „Im aktuellen `main`-Stand existiert
diese Funktion nicht."

Tatsächlich schreibt das Dashboard seit PR #62 in die Live-Datenbanken **aller
neun Bots** und seit PR #71 sogar **zeitversetzt ohne erneute Rückfrage**. Alle
drei Stellen sind richtiggestellt; der Telegram-Bot ist weiterhin korrekt als
rein lesend beschrieben.

## Die vier bekannten Lücken — alle geschlossen

| # | Thema | Wo es jetzt steht |
|---|---|---|
| 1 | **Warteaufträge** (PR #69/#71) | 4.3 (drei Zustände, „ohne Cronjob passiert nichts"), 8 (Vorab-Erlaubnis), 9 Punkt 10 (Cronjob-Status), 4.1 (Dateien + `requirements.txt`) |
| 2 | **caffeinate-Dienst** (PR #72) | **4.5 neu**: dritter launchd-Dienst, Vorfall vom 11.09.2026 (Mac schlief 08:50–12:06, 12:05-Lauf der Binance-Brücke und mehrere `elliott_wave`-Läufe fielen aus, Cron holt nicht nach), die vier dokumentierten Grenzen |
| 3 | **`broker/`** (PR #68/#70) | **4.4 neu** und ein eigener Warnabschnitt in `CLAUDE.md`: `--echt` nie ohne Zustimmung; IBKR nie gegen echte TWS gelaufen; `ib_async` braucht Python 3.10+, Nutzer hat 3.9.6 → dort nicht lauffähig |
| 4 | **Dreistufige Notbremse + Positionsanzahl** (PR #73) | 4.4 (Ebenen-Tabelle), 8 (Rückgabewert 0 ohne offene Aufgabe, 1 mit — mit Begründung) |

## Teil B — zusätzlich gefunden

**Korrigiert (eindeutig):**

- **B1** Zwei Verweise auf „Abschnitt 4.2" zeigten ins Leere — es gab keine
  Überschriften 4.1/4.2. Ergänzt, ohne Text zu verschieben.
- **B2** `quarterly_review.py` und `agent_optimise.py` gibt es nur bei **3 von
  9** Bots, nicht bei allen neun. Folge: die offene Cronjob-Frage betrifft drei
  mögliche Einträge, nicht neun — der Satz „mit sechs weiteren Bots grösser
  geworden" war falsch herum.
- **B3** Abschnitt 9 hatte **zweimal die Nummer 7**. Zusammengeführt, Liste
  läuft jetzt 1–12.
- **B4** PR #61 ist nicht „offen", sondern **am 2026-09-10 ohne Merge
  geschlossen**. Telegram bleibt dauerhaft rein lesend.
- **B5** Freigeschaltet sind **alle neun Bots**, nicht nur `t3_supertrend`.
- **B6** `shared/fetch_binance_data.py` und `config/email_config.py` standen
  ohne Hinweis im Baum, dass sie gitignored sind und nur lokal existieren.
- **B7** Kleinere Baum-Lücken (`sp500_top50/25.txt`,
  `test_empfehlung_format.py`).

**Geprüft und in Ordnung:** `research/` = 17 Ordner ✅ · „13 Versandstellen" ✅
(9 + 3 + 1) · `oos_equity_simulation.py`-Einschränkung ✅ · neun
`live_params.py` vorhanden, Bot-Tabelle unverändert richtig ✅ · das Protokoll
nennt keine Testzahlen, also nichts zu korrigieren ✅

## Benannt, nicht entschieden — braucht dich

- **E1** Die in der Aufgabe genannten Quellen
  `docs/ZUSAMMENFASSUNG_PR68_Binance_Testnet.md` und
  `…_PR70_IBKR_Paper.md` **existieren im Repo nicht**. Ich habe stattdessen
  `broker/README.md` und `broker/README_IBKR.md` benutzt (in der Aufgabe
  ebenfalls als Quelle genannt). Falls es die Zusammenfassungen doch gibt,
  lohnt ein Abgleich — sie könnten Entscheidungsgründe enthalten, die in den
  READMEs fehlen.
- **E2** `broker/README_IBKR.md` nennt „183 Prüfungen"; tatsächlich sind es
  **200** (mit `ib_async`) bzw. **168** (ohne). Nicht korrigiert, weil der
  Auftrag auf `docs/` und `CLAUDE.md` beschränkt war. Einzeiler-PR, wenn
  gewünscht.
- **E3** Die Cron-Angaben der Bot-Tabelle sind aus dem Repo **nicht
  überprüfbar** (Crontab liegt auf dem Mac). Unverändert gelassen statt
  bestätigt. `crontab -l` klärt es.
- **E4** Der Schlaf-Vorfall vom 11.09.2026 ist jetzt beschrieben, die **Folge
  aber nicht aufgearbeitet**: die ausgefallenen Läufe wurden nicht nachgeholt,
  die Paper-Trading-Zahlen dieses Tages beschreiben also eine Strategie, die so
  nicht gelaufen ist. Ob das in den Auswertungen vermerkt werden soll, habe ich
  offengelassen.

## Erhalten geblieben

Abschnittsnummerierung vollständig — Verweise aus älteren Dokumenten auf
„Abschnitt 4.3", „Abschnitt 8" oder „Abschnitt 9, Punkt 7" gehen weiterhin auf,
und Punkt 7 behandelt weiterhin dasselbe Thema, nur jetzt richtig.

## Empfehlung

Drei Punkte brauchen eine Entscheidung: **E1**, **E2**, **E4**. Alles andere
ist aus dem Repo belegt.
