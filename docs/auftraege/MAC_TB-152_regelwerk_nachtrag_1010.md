# TB-152 Regelwerk-Nachtrag 10.10.2026 — an: Mac-Sitzung (Claude Code) — 38 Stücke, darunter der BACKLOG-Block Kerzenformationen (B7) und fünf neue Stücke vom 11.10.2026 (R22, R23, R24, R25, U4)

**Stand: Entwurf vom 11.10.2026, 10:46** (Helfer BAU152; v2 nach den Entscheiden vom 10.10.2026, 22:55: Helfer BER152; v3 nach den Entscheiden E9 bis E23 vom 11.10.2026, 01:59 und 02:19: Helfer BER152_2; v4 nach den Entscheiden E24 bis E32 vom 11.10.2026, 08:51 und E34 vom 11.10.2026, 09:10: Helfer BER152_4B; per Skript aus 38 Bausteinen und `werte.json`), gebaut ausserhalb des Repos, nur lesend am Repo; alle Einfügungen an Kopien simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht. **Gebaut am HEAD `6d700d4`. TB-151 läuft vor diesem Auftrag: Der steuernde Chat baut am HEAD nach TB-151 neu (`sh alles.sh <HEAD> <Kennung>`, dann `fuellen152.py` für das Soll von 0a und die Journal-Kennung), bevor er auslegt.**

**Sitzungstitel:** `TB-152` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `6d700d4233712dab6f57c55cca2205b57a4f842a` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-152`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-152/tb152_einfuegen.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-152/`. **Ergebnis:** `docs/ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** Die Regeln, Berichtigungen, Betreiberworte und Abnahmebefunde vom 09.10.2026, 22:03 bis zum Nachtrag 11.10.2026, 01:38 stehen im Regelwerk: 38 Stücke — 36 in drei Dateien (131 Zeilen, nur eingefügt) und zwei im Journalblock der Sitzung (der Nachtrag aus J1, dahinter die Zeilen der BACKLOG-Blöcke, dahinter J2).
**Bauart wie TB-146** (`docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md`, Ergebnis `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`), mit den Werten von hier; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen. **Anders als in TB-146:** (1) Das Werkzeug steht nicht im Auftrag; die Sitzung leitet es in 0a aus `docs/belege/TB-146/tb146_einfuegen.py` ab (Anhang B: 11 Ersetzungen, je mit Trefferzahl). (2) `BACKLOG.md` bekommt sieben Blöcke (B1 bis B7) am selben Anker, in dieser Reihenfolge. (3) Der Nachtrag im Journal besteht aus J1, den 20 Zeilen `- …` der Blöcke B1 bis B7 und den 3 Zeilen aus J2. (4) Eine Zeile (R21) geht in die Tabelle von Abschnitt 23.2, nicht in Abschnitt 0. Wie in TB-146 steht jedes Stück wörtlich in Anhang A; das Werkzeug holt keine Zeile aus `UEBERGABE.md` und liest sie nicht, gibt nach stdout aus (die Sitzung leitet in den Beleg um), prüft alle Stücke, bevor es eine Datei schreibt, und schreibt an Ort und Stelle — es legt keine Hilfsdatei an. Die Sitzung ändert kein Werkzeug und kein Programm des Repos.
**Reihenfolge:** Schritt 0 → A (Modus) → E (Einfügen, Commit) → J (Journalblock) → F (Nachweis, Ergebnis, Abgabe).

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — der Auftrag fügt nur Dokumentation ein; kein Werkzeug und kein Programm wird geändert. Am HEAD gemessen: Register `docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 10 „Die Sperrliste“ (Z. 971–1177) und die Tabelle „Die Sperrliste, Stand 18.09.2026“ in `ARBEITSWEISE.md` (Z. 1188–1197) enthalten `projektfuehrung`, `auftraege`, `ARBEITSWEISE`, `UMZUG`, `BACKLOG`, `JOURNAL`, `belege`, `ERGEBNIS` und `docs/` je 0-mal.

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | Zeilen + (numstat-Soll, entfernt 0) |
|---|---|---|
| `docs/projektfuehrung/ARBEITSWEISE.md` | R01, R02, R03, R04, R05, R06, R07, R25, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R24, R23, R22 | **43** |
| `docs/projektfuehrung/UMZUG.md` | U1, U2, U3, U4 | **47** |
| `docs/projektfuehrung/BACKLOG.md` | B1, B2, B3, B4, B5, B6, B7 | **41** |
| `docs/projektfuehrung/JOURNAL.md` | J1, J2 (Schritt J, mit dem Block der Sitzung) | Block + 24 + 1 + 3 |
| neu: `docs/belege/TB-152/…`, `docs/ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md` | Belege, Werkzeug, Ergebnis | — |

In den vier Zieldateien wird **nur eingefügt;** keine bestehende Zeile wird geändert oder entfernt. Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (die Einträge aus 0a); das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** alles unter `docs/werkzeuge/` (auch `ablage_soll.py`); `docs/projektfuehrung/FABLE_DIALOG_INDEX.md`; `UEBERGABE.md` nach Schritt 0; Register und Registerkopie; `research/`, `shared/`, `strategies/`; frühere Belegordner (`docs/belege/` ausser `TB-152/`); den Wortlaut eines Stücks umformulieren, kürzen oder zusammenlegen (Sachfehler: melden, nicht berichtigen). Nie `git add -A`, nie `git add .`; jeder Commit nennt seine Dateien mit Namen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD `6d700d4` gemessen, Helfer BAU152, BER152_2 und BER152_4B, 11.10.2026, 10:46): Ausgang der vier Zieldateien wie in 0b; im Arbeitsbaum lauten sie wie am HEAD. Letzte Journalkennung EP (`JOURNAL.md` Z. 10455); vor `## Wiederkehrende Lehren` (Z. 10479) stehen `---` und eine Leerzeile. `docs/belege/TB-146/tb146_einfuegen.py` ist verfolgt, sha256 `09d57b7a8befc5a067210f62b2f378fb3f1334f90ddbaf318b2d27f20bd7660e` (gleich dem Soll im Auftrag TB-146, Schritt 0a). Unverfolgt und nicht ignoriert (`git ls-files -o --exclude-standard`): Stand beim Start, siehe 0a — die Einträge dort setzt `fuellen152.py` aus einer Messung. `git ls-files docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`: ein Treffer.
- **Annahmen zur Reihenfolge:** TB-152 läuft nach TB-151 und vor TB-154 (Vorgabe des steuernden Chats; `UEBERGABE.md`, Nachtrag 11.10.2026, 01:38). Am Start misst `fuellen152.py` den HEAD (der Auftrag muss an ihm gebaut sein), den Arbeitsbaum (daraus das Soll von 0a) und die letzte Journal-Kennung am HEAD (erwartet wird die nächste: EQ). Weitere Annahmen trägt dieser Absatz nicht. Kein Anker dieses Auftrags hängt am Dateiende von `BACKLOG.md` oder `JOURNAL.md`.
- **Vom Helfer nicht gemessen** (`git status` und `git diff` sind dem Helfer am Repo untersagt): der Arbeitsbaum. **Das Soll von 0a** (Einträge, Zahl, Pfade des Commits ⟨S0⟩) **und die erwartete Journal-Kennung** setzt `fuellen152.py` vor der Freigabe aus einer Messung; nichts davon ist fest eingetragen. Gemessen 11.10.2026, 10:47 mit `git ls-files -m`, `-d` und `-o --exclude-standard`; dazugesetzt, nicht gemessen: `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md`; Vorgemerktes (Index gegen HEAD) ist nicht gemessen. Journal: letzte Kennung am HEAD EP, erwartet EQ.
- **Offen — misst die Sitzung, nie raten:** Modus der Sitzung (Schritt A) · Stand der `UEBERGABE.md` beim Start (kein Sollwert) · Kennung des Journalblocks (erwartet EQ).
- **Simulation des Helfers** (Kopien `git show 6d700d4:<pfad>`; Linux, Python 3.10.12, das abgeleitete Werkzeug mit `ast.parse(feature_version=(3,9))` geprüft; zwei Läufe: am HEAD, wie er ist, und mit einer Attrappe für TB-151 — je ein Block am Dateiende von `BACKLOG.md`, vor dessen Abschnitt 6 und im Journal vor `## Wiederkehrende Lehren`): Ableitung mit dem Befehl aus 0a, sha256 wie Soll; `probe` rc 0, jeder Anker genau eine Zeile; `einfuegen` rc 0, geändert genau die drei Dateien; Zeilenbilanz per `diff` wie die Tabelle oben, 0 entfernte Zeilen; in `ARBEITSWEISE.md` 42 neue Tabellenzeilen mit je drei Zellen und eine mit fünf (R21), Zahl der Tabellen unverändert; in `UMZUG.md` +4 Zaunzeilen, die Zahl bleibt gerade; `vergleich` rc 0; zweiter Lauf rc 2, md5 unverändert; `journal` mit einer Attrappe als Block rc 0 (Kennung EQ am HEAD, wie er ist; ER mit der Attrappe), J1-Zeilen 24, zweiter Lauf rc 2; Gegenproben (Anker fehlt, Anker doppelt, `journal` vor `einfuegen`): nichts geschrieben. **Nicht simuliert:** `git status`, `git diff` (`numstat`), Commit und Push, Claude Code, der Sitzungswächter, Python 3.9 selbst, TB-151 selbst. Die Sitzung zählt selbst nach; ihre Zahl gilt.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-152/` entsteht:** `git status --porcelain > "$TMPDIR/tb152_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `6d700d4233712dab6f57c55cca2205b57a4f842a` und genau diese 4 Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md
```

Jeder andere oder weitere Eintrag: **ABBRUCH**.

Dann `git ls-files docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`. Soll: genau diese eine Zeile — die Datei ist seit TB-151 verfolgt, und sechs Stücke sagen das; leere Ausgabe: **ABBRUCH**, nichts ist eingefügt.

Dann `grep -c 'EROEFFNUNG_STEUERNDER_CHAT.md' docs/werkzeuge/ablage_soll.py`. Soll: mindestens 1 — R10, R21, U2 sagen, dass `ablage_soll.py` die Datei in der Liste `STAND` führt; 0 (`grep -c` endet dann mit rc 1): **ABBRUCH**, nichts ist eingefügt.

Dann das Werkzeug ableiten — aus dem Werkzeug zu TB-146, mit den Ersetzungen aus Anhang B:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md docs/belege/TB-146/tb146_einfuegen.py "$TMPDIR" <<'EOF'
import hashlib, json, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```json", z.index("### Unterschiede zum Werkzeug TB-146 (maschinenlesbar)"))
u = json.loads("\n".join(z[a + 1:z.index("```", a + 1)]))
t = open(sys.argv[2], encoding="utf-8").read()
assert hashlib.sha256(t.encode("utf-8")).hexdigest() == u["quelle_sha256"], "Werkzeug TB-146 weicht ab"
for alt, neu, n in u["ersetzungen"]:
    assert t.count(alt) == n, "Treffer %d statt %d: %s" % (t.count(alt), n, alt)
    t = t.replace(alt, neu)
open(sys.argv[3] + "/tb152_einfuegen.py", "w", encoding="utf-8").write(t)
print("tb152_einfuegen.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb152_einfuegen.py d5855393b5b138ef90b6ccfb40b5e70527a651057748c2abaa6776b6f41f70f5`; sonst **ABBRUCH**. Commit `TB-152 Schritt 0: Stand des steuernden Chats vor TB-152` mit genau den Pfaden aus 0a (jede Datei mit Namen, je Pfad eine Zeile: Block unten), pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb152_0a.txt` unverändert nach `docs/belege/TB-152/0a_status.txt` (`cmp` gleich) und das Werkzeug nach `docs/belege/TB-152/tb152_einfuegen.py` (sha256 noch einmal). **Für jede Rohausgabe gilt:** Sie bleibt roh. **Keine Kopfdateien** (`*.kopf.txt`), wie in TB-147; an ihre Stelle tritt die Tabelle „Belege“ im Ergebnis. Ausgaben von `WZ` tragen ihre Kopfzeile selbst.

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md
```

**0b. Ausgang** ⇒ `0b_ausgang.txt`: Zeilen und md5 der vier Zieldateien an ⟨S0⟩. Soll (am Bau-HEAD `6d700d4`): `ARBEITSWEISE.md` 2531 Z., `b856395e6c1df8581cf9a44ca33c441e` · `UMZUG.md` 392 Z., `017136adf27c96b861cab1357276b41c` · `BACKLOG.md` 422 Z., `1cf506eb32be6d8d217b8cff264b2f2c` · `JOURNAL.md` 10816 Z., `ec8f1995ece5136d4e8565803235afa4`. Weicht eine ab: vermerken; die Anker entscheiden (Schritt E). Dazu Zeilen und md5 von `UEBERGABE.md` an ⟨S0⟩ — **ohne Sollwert,** sie wächst bis zum Start; nach Schritt 0 ändert die Sitzung sie nicht (Schritt F misst den md5 noch einmal).

## Schritt A — Modus messen, bevor eingefügt wird

⇒ `a_modus.txt` (roh), die Aussage der Sitzung steht im Ergebnis (Tabelle „Belege“). Die eigene Sitzung:

```
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done
echo "EIGEN=$p"; ps -o command= -p "$p"
```

Soll: Die Prozesszeile trägt `--permission-mode manual`; sonst **ABBRUCH** — nichts ist eingefügt, das in der Meldung als Erstes sagen. Dazu die eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet. *Schützt:* vor einer Sitzung, die anders läuft, als der Auftrag sie voraussetzt (in TB-145 war die Prozesszeile wie Soll: `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md` Z. 14).

## Verfahren je Stück

Jedes Stück in Anhang A nennt Zieldatei, Art, Form und Anker; sein Text steht wörtlich zwischen zwei Zeilen `~~~`. **Anker:** ein Teil genau einer Zeile der Zieldatei (zwischen ⟦ und ⟧). **Art:** `nach` oder `vor` dieser Zeile. **Form `Zeilen`:** der Text ohne Leerzeile direkt an der Ankerzeile (eine Tabellenzeile bleibt in ihrer Tabelle). **Form `Block`:** genau eine Leerzeile davor und danach, keine verdoppelt. Die Grenze eines Stücks ist allein die Zeile `~~~`: U3 enthält Leerzeilen und zwei Codeblöcke mit drei Gravis — beides gehört zum Text. J1 und J2 haben keinen Anker — sie kommen mit dem Journalblock (Schritt J). B1 bis B7 haben denselben Anker; das Werkzeug setzt jeden Block vor die Ankerzeile, sie stehen danach in der Reihenfolge B1 bis B7. R24, R23 und R22 haben denselben Anker, ebenso R25 und R08; das Werkzeug setzt jedes Stück direkt hinter die Ankerzeile — danach stehen dort R22, R23, R24 und die Zeile aus R08 vor R25.

## Schritt E — Einfügen mit dem Werkzeug

**Probe.** `PY WZ probe; echo "rc $?"` ⇒ `e_probe.txt`. Soll rc 0: 36 Zeilen `<Id> · <Datei> · Anker Z. <n> · … · erste Zeile schon 0 · Anker in neuen Texten 0 · … · ok` (Ankerzeilen und Zeilen wie in Anhang A); drei Zeilen `Datei … · Soll +<n> · gleich`; `Stuecke 36 · eingefuegte Zeilen 131`; Schlusszeile `Gesamt: wie Soll, nichts geschrieben (Probe)`. rc ≠ 0 ⇒ **ABBRUCH** (rc 3: die Zeile `ABBRUCH: …` nennt den Grund; rc 64: falscher Aufruf des Werkzeugs, es hat dann nichts geprüft und nichts geschrieben).

**Einfügen.** `PY WZ einfuegen; echo "rc $?"` ⇒ `e_einfuegen.txt`. Das Werkzeug prüft alle Stücke, bevor es schreibt: Jeder Anker trifft genau eine Zeile, die erste Zeile keines Stücks steht schon da, kein Anker kommt in einem neuen Text vor, eine Tabellenzeile landet hinter einer Tabellenzeile, die Zeilenbilanz je Datei ist wie Soll. Soll rc 0: dieselben Zeilen wie in der Probe, drei Zeilen `geschrieben und zurueckgelesen: …`, Schlusszeile `Gesamt: wie Soll, alle eingefuegt, je genau einmal`. rc ≠ 0 ⇒ **ABBRUCH**; dann immer Zeilen und md5 der drei Dateien in `abbruch.txt`; nichts geschrieben ist nur belegt, wenn die Ausgabe mit `ABGEWIESEN, nichts geschrieben` oder `Gesamt: ABWEICHUNG, nichts geschrieben` endet.

**Vergleich.** `PY WZ vergleich; echo "rc $?"` ⇒ `e_vergleich.txt`. Soll rc 0: 36 Zeilen `… · Vorkommen 1 · GLEICH`, Schlusszeile `Gesamt: alle zeichengleich, je genau einmal`.

**Zweiter Lauf.** md5 der drei Dateien, dann `PY WZ einfuegen; echo "rc $?"`, dann md5 noch einmal ⇒ `e_zweitlauf.txt`. Soll rc 2, Schlusszeile `ABGEWIESEN, nichts geschrieben: …` mit allen 36 Kennungen, md5 je Datei vorher und nachher gleich.

Commit `TB-152 E: Regelwerk-Nachtrag 10.10.2026, 36 Stücke in drei Dateien` mit den drei Zieldateien und den Belegen bis hier, jede Datei mit Namen, je Pfad eine Zeile (Block unten); pushen ⇒ **⟨E⟩**.

```
git add docs/projektfuehrung/ARBEITSWEISE.md
git add docs/projektfuehrung/UMZUG.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/belege/TB-152/0a_status.txt
git add docs/belege/TB-152/tb152_einfuegen.py
git add docs/belege/TB-152/0b_ausgang.txt
git add docs/belege/TB-152/a_modus.txt
git add docs/belege/TB-152/e_probe.txt
git add docs/belege/TB-152/e_einfuegen.txt
git add docs/belege/TB-152/e_vergleich.txt
git add docs/belege/TB-152/e_zweitlauf.txt
```

**Numstat.** `PY WZ numstat ⟨S0⟩ ⟨E⟩; echo "rc $?"` ⇒ `e_numstat.txt`. Soll rc 0: die Rohzeilen von `git diff --numstat`, drei Zeilen `Soll <Datei> <n>⇥0 · Ist [<n>, 0] · gleich` (⇥ steht für einen Tabulator) mit n aus der Tabelle unter „Freigabe“, `JOURNAL.md` nicht in der Ausgabe, `weitere Dateien ausser Belegen und Ergebnis: keine`. rc 1 ⇒ melden; **keine Zeile von Hand richten.**

## Schritt J — Journalblock

Die Sitzung schreibt ihren Block nach `docs/belege/TB-152/j_block.md`, Gliederung wie Block EP (`JOURNAL.md` ab Z. 10455 am HEAD `6d700d4`): Kopfzeile `## <Kennung> — TB-152: …`, Quellenzeile, Absatz „**Quelle:**“, `### Was gemessen ist` (Leerzeile davor), `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-152. Quellenvermerk: siehe Kopf.*`; die Datei endet mit einem Zeilenende; kein `---`, nicht der Nachtrag aus J1 und J2 — was TB-152 selbst tat, schreibt die Sitzung in eigenen Worten.

`PY WZ journal docs/belege/TB-152/j_block.md --probe; echo "rc $?"` ⇒ `j_journal_probe.txt`, dann ohne `--probe` ⇒ `j_journal.txt`. Das Werkzeug misst die letzte Kennung, setzt vor `### Was gemessen ist` die Zeile J1, dahinter die 20 Zeilen aus B1 bis B7, die mit `- ` beginnen, und dahinter die 3 Zeilen aus J2 (alle wörtlich wie in Anhang A), und stellt den Block samt `---` vor `## Wiederkehrende Lehren`. Soll: acht Bedingungen `ja`, `Kennung EQ (erwartet EQ)`, `J1-Zeilen 24`, `Zeilen +<n>` mit n = Zeilen des Blocks + 24 + 1 + 3, rc 0. rc 2: die Bedingung mit `NEIN` lesen, den Block richten, neu — kein Abbruch; nennt das Werkzeug eine andere Kennung als EQ: diese nehmen und melden. rc 3: **ABBRUCH** (die Zeile `ABBRUCH: …` nennt den Grund) — ausser die Zeile `ABBRUCH: …` beginnt mit dem Pfad der Blockdatei (`docs/belege/TB-152/j_block.md`, etwa „kein Zeilenende am Schluss“): dann den Block richten und neu, kein Abbruch. rc 1, rc 64 (falscher Aufruf) oder ein Traceback (etwa: die Blockdatei fehlt): **ABBRUCH**.

## Schritt F — Nachweis, Ergebnis, Abgabe

**Nachweis.** `PY WZ vergleich; echo "rc $?"` noch einmal ⇒ `f_vergleich.txt` (Soll wie in Schritt E). Zeilen und md5 von `UEBERGABE.md` ⇒ `f_uebergabe.txt`; Soll: wie in 0b gemessen.

**Ergebnis** `docs/ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md`: Kopf (Stand, Commits, ⟨S0⟩) · **„Kurz“** (Tabelle Schritt · Soll · Ist) · **„Belege“** (Tabelle statt der Kopfdateien; Vorbild: `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md` Z. 43, dort die Spalten „Datei · Befehl · Zeilen · md5“; hier Datei · was · Befehl · Bytes · Zeilen · md5 — „was“ und „Bytes“ sind Zusatz dieses Auftrags; bei `a_modus.txt` die Aussage der Sitzung zu ihrem Modus) · **„Abweichungen vom Auftrag“** (jede, auch kleine; sonst „keine“ mit der Liste der geprüften Sollwerte) · **„Nicht getan“** (die Posten unter „Nicht in TB-152“; Aufgaben für den Betreiber) · **„In einfacher Sprache“**. Rückfragen an den Betreiber stehen samt Antwort wörtlich darin. `f_porcelain.txt` und `f_numstat.txt` entstehen erst nach dem Abgabe-Commit: In „Kurz“ steht dazu „nach der Abgabe gemessen, siehe Beleg“, die Werte nennt die Schlussmeldung.

**Abgabe.** Commit `TB-152 Abgabe: Ergebnis, Journal <Kennung>` mit `JOURNAL.md`, dem Ergebnis und den Belegen bis hier, jede Datei mit Namen, je Pfad eine Zeile (erster Block unten); pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb152_f.txt"`, unverändert nach `f_porcelain.txt` kopieren (`cmp` gleich; Soll 0 B), erst danach `PY WZ numstat ⟨S0⟩ ⟨F⟩ docs/belege/TB-152/j_block.md; echo "rc $?"` ⇒ `f_numstat.txt`. Soll rc 0: die drei Dateien wie in Schritt E, `JOURNAL.md` mit n aus Schritt J und 0 entfernten Zeilen, sonst nur Belege und Ergebnis. Kleiner letzter Commit `TB-152 F: porcelain und numstat nach der Abgabe`, die zwei Dateien mit Namen (zweiter Block unten), pushen; danach `git status --porcelain` noch einmal, Rohausgabe wörtlich in der Schlussmeldung. Die drei Dateien in `$TMPDIR` (`tb152_0a.txt`, `tb152_einfuegen.py`, `tb152_f.txt`) bleiben liegen: Die Sitzung löscht sie nicht (`deny`: `Bash(rm:*)`) und committet sie nicht.

```
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md
git add docs/belege/TB-152/e_numstat.txt
git add docs/belege/TB-152/j_block.md
git add docs/belege/TB-152/j_journal_probe.txt
git add docs/belege/TB-152/j_journal.txt
git add docs/belege/TB-152/f_vergleich.txt
git add docs/belege/TB-152/f_uebergabe.txt
```

```
git add docs/belege/TB-152/f_porcelain.txt
git add docs/belege/TB-152/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab. Ebenso in 0a: `git ls-files` nennt die Eröffnungsdatei nicht, oder `grep -c` zählt sie in `docs/werkzeuge/ablage_soll.py` 0-mal.
- Schritt A: Die Prozesszeile trägt nicht `--permission-mode manual`.
- Schritt E: `probe` oder `einfuegen` endet mit rc ≠ 0 — ein Anker hat nicht genau einen Treffer, oder die erste Zeile eines Stücks steht schon da. Das Werkzeug prüft alles, bevor es schreibt: Nach rc ≠ 0 ist keine Zieldatei geändert (die Ausnahme steht in Schritt E, „Einfügen“). Kein Stück von Hand einfügen, keinen Anker anpassen. Ebenso vor dem Commit ⟨E⟩: `vergleich` endet nicht mit rc 0, oder der zweite Lauf endet nicht mit rc 2 oder ändert einen md5.
- Schritt J: `journal` endet mit rc 3 und einer Zeile `ABBRUCH: …`, die nicht mit dem Pfad der Blockdatei beginnt, oder mit rc 1 oder rc 64.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung** (ganze Sitzung): melden, nicht umgehen. Verlangt schon Schritt 0 oder der Abbruchweg selbst (Belege committen, pushen) eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden. *Schützt:* vor einem halben Bau wie in TB-142.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch:** `journal` endet mit rc 2 oder mit rc 3 und einer Meldung, die mit dem Pfad der Blockdatei beginnt; die Kennung ist nicht EQ; 0b weicht ab; `numstat` endet mit rc 1; in F weicht `vergleich`, der md5 der `UEBERGABE.md` oder `f_porcelain.txt` ab — je weiter, unter „Abweichungen“ nennen. **Bei Abbruch:** Belege committen (je Datei eine Zeile `git add <Pfad>`, für jede Datei dieses Auftrags, die entstanden und noch nicht committet ist), Grund in `docs/belege/TB-152/abbruch.txt`, pushen, melden. Was bis dahin eingefügt ist, bleibt stehen, nichts zurückdrehen: geschriebene, noch nicht committete Zieldateien gehen mit Namen in den Abbruch-Commit; die Meldung nennt sie als Erstes. Ausnahme: Hat eine Zieldatei weniger Zeilen als am Stand ⟨S0⟩ (alle Stücke fügen nur ein), wird sie nicht committet — sie bleibt im Arbeitsbaum liegen und steht in der Meldung an erster Stelle.

## Nicht in TB-152

Zeilen meinen `UEBERGABE.md` im Arbeitsbaum vom 11.10.2026; „E“ sind die Entscheide des steuernden Chats zum Bau, „S“ die Nummern der Stückliste (Bestand).

- (a) UEBERGABE Z. 3297: Bestand S40 — „Zu prüfen, nicht untersucht“ — E8; die Quelle: „Nicht an Fable gegeben, nicht eingeordnet“
- (b) UEBERGABE Z. 3046: Bestand S46 — „Entscheide des Betreibers ohne Eile“ (b) bis (d) — E8; (a) ist entschieden und steht in B5
- (c) UEBERGABE Z. 3047: Bestand S47 — „Später“, darin die 27 Formhinweise aus TB-146 und Nr. 9 bis 11 aus TB-141 — E8; kein Wortlaut in der UEBERGABE
- (d) UEBERGABE Z. 2875: Bestand S02 — Fehler Nr. 39, Erstfassung — E1; die Lehre ist durch Z. 3059 berichtigt (R16)
- (e) UEBERGABE Z. 3238: Bestand S09, S10 — Fehler Nr. 45 und 46: keine Zeile in Abschnitt 0 — E2; wörtlich in J2. Nr. 44 (Z. 3176, „**Regel daraus:**“) hat nach dem Entscheid des steuernden Chats eine Zeile (R02)
- (f) UEBERGABE Z. 3061: Bestand S49 — „Zwei Nachträge tragen dieselbe Uhrzeit …“ und „Die Ampel wurde … nicht gemessen …“ — E2, nur Journal (J2)
- (g) UEBERGABE Z. 2934, 2939, 2945: Bestand S32, S33, S48 — schon im Ziel — E9 (BACKLOG Z. 389 und Z. 392; JOURNAL, Block EO)
- (h) UEBERGABE Z. 2967: ohne Bestandsnummer — V6 „„erfüllt“ nur mit Nachweis der Sitzung“ — V6 kommt nicht ins allgemeine Regelwerk: Die Quelle (`UEBERGABE.md` Z. 2967) gilt dem Registerauftrag TB-149; V6 geht als Vorgabe in den Bau von TB-154 (`UEBERGABE.md` Z. 3487 und Z. 3528). Der Entscheid vom 10.10.2026, 22:55 nimmt die Zeile hinein, „wenn die Quelle die Regel allgemein fasst“; die Quelle nennt „56.7“, „die Sitzung TB-149“ und „Vorbild TB-139, Schritte 0d und 0e“
- (i) UEBERGABE Z. 3272: Bestand S45 — falsche Fundstelle im Ergebnis TB-148 Z. 157 — eine Ergebnisdatei ist kein Träger; der Befund steht wörtlich in B2 (Z. 3168)
- (j) UEBERGABE Z. 2914: Bestand S50 — „Drei Helfer schrieben ihren Bericht erst am Ende“ — die Quelle nennt keine Regel; die Regel steht in AW Z. 307
- (k) UEBERGABE Z. 2854, 2916, 3064, 3142, 3242, 3317: Bestand S01, S23–S27, S22 — E3, Einzelfälle, Zählungen oder schon im Ziel: Z. 2854 „Dazu: … (so getragen)“; Z. 2916 Posten 1, 3, 4, 6 (Bestand und Entwurf in einem Lauf steht in AW Z. 285; Holen der Fable-Antwort; Vorprüfung neben dem dritten Gegenleser; Nachtrag vor dem Satz, vgl. AW Z. 273); Z. 3064 Posten 1 und 3 („bis zu sieben Helfer“; zwei Gegenleser und ein enger, AW Z. 300); Z. 3242 Posten 1 und 2 (steht mit R14; Bestand vor dem Bau, AW Z. 285); Z. 3317 „`project_write` mit `local_path` braucht die Datei im Arbeitsverzeichnis“ (AW Z. 207 und Z. 223). Auswahl des Helfers — strittig
- (l) UEBERGABE Z. 3265: Bestand S11 — zweiter Satz „Ungenau im vorgebauten Helferauftrag B …“ — Einzelfall, keine Regel
- (m) UEBERGABE Z. 3240: Bestand S19 — der `jq`-Befehl im Wortlaut — senkrechte Striche in einer Tabellenzeile; R03 verweist auf die UEBERGABE
- (n) UEBERGABE Z. 3133: Bestand S28 — die Zusammenfassung des steuernden Chats zur Anweisung 09:16 — ersetzt durch den Wortlaut des Betreibers (R05, U3)
- (o) Bestand E10 — Ersetzungen in bestehenden Zeilen (UMZUG Z. 228, 260, 270–272; ARBEITSWEISE Z. 118, 212, 2480) — E10 ist als Klarstellung daneben gebaut (R10, R20, R21, U1, U2), das Werkzeug fügt nur ein; „berichtigen“ im Sinn von Ersetzen verlangte eine neue Art im Werkzeug und entfernte Zeilen im numstat. Strittig
- (p) ohne Bestandsnummer — die Ablage, die Projekt-Erinnerung und `docs/werkzeuge/ablage_soll.py` (TB-151; macht der steuernde Chat); der Codeblock der alten Fassung in `UMZUG.md` Abschnitt 6

## In einfacher Sprache

In der Zeit vom 09.10.2026, 22:03 bis zum Nachtrag 11.10.2026, 01:38 sind neue Regeln, Berichtigungen und Prüfbefunde entstanden, die bisher nur in der Übergabe stehen. Dieser Auftrag trägt sie dort ein, wo man sie später sucht: im Regelwerk (ARBEITSWEISE), in der Umzugsanleitung, im Backlog und im Journal — 38 Stücke. Dazu gehören die Anweisung des Betreibers zum Namen des Chats und die Klarstellung, wo die Eröffnungsdatei liegt, dazu der Backlog-Block zu den Kerzenformationen, dazu fünf neue Stücke vom 11.10.2026 (Umzug über Chrome als Regel, keine Karte mehr zum Chatnamen, Anheften der Chats, „Satz abschicken“ erst nach dem Blick ins Fenster). Es wird nur ergänzt, nichts gelöscht oder umgeschrieben; ein kleines Programm fügt die fertigen Texte ein und prüft vorher, ob jede Stelle eindeutig ist. Kein Programm und kein Werkzeug des Projekts wird geändert.

## Anhang A — Stücke (wörtlich)

Reihenfolge wie beim Einfügen. Das Werkzeug liest je Stück die Kopfzeile, die Felder `Zieldatei`, `Art`, `Form`, `Anker` und den Text zwischen den beiden Zeilen `~~~`. Die Zeile „Am HEAD“ ist Auskunft: Ankerzeile und Zeilenbilanz aus der Rechnung des Bauskripts (die Simulation bestätigt sie), Bestandsnummern und Quellzeilen aus der Stückliste (Zeilen der UEBERGABE meinen den Arbeitsbaum vom 11.10.2026, alle anderen Dateien den HEAD `6d700d4`). Regeln und Betreiberworte sind per Skript aus der Quelle geschnitten; „Zusatz zur Zeile darüber:“, Datum, Fehlernummer und die Spalte „steht in“ setzt das Bauskript.

#### R01 — Abschnitt 0, „Immer“: Startzeiten aus dem Stempel des Auftrags (Fehler Nr. 50)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Für Helferläufe Anfang und Ende messen oder die Spanne zwischen zwei Messungen nennen⟧

Am HEAD `6d700d4`: Anker Z. 47 · eingefügt +1 · Bestand S14 · Quelle: UEBERGABE Z. 3311

~~~
| ☐ | Zusatz zur Zeile darüber: Startzeiten aus dem Stempel des Auftrags nehmen (10.10.2026, Fehler Nr. 50: In drei Antworten Uhrzeiten von Helferstarts ohne Messung genannt („16:05“, „16:21“, „16:37“); die Stempel der Aufträge: N3 16:00, E2 16:15, E3 16:27) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 7 Nr. 50 |
~~~

#### R02 — Abschnitt 0, „Immer“: Kernzahlen an festen Pfaden messen (Fehler Nr. 47); vor „passt nicht in Teil Tn“ messen (Fehler Nr. 44)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Messungen bündeln (ein Aufruf, mehrere Fragen); Helfer parallel starten⟧

Am HEAD `6d700d4`: Anker Z. 57 · eingefügt +2 · Bestand S11, S08 · Quelle: UEBERGABE Z. 3265, 3311, 3176, 3238

~~~
| ☐ | Kernzahlen an festen Pfaden messen, nicht über eine gekürzte Suche (10.10.2026, Fehler Nr. 47: zwei Messbefehle schnitten die Liste der Registerkopie-Teile mit `head -8` ab; T4 und T5 brauchten einen dritten Befehl) | UEBERGABE, Nachtrag 10.10.2026, 12:59; Umzug 10.10.2026, 16:36, Block 7 Nr. 47 |
| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschnitt liegt (10.10.2026, Fehler Nr. 44: 56.8 liegt in Abschnitt 56 und damit in T5 (54–56), nicht in T4 (43–53). Gefolgert aus „T4 nur 313 Bytes Luft“, ohne die Stelle zu lesen, die den Zuschnitt regelt) | UEBERGABE, Nachtrag 10.10.2026, 10:30; Umzug 10.10.2026, 11:31, Block 7 Nr. 44 |
~~~

#### R03 — Abschnitt 0, „Am Ende jeder Antwort“: Ampel im Arbeitsbereich des Chats mit `jq`

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Letzte Zeile: Umzugsampel, gemessen mit `docs/werkzeuge/ampel.py`⟧

Am HEAD `6d700d4`: Anker Z. 79 · eingefügt +1 · Bestand S19 · Quelle: UEBERGABE Z. 3240

~~~
| ☐ | Zusatz zur Zeile darüber: `ampel.py` läuft im Arbeitsbereich des Chats nicht (das Ausführen einer vom Gerät geholten Datei wird abgelehnt). Gemessen mit `jq` nach derselben Formel, gleiche `message.id` einmal, erster Wert Grundlast (10.10.2026; der `jq`-Befehl steht im Wortlaut in der UEBERGABE, er trägt senkrechte Striche und steht deshalb nicht in dieser Tabelle) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
~~~

#### R04 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Anfrage bindet die Ablagedatei; Fable-Übergabe als Datei in der Ablage

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Die Kennung einer Fable-Anfrage ist der Tag des Ausgebens⟧

Am HEAD `6d700d4`: Anker Z. 99 · eingefügt +2 · Bestand S22, S34 · Quelle: UEBERGABE Z. 3317, 3306

~~~
| ☐ | Eine Anfrage, die Grösse und md5 einer Ablagedatei nennt, bindet diese Datei, bis Fable gelesen hat (10.10.2026, gelernt) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 7 |
| ☐ | Die Fable-Übergabe liegt als Datei in der Ablage, der Betreiber bekommt nur Namenszeile und Verweis; die Anfrage (über 20 KB) geht als Datei (10.10.2026, Vorgaben des steuernden Chats, dem Betreiber genannt, ohne Widerspruch) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 6 |
~~~

#### R05 — Abschnitt 0, „Arbeitsabschnitt endet“: Chatname — Namenszeile als erste Zeile, Nachfrage nach jedem Umzug

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Arbeitet ein Chat nach dem Eröffnungstext weiter, kennzeichnet er den alten Text in derselben Antwort als überholt⟧

Am HEAD `6d700d4`: Anker Z. 120 · eingefügt +2 · Bestand S28, S29, S30 · Quelle: UEBERGABE Z. 3133, 3134, 3233, 3305, 3336

~~~
| ☐ | ⭐⭐ Chatname (Betreiber 10.10.2026, 09:16, wörtlich; „gilt ab sofort, auch für alle Nachfolger“): „Der Name dieses Chats ist: Opus Trading Bot“ · „Die erste Nachricht an die neue Unterhaltung (dein Startsatz oder Übergabetext, den ich einfüge) beginnt mit genau dieser Zeile, danach eine Leerzeile:“ `Opus Trading Bot-<TT><Mon><JJJJ>` · „Monat: Jan, Feb, Mrz, Apr, Mai, Jun, Jul, Aug, Sep, Okt, Nov, Dez. Das Datum liest du ab, du schätzt es nicht.“ · „Darunter steht der Auftrag an die neue Unterhaltung so knapp wie möglich, am besten nur, welche Datei sie zuerst lesen soll. Schreib in diese erste Nachricht keine Rollenbezeichnung und keinen zweiten Namen (kein „Du bist der neue …“); das gehört in die Datei, die sie liest.“ · „Gib mir die erste Nachricht als Codeblock.“ · „Die neue Unterhaltung fragt mich bei ihrer ersten Rückfrage mit, wie der Chat heißt, und hält Wortlaut und Ergebnis in ihrer Übergabe fest. Weicht der Name ab, berichtet sie mir, statt weiter zu probieren.“ (seit 11.10.2026 abgelöst: Den neuen Chat legt ein Helfer über Chrome an, benennt ihn und liest den Namen ab; die Rückfrage entfällt — Betreiber, Karten 11.10.2026) · „Nimm diese Regel in deine Übergabe an den Nachfolger auf, damit sie jeden Umzug überlebt.“ | UMZUG 6; `logs/steuernder_chat/2026-10-10_BETREIBER_chatname_opus_trading_bot.txt`; UEBERGABE, Umzug 10.10.2026, 09:52, Block 6 |
| ☐ | Zusatz zur Zeile darüber (Betreiber 10.10.2026, 09:38, wörtlich): „Hinweis: Wir prüfen iterativ bei der eröffnung eines neunen Chats im Zuge des Umzugs zukünftig immer ob der korrekte Chatname gesetzt wurde bis der korrekte Chatname automatisch gesetzt wird und ich das bestätige.“ Lesart des steuernden Chats, vorläufig: Der neue Chat fragt in seiner ersten Antwort; bei Abweichung berichtet er, und die Form der ersten Nachricht wird für den nächsten Versuch angepasst; er benennt nichts selbst um (seit 11.10.2026 abgelöst: Den neuen Chat legt ein Helfer über Chrome an, benennt ihn und liest den Namen ab; die Rückfrage entfällt — Betreiber, Karten 11.10.2026) (Anlass: dreimal „Opus Trading Bot setup“ statt des Solls „Opus Trading Bot-10Okt2026“ — Umzüge 10.10.2026, 09:52, 11:31 und 16:36; der Fable-Chat hiess „Fable Trading Bot Übergabe“) | UMZUG 6; UEBERGABE, Umzug 10.10.2026, 09:52, Block 6; Umzug 10.10.2026, 11:31, Block 6; Umzug 10.10.2026, 16:36, Block 6; Nachtrag 10.10.2026, 22:03 |
~~~

#### R06 — Abschnitt 0, „Arbeitsabschnitt endet“: Befunde sofort in die Übergabe; Neustart des Arbeitsbereichs

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Notizen unter `logs/steuernder_chat/`, solange eine Sitzung den Arbeitsbaum hat⟧

Am HEAD `6d700d4`: Anker Z. 122 · eingefügt +2 · Bestand S20, S22 · Quelle: UEBERGABE Z. 3243, 3317

~~~
| ☐ | Befunde aus der Antwort sofort in die Übergabe (10.10.2026, gelernt: Die Geräteanbindung fiel zweimal weg (10:53 bis 10:55; zwei Gegenleser verloren P3 bis P7 aus der Berichtsdatei)) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
| ☐ | Der Arbeitsbereich des Chats startete einmal neu (zwischen 10:36 und 10:44) ⇒ ein laufender Helfer ist danach nicht mehr ansprechbar, seine Schlussmeldung fehlt; der Bericht auf dem Gerät bleibt (10.10.2026, gelernt; ebenso zwischen 13:31 und 15:24: Die Schlussmeldung des Gegenlesers ging verloren, sein Bericht auf dem Gerät blieb; eine geplante Nachschau kam 1 h 39 min verspätet) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7; Umzug 10.10.2026, 16:36, Block 7 |
~~~

#### R07 — Abschnitt 0, „Entscheidung beim Betreiber“: Vorgabe gegen die Eröffnung erst nach Messung (Fehler Nr. 49 und Nr. 51)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor einer Vorgabe zur Reihenfolge das Vorbild im Register messen lassen⟧

Am HEAD `6d700d4`: Anker Z. 129 · eingefügt +2 · Bestand S13 · Quelle: UEBERGABE Z. 3311, 3344

~~~
| ☐ | Vor einer Vorgabe, die von der Eröffnung abweicht, die regelnde Stelle an der Quelle messen lassen (10.10.2026, Fehler Nr. 49: Auf einen Befund des ersten Gegenlesers hin fünf Kenntnis-Punkte zu Fragen gemacht, ohne die Registerzeilen prüfen zu lassen und gegen die Eröffnung (nur M4 ist Frage); der enge Gegenleser fand es, eine Berichtigungsrunde verloren) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 7 Nr. 49 |
| ☐ | Der Bestand vor einer Vorgabe misst auch die Regel, die den Gegenstand einordnet (hier die Klassen der Ablage), nicht nur das Werkzeug (10.10.2026, Fehler Nr. 51 — Fehler Nr. 49 in anderer Gestalt: Um 22:07 die Vorgabe gesetzt und dem Betreiber genannt, die Eröffnungsdatei bleibe unverfolgt unter `logs/steuernder_chat/` und `ablage_soll.py` bekomme eine Liste „nur in der Ablage“ — gestützt auf den Bestand BESTAND151, der 0a und das Werkzeug mass, nicht aber `ARBEITSWEISE.md` 23.1/23.2) | UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 7 Nr. 51 |
~~~

#### R25 — Abschnitt 0, „Mac-Sitzung“: „Satz abschicken“ erst nach dem eigenen Blick (Fehler Nr. 54; Stück 37)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zuerst Satz und Aufgaben zustellen, dann die Freigabe für den Blick ins Terminal anfordern⟧

Am HEAD `6d700d4`: Anker Z. 199 · eingefügt +1 · Bestand — · Quelle: UEBERGABE Z. 3496, 3513, 3520, 3532, 3549

~~~
| ☐ | Zusatz zu den zwei Zeilen darüber (Fehler Nr. 30 und Nr. 42) und zu Fehler Nr. 23: Ergebnis und Ankündigung zuerst zustellen, dann die Freigabe für den Blick anfordern — die Aufgabe „Satz abschicken“ samt Kopierfeld erst nach dem eigenen Blick ins Fenster (Kopf „Claude Max“, kein „Not logged in“). Der Wächter prüft den Schlüsselbund, nicht die Anmeldung (11.10.2026, Fehler Nr. 54: „Satz abschicken“ als Aufgabe gegeben, gestützt auf die Wächter-Zeile; der Blick zeigte eine nicht angemeldete Sitzung, „API Usage Billing“) | UEBERGABE, Umzug 11.10.2026, 01:24, Block 1, Block 4 Nr. 1 und Nr. 8, Block 7 Nr. 54, Zusatz 01:30 |
~~~

#### R08 — Abschnitt 0, „Mac-Sitzung“: Blick ins Fenster vor „Satz abschicken“ (Fehler Nr. 42)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zuerst Satz und Aufgaben zustellen, dann die Freigabe für den Blick ins Terminal anfordern⟧

Am HEAD `6d700d4`: Anker Z. 199 · eingefügt +1 · Bestand S06 · Quelle: UEBERGABE Z. 3081, 3139

~~~
| ☐ | Wartet eine Sitzung länger oder über einen Umzug hinweg, kommt der Blick ins Fenster vor der Aufgabe „Satz abschicken“; Fehler Nr. 30 (erst Satz, dann Freigabe) bleibt für den frischen Start (Vorgabe des steuernden Chats, vorläufig; 10.10.2026, Fehler Nr. 42: Dem Betreiber zwischen 07:49 und 07:55 „Sie wartet auf den Satz“ geschrieben und „Satz abschicken“ als Aufgabe gegeben, gestützt allein auf die Sonde. Die Sonde zeigt Prozess und Zustand, nicht, was die Sitzung getan hat; dasselbe galt für die Sonde 06:25) | UEBERGABE, Nachtrag 10.10.2026, 08:15; Umzug 10.10.2026, 09:52, Block 7 Nr. 42 |
~~~

#### R09 — Abschnitt 0, „Mac-Sitzung“: erst auslegen, dann der Auslöser (Fehler Nr. 40)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Probestart über `starte_TB-<n>` ohne Satz, Blick ins Fenster⟧

Am HEAD `6d700d4`: Anker Z. 200 · eingefügt +2 · Bestand S04, S23 · Quelle: UEBERGABE Z. 2948, 3060, 2916

~~~
| ☐ | Erst auslegen, dann der Auslöser (so macht es das Ablege-Skript) (09.10.2026, Fehler Nr. 40: den Start-Auslöser `starte_TB-147` um 23:19:59 gelegt, bevor der Zeiger auf TB-147 stand; der Wächter brach ab („steht nicht als gueltiger Auftrag“), folgenlos) | UEBERGABE, Nachtrag 09.10.2026, 23:51; Umzug 10.10.2026, 07:38, Block 7 Nr. 40 |
| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum genau 0a entspricht, bevor der Auslöser gelegt wird (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 22:41, Block 7 |
~~~

#### R10 — Abschnitt 0, „Ablage“: Eröffnungsdatei im Repo und in der Ablage (E10, berichtigt)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Ausnahme zur Zeile darüber: In der Ablage liegt auch `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`⟧

Am HEAD `6d700d4`: Anker Z. 212 · eingefügt +1 · Bestand E10 · Quelle: UEBERGABE Z. 3345, 3428 (Vorgabe des steuernden Chats, 10.10.2026; E10, berichtigt); ARBEITSWEISE Z. 2466 (G1) und Z. 2480 (B2 Stand), UMZUG Z. 213

~~~
| ☐ | Klarstellung zur Zeile darüber: Die Datei liegt seit TB-151 auch verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` — Klasse B2 Stand (23.2), `docs/werkzeuge/ablage_soll.py` führt sie in der Liste `STAND`; beim Umzug ersetzt der alte Chat beide Fassungen, md5 gleich (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; G1: „Alles, was den Umzug überleben muss, liegt dort committet“; UMZUG 4, Schritt 4: „muss mit dem Repo gleich lauten“) | 23.1, 23.2; UMZUG 4 und 6; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6 |
~~~

#### R11 — Abschnitt 0, „Ablage“: Nachsehen nach einer Fable-Antwort über einen Helfer (Fehler Nr. 38)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Neue Fable-Antworten über `project_info` (Liste) prüfen, nicht über die Suche⟧

Am HEAD `6d700d4`: Anker Z. 215 · eingefügt +1 · Bestand S01 · Quelle: UEBERGABE Z. 2854, 2912

~~~
| ☐ | Zusatz zur Zeile darüber: In der Eröffnung steht beim Nachsehen nach einer Fable-Antwort „über einen Helfer“ (09.10.2026, Fehler Nr. 38: `project_info` beim Einstieg selbst aufgerufen (die ganze Liste im Chat), bevor Block 7 Nr. 37 des Umzugs 21:06 gelesen war) | UEBERGABE, Nachtrag 09.10.2026, 22:03; Umzug 09.10.2026, 22:41, Block 7 Nr. 38 |
~~~

#### R12 — Abschnitt 0, „Ablage“: nichts über 3 KB in den Chat

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Nach jedem Helferblock die Ampel messen⟧

Am HEAD `6d700d4`: Anker Z. 220 · eingefügt +1 · Bestand S18 · Quelle: UEBERGABE Z. 2978

~~~
| ☐ | Ab jetzt nur noch Kurzberichte; nichts über 3 KB in den Chat (09.10.2026, Ampel 23:53: Verlauf 477 584 (Grundlast 126 607) — gelb nach den verdoppelten Schwellen. Teuer: die Fable-Antwort ganz gelesen (53 KB), der Cloud-Auftrag zweimal im Chat (gelesen und ausgegeben), die Entwürfe 56.7 und 56.8 (22 KB), neun lange Helferaufträge) | UEBERGABE, Nachtrag 09.10.2026, 23:53 (der zweite dieser Uhrzeit: „TB-147: enger Gegenleser ohne Sachbefund“) |
~~~

#### R13 — Abschnitt 0, „Ablage“: Dateiliste nicht holen (Fehler Nr. 48); Ablage-Helfer nur für Stage und md5, mit Vorrang vor den Zeilen, die einen Helfer nennen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Geht der Zeile darüber vor, soweit es um eine einzelne Datei geht⟧

Am HEAD `6d700d4`: Anker Z. 223 · eingefügt +2 · Bestand S12, S15 · Quelle: UEBERGABE Z. 3271, 3311, 2933, 3062, 3352, 3427

~~~
| ☐ | Die Dateiliste der Ablage nicht holen; nur ablegen, was sich geändert hat (messen, welche Abschnittsdateien sich ausser der Kopfzeile ändern) (10.10.2026, Fehler Nr. 48: `project_info` ganz in den Chat geholt (rund 12 KB) und 60 Quittungen von `project_write`; die Ampel stieg von 87 817 (12:56) auf 159 121 (13:04)) | UEBERGABE, Nachtrag 10.10.2026, 13:30; Umzug 10.10.2026, 16:36, Block 7 Nr. 48 |
| ☐ | Ein Ablage-Helfer nur noch für Stage und md5; `project_write` und `project_info` bleiben beim steuernden Chat. Geht den Zeilen darüber vor, soweit sie einen Helfer nennen (am HEAD `6d700d4`: Z. 215, 220, 222, 223): Helfer haben kein Projects-Werkzeug (09.10.2026: Der Helfer ABLAGE146 hatte kein Projects-Werkzeug (drei Suchen ohne Treffer, nichts abgelegt) — die drei Dateien hat der steuernde Chat selbst geschrieben; 10.10.2026: „`project_info` bleibt beim steuernden Chat“; der Vorrang ist Vorgabe des steuernden Chats, vorläufig) | UEBERGABE, Nachtrag 09.10.2026, 22:56; Umzug 10.10.2026, 07:38, Block 7; Nachtrag 10.10.2026, 22:27; Umzug 10.10.2026, 22:55, Block 6; Eröffnung (`projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`) |
~~~

#### R14 — Abschnitt 0, „fremdes Ergebnis“: Prüffrage (Fehler Nr. 43); Befund braucht die Quellenzeile; Abnahme in zwei Helfern; Helferbefund erst nach eigener Nachmessung (Fehler Nr. 53)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Eine Erfolgsmeldung, die der Betreiber einfügt, zuerst als solche benennen⟧

Am HEAD `6d700d4`: Anker Z. 242 · eingefügt +4 · Bestand S07, S21, S25 · Quelle: UEBERGABE Z. 3093, 3139, 3312, 3142, 3434

~~~
| ☐ | Vor einer Prüffrage die Stelle des Auftrags lesen, die den Ort regelt (10.10.2026, Fehler Nr. 43: Der Helferauftrag ABNAHME147 fragte, ob `JOURNAL.md` „nur angehängt“ sei; der Auftrag TB-147 (Z. 21, 26) verlangt das Einfügen vor `## Wiederkehrende Lehren`. Der Helfer meldete das als A2; es ist kein Befund an der Sitzung) | UEBERGABE, Nachtrag 10.10.2026, 08:43; Umzug 10.10.2026, 09:52, Block 7 Nr. 43 |
| ☐ | Ein Befund, der eine Aussage ändert, braucht die zitierte Quellenzeile (10.10.2026: Ein Gegenleser kann irren: Der erste nannte „Register-Code-Widerspruch“ eine Deutung; das Wort steht in REG Z. 11855 als Folge eines Wenn-Satzes) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 7 |
| ☐ | Abnahme in zwei gleichzeitigen Helfern mit getrenntem Zuschnitt; das Ergebnis einer fremden Sitzung zuerst sichern, dann abnehmen, dann schliessen (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 09:52, Block 7 |
| ☐ | Ein Helferbefund, der eine Aussage über ein fremdes Ergebnis ändert, geht erst nach der eigenen Nachmessung an den Betreiber (10.10.2026, Fehler Nr. 53: Um 22:35 einen Helferbefund zur Fable-Antwort („Stütze dünn“ zu R90 (f)) ohne eigene Messung an den Betreiber gegeben; die eigene Messung (R81 (b), REG Z. 11751) widerlegte ihn) | UEBERGABE, Umzug 10.10.2026, 22:55, Block 7 Nr. 53 |
~~~

#### R15 — Abschnitt 0, „Auftrag schreiben“: kleine Berichtigungen auch unter Zeitdruck (Fehler Nr. 41)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Kleine Berichtigungen (einzelne Zeilen, kein Sollwert) macht der steuernde Chat per Skript⟧

Am HEAD `6d700d4`: Anker Z. 297 · eingefügt +1 · Bestand S05 · Quelle: UEBERGABE Z. 2948, 3060

~~~
| ☐ | Zusatz zur Zeile darüber: Die Zeile „kleine Berichtigungen … enger Gegenleser“ gilt auch unter Zeitdruck; sonst steht „Berichtigungen nicht gegengelesen“ in der Übergabe an den Betreiber (09.10.2026, Fehler Nr. 41: den Cloud-Auftrag mit sechs eingearbeiteten Berichtigungen ausgegeben, bevor ein enger Gegenleser die geänderten Zeilen gelesen hatte, und dem Betreiber nur „gegengelesen“ gesagt) | UEBERGABE, Nachtrag 09.10.2026, 23:51; Umzug 10.10.2026, 07:38, Block 7 Nr. 41 |
~~~

#### R16 — Abschnitt 0, „Auftrag schreiben“: Befehlswörter gegen `deny` und `ask` (Fehler Nr. 39, berichtigt); Erlaubnislisten messen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Die Nachlese „als Mac-Sitzung durchgehen“ samt Abgleich mit den `deny`-Regeln⟧

Am HEAD `6d700d4`: Anker Z. 301 · eingefügt +2 · Bestand S03, S17 · Quelle: UEBERGABE Z. 3059, 3061

~~~
| ☐ | Vor jedem Mac-Auftrag prüft ein Skript die Befehlswörter gegen `deny` und `ask`; der Gegenleser liest die zwei Listen selbst (10.10.2026, Fehler Nr. 39, berichtigt: Der Abbruch von TB-146 kam von `chmod +x` im abgelehnten Aufruf (`deny`: `Bash(chmod:*)`), nicht vom Heredoc; Heredoc und Umleitung nach `$TMPDIR` liefen in TB-146 Schritt 0a) | UEBERGABE, Umzug 10.10.2026, 07:38, Block 7 Nr. 39 |
| ☐ | Zusatz zur Zeile darüber: Vor einer Vorgabe zur Befehlsform die Erlaubnislisten messen (10.10.2026: Eine eigene Vorgabe (Umleitung nicht wörtlich vorgeben) erzeugte einen A-Befund und wurde zurückgenommen) | UEBERGABE, Umzug 10.10.2026, 07:38, Block 7 |
~~~

#### R17 — Abschnitt 0, „Auftrag schreiben“: kein Rückweg durch die Sitzung, wenn er eine Verbotsregel träfe

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor einem Auftrag, der Programme ausserhalb des Repos steuert⟧

Am HEAD `6d700d4`: Anker Z. 309 · eingefügt +1 · Bestand S16 · Quelle: UEBERGABE Z. 2984, 3007

~~~
| ☐ | Kein Rückweg durch die Sitzung, wenn er eine Verbotsregel träfe: Die Sitzung setzt nichts zurück und nimmt keinen Ersatzbefehl (der Gegenleser mass `git show HEAD:<Register> > <Register>` als gangbar — das umginge die Verbotsregel des Betreibers); sie sichert den Unterschied als Beleg, committet das Register nicht, bricht ab und meldet; das Zurücksetzen entscheidet der Betreiber (Vorgabe des steuernden Chats; 10.10.2026: Der Rückweg nach einem roten Nachweis verweist an zwei Stellen auf `git checkout -- <Register>`; das steht in `deny`) | UEBERGABE, Nachtrag 10.10.2026, 00:38; Nachtrag 10.10.2026, 01:06 |
~~~

#### R18 — Abschnitt 0, „Auftrag schreiben“: so getragen, Umzüge 09.10.2026, 22:41 bis 10.10.2026, 16:36

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vorprobe als eigener kleiner Auftrag vor dem grossen⟧

Am HEAD `6d700d4`: Anker Z. 310 · eingefügt +5 · Bestand S23, S24, S25, S26, S27 · Quelle: UEBERGABE Z. 2916, 3064, 3142, 3242, 3316

~~~
| ☐ | Der Gegenleser der Stücke läuft gleichzeitig mit dem Bau-Helfer; der Auftrag ist per `alles.sh` neu baubar, jede Berichtigung per Skript mit `assert` (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 22:41, Block 7 |
| ☐ | Jeder Bau mit eigenem kleinem git-Repo als Simulation; Berichtigungen an den Bau-Helfer zurück; Rechercheposten des Backlogs als Helfer mit Netzzugang; das Ablege-Skript mit `--nur-ersetzen` für eine neue Fassung vor dem Satz (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 07:38, Block 7 |
| ☐ | Helferaufträge schreibt ein Skript mit `assert` auf die Ausgangsstände und eigener Uhrzeit; Neubau per `alles.sh`, Vergleich gegen die gegengelesene Fassung per Skript, ein enger Gegenleser nur für die geänderten Zeilen; das Auslege-Skript mit `--trocken` vor dem echten Lauf (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 09:52, Block 7 |
| ☐ | Bau in Stufen (erst verschobene Werte, dann Texte) durch denselben Helfer; Vorgaben für Ersetzungen als JSON mit `assert` auf die Trefferzahl; kleine Berichtigung selbst über die Bausteine und ein enger Gegenleser mit rund 10 Schritten für genau die geänderten Zeilen, gleichzeitig mit der Karte (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
| ☐ | Abnahme-Aufträge vorbauen, während die Sitzung arbeitet (ein Skript mit HEAD als Argument); Berichtigungen als ein Skript mit `assert` aus der Vorfassung in einen neuen Ordner (`final/` → `v2/` … `v7/`), enger Gegenleser misst die geänderten Zeilen selbst mit `difflib`; Ablage über ein Archiv und eine md5-Liste (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 16:36, Block 7 |
~~~

#### R19 — Abschnitt 0, „Auftrag schreiben“: gelernt — Bauskript ausserhalb seines Ordners; md5 der Vorgabe; Zeilenangaben setzt ein Skript (Fehler Nr. 52); Kriterium „Ergebniszahl vor Augen“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Im Helferauftrag die Suche auf benannte Dateien begrenzen⟧

Am HEAD `6d700d4`: Anker Z. 312 · eingefügt +4 · Bestand S20 · Quelle: UEBERGABE Z. 3243, 3433, 2983

~~~
| ☐ | Ein Bauskript, das eine Datei ausserhalb seines Ordners überschreibt (`b1` Z. 132, `y3`), vor dem Start im Helferauftrag nennen (10.10.2026, gelernt) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
| ☐ | Ein Helferskript mit fest eingetragenem md5 seiner Vorgabe (b5 Z. 26) bricht, wenn die Vorgabe berichtigt wird — den md5 nachziehen (10.10.2026, gelernt) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
| ☐ | Zeilenangaben in Helferaufträgen setzt ein Skript (`grep -n`), nicht das Auge am Ausschnitt; eine Einordnung stützt sich auf die Quellzeile, nicht auf die Sammelzeile (10.10.2026, Fehler Nr. 52: Zwei Fundstellen nicht an der Quelle gemessen) | UEBERGABE, Umzug 10.10.2026, 22:55, Block 7 Nr. 52 |
| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitzung am ersten Messpunkt angehalten, weil im Kopf von `shared/zuteilung.py` Ergebniszahlen als Kommentar stehen — ersetzt durch „weiterlesen, nichts hinschreiben, nur den Ort nennen“ (10.10.2026, Auftrag TB-148, Gegenleser GEGEN148, ein A-Befund) | UEBERGABE, Nachtrag 10.10.2026, 00:38 |
~~~

#### R20 — Abschnitt 0, „Arbeitsabschnitt endet“: Eröffnungsdatei im Repo und in der Ablage (E10, berichtigt)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Der Eröffnungstext liegt als Datei `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` in der Projektablage⟧

Am HEAD `6d700d4`: Anker Z. 118 · eingefügt +1 · Bestand E10 · Quelle: UEBERGABE Z. 3345, 3428 (Vorgabe des steuernden Chats, 10.10.2026; E10, berichtigt); ARBEITSWEISE Z. 2466 (G1) und Z. 2480 (B2 Stand), UMZUG Z. 213

~~~
| ☐ | Klarstellung zur Zeile darüber: Die Datei liegt seit TB-151 verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und in der Ablage unter `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`; beim Umzug ersetzt der alte Chat beide, md5 gleich. Jeder Auftrag führt sie nach einem Umzug in 0a mit, wie `UEBERGABE.md` (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; G1: „Alles, was den Umzug überleben muss, liegt dort committet“) | 23.1, 23.2; UMZUG 6; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6 |
~~~

#### R21 — Abschnitt 23.2, Klasse „B2 Stand“: die Eröffnungsdatei als weiteres Beispiel (E10, berichtigt)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| **B2 Stand** | Repo **und** Ablage, eine Fassung ohne Datum im Namen |⟧

Am HEAD `6d700d4`: Anker Z. 2480 · eingefügt +1 · Bestand E10 · Quelle: UEBERGABE Z. 3345, 3428 (Vorgabe des steuernden Chats, 10.10.2026; E10, berichtigt); ARBEITSWEISE Z. 2466 (G1) und Z. 2480 (B2 Stand), UMZUG Z. 213

~~~
| **B2 Stand**, Zusatz mit TB-152 | Repo **und** Ablage, eine Fassung ohne Datum im Namen | — | **nie**; bei jedem Umzug ersetzt der alte steuernde Chat beide Fassungen, md5 gleich | `EROEFFNUNG_STEUERNDER_CHAT.md` — im Repo `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, in der Ablage `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`; verfolgt seit TB-151, `docs/werkzeuge/ablage_soll.py` führt sie in der Liste `STAND` (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6) |
~~~

#### R24 — Abschnitt 0, „Arbeitsabschnitt endet“: alle aktuellen Chats sind angeheftet (Stück 36)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Beim Umzug wird kein Chat per geplanter Aufgabe angelegt⟧

Am HEAD `6d700d4`: Anker Z. 119 · eingefügt +1 · Bestand — · Quelle: UEBERGABE Z. 3558, 3560, 3563, 3564

~~~
| ☐ | Alle aktuellen Chats sind angeheftet; wird einer nicht mehr gebraucht, wird er gelöst. Beim Umzug heftet der Helfer den neuen Chat an und löst den alten; zugeordnet wird über die Adresse, nicht über den Namen (Vorgabe des steuernden Chats, vorläufig: am 11.10.2026 trugen der alte und der neue Chat denselben Namen); vor dem Klick auf den Menüknopf überfährt er den Eintrag und macht ein Bildschirmfoto (Betreiber 11.10.2026: „Es wurde vergessen diesen anzupinnen und den alten zu lösen. Ziel wäre es dass immer alle aktuellen chats angepinnt sind und wenn sie nicht mehr benötigt werden sollen sie wieder gelöst werden“; 11.10.2026: der erste Helfer bekam das Menü ohne Bildschirmfoto dreimal nicht auf) | UEBERGABE, Nachtrag 11.10.2026, 01:38 |
~~~

#### R23 — Abschnitt 0, „Arbeitsabschnitt endet“: die Karte zum Chatnamen entfällt (Stück 35)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Beim Umzug wird kein Chat per geplanter Aufgabe angelegt⟧

Am HEAD `6d700d4`: Anker Z. 119 · eingefügt +1 · Bestand — · Quelle: UEBERGABE Z. 3133, 3134, 3558, 3560

~~~
| ☐ | Die Karte zum Chatnamen entfällt: Den Namen liest der Helfer nach dem Umbenennen in Chrome ab, er steht in der Übergabe. Das löst die Rückfrage aus den Anweisungen vom 10.10.2026, 09:16 und 09:38 ab (Betreiber 11.10.2026: „Diese Frage brauchst du mir zukünftig nicht mehr stellen da dieser neu hauptchat vom alten hauptchat via chrome angelegt wird und umbenannt“; Lesart des steuernden Chats, vorläufig: gilt für Fable-Chats ebenso, sobald sie über Chrome angelegt werden) | UEBERGABE, Nachtrag 11.10.2026, 01:38; Umzug 10.10.2026, 09:52, Block 6 |
~~~

#### R22 — Abschnitt 0, „Arbeitsabschnitt endet“: Umzug über Chrome als Regel (Stück 34)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Beim Umzug wird kein Chat per geplanter Aufgabe angelegt⟧

Am HEAD `6d700d4`: Anker Z. 119 · eingefügt +1 · Bestand — · Quelle: UEBERGABE Z. 3493, 3549, 3558, 3560

~~~
| ☐ | ⭐ Löst die Zeile darüber ab, soweit sie den Kopierblock als Regelweg nennt: Den Umzug macht der steuernde Chat über Chrome. Ein Helfer des alten Chats legt den neuen Chat an (Projekt Trading Bots, Modell wie bisher), schickt die erste Nachricht, benennt ihn um, heftet ihn an und löst den alten; der Betreiber bestätigt im neuen Chat nur die Ordner-Freigabe. Scheitert ein Schritt, bekommt der Betreiber wie bisher den Kopierblock. Eine geplante Aufgabe wird dafür weiter nie angelegt; die Freigabeabfrage für Ordner beantwortet der steuernde Chat nie selbst (Betreiber, Karten 11.10.2026: „Ja, als Probe (Recommended)“, nach der Probe „Ja, zur Regel (Recommended)“) | UEBERGABE, Umzug 11.10.2026, 01:24, Kopf und Zusatz 01:30; Nachtrag 11.10.2026, 01:38 |
~~~

#### U1 — UMZUG.md, Abschnitt 4, Schritt 6: Der Eröffnungstext ist eine Datei im Repo und in der Ablage (E10, berichtigt)

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦**Vorlage in Abschnitt 6 dieses Dokuments.**⟧

Am HEAD `6d700d4`: Anker Z. 229 · eingefügt +2 · Bestand E10 · Quelle: UEBERGABE Z. 3345, 3428 (Vorgabe des steuernden Chats, 10.10.2026; E10, berichtigt); ARBEITSWEISE Z. 2466 (G1) und Z. 2480 (B2 Stand), UMZUG Z. 213

~~~
⭐ **Nachtrag mit TB-152 (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6):** „kein Download, keine Datei, kein Anhang“ im Absatz darüber ist für den Eröffnungstext überholt: Im Chat steht seit 09.10.2026 nur der kurze Text (Abschnitt 6); der Eröffnungstext selbst ist eine Datei. Die Datei liegt seit TB-151 verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und in der Ablage unter `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`; beim Umzug ersetzt der alte steuernde Chat beide, md5 gleich. Seit 10.10.2026 beginnt die erste Nachricht mit der Namenszeile (Abschnitt 6, Chatname).
~~~

#### U2 — UMZUG.md, Abschnitt 6: Ort der Eröffnungsdatei — Repo und Ablage, die Kopie unter `logs/` entfällt (E10, berichtigt)

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: vor
Form: Block
Anker: ⟦⭐ **Dies ist die verbindliche Fassung des Eröffnungstextes; sie steht nur hier.**⟧

Am HEAD `6d700d4`: Anker Z. 270 · eingefügt +2 · Bestand E10 · Quelle: UEBERGABE Z. 3345, 3428 (Vorgabe des steuernden Chats, 10.10.2026; E10, berichtigt); ARBEITSWEISE Z. 2466 (G1) und Z. 2480 (B2 Stand), UMZUG Z. 213

~~~
⭐ **Klarstellung mit TB-152 zum Ort der Eröffnungsdatei (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6):** Die Datei liegt seit TB-151 verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und in der Ablage unter `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` — Klasse B2 Stand (`ARBEITSWEISE.md` 23.2), `docs/werkzeuge/ablage_soll.py` führt sie in der Liste `STAND`. Grund: G1 (`ARBEITSWEISE.md` 23.1: „Alles, was den Umzug überleben muss, liegt dort committet“) und Abschnitt 4, Schritt 4 („muss mit dem Repo gleich lauten“). Im Nachtrag vom 09.10.2026 darüber ist damit überholt: „Kopie unter `logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md`“ — die Kopie unter `logs/steuernder_chat/` entfällt als Ort; beim Umzug ersetzt der alte steuernde Chat die Datei im Repo und in der Ablage, md5 gleich. Im Absatz direkt darunter sind „sie steht nur hier“ und „Keine Anhänge. Keine Dateien.“ für diese Datei überholt: Der neue Chat liest sie mit `project_read`.
~~~

#### U3 — UMZUG.md, Abschnitt 6: Chatname — Wortlaut des Betreibers, kurzer Text mit Namenszeile, Ergebnis

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦## 6. Der Eröffnungstext — die einzige Fassung⟧

Am HEAD `6d700d4`: Anker Z. 258 · eingefügt +41 · Bestand S28, S29, S30 · Quelle: UEBERGABE Z. 3133, 3134, 3233, 3305, 3328, 3336

~~~
⭐⭐ **Gilt seit 10.10.2026 (eingetragen mit TB-152) — Chatname: Die erste Nachricht an die neue Unterhaltung beginnt mit der Namenszeile.** Betreiber 10.10.2026, 09:16, wörtlich (`logs/steuernder_chat/2026-10-10_BETREIBER_chatname_opus_trading_bot.txt`):

```
Anweisung des Betreibers zum Namen dieses Chats (gilt ab sofort, auch für alle Nachfolger)

Der Name dieses Chats ist: Opus Trading Bot

Ziel: Nach jedem Umzug soll die neue Unterhaltung von selbst „Opus Trading Bot-<TT><Mon><JJJJ>“ heißen, mit dem Datum des Tages, zum Beispiel „Opus Trading Bot-10Okt2026“. Ich benenne nichts von Hand um.

So verhält sich die App (am 10.10.2026 mit zwölf Test-Chats gemessen, am Namen „Opus Saldenspiegel“):
- Sie bildet den Namen eines Chats aus seiner ersten Nachricht. Sie nimmt die erste Zeile, wenn im Rest der Nachricht keine anderen auffälligen Bezeichnungen stehen.
- Ein Datum mit Punkten, mit Monatsnamen, mit Unterstrich oder als Jahr-Monat-Tag streicht sie. Stehen blieb nur diese Form: Tag, Monat als drei Buchstaben, Jahr, ohne Punkte und ohne Leerzeichen, mit einem Bindestrich fest an das letzte Wort des Namens gehängt.
- Bindestriche mit Leerzeichen davor und dahinter fallen weg.

Deine Regel für jeden Umzug:
1. Die erste Nachricht an die neue Unterhaltung (dein Startsatz oder Übergabetext, den ich einfüge) beginnt mit genau dieser Zeile, danach eine Leerzeile:
   Opus Trading Bot-<TT><Mon><JJJJ>
   Monat: Jan, Feb, Mrz, Apr, Mai, Jun, Jul, Aug, Sep, Okt, Nov, Dez. Das Datum liest du ab, du schätzt es nicht.
2. Darunter steht der Auftrag an die neue Unterhaltung so knapp wie möglich, am besten nur, welche Datei sie zuerst lesen soll. Schreib in diese erste Nachricht keine Rollenbezeichnung und keinen zweiten Namen (kein „Du bist der neue …“); das gehört in die Datei, die sie liest. Sonst nimmt die App diese Wörter als Namen.
3. Gib mir die erste Nachricht als Codeblock.
4. Die neue Unterhaltung fragt mich bei ihrer ersten Rückfrage mit, wie der Chat heißt, und hält Wortlaut und Ergebnis in ihrer Übergabe fest. Weicht der Name ab, berichtet sie mir, statt weiter zu probieren.
5. Nimm diese Regel in deine Übergabe an den Nachfolger auf, damit sie jeden Umzug überlebt.

Nicht gemessen: Namen mit mehr als zwei Wörtern (die App hat bisher nur Namen mit zwei bis drei Wörtern vergeben) und andere Monate als Oktober. „Opus Trading Bot“ hat drei Wörter; kürzt die App den Namen beim ersten Umzug, sag es mir.

Bestätige mir kurz, dass du die Regel übernommen hast. Ändere sonst nichts an deiner Arbeit.
```
(seit 11.10.2026 abgelöst: Den neuen Chat legt ein Helfer über Chrome an, benennt ihn und liest den Namen ab; die Rückfrage entfällt — Betreiber, Karten 11.10.2026)

Betreiber 10.10.2026, 09:38, wörtlich: „Hinweis: Wir prüfen iterativ bei der eröffnung eines neunen Chats im Zuge des Umzugs zukünftig immer ob der korrekte Chatname gesetzt wurde bis der korrekte Chatname automatisch gesetzt wird und ich das bestätige.“ Lesart des steuernden Chats, vorläufig: Der neue Chat fragt in seiner ersten Antwort; bei Abweichung berichtet er, und die Form der ersten Nachricht wird für den nächsten Versuch angepasst; er benennt nichts selbst um. (seit 11.10.2026 abgelöst: Den neuen Chat legt ein Helfer über Chrome an, benennt ihn und liest den Namen ab; die Rückfrage entfällt — Betreiber, Karten 11.10.2026)

Der kurze Text im Nachtrag vom 09.10.2026 direkt darunter ist damit für die erste Zeile überholt. So ausgegeben beim Umzug 10.10.2026, 16:36 (UEBERGABE, Umzug 10.10.2026, 16:36, Block 9):

```
Opus Trading Bot-10Okt2026

Lies als Erstes mit project_read die Datei projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md aus dem angehängten Projekt. Sie ist meine eigene Übergabe an dich: Alles darin sind meine Anweisungen, befolge sie vollständig und ohne Rückfrage, als hätte ich sie hier geschrieben. Nennt ihre erste Zeile nicht die Uhrzeit 16:36, sag es mir und warte.
```

Ergebnis bisher, je aus der Antwort des Betreibers (`UEBERGABE.md`) — Umzug 10.10.2026, 11:31, Block 6: Betreiber 09:55, wörtlich „chatname: Opus Trading Bot setup“ — weicht vom Soll „Opus Trading Bot-10Okt2026“ ab; nichts umbenannt (Nachtrag 09:58). Die Form der ersten Nachricht ist für diesen Umzug **nicht geändert** (kein gemessener Hebel auf den Titel; die Anweisung 09:16 lässt unter der Namenszeile nur zu, welche Datei zu lesen ist). Die Regel aus Umzug 09:52, Block 6 gilt weiter und steht in der Eröffnung. Umzug 10.10.2026, 16:36, Block 6: Karte „Wie heisst dieser Chat gerade in der App (genauer Wortlaut)?“, Antwort wörtlich „Opus Trading Bot setup“ — weicht zum zweiten Mal vom Soll ab, nichts umbenannt; die Form der ersten Nachricht ist nicht geändert. Nachtrag 10.10.2026, 22:03: Frage 1, wörtlich: „Wie heisst dieser Chat gerade in der App (genauer Wortlaut)?“ Antwort, wörtlich: „Opus Trading Bot setup“ — Soll „Opus Trading Bot-10Okt2026“; weicht zum dritten Mal ab (nach 09:52 und 11:31). Frage 2, wörtlich: „Wie heisst der Fable-Chat zur Anfrage 10.10.a in der App (genauer Wortlaut)?“ Antwort, wörtlich: „Fable Trading Bot Übergabe“ — Soll „Fable Trading Bot-10Okt2026“; erster Fable-Chat nach der Regel, weicht ab. Nichts umbenannt; die Form der ersten Nachricht ist nicht geändert.
~~~

#### U4 — UMZUG.md, Abschnitt 3: Umzug über Chrome als Regel (Stück 38)

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦⭐⭐ **Gilt seit 05.10.2026, 23:58 (Betreiber, „zukünftig“):**⟧

Am HEAD `6d700d4`: Anker Z. 108 · eingefügt +2 · Bestand — · Quelle: UEBERGABE Z. 3474, 3475, 3493, 3549, 3558, 3560

~~~
⭐⭐ **Gilt seit 11.10.2026 (Betreiber, Karten 11.10.2026: „Ja, als Probe (Recommended)“, danach „Ja, zur Regel (Recommended)“):** Den Umzug macht der steuernde Chat über Chrome: Ein Helfer des alten Chats legt den neuen Chat an (Projekt Trading Bots, Modell wie bisher), schickt die erste Nachricht nach Abschnitt 6, benennt ihn um, heftet ihn an und löst den alten; der Betreiber bestätigt im neuen Chat nur die Ordner-Freigabe. Scheitert ein Schritt, bekommt der Betreiber den Eröffnungstext wie bisher als Kopierblock. Wo dieses Dokument dem Betreiber den Eröffnungstext oder den kurzen Text als Kopierblock gibt (Abschnitt 4, „Als Kopierblock, als ERSTE Nachricht im laufenden Chat“; Abschnitt 6, „Im Chat steht nur der kurze Text als Kopierblock“), ist das seither der Rückfall; die erste Nachricht selbst bleibt, wie Abschnitt 6 sie festlegt. Unverändert: Umgezogen wird nur mit dem Ja des Betreibers (Absatz darüber); eine geplante Aufgabe wird dafür nie angelegt; die Freigabeabfrage für Ordner beantwortet der Chat nie selbst. Die Karte zum Chatnamen entfällt; den Namen liest der Helfer in Chrome ab, er steht in der Übergabe. *Anlass: Frage des Betreibers vom 11.10.2026, 00:11; Probe beim Umzug 11.10.2026, 01:24 (`UEBERGABE.md`, Zusatz 01:30); beim ersten Lauf fehlten Anheften und Lösen (Nachtrag 11.10.2026, 01:38).*
~~~

#### B1 — BACKLOG, Abschnitt 5: Aus der Abnahme TB-147 (10.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +5 · Bestand S35, S43, S44 · Quelle: UEBERGABE Z. 3091, 3092

~~~
### Aus der Abnahme TB-147 (10.10.2026) — eingetragen mit TB-152

- **Abnahme, enger Helfer ABNAHME147, nur lesend** (20 Aufrufe; Bericht `logs/steuernder_chat/2026-10-10_BERICHT_ABNAHME147.md`, md5 `5fd2da939c709005dd7141210d818d3c`). Aussagen des Helfers: Schritt 0 enthält genau die drei Dateien, kein späterer Commit fasst Verbotenes an, 13 von 13 alten Belegen md5-gleich; Soll gegen Beleg 16 von 19 gleich, 3 ohne Beleg; Zeilenbilanz selbst gerechnet +532/−2 · +156/0 · +98/0 · +37/0; Block EM in `JOURNAL.md` Z. 10332–10375, ohne J1 zeichengleich `j_block.md`; Ergebnis 6 von 6 Teilen, 23 von 24 Angaben. Kernzahlen des steuernden Chats 08:42: `ARBEITSWEISE.md` 2 531 Z., `UMZUG.md` 392 Z., `BACKLOG.md` 395 Z., je md5 wie Soll im Auftrag Z. 97; `JOURNAL.md` 10 713 Z.; `t147_f_porcelain.txt` 0 B. (UEBERGABE, Nachtrag 10.10.2026, 08:43)
- **Abweichungen aus der Abnahme:** A1 — `JOURNAL.md` Z. 10336 sagt „jeder Shell-Befehl stand wörtlich im Auftrag“; das Ergebnis Z. 69 meldet einen lesenden Befehl (`grep`, `wc` auf `AKTUELLER_AUFTRAG.md`) ausserhalb der Codeblöcke und vor dem Lesen des Auftrags. Der Satz steht unberichtigt; offen: Berichtigung als Nachtrag in einem späteren Journalblock. A3 — derselbe Befehl, von der Sitzung selbst gemeldet, gegen Regel 1 des Auftrags (Z. 13), nach Wortlaut kein Abbruchkriterium. Klein: `JOURNAL.md` Z. 10348 trägt „in diesem BACKLOG“. Schritt A: Prozesszeile mit `--permission-mode manual`; ihren Modus kennt die Sitzung nach eigener Aussage nicht. (UEBERGABE, Nachtrag 10.10.2026, 08:43)
~~~

#### B2 — BACKLOG, Abschnitt 5: Aus der Abnahme TB-148 (10.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +6 · Bestand S36, S45 · Quelle: UEBERGABE Z. 3166, 3167, 3168

~~~
### Aus der Abnahme TB-148 (10.10.2026) — eingetragen mit TB-152

- **TB-148 abgenommen mit Befunden** (Urteil des steuernden Chats; HEAD `15775a7`). Zwei Helfer, nur lesend: ABNAHME148_A (09:58–10:05, 23 Aufrufe; Bericht 18 706 B, md5 `c7b60a97b9458ad946e3a6dc5b2c4255`) und ABNAHME148_B (09:58–10:09, 30 Aufrufe; 24 979 B, md5 `c87c10d5c39aa3e942e1159223216eb7`); Kopien `logs/steuernder_chat/2026-10-10_BERICHT_ABNAHME148_A.md` und `_B.md`. Kernzahlen selbst nachgerechnet 10:05 und 10:09 (8 Commits, md5 von Auftrag und Ergebnis, 12 Belege, Journal +31/−0, `leseprotokoll.md` in `d9f8489` +75/−73, drei Kernstellen aus B im Wortlaut). (UEBERGABE, Nachtrag 10.10.2026, 10:13)
- **Form (A):** Commits 8 von 8 wie verlangt; Soll 11 von 13 bestätigt, 2 nicht prüfbar (`cmp` ohne Ausgabe steht in keinem Beleg); Leseprotokoll md5 und Zeilen 70 von 70; kein verbotener Pfad; keine Zahl aus einem Lauf. **Abweichung:** `d9f8489` änderte im Leseprotokoll 13 Zellen „Zeilenbereich“ und 26 Zellen „Messpunkt“, das Ergebnis nennt es unter „Abweichungen“ nicht. Grenzfälle: Ergebnis Z. 154 (drei Rasterwerte eines Parameters im Klartext), Z. 65 (Beispiel-Zeitstempel aus einem Kommentar). (UEBERGABE, Nachtrag 10.10.2026, 10:13)
- **Inhalt (B):** 167 Zitate geprüft (M4 34, M5 25, M2 38, M3 49, M1 21), keines fehlt am HEAD; 2 nicht geprüft (M4-1, M4-2, keine Code-Datei). **M4: bei allen neun Bots „erschlossen“** (durch Lesen, kein Lauf); eine übersehene Vergleichsstelle gegen den Handelbar-Tag fand die Suche in den genannten Dateien nicht. **M5 bestätigt:** `bh_tagesrenditen` liefert den Tag nicht; Kernstelle `research/vorregistrierung/benchmark.py:276`. **M2:** 11 Treffer zu Zeitzonen-Wörtern in 7 von 45 Dateien, keiner betrifft `open_time` oder den Schnitt. **Befunde:** falsche Zeilenangabe `strategies/elliott_wave_stocks/zigzag_indicator.py:134-136` (tragend Z. 159–163); `research/faltenplan_neun/faltenplan_neun.py:197-201` und `:220-224` beschreiben `start_i` anders, als es am HEAD in den zwei `backtest_breakout.py` steht (Z. 129 und Z. 170); nicht genannt: Vergleich gegen `entry_cutoff` in drei Krypto-Backtests, bei gleichen Schlüsseln entscheidet die Listenreihenfolge (`shared/zuteilung.py:577`, `:540`; `research/mtm_drawdown/mtm_kern.py:107-111`); „In einfacher Sprache“ lässt bei M4 und M3 (b) den Vorbehalt „erschlossen“ weg. Das Ergebnis selbst: kein Suchwerkzeug in der Sitzung, Aussagen „an keiner Stelle“ sind erschlossen. (UEBERGABE, Nachtrag 10.10.2026, 10:13)
~~~

#### B3 — BACKLOG, Abschnitt 5: Aus der Abnahme TB-149 (10.10.2026), neun Befunde

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +7 · Bestand S37, S38 · Quelle: UEBERGABE Z. 3261, 3262, 3263, 3264

~~~
### Aus der Abnahme TB-149 (10.10.2026), neun Befunde — eingetragen mit TB-152

- **Abnahme:** Helfer ABNAHME149_A (Form, 22 Aufrufe) und ABNAHME149_B (Inhalt, 24 Aufrufe), gleichzeitig, nur lesend; ihre Aufträge baute der Helfer VORBAU_ABNAHME149 (17 Aufrufe, `sc/werk/schreibe_abnahme149.py`), **nicht gegengelesen**. Berichte, Aufträge und Skript unter `logs/steuernder_chat/2026-10-10_{BERICHT,HELFER,WERK}_*`. (UEBERGABE, Nachtrag 10.10.2026, 12:59)
- **Kernzahlen, selbst gemessen (12:57):** Register 11 733 → 11 920, +187 −0, 22 Einschübe, `## 56.` einmal, sha256 `b2d56949…`, md5 `4359577a…`; BACKLOG 395 → 415, +20 −0, ein Einschub; T4 239 683 B, T5 145 682 B, fünf Teile, 57 Abschnittsdateien; Journal 10 792 Zeilen, `## EO` einmal; Index 560 Zeilen; Dialog-Index 73 → 74 Zeilen; 65 Belege, `d3_porcelain.txt` 0 B; `origin/main` lokal = HEAD; Arbeitsbaum sauber. Nicht selbst gemessen: 31 Marken an 21 Orten (Helfer B: 31/31; Abschnitt 56 93/93 Zeilen, davon 12 Zitatzeilen mit Vorsatz „> “). (UEBERGABE, Nachtrag 10.10.2026, 12:59)
- **Befunde, einzeln** (E = `docs/ERGEBNIS_TB-149_register_fable_09a.md`): (1) `a_commit.txt` trägt nur `git show --stat`; das nach Auftrag Z. 238 davor verlangte `git status --porcelain` steht in keinem Beleg, E nennt es nicht — Abweichung vom Auftrag, ungenannt. (2) E:7 beschreibt den Abgabe-Commit ohne die vier mitcommitteten Belege — Lücke in der Beschreibung. (3) E:10 „bis nach 12:40“, letzter Commit 12:38:57 — Uhrzeit ohne Beleg. (4) E:115 „Der neue Wert steht nur hier“ — er steht auch in `0b_nachher.txt:9` und `:38`; Aussage falsch. (5) E:8 „Nach jedem Commit gepusht, jeder Push im ersten Versuch“ — kein Beleg. (6) E:262 „Alle Prüfungen … grün“ — `0b_nachher.txt` zeigt Sonde rc 2 und registerbericht rc 1 (beide wie im Ausgang, im Auftrag Z. 60 so erwartet); geglättet. (7) Die Ausgabe von `registerbericht.py --pruefen` liegt nur im Scratch. (8) E:136: `test_vorregistrierung` lief im Hintergrund vor Commit A; E nennt es; im Auftrag kein Verbot gefunden (Suche nach „Hintergrund“ ohne Treffer) — Hinweis. (9) E hat keinen Abschnitt „Abweichungen“. Zitate: 64, streng 57 gefunden; die sieben übrigen sind drei Verweise, drei an anderer Quelle bestätigte Wortlaute und ein über drei Zeilen umbrochener — kein fehlendes Zitat. (UEBERGABE, Nachtrag 10.10.2026, 12:59)
- **Nicht geprüft:** übrige Zeilen von 56.7 und ganz 56.8; ob Marke 23 „nach der Tabelle“ steht; Inhalt der 20 umgestellten Skripte; Push je Commit und am Server. (UEBERGABE, Nachtrag 10.10.2026, 12:59)
~~~

#### B4 — BACKLOG, Abschnitt 5: Aus der Abnahme TB-150 (10.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +4 · Bestand S39 · Quelle: UEBERGABE Z. 3083

~~~
### Aus der Abnahme TB-150 (10.10.2026) — eingetragen mit TB-152

- **Abnahme an Stichproben, zwei enge Helfer, nur lesend** (je 29 Aufrufe; Berichte `logs/steuernder_chat/2026-10-10_BERICHT_ABNAHME150_A.md`, md5 `612e7101d3de586446f7d59dfe285a49`, und `…_B.md`, md5 `8be61096535bcd6a8c0047c07d6af8c8`; Aufträge daneben als `2026-10-10_HELFER_ABNAHME150_*.md`). Aussagen der Helfer: Stand bestätigt; Paket 7 bestätigt (88 von 88 Zitaten zeichengleich; nicht geprüft 55 Verweise, Zuschreibungen, Vollständigkeit); Paket 8: 161 Zeilen bestätigt, „203 nur genannt“ (Ergebnis Z. 3258, 3329) gegen 195 in der Arbeitsdatei; Stichproben 60 von 60, Code-Fundstellen zu M1 bis M5 20 von 20. Abweichungen: 12 Zitate mit `'` statt Backtick; Paket 4 mit 20 von 31 Klammern auf 150 Zeichen gekürzt (Auftrag: ganz, bis 600; ungekürzt in `paket_04.md` im Archiv); `git status --short` in der Sitzung (Auftrag Z. 10 nennt es nicht); eine Sichtschutz-Berührung, vom Ergebnis selbst gemeldet (Z. 3647: Zeilen aus `ergebnisse/` und `daten/` in einer Suchausgabe, nach Bericht nur ein Datum). Kernzahlen des steuernden Chats 08:13: md5 des Ergebnisses, 27 und 4 Klammern, Wortlaut Z. 3647, „203“ in Z. 3258. (UEBERGABE, Nachtrag 10.10.2026, 08:15)
~~~

#### B5 — BACKLOG, Abschnitt 5: Entscheid des Betreibers zum Schnitt der Registerkopie (10.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +4 · Bestand S31 · Quelle: UEBERGABE Z. 3231, 3230

~~~
### Entscheid des Betreibers zum Schnitt der Registerkopie (10.10.2026) — eingetragen mit TB-152

- **Schnitt der Registerkopie (Entscheid (a)):** dieselbe Karte, wörtlich „Werkzeug schneiden lassen (Empfohlen)“ — nichts ändern; reisst T4, wandert Abschnitt 53 nach T5, der Registerauftrag führt die Spalte T im Index nach. „Dieselbe Karte“ ist die Karte zur Freigabe TB-149: Karte gestellt nach 11:24, Antwort eingetragen 11:26, wörtlich „Ja, freigeben (Empfohlen)“; Kartentext im Auftrag Z. 22 und in `logs/steuernder_chat/2026-10-10_KARTE_FREIGABE_TB-149_187_0_und_Schnitt.txt` (UEBERGABE, Umzug 10.10.2026, 11:31, Block 6).
~~~

#### B6 — BACKLOG, Abschnitt 5: Fehler Nr. 38 bis 54, Chatname, Ort der Eröffnungsdatei (09.–11.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +8 · Bestand S41, S28–S30, S01–S14 · Quelle: UEBERGABE Z. 2912, 2948, 2967, 3046, 3047, 3059, 3081, 3093, 3123, 3176, 3220, 3240, 3265, 3271, 3295, 3297, 3311, 3336, 3344, 3345, 3428, 3433, 3434, 3487, 3528, 3532, 3641

~~~
### Fehler Nr. 38 bis 54, Chatname, Ort der Eröffnungsdatei (09.–11.10.2026) — eingetragen mit TB-152

- **Fehler Nr. 38 bis 44 und Nr. 47 bis 54:** Regeln in `ARBEITSWEISE.md` Abschnitt 0, eingetragen mit TB-152; Nr. 39 in der berichtigten Fassung (UEBERGABE, Umzug 09.10.2026, 22:41, Block 7 Nr. 38; Umzug 10.10.2026, 07:38, Block 7 Nr. 39; Nachtrag 09.10.2026, 23:51; Nachtrag 10.10.2026, 08:15; Nachtrag 10.10.2026, 08:43; Nachtrag 10.10.2026, 10:30; Nachtrag 10.10.2026, 12:59; Nachtrag 10.10.2026, 13:30; Umzug 10.10.2026, 16:36, Block 7 Nr. 49 und 50; Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 7 Nr. 52 und 53; Umzug 11.10.2026, 01:24, Block 7 Nr. 54). **Nr. 45 und 46** haben keine Zeile in Abschnitt 0 — ihre Quelle nennt keine Regel mit „⇒“; Nr. 44 bis 46 stehen im Wortlaut im Journalblock zu TB-152. Stand der Zählung: „Fehler ab Nr. 57“ (UEBERGABE, Nachtrag 11.10.2026, 09:08, Berichtigung 09:10).
- **Weitere Zeilen in Abschnitt 0, eingetragen mit TB-152:** Regeln, „gelernt“ und „so getragen“ aus den Umzügen 09.10.2026, 22:41 bis 10.10.2026, 16:36, je mit Fundstelle in der Spalte „steht in“.
- **Chatname:** Die zwei Anweisungen des Betreibers vom 10.10.2026, 09:16 und 09:38 stehen mit TB-152 in `ARBEITSWEISE.md` Abschnitt 0 (Gruppe „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“) und in `UMZUG.md` Abschnitt 6. Stand: Frage 1, wörtlich: „Wie heisst dieser Chat gerade in der App (genauer Wortlaut)?“ Antwort, wörtlich: „Opus Trading Bot setup“ — Soll „Opus Trading Bot-10Okt2026“; weicht zum dritten Mal ab (nach 09:52 und 11:31). Frage 2, wörtlich: „Wie heisst der Fable-Chat zur Anfrage 10.10.a in der App (genauer Wortlaut)?“ Antwort, wörtlich: „Fable Trading Bot Übergabe“ — Soll „Fable Trading Bot-10Okt2026“; erster Fable-Chat nach der Regel, weicht ab. Nichts umbenannt; die Form der ersten Nachricht ist nicht geändert. Kopie: `logs/steuernder_chat/2026-10-10_CHATNAME_ergebnis_umzug_1636.txt`. Erschlossen, nicht gemessen: Es gibt einen Fable-Chat zur Anfrage 10.10.a; ob die Anfrage gesendet ist, zeigt erst Fables Antwort. (UEBERGABE, Nachtrag 10.10.2026, 22:03)
- **Ort der Eröffnungsdatei:** Die Datei liegt seit TB-151 verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und in der Ablage unter `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`; beim Umzug ersetzt der alte steuernde Chat beide, md5 gleich; die Kopie unter `logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md` entfällt dann als Ort (Vorgabe des steuernden Chats, 10.10.2026, vorläufig; UEBERGABE, Nachtrag 10.10.2026, 22:20; Umzug 10.10.2026, 22:55, Block 6). Klarstellungen dazu stehen mit TB-152 in `ARBEITSWEISE.md` Abschnitt 0 (zwei Zeilen) und 23.2 (Klasse B2 Stand) und in `UMZUG.md` Abschnitt 4, Schritt 6, und Abschnitt 6.
- **Nicht in TB-152** (Gründe im Auftrag `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md`, Abschnitt „Nicht in TB-152“): „Zu prüfen, nicht untersucht“ (UEBERGABE, Umzug 10.10.2026, 16:36, Block 4); „Entscheide des Betreibers ohne Eile“ (UEBERGABE, Umzug 10.10.2026, 07:38, Block 4); „Später“ mit den 27 Formhinweisen aus TB-146 (UEBERGABE, Umzug 10.10.2026, 07:38, Block 4); der `jq`-Befehl zur Ampel im Wortlaut (UEBERGABE, Umzug 10.10.2026, 11:31, Block 7); V6 „„erfüllt“ nur mit Nachweis der Sitzung“ — V6 kommt nicht ins allgemeine Regelwerk: Die Quelle (`UEBERGABE.md` Z. 2967) gilt dem Registerauftrag TB-149; V6 geht als Vorgabe in den Bau von TB-154 (`UEBERGABE.md` Z. 3487 und Z. 3528). (UEBERGABE, Nachtrag 09.10.2026, 23:53 (der erste dieser Uhrzeit: „Abnahme der Antwort 09.10.a: Befunde im Wortlaut (für Register 56.7); Vorgaben zum Registerauftrag TB-149“)).
~~~

#### B7 — BACKLOG, Abschnitt 5: Kerzenformationen: Prüfauftrag und Entscheid des Betreibers (10.–11.10.2026)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD `6d700d4`: Anker Z. 411 · eingefügt +7 · Bestand — · Quelle: UEBERGABE Z. 3451, 3452, 3459, 3460, 3461

~~~
### Kerzenformationen: Prüfauftrag und Entscheid des Betreibers (10.–11.10.2026) — eingetragen mit TB-152

- **Neuer Prüfauftrag des Betreibers: Kerzenformationen:** Antwort des Betreibers, wörtlich: „Wäre es eventuell sinnvoll die Bots würden auch Kerzenformationen beobachten und danach abwägen oder handeln es gibt sicherlich noch viele weitere Kerzenformationen, die ein gewisses Handelssignal auslösen. Ich habe ein Beispiel angehängt. Prüfe diese Idee ob dies nicht zufällig irgendwo entweder mit integriert werden kann oder man auf dieser Grundlage weitere Strategien oder Boards aufbauen kann. Prüfe zudem, welche Kerzenformationen es gibt und wie zuverlässig aussagekräftig diese sind und ob man diese verwenden kann“. Das Beispiel kam um 23:44 als Bild (UEBERGABE, Zusatz 10.10.2026, 23:56 zum Umzug 22:55)
- **Entscheid des Betreibers:** Frage, wörtlich: „Wie soll es mit der Idee „Kerzenformationen“ weitergehen?“ Antwort des Betreibers, wörtlich: „Kleiner Messauftrag vor dem Tag“ (UEBERGABE, Zusatz 11.10.2026, 00:03 zum Umzug 22:55)
- **Nummer und Reihenfolge (Vorgabe des steuernden Chats, vorläufig):** TB-153 Messauftrag Kerzenformationen. (1) Verfahrensfrage an Fable, mit der nächsten Anfrage an den neuen Fable-Chat; (2) Definition festlegen, bevor Daten gelesen werden. Kandidaten aus der Recherche: H1 (Three Outside Up und Morning Star im Abwärtstrend gegen alle übrigen Tage mit derselben Trendbedingung, S&P 500, Tag) und H3 (Krypto auf 4h und Tag, Definition ohne Kurslücke). **Nicht vor dem Tag:** H2 (Muster als Filter auf vorhandene Trade-Listen) — das wäre eine Wahl nach dem Ergebnis. (3) Bestand (ob die Aktien-Dateien die Eröffnung führen — nicht belegt), dann Bau durch einen Helfer und Gegenleser, wie jeder Mac-Auftrag (UEBERGABE, Zusatz 11.10.2026, 00:03 zum Umzug 22:55)
- **Recherche:** `docs/projektfuehrung/RECHERCHE_2026-10-10_kerzenformationen.md` (UEBERGABE, Zusatz 10.10.2026, 23:56 zum Umzug 22:55)
~~~

#### J1 — JOURNAL: erste Zeile des Nachtrags im neuen Block der Sitzung

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

Kein Anker: `WZ journal` setzt J1, dahinter die 20 Zeilen `- …` aus B1 bis B7 und dahinter J2 vor `### Was gemessen ist` des Blocks. Bestand S42 · Quelle: UEBERGABE Z. 3123, 3220, 3295

~~~
**Nachtrag des steuernden Chats zum Stand vor TB-152, wie in `BACKLOG.md` Abschnitt 5 eingetragen (aus `UEBERGABE.md`, Nachträge und Umzüge vom 09.10.2026, 22:03 bis zum Nachtrag 11.10.2026, 01:38; die letzten drei Zeilen stehen nur hier: Fehler Nr. 44 bis 46 im Wortlaut, zwei Sätze aus dem Umzug 10.10.2026, 07:38 und die Berichtigung zu Block EM):**
~~~

#### J2 — JOURNAL: drei Zeilen, die nur im Journal stehen (Fehler Nr. 44 bis 46; Umzug 07:38; Berichtigung zu Block EM)

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

Kein Anker: `WZ journal` setzt J1, dahinter die 20 Zeilen `- …` aus B1 bis B7 und dahinter J2 vor `### Was gemessen ist` des Blocks. Bestand S08, S09, S10, S49, S43 · Quelle: UEBERGABE Z. 3176, 3238, 3177, 3061, 3092

~~~
- **Fehler Nr. 44 bis 46 im Wortlaut — Nr. 44 hat mit TB-152 eine Zeile in `ARBEITSWEISE.md` Abschnitt 0; Nr. 45 und Nr. 46 haben keine, ihre Quelle nennt keine Regel mit „⇒“:** **Fehler Nr. 44 (dieser Chat):** Im Nachtrag 10:13 und in zwei Antworten an den Betreiber (nach 10:13 und nach 10:17) stand, die fünf Zusatzzeilen lägen über der Luft von T4 und der Schnitt müsse vor dem Eintrag entschieden sein. **Falsch:** 56.8 liegt in Abschnitt 56 und damit in T5 (54–56), nicht in T4 (43–53). Gefolgert aus „T4 nur 313 Bytes Luft“, ohne die Stelle zu lesen, die den Zuschnitt regelt (`docs/werkzeuge/registerkopie.py` Z. 71 und Z. 124–137). Dem Betreiber berichtigt (Antwort nach 10:21). **Regel daraus:** Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschnitt liegt. **Nr. 44** (Nachtrag 10:30): „passt nicht in T4“ gefolgert, ohne zu messen, in welchem Teil Abschnitt 56 liegt. **Nr. 45:** in der Vorgabe `berichtigung5.json` „abgegeben mit `15775a7`“ geschrieben, obwohl die Commit-Betreffs seit 09:54 vorlagen (Abgabe ist `d9f8489`); vom engen Gegenleser gefunden, berichtigt. **Nr. 46:** eine Uhrzeit („10:11“) ohne Messung in den Nachtrag 10:13 geschrieben. **Berichtigung zum Nachtrag 10:13:** „am Wortlaut gelesen, 10:11“ war nicht gemessen; richtig: zwischen 10:10 und 10:12. (UEBERGABE, Nachtrag 10.10.2026, 10:30; Umzug 10.10.2026, 11:31, Block 7)
- **Aus dem Umzug 10.10.2026, 07:38, Block 7, nur hier:** Zwei Nachträge tragen dieselbe Uhrzeit (23:53). Die Ampel wurde zwischen 23:54 und 01:06 nicht gemessen, sieben Antworten nannten den alten Wert mit Vermerk. (UEBERGABE, Umzug 10.10.2026, 07:38, Block 7)
- **Berichtigung zu Block EM (Abnahme TB-147, A1):** In Block EM (`JOURNAL.md` Z. 10336 am HEAD `6d700d4`) steht: „In TB-147 hat Claude Code bis zum Schreiben dieses Blocks keinen Aufruf abgelehnt und keine Bestätigung verlangt; jeder Shell-Befehl stand wörtlich im Auftrag.“ Der zweite Halbsatz trifft nicht zu: Das Ergebnis (`docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md` Z. 69) meldet einen lesenden Shell-Befehl ausserhalb der Codeblöcke und vor dem Lesen des Auftrags (`grep` und `wc` auf `AKTUELLER_AUFTRAG.md`); dieselbe Zeile sagt: „Danach lief kein Shell-Befehl, der nicht wörtlich in einem `sh`-Block steht.“ Block EM bleibt unverändert, diese Zeile ist die Berichtigung. Den Halbsatz „jeder Shell-Befehl stand wörtlich im Auftrag“ trägt auch Block EN (TB-148, `JOURNAL.md` Z. 10380); zu TB-148 liegt dazu kein Befund vor, geprüft ist es nicht. Sonst trägt ihn keine Zeile in `JOURNAL.md`, `ARBEITSWEISE.md`, `UMZUG.md` und `BACKLOG.md`; `UEBERGABE.md` zitiert ihn (UEBERGABE, Nachtrag 10.10.2026, 08:43).
~~~

## Anhang B — Werkzeug und Sollwerte

Das Werkzeug dieses Auftrags entsteht in 0a aus `docs/belege/TB-146/tb146_einfuegen.py` (sha256 `09d57b7a8befc5a067210f62b2f378fb3f1334f90ddbaf318b2d27f20bd7660e`; Wortlaut: Auftrag TB-146, Anhang B) durch die 11 Ersetzungen unten, in dieser Reihenfolge; jede nennt ihre Trefferzahl, der Befehl in 0a prüft sie und bricht bei jeder Abweichung ab. In Worten: die Namen (Auftrag, Ergebnis, Belegordner, Kopfzeilen der Ausgaben) lauten auf TB-152; Stücke, deren Kennung mit J beginnt, haben keinen Anker und werden nicht eingefügt; `journal` setzt J1, dahinter die Zeilen `- …` aller B-Stücke und dahinter J2, und es prüft, dass jedes B-Stück genau einmal im BACKLOG steht. Sonst ist es das Werkzeug aus TB-146: Aufrufe, Rückgabewerte und Ausgabezeilen wie dort. sha256 des abgeleiteten Werkzeugs: `d5855393b5b138ef90b6ccfb40b5e70527a651057748c2abaa6776b6f41f70f5`.

### Unterschiede zum Werkzeug TB-146 (maschinenlesbar)

```json
{
 "quelle": "docs/belege/TB-146/tb146_einfuegen.py",
 "quelle_sha256": "09d57b7a8befc5a067210f62b2f378fb3f1334f90ddbaf318b2d27f20bd7660e",
 "ersetzungen": [
  [
   "MAC_TB-146_regelwerk_dokunachtrag_0910.md",
   "MAC_TB-152_regelwerk_nachtrag_1010.md",
   1
  ],
  [
   "ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md",
   "ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md",
   1
  ],
  [
   "TB-146",
   "TB-152",
   9
  ],
  [
   "tb146",
   "tb152",
   1
  ],
  [
   "# tb152_einfuegen.py - Werkzeug zum Auftrag TB-152, ausgelesen aus Anhang B.\n# Abgeleitet von tb145_einfuegen.py (TB-145, Anhang B), ohne Direktiven: jedes Stueck\n",
   "# tb152_einfuegen.py - Werkzeug zum Auftrag TB-152, abgeleitet aus dem Werkzeug zum Auftrag davor\n# (tb146_einfuegen.py; Ersetzungen im Auftrag, Anhang B), ohne Direktiven: jedes Stueck\n",
   1
  ],
  [
   "alle Stuecke ausser J1\n",
   "alle Stuecke ausser J1 und J2\n",
   1
  ],
  [
   "assert s[\"id\"] == \"J1\" or (s[\"art\"]",
   "assert s[\"id\"][0] == \"J\" or (s[\"art\"]",
   1
  ],
  [
   "if s[\"id\"] != \"J1\"]",
   "if s[\"id\"][0] != \"J\"]",
   1
  ],
  [
   "        if s[\"id\"] == \"J1\":\n            continue",
   "        if s[\"id\"][0] == \"J\":\n            continue",
   1
  ],
  [
   "    zl, b, b1 = zeilen(JOU), zeilen(blockpfad), fertig(st[\"B1\"])\n    j1 = fertig(st[\"J1\"]) + [x for x in b1 if x.startswith(\"- \")]\n",
   "    zl, b, bs = zeilen(JOU), zeilen(blockpfad), [fertig(st[i]) for i in st if i[0] == \"B\"]\n    j1 = fertig(st[\"J1\"]) + [x for t in bs for x in t if x.startswith(\"- \")] + fertig(st[\"J2\"])\n",
   1
  ],
  [
   "(\"B1 steht genau einmal im BACKLOG (Schritt E gelaufen)\", len(vorkommen(zeilen(BACK), b1)) == 1),",
   "(\"jedes B-Stueck steht genau einmal im BACKLOG (Schritt E gelaufen)\", all(len(vorkommen(zeilen(BACK), t)) == 1 for t in bs)),",
   1
  ]
 ]
}
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
  "R25",
  "R08",
  "R09",
  "R10",
  "R11",
  "R12",
  "R13",
  "R14",
  "R15",
  "R16",
  "R17",
  "R18",
  "R19",
  "R20",
  "R21",
  "R24",
  "R23",
  "R22",
  "U1",
  "U2",
  "U3",
  "U4",
  "B1",
  "B2",
  "B3",
  "B4",
  "B5",
  "B6",
  "B7",
  "J1",
  "J2"
 ],
 "numstat": {
  "docs/projektfuehrung/ARBEITSWEISE.md": [
   43,
   0
  ],
  "docs/projektfuehrung/BACKLOG.md": [
   41,
   0
  ],
  "docs/projektfuehrung/UMZUG.md": [
   47,
   0
  ]
 },
 "j1_zeilen": 24,
 "kennung": "EQ"
}
```
