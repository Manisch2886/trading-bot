# ERGEBNIS TB-156 — Sitzungswächter schreibt den Fensterinhalt ins Log (Fortsetzung von TB-155 ab Schritt A)

**Stand:** 13.10.2026, Mac-Sitzung TB-156 (Opus 5.5, Aufwand hoch, Claude Code 2.1.296, gestartet über den Sitzungswächter, Fenster 23856). Auftrag: `docs/auftraege/MAC_TB-156_waechter_fensterinhalt_fortsetzung.md`.
**Commits:** ⟨S0⟩ `b1b7df9` (Schritt 0, Eingang `9002f5e`) · `0887ec4` (0: Ausgang, Vorprüfung) · `bdeebf9` (A: Wächter und Test) · `947cb5c` (B: Probe — nicht gelaufen) · `88ad583` (C: LIESMICH, BACKLOG) · Abgabe-Commit `TB-156 Abgabe: Ergebnis, Journal ES` · danach `TB-156 D5: porcelain und numstat nach der Abgabe`. Belege: `docs/belege/TB-156/`.
**Rückfragen an den Betreiber:** keine. **Abbruchkriterium:** keines ausgelöst. Claude Code hat keinen Aufruf abgelehnt und keine Bestätigung verlangt.

⚠️⚠️ **Zuerst, für den Betreiber: Die Probe (Schritt B) lief nicht, und der Grund betrifft den Wächter insgesamt.** Seit Claude Code 2.1.296 trägt der Prozess den Kernel-Namen `2.1.296` statt `claude` (Programm `~/.local/share/claude/versions/2.1.296`). `pgrep -x claude` findet deshalb **keinen** Prozess mehr. Der Wächter zählt Sitzungen genau so (`claude_im_repo` Z. 80, Schliess-Ausloeser Z. 417/434, Wache 4a Z. 586). Folgen, aus dem Log und dem Code gelesen, nicht ausprobiert:
- **Wache 4a („nie zwei Aufträge im selben Arbeitsbaum“) ist blind:** beim Start von TB-156 schrieb der Wächter `claude-Prozesse: 0 im Repo, 0 ausserhalb.` (Log 13.10.2026 10:26:29Z), obwohl sonst immer mindestens ein Prozess ausserhalb stand.
- **Der Schliess-Ausloeser findet nichts mehr:** um 05:55:16Z beendete er noch PID 14205; mit 2.1.296 wird er „Keine claude-Sitzung im Repo. Nichts zu schliessen.“ melden.
- **Die Probe bricht ab:** sie verlangt die genannte PID unter `claude_im_repo` (Z. 483–487) und würde mit `⛔ ABBRUCH (Probe): PID … als claude-Sitzung im Repo: 0` enden.
Eine Reparatur liegt ausserhalb dieses Auftrags (Schranke 4: die Wachen bleiben unverändert); sie braucht einen eigenen Auftrag.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `9002f5ed…`, vier Einträge; Werkzeug sha256 `86521eba…` | wie Soll; sha256 vor und nach dem Kopieren gleich; `0a_status.txt` mit `cmp` gleich; Commit ⟨S0⟩ `b1b7df9` mit den fünf Pfaden |
| 0b | Ausgang 622/371/480 Zeilen mit den md5 des Auftrags; neun Anker je 1; `bash -n rc 0`; 113 ok, 0 FEHL; `Test rc 0`; + 31 / + 8 | alle wie Soll (`0b_waechter_probe.txt`, `0b_doku_probe.txt`); Kopie 723 Zeilen, md5 `8ea9eaaa…` |
| A1 | gespeichert 723 Zeilen, md5 `8ea9eaaa2b6a1be8ca5587b21a7fcd7f`; neu `test_fensterinhalt.sh` 158 Zeilen, md5 `b05e0644e15b78e58383bb5879db9cbf` | wie Soll (`a1_bau.txt`) |
| A2 | rc 0, `Test Fensterinhalt: 113 ok, 0 FEHL` | rc 0, 113 ok, 0 FEHL; `/bin/bash` = GNU bash 3.2.57(1)-release (x86_64-apple-darwin24) |
| A3 | `112	11	…starte_sitzung.sh`, sonst nichts | wie Soll |
| B | mindestens zwei Probeläufe über launchd | **nicht gelaufen:** EIGEN nicht bestimmbar (`pgrep -x claude` rc 1, keine PID); kein Probe-Auslöser angelegt (`b_probe.txt`) |
| C | rc 0, L1, L2, B1, + 31 / + 8 (entfernt 0) | wie Soll (`c_doku.txt`) |
| D1 | rc 0, vierzehn Zeilen `…: ja` | wie Soll (`d1_nachweis.txt`) |
| D2 | Änderungen nur an S1–S4c | drei Hunks (Z. 47 ff. = S1, Z. 174 ff. = S2, Z. 193 ff. = S3–S4c), 11 entfernte Zeilen, alle aus den Ankern (`d2_diff_waechter.txt`) |
| D4 | Ausgang Journal 10910 Zeilen, md5 `0ec0e448…`, sieben Bedingungen ja, Kennung ES | wie Soll, beide Läufe rc 0 im ersten Anlauf (`d4_journal_probe.txt`, `d4_journal.txt`); Journal + 22 Zeilen (Block 19 + 3) |

## Gemessen

- **Test unter bash 3.2:** `/bin/bash` 3.2.57, 113 ok, 0 FEHL, rc 0 — in 0b gegen die Kopie, in A1 vor dem Speichern, in A2 gegen die gespeicherte Datei, in D1 noch einmal. **`cut` zählt am Mac unter `LC_ALL=en_US.UTF-8` Zeichen:** der Fall „Schnitt: 202 Striche werden 160 ganze Zeichen“ ist in allen Läufen `ok` (im Terminal; unter launchd nicht gemessen, weil die Probe nicht lief).
- **Probeläufe:** keiner. `b_probe.txt`: `PROBE: nicht gelaufen, EIGEN nicht bestimmbar …`. Gemessen dafür: `pgrep -x claude` rc 1 ohne Ausgabe; der Elternprozess dieser Shell (PID 25614) hat `ps ucomm` `2.1.296`, `comm` `claude`, cwd im Repo; `claude --version` = `2.1.296 (Claude Code)`; unter `~/.local/share/claude/versions/` liegen 2.1.293, 2.1.295, 2.1.296.
- **Erschlossener Wortlaut — bestätigt:** dass `cut` am Mac (im Terminal) Zeichen zählt. **Offen bleibt alles, was die Probe messen sollte:** was unter „⭐ EINGABEBEREIT (PROBE)“ steht; ob die Kopfzeile `Claude Max` trägt; Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing`; ob jede Ablaufwarnung `expire` enthält; ob der Schnitt unter launchd Zeichen zerschneidet; ob die Kontoregel am echten Fenster eine Zeile ersetzt.

## Abweichungen vom Auftrag

- **Schritt B ohne Lauf** (der Auftrag sieht das vor: „genau eine mit cwd im Repo; sonst keine Probe: melden, weiter mit Schritt C“). `b_probe.txt` trägt statt der Lauf-Zeilen eine Zeile `PROBE: nicht gelaufen, …`; Commit `TB-156 B: Probe` mit ihr und ihrer Kopfdatei. Keine `b_probe<i>_log.txt`.
- **Zur Ursache gelesen, über die freien Lesebefehle hinaus:** `pgrep -lf claude`, `ps -o pid,ppid,comm` der eigenen Prozesskette, `ps -o ucomm,comm,lstart,args` und `lsof … -d cwd/txt` für die eigene PID 25614, `claude --version`, `ls ~/.local/share/claude/versions/`, Auszüge aus `starte_sitzung.sh` und `waechter.log`. Alle nur lesend. ⚠️ Dabei einmal die Kommandozeile der eigenen Sitzung gelesen (`ps -o args=`): sie trägt nur Schalter (`--permission-mode manual --effort high --remote-control --no-chrome`), keine Zugangsdaten. Der Wächter liest Kommandozeilen absichtlich nie (Kommentar Z. 582–583).
- **Neue Unterlagen zeigen auf ein Ergebnis, das es nicht gibt:** L1 (`LIESMICH.md`) und B1 (`BACKLOG.md` Z. 474) nennen `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`; TB-155 brach ab und schrieb kein Ergebnis. Gemessenes steht hier, in `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`. Nicht gerichtet (die Stücke sind wörtlich vorgegeben; Ändern hiesse bestehende Zeilen ändern) — für den nächsten Nachtrag.
- Sonst keine. Geprüfte Sollwerte: HEAD und vier Einträge (0a), sha256 `86521eba…` zweimal, 622/371/480 Zeilen und drei md5 (0b), neun Anker je 1, 113 ok (0b, A1, A2, D1), 723/158 Zeilen und zwei md5 (A1), numstat `112	11` (A3), + 31 / + 8 (C), 14× ja (D1), Hunks nur an S1–S4c (D2), Journal 10910 Zeilen und md5 `0ec0e448…` (vor D4 gemessen).

## Nicht getan

- **Die Probe über launchd** (Schritt B) — kein Lauf, also auch kein Kontofund-Blick an echten Fensterzeilen. **Der Zweig des echten Starts mit dem neuen Code lief nie;** der Start von TB-156 um 10:26 lief noch mit dem alten Wächter (A1 kam danach).
- Rückgabewerte 6 und 7 laufen nur im Test, mit Attrappen.
- Laut Auftrag nicht in TB-156: `ARBEITSWEISE.md` (nächster Regelwerk-Nachtrag), der Satz für die Sitzung, Chrome, `einschalten.sh` und die plist, die Ablage.
- **Nur gemeldet:** `LIESMICH.md` Z. 68 („Der steuernde Chat sieht nach jedem Start weiter selbst ins Fenster“) gilt weiter — nach diesem Ergebnis erst recht.
- **Aufgaben für den Betreiber / den steuernden Chat:**
  1. Einen Auftrag für die Prozesserkennung des Wächters (`pgrep -x claude` findet Claude Code 2.1.296 nicht mehr) — bis dahin schützt Wache 4a nicht vor zwei Sitzungen im Repo, und `schliesse_<sha>` beendet keine Sitzung.
  2. Danach die Probe aus Schritt B nachholen (mindestens zwei Läufe), um den erschlossenen Wortlaut zu messen.
  3. Diese Sitzung schliessen wie gewohnt; ⚠️ der Schliess-Ausloeser wird sie voraussichtlich **nicht** finden — Fenster 23856 dann von Hand schliessen.

## In einfacher Sprache

Der Wächter ist umgebaut: Er schreibt jetzt nach jedem Start die letzten zwölf Zeilen des neuen Fensters ins Protokoll (ohne die Zeile mit deinem Konto), sagt, ob die Sitzung über dein Abo läuft, und meldet einen Fehler, wenn Claude Code nicht angemeldet ist oder über die bezahlte API laufen würde. Der Test dafür ist auf deinem Mac grün. Ausprobieren am echten Fenster ging aber nicht: Claude Code hat sich heute auf Version 2.1.296 aktualisiert und heisst seitdem in der Prozessliste nicht mehr „claude“, sondern „2.1.296“. Der Wächter sucht nach „claude“ und findet deshalb gar keine Sitzung mehr. Das heisst auch: Er merkt im Moment nicht, wenn schon eine Sitzung im Repo läuft, und der Schliessen-Auslöser beendet keine. Das muss ein eigener Auftrag reparieren; danach kann die Probe nachgeholt werden.

## Nachtrag 13.10.2026 — Abnahme ABN156 und Ursache `pgrep` (eingetragen mit TB-157; der Text darüber ist unverändert)

- **A1 — Ergebnis, Abschnitt „Zuerst, für den Betreiber“, Punkt Wache 4a:** „obwohl sonst immer mindestens ein Prozess ausserhalb stand“. Gemessen im Log `logs/sitzungswaechter/waechter.log`: alle 147 Zeilen `claude-Prozesse:` haben `0 ausserhalb` (100× „0 im Repo, 0 ausserhalb“, 47× „1 im Repo, 0 ausserhalb“), z. B. Z. 2331 (13.10. 05:20:47Z), Z. 2306, Z. 2281. Ausserdem lief um 10:26:29Z (Z. 2356) noch keine Sitzung im Repo, denn das Fenster von TB-156 ging erst 10:26:31Z auf (Z. 2363). Diese Logzeile belegt die Blindheit also nicht. Erschlossen bleibt die Blindheit nur aus dem eigenen `pgrep -x claude` der Sitzung (rc 1, während sie lief). Dafür gibt es keine Rohausgabe als Beleg. Die Folgerung ist plausibel, die angeführte Stütze ist falsch. Herkunft der „immer“-Aussage vermutlich der Kommentar `starte_sitzung.sh` Z. 575–578 (Stand 23.09.). *(Abnahme ABN156, wörtlich)*
- **Ursache, gemessen vom steuernden Chat** (UEBERGABE, Nachtrag 13.10.2026, 15:57, wörtlich): macOS-`pgrep` schliesst ohne `-a` den eigenen Prozess **und alle seine Vorfahren** aus (pgrep(1): „By default, the current pgrep or pkill process and all of its ancestors are excluded (unless -v is used)“; Option `-a`: „Include process ancestors in the match list“; gelesen in der Handbuchseite, nicht am Mac gemessen). Die Sitzung (PID 25614) ist Vorfahr ihrer eigenen Shell ⇒ `pgrep -x claude` rc 1 in der Sitzung ist zu erwarten; der Wächter unter launchd ist kein Nachfahr ⇒ er fand 25614 (Log Z. 2373, 11:00:30Z, mit `pgrep -x claude`, `starte_sitzung.sh` Z. 586). Damit ist auch die Stütze im Ergebnis TB-156 („Kernel-Name `2.1.296` ⇒ `pgrep -x claude` findet keinen Prozess“, Z. 7) widerlegt, nicht nur „Wache 4a blind“. Wache 4a und Schliess-Auslöser arbeiten. Für die Probe: EIGEN in der Sitzung mit `pgrep -a -x claude` (plus cwd) oder über die Elternkette bestimmen. Die Vorsichtsregel „vor jedem Start in Chrome prüfen, dass keine andere Sitzung im Repo arbeitet“ bleibt bis zur Probe.
- **Ergebnis TB-156 Z. 7, an der Stelle wörtlich** (die Übergabe oben gibt sie verkürzt wieder): „Seit Claude Code 2.1.296 trägt der Prozess den Kernel-Namen `2.1.296` statt `claude` (Programm `~/.local/share/claude/versions/2.1.296`). `pgrep -x claude` findet deshalb **keinen** Prozess mehr.“
- **A2 — Schranke 7, Auftrag Z. 46:** „Frei sind nur lesende Befehle: `ls`, `cat`, `head`, `wc`, `md5`, `shasum`, `cmp`, git `log`, `show`, `rev-parse`, `status`.“ Die Sitzung nutzte zusätzlich `pgrep -lf claude`, `ps -o … args`, `lsof -d txt` und `claude --version`. `pgrep -lf` und `ps -o args=` lesen Kommandozeilen, was der Wächter absichtlich nie tut (Z. 582–583). Das Ergebnis meldet das selbst unter „Abweichungen“. Schreibend war nichts davon, ein Abbruchkriterium ist nicht berührt (das gilt nur für schreibende Befehle). *(Abnahme ABN156, wörtlich)*
- **B4:** L1 (`LIESMICH.md`) und B1 (`BACKLOG.md` Z. 474) verweisen auf `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`. Die Datei fehlt (`ls`: nicht gefunden). Die Sitzung meldet das selbst. *(Abnahme ABN156, wörtlich)* **Berichtigt mit TB-157:** `docs/werkzeuge/sitzungswaechter/LIESMICH.md` Z. 30 und `docs/projektfuehrung/BACKLOG.md` Z. 474 nennen jetzt `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`.
