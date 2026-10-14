# Ergebnis TB-158 — Probe des Wächters: EIGEN mit `pgrep -a`, cwd und Elternkette, zwei Probeläufe

**Stand:** 14.10.2026, 07:12 · Mac-Sitzung TB-158 (Opus 5.5) · Auftrag `docs/auftraege/MAC_TB-158_waechter_probe.md`

**Commits:** ⟨S0⟩ `e7b31f8ee07dd03c9c17725c441e3ef872c7a4f7` · ⟨0⟩ `e80cc0582b5d12b9c2763d5563c4f87c10d2b798` · ⟨A⟩ `0002a28828d102e345d055fbd8fb8163d6e6adbf` · ⟨B⟩ `3e18410d7d73d3e450781b8c33d0399cb94bc3a6` · ⟨Abgabe⟩ = der Commit „TB-158 Abgabe: Ergebnis, Backlog, Journal EV“ (er enthält dieses Ergebnis und kann seinen eigenen Hash nicht nennen).

Kein Abbruch. Kein Aufruf abgelehnt, keine Bestätigung verlangt. Kein `osascript`, kein `launchctl`, keine Taste, kein `/login` durch die Sitzung.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `882b487…`, genau 2 Einträge; sha256 Werkzeug `f0a3c21b…c896` | wie Soll |
| ⟨S0⟩ | Commit mit den 2 Pfaden, gepusht | `e7b31f8`, Push rc 0 |
| 0a nach ⟨S0⟩ | `0a_status.txt` `cmp` gleich, sha256 Kopie wie Soll | wie Soll |
| 0b | `starte_sitzung.sh` 723 Z. `8ea9eaaa…`; `BACKLOG.md` 497 Z. `c803f0d6…`; `JOURNAL.md` 10977 Z. `f305e8ee…`; sha256 `WZ6` `86521eba…` | alle wie Soll |
| A | rc 0, `EIGEN: <PID>`, letzte Zeile `Probe: ja` | rc 0, `EIGEN: 67799`, `Probe: ja` |
| B | mindestens zwei Läufe, je rc 0, danach im Repo nur EIGEN | zwei Läufe, je rc 0, je nur EIGEN |
| C1 | 9 × `ja`, Kennung EV, Zeilen +22 (19 + 3), rc 0 | wie Soll (`d_journal_probe1.txt`) |
| C2 | je 6 × `ja`, Zeilen +1, rc 0 (Probe und Lauf) | wie Soll, Anker Z. 483 |
| D Journal | wie C1, rc 0 | wie Soll, md5 `JOURNAL.md` danach `e37e0af3…` |

## EIGEN

Aus `docs/belege/TB-158/a_eigen.txt`:

- (a) `pgrep -x claude`: keine (rc 1, 0 Zeilen)
- (b) `pgrep -a -x claude`: 67799
- `(a) gegen (b)`: nur in (b) 67799 · nur in (a) keine
- (b) mit cwd im Repo: 67799 (cwd `~/trading-bot`)
- (c) Elternkette ab `$$`: 68619 (`/bin/bash`) → 67799 (`claude`) → 67796 (`login`) → 52069 (Terminal) → 1
- (b) mit cwd im Repo, nicht in (c): keine
- Startzeit EIGEN: `Wed Oct 14 06:53:47 2026` (lesbar)
- EIGEN: 67799 · Probe: ja

**Handbuchstelle bestätigt:** Ohne `-a` lässt `pgrep` auf dem Mac den eigenen Prozess und seine Vorfahren aus — die eigene Sitzung 67799 steht nur in (b). Gemessen, nicht nur gelesen.

## Probe

Aus `docs/belege/TB-158/b_probe.txt` (je Lauf), belegt durch `b_probe<i>_log.txt` und `b_nach<i>.txt`:

| Lauf | Fenster | Sekunden bis eingabebereit (Wecken bis fertig) | Anmeldung | Ablaufwarnung | Zeilen `   \| …` | davon ersetzt | Adresse | rc |
|---|---|---|---|---|---|---|---|---|
| 1 | 24412 | 15 (26) | Abo | nein | 8 | 1 | ja | 0 |
| 2 | 24414 | 6 (15) | Abo | nein | 8 | 1 | ja | 0 |

Je Lauf im Log: `Fenster <n> neu geoeffnet`, `⭐ EINGABEBEREIT (PROBE)`, `Anmeldung: Abo`, `Ablaufwarnung: nein`, die Kopfzeile „Letzte Zeilen …“, 8 Zeilen `   | …` mit genau einer `<<entfernt: Kontozeile>>` und keiner mit `@`, die Adresse `https://claude.ai/code/session_…`, `Probe: beende PID <p> (ttys017) mit TERM. PID 67799 bleibt unberuehrt.`, `Fenster <n> geschlossen`, `----- fertig (probe), rc 0 -----`. Danach im Repo je genau eine `claude`-PID, 67799 = EIGEN. Abstand der Läufe: 35 s Wartebefehl dazwischen. Der Auslöser `probe_67799` war nach jedem Lauf vom Wächter weggeräumt (kein `mv` nötig). `warte` endete nie mit rc 3; kein `b_start<i>` nötig (keine weitere `claude`-PID im Repo).

**Befunde aus Schritt B:** keine der im Auftrag genannten (keine `Anmeldung: unklar`, keine fehlende Ersetzung, Adresse vorhanden, 0 zerschnittene Zeichen, kein rc 5/6/7, keine `STARTFRAGE`, keine `KEINE EINGABEZEILE`). Nebenbeobachtung, nicht gerichtet: die Log-Zeile „Gemerkt in …“ trägt im Rohlog den Heimordnerpfad; `WZ6 beleg` ersetzt ihn in den Belegen durch `~`.

## Belege

Alle unter `docs/belege/TB-158/`. Befehle im Wortlaut siehe Auftrag, Anhang „Dateien und ihre Befehle“.

| Datei | was | Befehl | Bytes | Zeilen | md5 |
|---|---|---|---|---|---|
| `0a_status.txt` | `git status --porcelain` vor Beginn | `cp "$TMPDIR/tb158_0a.txt" …` | 86 | 2 | `1ba306864a40d58a16e9e2391f2bb32d` |
| `tb158_werkzeug.py` | Werkzeug aus Anhang A | `cp "$TMPDIR/tb158_werkzeug.py" …` | 4265 | 88 | `58b58348b2e5404e7b65ace2c875570a` |
| `0b_ausgang.txt` | Zeilen und md5 der Ausgangsdateien, sha256 `WZ6` | Block aus 0b | 496 | 8 | `e8edd6144875ec37b9cfb6070845a8c2` |
| `a_eigen.txt` | EIGEN-Messung | `PY WZ6 beleg "$TMPDIR/tb158_a_eigen.txt" …` | 810 | 25 | `231cd642ad96b844fd140925a7f76ab7` |
| `b_probe1_log.txt` | Wächter-Log Lauf 1 | `PY WZ6 beleg "$TMPDIR/tb158_b_probe1.txt" …` | 2444 | 19 | `7522cf1f842e58ca7066e2bdd97ddd22` |
| `b_nach1.txt` | `claude`-PIDs und cwd nach Lauf 1 | `PY WZ6 beleg "$TMPDIR/tb158_b_nach1.txt" …` | 113 | 5 | `964a8ca32458adb1753cd41860feb23e` |
| `b_probe2_log.txt` | Wächter-Log Lauf 2 | `PY WZ6 beleg "$TMPDIR/tb158_b_probe2.txt" …` | 2432 | 19 | `a71a66874b494399127b05a8e536c402` |
| `b_nach2.txt` | `claude`-PIDs und cwd nach Lauf 2 | `PY WZ6 beleg "$TMPDIR/tb158_b_nach2.txt" …` | 113 | 5 | `964a8ca32458adb1753cd41860feb23e` |
| `b_probe.txt` | je Lauf eine Zeile `PROBE:` | Schreib-, dann Edit-Werkzeug | 387 | 2 | `74018291b521c1baf347a005ae379a05` |
| `d_block.md` | Journal-Block EV | Schreibwerkzeug | 2249 | 19 | `636d475487ebc1fe72084781f5b22931` |
| `d_journal_probe1.txt` | `WZ journal --probe` | `PY WZ journal … --probe > … ; echo "rc $?" >> …` | 380 | 13 | `4af4ffe8f002b9feff912e9d9e47e4ff` |
| `c_backlog_zeile.md` | Backlog-Zeile | Schreibwerkzeug | 318 | 1 | `4f2d3158cd3b2527409812efdd4be7a1` |
| `c_backlog_probe.txt` | `WZ backlog --probe` | `PY WZ backlog … --probe > … ; echo "rc $?" >> …` | 373 | 10 | `b5245f676e96d63271e11e3a273ef9d4` |
| `c_backlog.txt` | `WZ backlog` (schreibend) | `PY WZ backlog … > … ; echo "rc $?" >> …` | 461 | 10 | `d7f986c227098f6454a5e64e272f1517` |
| `d_journal.txt` | `WZ journal` (schreibend) | `PY WZ journal … > … ; echo "rc $?" >> …` | 468 | 13 | `a56c291fea5a0173534eac7fa6ce61ef` |

`b_nach1.txt` und `b_nach2.txt` sind bytegleich (gleiche md5) — beide Male dieselbe eine PID mit demselben cwd. `d_journal_probe2.txt` gibt es nicht (erste Probe rc 0). `d_porcelain.txt` und `d_numstat.txt` entstehen erst nach ⟨Abgabe⟩.

## Abweichungen vom Auftrag

- **Reihenfolge in Schritt D:** Der Journal-Lauf ohne `--probe` (`d_journal.txt`) lief **vor** dem Schreiben dieses Ergebnisses, nicht danach, damit die Tabelle „Belege“ auch `d_journal.txt` mit Bytes und md5 nennen kann. Befehle und Dateien unverändert; die Journal-Probe mit rc 0 (C1) lag vorher vor.
- Sonst keine. Geprüfte Sollwerte: HEAD `882b487…` und 2 Einträge (0a); sha256 Werkzeug `f0a3c21b…c896` (0a, auch der Kopie); 0b alle vier Werte; A rc 0, `EIGEN: 67799`, `Probe: ja`; B zwei Läufe je rc 0 mit allen Soll-Zeilen, danach nur EIGEN; C1 9 × ja, EV, +22, rc 0; C2 je 6 × ja, +1, rc 0; Journal 9 × ja, EV, +22, rc 0.
- Das Werkzeug `WZ6 beleg`/`warte` druckt zusätzlich selbst eine Zeile `rc 0`; ohne Folgen.

## Nicht getan

- Kein Bau am Wächter, nichts unter `docs/werkzeuge/` geändert oder gelesen ausser `wc`/`md5` in 0b und dem Log.
- Regelwerk-Nachtrag zu Fassung 2 und Fehler ab Nr. 74 — eigener Auftrag.
- Bereinigung der Heimordner-Pfade.
- **Der Zweig des echten Starts** (Wache 4a, `starte_sitzung.sh` Z. 573–622) ist nicht geprobt.

## In einfacher Sprache

Die Sitzung hat zuerst sich selbst gefunden: Mit `pgrep -a` taucht sie auf (PID 67799), ohne `-a` nicht — genau wie das Handbuch sagt, jetzt auch gemessen. Dann hat sie dem Wächter zweimal einen Probe-Auftrag hingelegt. Beide Male hat der Wächter ein neues Fenster geöffnet, Claude Code darin gestartet, erkannt, dass es angemeldet (Abo) und bereit ist, die letzten Zeilen des Fensters ohne Kontodaten ins Protokoll geschrieben, die Probe-Sitzung wieder beendet und das Fenster geschlossen. Danach lief im Repo jedes Mal nur noch diese Sitzung. Am Wächter wurde nichts geändert.
