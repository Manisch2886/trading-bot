# db-Sicherung — die Datenbanken täglich nach iCloud

**Gebaut:** 26.09.2026, TB-112 (Fable 25f O6; Ziel „iCloud Drive“ per Auswahlkarte, 26.09.2026, ca. 06:40)
**Warum:** Die neun `paper_trading_*.db` und die übrigen Datenbanken des Projekts
existieren **nur auf diesem MacBook**. Sie sind die einzige Evidenz aus dem
Paper-Betrieb (Prüfprinzip D6). Geht der Rechner verloren, ist sie weg.

---

## Was das Skript tut

`db_sicherung.sh` hat eine Aufgabe: jede `*.db` im Repo-Wurzelordner und unter
`strategies/*/` **lesend** kopieren (gemessen am 26.09.2026: zwölf Dateien, elf im
Wurzelordner und eine leere unter `strategies/volatility_breakout/`).

| Schritt | wie |
|---|---|
| kopieren | `sqlite3 -readonly <db> ".backup '<kopie>'"`, die Backup-API von SQLite. Sicher, auch wenn gerade ein Cron schreibt. ⛔ **Kein `cp`.** |
| Schlüssel-Prüfung | nur das **Schema** der Kopie: Spaltennamen gegen `key`, `secret`, `token`, `api`, `passw`. ⛔ **Nie ein Wert.** Bei einem Treffer wird die Datei **nicht** gesichert (Rückgabe 1), bis du entscheidest. |
| prüfen | `PRAGMA integrity_check` an der Kopie im Ziel (erwartet `ok`) |
| Quersumme | `sha256` jeder Kopie in `SHA256SUMS` im Zielordner |
| Protokoll | auf dem Bildschirm bzw. im Cron-Log, dazu `PROTOKOLL.txt` im Zielordner |

**Ziel:** `~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung/<JJJJ-MM-TT>/`
(das ist „iCloud Drive → trading-bot-db-sicherung“ im Finder). Läuft das Skript am
selben Tag ein zweites Mal, entsteht `<JJJJ-MM-TT>_<HHMMSS>/`; eine vorhandene
Sicherung wird **nie überschrieben**.

⛔ **Das Skript löscht nichts.** Alte Sätze bleiben liegen. Ein Satz ist heute
etwa **370 KiB** groß (gemessen 26.09.2026), ein Jahr täglicher Sätze also etwa
130 MiB. Wie lange aufbewahrt wird, ist **deine Entscheidung** (offene Frage).

**Rückgabewert:** 0 nur, wenn jede gefundene Datenbank gesichert ist und jede
Kopie `ok` meldet. Sonst 1, und die Meldung nennt die Datei.

---

## ⭐ Einschalten — eine Cron-Zeile, die du selbst einträgst

Vorschlag: täglich **05:20** Uhr (die Wächter-Crons liegen um 3:50, 4:10, 4:40
und 4:50, die Brücke alle 4 h zur Minute 5).

```
20 5 * * * cd ~/trading-bot && /bin/bash docs/werkzeuge/db_sicherung/db_sicherung.sh >> logs/system/db_sicherung.log 2>&1
```

Eintragen mit `crontab -e`, Zeile ans Ende, speichern.

⚠️⚠️ **Festplattenvollzugriff.** Ein Cron-Job darf auf dem Mac nicht ohne
Weiteres in den iCloud-Ordner schreiben. Steht im Log

```
FEHLER: Zielordner nicht anlegbar: mkdir: ...: Operation not permitted
```

dann braucht **cron** den Festplattenvollzugriff:
*Systemeinstellungen → Datenschutz & Sicherheit → Festplattenvollzugriff → „+“*,
dann mit ⌘⇧G den Pfad `/usr/sbin/cron` eingeben und hinzufügen. Aus dem
Terminal heraus lief das Skript am 26.09.2026 ohne diesen Schritt (die
Claude-Code-Sitzung hatte die Rechte schon); ob **cron** sie hat, zeigt erst
der erste Cron-Lauf. Danach im Log nachsehen:

```
tail -30 ~/trading-bot/logs/system/db_sicherung.log
```

**Von Hand:** `bash docs/werkzeuge/db_sicherung/db_sicherung.sh` aus der
Repo-Wurzel. Mit einem Ordner als Argument sichert es dorthin statt nach
iCloud (für Tests): `bash docs/werkzeuge/db_sicherung/db_sicherung.sh /tmp/probe`.

---

## Eine Sicherung zurückspielen (nur beschrieben — nicht automatisch)

1. **Alle Bots anhalten**, die in die Datenbank schreiben: die Cron-Zeilen mit
   `#` auskommentieren (`crontab -e`) und warten, bis kein Lauf mehr aktiv ist.
2. Den Satz prüfen, aus dem zurückgespielt wird:
   `cd "<satzordner>" && shasum -a 256 -c SHA256SUMS` (jede Zeile `OK`) und
   `sqlite3 <datei>.db "PRAGMA integrity_check"` (`ok`).
3. Die kaputte Datenbank im Repo **nicht löschen, sondern umbenennen**, z. B.
   `mv paper_trading_rsi2_crypto.db paper_trading_rsi2_crypto.db.kaputt_<datum>`.
4. Die Kopie mit SQLite zurückschreiben:
   `sqlite3 "<satzordner>/paper_trading_rsi2_crypto.db" ".backup 'paper_trading_rsi2_crypto.db'"`
   (aus der Repo-Wurzel; Dateien unter `strategies/...` liegen im Satz unter
   demselben Unterpfad).
5. `sqlite3 paper_trading_rsi2_crypto.db "PRAGMA integrity_check"` → `ok`.
6. Cron-Zeilen wieder einschalten.

⚠️ Alles zwischen dem Zeitpunkt der Sicherung und dem Zurückspielen ist in der
zurückgespielten Datei **nicht** enthalten. Das gehört als Lücke in
`docs/DATENLUECKEN.md`.

---

## Herkunft

Auftrag `docs/auftraege/MAC_TB-112_19_laufbereich_db_sicherung.md`, Block B.
Belege: `docs/belege/TB-112/b2_schema.txt` (Schema je Kopie, Gegenprobe mit einer
`api_key`-Spalte), `b3_test.txt` (zwei Läufe gegen ein Testziel, Originale
unverändert), `b4_icloud.txt` (erster Lauf ins iCloud-Ziel).
