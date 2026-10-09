## EK — TB-144: Wächter-Reparatur, Rest von TB-142 — neues Fenster aus dem Tab, Lesen statt Warten (Merkmal `? for shortcuts`), Aufräumen des gemerkten Fensters, Probe `probe_<PID>` über launchd 4× rc 0; Startzeile mit `--no-chrome`; vier alte Fenster nicht geschlossen (09.10.2026)

*Quelle: `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`*

**Quelle:** Mac-Sitzung **TB-144** (Hauptordner, lokal), 09.10.2026, ab 12:55 MESZ, gestartet über den Sitzungswächter (alter Stand), Eingang `6415b89`. Commits `0c67804` (Schritt 0), `d7b4bc4` (C, Wächter), `7b212c4` (D, Probe), `107bf33` (E, Unterlagen) und der Abgabe-Commit. Belege `docs/belege/TB-144/`. Freigabe: Handwerk mit Einzelfreigabe des Betreibers (Karte 09.10.2026, beantwortet vor 12:53, wörtlich im Auftrag). Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst; Claude Code hat keinen Aufruf abgelehnt.

### Was gemessen ist

| | |
|---|---|
| **A** | Prozesszeile `claude --permission-mode manual --effort high --remote-control`; ein lesender `osascript`-Aufruf über eine Skriptdatei lief ohne Rückfrage (in TB-142 im Auto-Modus abgelehnt) |
| **M1** | `do script` ohne `in` liefert `tab 1 of window id <n>`, `<n>` neu in der Fensterliste — die Form im Entwurf trägt |
| **M2** | Die wartende Sitzung steht schon nach 3 s; Merkmal `? for shortcuts` in allen 18 Lesungen; keine Frage, „manual mode on“ sichtbar |
| **M3** | Mit und ohne `--no-chrome` keine Frage ⇒ Schalter angehängt, Wirkung nicht zuzuordnen |
| **M4** | Nach `TERM` schliesst Terminal das Fenster ohne Rückfrage ⇒ `FENSTER_SCHLIESSEN=ja`. Befund: `busy` ist auch bei laufendem `exec claude` `false` — Schutz liegt allein bei `claude_im_repo` |
| **M5** | „Teach auto mode“ 0-mal (Teilmessung, nur Start ohne Auftrag) |
| **C** | W2–W6 per Werkzeug, 357 → 622 Zeilen, `bash -n` rc 0, numstat 294/29, zweiter Lauf abgewiesen |
| **D0** | Keines der vier alten Fenster geschlossen: 21040 trägt eine bash ohne `exec claude` im Verlauf; 21346/21349/21560 sind ohne Prozess, Terminal nennt für sie aber das tty dieser Sitzung (`ttys008`) — die Prüfung „kein `claude` auf dem tty“ schlug an |
| **D** | Vier Probeläufe über `probe_52208` und launchd (Fenster 21632–21635), je eingabebereit nach 6 s, Probesitzung beendet, Fenster zu, rc 0; keine neue Berechtigung. Zwei Läufe mit zu kurzem Abstand (launchd drosselte, lief trotzdem) |
| **E/F1** | LIESMICH +65, ARBEITSWEISE +8 (mit E6), BACKLOG +13; `nachweis` rc 0 |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| | Wer Läufe über launchd mit Mindestabstand auslöst, baut die Wartezeit in den Aufruf selbst ein — nach Augenmass waren zwei von vier Abständen zu kurz |
| | Der Name des tty, den Terminal für ein Fenster nennt, beweist nicht, dass die Prozesse auf diesem tty zu diesem Fenster gehören: ein Fenster ohne Prozess behält seinen alten Namen. Für alte Fenster `processes of tab` lesen |

### Was offen bleibt

- Erster echter Start mit W5/W6 (die Probe nimmt W4) — steuernder Chat sieht ins Log und ins Fenster; W3 (`schliesse_<HEAD>`) ebenso noch nie gelaufen.
- Vier alte Fenster (21040, 21346, 21349, 21560) schliesst der Betreiber von Hand.
- Anmeldung in Claude Code läuft laut Fenster in einem Tag ab — Betreiber, `/login`.
- Befunde `busy` (M4) und tty-Namen (D0) — zur Entscheidung beim steuernden Chat.
- Ablage; Stellen ausserhalb des Auftrags (`SITZUNGSWAECHTER_ausloeser_statt_tippen.md`, `_ausloeser/LIESMICH.md` und `.gitignore` ohne `schliesse_`/`probe_`).
- Nächste Journalkennung nach EK: **EL**.

*Geschrieben 09.10.2026 von der Mac-Sitzung TB-144. Quellenvermerk: siehe Kopf.*
