# Ergebnis TB-159 — Agent 1, 3 und 4 abgeschaltet über `config/agenten_aus.txt`

**Stand:** 13.10.2026, 22:56 · Mac-Sitzung TB-159 (Claude Code, Opus 5.5) · Auftrag `docs/auftraege/MAC_TB-159_agenten_aus.md`
**Commits:** ⟨S0⟩ `3a2a700c3aceaebe3829d6823b0f882365248a09` · ⟨A⟩ `3a5b7bc8e23566c1946293b16444f9015839eeba` · ⟨F⟩ = der Commit „TB-159 Abgabe: Ergebnis, Journal EU“ (enthält diese Datei)
**Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6) · **Journal:** Block EU · **Backlog:** K4v

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `300ba31`, 4 Einträge; Werkzeug sha256 `d5a403dd…c16d` | wie Soll |
| ⟨S0⟩ | Commit + Push der vier Pfade | `3a2a700`, gepusht |
| 0b | 134/60/84/174/496/10953 Z., md5 wie Auftrag | wie Soll |
| 0c | 18 Zeilen, je Paar gleich | 18 Zeilen, alle 9 Paare gleich |
| 0d | 223 Zeilen | 223 Zeilen |
| A | 3 × rc 0 | 3 × rc 0 |
| B1 probe | alle Anker „Vorkommen 1“ bzw. „neu“, numstat wie Tabelle, rc 0 | wie Soll |
| B2 kopie | rc 0 | 1101 verfolgte Dateien, 27 438 990 B, rc 0 |
| B3 einbau | „6 Dateien geschrieben“, rc 0 | wie Soll |
| B4 vergleich (Kopie) | 9 × GLEICH, rc 0 | wie Soll |
| B5 Tests (Kopie) | 4 × rc 0, „Alle <n> Pruefungen bestanden.“ | 4 × rc 0, „Alle 30 Pruefungen bestanden.“ |
| B6 cp/cmp | ohne Ausgabe | ohne Ausgabe, rc 0 |
| B7 vergleich (Repo) | 9 × GLEICH, rc 0 | wie Soll |
| B8 Tests (Repo) | 4 × rc 0 | 4 × rc 0 |
| 8a | Datenstand gleich; db-md5 gegen 0c | Datenstand bytegleich; 1 von 9 db geändert (Cron, siehe Abweichungen) |
| ⟨A⟩ | Commit + Push, numstat 21 Zeilen | `3a5b7bc`, gepusht, 21 Zeilen, Code-Zahlen wie Soll |
| C backlog --probe / backlog | vier `ja`, „Zeile als Z. 196“, rc 0 | wie Soll; numstat BACKLOG 1/0 |
| C kennung | „Kennung EU …“, rc 0 | wie Soll (höchste vorhandene ET) |
| C journal --probe / journal | sechs `ja`, rc 0 | wie Soll; 21 Zeilen Block, numstat JOURNAL 24/0 |

## Basislauf und Nachlauf

| Testdatei | vorher (A) | Kopie (B5) | nachher (B8) |
|---|---|---|---|
| `shared/test_empfehlung_format.py` | rc 0 · `[OK ]` 70 · 1,0 s | rc 0 · 70 · 0,6 s | rc 0 · 70 · 0,6 s |
| `shared/test_agent2_kapitalmass.py` | rc 0 · 34/34 (`[OK ]` 0) · 0,6 s | rc 0 · 34/34 · 0,6 s | rc 0 · 34/34 · 0,5 s |
| `shared/test_agent2_zielfunktion.py` | rc 0 · `[OK ]` 41 · 5,0 s | rc 0 · 41 · 5,0 s | rc 0 · 41 · 4,9 s |
| `shared/test_agenten_aus.py` (neu) | — | rc 0 · 30 · 0,1 s | rc 0 · 30 · 0,1 s |

Kein Test hat die API aufgerufen (Platzhalter-Modul `anthropic` in jeder Testdatei; `WZ basis` entfernt zusätzlich `ANTHROPIC_API_KEY` aus der Umgebung).

## Belege

Alle unter `docs/belege/TB-159/`.

| Datei | was | Befehl | Bytes | Zeilen | md5 |
|---|---|---|---|---|---|
| `0a_status.txt` | `git status --porcelain` vor ⟨S0⟩ | 0a, `cp` aus `$TMPDIR` | 174 | 4 | `5fb4523eed97a61d55cd4f2b62331ec3` |
| `tb159_werkzeug.py` | Werkzeug aus Anhang B | Holbefehl 0a, `cp` | 9930 | 231 | `049f7ab336d835c19acff38974f19867` |
| `0b_ausgang.txt` | Zeilen und md5 der Zieldateien | 0b | 685 | 13 | `5d8fd8afb8488b8406a2224e37d58627` |
| `0c_db_sicherung.txt` | md5 der neun db und ihrer Sicherung | 0c | 1903 | 18 | `507438ef2b7a76e49a59e6291d34408e` |
| `0d_datenstand_vorher.txt` | md5 `data/*` vorher | 0d | 13055 | 223 | `d14cb609615de4449bb4ba5c4b79c88a` |
| `a_basis_vorher.txt` | Basislauf | `WZ basis vorher` | 734 | 6 | `4108d268524d0dc6b9336bcf5eab45e4` |
| `b_probe.txt` | Probe am Repo | `WZ probe` | 933 | 17 | `01fd3b90880e65e6ce2baacc4a08f973` |
| `b_kopie.txt` | Kopie nach `$TMPDIR` | `WZ kopie` | 145 | 2 | `e6985c0c4ae6c5523c408dcf20a816ab` |
| `b_einbau_kopie.txt` | Einbau in der Kopie | `WZ einbau --in` | 923 | 17 | `0ff3b03aef5791c58ea7e736c349501d` |
| `b_vergleich_kopie.txt` | Vergleich in der Kopie | `WZ vergleich --in` | 396 | 10 | `09883238a4322a0467920b044ae62954` |
| `b_basis_kopie.txt` | Tests in der Kopie | `WZ basis kopie … --in` | 953 | 8 | `94e2fa8cf941d9379f899c911a8d0f1b` |
| `b_vergleich.txt` | Vergleich im Repo | `WZ vergleich` | 396 | 10 | `09883238a4322a0467920b044ae62954` |
| `b_basis_nachher.txt` | Nachlauf im Repo | `WZ basis nachher` | 961 | 8 | `f1913f5ab32dfd4b631208592d4a214a` |
| `b_db_nachher.txt` | md5 der neun db nachher | 8a | 686 | 9 | `fb1f0aee3cc4186ccc1af6bea7c5d4cc` |
| `b_datenstand_nachher.txt` | md5 `data/*` nachher | 8a | 13055 | 223 | `d14cb609615de4449bb4ba5c4b79c88a` |
| `b_numstat.txt` | numstat ⟨S0⟩..⟨A⟩ | `git diff --numstat` | 828 | 21 | `b7ae8022016fcb1b3d1091995c2fb00e` |
| `c_backlog_probe.txt` | Backlog-Probe | `WZ backlog --probe` | 105 | 3 | `d5ebf6db79bf864b9b4ac7de5584e30c` |
| `c_backlog.txt` | Backlog-Eintrag | `WZ backlog` | 110 | 3 | `24064425b989739f891bd3a16e3349ba` |
| `c_kennung.txt` | Journal-Kennung | `WZ kennung` | 57 | 2 | `d6a635fcf71afd683e33d7d13a0c3e69` |
| `c_block.md` | Journalblock EU | Schreibwerkzeug | 2925 | 21 | `fbd13c1a2377eddc3eb62448a875fe8f` |
| `c_journal_probe.txt` | Journal-Probe | `WZ journal --probe` | 251 | 8 | `88496d69421e567e6e8c7260ea0383c8` |
| `c_journal.txt` | Journal-Eintrag | `WZ journal` | 256 | 8 | `197a7ca3991342bee9f5f3c928650f6a` |
| `f_porcelain.txt` | `git status --porcelain` nach ⟨F⟩ | Abgabe | entsteht nach ⟨F⟩ | | |
| `f_numstat.txt` | numstat ⟨S0⟩..⟨F⟩ | Abgabe | entsteht nach ⟨F⟩ | | |

## Abweichungen

1. **8a — `paper_trading_volatility_breakout.db` geändert** (0c `e1533e23…5959`, nachher `3dbec255…e95f`). Ursache: der Cronjob dieses Bots; die Datei trägt die Zeit 13.10.2026 22:50:50, `logs/volatility_breakout/forward_test.log` dieselbe Zeit (letzter Eintrag: CAT `stop_loss` am 13.10.). Die Sitzung schreibt in keine db; die Tests berühren keine db. Die übrigen acht db sind unverändert. Laut Auftrag kein Abbruch.
2. **Ein zusätzlicher Prüfaufruf wurde abgelehnt.** Nach B8 wollte die Sitzung die Zeile „Stand der Datei: aus = …“ des neuen Tests sehen, die `WZ basis` nicht speichert (es speichert nur die letzte Zeile). Der dafür gestellte Aufruf (`env -u ANTHROPIC_API_KEY … python3 -B shared/test_agenten_aus.py | grep "Stand der Datei"`) stand nicht im Auftrag und wurde von Claude Code abgelehnt. Er wurde nicht wiederholt und nicht umgangen. Der Inhalt der Datei ist trotzdem belegt: A1 wörtlich, `cmp` in B6, Vergleich B7 „GLEICH“; der Test prüft „jeder Name ist agent1, agent3 oder agent4“ grün mit. Ein Pflichtschritt war nicht betroffen, deshalb kein Abbruch.
3. `c_kennung.txt` hat 2 Zeilen (die Kennung, dahinter `rc 0`), wie vom Befehl vorgesehen.

Sonst keine: 0b, 0d, numstat ⟨S0⟩..⟨A⟩ (21 Zeilen, Code wie Soll), Backlog und Journal wie Soll.

## Festlegung F10

Ist `config/agenten_aus.txt` **vorhanden, aber nicht lesbar** (Rechte, kein UTF-8, ein Verzeichnis statt einer Datei), gilt der gefragte Agent als **aus**: lieber kein Aufruf als ein ungewollter. Im Log steht dann „Warnung: config/agenten_aus.txt nicht lesbar (…) - Agent <n> bleibt aus“. **Fehlt** die Datei ganz, laufen alle drei Agenten wie vor TB-159. Der Test „nicht lesbare Schalterdatei: Agent bleibt aus, mit Warnung“ ist grün.

## So schaltest du einen Agent wieder ein

1. `config/agenten_aus.txt` öffnen.
2. Die Zeile mit seinem Namen löschen (`agent1` = Einordnung der neun Tagesberichte, `agent3` = Marktkontext per Web-Suche, `agent4` = Einordnung der Wochen-Mail) **oder** ein `#` davorsetzen.
3. Speichern und committen. Ab dem nächsten Lauf fragt der Agent die KI wieder.

Wird die Datei ganz gelöscht, sind alle drei wieder an. Agent 2 und der Quartals-Interpreter sind von diesem Schalter nicht betroffen.

## In einfacher Sprache

Drei KI-Helfer haben bisher Einordnungen in die Berichte geschrieben: zu den neun Tagesberichten (Agent 1), zur Marktlage (Agent 3) und zur Wochen-Mail (Agent 4). Jede Anfrage kostet Geld. Ab jetzt schaut jeder dieser Helfer zuerst in eine kleine Liste, `config/agenten_aus.txt`. Dort stehen gerade alle drei. Deshalb fragen sie die KI nicht mehr, und die Berichte gehen ohne KI-Teil raus. Die Zahlen bleiben alle drin. Alle Tests waren vorher und nachher grün. Der neue Test prüft auch, dass ein abgeschalteter Helfer wirklich keine Anfrage schickt. Zum Wiedereinschalten löschst du den Namen aus der Liste und committest. Ob die nächste Wochen-Mail wirklich ohne KI-Teil kommt, sieht man erst beim nächsten Wochenlauf.
