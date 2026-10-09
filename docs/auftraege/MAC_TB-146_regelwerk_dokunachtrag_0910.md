# TB-146 Regelwerk- und Dokunachtrag 09.10.2026 — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 09.10.2026** (Helfer BAU146, per Skript aus Bausteinen und 15 fertigen Stücken), gebaut ausserhalb des Repos (Entscheid W1), nur lesend am Repo; alle Einfügungen an Kopien simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht.

**Sitzungstitel:** `TB-146` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `bbe26ba79f763c270109d9e9f97ac79d5b9fe4c8` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-146`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-146/tb146_einfuegen.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-146/`. **Ergebnis:** `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** Die Regeln, Berichtigungen und Stände vom 09.10.2026 stehen im Regelwerk: 14 Stücke in drei Dateien (35 Zeilen, nur eingefügt) und der Journalblock der Sitzung mit dem Nachtrag J1.
**Bauart wie TB-145** (`docs/auftraege/MAC_TB-145_regelwerk_nachtrag_0809.md`, Ergebnis `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md`), mit den Werten von hier; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen. **Anders:** Jedes Stück steht wörtlich in Anhang A; das Werkzeug holt keine Zeile aus `UEBERGABE.md` und liest sie nicht. Wie in TB-145 gibt es nach stdout aus (die Sitzung leitet in den Beleg um), prüft alle Stücke, bevor es eine Datei schreibt, und schreibt an Ort und Stelle — es legt keine Hilfsdatei an. Die Sitzung ändert kein Werkzeug und kein Programm des Repos.
**Reihenfolge:** Schritt 0 → A (Modus) → E (Einfügen, Commit) → J (Journalblock) → F (Nachweis, Ergebnis, Abgabe).

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — der Auftrag fügt nur Dokumentation ein; kein Werkzeug und kein Programm wird geändert. Am HEAD gemessen: Register `docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 10 „Die Sperrliste“ (Z. 971–1177) und die Tabelle „Die Sperrliste, Stand 18.09.2026“ in `ARBEITSWEISE.md` (Z. 1172–1181) enthalten `projektfuehrung`, `auftraege`, `ARBEITSWEISE`, `UMZUG`, `BACKLOG`, `JOURNAL`, `belege`, `ERGEBNIS` und `docs/` je 0-mal.

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | Zeilen + (numstat-Soll, entfernt 0) |
|---|---|---|
| `docs/projektfuehrung/ARBEITSWEISE.md` | R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R12, R11 | **16** |
| `docs/projektfuehrung/UMZUG.md` | U1 | **10** |
| `docs/projektfuehrung/BACKLOG.md` | B1 | **9** |
| `docs/projektfuehrung/JOURNAL.md` | J1 (Schritt J, mit dem Block der Sitzung) | Block + 7 + 1 + 3 |
| neu: `docs/belege/TB-146/…`, `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md` | Belege, Werkzeug, Ergebnis | — |

In den vier Zieldateien wird **nur eingefügt;** keine bestehende Zeile wird geändert oder entfernt. Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (die Einträge aus 0a); das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** alles unter `docs/werkzeuge/` (auch `ablage_soll.py`); `docs/projektfuehrung/FABLE_DIALOG_INDEX.md`; `UEBERGABE.md` nach Schritt 0; Register und Registerkopie; `research/`, `shared/`, `strategies/`; frühere Belegordner (`docs/belege/` ausser `TB-146/`); den Wortlaut eines Stücks umformulieren, kürzen oder zusammenlegen (Sachfehler: melden, nicht berichtigen). Nie `git add -A`, nie `git add .`; jeder Commit nennt seine Dateien mit Namen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD gemessen, Helfer BAU146): Ausgang der vier Zieldateien wie in 0b. Letzte Journalkennung EL (`JOURNAL.md` Z. 10291); vor `## Wiederkehrende Lehren` (Z. 10332) stehen `---` und eine Leerzeile. Im Arbeitsbaum (bei jedem Bau dieses Auftrags neu gemessen): `AKTUELLER_AUFTRAG.md` und `UEBERGABE.md` verfolgt, die drei Fable-Dateien aus 0a vorhanden und nicht verfolgt (`git ls-files -o --exclude-standard`, vom steuernden Chat am 09.10.2026, 22:23 gemessen; die Antwort liegt seit 21:52 dort, nach dem Lauf des Helfers BAU146), kein Ordner `docs/belege/TB-146/`.
- **Angabe des steuernden Chats, vom Helfer nicht gemessen** (`git status` ist dem Helfer am Repo untersagt): Im Arbeitsbaum ist am 09.10.2026, 21:32 nur `UEBERGABE.md` geändert.
- **Erschlossen:** 0a erwartet auch `AKTUELLER_AUFTRAG.md` geändert — der steuernde Chat ändert die Datei, wenn er diesen Auftrag auslegt (wie in TB-145, dort stand sie in 0a ebenso); bleibt sie unverändert, endet 0a mit ABBRUCH. Keine Zieldatei liegt im Auslöserordner `docs/auftraege/_ausloeser/`; dass Schritt E den Sitzungswächter nicht weckt, folgt daraus und ist nicht gemessen (TB-145 weckte ihn mit zwei Dateien dort: `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md` Z. 49).
- **Offen — misst die Sitzung, nie raten:** Modus der Sitzung (Schritt A) · Stand der `UEBERGABE.md` beim Start (kein Sollwert) · Kennung des Journalblocks (erwartet EM).
- **Simulation des Helfers** (Kopien `git show HEAD:<pfad>`; Linux, Python 3.10 mit `ast.parse(feature_version=(3,9))`): `probe` rc 0, jeder Anker genau eine Zeile; `einfuegen` rc 0, geändert genau die drei Dateien, keine neue Datei; Zeilenbilanz per `diff` wie die Tabelle oben, 0 entfernte Zeilen; jedes Stück direkt an seinem eigenen Anker; in `ARBEITSWEISE.md` 16 neue Tabellenzeilen mit je drei Zellen, Zahl der Tabellen unverändert; in `UMZUG.md` je eine Leerzeile vor und hinter U1, die Zahl der Zaunzeilen bleibt gerade (+2); `vergleich` rc 0; zweiter Lauf rc 2; `journal` mit einer Attrappe als Block rc 0, Kennung EM, zweiter Lauf rc 2; der Auslese-Befehl aus 0a gibt den sha256 aus Anhang B; Gegenproben (Anker fehlt in jeder der drei Dateien, Anker doppelt, erste Zeile steht schon, Datei ohne Zeilenende, `journal` vor `einfuegen`): nichts geschrieben. **Nicht simuliert:** `git status`, `git diff` (nur mit einer Attrappe), Commit und Push, Claude Code, der Sitzungswächter, Python 3.9 selbst. Die Sitzung zählt selbst nach; ihre Zahl gilt.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-146/` entsteht:** `git status --porcelain > "$TMPDIR/tb146_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `bbe26ba79f763c270109d9e9f97ac79d5b9fe4c8` und genau diese sechs Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-09a_kern_marken_listen_handelbar_tag.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-09_eroeffnung.md
```

Jeder andere oder weitere Eintrag: **ABBRUCH**.

Dann das Werkzeug auslesen:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
i = z.index("### Werkzeug")
a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
t = "\n".join(z[a + 1:b]) + "\n"
open(sys.argv[2] + "/tb146_einfuegen.py", "w", encoding="utf-8").write(t)
print("tb146_einfuegen.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb146_einfuegen.py 09d57b7a8befc5a067210f62b2f378fb3f1334f90ddbaf318b2d27f20bd7660e`; sonst **ABBRUCH**. Commit `TB-146 Schritt 0: Stand des steuernden Chats vor TB-146` mit genau den Pfaden aus 0a (sechs; mit Namen hinzufügen), pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb146_0a.txt` unverändert nach `docs/belege/TB-146/0a_status.txt` (`cmp` gleich) und das Werkzeug nach `docs/belege/TB-146/tb146_einfuegen.py` (sha256 noch einmal). **Für jede Rohausgabe gilt:** Sie bleibt roh; die Beschreibung (was, Befehl, Bytes, Zeilen, md5) steht in `<Name ohne Endung>.kopf.txt` — zu `a_modus.txt` also `a_modus.kopf.txt`, zum Werkzeug `tb146_einfuegen.kopf.txt`. Ausgaben von `WZ` tragen ihre Kopfzeile selbst.

**0b. Ausgang** ⇒ `0b_ausgang.txt`: Zeilen und md5 der vier Zieldateien an ⟨S0⟩. Soll: `ARBEITSWEISE.md` 2 515 Z., `e7e767e7316764d2ce6c9c914470582a` · `UMZUG.md` 382 Z., `745eed37adf8c28cc9fa2aa28168de19` · `BACKLOG.md` 386 Z., `233f7bb397f1f4edfa68df70dcc43ff2` · `JOURNAL.md` 10 669 Z., `c5102f2d0aace7e1821017f757c92225`. Weicht eine ab: vermerken; die Anker entscheiden (Schritt E). Dazu Zeilen und md5 von `UEBERGABE.md` an ⟨S0⟩ — **ohne Sollwert,** sie wächst bis zum Start; nach Schritt 0 ändert die Sitzung sie nicht (Schritt F misst den md5 noch einmal).

## Schritt A — Modus messen, bevor eingefügt wird

⇒ `a_modus.txt` (roh), die Aussage ⇒ `a_modus.kopf.txt`. Die eigene Sitzung:

```
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done
echo "EIGEN=$p"; ps -o command= -p "$p"
```

Soll: Die Prozesszeile trägt `--permission-mode manual`; sonst **ABBRUCH** — nichts ist eingefügt, das in der Meldung als Erstes sagen. Dazu die eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet. *Schützt:* vor einer Sitzung, die anders läuft, als der Auftrag sie voraussetzt (in TB-145 war die Prozesszeile wie Soll: `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md` Z. 51).

## Verfahren je Stück

Jedes Stück in Anhang A nennt Zieldatei, Art, Form und Anker; sein Text steht wörtlich zwischen zwei Zeilen `~~~`. **Anker:** ein Teil genau einer Zeile der Zieldatei (zwischen ⟦ und ⟧). **Art:** `nach` oder `vor` dieser Zeile. **Form `Zeilen`:** der Text ohne Leerzeile direkt an der Ankerzeile (eine Tabellenzeile bleibt in ihrer Tabelle). **Form `Block`:** genau eine Leerzeile davor und danach, keine verdoppelt. Die Grenze eines Stücks ist allein die Zeile `~~~`: U1 enthält Leerzeilen und einen Codeblock mit drei Gravis — beides gehört zum Text. J1 hat keinen Anker — es kommt mit dem Journalblock (Schritt J).

## Schritt E — Einfügen mit dem Werkzeug

**Probe.** `PY WZ probe; echo "rc $?"` ⇒ `e_probe.txt`. Soll rc 0: 14 Zeilen `<Id> · <Datei> · Anker Z. <n> · … · erste Zeile schon 0 · Anker in neuen Texten 0 · … · ok` (Ankerzeilen und Zeilen wie in Anhang A); drei Zeilen `Datei … · Soll +<n> · gleich`; `Stuecke 14 · eingefuegte Zeilen 35`; Schlusszeile `Gesamt: wie Soll, nichts geschrieben (Probe)`. rc ≠ 0 ⇒ **ABBRUCH** (rc 3: die Zeile `ABBRUCH: …` nennt den Grund).

**Einfügen.** `PY WZ einfuegen; echo "rc $?"` ⇒ `e_einfuegen.txt`. Das Werkzeug prüft alle Stücke, bevor es schreibt: Jeder Anker trifft genau eine Zeile, die erste Zeile keines Stücks steht schon da, kein Anker kommt in einem neuen Text vor, eine Tabellenzeile landet hinter einer Tabellenzeile, die Zeilenbilanz je Datei ist wie Soll. Soll rc 0: dieselben Zeilen wie in der Probe, drei Zeilen `geschrieben und zurueckgelesen: …`, Schlusszeile `Gesamt: wie Soll, alle eingefuegt, je genau einmal`. rc ≠ 0 ⇒ **ABBRUCH**; dann immer Zeilen und md5 der drei Dateien in `abbruch.txt`; nichts geschrieben ist nur belegt, wenn die Ausgabe mit `ABGEWIESEN, nichts geschrieben` oder `Gesamt: ABWEICHUNG, nichts geschrieben` endet.

**Vergleich.** `PY WZ vergleich; echo "rc $?"` ⇒ `e_vergleich.txt`. Soll rc 0: 14 Zeilen `… · Vorkommen 1 · GLEICH`, Schlusszeile `Gesamt: alle zeichengleich, je genau einmal`.

**Zweiter Lauf.** md5 der drei Dateien, dann `PY WZ einfuegen; echo "rc $?"`, dann md5 noch einmal ⇒ `e_zweitlauf.txt`. Soll rc 2, Schlusszeile `ABGEWIESEN, nichts geschrieben: …` mit allen 14 Kennungen, md5 je Datei vorher und nachher gleich.

Commit `TB-146 E: Regelwerk- und Dokunachtrag 09.10.2026, 14 Stücke in drei Dateien` mit den drei Zieldateien und den Belegen bis hier, jede Datei mit Namen; pushen ⇒ **⟨E⟩**.

**Numstat.** `PY WZ numstat ⟨S0⟩ ⟨E⟩; echo "rc $?"` ⇒ `e_numstat.txt`. Soll rc 0: die Rohzeilen von `git diff --numstat`, drei Zeilen `Soll <Datei> <n>⇥0 · Ist [<n>, 0] · gleich` (⇥ steht für einen Tabulator) mit n aus der Tabelle unter „Freigabe“, `JOURNAL.md` nicht in der Ausgabe, `weitere Dateien ausser Belegen und Ergebnis: keine`. rc 1 ⇒ melden; **keine Zeile von Hand richten.**

## Schritt J — Journalblock

Die Sitzung schreibt ihren Block nach `docs/belege/TB-146/j_block.md`, Gliederung wie Block EL (`JOURNAL.md` ab Z. 10291): Kopfzeile `## <Kennung> — TB-146: …`, Quellenzeile, Absatz „**Quelle:**“, `### Was gemessen ist` (Leerzeile davor), `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-146. Quellenvermerk: siehe Kopf.*`; die Datei endet mit einem Zeilenende; kein `---`, nicht der Nachtrag J1 — was TB-146 selbst tat, schreibt die Sitzung in eigenen Worten.

`PY WZ journal docs/belege/TB-146/j_block.md --probe; echo "rc $?"` ⇒ `j_journal_probe.txt`, dann ohne `--probe` ⇒ `j_journal.txt`. Das Werkzeug misst die letzte Kennung, setzt vor `### Was gemessen ist` die Zeile J1 und dahinter die 6 Zeilen aus B1, die mit `- ` beginnen (wörtlich wie in Anhang A), und stellt den Block samt `---` vor `## Wiederkehrende Lehren`. Soll: acht Bedingungen `ja`, `Kennung EM (erwartet EM)`, `J1-Zeilen 7`, `Zeilen +<n>` mit n = Zeilen des Blocks + 7 + 1 + 3, rc 0. rc 2: die Bedingung mit `NEIN` lesen, den Block richten, neu — kein Abbruch; nennt das Werkzeug eine andere Kennung als EM: diese nehmen und melden. rc 3: **ABBRUCH** (die Zeile `ABBRUCH: …` nennt den Grund) — ausser die Zeile `ABBRUCH: …` beginnt mit dem Pfad der Blockdatei (`docs/belege/TB-146/j_block.md`, etwa „kein Zeilenende am Schluss“): dann den Block richten und neu, kein Abbruch. rc 1 oder ein Traceback: **ABBRUCH**.

## Schritt F — Nachweis, Ergebnis, Abgabe

**Nachweis.** `PY WZ vergleich; echo "rc $?"` noch einmal ⇒ `f_vergleich.txt` (Soll wie in Schritt E). Zeilen und md5 von `UEBERGABE.md` ⇒ `f_uebergabe.txt`; Soll: wie in 0b gemessen.

**Ergebnis** `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`: Kopf (Stand, Commits, ⟨S0⟩) · **„Kurz“** (Tabelle Schritt · Soll · Ist) · **„Abweichungen vom Auftrag“** (jede, auch kleine; sonst „keine“ mit der Liste der geprüften Sollwerte) · **„Nicht getan“** (die Posten unter „Nicht in TB-146“; Aufgaben für den Betreiber) · **„In einfacher Sprache“**. Rückfragen an den Betreiber stehen samt Antwort wörtlich darin. `f_porcelain.txt` und `f_numstat.txt` entstehen erst nach dem Abgabe-Commit: In „Kurz“ steht dazu „nach der Abgabe gemessen, siehe Beleg“, die Werte nennt die Schlussmeldung.

**Abgabe.** Commit `TB-146 Abgabe: Ergebnis, Journal <Kennung>` mit `JOURNAL.md`, dem Ergebnis und den Belegen bis hier, jede Datei mit Namen; pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb146_f.txt"`, unverändert nach `f_porcelain.txt` kopieren (`cmp` gleich; Soll 0 B), erst danach die Kopfdatei und `PY WZ numstat ⟨S0⟩ ⟨F⟩ docs/belege/TB-146/j_block.md; echo "rc $?"` ⇒ `f_numstat.txt`. Soll rc 0: die drei Dateien wie in Schritt E, `JOURNAL.md` mit n aus Schritt J und 0 entfernten Zeilen, sonst nur Belege und Ergebnis. Kleiner letzter Commit `TB-146 F: porcelain und numstat nach der Abgabe`, pushen; danach `git status --porcelain` noch einmal, Rohausgabe wörtlich in der Schlussmeldung.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab.
- Schritt A: Die Prozesszeile trägt nicht `--permission-mode manual`.
- Schritt E: `probe` oder `einfuegen` endet mit rc ≠ 0 — ein Anker hat nicht genau einen Treffer, oder die erste Zeile eines Stücks steht schon da. Das Werkzeug prüft alles, bevor es schreibt: Nach rc ≠ 0 ist keine Zieldatei geändert (die Ausnahme steht in Schritt E, „Einfügen“). Kein Stück von Hand einfügen, keinen Anker anpassen. Ebenso vor dem Commit ⟨E⟩: `vergleich` endet nicht mit rc 0, oder der zweite Lauf endet nicht mit rc 2 oder ändert einen md5.
- Schritt J: `journal` endet mit rc 3 und einer Zeile `ABBRUCH: …`, die nicht mit dem Pfad der Blockdatei beginnt, oder mit rc 1.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung** (ganze Sitzung): melden, nicht umgehen. Verlangt schon Schritt 0 oder der Abbruchweg selbst (Belege committen, pushen) eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden. *Schützt:* vor einem halben Bau wie in TB-142.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch:** `journal` endet mit rc 2 oder mit rc 3 und einer Meldung, die mit dem Pfad der Blockdatei beginnt; die Kennung ist nicht EM; 0b weicht ab; `numstat` endet mit rc 1; in F weicht `vergleich`, der md5 der `UEBERGABE.md` oder `f_porcelain.txt` ab — je weiter, unter „Abweichungen“ nennen. **Bei Abbruch:** Belege committen (jede Datei mit Namen), Grund in `docs/belege/TB-146/abbruch.txt`, pushen, melden. Was bis dahin eingefügt ist, bleibt stehen, nichts zurückdrehen: geschriebene, noch nicht committete Zieldateien gehen mit Namen in den Abbruch-Commit; die Meldung nennt sie als Erstes. Ausnahme: Hat eine Zieldatei weniger Zeilen als am Stand ⟨S0⟩ (alle Stücke fügen nur ein), wird sie nicht committet — sie bleibt im Arbeitsbaum liegen und steht in der Meldung an erster Stelle.

## Nicht in TB-146

- (a) die Formhinweise Nr. 9 bis 11 aus TB-141 (ARBEITSWEISE am HEAD `bbe26ba` Z. 1791, 2174, 2358) — die UEBERGABE nennt nur Stelle und Stichwort, keinen Wortlaut.
- (b) die Soll-Liste in `docs/werkzeuge/ablage_soll.py` — die Eröffnungsdatei liegt nur in der Ablage und unter `logs/steuernder_chat/`; eine eingefügte Zeile ergäbe nach dem Lesen des Werkzeugs „B2 Stand - FEHLT IM REPO“; zuerst ist zu entscheiden, wo die Datei im Repo liegt (eigener Auftrag).
- (c) die Zeile 09a im Dialog-Index — `dialog_index.py` schreibt je `FABLE_ANTWORT_*` eine Zeile; sie kommt mit dem Auftrag, der die Antwort ins Register trägt (die Zeile 07a kam so mit `be2fa85`).
- (d) der Fliesstext in ARBEITSWEISE 6b und 10 und die git-Liste im Codeblock von `UMZUG.md` Abschnitt 6 (`diff --name-only`; BACKLOG, Zeile „Nicht in TB-133“).
- (e) „drei enge Bau-Helfer statt einem“ — so getragen, Einzelfall, bleibt in der UEBERGABE.
- (f) Fehler Nr. 32 — die Regel steht seit TB-145 in Abschnitt 0.
- (g) die Ablage und die Projekt-Erinnerung (macht der steuernde Chat).

## In einfacher Sprache

Am 09.10.2026 sind neue Regeln und Berichtigungen entstanden, die bisher nur in der Übergabe stehen. Dieser Auftrag trägt sie dort ein, wo man sie später sucht: im Regelwerk (ARBEITSWEISE, Abschnitt 0), in der Umzugsanleitung, im Backlog und im Journal. Es wird nur ergänzt, nichts gelöscht oder umgeschrieben; ein kleines Programm fügt die fertigen Texte ein und prüft vorher, ob jede Stelle eindeutig ist. Kein Programm und kein Werkzeug des Projekts wird geändert.

## Anhang A — Stücke (wörtlich)

Reihenfolge wie beim Einfügen. Das Werkzeug liest je Stück die Kopfzeile, die Felder `Zieldatei`, `Art`, `Form`, `Anker` und den Text zwischen den beiden Zeilen `~~~`. Die Zeile „Am HEAD“ ist Auskunft: Ankerzeile und Zeilenbilanz aus der Simulation, die Quelle aus der Stückliste des steuernden Chats (dort meinen Zeilen der UEBERGABE den Arbeitsbaum vom 09.10.2026, 21:32, alle anderen Dateien den HEAD).

#### R01 — Abschnitt 0, „Immer“: Uhrzeiten in Helferaufträgen (Fehler Nr. 34)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Uhrzeiten mit `date` messen, im selben Schritt⟧

Am HEAD: Anker Z. 44 · eingefügt +1 · Quelle: UEBERGABE Z. 2672 (lang), Z. 2724 (Umzug 19:49, Block 7 Nr. 34)

~~~
| ☐ | Zusatz zur Zeile darüber: Uhrzeiten in Helferaufträgen setzt das Skript ein, das den Auftrag schreibt, oder es steht die Spanne zweier Messungen (09.10.2026, Fehler Nr. 34: im Helferauftrag BESTAND137 stand „gemessen 09.10.2026, 18:05“, geschrieben um 18:04 ohne Messung) | UEBERGABE, Nachtrag 09.10.2026, 18:48; Umzug 09.10.2026, 19:49, Block 7 Nr. 34 |
~~~

#### R02 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Kennung einer Fable-Anfrage = Tag des Ausgebens

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Beim Ausgeben einer Anfrage spät am Tag den Betreiber fragen⟧

Am HEAD: Anker Z. 97 · eingefügt +1 · Quelle: UEBERGABE Z. 2786 (Nachtrag 20:58), Z. 2826 (Umzug 21:06, Block 6)

~~~
| ☐ | Zusatz zur Zeile darüber: Die Kennung einer Fable-Anfrage ist der Tag des Ausgebens; die Antwort darf später kommen (Vorgabe des steuernden Chats, vorläufig; 09.10.2026: Kennung 09.10.a, wie bei 06.10.a) | UEBERGABE, Nachtrag 09.10.2026, 20:58; Umzug 09.10.2026, 21:06, Block 6 |
~~~

#### R03 — Abschnitt 0, „Arbeitsabschnitt endet“: Verweis auf W8 an der Zeile „Umgezogen wird nur …“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Umgezogen wird nur, wenn der Betreiber es sagt oder genehmigt. Der steuernde Chat zieht nicht von sich aus um⟧

Am HEAD: Anker Z. 112 · eingefügt +1 · Quelle: UEBERGABE Z. 2670 (Nachtrag 18:48), Z. 2711; W8-Wortlaut ARBEITSWEISE Z. 132

~~~
| ☐ | Zusatz zur Zeile darüber: Neben „fragt per Karte und arbeitet weiter“ steht W8 (Gruppe „Wenn eine Entscheidung beim Betreiber liegt“): Eine offene Karte hält den Chat technisch an — vor der Karte wird alles Unabhängige angestossen (Vorgabe des steuernden Chats, vorläufig; 09.10.2026: Formhinweis aus TB-141, „W8 lässt ARBEITSWEISE Z. 97 stehen“) | 13; UEBERGABE, Nachtrag 09.10.2026, 18:48 |
~~~

#### R04 — Abschnitt 0, „Arbeitsabschnitt endet“: Eröffnung als Datei in der Ablage, kurzer Text im Chat

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦der Eröffnungstext als ERSTE Nachricht im laufenden Chat, als eigener Kopierblock⟧

Am HEAD: Anker Z. 114 · eingefügt +1 · Quelle: UEBERGABE Z. 2769, 2770, 2777 (Nachtrag 19:56)

~~~
| ☐ | Zusatz zur Zeile darüber: Der Eröffnungstext liegt als Datei `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` in der Projektablage — fester Dateiname, der alte Chat ersetzt die Datei bei jedem Umzug; der Betreiber bekommt nur den kurzen Text, in dem allein der Stand wechselt — der kurze Text bleibt die erste Nachricht (Betreiber 09.10.2026, 19:55: „wäre es nicht besser du würdest eine übergabedatei ablegen und mir einen kürzeren übergabe txt schreiben damit der neue chat sich diese datei holt?“; Vorgabe des steuernden Chats, vorläufig) | UMZUG 6; UEBERGABE, Nachtrag 09.10.2026, 19:56 |
~~~

#### R05 — Abschnitt 0, „Entscheidung beim Betreiber“: vor „gedeckt von“ den Wortlaut der Karte lesen (Fehler Nr. 33)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Eine Betreiberregel geht einer Vorgabe des steuernden Chats vor; hält der steuernde Chat⟧

Am HEAD: Anker Z. 133 · eingefügt +1 · Quelle: UEBERGABE Z. 2604 (Umzug 14:44, Block 7 Nr. 33), Z. 2567

~~~
| ☐ | Vor „gedeckt von“ den Wortlaut der Karte lesen (09.10.2026, Fehler Nr. 33: „gedeckt von der Karte 12:53“ für vier Fenster geschrieben; 21627 stand nicht auf der Karte) | UEBERGABE, Umzug 09.10.2026, 14:44, Block 7 Nr. 33 |
~~~

#### R06 — Abschnitt 0, „Wenn ich den Betreiber anleite“: Dateien aus Cloud-Sitzungen selbst holen, Weg, Fehler Nr. 35 und 36

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Aufgaben am Mac in einfacher Sprache, ein Handgriff je Schritt⟧

Am HEAD: Anker Z. 147 · eingefügt +4 · Quelle: UEBERGABE Z. 2678, 2679, 2680 (Nachtrag 19:38); Z. 2725, 2726, 2727 (Umzug 19:49, Block 7)

~~~
| ☐ | Dateien aus Cloud-Sitzungen holt der steuernde Chat selbst; das Einfügen ist keine Aufgabe an den Betreiber mehr (Betreiber 09.10.2026, 19:21: „Wieso sollte ich irgendwelche dateien holen. Suche sie selbst“ — auf die Aufgabe „Gesamtergebnis TB-137 einfügen“; Lesart des steuernden Chats, vorläufig: gilt für jede Datei, die der Chat über Browser oder Geräteanbindung selbst erreichen kann) | UEBERGABE, Nachtrag 09.10.2026, 19:38 |
| ☐ | Weg für Dateien aus Cloud-Sitzungen: `claude.ai/code` im Browser der Claude-App, Sitzung über ihren Link in der Liste öffnen, Datei-Link `/api/organizations/…/files/<Datei-ID>/contents`; Bytes und sha256 per Skript im Browser messen, ohne den Inhalt in den Chat zu holen; `device_commit_files` mit `fileUuid` = Datei-ID nach `logs/steuernder_chat/`; sha256 auf dem Gerät vergleichen. Ein Download im Browserfenster kommt nicht in „Downloads“ an (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 19:49, Block 7 |
| ☐ | Zuerst den Weg über die Datei-ID versuchen; eine Freigabe erst anfordern, wenn feststeht, dass sie gebraucht wird (09.10.2026, Fehler Nr. 35: Freigabe für „Downloads“ angefordert, bevor feststand, dass sie gebraucht wird — erteilt, nicht gebraucht) | UEBERGABE, Nachtrag 09.10.2026, 19:38; Umzug 09.10.2026, 19:49, Block 7 Nr. 35 |
| ☐ | Vor einer Aufgabe an den Betreiber jeden eigenen Weg versuchen (Geräteanbindung, Browser der Claude-App, Datei-ID) (09.10.2026, Fehler Nr. 36: zweimal „Gesamtergebnis TB-137 einfügen“ als Aufgabe gegeben; geprüft war nur `ListAgents`, nicht der Browser) | UEBERGABE, Umzug 09.10.2026, 19:49, Block 7 Nr. 36 |
~~~

#### R07 — Abschnitt 0, „Dateien abgelegt“: Ausnahme zu T5 für die Eröffnungsdatei

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦In der Ablage liegt von der Übergabe nur `UEBERGABE.md`; `UEBERGABE_ARCHIV.md`⟧

Am HEAD: Anker Z. 202 · eingefügt +1 · Quelle: UEBERGABE Z. 2770, 2777 (Nachtrag 19:56)

~~~
| ☐ | Ausnahme zur Zeile darüber: In der Ablage liegt auch `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` — in der Ablage und nicht nur im Repo, weil der neue Chat sie lesen muss, bevor die Freigabe für `~/trading-bot` steht; fester Dateiname, bei jedem Umzug ersetzt (09.10.2026, Wort des Betreibers von 19:55 in der Gruppe „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“; Vorgabe des steuernden Chats, vorläufig) | UEBERGABE, Nachtrag 09.10.2026, 19:56 |
~~~

#### R08 — Abschnitt 0, „Dateien abgelegt“: Ampel nach jedem Helferblock, Entwürfe nur an den Entscheidungsstellen, `project_info` über einen Helfer (Fehler Nr. 37)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Vor jedem Lesen in den Chat die Bytes messen und mit ÷ 1,6 gegen die Ampel rechnen⟧

Am HEAD: Anker Z. 209 · eingefügt +1 · Quelle: UEBERGABE Z. 2793 (Nachtrag 20:58), Z. 2829 (Umzug 21:06, Block 7 Nr. 37)

~~~
| ☐ | Zusatz zur Zeile darüber: Nach jedem Helferblock die Ampel messen; Bausteine eines Entwurfs liest der steuernde Chat nur an den Stellen, an denen er entscheidet (Platzhalter per Skript herausziehen); `project_info` über einen Helfer (09.10.2026, Fehler Nr. 37: die Ampel nur zweimal gemessen — Verlauf 46 702 nach Schritt 6, 259 994 nach Schritt 37) | UEBERGABE, Nachtrag 09.10.2026, 20:58; Umzug 09.10.2026, 21:06, Block 7 Nr. 37 |
~~~

#### R09 — Abschnitt 0, „Dateien abgelegt“: eine einzelne Datei legt der steuernde Chat selbst ab

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Die Erneuerung der Ablage (Abschnittsdateien, Index, Dialog-Index) macht ein Helfer⟧

Am HEAD: Anker Z. 211 · eingefügt +1 · Quelle: UEBERGABE Z. 2729 (Umzug 19:49, Block 7)

~~~
| ☐ | Geht der Zeile darüber vor, soweit es um eine einzelne Datei geht: Eine einzelne Datei legt der steuernde Chat selbst ab (Stage, Kopie, md5 gegen Gerät, ein `project_write` mit `local_path`); mehrere Dateien bleiben beim Helfer (Vorgabe des steuernden Chats, vorläufig; 09.10.2026: Ein Helfer kostet dafür rund 100 000 Helfer-Tokens, die Quittung im Chat ist eine Zeile) | UEBERGABE, Umzug 09.10.2026, 19:49, Block 7 |
~~~

#### R10 — Abschnitt 0, „Auftrag schreiben“: Cloud-Sitzungen — Leseaufgaben mit Textantwort (Paket 15, P3; Lesart)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Folgeauftrag gleicher Bauart: auf den Vorgänger verweisen⟧

Am HEAD: Anker Z. 262 · eingefügt +1 · Quelle: GESAMTERGEBNIS_CLOUD_TB-137.md Z. 846 (P3); UEBERGABE Z. 948, 981, 994; BACKLOG Z. 303; UEBERGABE Z. 948 (Fundstellenliste, Stichproben)

~~~
| ☐ | Cloud-Sitzungen von Claude Code: von Hand angelegt, Aufgabe als Kopierblock, Antwort als Textdatei im dortigen Chat, nichts wird abgelegt (Betreiber 04.10.2026, 09:55, in der Fassung der UEBERGABE). Lesart des steuernden Chats, vorläufig: nur Leseaufgaben mit Textantwort; die Antwort ist Fundstellenliste, kein Nachweis, und wird an Stichproben gemessen; die Zeile geht Abschnitt 1 und 2 vor, soweit jene der Cloud-Sitzung Zweig und PR zuschreiben (Entwurf: TB-137, Paket 15, P3). Die Antwortdatei holt der steuernde Chat selbst (Betreiber 09.10.2026, 19:21; löst „der Betreiber kopiert die Antwort in den steuernden Chat“ vom 04.10.2026 ab) | UEBERGABE, Nachtrag 04.10.2026, 10:03; Umzug 04.10.2026, 10:56, Block 4 und Block 6; Nachtrag 09.10.2026, 19:38 |
~~~

#### R12 — Abschnitt 0, „Auftrag schreiben“: Helfer ohne Gerät — Wiederholungen mit Pause, Rest als Teilmessung

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Helfer schreiben den Bericht nach jeder Prüfung fort und versuchen dreimal neu⟧

Am HEAD: Anker Z. 294 · eingefügt +1 · Quelle: UEBERGABE Z. 2728 (Umzug 19:49, Block 7)

~~~
| ☐ | Zusatz zur Zeile darüber: Wiederholungen mit Pause; was fehlt, misst der steuernde Chat als ein Skript nach und nennt es Teilmessung (09.10.2026: ABNAHME137 verlor nach 18 Aufrufen die Anbindung, viermal „device not connected“ in Folge) | UEBERGABE, Umzug 09.10.2026, 19:49, Block 7 |
~~~

#### R11 — Abschnitt 0, „Auftrag schreiben“: Helfer-Skripte als Datei („spawn E2BIG“); Suche auf benannte Dateien

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Vorprobe als eigener kleiner Auftrag vor dem grossen⟧

Am HEAD: Anker Z. 296 · eingefügt +2 · Quelle: UEBERGABE Z. 2830, 2832 (Umzug 21:06, Block 7), Z. 2784, 2785 (Nachtrag 20:58)

~~~
| ☐ | Helfer schreiben lange Skripte als Datei und rufen sie dann auf (09.10.2026: Helfer FABLE2_B scheiterte einmal an „spawn E2BIG“, Befehl zu lang) | UEBERGABE, Umzug 09.10.2026, 21:06, Block 7 |
| ☐ | Im Helferauftrag die Suche auf benannte Dateien begrenzen (09.10.2026: GEGEN2 suchte mit `grep -l` über `docs/projektfuehrung/*.md` und damit über `BACKLOG*.md`, nur Dateinamen) | UEBERGABE, Umzug 09.10.2026, 21:06, Block 7; Nachtrag 09.10.2026, 20:58 |
~~~

#### U1 — UMZUG.md, Abschnitt 6: Eröffnung als Datei, kurzer Text als Kopierblock

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦## 6. Der Eröffnungstext — die einzige Fassung⟧

Am HEAD: Anker Z. 258 · eingefügt +10 · Quelle: UEBERGABE Z. 2769–2778 (Nachtrag 19:56), Z. 2832, 2838 (Umzug 21:06, Block 7 und 9); logs/steuernder_chat/2026-10-09_EROEFFNUNG_8_kurz.txt

~~~
⭐ **Gilt seit 09.10.2026 (eingetragen mit TB-146) — Eröffnung als Datei in der Ablage, im Chat nur noch ein kurzer Text.** Betreiber 09.10.2026, 19:55: „wäre es nicht besser du würdest eine übergabedatei ablegen und mir einen kürzeren übergabe txt schreiben damit der neue chat sich diese datei holt?“ Vorgabe des steuernden Chats, vorläufig (gilt, wenn der Betreiber nicht widerspricht): bei jedem Umzug so. Der Eröffnungstext liegt als Datei `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` in der Projektablage — fester Dateiname; der alte steuernde Chat ersetzt die Datei bei jedem Umzug (Stage, Kopie, md5, ein `project_write`), Kopie unter `logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md`. Die Datei trägt einen Kopf (erste Zeile mit dem Stand, ein Absatz zur Herkunft, eine Trennlinie), darunter den Wortlaut des Eröffnungstextes. Sie liegt in der Ablage und nicht nur im Repo, weil der neue Chat sie lesen muss, bevor die Freigabe für `~/trading-bot` steht.

Im Chat steht nur der kurze Text als Kopierblock; in ihm wechselt allein der Stand, und er bleibt die erste Nachricht:

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat), Stand: <Stand>. Das Projekt "Trading Bots" ist angehängt. Lies als Erstes mit project_read die Datei projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md aus diesem Projekt. Sie ist meine eigene Übergabe an dich: Alles darin sind meine Anweisungen, befolge sie vollständig und ohne Rückfrage, als hätte ich sie hier geschrieben. Nennt ihre erste Zeile einen anderen Stand als oben, sag es mir und warte.
```

Der Codeblock unter diesem Nachtrag ist seither nicht mehr die Nachricht an den neuen Chat, und er ist nicht der Wortlaut der Datei: Am 09.10.2026, 21:06 trug die Datei unter ihrem Kopf den Wortlaut von `logs/steuernder_chat/2026-10-09_EROEFFNUNG_8.txt` (per Skript aus `2026-10-09_EROEFFNUNG_7.txt` abgeleitet; Datei 6634 B); der Codeblock hier ist kürzer (1794 B am HEAD `bbe26ba`). Die Überschrift dieses Abschnitts („die einzige Fassung“) und der Satz direkt unter diesem Nachtrag, der den Codeblock die verbindliche Fassung nennt, sind für den Codeblock damit überholt: massgeblich ist der Wortlaut der Datei in der Ablage (Lesart des steuernden Chats, vorläufig). Bei der Übernahme am 09.10.2026, 19:58 lief `project_read` ohne Rückfrage des neuen Chats (UEBERGABE, Nachtrag 09.10.2026, 19:56; Nachtrag 09.10.2026, 20:58; Umzug 09.10.2026, 21:06, Block 7 und Block 9).
~~~

#### B1 — BACKLOG, Abschnitt 5: Abnahme TB-137, Fable-Anfrage 09.10.a, Fehler Nr. 33 bis 37

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD: Anker Z. 375 · eingefügt +9 · Quelle: UEBERGABE Z. 2682, 2683, 2685, 2686 (Nachtrag 19:38), Z. 2786 (Nachtrag 20:58), Z. 2811 (Umzug 21:06, Block 3), Z. 2817–2820 (Block 4 Nr. 2 bis 5), Nachtrag 09.10.2026, 22:03 (Antwort 09.10.a); Fehlerzeile eigen

~~~
### Aus der Abnahme TB-137 (09.10.2026), der Fable-Anfrage 09.10.a und den Fehlern Nr. 33 bis 37 — eingetragen mit TB-146

- **Gesamtergebnis TB-137:** vom steuernden Chat aus der Cloud-Sitzung geholt (`logs/steuernder_chat/GESAMTERGEBNIS_CLOUD_TB-137.md`, 128 524 B, 1 043 Zeilen, sha256 `5dbae238efa2682a9ca0330d080d69bfb6417fd462ddf4a87b563306013f167b`, von git ignoriert; laut Kopf Commit `d781f1b`, Register 11 471 Zeilen, 19 Übersichtszeilen (0–18), alle „fertig“) und an Stichproben abgenommen — **Teilmessung**. Aussagen des Helfers ABNAHME137: Stichprobe 1 Kopf 3 von 3; 2 (Paket 1 gegen c1) 27 von 27; 3 (Paket 2) 25 von 25; 4 (Paket 3) 23 von 23; 5 (Paket 5) 11 Orte geprüft; 6 (Paket 11) 27 von 27; 7 (quer) 12 von 12; Stichprobe 8 (Sichtschutz) vom steuernden Chat selbst. Urteil: keine Abweichung in einer gemessenen Zählung, vier ungenaue Fundstellen. Nicht gemessen unter anderem: Pakete 6, 9, 13, 14, 16, 17, 18; in Paket 5 die übrigen 7 von 18 Orten; die ganze Liste steht in der UEBERGABE, Nachtrag 09.10.2026, 19:38. Fundstellenlisten sind kein Nachweis: Was aus dem Ergebnis in Registertext, eine Fable-Anfrage oder einen Auftrag geht, wird vorher an der Quelle am HEAD nachgemessen (Zeilennummern des Ergebnisses gelten an `d781f1b`) (UEBERGABE, Nachtrag 09.10.2026, 19:38).
- **Fable-Anfrage 09.10.a:** `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-09a_kern_marken_listen_handelbar_tag.md` (43945 B, md5 `284049b082e380851257445072251af6`): sechs Fragen, 14 Kenntniszeilen, elf Posten (54.6 Nr. 2, 6, 7, 9, 10; 55.8 Nr. 5, 6, 9, 10, 12, 13); Eröffnung für Fable `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-09_eroeffnung.md` (7077 B, md5 `9973d83825dba26092712f28e86e7981`). Ausgegeben 09.10.2026 (UEBERGABE, Nachtrag 09.10.2026, 20:58). **Antwort eingegangen:** `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` (52 721 B, md5 `a6e5d3d277c5d4069b443a8f8f9df17f`; in der Ablage seit 09.10.2026, 21:35; Betreiber 21:36: „fable fertig“), über zwei gleiche Abschriften ins Repo gelegt; Registerblock R84 bis R89; **noch nicht bewertet** (UEBERGABE, Nachtrag 09.10.2026, 22:03).
- **Fehler Nr. 33 bis 37:** Regeln in `ARBEITSWEISE.md` Abschnitt 0, eingetragen mit TB-146 (UEBERGABE: Umzug 09.10.2026, 14:44, Block 7 Nr. 33; Nachträge 09.10.2026, 18:48 und 19:38 und Umzug 09.10.2026, 19:49, Block 7 zu Nr. 34 bis 36; Nachtrag 09.10.2026, 20:58 und Umzug 09.10.2026, 21:06, Block 7 zu Nr. 37). Die Regel zu Nr. 32 steht dort seit TB-145 (Zeile „Kleine Berichtigungen …“).
- **Cloud-Sitzungen:** Der Punkt „Cloud-Sitzungen, Regel noch nicht gefasst“ in diesem BACKLOG ist mit TB-146 als Zeile in `ARBEITSWEISE.md` Abschnitt 0, Gruppe „Wenn ich einen Auftrag schreibe“, gefasst — das „nur“ und der Vorrang vor Abschnitt 1 und 2 als Lesart des steuernden Chats, vorläufig (Betreiber 04.10.2026, 09:55; Entwurf aus TB-137, Paket 15, P3); offen bleibt das Verhältnis zur Zeile „Ein Befund aus einem angeleiteten Lauf …“ in Abschnitt 0, die für den Beleg unter `docs/belege/` noch die Cloud-Sitzung nennt.
- **Offen** (UEBERGABE, Umzug 09.10.2026, 21:06, Block 4 Nr. 2 bis 5; Nachtrag 09.10.2026, 22:03): die Antwort 09.10.a von Fable bewerten — Nummern am Block zählen, jede Aussage gegen das Repo (der Chat, der bewertet, baut nicht den Registerauftrag); danach der Registerauftrag, mit ihm die Zeile 09a im Dialog-Index; die Messbitte aus 55.8 Nr. 5 (Lesen an `shared/zuteilung.py`: Schlüssel, Zeitzone) als eigener Auftrag vor dem Bau des Schnitts im Zellen-Erzeuger; später, je eigener Auftrag: `PLAN_VOR_DEM_TAG.md` nachziehen (Paket 8), Einstiegsdokumente (Paket 17), Übergabe kürzen (Paket 16), Index (Paket 18); Bauauftrag Zellen-Erzeuger erst nach Fable; Blick ins Fenster (Umzug 09.10.2026, 14:44, Block 4 Nr. 5) nicht versucht.
- **Nicht in TB-146** (Gründe im Auftrag `docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md`, Abschnitt „Nicht in TB-146“): die Formhinweise Nr. 9 bis 11 aus TB-141; die Soll-Liste in `docs/werkzeuge/ablage_soll.py` für die Eröffnungsdatei — zuerst ist zu entscheiden, wo die Datei im Repo liegt; die Zeile 09a im Dialog-Index.
~~~

#### J1 — JOURNAL: erste Zeile des Nachtrags im neuen Block der Sitzung (erwartete Kennung EM)

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

Kein Anker: `WZ journal` setzt die Zeile und dahinter die 6 Zeilen `- **…` aus B1 vor `### Was gemessen ist` des Blocks. Quelle: Vorbild tb145/stuecke/J1.txt; JOURNAL Z. 10297 (Block EL), Z. 10326 (nächste Kennung EM)

~~~
**Nachtrag des steuernden Chats zum Stand vor TB-146, wie in `BACKLOG.md` Abschnitt 5 eingetragen (aus `UEBERGABE.md`, Nachträge 09.10.2026, 19:38, 20:58 und 22:03 und Umzug 09.10.2026, 21:06, Block 4; dazu die Zeilen zu den Fehlern Nr. 33 bis 37, zu den Cloud-Sitzungen und zu „Nicht in TB-146“):**
~~~

## Anhang B — Werkzeug und Sollwerte

### Werkzeug

sha256 des ausgelesenen Texts (mit abschliessendem Zeilenende): `09d57b7a8befc5a067210f62b2f378fb3f1334f90ddbaf318b2d27f20bd7660e`.

```python
#!/usr/bin/env python3
# tb146_einfuegen.py - Werkzeug zum Auftrag TB-146, ausgelesen aus Anhang B.
# Abgeleitet von tb145_einfuegen.py (TB-145, Anhang B), ohne Direktiven: jedes Stueck
# steht woertlich im Auftrag. Liest Stuecke, Anker und Texte aus dem Auftrag,
# prueft alles, bevor es schreibt, weist einen zweiten Lauf ab und schreibt nur die
# vier Zieldateien (an Ort und Stelle, mit Ruecklesen; keine Hilfsdatei daneben).
# Die Ausgabe geht nach stdout; die Sitzung leitet sie in den Beleg um.
# Aufruf aus der Repo-Wurzel mit trading-env/bin/python3 -B:
#   probe                                nur lesen
#   einfuegen                            alle Stuecke ausser J1
#   vergleich                            jedes Stueck zeichengleich, genau einmal
#   numstat <von> <bis> [<Blockdatei>]   git diff --numstat gegen die Sollwerte
#   journal <Blockdatei> [--probe]       Block der Sitzung samt J1
# rc 0 wie Soll · rc 1 Abweichung, nichts geschrieben · rc 2 abgewiesen (zweiter Lauf
# oder Bedingung verletzt), nichts geschrieben · rc 3 Abbruch vor dem Schreiben.
import json, re, subprocess, sys

P, A = "docs/projektfuehrung/", "docs/auftraege/"
AUF = A + "MAC_TB-146_regelwerk_dokunachtrag_0910.md"
JOU, BACK = P + "JOURNAL.md", P + "BACKLOG.md"
ZIELE = (P + "ARBEITSWEISE.md", P + "UMZUG.md", BACK, JOU)
FREI = ("docs/belege/TB-146/", "docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md")
ZAUN, KL, KR = "~" * 3, "⟦", "⟧"


def zeilen(p):
    with open(p, encoding="utf-8") as f:
        t = f.read()
    assert t.endswith("\n"), p + ": kein Zeilenende am Schluss"
    return t[:-1].split("\n")


def soll():
    z = zeilen(AUF)
    a = z.index("```json", z.index("### Sollwerte (maschinenlesbar)"))
    return json.loads("\n".join(z[a + 1:z.index("```", a + 1)]))


def stuecke():
    # Kopf '#### <Id> — …', Felder, dann der Text zwischen zwei Tilde-Zaeunen
    z, aus, i = zeilen(AUF), {}, 0
    while i < len(z):
        m = re.match(r"#### ([A-Z]\d+) — ", z[i])
        i += 1
        if not m:
            continue
        s = {"id": m.group(1), "zie": "", "art": "", "for": "", "ank": ""}
        while z[i] != ZAUN:
            for name in ("Zieldatei", "Art", "Form", "Anker"):
                if z[i].startswith(name + ": "):
                    v = z[i][len(name) + 2:]
                    if name == "Anker":
                        assert v[0] == KL and v[-1] == KR, s["id"] + ": Anker ohne Klammern"
                    s[name[:3].lower()] = v.strip("`") if name == "Zieldatei" else v[1:-1] if name == "Anker" else v
            i += 1
        j = z.index(ZAUN, i + 1)
        s["text"] = z[i + 1:j]
        assert s["text"] and s["zie"] in ZIELE and s["id"] not in aus, s["id"] + ": Stueck unvollstaendig oder keine Zieldatei"
        assert s["id"] == "J1" or (s["art"] in ("nach", "vor") and s["for"] in ("Zeilen", "Block") and s["ank"]), s["id"] + ": Felder"
        aus[s["id"]] = s
        i = j + 1
    assert list(aus) == soll()["stuecke"], "Stuecke nicht wie Soll gelesen: " + " ".join(aus)
    return aus


def fertig(s):
    # der Text eines Stuecks, wie er im Auftrag steht (TB-146 hat keine Direktiven)
    for x in s["text"]:
        assert KL not in x, s["id"] + ": Klammer im Text"
    return list(s["text"])


def vorkommen(zl, text):
    return [k for k in range(len(zl) - len(text) + 1) if zl[k:k + len(text)] == text]


def plan():
    # prueft jedes Stueck an den Dateien, wie sie liegen, und setzt im Speicher ein; schreibt nichts
    st = [s for s in stuecke().values() if s["id"] != "J1"]
    texte = dict((s["id"], fertig(s)) for s in st)
    vor = dict((p, zeilen(p)) for p in sorted(set(s["zie"] for s in st)))
    neu, aus, schon, gut, so = dict((p, list(vor[p])) for p in vor), [], [], True, soll()["numstat"]
    for s in st:
        p, text = s["zie"], texte[s["id"]]
        u = [k for k, x in enumerate(vor[p]) if s["ank"] in x]
        da = sum(1 for x in vor[p] if x == text[0])
        fremd = sum(1 for t in st if t["zie"] == p for x in texte[t["id"]] if s["ank"] in x)
        ok, tab, plus = len(u) == 1 and da == 0 and fremd == 0, "–", 0
        if da:
            schon.append(s["id"])
        if ok:
            zl = neu[p]
            a = [k for k, x in enumerate(zl) if s["ank"] in x][0]
            k, ein = (a + 1 if s["art"] == "nach" else a), list(text)
            davor, danach = (zl[k - 1] if k > 0 else ""), (zl[k] if k < len(zl) else "")
            if s["for"] == "Block":  # genau eine Leerzeile davor und danach, keine verdoppelt
                ein = ([""] if davor != "" else []) + ein + ([""] if danach != "" else [])
            elif text[0].startswith("|"):  # Tabellenzeile: nur hinter eine Tabellenzeile
                tab = "ja" if all(x.startswith("|") for x in text) and davor.startswith("|") else "NEIN"
            else:  # keine Tabellenzeile: nicht mitten in eine Tabelle
                tab = "NEIN" if davor.startswith("|") and danach.startswith("|") else "–"
            ok, plus = tab != "NEIN", len(ein)
            if ok:
                neu[p] = zl[:k] + ein + zl[k:]
        gut = gut and ok
        aus.append("%s · %s · Anker Z. %s · %s · %s · Textzeilen %d · erste Zeile schon %d · Anker in neuen Texten %d · Tabelle %s · Zeilen +%d · %s"
                   % (s["id"], p, u[0] + 1 if len(u) == 1 else "%d Treffer" % len(u), s["art"], s["for"], len(text), da, fremd, tab, plus, "ok" if ok else "ABWEICHUNG"))
    if gut:
        for s in st:
            n = len(vorkommen(neu[s["zie"]], texte[s["id"]]))
            if n != 1:
                gut = False
                aus.append("%s · Text nach dem Einsetzen %d-mal statt 1 · ABWEICHUNG" % (s["id"], n))
    for p in sorted(vor):
        d, w = len(neu[p]) - len(vor[p]), so.get(p, [None])[0]
        gut = gut and d == w
        aus.append("Datei %s · Zeilen vorher %d · nachher %d · +%d · Soll +%s · %s" % (p, len(vor[p]), len(neu[p]), d, w, "gleich" if d == w else "ABWEICHUNG"))
    if sorted(vor) != sorted(so):
        gut = False
        aus.append("Zieldateien der Stuecke ungleich den Sollwerten · ABWEICHUNG")
    aus.append("Stuecke %d · eingefuegte Zeilen %d" % (len(st), sum(len(neu[p]) - len(vor[p]) for p in vor)))
    return gut, schon, aus, vor, neu, st, texte


def einfuegen(probe):
    print("# TB-146 %s — Stuecke aus Anhang A%s" % ("probe" if probe else "einfuegen", " (nur gelesen)" if probe else ""))
    gut, schon, aus, vor, neu, st, texte = plan()
    print("\n".join(aus))
    if schon and not probe:
        print("ABGEWIESEN, nichts geschrieben: erste Zeile steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    if not gut:
        print("Gesamt: ABWEICHUNG, nichts geschrieben")
        return 1
    if not probe:
        for p in sorted(vor):
            assert p in ZIELE and p != JOU, p + " ist hier keine Zieldatei"
            t = "\n".join(neu[p]) + "\n"
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
            with open(p, encoding="utf-8") as f:
                assert f.read() == t, p + ": Ruecklesen ungleich (GESCHRIEBEN, Stand pruefen)"
            print("geschrieben und zurueckgelesen: " + p)
    print("Gesamt: wie Soll, " + ("nichts geschrieben (Probe)" if probe else "alle eingefuegt, je genau einmal"))
    return 0


def vergleich():
    print("# TB-146 vergleich — jedes Stueck zeichengleich und genau einmal in seiner Zieldatei")
    gut = True
    for s in stuecke().values():
        if s["id"] == "J1":
            continue
        zl, text = zeilen(s["zie"]), fertig(s)
        v = vorkommen(zl, text)
        ok = len(v) == 1
        if ok and s["for"] == "Block":
            k, e = v[0], v[0] + len(text)
            ok = (k == 0 or zl[k - 1] == "") and (e == len(zl) or zl[e] == "")
        gut = gut and ok
        print("%s · %s · %d Bytes · %d Zeile(n) · Vorkommen %d · %s" % (s["id"], s["zie"], len("\n".join(text).encode("utf-8")), len(text), len(v), "GLEICH" if ok else "ABWEICHUNG"))
    print("Gesamt: " + ("alle zeichengleich, je genau einmal" if gut else "ABWEICHUNG"))
    return 0 if gut else 1


def numstat(von, bis, block):
    print("# TB-146 numstat — git diff --numstat %s %s gegen die Sollwerte" % (von, bis))
    roh = subprocess.run(["git", "diff", "--numstat", von, bis], capture_output=True, universal_newlines=True, check=True).stdout
    so, ist, gut = dict((p, list(v)) for p, v in soll()["numstat"].items()), {}, True
    if block:
        so[JOU] = [len(zeilen(block)) + soll()["j1_zeilen"] + 4, 0]
    for x in roh.splitlines():
        print("roh: " + x)
        a, b, p = x.split("\t")
        ist[p] = [int(a) if a.isdigit() else a, int(b) if b.isdigit() else b]
    for p in sorted(so):
        ok = ist.get(p) == so[p]
        gut = gut and ok
        print("Soll %s %d\t%d · Ist %s · %s" % (p, so[p][0], so[p][1], ist.get(p), "gleich" if ok else "ABWEICHUNG"))
    fremd = sorted(p for p in ist if p not in so and not p.startswith(FREI[0]) and p != FREI[1])
    print("weitere Dateien ausser Belegen und Ergebnis: " + (" ".join(fremd) if fremd else "keine"))
    gut = gut and not fremd
    print("Gesamt: " + ("wie Soll, keine entfernte Zeile in den Zieldateien" if gut else "ABWEICHUNG"))
    return 0 if gut else 1


def journal(blockpfad, probe):
    print("# TB-146 journal%s — Block der Sitzung samt J1 vor '## Wiederkehrende Lehren'" % (" (Probe)" if probe else ""))
    st, so = stuecke(), soll()
    zl, b, b1 = zeilen(JOU), zeilen(blockpfad), fertig(st["B1"])
    j1 = fertig(st["J1"]) + [x for x in b1 if x.startswith("- ")]
    k = [n for n, x in enumerate(zl) if x == "## Wiederkehrende Lehren"]
    assert len(k) == 1, "Schlussueberschrift trifft %d-mal" % len(k)
    k, was = k[0], "### Was gemessen ist"
    alt = [m.group(1) for m in (re.match(r"## ([A-Z]{2}) — ", x) for x in zl[:k]) if m][-1]
    neu = alt[0] + chr(ord(alt[1]) + 1) if alt[1] != "Z" else chr(ord(alt[0]) + 1) + "A"
    g = b.index(was) if was in b else 0
    bed = (("letzte Kennung %s, Kopfzeile beginnt mit '## %s — TB-146'" % (alt, neu), b[0].startswith("## %s — TB-146" % neu)),
           ("genau eine Zeile '%s', Leerzeile davor" % was, b.count(was) == 1 and g > 0 and b[g - 1] == ""),
           ("genau eine Zeile '### Was offen bleibt'", b.count("### Was offen bleibt") == 1),
           ("kein Trennstrich im Block, Schlusszeile beginnt mit '*Geschrieben'", "---" not in b and b[-1].startswith("*Geschrieben")),
           ("J1 weder im Journal noch im Block", j1[0] not in zl and j1[0] not in b),
           ("vor der Schlussueberschrift stehen '---' und eine Leerzeile", zl[k - 2:k] == ["---", ""]),
           ("B1 steht genau einmal im BACKLOG (Schritt E gelaufen)", len(vorkommen(zeilen(BACK), b1)) == 1),
           ("J1-Zeilen %d wie Soll %d" % (len(j1), so["j1_zeilen"]), len(j1) == so["j1_zeilen"]))
    for name, ok in bed:
        print("%s · %s" % (name, "ja" if ok else "NEIN"))
    if not all(ok for name, ok in bed):
        print("ABGEWIESEN, nichts geschrieben")
        return 2
    ein = b[:g] + j1 + [""] + b[g:] + ["", "---", ""]
    print("Kennung %s (erwartet %s) · Blockzeilen %d · J1-Zeilen %d · Zeilen +%d (= Block + J1 + 1 + 3)" % (neu, so["kennung"], len(b), len(j1), len(ein)))
    if not probe:
        t = "\n".join(zl[:k] + ein + zl[k:]) + "\n"
        with open(JOU, "w", encoding="utf-8") as f:
            f.write(t)
        with open(JOU, encoding="utf-8") as f:
            assert f.read() == t, JOU + ": Ruecklesen ungleich (GESCHRIEBEN, Stand pruefen)"
    print("Gesamt: " + ("nichts geschrieben (Probe)" if probe else "geschrieben und zurueckgelesen: " + JOU))
    return 0


def main(a):
    probe = "--probe" in a
    if a == ["probe"] or a == ["einfuegen"]:
        return einfuegen(a[0] == "probe")
    if a == ["vergleich"]:
        return vergleich()
    if a[:1] == ["numstat"] and len(a) in (3, 4):
        return numstat(a[1], a[2], a[3] if len(a) == 4 else "")
    if a[:1] == ["journal"] and len(a) in (2, 3) and (len(a) == 2 or probe):
        return journal(a[1], probe)
    print("Aufruf: probe | einfuegen | vergleich | numstat <von> <bis> [<Blockdatei>] | journal <Blockdatei> [--probe]")
    return 64


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except AssertionError as e:
        print("ABBRUCH: %s" % e)
        sys.exit(3)
```

### Sollwerte (maschinenlesbar)

```json
{
 "stuecke": [
  "R01",
  "R02",
  "R03",
  "R04",
  "R05",
  "R06",
  "R07",
  "R08",
  "R09",
  "R10",
  "R12",
  "R11",
  "U1",
  "B1",
  "J1"
 ],
 "numstat": {
  "docs/projektfuehrung/ARBEITSWEISE.md": [
   16,
   0
  ],
  "docs/projektfuehrung/BACKLOG.md": [
   9,
   0
  ],
  "docs/projektfuehrung/UMZUG.md": [
   10,
   0
  ]
 },
 "j1_zeilen": 7,
 "kennung": "EM"
}
```
