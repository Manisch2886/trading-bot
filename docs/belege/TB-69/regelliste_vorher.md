# TB-69, Schritt 1 — Regelliste VORHER

**Stand:** `docs/projektfuehrung/ARBEITSWEISE.md` auf `5a1f5e1` (21.09.2026), 70 905 B, 1 293 Zeilen, 25 Abschnitte (`## …`), 15 Unterabschnitte (`### …`).

**Wie gezählt wurde:** Das ganze Dokument wurde von oben nach unten gelesen. Jede Anforderung, die ein Verhalten vorschreibt (nicht: Messung, Anlass, Begründung, Hintergrund, Änderungsvermerk), ist eine Zeile. Zusammengehörige Angaben derselben Vorschrift (z. B. die drei Angaben „Was · Wo · Woran“) sind eine Regel, nicht drei; eine Vorschrift, die in einem Abschnitt eigens wiederholt oder verschärft wird, ist eine eigene Zeile, wenn sie etwas hinzufügt (Verweis auf die Erstnennung in Spalte „Kern“).

**Spalte „Betrifft“:**
- **A** = betrifft die Ausgabe einer Antwort des steuernden Chats — Form oder Inhalt dessen, was er schreibt (Chat-Antwort, Anweisung, Entscheidungsvorlage, Auftragsdokument, Bericht).
- **S** = etwas anderes — Verfahren, Sachstand, Dokumentationsführung, Abnahme, Betrieb.

**Spalte „Lage“** (nur bei A): die Situation, in der die Regel greift — für den Aufbau der Checkliste in Schritt 2.

**Nicht als Regel gezählt** (bleiben wörtlich stehen, sind Messung/Anlass/Hintergrund): der Änderungsvermerk „Geprüfte Fassung vom 18.09.2026“ (Kopf); die Berichtigung zum Einzeiler vom 19.09. (Abschnitt 1, Zeile 46 ff.); der Hintergrund „ZIP hat immer funktioniert“ (2, Zeile 195); die Kostentabelle des Downloads (5b); „Der Preis, benannt“ (5b, zweimal); die Zitate der Betreiberanweisungen (überall); die Ursachenanalyse und die Herleitung von TB-69 (6d); die Messungen zu `screen`/`tmux`/Schlüsselbund (6b); die Berichtigung zur Fassung v2.1.276/278 (5b Punkt 3, 14); der offene Punkt P1 (18, P.3); „Nicht gemessen: Historieneintrag“ (14, Regel 2); die Sperrlisten-Tabelle selbst (7, Sachstand — die Regel dazu ist R70).

| Nr | Abschnitt (Zeile) | Kern in einem Satz | Betrifft | Lage |
|---:|---|---|:---:|---|
| R1 | Kopf (6) | Dieses Dokument wird bei jeder Sitzungsübergabe mitgegeben, als Bestandteil des Übergabepakets, nicht optional | S | — |
| R2 | Kopf (8) | Vor jeder Übergabe wird der Nutzer gefragt, ob es noch passt oder ergänzt werden soll | S | — |
| R3 | 1 (28) | Bei jedem Dokument und jeder Aufgabe wird ausdrücklich gesagt, wohin es geht (welcher der vier Wege) — auch in der Begleitnachricht | A | immer |
| R4 | 1 (31–36) | Die vier Wege und ihre Zuordnung: Cloud (TB-Aufgaben, Sitzungstitel im Kopf), Mac (`TESTAUFTRAG_*`, Einzeiler mit Pfad), Fable (methodische Fragen, ein durchgehender Chat, Dateien `RUECKFRAGE_`/`ANFRAGE_`/`RUECKMELDUNG_`), diese Sitzung (Planung, Backlog) | S | — |
| R5 | 1 (38–44) | Der lokale Start wird immer als ein einziger, kopierfertiger Befehl ausgegeben (`cd` + Aufruf) — *berichtigt 20.09.: der Anweisungstext reist nicht mehr im Befehl mit, Abschnitt 14* | A | Start Mac-Sitzung |
| R6 | 1 (46–52, 65–66) | Pfad immer mitgeben, nie beschreiben — gilt für jeden Zugriff auf eine Datei, seit 20.09. für den Einfügetext statt für die Befehlszeile | A | Anweisung |
| R7 | 1 (54–63) | `--remote-control` gehört immer zum Start; jede lokale Sitzung wird so gestartet, dass sie in Web und App erscheint (Wunsch 15.09.) | A | Start Mac-Sitzung |
| R8 | 1 (68–71) | Bei Fable immer dazusagen: bestehender Chat oder neuer (Faustregel: Bezug auf frühere Aussagen/Kürzel → bestehender; ergebnisoffen → neuer) | A | Fable-Datei |
| R9 | 1 (73–74) | Eine Sitzung je Aufgabe, immer frisch von `main`; nach einem Merge nicht auf demselben Branch weiterarbeiten | S | — |
| R10 | 2 (84–89) | Jedes Ergebnisdokument wird als Download-Datei bereitgestellt, für alle vier Wege — nie als Chat-Text zum Herauskopieren | A | immer (Dokument) |
| R11 | 2 (90–101) | Dateiname UND Überschrift nennen den Empfänger (Tabelle `CLOUD_TB-`/`MAC_TESTAUFTRAG_`/`FABLE_RUECKFRAGE_`); bei Fable steht bestehender/neuer Chat in der Überschrift | A | immer (Dokument) |
| R12 | 2 (102–117) | Kein Archiv: Ergebnisse als Commit im Repo und als einzelne Dateien im Chat — nie als ZIP (20.09.); Tabelle, was am Ende wo liegt (Mac: `docs/`, `docs/belege/TB-<Nr>/`, `docs/auftraege/`, committet nach jedem fertigen Teil; Cloud: über Zweig und PR; Chat: einzelne Dateien in der Antwort) | A | immer (Abgabe) |
| R13 | 2 (119–133) | Erzeugt ein im Chat Schritt für Schritt angewiesener Mac-Lauf einen Befund, wird die Ausgabe in eine Datei unter `docs/belege/` geschrieben und committet; die Anforderung gehört ausdrücklich in den Auftrag an die Cloud-Sitzung („Das Testdokument verlangt am Ende ebenfalls …“) | A | Anweisung / Auftrag |
| R14 | 2 (135–141) | Beim Abnehmen jeder Cloud-Übergabe wird nachgesehen, ob das Testdokument die Commit-Pflicht und „In einfacher Sprache“ enthält (Abnahmeliste) | S | — |
| R15 | 2 (142–146) | `ARBEITSWEISE.md`, `JOURNAL.md`, `BACKLOG.md` werden nicht bei jeder Änderung mitgeschickt; geänderte Regeln werden im Chat genannt, mit Datum und Abschnitt | A | immer |
| R16 | 2 (148–152) | Der Nutzer wird zu geeigneten Zeitpunkten an den Download erinnert (Ende eines Arbeitsabschnitts, vor Pause, vor Übergabe, viel Ungesichertes) — dann samt aller nötigen Schritte | A | Abschnittsende |
| R17 | 2 (153–174) | Die Sicherung geht immer ins Repo nach `docs/projektfuehrung/`, mit dem vierschrittigen Ablauf (Einzeldateien · `git branch`/`status` auf `main` · `ls -lt` mit Bytegrössen · kopieren, prüfen, add+commit+push in einem Zug) — seit 18.09. die Ausnahme für Texte, die für einen Auftrag zu gross sind (Regelweg 5b) | S | — |
| R18 | 2 (176–180) | Ab der ersten Ablage ist die Fassung im Repo die massgebliche; jede Änderung nimmt denselben Weg zurück | S | — |
| R19 | 2 (182–186) | Stehende Regeln werden nicht in jedes Aufgabendokument abgeschrieben — ein Verweis auf `docs/projektfuehrung/ARBEITSWEISE.md` genügt | A | Auftrag |
| R20 | 2 (188–195) | Grosse Dokumente (`BACKLOG.md`, `JOURNAL.md`) werden nicht neu geschrieben, sondern als Nachtrag geliefert: neue Blöcke plus benannte Ersetzungen mit Stelle; `ARBEITSWEISE.md` ist die Ausnahme und wird ganz geliefert | A | Dokumentation |
| R21 | 3 (200–216) | Jedes Aufgabendokument trägt im Kopf: `# TB-<Nr> <Kurzname>`, Sitzungstitel (Pflicht), Modell, Repo/Base „frisch von `main`“ | A | Auftrag |
| R22 | 3 (213–216) | Modell-Standard ist Opus 5, Aufwand hoch; eine abweichende Empfehlung wird begründet dazugeschrieben | A | Auftrag |
| R23 | 4 (221–229) | Jedes Ergebnis endet mit „In einfacher Sprache“ (Was wir wissen wollten · Was herauskam · Warum · Was das für dich heisst), kein Fachbegriff ohne Erklärung — auch im Journal bei jedem Ergebnisblock | A | Bewertung |
| R24 | 4 (231–246) | Eingegrenzt 15.09.: nur bei aufbereiteten Rückmeldungen von aussen (Cloud, Fable, Mac) — dort immer, im Dokument UND am Ende der Chat-Antwort; nicht in der Planungsunterhaltung. Prüffrage: berichte ich Fremdes → ja; rede ich übers Vorgehen → nein | A | Bewertung |
| R25 | 5 (250–251) | `BACKLOG.md` ist die kanonische Quelle; bei Widerspruch zu Notizen gilt die Datei | S | — |
| R26 | 5 (252–254) | Jedes offene Thema, jede getroffene und ausstehende Entscheidung, auch verworfene Ideen mit Begründung, wird eingetragen | S | — |
| R27 | 5 (255–256) | `JOURNAL.md` nimmt abgeschlossene Ergebnisblöcke auf und wird nie umgeschrieben, nur ergänzt | S | — |
| R28 | 5 (257–258) | Nach jedem relevanten Abschnitt beide Dateien aktualisieren und als Download ausgeben — *seit 5b als Auftrag an die Mac-Sitzung statt Download* | A | Abschnittsende |
| R29 | 5 (259–265) | Fortschreiben spätestens bei der Übergabe, und dann vollständig | S | — |
| R30 | 5b (270–279) | Drei Wege der Dokumentationsänderung (ganz ersetzen · Nachtrag · neu dazulegen); Regelweg ist der Auftrag an die Mac-Sitzung; Nachträge an `BACKLOG.md`/`JOURNAL.md` immer als Auftrag an eine Sitzung, nie von Hand — Anweisung „mache das zukünftig immer so“ | S | — |
| R31 | 5b (281–296) | „Null entfernte Zeilen“ wird an der git-Zeile belegt (`numstat` je Datei), Ersetzungen exakt getroffen, der letzte Journal-Block geprüft statt geraten, mehrere Dateien in einem Zug | S | — |
| R32 | 5b (298–312) | Dokumentationsänderungen gehen als Auftrag an die Mac-Sitzung, nicht als Download; sie pusht direkt auf `main`, ohne Zweig und PR | S | — |
| R33 | 5b (314–319) | Der Text steht wörtlich im Auftrag, mit der Einfügestelle als Ankertext; ein neues Dokument bis ein paar hundert Zeilen ebenso, sonst Download | A | Auftrag (Dokumentation) |
| R34 | 5b (321–329) | Harte Auflagen jedes Dokumentationsauftrags: nur `docs/`; `numstat` je Datei mit Zuordnung jeder entfernten Zeile; nichts inhaltlich umformuliert (Sachfehler melden, nicht korrigieren); `git status --porcelain` nach dem letzten Commit; Ankertext wörtlich | A | Auftrag (Dokumentation) |
| R35 | 5b (338–362) | Jede Bewertung eines Ergebnisses bringt ihren Backlog- und Journal-Nachtrag in derselben Antwort mit — auch bei Fable-Antworten, auch wenn er kurz ist, nicht in einer späteren Antwort | A | Bewertung |
| R36 | 5b (364–381) | Der feste Ablauf: Nachtrag schreiben → Auftrag `MAC_TB-<Nr>_<Kurzname>.md` mit Numstat-Auflage, Ankertext, „nichts umformuliert“ → Nutzer startet die Mac-Sitzung (Text kommt gesondert) → vor dem Merge Merge-Basis-Vergleich, `numstat`, `git status` nach dem letzten Commit | S | — |
| R37 | 5b (383–384) | Der Dokumentationsauftrag berührt ausschliesslich `docs/` und läuft parallel zu fachlichen Aufgaben | S | — |
| R38 | 5b (386–388) | Der Stand-Abschnitt in `START_HIER.md` wird bei jeder Dokumentationsrunde mitgeschrieben | S | — |
| R39 | 6 (394–395) | Nichts wird verworfen oder gelöscht, ohne vorher zu fragen — Notizen, Dateien, Backlog-Einträge | A | Verlust droht |
| R40 | 6 (397–404) | Vor jedem drohenden Verlust wird ausdrücklich gewarnt: vor dem Ersetzen einer Datei, bei ungesicherten Änderungen an `BACKLOG`/`JOURNAL`/`ARBEITSWEISE` am Abschnittsende, vor jeder Übergabe | A | Verlust droht |
| R41 | 6 (406–412) | Der Arbeitsordner der Sitzung ist kein Speicherort; ein Download wird an jedem abgeschlossenen Abschnitt angeboten, nicht erst am Ende | A | Abschnittsende |
| R42 | 6b (417–419) | Anweisungen an den Nutzer: Schritt für Schritt, nummeriert — keine zusammengefassten Absätze | A | Anweisung |
| R43 | 6b (421–427) | Je Schritt drei Angaben: Was · Wo · Woran du merkst, dass es geklappt hat | A | Anweisung |
| R44 | 6b (429–432) | Bei Dateien sagen, wo sie liegen müssen; bei mehreren Wegen, welcher zuerst und ob die Reihenfolge zwingend ist; was schiefgehen kann und was dann zu tun ist | A | Anweisung |
| R45 | 6b (434–440) | Gilt auch für Termius und das Beenden einer Sitzung: jeder Schritt einzeln, auch Trennen und Schliessen, mit der Folge für den laufenden Prozess; Knopfnamen und Menüpfade, die die Sitzung nicht sehen kann, werden nicht erfunden — das Ziel wird benannt | A | Anweisung |
| R46 | 6b (442–447) | Auch wenn der Schritt trivial aussieht — ohne Ausnahme | A | Anweisung |
| R47 | 6b/Editor (449–479) | Ein Befehl, der einen Editor öffnet (`crontab -e`, `git rebase -i`, `git commit` ohne `-m`, …), wird nie ohne den Weg heraus gegeben: Speichern und Schliessen in derselben Anweisung, Tastendruck für Tastendruck, mit Erkennungszeichen; für `crontab` wird `EDITOR=nano` vorangestellt; der Weg hinaus ohne Speichern gehört dazu | A | Anweisung (Editor) |
| R48 | 6b/Editor (481–483) | Danach immer eine Zählung als Kontrolle (`crontab -l \| grep -c <muster>` mit erwarteter Zahl), nie „sollte jetzt drin sein“ | A | Anweisung (Editor) |
| R49 | 6b/Start (486–507) | Der Start einer Mac-Sitzung wird als getrennte Kopierblöcke ausgegeben, in dieser Reihenfolge: `screen -U -S tb` (immer, zuerst) · `security unlock-keychain` (immer, zweites Fenster) · `cd ~/trading-bot && claude --remote-control` (immer) · Einfügesatz mit TB-Nummer (immer) · `screen -r tb` (nach Abbruch) · `/remote-control` (nur wenn die Sitzung schon läuft) — nie beschrieben statt geliefert | A | Start Mac-Sitzung |
| R50 | 6b/Start (520–526) | Meldet der Betreiber „Abbruch“, wird gemessen, wie weit die Sitzung kam (Commits, Arbeitsbaum, `index.lock`), und die passenden Blöcke kommen ohne Rückfrage | A | „Abbruch“ |
| R51 | 6b/Ende (528–546) | Das Ende einer Sitzung wird genauso vorgegeben wie der Anfang; zuerst der Unterschied Ablegen (`Strg`+`A`, `D` — Claude läuft weiter) gegen Schliessen (Schliessfolge); Ablegen ist der Normalfall, solange ein Auftrag rechnet | A | Ende Mac-Sitzung |
| R52 | 6b/Ende (548–556) | Die Schliessfolge, vier Schritte mit Erkennungszeichen: `Strg`+`D` an der leeren Eingabezeile (sonst zweimal `Strg`+`C`, erst dann `/exit`) · `exit` · `screen -ls` · Termius trennen | A | Ende Mac-Sitzung |
| R53 | 6b/Ende (558–567) | `/exit` steht bewusst zuletzt (ein offener Dialog fängt es ab); auf dem Telefon liegt `Strg` in der Termius-Zusatzreihe; die Verbindung wird nie gekappt, während oben etwas läuft — Schritt 4 kommt zuletzt | A | Ende Mac-Sitzung |
| R54 | 6b/Ende (569–576) | Wann was mitgegeben wird, ohne dass er fragt: Auftrag gestartet → Startblöcke und Ablegen · fertig, es geht weiter → Startblöcke des nächsten · fertig, Schluss → vollständige Schliessfolge · „Abbruch“ → erst messen, dann `screen -r tb` | A | Start/Ende Mac-Sitzung |
| R55 | 6b/Ende (578–580) | Nie zusammengefasst, nie im Fliesstext beschrieben, nie mit der Begründung weggelassen, dass es letztes Mal schon dastand | A | Start/Ende Mac-Sitzung |
| R56 | 6b/Ende (582–584) | Die Kontrolle nach Abschnitt 14 gehört dazu: Kopfzeile nennt „Claude Max“, Fusszeile zeigt kein „Not logged in“; bleibt es dabei, erst dann `/login` | A | Start Mac-Sitzung |
| R57 | 6bb (590–606) | Jede Antwort, aus der für den Nutzer etwas zu tun folgt, endet mit einem eigenen, abgesetzten Block („Deine Aufgaben“ / „Was du jetzt tust“): nummeriert in Reihenfolge, je Aufgabe Was · Wo · Woran, dazu was nicht von ihm abhängt; ist nichts zu tun, wird das ausdrücklich gesagt — kein erfundener Block | A | immer (Antwortende) |
| R58 | 6bb (614–615) | Auch bei Wartezuständen: was wann von wem kommt, und was in der Zwischenzeit zu tun ist | A | immer (Antwortende) |
| R59 | 6c (619–627) | Keine Bemerkungen zu Tageszeit, Arbeitsdauer oder Arbeitsende; sachliche Terminhinweise (Fristen, Dauer eines Schritts) bleiben unberührt | A | immer |
| R60 | 6d (632–648) | Wo eine Entscheidung ansteht, stehen drei Dinge beieinander: die Möglichkeiten vollständig, jede mit ihrem Preis · eine Empfehlung, ausdrücklich benannt · die Begründung, warum diese und was sie schlechter macht | A | Entscheidung |
| R61 | 6d/Form (668–692) | Jede Entscheidung, die beim Betreiber liegt, wird als anklickbare Multiple-Choice-Frage gestellt — nicht beschrieben, nicht als Tabelle; die empfohlene Antwort steht an erster Stelle und ist gekennzeichnet; auch bei zwei Wegen, auch wenn sie klein wirkt; nicht gesammelt ans Ende der Antwort | A | Entscheidung |
| R62 | 6d (699–702) | Grenze: hängt die Entscheidung von etwas ab, das nur der Betreiber weiss (Risikotragfähigkeit, Zeit, Wohnsitzrecht), wird das gesagt statt geraten | A | Entscheidung |
| R63 | 7 (705) | Ein Befehl je Nachricht, nicht mehrere hintereinander | A | Terminal |
| R64 | 7 (706–707) | Vor jedem `git pull`: `git status --short` | S | — |
| R65 | 7 (708) | Bei SSH-Sitzungen vorher `pwd` und `git branch --show-current` prüfen | S | — |
| R66 | 7 (709–732) | Secrets nie anzeigen (`grep -c` statt `cat`); es wird gar kein Befehl vorgeschlagen, dessen Ausgabe einen Schlüssel enthalten könnte — Nie-Liste (`cat`/`head`/`tail`/`less`/`more`/`env`/`printenv`/`echo $VAR`/`set` auf `.env`, Konfigurationen, Schlüsselablagen, Logs; `git diff`/`git show` darauf; `security find-generic-password`; `curl` mit Klartext-Header), Stattdessen-Liste (`grep -c`, `test -f`, `wc -l`, `grep -q … && echo GESETZT`); Werte nur über `shasum` oder Länge vergleichen; sonst schaut der Nutzer selbst und antwortet ja/nein | A | Terminal |
| R67 | 7 (733–735) | Mehrzeilige Eingaben (Heredoc, Python-Blöcke) funktionieren über Termius nicht; zeilenweise mit `echo … >>` aufbauen | A | Terminal |
| R68 | 7 (736–748) | Vor jedem Merge gegen die Merge-Basis vergleichen (`git diff --stat $(git merge-base main origin/<zweig>)..origin/<zweig>`), nie `main..zweig` und nicht die Drei-Punkt-Form | S | — |
| R69 | 7 (749–753) | Vor dem Merge wird der Diff der Sperrlisten-Dateien angesehen, wenn die Statistik eine davon nennt — auch bei ausdrücklicher Freigabe | S | — |
| R70 | 7 (755–764) | Die Sperrliste (Stand 18.09.): `live_params.py`, `forward_test.py`, `equity_simulation.py` (hart), `multi_symbol_optimise.py`, `shared/entscheidungskerze.py`, `shared/paths.py` | S | — |
| R71 | 7 (766–777) | `git status --porcelain` wird nach dem letzten Commit aufgenommen; vor jedem Merge zusätzlich `git diff --stat origin/<zweig> -- docs/ research/` | S | — |
| R72 | 7 (779–785) | Eine Abweichung, die auf den Betrieb zeigt, wird gegen den Betrieb geprüft (Zeitstempel gegen Crontab desselben Bots, Ortszeit gegen UTC; Inhalt gegen die Logzeile) — nicht von Hand plausibilisiert | S | — |
| R73 | 7 (787–790) | Fundstellen werden nur genannt, wenn sie vor einem liegen; sonst steht ausdrücklich „aus dem Gedächtnis“ dabei | A | immer |
| R74 | 7 (791–797) | Jede Zahl aus einem fremden Bericht wird an der Rohausgabe (`docs/belege/`) nachgerechnet, bevor sie weitergereicht wird | A | Bewertung |
| R75 | 7 (798–801) | Zeilen, die kein Befehl sind (SSH-Schlüssel, Dateiauszug, Beispieltext), werden als solche gekennzeichnet — sie gehören ins Web-Formular oder in den Editor, nicht in die Eingabezeile | A | Terminal |
| R76 | 7b (809–827) | Sachstand GitHub vom Mac: `origin` über SSH, Schlüssel `~/.ssh/id_ed25519_signing` (Authentication und Signing Key), `~/.ssh/config`-Eintrag nötig; beim Anlegen eines Schlüssels verlangt GitHub „Confirm access“; `gh` und Homebrew sind nicht installiert (Merges lokal, PR-Reihe ab TB-42 unvollständig, E5) | S | — |
| R77 | 7b (829–837) | Sachstand der übrigen Zugänge: Binance (`.env`, dritter Schlüssel), Telegram (`config/`), E-Mail (`config/email_config.py`, 17 Module, T37.3), IBKR (`broker/zugang.py`, T37.4), Dashboard über Tailscale (`DASHBOARD_HOST` nur in `.env`, F6/O2) | S | — |
| R78 | 7b (839) | Für alle Zugänge gilt Abschnitt 7 ohne Ausnahme: Existenz prüfen, nie den Wert (Wiederholung von R66) | A | Terminal |
| R79 | 7c (843–858) | Was in jedem Testauftrag für den Mac steht: Schritt 0 Sicherung der neun `*.db` mit Quersummen · Datenstand vorher/nachher (Soll `d9449faf…`, 223 Dateien) · Basislauf mit Zeitgrenze, bekannt rote und ungeprüfte Tests gekennzeichnet, auch plötzlich grüne · Interpreter `trading-env/bin/python3` · Abbruchkriterium nur für Fehlschläge am Gegenstand (T44.11) · `git status --porcelain` nach dem letzten Commit · Commit nach jedem fertigen Teil, kein Archiv · „In einfacher Sprache“ am Ende | A | Auftrag (Mac) |
| R80 | 8 (863–866) | Laufend prüfen, ob weitere profitable Strategien möglich sind — ohne eine als profitabel zu bezeichnen, bevor sie gemessen ist; Kandidaten mit Hypothese und Abbruchkriterium ins Backlog | S | — |
| R81 | 8 (867–869) | Wochenrückmeldung an Fable, sonntags: gemessene Ergebnisse und Widersprüche, keine Fortschrittsberichte | S | — |
| R82 | 9 (874–875) | Direkt und ehrlich: wenn eine Zahl nicht trägt, wird das gesagt — auch wenn sie aus einer eigenen Empfehlung stammt | A | immer |
| R83 | 9 (876–877) | Eigene Fehler werden benannt, nicht stillschweigend korrigiert; im Backlog bleiben sie mit Begründung stehen | A | immer |
| R84 | 9 (878–879) | Keine Gefälligkeit — die unbequeme Antwort | A | immer |
| R85 | 10 (885–893) | Der Umzug folgt `UMZUG.md`; für ihn gilt dieselbe Regel wie für jede Abgabe: Commit im Repo und einzelne Dateien, kein Archiv | S | — |
| R86 | 10 (890–891) | Der Betreiber wird frühzeitig auf einen nötigen Umzug hingewiesen (Weisung 19.09.) | A | Umzug nötig |
| R87 | 10 (897–898) | Die Übergabe wird laufend fortgeschrieben, nicht beim Umzug geschrieben | S | — |
| R88 | 10 (899–902) | Nichts, was den Umzug überleben muss, steht in nur einem Träger und niemals nur im Chatverlauf; Träger sind Erinnerung, Projektablage, Repo — `logs/auftraege/` ist keiner | S | — |
| R89 | 10 (903–904) | Nicht umziehen, während eine Sitzung läuft oder Arbeit uncommittet ist | S | — |
| R90 | 10 (906–909) | Vor jedem Umzug wird der Betreiber gefragt, ob die Arbeitsweise passt; jede vereinbarte Regel wird gegen dieses Dokument geprüft, nicht erinnert (schärft R2) | S | — |
| R91 | 11 (925) | Ein Verbot nennt, wovor es schützt — dann ist eine neue Datei erkennbar nicht gemeint | A | Auftrag |
| R92 | 11 (926) | Prüfwerkzeuge, die eine Aufgabe erzeugt, gehören ins Repo — ausdrücklich, mit Zielpfad | A | Auftrag |
| R93 | 11 (927) | Beim Abnehmen gegenprüfen, ob alles, was die Aufgabe erzeugt hat, dort liegt, wo es gebraucht wird | S | — |
| R94 | 12 (936–948) | Die Prüfprinzipien stehen in `docs/PRUEFPRINZIPIEN.md`, gehören ins Übergabepaket und werden in jedes Aufgabendokument verwiesen, nicht abgeschrieben | A | Auftrag |
| R95 | 13 (953–968) | Eine Antwort endet nie mit einem Stillstand: der nächste Handwerksschritt wird getan; kein „soll ich …?“ für Anstehendes; keine offene Frage nach dem nächsten Schritt am Ende; die nächste Aufgabe wird begonnen; neben einer Rückfrage wird alles Unabhängige in derselben Antwort erledigt | A | immer (Antwortende) |
| R96 | 13 (970–976) | Grenze: Verfahrensfragen vor dem signierten Tag gehen an Betreiber oder Fable, nie nach erwartetem Effekt; eine Entscheidungsvorlage ist kein Haltepunkt — gefragt wird nebenher, nicht statt zu arbeiten | A | Entscheidung |
| R97 | 13 (978–981) | Freigabepflichtige Befehle bleiben beim Betreiber; alles bis zu ihnen wird fertig gemacht, sodass nur das Einfügen bleibt | A | Terminal |
| R98 | 13 (983–988) | Die Aufgabenliste nach 6bb ist so kurz wie möglich und enthält nie „entscheiden, wie es weitergeht“; ist nichts zu tun, wird das gesagt und die Arbeit läuft weiter | A | immer (Antwortende) |
| R99 | 14/Regel 0 (1004–1046) | Zuerst die Anmeldung prüfen: `security unlock-keychain` in einem zweiten Fenster (Passwort an der Eingabeaufforderung, nie als Argument, nie in den Chat), dann `cd ~/trading-bot && claude --remote-control`; bleibt es bei „Not logged in“, erst dann `/login`; Kontrolle: Kopfzeile „Claude Max“, Fusszeile ohne „Not logged in“ | A | Start Mac-Sitzung |
| R100 | 14/Regel 1 (1051–1060) | Der Anweisungstext reist nie im Startbefehl mit: nackter Start in einer Zeile, der Text danach als eigener Block in die wartende Eingabezeile; läuft die Sitzung schon, `/remote-control` als eigener Block davor | A | Start Mac-Sitzung |
| R101 | 14/Regel 2 (1062–1078) | Ein fester Zeiger: `docs/auftraege/AKTUELLER_AUFTRAG.md` enthält nur den Pfad des gültigen Auftrags; der Einfügesatz ist bis auf die vorangestellte TB-Nummer immer gleich, der letzte Satz ist die Wache (Abbruch bei falscher Nummer), die Empfangsbestätigung ist die Zeile mit dem Auftragsnamen | A | Start Mac-Sitzung |
| R102 | 14/Regel 3 (1083–1087) | Gesichert wird nach jedem fertigen Teil, nicht am Ende; jeder Mac-Auftrag trägt einen Schritt 0 („Committe, was im Arbeitsbaum liegt“), und der Nachweis „Arbeitsbaum sauber“ wird danach geprüft | A | Auftrag (Mac) |
| R103 | 14/Regel 3 (1089–1097) | Commit und Push stehen nicht als letzter Nachweis in der Liste — Sichern ist ein Schritt, keine Abgabe | A | Auftrag (Mac) |
| R104 | 14/Regel 3 (1099–1107) | Die Sitzung committet ihren eigenen Auftrag (`docs/auftraege/`) und ihre Belege (`docs/belege/TB-<Nr>/`) mit, im Zug des Teils, zu dem sie gehören; kein Archiv | A | Auftrag (Mac) |
| R105 | 14/Regel 3 (1109–1122) | Zur Abgabe gehört seit 21.09. der Journalblock selbst: die Mac-Sitzung fügt ihn ans Ende von `JOURNAL.md` an, mit Quellenzeile auf ihr Ergebnisdokument, Buchstabe gemessen, nichts umgeschrieben; Chat-Nachträge bleiben Nachtragsdateien (Wächter zuständig); Preis: keine Wache für Mac-Blöcke, die Probe „Ergebnisdokument ohne Quellenzeile“ ist nicht gebaut | A | Auftrag (Mac) |
| R106 | 14/Regel 4 (1124–1145) | Nach jedem Start wird gemessen, ob der Text angekommen ist (`git --no-optional-locks log -1 …` und `ls-files --others`); die Messung beweist den Empfang, nicht den Fortschritt (Deutungstabelle); eine lesende Sitzung zeigt ihren Fortschritt in Web und App | S | — |
| R107 | 14/Regel 4 (1147–1148) | `git status` bleibt über die Geräteanbindung verboten (Block 7, Punkt 8) — die beiden Befehle oben beantworten dieselbe Frage lesend | A | Terminal |
| R108 | 15 (1154–1172) | Leitet der Betreiber eine Angabe mit „zukünftig“ ein, ist das eine stehende Anforderung: sie wird in derselben Antwort in die zuständigen Träger eingetragen, ohne Rückfrage — Erinnerung (immer), `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, Backlog-Nachtrag (immer, Nummer nach K2i), Projektablage | A | „zukünftig“ |
| R109 | 15 (1174–1177) | Läuft gerade eine Mac-Sitzung, ist `docs/` gesperrt; der Text geht ins Zwischenlager `logs/auftraege/` mit der Bringschuld im Kopf und wird übertragen, sobald die Sitzung fertig ist | S | — |
| R110 | 15 (1184–1203) | Jede Rückfrage an den Betreiber steht samt Antwort wörtlich, mit Zeitpunkt, im Ergebnisdokument — Mac, Cloud, Chat; nicht als Zusammenfassung, nicht als „nach Rücksprache freigegeben“ | A | Bericht / Auftrag |
| R111 | 16 (1210–1211) | Jede Änderung sagt, was sie ablöst — und das Abgelöste wird entfernt, nicht danebengestellt | S | — |
| R112 | 16 (1212–1214) | Vier Träger sind ausgenommen: Register, `JOURNAL.md`, Backlog-Abschnitt 8, `PRUEFPRINZIPIEN.md` | S | — |
| R113 | 16 (1215–1216) | Gelöscht wird nur mit Nachweis — byteweise gegen den Verbleib geprüft oder ausdrücklich als ersatzlos benannt | S | — |
| R114 | 17 (1224–1243) | Jede Aufgabe beginnt mit ein bis zwei Sätzen in einfacher Sprache, was jetzt passiert — vor der ersten Messung, ohne Fachbegriffe und Vorgeschichte; Abgrenzung zu Abschnitt 4 (Einstieg immer, Abschluss nur bei Fremdergebnissen) | A | Aufgabenbeginn |
| R115 | 18 (1252–1253) | Regel 9 wirkt in beide Richtungen: Aufräumen heisst auch zurückholen, was am falschen Ort gelandet ist | S | — |
| R116 | 18/P.3 (1255–1270) | Sachstand: drei Dateien, die der Betrieb selbst schreibt (`portfolio_overview_curve_live.csv`, `results/*/equity_curve.csv`, `dashboard_snapshot.json`), ändern sich ohne Zutun und blockieren Pulls | S | — |
| R117 | 18/P.4 (1272–1293) | In jede Aufgabenbeschreibung gehört: belegt/erschlossen/offen trennen · Raten verbieten, Platzhalter verlangen · Sitzungstitel · frisch von `main` · alle Ergebnisdokumente am Ende im Repo, nicht gebündelt (Wortlaut) · kurze Dokumente zusätzlich als einzelne Datei im Chat | A | Auftrag |

## Die Zahl

**117 Regeln.** Davon **A (Ausgabe einer Antwort): 76**, **S (anderes): 41**.

Das ist das SOLL für Schritt 4: jede der 117 Nummern muss sich im neuen Stand wiederfinden, mit ihrem Ort.

## Nebenbefunde beim Lesen (keine Änderung in diesem Schritt)

| | Befund | Ort |
|---|---|---|
| N1 | Abschnitt 14 Regel 0 sagt *„der erste Befehl jeder Mac-Sitzung ist `/login`, nicht der Auftrag“* und vier Zeilen später *„Bleibt es bei ‚Not logged in', erst dann `/login`“* — beide Sätze stehen nebeneinander; die zweite Fassung ist die, die 6b/Ende und `AKTUELLER_AUFTRAG.md` wiederholen | 14, Zeilen 1027 und 1041 |
| N2 | Der Einfügesatz in 14 Regel 2 lautet anders als der in `docs/auftraege/AKTUELLER_AUFTRAG.md` (dort: *„suche dort die Zeile mit genau der TB-Nummer … Kommt deine Nummer dort nicht vor“*; hier: *„Nennt diese Datei eine andere TB-Nummer als die vorangestellte“*). Die Datei ist die gelebte Fassung — mit dieser Sitzung gestartet | 14, Zeile 1069 |
| N3 | Abschnitt 2, letzter Absatz: *„ZIP hat immer funktioniert“* steht als Hintergrund unter einem Abschnitt, der ZIP seit 20.09. abschafft — historischer Beleg, bleibt wörtlich | 2, Zeile 195 |
| N4 | Abschnitt 5, vierter Punkt (R28) verlangt *„als Download ausgeben“*, 5b macht den Auftrag an die Mac-Sitzung zum Regelweg — R28 gilt nur noch mit 5b gelesen | 5, Zeile 257 |
| N5 | 14 Regel 4 verweist auf *„Block 7, Punkt 8“* und *„Block 7, Punkt 2“* — das sind Nummern der Erinnerung des steuernden Chats, nicht dieses Dokuments | 14, Zeilen 1140 und 1148 |
