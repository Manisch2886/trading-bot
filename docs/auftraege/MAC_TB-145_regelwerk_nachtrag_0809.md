# TB-145 Regelwerk-Nachtrag 08.–09.10.2026 — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 09.10.2026** (Helfer BAU145, per Skript aus Bausteinen und 31 fertigen Stücken), gebaut ausserhalb des Repos (Entscheid W1), nur lesend am Repo; alle Einfügungen an Kopien simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht.

**Sitzungstitel:** `TB-145` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `80c5a9b116e0b02b240568d35232b490ee07bfde` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-145`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-145_regelwerk_nachtrag_0809.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-145/tb145_einfuegen.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-145/`. **Ergebnis:** `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** Die Regeln, Berichtigungen und Stände vom 08. und 09.10.2026 stehen im Regelwerk: 30 Stücke in sieben Dateien (77 Zeilen, nur eingefügt) und der Journalblock der Sitzung mit dem Nachtrag J1. Dazu schliesst die Sitzung bis zu vier tote Terminal-Fenster (Schritt W).
**Bauart wie TB-141** (`docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md`: Schritt 0, Einfügen per Werkzeug, Nachweis, Abgabe) **und TB-144** (`docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md`: Modus-Messung, BACKLOG-Direktiven, Journalblock), mit den Werten von hier; bei Widerspruch gilt dieser Auftrag. **Anders:** Das Werkzeug gibt nach stdout aus (die Sitzung leitet in den Beleg um), prüft alle Stücke, bevor es eine Datei schreibt, und schreibt an Ort und Stelle — es legt keine Hilfsdatei an, auch nicht im Auslöserordner. Die Sitzung ändert kein Werkzeug des Repos.
**Reihenfolge:** Schritt 0 → A (Modus) → E (Einfügen, Commit) → W (tote Fenster) → J (Journalblock) → F (Nachweis, Ergebnis, Abgabe).

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — der Auftrag fügt nur Dokumentation ein. Am HEAD gemessen: Register `docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 10 „Die Sperrliste“ (Z. 971–1177) und die Tabelle „Die Sperrliste, Stand 18.09.2026“ in `ARBEITSWEISE.md` (Z. 1141–1150) enthalten `projektfuehrung`, `auftraege`, `werkzeuge`, `_ausloeser`, `LIESMICH`, `.gitignore` und `docs/` je 0-mal.

**Lesart des steuernden Chats, vorläufig:** Die Berichtigung in der Wächter-LIESMICH (L1) und die zwei Zeilen in `docs/auftraege/_ausloeser/.gitignore` (A1) ändern den Wächter nicht.

**Schritt W** ist für `21346`, `21349`, `21560` von der Karte des Betreibers vom 09.10.2026 gedeckt (Wortlaut `docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md` Z. 14: „Schliessen der vier Fenster 21040, 21346, 21349, 21560 (nur wenn nichts darin läuft)“); für `21627` (totes Fenster der Sitzung TB-144) ist es eine **Vorgabe des steuernden Chats, vorläufig** — dem Betreiber am 09.10.2026, 13:30 genannt („gilt, wenn du nicht widersprichst“), kein Widerspruch (UEBERGABE, Nachtrag 09.10.2026, 13:30, Zeile „Offen“, und der Nachtrag danach).

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | Zeilen + (numstat-Soll, entfernt 0) |
|---|---|---|
| `docs/projektfuehrung/ARBEITSWEISE.md` | R01, R02, R03, R04, R05, R06, R07, G1, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, G2, G3, G4, G5 | **36** |
| `docs/projektfuehrung/UMZUG.md` | U1 | **2** |
| `docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md` | S1 | **15** |
| `docs/projektfuehrung/BACKLOG.md` | B1 | **11** |
| `docs/projektfuehrung/JOURNAL.md` | J1 (Schritt J, mit dem Block der Sitzung) | Block + 9 + 1 + 3 |
| `docs/werkzeuge/sitzungswaechter/LIESMICH.md` | L1 | **2** |
| `docs/auftraege/_ausloeser/.gitignore` | A1 | **2** |
| `docs/auftraege/_ausloeser/LIESMICH.md` | A2 | **9** |
| neu: `docs/belege/TB-145/…`, `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md` | Belege, Werkzeug, Ergebnis | — |

In den acht Zieldateien wird **nur eingefügt;** keine bestehende Zeile wird geändert oder entfernt. Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (`UEBERGABE.md`, `AKTUELLER_AUFTRAG.md`, dieser Auftrag); das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`, `einschalten.sh`, die plist; `UEBERGABE.md`; Register; `research/`, `shared/`, `strategies/`; `docs/belege/TB-142/`, `docs/belege/TB-144/`; den Wortlaut eines Stücks umformulieren, kürzen oder zusammenlegen (Sachfehler: melden, nicht berichtigen). Nie `git add -A`, nie `git add .`; jeder Commit nennt seine Dateien mit Namen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD gemessen, Helfer BAU145): Ausgang der acht Zieldateien wie in 0b. Letzte Journalkennung EK (`JOURNAL.md` Z. 10241); vor `## Wiederkehrende Lehren` (Z. 10291) stehen `---` und eine Leerzeile. `UEBERGABE.md` im Arbeitsbaum (2562 Zeilen): „Nachtrag 09.10.2026, 13:30“ ab Z. 2552, daraus sieben Zeilen für B1. TB-144 schloss keines der alten Fenster (`docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md` Z. 55–64; `docs/belege/TB-144/d0_fenster.txt` Z. 120–135): 21346, 21349, 21560 je ein Tab, `processes` leer, Verlauf mit `exec claude`; 21040 trägt `login, -bash` und bleibt beim Betreiber; in 21627 lief die Sitzung TB-144 (`login, claude, caffeinate`), sie wurde 13:26 beendet (UEBERGABE Z. 2560). Terminal (PID 52069) lief seit 15.09.2026, 09:14.
- **Erschlossen:** launchd überwacht den Ordner `docs/auftraege/_ausloeser/` (plist Z. 23–26); A1 und A2 schreiben dort in zwei bestehende Dateien. Ob das den Wächter weckt, ist nicht gemessen. Geweckt ohne Auslöser schreibt er „Kein Ausloeser da. Nichts zu tun.“ ins Log (`starte_sitzung.sh` Z. 425).
- **Offen — misst die Sitzung, nie raten:** Modus der Sitzung (Schritt A) · ob Claude Code die direkten `osascript`-Aufrufe aus Schritt W ohne Rückfrage ausführt (TB-144 mass den Weg über eine Skriptdatei) · ob die vier Fenster noch stehen und leer sind (Schritt W) · Kennung des Journalblocks (erwartet EL) · ob Schritt E den Wächter weckt (nur melden).
- **Simulation des Helfers** (Kopien `git show HEAD:<pfad>`, `UEBERGABE.md` aus dem Arbeitsbaum; Linux, Python 3.10 mit `ast.parse(feature_version=(3,9))`): `probe` rc 0, jeder Anker genau eine Zeile; `einfuegen` rc 0; Zeilenbilanz per `diff` wie die Tabelle oben, 0 entfernte Zeilen; `vergleich` rc 0; zweiter Lauf rc 2; `journal` mit einer Attrappe als Block rc 0, Kennung EL, zweiter Lauf rc 2; Gegenproben (Anker fehlt, Anker doppelt, erste Zeile steht schon, UEBERGABE-Zeile geändert): nichts geschrieben. **Nicht simuliert:** `git diff` (nur mit einer Attrappe), `osascript`, Terminal, Claude Code, Python 3.9 selbst. Die Sitzung zählt selbst nach; ihre Zahl gilt.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-145/` entsteht:** `git status --porcelain > "$TMPDIR/tb145_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `80c5a9b116e0b02b240568d35232b490ee07bfde` und genau diese drei Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-145_regelwerk_nachtrag_0809.md
```

Dann das Werkzeug auslesen:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-145_regelwerk_nachtrag_0809.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
i = z.index("### Werkzeug")
a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
t = "\n".join(z[a + 1:b]) + "\n"
open(sys.argv[2] + "/tb145_einfuegen.py", "w", encoding="utf-8").write(t)
print("tb145_einfuegen.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb145_einfuegen.py 2e04e5a4c6841c997e84c9e70e7b8db9adb9c1b7d7afd69be6ca7851459b7a49`; sonst **ABBRUCH**. Commit `TB-145 Schritt 0: Stand des steuernden Chats 09.10.2026` mit genau den drei Pfaden (mit Namen hinzufügen), pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb145_0a.txt` unverändert nach `docs/belege/TB-145/0a_status.txt` (`cmp` gleich) und das Werkzeug nach `docs/belege/TB-145/tb145_einfuegen.py` (sha256 noch einmal). **Für jede Rohausgabe gilt:** Sie bleibt roh; die Beschreibung (was, Befehl, Bytes, Zeilen, md5) steht in `<name>.kopf.txt`. Ausgaben von `WZ` tragen ihre Kopfzeile selbst.

**0b. Ausgang** ⇒ `0b_ausgang.txt`: Zeilen und md5 der acht Zieldateien an ⟨S0⟩. Soll: `ARBEITSWEISE.md` 2 479 Z., `7c6b41f1ed3728e6b57058abca90b84d` · `UMZUG.md` 380 Z., `4c2dda0b24fa888107429a5aa1addd97` · `SITZUNGSWAECHTER_ausloeser_statt_tippen.md` 229 Z., `6daacc8f763fca9dcc2402a57356168f` · `BACKLOG.md` 375 Z., `e64195f08e152cb7702ec28a7b38aadf` · `JOURNAL.md` 10 628 Z., `6704e039b1e3e2793db20cf16e3e555d` · `sitzungswaechter/LIESMICH.md` 369 Z., `6fbed208259d1b9cd1f462d7e423755f` · `_ausloeser/.gitignore` 6 Z., `9a4e82c60cd3521c8e6f6e39f7537808` · `_ausloeser/LIESMICH.md` 14 Z., `53f240fe2e77d551b73a400ddcbae4e4`. Weicht eine ab: vermerken; die Anker entscheiden (Schritt E). Dazu `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`: Soll 622 Zeilen, md5 `464ac93c53829935e479c5f14121c574` — **diese Datei ändert TB-145 nicht;** ihr md5 wird in Schritt F noch einmal gemessen. Und `wc -l logs/sitzungswaechter/waechter.log` (Vergleichswert für Schritt E).

## Schritt A — Modus messen, bevor eingefügt wird

⇒ `a_modus.txt` (roh), die Aussage ⇒ `a_modus.kopf.txt`. Die eigene Sitzung (`EIGEN` wie in TB-144, M0):

```
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done
echo "EIGEN=$p"; ps -o command= -p "$p"
```

Soll: Die Prozesszeile trägt `--permission-mode manual`; sonst **ABBRUCH** — nichts ist eingefügt, das in der Meldung als Erstes sagen. Dazu die eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet. *Schützt:* Im Auto-Modus verwehrte Claude Code in TB-142 `osascript`-Aufrufe an Terminal (`docs/belege/TB-142/abbruch.txt` Z. 5–9); Schritt W braucht sie.

## Verfahren je Stück

Jedes Stück in Anhang A nennt Zieldatei, Art, Form und Anker; sein Text steht wörtlich zwischen zwei Zeilen `~~~`. **Anker:** ein Teil genau einer Zeile der Zieldatei (zwischen ⟦ und ⟧). **Art:** `nach` oder `vor` dieser Zeile. **Form `Zeilen`:** der Text ohne Leerzeile direkt an der Ankerzeile (eine Tabellenzeile bleibt in ihrer Tabelle). **Form `Block`:** genau eine Leerzeile davor und danach, keine verdoppelt. In B1 stehen sieben Zeilen als Direktive `⟦UEBERGABE: <Zeilenanfang> |md5 <12 Zeichen>⟧`: Das Werkzeug holt die eine Zeile mit diesem Anfang unverändert aus `UEBERGABE.md`, „Nachtrag 09.10.2026, 13:30“, und prüft ihren md5 (Wache); abgetippt wird nichts. J1 hat keinen Anker — es kommt mit dem Journalblock (Schritt J).

## Schritt E — Einfügen mit dem Werkzeug

**Probe.** `PY WZ probe; echo "rc $?"` ⇒ `e_probe.txt`. Soll rc 0: 30 Zeilen `<Id> · <Datei> · Anker Z. <n> · … · erste Zeile schon 0 · Anker in neuen Texten 0 · … · ok` (Ankerzeilen und Zeilen wie in Anhang A); sieben Zeilen `Datei … · Soll +<n> · gleich`; `Stuecke 30 · eingefuegte Zeilen 77`; Schlusszeile `Gesamt: wie Soll, nichts geschrieben (Probe)`. rc ≠ 0 ⇒ **ABBRUCH** (rc 3: die Zeile `ABBRUCH: …` nennt den Grund, etwa die md5-Wache einer Direktive).

**Einfügen.** `PY WZ einfuegen; echo "rc $?"` ⇒ `e_einfuegen.txt`. Das Werkzeug prüft alle Stücke, bevor es schreibt: Jeder Anker trifft genau eine Zeile, die erste Zeile keines Stücks steht schon da, kein Anker kommt in einem neuen Text vor, eine Tabellenzeile landet hinter einer Tabellenzeile, die Zeilenbilanz je Datei ist wie Soll. Soll rc 0: dieselben Zeilen wie in der Probe, sieben Zeilen `geschrieben und zurueckgelesen: …`, Schlusszeile `Gesamt: wie Soll, alle eingefuegt, je genau einmal`. rc ≠ 0 ⇒ **ABBRUCH**; dann immer Zeilen und md5 der sieben Dateien in `abbruch.txt`; nichts geschrieben ist nur belegt, wenn die Ausgabe mit `ABGEWIESEN, nichts geschrieben` oder `Gesamt: ABWEICHUNG, nichts geschrieben` endet.

**Vergleich.** `PY WZ vergleich; echo "rc $?"` ⇒ `e_vergleich.txt`. Soll rc 0: 30 Zeilen `… · Vorkommen 1 · GLEICH`, Schlusszeile `Gesamt: alle zeichengleich, je genau einmal`.

**Zweiter Lauf.** md5 der sieben Dateien, dann `PY WZ einfuegen; echo "rc $?"`, dann md5 noch einmal ⇒ `e_zweitlauf.txt`. Soll rc 2, Schlusszeile `ABGEWIESEN, nichts geschrieben: …` mit allen 30 Kennungen, md5 je Datei vorher und nachher gleich.

Commit `TB-145 E: Regelwerk-Nachtrag 08.–09.10.2026, 30 Stücke in sieben Dateien` mit den sieben Zieldateien und den Belegen bis hier, jede Datei mit Namen; pushen ⇒ **⟨E⟩**.

**Numstat.** `PY WZ numstat ⟨S0⟩ ⟨E⟩; echo "rc $?"` ⇒ `e_numstat.txt`. Soll rc 0: die Rohzeilen von `git diff --numstat`, sieben Zeilen `Soll <Datei> <n>	0 · Ist [<n>, 0] · gleich` mit n aus der Tabelle unter „Freigabe“, `JOURNAL.md` nicht in der Ausgabe, `weitere Dateien ausser Belegen und Ergebnis: keine`. rc 1 ⇒ melden; **keine Zeile von Hand richten.** Dazu `wc -l logs/sitzungswaechter/waechter.log` und die Zeilen seit 0b roh ⇒ `e_waechterlog.txt` (nur melden, ob das Schreiben im Auslöserordner den Wächter geweckt hat).

## Schritt W — tote Fenster schliessen

Rohausgaben ⇒ `w_fenster.txt` (jeder Befehl mit Ausgabe und `rc`). **Liste: `21346`, `21349`, `21560`, `21627`. Nie `21040`, nie ein Fenster ausserhalb der Liste** (*schützt:* Fenster des Betreibers und die eigene Sitzung). Jeder Aufruf direkt, ohne Skriptdatei: `osascript -e 'tell application "Terminal" to return <Ausdruck>'`, unten kurz `T <Ausdruck>`. Kein Enter, kein `keystroke`, kein System Events, kein Text in ein Fenster.

**Einmal vorweg:** `T id of every window` · `pgrep -a -x Terminal` · `ps -o lstart= -p <diese PID>` · `date`, alles roh. Soll: `pgrep` nennt genau die PID `52069`, und `ps -o lstart= -p 52069` gibt, ohne die Leerzeichen am Ende, `Di 15 Sep 09:14:08 2026` (zeichengleich mit `docs/belege/TB-144/d0_fenster.txt` Z. 97 und 99); sonst **nichts schliessen, melden.**

**Je Nummer `<n>` der Liste, in dieser Reihenfolge:**

1. `T exists window id <n>`
2. `T count of tabs of window id <n>`
3. `T processes of tab 1 of window id <n>`
4. `T busy of tab 1 of window id <n>`
5. `osascript -e 'tell application "Terminal" to get history of tab 1 of window id <n>' | grep -c 'exec claude'` — in den Beleg geht nur die **Zahl;** der Verlauf selbst geht in keine Datei (Zahl 0 gibt `rc 1`, das ist kein Fehler).

Geschlossen wird `<n>` nur, wenn alle fünf Bedingungen zutreffen:

| Bedingung | schützt vor |
|---|---|
| (1) ist `true`: das Fenster existiert | einem Schliessbefehl an ein Fenster, das es nicht mehr gibt |
| (2) ist `1`: genau ein Tab | dem Schliessen eines Fensters, in dem der Betreiber einen weiteren Tab geöffnet hat |
| (3) endet, mit `2>&1` aufgerufen, mit rc 0, und die ganze Ausgabe ist genau eine leere Zeile: `processes of tab 1` nennt keinen Prozess | dem Schliessen eines Fensters, in dem etwas läuft — der Prüfwert aus der Abnahme TB-144; das Fenster der eigenen Sitzung trägt dort `claude` und fällt so heraus |
| (5) ist ≥ 1: der Verlauf enthält `exec claude` | einem Fenster, das nie eine Sitzung des Wächters trug (21040 hatte 0) |
| Terminal ist noch derselbe Prozess wie in TB-144: PID `52069`, `lstart` `Di 15 Sep 09:14:08 2026` (Soll oben) | neu vergebenen Fensternummern nach einem Neustart von Terminal |

`busy` (4) wird gemessen und gemeldet, entscheidet aber nicht (Stück L1). Dann `osascript -e 'tell application "Terminal" to close window id <n>'`, nach 1 s `T exists window id <n>`. Steht es noch: **kein weiteres Fenster schliessen,** melden (*schützt:* vor einer Rückfrage von Terminal, die niemand beantwortet). Scheitert eine Abfrage oder trifft eine Bedingung nicht zu: Das Fenster bleibt, der Grund steht im Ergebnis; **kein Abbruch.** Lehnt Claude Code in diesem Schritt einen Aufruf ab oder verlangt es eine Bestätigung: Schritt W endet sofort (kein weiterer `osascript`-Aufruf, nichts umgehen), der Wortlaut geht ins Ergebnis, weiter mit Schritt J; **kein Abbruch der Sitzung** (Vorgabe des steuernden Chats: Einfügungen und Journal hängen nicht an den Fenstern).

**Einmal danach:** `T id of every window`. Soll: die Liste von vorher ohne die geschlossenen Nummern. `w_fenster.txt` geht mit der Abgabe ins Repo.

## Schritt J — Journalblock

Die Sitzung schreibt ihren Block nach `docs/belege/TB-145/j_block.md`, Gliederung wie Block EK (`JOURNAL.md` ab Z. 10241): Kopfzeile `## <Kennung> — TB-145: …`, Quellenzeile, Absatz „**Quelle:**“, `### Was gemessen ist` (Leerzeile davor), `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-145. Quellenvermerk: siehe Kopf.*`; kein `---`, nicht der Nachtrag J1 — was TB-145 selbst tat (auch Schritt W je Fenster), schreibt die Sitzung in eigenen Worten.

`PY WZ journal docs/belege/TB-145/j_block.md --probe; echo "rc $?"` ⇒ `j_journal_probe.txt`, dann ohne `--probe` ⇒ `j_journal.txt`. Das Werkzeug misst die letzte Kennung, setzt vor `### Was gemessen ist` die Zeile J1 und dahinter die 8 Zeilen aus B1 (sieben wörtlich aus `UEBERGABE.md`, md5-Wache je Zeile, und die Zeile zu den Fehlern Nr. 24 bis 31) und stellt den Block samt `---` vor `## Wiederkehrende Lehren`. Soll: acht Bedingungen `ja`, `Kennung EL (erwartet EL)`, `J1-Zeilen 9`, `Zeilen +<n>` mit n = Zeilen des Blocks + 9 + 1 + 3, rc 0. rc 2: die Bedingung mit `NEIN` lesen, den Block richten, neu — kein Abbruch; nennt das Werkzeug eine andere Kennung als EL: diese nehmen und melden. rc 3 (md5-Wache): **ABBRUCH.**

## Schritt F — Nachweis, Ergebnis, Abgabe

**Nachweis.** `PY WZ vergleich; echo "rc $?"` noch einmal ⇒ `f_vergleich.txt` (Soll wie in Schritt E). md5 und Zeilen von `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` ⇒ `f_waechter_md5.txt`; Soll wie in 0b: 622 Zeilen, `464ac93c53829935e479c5f14121c574`.

**Ergebnis** `docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md`: Kopf (Stand, Commits, ⟨S0⟩) · **„Kurz“** (Tabelle Schritt · Soll · Ist) · **„Schritt W“** (Tabelle je Fenster: existiert, Tabs, `processes`, `busy`, Verlauf-Zahl, geschlossen ja oder nein, Grund) · **„Abweichungen vom Auftrag“** (jede, auch kleine; sonst „keine“ mit der Liste der geprüften Sollwerte) · **„Nicht getan“** (die Posten unter „Nicht in TB-145“; Fenster, die blieben; Aufgaben für den Betreiber) · **„In einfacher Sprache“**. Rückfragen an den Betreiber stehen samt Antwort wörtlich darin.

**Abgabe.** Commit `TB-145 Abgabe: Ergebnis, Journal <Kennung>` mit `JOURNAL.md`, dem Ergebnis und den Belegen bis hier, jede Datei mit Namen; pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb145_f.txt"`, unverändert nach `f_porcelain.txt` kopieren (`cmp` gleich; Soll 0 B), erst danach die Kopfdatei und `PY WZ numstat ⟨S0⟩ ⟨F⟩ docs/belege/TB-145/j_block.md; echo "rc $?"` ⇒ `f_numstat.txt`. Soll rc 0: die sieben Dateien wie in Schritt E, `JOURNAL.md` mit n aus Schritt J und 0 entfernten Zeilen, sonst nur Belege und Ergebnis. Kleiner letzter Commit `TB-145 F: porcelain und numstat nach der Abgabe`, pushen; danach `git status --porcelain` noch einmal, Rohausgabe wörtlich in der Schlussmeldung.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab.
- Schritt A: Die Prozesszeile trägt nicht `--permission-mode manual`.
- Schritt E: `probe` oder `einfuegen` endet mit rc ≠ 0 — ein Anker hat nicht genau einen Treffer, oder die erste Zeile eines Stücks steht schon da. Das Werkzeug prüft alles, bevor es schreibt: Nach rc ≠ 0 ist keine Zieldatei geändert (die Ausnahme steht in Schritt E, „Einfügen“). Kein Stück von Hand einfügen, keinen Anker anpassen. Ebenso vor dem Commit ⟨E⟩: `vergleich` endet nicht mit rc 0, oder der zweite Lauf endet nicht mit rc 2 oder ändert einen md5.
- Die md5-Wache einer BACKLOG-Direktive weicht ab (rc 3, in Schritt E oder J): `UEBERGABE.md` ist dort nicht mehr, was der steuernde Chat freigab.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung** (ganze Sitzung, **ausser Schritt W** — dort endet nur Schritt W, siehe dort): melden, nicht umgehen. Verlangt schon Schritt 0 oder der Abbruchweg selbst (Belege committen, pushen) eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden. *Schützt:* vor einem halben Bau wie in TB-142.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch:** In Schritt W bleibt ein Fenster offen, eine Abfrage dort scheitert, oder Claude Code lehnt dort ab oder fragt nach (dann endet nur Schritt W); `journal` endet mit rc 2; die Kennung ist nicht EL; 0b weicht ab; der Wächter wurde geweckt; `numstat` endet mit rc 1; in F weicht `vergleich`, der md5 von `starte_sitzung.sh` oder `f_porcelain.txt` ab — je weiter, unter „Abweichungen“ nennen. **Bei Abbruch:** Belege committen (jede Datei mit Namen), Grund in `docs/belege/TB-145/abbruch.txt`, pushen, melden. Was bis dahin eingefügt ist, bleibt stehen, nichts zurückdrehen: geschriebene, noch nicht committete Zieldateien gehen mit Namen in den Abbruch-Commit; die Meldung nennt sie als Erstes. Ausnahme: Hat eine Zieldatei weniger Zeilen als am Stand ⟨S0⟩ (alle Stücke fügen nur ein), wird sie nicht committet — sie bleibt im Arbeitsbaum liegen und steht in der Meldung an erster Stelle.

## Nicht in TB-145

- Die 14 Formhinweise aus TB-141 (die UEBERGABE nennt nur Kennungen, keinen Wortlaut).
- „W8 und ARBEITSWEISE Z. 97“ (ohne Wortlaut).
- Jede Änderung an `starte_sitzung.sh`: Die Befunde zu `busy` und zum tty wären eine Wächter-Änderung mit Einzelfreigabe; L1 berichtigt nur die LIESMICH.
- Die Ablage.
- Die Projekt-Erinnerung.

## In einfacher Sprache

In den letzten zwei Tagen sind neue Regeln und Berichtigungen entstanden, die bisher nur in der Übergabe stehen. Dieser Auftrag trägt sie dort ein, wo man sie später sucht: im Regelwerk, in der Umzugsanleitung, in den Texten zum Sitzungswächter, im Backlog und im Journal. Es wird nur ergänzt, nichts gelöscht oder umgeschrieben; ein kleines Programm fügt die fertigen Texte ein und prüft vorher, ob jede Stelle eindeutig ist. Der Wächter selbst wird nicht angefasst. Nebenbei schliesst die Sitzung bis zu vier alte, leere Terminal-Fenster auf dem Mac — nur, wenn darin nachweislich nichts mehr läuft. Dein Fenster 21040 bleibt, wie es ist.

## Anhang A — Stücke (wörtlich)

Reihenfolge wie beim Einfügen. Das Werkzeug liest je Stück die Kopfzeile, die Felder `Zieldatei`, `Art`, `Form`, `Anker` und den Text zwischen den beiden Zeilen `~~~`. Die Zeile „Am HEAD“ ist Auskunft: Ankerzeile und Zeilenbilanz aus der Simulation, die Quelle aus der Stückliste des steuernden Chats („BESTAND145“ und `tb144/bau/…` meinen Berichte und Arbeitsdateien ausserhalb des Repos).

#### R01 — Abschnitt 0, „Am Ende jeder Antwort“: Zwischenmeldung je Stufe

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Zwischenmeldungen mit Ergebnis statt Rückfragen (Lesart⟧

Am HEAD: Anker Z. 74 · eingefügt +1 · Quelle: UEBERGABE Z. 2329 (Posten 21d)

~~~
| ☐ | Zusatz zur Zeile darüber: eine Zwischenmeldung an den Betreiber je abgeschlossener Stufe (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
~~~

#### R02 — Abschnitt 0, „Am Ende jeder Antwort“: kein Kopierfeld ohne Auftrag (Fehler Nr. 25)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦unmittelbar vor der Umzugsampel (deren Zeile bleibt die letzte)⟧

Am HEAD: Anker Z. 78 · eingefügt +1 · Quelle: UEBERGABE Z. 2367 (Posten 23)

~~~
| ☐ | Löst den letzten Halbsatz der Zeile darüber ab („ist kein Auftrag startklar, steht das dort“): Ist kein Auftrag startklar, steht das als gewöhnlicher Satz am Schluss der Antwort, nicht in einem Kopierfeld und ohne Empfängerzeile — ein Kopierfeld trägt nur Text, der abgeschickt werden soll. Das ändert die Form der Regel vom 02.10.2026, 10:45 für diesen einen Fall (Vorgabe des steuernden Chats vom 09.10.2026, vom Betreiber mit dem Eröffnungstext des Umzugs 11:06 abgeschickt; Fehler Nr. 25: der Betreiber schickte den Kopierfeld-Text an eine Claude-Code-Cloud-Sitzung) | UEBERGABE, Nachtrag 09.10.2026, 07:01; Umzug 09.10.2026, 11:06, Block 9; Nachtrag 09.10.2026, 12:56 (Übernahme 11:32) |
~~~

#### R03 — Abschnitt 0, „Arbeitsabschnitt endet“: kein Chat per geplanter Aufgabe (Fehler Nr. 27)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦der Eröffnungstext als ERSTE Nachricht im laufenden Chat, als eigener Kopierblock⟧

Am HEAD: Anker Z. 112 · eingefügt +1 · Quelle: UEBERGABE Z. 2450 (Posten 30a), Z. 2452 (Posten 31)

~~~
| ☐ | Beim Umzug wird kein Chat per geplanter Aufgabe angelegt; der Betreiber bekommt den Eröffnungstext als Kopierblock und öffnet den neuen Chat selbst. Die Lesart „neuer steuernder Chat beim Umzug“ in den Umzugsblöcken 08.10.2026, 19:58 und 22:03 sowie 09.10.2026, 06:52 und 07:23 (je Kopf und Block 9) ist überholt (09.10.2026, Fehler Nr. 27: Betreiber 08.10.2026, 08:36: „Lege mir zukünftig immer einen neuen Chat bereit“ meinte die initiale Claude-Code-Sitzung) | UEBERGABE, Nachtrag 09.10.2026, 07:26; Umzug 08.10.2026, 19:58, Kopf und Block 9 |
~~~

#### R04 — Abschnitt 0, „Arbeitsabschnitt endet“: Notizen, solange eine Sitzung den Arbeitsbaum hat

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦der Ordner ist von git ignoriert und zählt nicht als Träger nach 10 Nr. 2⟧

Am HEAD: Anker Z. 114 · eingefügt +1 · Quelle: UEBERGABE Z. 2235 (Posten 14d)

~~~
| ☐ | Zusatz zur Zeile darüber: Notizen unter `logs/steuernder_chat/`, solange eine Sitzung den Arbeitsbaum hat (08.10.2026, so getragen) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 |
~~~

#### R05 — Abschnitt 0, „Entscheidung beim Betreiber“: Betreiberregel vor Vorgabe (Fehler Nr. 26)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Eine offene Karte hält den Chat technisch an — vor der Karte wird alles Unabhängige angestossen⟧

Am HEAD: Anker Z. 128 · eingefügt +1 · Quelle: UEBERGABE Z. 2372 (Posten 25)

~~~
| ☐ | Eine Betreiberregel geht einer Vorgabe des steuernden Chats vor; hält der steuernde Chat den Weg für riskant, nennt er das Risiko und fragt per Karte, statt dem Betreiber die Arbeit zu geben (09.10.2026, Fehler Nr. 26: die Vorgabe „Start einmal von Hand“ stand über der Betreiberregel vom 08.10.2026, 21:26) | UEBERGABE, Nachtrag 09.10.2026, 07:12 |
~~~

#### R06 — Abschnitt 0, „Wenn ich den Betreiber anleite“: Aufgaben am Mac (Fehler Nr. 24)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Ein Befund aus einem angeleiteten Lauf geht als Datei nach⟧

Am HEAD: Anker Z. 141 · eingefügt +1 · Quelle: UEBERGABE Z. 2229 (Posten 8a)

~~~
| ☐ | Aufgaben am Mac in einfacher Sprache, ein Handgriff je Schritt, mit dem, was der Betreiber sieht (08.10.2026, Fehler Nr. 24: die Aufgabe verlangte, unter fünf Terminal-Fenstern das richtige über das Menü „Fenster“ zu finden) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 Nr. 24 |
~~~

#### R07 — Abschnitt 0, „Terminalbefehle“: `list_triggers` mit kleiner Grenze

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Ausgabe mit `head` begrenzen (06.10.2026: zwei Werkzeugausgaben ohne Grenze)⟧

Am HEAD: Anker Z. 154 · eingefügt +1 · Quelle: UEBERGABE Z. 2234 (Posten 13)

~~~
| ☐ | `list_triggers` nur mit kleiner Grenze aufrufen (08.10.2026, 22:02: eine Liste aller geplanten Aufgaben des Kontos, unnötig gross) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 |
~~~

#### G1 — Abschnitt 0, „Mac-Sitzung“: Start von Hand mit Modus-Schalter

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦`security unlock-keychain` (zweites Fenster) · `cd ~/trading-bot && claude --remote-control`⟧

Am HEAD: Anker Z. 161 · eingefügt +1 · Quelle: UEBERGABE Z. 2459 (Ursache), Z. 2550 (Posten 40); BESTAND145 3.1

~~~
| ☐ | ⭐ Gilt seit TB-143 (09.10.2026; für den Start von Hand Vorgabe des steuernden Chats, vorläufig): Ein Start von Hand trägt `--permission-mode manual` — `cd ~/trading-bot && claude --permission-mode manual --effort high --remote-control`; ohne andere Vorgabe starten Terminal-Sitzungen im Auto-Modus, und beim Eintritt in den Auto-Modus fallen breite Erlaubnisregeln weg, ausdrücklich `Bash(*)` | 22.1; UEBERGABE, Nachtrag 09.10.2026, 07:55 |
~~~

#### R08 — Abschnitt 0, „Mac-Sitzung“: Schliessen erst nach dem Helferbericht (Fehler Nr. 28)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Vor dem Schliess-Auslöser das Alter des letzten Commits messen⟧

Am HEAD: Anker Z. 173 · eingefügt +1 · Quelle: UEBERGABE Z. 2500 (Posten 33)

~~~
| ☐ | Schliessen erst nach dem Helferbericht (09.10.2026, Fehler Nr. 28: die wartende TB-142-Sitzung nach den eigenen Kernzahlen geschlossen, bevor der Abnahme-Helfer fertig war) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 Nr. 28 |
~~~

#### R09 — Abschnitt 0, „Mac-Sitzung“: Sitzung hängt unsichtbar an einer Frage (Fehler Nr. 24)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦legt der steuernde Chat die Claude-Code-Sitzung selbst über den Sitzungswächter an, bevor er dem Betreiber⟧

Am HEAD: Anker Z. 174 · eingefügt +1 · Quelle: UEBERGABE Z. 2229 (Posten 8b)

~~~
| ☐ | Hängt eine Sitzung unsichtbar an einer Frage: nicht das Fenster suchen lassen, sondern die Sitzung schliessen (Schliess-Auslöser) und neu beginnen (08.10.2026, Fehler Nr. 24) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 Nr. 24 |
~~~

#### R10 — Abschnitt 0, „Mac-Sitzung“: erst zustellen, dann Freigabe (Fehler Nr. 30); Probestart

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Nach einem Start-Auslöser stützt sich der steuernde Chat auf die Zeile des Wächter-Logs⟧

Am HEAD: Anker Z. 179 · eingefügt +2 · Quelle: UEBERGABE Z. 2502 (Posten 35a, 35b), Z. 2505 (Posten 38b)

~~~
| ☐ | Zuerst Satz und Aufgaben zustellen, dann die Freigabe für den Blick ins Terminal anfordern; der Zugriff verfällt nach 30 Minuten ohne Nutzung (09.10.2026, Fehler Nr. 30: die Freigabeanfrage hielt den Chat von etwa 08:20 bis 09:04 an) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 Nr. 30 |
| ☐ | Probestart über `starte_TB-<n>` ohne Satz, Blick ins Fenster, `schliesse_<HEAD>` — misst den Wächter ohne Handgriff des Betreibers (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 |
~~~

#### R11 — Abschnitt 0, „fremdes Ergebnis“: Kernzahlen in einem Befehl

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Die Abnahme macht ein eng zugeschnittener Helfer, nur lesend⟧

Am HEAD: Anker Z. 214 · eingefügt +1 · Quelle: UEBERGABE Z. 2235 (Posten 14b)

~~~
| ☐ | Zusatz zur Zeile darüber: Abnahme durch Helfer und Kernzahlen in einem einzigen eigenen Befehl (08.10.2026, so getragen) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 |
~~~

#### R12 — Abschnitt 0, „fremdes Ergebnis“: Erfolgsmeldung benennen (Fehler Nr. 24)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Bei Widerspruch misst der steuernde Chat die eine Tatsache selbst⟧

Am HEAD: Anker Z. 216 · eingefügt +1 · Quelle: UEBERGABE Z. 2229 (Posten 8c)

~~~
| ☐ | Eine Erfolgsmeldung, die der Betreiber einfügt, zuerst als solche benennen (08.10.2026, Fehler Nr. 24: der Betreiber schrieb um 21:37 „Nichts funktioniert mehr“, gemeint war die Erfolgsmeldung von TB-141) | UEBERGABE, Umzug 08.10.2026, 22:03, Block 7 Nr. 24 |
~~~

#### R13 — Abschnitt 0, „Auftrag schreiben“: Erinnerungsdateien; Byte-Abgleich

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Urteil und Freigabe bleiben beim steuernden Chat; ins Repo schreibt nur die Mac-Sitzung; ein frischer Gegenleser ist Pflicht (Betreiber⟧

Am HEAD: Anker Z. 255 · eingefügt +2 · Quelle: UEBERGABE Z. 2132 (Posten 1c), Z. 2167 (Wortlaut), Z. 2148 (Posten 4d)

~~~
| ☐ | Erinnerungsdateien schreibt nur der steuernde Chat selbst (08.10.2026: Helfer haben kein memory_str_replace) | UEBERGABE, Umzug 08.10.2026, 19:58, Block 4 Nr. 6 und Block 9 |
| ☐ | Byte-Abgleich beim Schreiben der Erinnerung (08.10.2026, so getragen) | UEBERGABE, Umzug 08.10.2026, 19:58, Block 7 |
~~~

#### R14 — Abschnitt 0, „Auftrag schreiben“: Schrittgrenze für Bestands- und Bau-Helfer (Fehler Nr. 29, 31)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Die Bestandsaufnahme vor dem Bau (zwei Helfer, getrennter Zuschnitt)⟧

Am HEAD: Anker Z. 256 · eingefügt +2 · Quelle: UEBERGABE Z. 2501 (Posten 34), Z. 2545 (Posten 39)

~~~
| ☐ | Bestandsaufnahmen auf die Stellen des gewählten Wegs zuschneiden, mit Schrittgrenze wie bei Gegenlesern (rund 25) (09.10.2026, Fehler Nr. 29: der Bestands-Helfer lief 13,5 Minuten und kostete rund 300 000 Helfer-Tokens) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 Nr. 29 |
| ☐ | Auch Bau-Helfer bekommen eine Schrittgrenze und ein Zwischenziel (09.10.2026, Fehler Nr. 31: der Helferauftrag BAU144 trug keine Schrittgrenze, obwohl Fehler Nr. 29 sie verlangt) | UEBERGABE, Nachtrag 09.10.2026, 12:56 |
~~~

#### R15 — Abschnitt 0, „Auftrag schreiben“: Grössenziel aus dem Vorbild

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦dem Berichtiger ein Grössenziel geben⟧

Am HEAD: Anker Z. 259 · eingefügt +1 · Quelle: UEBERGABE Z. 2327 (Posten 19)

~~~
| ☐ | Ein Grössenziel aus dem Vorbild gleicher Bauart ableiten (TB-141: 76,6 KB) (09.10.2026: 45 KB war gesetzt, nicht gemessen; v1 hatte 69 KB, v5 75,9 KB) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
~~~

#### R16 — Abschnitt 0, „Auftrag schreiben“: Berichtigen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Vorzählung als Skript vor und nach jeder Berichtigung⟧

Am HEAD: Anker Z. 263 · eingefügt +3 · Quelle: UEBERGABE Z. 2328 (Posten 20a, 20b), Z. 2504 (Posten 37a)

~~~
| ☐ | Der Berichtiger arbeitet in den Bausteinen und übernimmt Sollwerte aus der Simulation (`werte.json`), nie von Hand (09.10.2026) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
| ☐ | Kleine Berichtigungen (einzelne Zeilen, kein Sollwert) macht der steuernde Chat per Skript mit `assert` auf genau einen Treffer und lässt einen engen frischen Gegenleser nur diese Zeilen lesen (rund 12 Schritte) (09.10.2026: Nach v5 kam kein Gegenleser mehr — dem Betreiber vor der Karte gesagt) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
| ☐ | Kleine Aufträge einmal schreiben, Berichtigungen nur per Skript (09.10.2026: der Auftrag TB-143 zweimal ganz geschrieben, 12 und 15 KB) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 |
~~~

#### R17 — Abschnitt 0, „Auftrag schreiben“: Nachlese als Mac-Sitzung; Attrappen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Ein Bauskript prüft an der Quelle; zwei gleichzeitige Gegenleser⟧

Am HEAD: Anker Z. 265 · eingefügt +2 · Quelle: UEBERGABE Z. 2329 (Posten 21a, 21b)

~~~
| ☐ | Die Nachlese „als Mac-Sitzung durchgehen“ samt Abgleich mit den `deny`-Regeln (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
| ☐ | Prüfstände der Gegenleser mit Attrappen für `osascript` (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
~~~

#### R18 — Abschnitt 0, „Auftrag schreiben“: Simulation unter Python 3.9

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Die Simulation an Kopien samt Gegenprobe⟧

Am HEAD: Anker Z. 266 · eingefügt +1 · Quelle: UEBERGABE Z. 2148 (Posten 4c)

~~~
| ☐ | Zusatz zur Zeile darüber: Simulation unter Python 3.9 (08.10.2026, so getragen) | UEBERGABE, Umzug 08.10.2026, 19:58, Block 7 |
~~~

#### R19 — Abschnitt 0, „Auftrag schreiben“: Helfer und Geräteanbindung; Berechtigungsmodus und Vorprobe

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Vor einem Helferstart prüfen, ob der Zielordner schon existiert⟧

Am HEAD: Anker Z. 267 · eingefügt +4 · Quelle: UEBERGABE Z. 2326 (Posten 18a, 18b), Z. 2410 (Posten 28), Z. 2505 (Posten 38a)

~~~
| ☐ | Zusatz zur Zeile darüber: ein abgebrochener Helferauftrag läuft als frischer Helfer neu (Zielordner vorher ansehen) (09.10.2026) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
| ☐ | Helfer schreiben den Bericht nach jeder Prüfung fort und versuchen dreimal neu (09.10.2026: einem Helfer fiel die Anbindung nach 13 Aufrufen weg, „device not connected“) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
| ☐ | Vor einem Auftrag, der Programme ausserhalb des Repos steuert (`osascript`, `launchctl`, `kill`), den Berechtigungsmodus der Mac-Sitzung messen und den heikelsten Befehl in einer kurzen Vorprobe laufen lassen, bevor der grosse Auftrag gebaut wird (09.10.2026: der Auftrag TB-142 rechnete nicht mit dem Auto-Modus) | UEBERGABE, Umzug 09.10.2026, 07:23, Block 7 |
| ☐ | Vorprobe als eigener kleiner Auftrag vor dem grossen (09.10.2026, so getragen) | UEBERGABE, Umzug 09.10.2026, 11:06, Block 7 |
~~~

#### G2 — Abschnitt 6b, Tabelle der Startblöcke (Block 3, Z. 777): Start von Hand mit Modus-Schalter

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Block
Anker: ⟦| **6** | `/remote-control` |⟧

Am HEAD: Anker Z. 780 · eingefügt +2 · Quelle: UEBERGABE Z. 2459 (Ursache), Z. 2550 (Posten 40); BESTAND145 3.1

~~~
⭐ **Gilt seit TB-143 (09.10.2026), zu Block 3 der Tabelle darüber:** Ein Start von Hand trägt (Vorgabe des steuernden Chats, vorläufig) `--permission-mode manual` — `cd ~/trading-bot && claude --permission-mode manual --effort high --remote-control`; ohne andere Vorgabe starten Terminal-Sitzungen im Auto-Modus, und beim Eintritt in den Auto-Modus fallen breite Erlaubnisregeln weg, ausdrücklich `Bash(*)` (UEBERGABE, Nachtrag 09.10.2026, 07:55; Abschnitt 22.1).
~~~

#### G3 — Abschnitt 14, Regel 0 (Codeblock Z. 1448–1450): Start von Hand mit Modus-Schalter

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: vor
Form: Block
Anker: ⟦Bleibt es bei „Not logged in", erst dann `/login`⟧

Am HEAD: Anker Z. 1452 · eingefügt +2 · Quelle: UEBERGABE Z. 2459 (Ursache), Z. 2550 (Posten 40); BESTAND145 3.1

~~~
⭐ **Gilt seit TB-143 (09.10.2026), zu „2. Sitzung starten“:** Ein Start von Hand trägt (Vorgabe des steuernden Chats, vorläufig) `--permission-mode manual` — `cd ~/trading-bot && claude --permission-mode manual --effort high --remote-control`; ohne andere Vorgabe starten Terminal-Sitzungen im Auto-Modus, und beim Eintritt in den Auto-Modus fallen breite Erlaubnisregeln weg, ausdrücklich `Bash(*)` (UEBERGABE, Nachtrag 09.10.2026, 07:55; Abschnitt 22.1).
~~~

#### G4 — Abschnitt 14, Regel 1 (Codeblock Z. 1466–1468): Start von Hand mit Modus-Schalter

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: vor
Form: Block
Anker: ⟦Der Anweisungstext kommt **danach** als eigener Block in die wartende⟧

Am HEAD: Anker Z. 1470 · eingefügt +2 · Quelle: UEBERGABE Z. 2459 (Ursache), Z. 2550 (Posten 40); BESTAND145 3.1

~~~
⭐ **Gilt seit TB-143 (09.10.2026), zur Startzeile im Codeblock darüber:** Ein Start von Hand trägt (Vorgabe des steuernden Chats, vorläufig) `--permission-mode manual` — `cd ~/trading-bot && claude --permission-mode manual --effort high --remote-control`; ohne andere Vorgabe starten Terminal-Sitzungen im Auto-Modus, und beim Eintritt in den Auto-Modus fallen breite Erlaubnisregeln weg, ausdrücklich `Bash(*)` (UEBERGABE, Nachtrag 09.10.2026, 07:55; Abschnitt 22.1).
~~~

#### G5 — Abschnitt 22.4: neue Log-Zeile hinter „Satz ins Fenster gelegt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦Der Wächter legt den Satz nicht mehr ins Terminalfenster, und die Meldung⟧

Am HEAD: Anker Z. 2105 · eingefügt +1 · Quelle: ARBEITSWEISE Z. 2240 (ohne die drei Leerzeichen Einzug; „Die Zeile“ ersetzt durch „Die Meldung im Wächter-Log“, sonst zeichengleich); BESTAND145 3.1 (b)

~~~
⭐ **Gilt seit TB-144 (Wächter-Reparatur, Fehler Nr. 23):** Die Meldung im Wächter-Log heisst jetzt „⭐ EINGABEBEREIT (TB-<Nr>)“. Steht dort „⛔ STARTFRAGE“ oder „⛔ KEINE EINGABEZEILE“, ist die Sitzung nicht eingabebereit. Dazu sieht der steuernde Chat selbst ins Fenster (Abschnitt 0, Gruppe „Wenn eine Mac-Sitzung startet, endet oder abbricht“).
~~~

#### U1 — UMZUG.md, Abschnitt 4, Schritt 6: U25 (alter Eröffnungstext überholt)

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦**Vorlage in Abschnitt 6 dieses Dokuments.**⟧

Am HEAD: Anker Z. 229 · eingefügt +2 · Quelle: TB-141_bestand_REGELN.md Z. 76 (U25); Auftrag TB-141 Z. 475; ARBEITSWEISE Z. 113

~~~
⭐ **Nachtrag mit TB-145 (U25, Regel vom 07.10.2026):** Arbeitet ein Chat nach dem Eröffnungstext weiter, kennzeichnet er den alten Text in derselben Antwort als überholt und gibt beim Umzug einen neuen aus (06.10.2026: Der Eröffnungstext von 16:41 lag drei Stunden im Chat; UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 2; `ARBEITSWEISE.md` Abschnitt 0, Gruppe „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“).
~~~

#### L1 — Wächter-LIESMICH, hinter der Tabelle „Gemessen in TB-144“: Berichtigung zu `busy` und tty

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: nach
Form: Block
Anker: ⟦| **Probe** über Auslöser und launchd |⟧

Am HEAD: Anker Z. 60 · eingefügt +2 · Quelle: UEBERGABE Z. 2558, 2559 (a) (Posten 41, 43b); Belege b_m1.txt, b_m3.txt, d0_fenster.txt; ERGEBNIS TB-144 Z. 53–64

~~~
⭐ **Berichtigung aus der Abnahme TB-144 (09.10.2026):** `busy` war bei wartender Sitzung `false` (`docs/belege/TB-144/b_m1.txt` Z. 15–16, `b_m3.txt` Z. 15–16), am Fenster der arbeitenden Sitzung aber `true` (`d0_fenster.txt` Z. 112–113; in diesem Tab liefen `login, claude, caffeinate`, Z. 133–134). `busy` sagt also nicht verlässlich, ob in einem Fenster eine Sitzung läuft; vor dem Schliessen schützt die Prüfung `claude_im_repo` in `fenster_aufraeumen`. Für die drei toten Fenster nannte Terminal das tty des Fensters der laufenden Sitzung; für eine Aufräumregel über alte Fenster wäre `processes of tab` der zuverlässigere Prüfwert (`docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`, Abschnitt D0).
~~~

#### S1 — SITZUNGSWAECHTER_ausloeser_statt_tippen.md, oben: was seit TB-142/TB-144 anders ist

Zieldatei: `docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md`
Art: nach
Form: Block
Anker: ⟦Dieser Wächter macht aus einer Datei einen Sitzungsstart.⟧

Am HEAD: Anker Z. 6 · eingefügt +15 · Quelle: Wächter-LIESMICH Z. 10–49 (HEAD); ERGEBNIS TB-144 Z. 86; BESTAND145 3.3 (Z. 79–80, 89–90, 98, 205–206)

~~~
⭐⭐ **Gilt seit TB-142 und TB-144 (Wächter-Reparatur, 09.10.2026) — geht dem Text
unten vor:** Der Wächter legt den Auftragssatz nicht mehr ins Fenster (seit
TB-142); abgeschickt wird der Satz vom Betreiber. Nach `starte_TB-<Nr>` liest
der Wächter den Inhalt des neu geöffneten Fensters; die Erfolgszeile im Log
heisst „⭐ EINGABEBEREIT (TB-<Nr>)“. Der Wächter kennt drei Auslöserarten:
`starte_TB-<Nr>`, `schliesse_<HEAD>` und `probe_<PID>`. Alles Weitere steht in
`docs/werkzeuge/sitzungswaechter/LIESMICH.md`, Abschnitt „Gilt seit TB-144
(Wächter-Reparatur)“, und wird hier nicht wiederholt. Den Stand davor
beschreiben in diesem Dokument mindestens vier Stellen: im Abschnitt „Die
Betreiberentscheidung vom 23.09.2026: kein Return“ die Sätze „Der Wächter
schreibt den Auftragssatz in die Eingabezeile“ und „er schickt den Satz per
AppleScript an Terminal“ sowie die Tabellenzeile „Was entfällt“ („Text einfügen
— all das macht der Wächter“); im Abschnitt „Was der Wächter NICHT kann“ der
Satz „Der Wächter wartet **20 Sekunden**“.
~~~

#### A1 — Auslöserordner, .gitignore: `schliesse_*` und `probe_*`

Zieldatei: `docs/auftraege/_ausloeser/.gitignore`
Art: nach
Form: Zeilen
Anker: ⟦starte_TB-*⟧

Am HEAD: Anker Z. 2 · eingefügt +2 · Quelle: ERGEBNIS TB-144 Z. 86; BESTAND145 3.4

~~~
schliesse_*
probe_*
~~~

#### A2 — Auslöserordner, LIESMICH: die zwei weiteren Auslöserarten

Zieldatei: `docs/auftraege/_ausloeser/LIESMICH.md`
Art: nach
Form: Block
Anker: ⟦Name, und aus dem nur die Nummer.⟧

Am HEAD: Anker Z. 8 · eingefügt +9 · Quelle: Wächter-LIESMICH Z. 45 und Z. 49 (HEAD), Abschnitt „Gilt seit TB-144 (Wächter-Reparatur)“

~~~
Der Wächter kennt hier zwei weitere Auslöser
(`docs/werkzeuge/sitzungswaechter/LIESMICH.md`, Abschnitt „Gilt seit TB-144
(Wächter-Reparatur)“): Nach `schliesse_<HEAD>` (beide Wachen unverändert:
HEAD-Gleichheit, 600 s) schliesst der Wächter genau das gemerkte Fenster; die
Bedingungen dafür stehen dort. Eine Datei `probe_<PID>` öffnet ein Fenster
wie ein echter Start, prüft die Eingabezeile, beendet genau die dabei
entstandene Sitzung mit `TERM` und räumt das Fenster auf — kein Auftrag, kein
Satz; gelesen wird nur der Dateiname.
~~~

#### B1 — BACKLOG, Abschnitt 5: Abnahme TB-144 und Fehler Nr. 24 bis 31

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD: Anker Z. 364 · eingefügt +11 · Quelle: UEBERGABE (Arbeitsbaum), Nachtrag 09.10.2026, 13:30: Z. 2554, 2555, 2556, 2557, 2558, 2559, 2561 (wörtlich über Direktiven); letzte Zeile eigen

~~~
### Aus der Abnahme TB-144 (09.10.2026) und den Fehlern Nr. 24 bis 31 — eingetragen mit TB-145

⟦UEBERGABE: - **Abgabe TB-144:** |md5 afd89a3a24a4⟧
⟦UEBERGABE: - **Abnahme** (Helfer ABNAHME144, |md5 6ef97229c774⟧
⟦UEBERGABE: - **Gesetzte Werte:** |md5 78eca3252b90⟧
⟦UEBERGABE: - **Probe in der Sitzung:** |md5 4b2e048d7965⟧
⟦UEBERGABE: - **D0: kein altes Fenster geschlossen.** |md5 d2c49673e148⟧
⟦UEBERGABE: - **Befunde zur Entscheidung, |md5 940a4b93cf39⟧
⟦UEBERGABE: - **Echter Probestart ohne Auftrag** |md5 8b959c3438ed⟧
- **Fehler Nr. 24 bis 31:** Regeln in `ARBEITSWEISE.md` Abschnitt 0, eingetragen mit TB-145 (UEBERGABE: Umzug 08.10.2026, 22:03, Block 7 Nr. 24; Nachträge 09.10.2026, 07:01, 07:12 und 07:26 zu Nr. 25, 26 und 27; Umzug 09.10.2026, 11:06, Block 7 Nr. 28 bis 30; Nachtrag 09.10.2026, 12:56 zu Nr. 31).
~~~

#### J1 — JOURNAL: erste Zeile des Nachtrags im neuen Block der Sitzung

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

Kein Anker: `WZ journal` setzt die Zeile samt den aufgelösten Zeilen aus B1 vor `### Was gemessen ist` des Blocks. Quelle: Vorbild tb144/bau/j1.txt und JOURNAL Z. 10247 (Block EK)

~~~
**Nachtrag des steuernden Chats zum Stand vor TB-145, wie in `BACKLOG.md` Abschnitt 5 eingetragen (wörtlich aus `UEBERGABE.md`, Nachtrag 09.10.2026, 13:30; dazu die Zeile zu den Fehlern Nr. 24 bis 31):**
~~~

## Anhang B — Werkzeug und Sollwerte

### Werkzeug

sha256 des ausgelesenen Texts (mit abschliessendem Zeilenende): `2e04e5a4c6841c997e84c9e70e7b8db9adb9c1b7d7afd69be6ca7851459b7a49`.

```python
#!/usr/bin/env python3
# tb145_einfuegen.py - Werkzeug zum Auftrag TB-145, ausgelesen aus Anhang B.
# Abgeleitet vom Einfuegeskript aus TB-141 (Anhang A); Direktiven und Journal wie im
# Werkzeug von TB-144 (Anhang C). Liest Stuecke, Anker und Texte aus dem Auftrag,
# prueft alles, bevor es schreibt, weist einen zweiten Lauf ab und schreibt nur die
# acht Zieldateien (an Ort und Stelle, mit Ruecklesen; keine Hilfsdatei daneben).
# Die Ausgabe geht nach stdout; die Sitzung leitet sie in den Beleg um.
# Aufruf aus der Repo-Wurzel mit trading-env/bin/python3 -B:
#   probe                                nur lesen
#   einfuegen                            alle Stuecke ausser J1
#   vergleich                            jedes Stueck zeichengleich, genau einmal
#   numstat <von> <bis> [<Blockdatei>]   git diff --numstat gegen die Sollwerte
#   journal <Blockdatei> [--probe]       Block der Sitzung samt J1
# rc 0 wie Soll · rc 1 Abweichung, nichts geschrieben · rc 2 abgewiesen (zweiter Lauf
# oder Bedingung verletzt), nichts geschrieben · rc 3 Abbruch vor dem Schreiben.
import hashlib, json, re, subprocess, sys

P, A = "docs/projektfuehrung/", "docs/auftraege/"
AUF = A + "MAC_TB-145_regelwerk_nachtrag_0809.md"
UEB, JOU, BACK = P + "UEBERGABE.md", P + "JOURNAL.md", P + "BACKLOG.md"
ZIELE = (P + "ARBEITSWEISE.md", P + "UMZUG.md", P + "SITZUNGSWAECHTER_ausloeser_statt_tippen.md", BACK, JOU,
         "docs/werkzeuge/sitzungswaechter/LIESMICH.md", A + "_ausloeser/.gitignore", A + "_ausloeser/LIESMICH.md")
FREI = ("docs/belege/TB-145/", "docs/ERGEBNIS_TB-145_regelwerk_nachtrag_0809.md")
NACHTRAG = "## Nachtrag 09.10.2026, 13:30"
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
    # eine Zeile '⟦UEBERGABE: <Anfang> |md5 <12 Zeichen>⟧' kommt unveraendert aus dem Nachtrag 13:30 der UEBERGABE
    aus = []
    for x in s["text"]:
        if x.startswith(KL + "UEBERGABE: "):
            anfang, md = x[len(KL) + 11:-1].split(" |md5 ")
            zl = zeilen(UEB)
            a = [k for k, y in enumerate(zl) if y.startswith(NACHTRAG)]
            assert len(a) == 1, "Nachtrag 13:30 trifft %d-mal" % len(a)
            e = next((k for k in range(a[0] + 1, len(zl)) if zl[k].startswith("## ")), len(zl))
            t = [y for y in zl[a[0]:e] if y.startswith(anfang)]
            assert len(t) == 1 and hashlib.md5(t[0].encode("utf-8")).hexdigest()[:12] == md, "UEBERGABE-Zeile '%s': %d Treffer oder md5 anders" % (anfang, len(t))
            aus.append(t[0])
        else:
            assert KL not in x, s["id"] + ": Klammer im Text"
            aus.append(x)
    return aus


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
    print("# TB-145 %s — Stuecke aus Anhang A%s" % ("probe" if probe else "einfuegen", " (nur gelesen)" if probe else ""))
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
    print("# TB-145 vergleich — jedes Stueck zeichengleich und genau einmal in seiner Zieldatei")
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
    print("# TB-145 numstat — git diff --numstat %s %s gegen die Sollwerte" % (von, bis))
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
    print("# TB-145 journal%s — Block der Sitzung samt J1 vor '## Wiederkehrende Lehren'" % (" (Probe)" if probe else ""))
    st, so = stuecke(), soll()
    zl, b, b1 = zeilen(JOU), zeilen(blockpfad), fertig(st["B1"])
    j1 = fertig(st["J1"]) + [x for x in b1 if x.startswith("- ")]
    k = [n for n, x in enumerate(zl) if x == "## Wiederkehrende Lehren"]
    assert len(k) == 1, "Schlussueberschrift trifft %d-mal" % len(k)
    k, was = k[0], "### Was gemessen ist"
    alt = [m.group(1) for m in (re.match(r"## ([A-Z]{2}) — ", x) for x in zl[:k]) if m][-1]
    neu = alt[0] + chr(ord(alt[1]) + 1) if alt[1] != "Z" else chr(ord(alt[0]) + 1) + "A"
    g = b.index(was) if was in b else 0
    bed = (("letzte Kennung %s, Kopfzeile beginnt mit '## %s — TB-145'" % (alt, neu), b[0].startswith("## %s — TB-145" % neu)),
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
  "G1",
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
  "G2",
  "G3",
  "G4",
  "G5",
  "U1",
  "L1",
  "S1",
  "A1",
  "A2",
  "B1",
  "J1"
 ],
 "numstat": {
  "docs/auftraege/_ausloeser/.gitignore": [
   2,
   0
  ],
  "docs/auftraege/_ausloeser/LIESMICH.md": [
   9,
   0
  ],
  "docs/projektfuehrung/ARBEITSWEISE.md": [
   36,
   0
  ],
  "docs/projektfuehrung/BACKLOG.md": [
   11,
   0
  ],
  "docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md": [
   15,
   0
  ],
  "docs/projektfuehrung/UMZUG.md": [
   2,
   0
  ],
  "docs/werkzeuge/sitzungswaechter/LIESMICH.md": [
   2,
   0
  ]
 },
 "j1_zeilen": 9,
 "kennung": "EL"
}
```
