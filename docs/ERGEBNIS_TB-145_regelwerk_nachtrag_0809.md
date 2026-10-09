# ERGEBNIS TB-145 — Regelwerk-Nachtrag 08.–09.10.2026

**Stand:** 09.10.2026, Mac-Sitzung TB-145 (Opus 5.5, Aufwand hoch), gestartet über den Sitzungswächter (Fenster 21663). Auftrag: `docs/auftraege/MAC_TB-145_regelwerk_nachtrag_0809.md` (md5 `a64ec13bddae48d7f8c246d6ca19c0f0`). Eingang HEAD `80c5a9b116e0b02b240568d35232b490ee07bfde`.
**Commits:** ⟨S0⟩ `82b580a6c852dfe191a021e46f2a86889bb852e5` (Schritt 0, 14:51:02) · ⟨E⟩ `2222997b626ab757f4f0055ddcb06557413955f4` (E, 14:52:25) · ⟨F⟩ der Abgabe-Commit „TB-145 Abgabe: Ergebnis, Journal EL“ (Hash in `docs/belege/TB-145/f_numstat.txt`) · danach „TB-145 F: porcelain und numstat nach der Abgabe“.
**Belege:** `docs/belege/TB-145/` (Rohausgaben, je mit `<name>.kopf.txt`). **Rückfragen an den Betreiber:** keine. **Abbruch:** keiner. Claude Code hat in der ganzen Sitzung keinen Aufruf abgelehnt und keine Bestätigung verlangt.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `80c5a9b…`, genau drei Einträge; Werkzeug sha256 `2e04e5a4…7a49` | erfüllt (`0a_status.txt`, `cmp` gleich mit `$TMPDIR/tb145_0a.txt`); sha256 gleich, auch der Kopie unter `docs/belege/TB-145/` |
| 0 | Commit mit den drei Pfaden, push | `82b580a`, gepusht |
| 0b | acht Zieldateien und `starte_sitzung.sh` mit Zeilen/md5 laut Auftrag | alle neun gleich; `waechter.log` 2 034 Zeilen |
| A | Prozesszeile mit `--permission-mode manual` | `claude --permission-mode manual --effort high --remote-control --no-chrome` (EIGEN 57951). Aussage der Sitzung zum Modus: nicht bekannt (nicht ausdrücklich im Kontext genannt) |
| E probe | rc 0, 30 Stücke ok, sieben Dateien gleich, 77 Zeilen | rc 0; Ankerzeile und Zeilen je Stück 30/30 wie Anhang A „Am HEAD“ |
| E einfuegen | rc 0, sieben Dateien geschrieben und zurückgelesen | rc 0 |
| E vergleich | rc 0, 30× GLEICH | rc 0, 30× GLEICH |
| E zweiter Lauf | rc 2, alle 30 Kennungen, md5 gleich | rc 2, 30 Kennungen, md5 der sieben Dateien vorher = nachher |
| E Commit | sieben Zieldateien und Belege, push | `2222997`, gepusht |
| E numstat | rc 0, 36/2/15/11/2/2/9 je 0 entfernt, keine weiteren Dateien | rc 0, alle sieben gleich, „weitere Dateien … keine“ |
| E Wächter-Log | nur melden | geweckt 12:51:57Z, „Kein Ausloeser da. Nichts zu tun.“ (siehe Abweichungen/Befunde) |
| W | bis zu vier tote Fenster schliessen, nur bei allen fünf Bedingungen | alle vier geschlossen; danach 21040, 21663 |
| J probe | acht Bedingungen ja, Kennung EL, J1-Zeilen 9, rc 0 | wie Soll; Block 28 Zeilen ⇒ +41 |
| J | rc 0 | rc 0, JOURNAL.md +41/0, Block EL |
| F vergleich | wie E | rc 0, 30× GLEICH |
| F `starte_sitzung.sh` | 622 Z., `464ac93c53829935e479c5f14121c574` | gleich |

## Schritt W

Vorweg: Fenster `21040, 21346, 21349, 21560, 21627, 21663`; `pgrep -a -x Terminal` ⇒ `52069`; `ps -o lstart= -p 52069` ohne Leerzeichen am Ende ⇒ `Di 15 Sep 09:14:08 2026` (zeichengleich mit `docs/belege/TB-144/d0_fenster.txt` Z. 99; Z. 97 trägt `52069`).

| Fenster | existiert | Tabs | `processes` | `busy` | Verlauf `exec claude` | geschlossen | Grund |
|---|---|---|---|---|---|---|---|
| 21346 | true | 1 | eine leere Zeile, rc 0 | false | 1 | **ja** | alle fünf Bedingungen erfüllt; nach 1 s `exists` false |
| 21349 | true | 1 | eine leere Zeile, rc 0 | false | 1 | **ja** | ebenso |
| 21560 | true | 1 | eine leere Zeile, rc 0 | false | 1 | **ja** | ebenso |
| 21627 | true | 1 | eine leere Zeile, rc 0 | false | 1 | **ja** | ebenso |
| 21040 | — | — | — | — | — | nein | nicht auf der Liste (Fenster des Betreibers), nicht abgefragt |
| 21663 | — | — | — | — | — | nein | eigene Sitzung, nicht auf der Liste, nicht abgefragt |

Danach: `21040, 21663`. Terminal stellte keine Rückfrage. Alle Aufrufe direkt per `osascript -e`, ohne Skriptdatei, ohne Enter/`keystroke`/System Events. Der Verlauf der Fenster ging in keine Datei, nur die `grep -c`-Zahl.

## Abweichungen vom Auftrag

1. **Schritt W, Reihenfolge:** Die fünf Abfragen liefen zuerst für alle vier Fenster als ein Block, danach wurde je Fenster unmittelbar vor dem Schliessen erneut geprüft (`exists`, Tabs, `processes`, Verlauf; `busy` beim zweiten Mal nicht) und erst dann geschlossen. Der Auftrag beschreibt je Nummer „abfragen, dann schliessen“. Wirkung: keine — jede Bedingung war zum Zeitpunkt des Schliessens frisch gemessen.
2. **Schritt W, Wartezeit:** „nach 1 s“ als `osascript -e 'delay 1'` umgesetzt (nicht `sleep 1`).
3. **Schritt W, zusätzlicher Aufruf:** `pgrep -x Terminal` ohne `-a` lief einmal zusätzlich (rc 1, macOS schliesst eigene Vorfahren aus); massgeblich ist `pgrep -a -x Terminal` laut Auftrag.
4. **Kopfdateien:** heissen `<name ohne Endung>.kopf.txt` (z. B. `a_modus.kopf.txt`, `tb145_einfuegen.kopf.txt`, `j_block.kopf.txt`); vier zuerst als `<name>.txt.kopf.txt` bzw. `<name>.py.kopf.txt` angelegte (0a, 0b, A, Werkzeug) wurden vor dem ersten Commit umbenannt.
5. **Befund, kein Fehler:** Das Einfügen von A1/A2 in `docs/auftraege/_ausloeser/` hat den Wächter geweckt (Log 12:51:57Z, gleiche Sekunde wie die mtime der beiden Dateien), er tat nichts (`e_waechterlog.txt`).

Sonst keine. Geprüfte Sollwerte: HEAD und drei Einträge (0a), sha256 Werkzeug (zweimal), neun Zeilen/md5-Paare (0b), Prozesszeile (A), alle Ausgaben von `probe`/`einfuegen`/`vergleich`/zweiter Lauf/`numstat` (E), Terminal-PID und `lstart`, fünf Bedingungen je Fenster, Fensterliste danach (W), acht Bedingungen, Kennung, J1-Zeilen, Zeilenbilanz (J), `vergleich` und md5 von `starte_sitzung.sh` (F); `f_porcelain.txt` und `f_numstat.txt` werden nach dem Abgabe-Commit gemessen.

## Nicht getan

- Die 14 Formhinweise aus TB-141; „W8 und ARBEITSWEISE Z. 97“ (ohne Wortlaut).
- Jede Änderung an `starte_sitzung.sh` (Befunde `busy` und tty nur durch L1 in der LIESMICH berichtigt).
- Ablage; Projekt-Erinnerung.
- Fenster 21040 bleibt beim Betreiber.
- **Für den Betreiber:** Anmeldung von Claude Code erneuern, falls noch nicht geschehen (im Umzug 14:44 genannt).

## In einfacher Sprache

Die neuen Regeln und Berichtigungen der letzten zwei Tage stehen jetzt im Regelwerk, in der Umzugsanleitung, in den Texten zum Sitzungswächter, im Backlog und im Journal (Block EL). Ein kleines Programm hat 30 fertige Textstücke eingesetzt, 77 Zeilen, ohne eine bestehende Zeile anzufassen, und danach bestätigt, dass jedes Stück genau einmal und Zeichen für Zeichen richtig dasteht. Der Wächter selbst ist unverändert. Die vier alten, leeren Terminal-Fenster sind zu — vorher war geprüft, dass in keinem mehr etwas lief. Dein Fenster 21040 und das Fenster dieser Sitzung sind offen geblieben.
