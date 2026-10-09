# ERGEBNIS TB-144 — Wächter-Reparatur, Rest von TB-142

**Stand:** 09.10.2026, Mac-Sitzung TB-144 (Opus 5.5, Aufwand hoch, Prozesszeile `claude --permission-mode manual --effort high --remote-control`, PID 52208, Fenster 21627). Auftrag: `docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md`.
**Commits:** ⟨S0⟩ `0c67804` (Schritt 0, Eingang `6415b89`) · ⟨C⟩ `d7b4bc4` (Wächter) · `7b212c4` (D: Probe) · `107bf33` (E: Unterlagen) · Abgabe-Commit `TB-144 Abgabe: Ergebnis, Journal EK` · danach `TB-144 F5: porcelain und numstat nach der Abgabe`. Belege: `docs/belege/TB-144/`.
**Rückfragen an den Betreiber:** keine. **Abbruchkriterium:** keines ausgelöst. Claude Code hat keinen Aufruf abgelehnt und keine Bestätigung verlangt.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `6415b899…`, drei Einträge; Werkzeug sha256 `11367fd8…` | wie Soll; `0a_status.txt` mit `cmp` gleich; sha256 vor und nach dem Kopieren gleich |
| 0b | fünf Zieldateien mit Zeilen/md5 wie im Auftrag, `do script` 1, `--permission-mode` 1, Journal bis EJ | alle wie Soll (`0b_ausgang.txt`) |
| A1 | Prozesszeile trägt `--permission-mode manual` | `claude --permission-mode manual --effort high --remote-control` |
| A2 | Aussage zum Modus | Der Sitzung ist ihr Modus nicht unmittelbar bekannt; nach der Prozesszeile „manual“ |
| A3 | ein lesender `osascript`-Aufruf über Skriptdatei | **LÄUFT**, rc 0, keine Rückfrage |
| M0 | `TERM_PROGRAM=Apple_Terminal`, EIGEN mit cwd im Repo | wie Soll; EIGEN 52208, einzige `claude`-PID |
| M1 | Tab-Form messen | `tab 1 of window id <n>`, `<n>` vorher nicht, nachher in der Liste |
| M2 | ein Merkmal der Eingabezeile | `? for shortcuts` (in allen 18 Lesungen, ab 3 s) |
| M3 | Wirkung `--no-chrome` | keine Frage mit und ohne ⇒ Schalter angehängt, Wirkung nicht zuzuordnen |
| M4 | schliesst Terminal ohne Rückfrage? | ja (`exists` false) ⇒ `FENSTER_SCHLIESSEN=ja` |
| M5 | „Teach auto mode“ zählen | 0 in allen 18 Lesungen und 4 Probe-Logs |
| C1 | fünf AppleScript-Stücke rc 0 | je rc 0 |
| C2 | W2 +210, W3 +2, W4 +64, W5 16→2, W6 16→19, 622 Z., bash -n rc 0; zweiter Lauf rc 2 | wie Soll; zweiter Lauf `ABGEWIESEN`, rc 2; numstat `294 29` |
| D0 | vier alte Fenster schliessen, wenn alle Bedingungen gelten | **keines geschlossen** — bei allen vier ist eine Bedingung verletzt (unten) |
| D | mindestens zwei Probeläufe, je rc 0 | vier Läufe, je rc 0 (Fenster 21632–21635) |
| E | ARBEITSWEISE +8 (mit E6), LIESMICH +65, BACKLOG +13; zweiter Lauf rc 2 | wie Soll |
| F1 | `nachweis` rc 0, `--permission-mode manual` 1 | rc 0, „wie Soll“; W2 206/209 wörtlich (die drei gesetzten Konstanten), W3–W6 vollständig; von Hand 1 |
| F2 | nur Stellen der Stücke geändert, Z. 44–132 und 142–323 von ⟨S0⟩ unverändert | entfernt nur ⟨S0⟩-Z. 324–357 (29 Zeilen), sonst nur Einfügungen |
| F4 | Kennung EK, sechs Bedingungen ja, J1 8 Zeilen | siehe `f4_journal.txt` |

## Gemessen (M1–M5)

**Werte im Skript** (`starte_sitzung.sh`): `STARTZEILE="cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control --no-chrome"`, `MERKMAL_EINGABEZEILE="? for shortcuts"`, `FENSTER_SCHLIESSEN="ja"`; unverändert aus dem Entwurf: `MERKMAL_FRAGE="Enter to confirm"`, `LESE_EIGENSCHAFT="contents"`, `STUFEN="3 3 4 5 5 10 10 10 10"`.

- **M0 Umgebung** (`b_m0.txt`): macOS 15.7.9, `/bin/bash` 3.2.57, Claude Code 2.1.295, `TERM_PROGRAM=Apple_Terminal`. `claude --help` nennt `--no-chrome` (Z. 141). `Terminal.sdef` kennt `close`, `exists`, `do script`, `contents`, `history`, `busy`, `processes`, `tty` — die Wörter aus Anhang A stimmen.
- **M1 Fenster zu einem Tab** (`b_m1.txt`): `osascript … set neu to do script "<Startzeile vom HEAD>" … return neu` lieferte `tab 1 of window id 21630`; 21630 stand vorher nicht in `id of every window` und nachher schon. Testfenster 2: `tab 1 of window id 21631`, ebenso. tty des Tabs `/dev/ttys017`; `ps -o tty=` meldet `ttys017 ` mit einem Leerzeichen am Ende (W4 entfernt Leerzeichen mit `tr -d ' '`, der Vergleich trägt). ⇒ Die Form in `fenster_oeffnen` passt ohne Änderung.
- **M2 Eingabezeile** (`b_m2_<s>.txt`, s = 3 … 60): Schon die erste Lesung nach 3 s zeigte die wartende Sitzung (Kopf, Eingabezeile `❯ Try "…"`, Fusszeile `⏸ manual mode on · ? for shortcuts · ← for agents`). Keine Lesung zeigte die Shell, eine Ladeanzeige oder eine Frage; `Enter to confirm` kam in keiner Lesung vor. Zeilen mit LF getrennt, kein CR. „manual mode on“ stand in jeder Lesung (Beobachtung). Gewählt: `? for shortcuts` — nur ASCII, ohne `|`, `"`, `$`, `\`, Backtick. ⚠️ „In keiner Lesung davor“ ist nicht prüfbar gewesen: es gab keine Lesung vor der wartenden Sitzung. Ob die Fusszeile auch unter einer Startfrage steht, ist nicht gemessen; der Wächter prüft `MERKMAL_FRAGE` zuerst, eine Frage mit „Enter to confirm“ geht also vor.
- **M3 `--no-chrome`** (`b_m3.txt`, `b_m3_<s>.txt`): Testfenster 2 (21631) mit ` --no-chrome` zeigte ebenfalls 60 s lang die wartende Sitzung ohne Frage. Tabelle in Schritt B, Zeile 2 („keine Frage | keine Frage“) ⇒ `--no-chrome` angehängt; **die Wirkung des Schalters ist nicht zuzuordnen** (die Chrome-Frage vom 08.10.2026 trat in beiden Fenstern nicht auf). Lesart des Helfers, vorläufig.
- **M4 Schliessen** (`b_m4.txt`): Auf `ttys017` liefen `login` und `claude` (PID 52522 ≠ EIGEN); Prozesszeile mit `--permission-mode manual`. `kill -TERM 52522`; nach 5 s `busy` = `false`, Prozess weg, `processes` leer. `close window id 21630` ⇒ nach 1 s `exists` = `false`, **keine Rückfrage** ⇒ `FENSTER_SCHLIESSEN=ja`. Testfenster 2 genauso (PID 52923, Fenster 21631 zu).
  ⚠️ **Befund:** `busy` meldete auch **vor** dem `TERM` `false`, während `claude` im Tab lief (`processes`: `login, claude`). Mit `exec claude` gibt es keine Shell mehr, und Terminal zählt den einen Prozess nicht als „busy“. Die Prüfung `busy` in `fenster_zu` schützt damit **nicht** vor dem Schliessen eines Fensters mit laufender Sitzung; der Schutz liegt allein bei `claude_im_repo` in `fenster_aufraeumen` (kein `claude` mit cwd im Repo, ausser der Probe-PID). Nicht geändert (der Auftrag sieht dafür keine Änderung vor); die LIESMICH-Zeile „darin kein Prozess mehr läuft“ beschreibt die Absicht, nicht die Wirkung von `busy`. Zur Entscheidung beim steuernden Chat.
- **M5 „Teach auto mode“** (`b_m5.txt`): 0 in allen 18 Lesungen aus M2/M3 und in allen vier Probe-Logs (dort stehen Fensterzeilen ohnehin nur bei ⛔). Teilmessung: sagt nichts über die Zeit nach dem ersten Auftrag.
- **Probe über Auslöser und launchd** (`d_probe<i>_fenster.txt`, `d_probe<i>_log.txt`): Auslöser `probe_52208`, Wächter von launchd geweckt.

| Lauf | Auslöser (UTC) | geweckt | Fenster | EINGABEBEREIT | Probesitzung | Fenster | rc | Abstand zum Ende des Vorlaufs |
|---|---|---|---|---|---|---|---|---|
| 1 | 11:04:13 | 11:04:13 | 21632 neu | nach 6 s, Lesung 2 | PID 53770 TERM | geschlossen 11:04:27 | 0 | — |
| 2 | 11:04:41 | 11:04:43 | 21633 neu | nach 6 s, Lesung 2 | PID 53949 TERM | geschlossen 11:04:57 | 0 | 14 s ⚠️ |
| 3 | 11:05:08 | 11:05:14 | 21634 neu | nach 6 s, Lesung 2 | PID 54178 TERM | geschlossen 11:05:28 | 0 | 11 s ⚠️ |
| 4 | 11:06:16 | 11:06:17 | 21635 neu | nach 6 s, Lesung 2 | PID 54414 TERM | geschlossen 11:06:31 | 0 | 48 s |

Je Lauf: Fensternummer vorher nicht in der Liste, je Lauf eine andere; `Probe: beende PID … PID 52208 bleibt unberuehrt`; danach im Repo nur 52208; Fensterliste vorher = nachher; der Auslöser lag danach in `_erledigt/`. Prozesszeile der Probesitzung in Lauf 2–4 gelesen: `claude --permission-mode manual --effort high --remote-control --no-chrome`; in Lauf 1 nicht gelesen (Sitzung nach 7 s beendet, Nachsehen alle 10 s). `launchd_fehler.log` unverändert seit 23.09.2026, `launchd_aus.log` seit 09.10.2026, 07:08 — **keine neue Berechtigung** unter launchd nötig.

## D0 — alte Fenster (`d0_fenster.txt`)

Terminal (PID 52069) läuft seit 15.09.2026, 09:14 (Ortszeit), also seit vor dem 09.10.2026, 11:04 MESZ — die Nummern sind nicht neu vergeben. **Keines der vier Fenster wurde geschlossen:**

| Fenster | Tabs | tty laut Terminal | busy | `processes` | Verlauf `exec claude` | `claude` auf dem tty | Ergebnis |
|---|---|---|---|---|---|---|---|
| 21040 | 1 | `/dev/ttys004` | false | `login, -bash` | 0 | nein | offen: kein Sitzungsfenster (Verlauf ohne `exec claude`, darin läuft eine bash) |
| 21346 | 1 | `/dev/ttys008` | false | leer | 1 | **ja** (PID 52208, diese Sitzung) | offen: Bedingung „kein `claude` auf dem tty“ verletzt |
| 21349 | 1 | `/dev/ttys008` | false | leer | 1 | **ja** (52208) | ebenso |
| 21560 | 1 | `/dev/ttys008` | false | leer | 1 | **ja** (52208) | ebenso |

⚠️ **Befund:** Terminal nennt für die drei alten Fenster ohne Prozess das tty `/dev/ttys008`, das jetzt dem Fenster 21627 dieser Sitzung gehört (`tty of every tab of every window`: `ttys004, ttys008, ttys008, ttys008, ttys008`). Ein Fenster, dessen Prozess beendet ist, behält in Terminal offenbar den Namen seines alten tty, und macOS vergibt den Namen neu (erschlossen). `ps -t <tty>` sieht dann die Prozesse eines **anderen** Fensters. Für W4 ist das unschädlich (dort wird das tty des eben geöffneten Tabs gelesen, der lebt); für eine Aufräumregel über alte Fenster wäre `processes of tab` der zuverlässigere Prüfwert.

## Abweichungen vom Auftrag

1. **Probeabstand:** Läufe 2 und 3 wurden 14 s bzw. 11 s nach dem Ende des Vorlaufs ausgelöst, nicht nach mindestens 35 s; launchd weckte den Wächter jeweils erst 30 s nach dem vorigen Wecken (`ThrottleInterval`). Beide liefen trotzdem wie Soll. Lauf 4 hielt den Abstand ein (48 s); damit gibt es zwei Läufe mit eingehaltenem Abstand (Lauf 1 und Lauf 4). Vier statt zwei Läufe.
2. **Nachsehen alle 2 s statt alle 10 s** in Lauf 2–4 (höchstens 100 × 2 s = 200 s), damit die Prozesszeile der Probesitzung gelesen wird; in Lauf 1 (10 s) wurde sie verpasst.
3. **D0, erster Messlauf:** `pgrep -x Terminal` ohne `-a` fand den Vorfahren nicht, `ps -o lstart= -p` lief ohne PID ins Leere (im Beleg sichtbar). Nachgeholt mit `pgrep -a -x Terminal`. Zusätzlich, nur lesend: `processes of tab 1` je Fenster, `count/tty/busy` des eigenen Fensters 21627, `tty of every tab of every window`, `name of every window` (nur Zeichenzahl).
4. **M1/M2 als ein Skript** (`$TMPDIR/m12.sh`): Öffnen und die neun Lesungen liefen in einem Shell-Aufruf mit `sleep` zwischen den Lesungen; die Sekunden zählen ab dem Ende des Öffnens, die Laufzeit der Lesungen selbst (je unter 1 s) kommt dazu. `tty` und `busy` wurden nach der letzten Lesung gelesen. M4 las zusätzlich `ps -p <pid>` und `processes of tab` nach dem `TERM`.
5. **A3:** Der Aufruf lief ohne Umleitung (damit er dem in TB-142 abgelehnten gleicht); seine Ausgabe ist von Hand in `a_modus.txt` übertragen (so in `a_modus.kopf.txt` gesagt).
6. **Schwärzung (Schranke 3):** In jeder Lesung sind zwei Zeilen durch `<<entfernt: Kontozeile>>` ersetzt — die mit dem Abo-Namen und die mit dem Ablauf der Anmeldung; eine Zeile mit `@` kam nicht vor. Die Zählungen in `b_m5.txt` sind zusätzlich auf den ungeschwärzten Lesungen im Scratch gemacht.
7. **Zusätzliche Belege:** `c2_bau_zweit.txt`, `c2_hand.txt`, `e_doku_zweit.txt` (zweite Läufe, Handzählung); M3 Öffnen und Beenden zusammen in `b_m3.txt`; je Lesung eine eigene Kopfdatei.

Sonst keine. Geprüft und wie Soll: 0a (HEAD, drei Einträge, sha256), 0b (fünf Dateien), A1, M0, C1 (5× rc 0), C2 (Stückbilanzen, 622 Z., Prüfzahlen, zweiter Lauf rc 2, numstat 294/29), E (Zeilenbilanzen, zweiter Lauf rc 2), F1, F2.

## Nicht getan

- **Ablage** der geänderten Dateien — steuernder Chat.
- **Vier alte Fenster offen** (21040, 21346, 21349, 21560): Aufgabe für den Betreiber, von Hand schliessen. ⚠️ 21040 trägt eine laufende bash — vorher ansehen, ob es ein eigenes Fenster des Betreibers ist.
- **W5 und W6 liefen in TB-144 nie** — die Probe nimmt W4. Ihr erster Lauf ist der erste echte Start (`starte_TB-<n>`); der steuernde Chat sieht danach ins Log (`⭐ EINGABEBEREIT (TB-<n>)`) und selbst ins Fenster. Ebenso lief W3 (`schliesse_<HEAD>` räumt `letztes_fenster.txt` auf) nie; `letztes_fenster.txt` entsteht erst beim echten Start.
- **Anmeldung läuft ab:** Jede Lesung zeigte „Your login expires in 1 day · run /login to renew“. Läuft sie ab, steht beim nächsten Start vermutlich eine Anmeldefrage statt der Eingabezeile (der Wächter meldet dann ⛔). Aufgabe für den Betreiber: bald `/login` (ARBEITSWEISE 14, Regel 0).
- **Befund `busy`** (M4) und **Befund tty-Namen** (D0): zur Entscheidung beim steuernden Chat, nichts geändert.
- **Eigener Start dieser Sitzung:** Der alte Wächter meldete um 10:54:44Z „Terminal-Fenster 21040 offen“, die Sitzung läuft aber in Fenster 21627 — Fehler Nr. 23 ein letztes Mal, noch mit dem Code am Stand ⟨S0⟩.
- **Nicht in TB-144 (V9):** der übrige Regelwerk-Nachtrag (UEBERGABE, Umzug 08.10.2026, 19:58, Block 4 Nr. 6); das Abschicken des Satzes durch den Wächter; `einschalten.sh` und plist (die Probe verlangte dort keine Änderung); die Stellen „ausserhalb dieses Auftrags“: `docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md` Z. 79, 89, 98, 205; `docs/auftraege/_ausloeser/LIESMICH.md` und die `.gitignore` dort kennen weder `schliesse_` noch `probe_` (ein liegengebliebener `probe_<PID>` wäre von git nicht ignoriert).

## In einfacher Sprache

Der Wächter, der auf dem Mac die Claude-Code-Sitzungen startet, ist repariert. Er öffnet jetzt ein neues Fenster, merkt sich genau dieses, schaut selbst hinein und schreibt nur dann „eingabebereit“ ins Protokoll, wenn Claude Code wirklich auf eine Eingabe wartet. Den Auftragssatz legt er nicht ins Fenster; den schickst du selbst ab. Vier Probestarts ohne Auftrag liefen sauber: Fenster auf, nach 6 Sekunden bereit, Sitzung beendet, Fenster wieder zu. Die vier alten Fenster habe ich nicht geschlossen, weil die Sicherheitsprüfung bei allen anschlug — bitte selbst schliessen. Und: Deine Anmeldung in Claude Code läuft in einem Tag ab; bitte bald `/login`.
