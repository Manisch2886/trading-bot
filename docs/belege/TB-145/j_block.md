## EL — TB-145: Regelwerk-Nachtrag 08.–09.10.2026 — 30 Stücke in sieben Dateien per Werkzeug (77 Zeilen, 0 entfernt), vier tote Terminal-Fenster geschlossen (21346, 21349, 21560, 21627); `starte_sitzung.sh` unverändert (09.10.2026)

*Quelle: `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md`*

**Quelle:** Mac-Sitzung **TB-145** (Hauptordner, lokal), 09.10.2026, ab 14:44 MESZ, gestartet über den Sitzungswächter (Fenster 21663, Log 12:44:07Z „⭐ EINGABEBEREIT (TB-145)“), Eingang `80c5a9b`. Commits `82b580a` (Schritt 0, 14:51:02), `2222997` (E, 14:52:25) und der Abgabe-Commit. Belege `docs/belege/TB-145/`. Freigabe: Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026); Schritt W für 21346, 21349, 21560 von der Karte vom 09.10.2026 gedeckt, für 21627 Vorgabe des steuernden Chats. Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst; Claude Code hat keinen Aufruf abgelehnt und keine Bestätigung verlangt, auch nicht bei den direkten `osascript`-Aufrufen an Terminal in Schritt W.

### Was gemessen ist

| | |
|---|---|
| **0** | Ausgang genau die drei Einträge am HEAD `80c5a9b`; Werkzeug sha256 `2e04e5a4…7a49` wie Soll; alle acht Zieldateien und `starte_sitzung.sh` mit Zeilen und md5 wie 0b |
| **A** | Prozesszeile `claude --permission-mode manual --effort high --remote-control --no-chrome` (EIGEN 57951) |
| **E** | `probe` rc 0, Ankerzeilen und Zeilen je Stück wie Anhang A „Am HEAD“ (30/30); `einfuegen` rc 0; `vergleich` rc 0 (30× GLEICH); zweiter Lauf rc 2 mit allen 30 Kennungen, md5 unverändert; `numstat` S0..E rc 0: ARBEITSWEISE 36/0, UMZUG 2/0, SITZUNGSWAECHTER_ausloeser_statt_tippen 15/0, BACKLOG 11/0, Wächter-LIESMICH 2/0, `_ausloeser/.gitignore` 2/0, `_ausloeser/LIESMICH.md` 9/0 |
| **E, Wächter** | Das Einfügen in `_ausloeser/.gitignore` und `_ausloeser/LIESMICH.md` hat den Wächter geweckt: Log 12:51:57Z „Waechter geweckt“, „Kein Ausloeser da. Nichts zu tun.“ — gleiche Sekunde wie die mtime der beiden Dateien; folgenlos |
| **W, vorweg** | Fenster 21040, 21346, 21349, 21560, 21627, 21663; Terminal PID 52069, `lstart` „Di 15 Sep 09:14:08 2026“ wie TB-144. `pgrep -x Terminal` ohne `-a` gibt rc 1 (macOS schliesst die eigenen Vorfahren aus) |
| **W, je Fenster** | 21346, 21349, 21560, 21627: je `exists` true, 1 Tab, `processes` genau eine leere Zeile (rc 0), `busy` false, Verlauf mit `exec claude` 1 ⇒ alle vier geschlossen, je `exists` false nach 1 s, keine Rückfrage von Terminal |
| **W, danach** | Fenster 21040, 21663 — die Liste von vorher ohne die vier |

### Was offen bleibt

- Fenster 21040 (bash, vermutlich des Betreibers) bleibt beim Betreiber.
- Die 14 Formhinweise aus TB-141 und „W8 und ARBEITSWEISE Z. 97“ — ohne Wortlaut, nicht in TB-145.
- Befunde `busy` und tty am Wächter: nur in der LIESMICH berichtigt (L1), `starte_sitzung.sh` unverändert.
- Ob ein Schreiben im Auslöserordner den Wächter wecken soll (gemessen: er wird geweckt, tut nichts) — nur gemeldet.
- Ablage; Projekt-Erinnerung.
- Nächste Journalkennung nach EL: **EM**.

*Geschrieben 09.10.2026 von der Mac-Sitzung TB-145. Quellenvermerk: siehe Kopf.*
