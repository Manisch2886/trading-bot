## EM — TB-146 und TB-147: Regelwerk- und Dokunachtrag 09.10.2026 — 14 Stücke in drei Dateien per Werkzeug (35 Zeilen, 0 entfernt); TB-146 brach in Schritt E nach Vorschrift ab (Claude Code lehnte einen Hilfsskript-Aufruf ab), den Rest (numstat-Beleg, dieser Block, Ergebnis) trug TB-147 nach (09.–10.10.2026)

*Quelle: `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`*

**Quelle:** Mac-Sitzung **TB-147** (Hauptordner, lokal), 10.10.2026, Eingang `e39cc44` (HEAD in 0a gemessen); gestartet laut Auftrag über den Sitzungswächter (`starte_TB-147`) — von der Sitzung nicht gemessen. Commits von TB-146: `7f0b59d` (Schritt 0), `e39cc44` (Abbruch in Schritt E); von TB-147: `066b267` (Schritt 0), dazu der Commit, der diesen Block und den numstat-Beleg trägt, der Abgabe-Commit mit dem Ergebnis und ein letzter Commit mit porcelain und numstat nach der Abgabe. Belege beider Aufträge in `docs/belege/TB-146/`. Auftrag TB-146: `docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md`; Auftrag TB-147: `docs/auftraege/MAC_TB-147_rest_tb146_journal_ergebnis.md`. Freigabe: Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026). Keine Rückfrage an den Betreiber in beiden Aufträgen. In TB-147 hat Claude Code bis zum Schreiben dieses Blocks keinen Aufruf abgelehnt und keine Bestätigung verlangt; jeder Shell-Befehl stand wörtlich im Auftrag.

**Was TB-146 tat:** Schritt 0 committete den Stand des steuernden Chats (sechs Einträge, darunter die drei Fable-Dateien vom 09.10.2026) und legte das Werkzeug `tb146_einfuegen.py` aus Anhang B des Auftrags ab. Schritt A fand die eigene Sitzung im Modus `manual`. Schritt E fügte mit dem Werkzeug die 14 Stücke ein: zwölf Tabellenzeilen-Stücke (16 Zeilen) in `ARBEITSWEISE.md` Abschnitt 0, U1 in `UMZUG.md` Abschnitt 6 (+10), B1 in `BACKLOG.md` Abschnitt 5 (+9); `vergleich` fand jedes Stück zeichengleich und genau einmal, der zweite Lauf wurde abgewiesen und änderte nichts.

**Der Abbruch von TB-146:** Nach dem Einfügen, vor dem Commit ⟨E⟩, wollte die Sitzung die vier Kopfdateien zu `e_probe`, `e_einfuegen`, `e_vergleich` und `e_zweitlauf` mit einem kleinen Hilfsskript `kopf.sh` im Scratchpad schreiben (`mkdir`, `cat`-Heredoc, `chmod +x`). Claude Code lehnte diesen Bash-Aufruf ab („… has been denied.“, `abbruch.txt`). Das ist ein Abbruchkriterium des Auftrags; die Sitzung umging die Ablehnung nicht, schrieb `abbruch.txt` und committete die drei geschriebenen Zieldateien und die Belege mit Namen im Abbruch-Commit `e39cc44`. Nicht erreicht wurden die Kopfdateien zu `e_*`, Commit ⟨E⟩, `e_numstat.txt`, der Journalblock und das Ergebnis.

**Der Abschluss mit TB-147:** Ein Folgeauftrag mit wörtlich vorgegebenen Befehlen (je Aufruf ein Codeblock, kein Hilfsskript, nichts ausserhalb des Repos ausser zwei porcelain-Dateien in `$TMPDIR`) holt nach, was fehlte: den numstat-Beleg `e_numstat.txt` über `7f0b59d..e39cc44`, diesen Block samt Nachtrag J1 (vom Werkzeug eingesetzt) und ein gemeinsames Ergebnis für TB-146 und TB-147. Die Kopfdateien zu `e_*` entfallen; an ihre Stelle tritt die Tabelle „Belege“ im Ergebnis. Am Regelwerk ändert TB-147 nichts.

### Was gemessen ist

| | |
|---|---|
| **TB-146, 0** | 0a: genau die sechs Einträge am HEAD `bbe26ba` (`0a_status.txt`); Werkzeug sha256 `09d57b7a…660e` wie Soll; 0b: vier Zieldateien an `7f0b59d` wie Soll (ARBEITSWEISE 2515, UMZUG 382, BACKLOG 386, JOURNAL 10 669 Z.), `UEBERGABE.md` 2866 Z. ohne Sollwert (`0b_ausgang.txt`) |
| **TB-146, A** | Prozesszeile `claude --permission-mode manual --effort high --remote-control --no-chrome` (EIGEN 70880, `a_modus.txt`) |
| **TB-146, E** | `probe` rc 0 (14 Stücke, 35 Zeilen); `einfuegen` rc 0, je Datei +16/+10/+9 wie Soll; `vergleich` rc 0 (14× GLEICH); zweiter Lauf rc 2 mit allen 14 Kennungen, md5 der drei Dateien vorher = nachher |
| **TB-146, Abbruch** | `abbruch.txt`: abgelehnter Bash-Aufruf (Hilfsskript im Scratchpad); Zieldateien beim Abbruch ARBEITSWEISE 2531, UMZUG 392, BACKLOG 395 Z., numstat gegen `7f0b59d` 16/0, 10/0, 9/0 |
| **TB-147, 0** | 0a: genau die drei Einträge (`AKTUELLER_AUFTRAG.md`, `UEBERGABE.md` geändert, Auftrag TB-147 neu) am HEAD `e39cc44`; Beleg `t147_0a_status.txt` per `cmp` gleich (rc 0); 0b: ARBEITSWEISE 2531, UMZUG 392, BACKLOG 395, JOURNAL 10 669 Z. (Summe 13 987), md5 je wie Soll, Werkzeug md5 `483dae10…c9b9` wie Soll |
| **TB-147, A** | Prozesszeile `claude --permission-mode manual --effort high --remote-control --no-chrome` (EIGEN 90475) |
| **TB-147, N** | `numstat 7f0b59d e39cc44` rc 0: 16 Rohzeilen (13 Belege, drei Zieldateien), ARBEITSWEISE 16/0, BACKLOG 9/0, UMZUG 10/0, weitere Dateien keine; `vergleich` rc 0 (14× GLEICH, je genau einmal) |

### Was offen bleibt

- Die Posten (a) bis (g) aus „Nicht in TB-146“ (Formhinweise Nr. 9 bis 11 aus TB-141, Soll-Liste in `ablage_soll.py`, Zeile 09a im Dialog-Index, Fliesstext ARBEITSWEISE 6b und 10 samt git-Liste in UMZUG 6, „drei enge Bau-Helfer“, Fehler Nr. 32, Ablage und Projekt-Erinnerung).
- Die vier Kopfdateien zu `e_*` aus TB-146 entfallen; Ersatz ist die Tabelle „Belege“ im Ergebnis.
- Ob Claude Code im Modus `manual` für einen Befehl ausserhalb von `deny` und `ask` nachfragt: In TB-147 fragte es bis zum Schreiben dieses Blocks bei keinem Befehl nach — das ist ein Befund dieser Sitzung, keine Regel.
- Abnahme von TB-146 und TB-147, `AKTUELLER_AUFTRAG.md` umstellen, Ablage, Projekt-Erinnerung (steuernder Chat).
- Nächste Journalkennung nach EM: **EN**.

*Geschrieben 10.10.2026 von der Mac-Sitzung TB-147. Quellenvermerk: siehe Kopf.*
