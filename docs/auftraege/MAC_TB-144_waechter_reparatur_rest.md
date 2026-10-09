# TB-144 Wächter-Reparatur, Rest von TB-142 — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 09.10.2026** (Helfer BAU144, per Skript aus den Bausteinen von TB-142), gebaut ausserhalb des Repos (Entscheid W1), nur lesend am Repo; Wächterstücke und Einfügungen an Kopien simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht.

**Sitzungstitel:** `TB-144` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `6415b899e084a4d202c676609bb4d122e8602030` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-144`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-144/tb144_werkzeug.py` (Anhang C) kurz `WZ`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15).
**Ziel** (Vorgaben V1–V9, `logs/steuernder_chat/TB-142_VORGABEN.md`, md5 `022ef7fba702ea528566c06a4c704e58`): Nach `docs/auftraege/_ausloeser/starte_TB-<n>` steht die Claude-Code-Sitzung in einem **neuen** Terminal-Fenster eingabebereit (keine Startfrage), und das Wächter-Log sagt wahr, ob das so ist.
**Bauart wie TB-141** (`docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md`): Schritt 0, Belege, Journal und Abgabe wie dort, mit den Werten von hier; bei Widerspruch gilt dieser Auftrag. **Anders:** Die Sitzung ändert ein Werkzeug, misst an Terminal und Claude Code (M0–M5) und probt den Wächter über launchd.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**Freigabeklasse: Handwerk mit Einzelfreigabe** — der Wächter wird geändert (`docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md` Z. 369–373: „Bis zu einem Umbau (Handwerk mit Freigabe, weil der Wächter geändert wird)“). Keine `deny`-/`ask`-Regel trifft `docs/werkzeuge/sitzungswaechter/`; Register 36.3/37.3 nennen den Ordner nicht (Bestand `logs/steuernder_chat/TB-142_BESTAND_WAECHTER_bericht.md`, Abschnitt 3).

**Freigabe des Betreibers — Karte vom 09.10.2026, gestellt nach 12:42, beantwortet vor 12:53.** Frage, wörtlich: „Einzelfreigabe TB-144 (Rest von TB-142): Darf die Mac-Sitzung den Sitzungswächter mit den Stücken W2–W6 umbauen wie für TB-142 freigegeben, jetzt mit --permission-mode manual in der Startzeile, und dazu neu: vorab ihren Modus messen (Schritt A), die vier alten Terminal-Fenster ohne Sitzung schliessen (Schritt D0), 7 (mit --no-chrome 8) Zeilen in ARBEITSWEISE, 13 Zeilen im BACKLOG und den Journalblock EK eintragen?“ Antwort, wörtlich die gewählte Möglichkeit: „Freigeben wie gebaut (Empfohlen)“ — mit ihrer Beschreibung auf der Karte: „Mit Modus-Messung, Schliessen der vier Fenster 21040, 21346, 21349, 21560 (nur wenn nichts darin läuft) und der Zeile zur Startzeile seit TB-143. Preis: Die vier Fenster samt ihrem Verlauf sind danach zu; mindestens vier Probesitzungen erscheinen kurz in der Claude-App.“ Weiter in Kraft: die Karte zu TB-142 (`docs/auftraege/MAC_TB-142_waechter_reparatur.md` Z. 14) und die Karte zum Modus „Manual“ (`docs/auftraege/MAC_TB-143_waechter_modus_schalter.md` Z. 14). Nach der Antwort eingearbeitet, ohne den Umfang zu ändern: vier Berichtigungen der Nachlese (Z. 143, 157, 191).

**Die Sitzung darf ändern, und nichts sonst:**

| Datei | was |
|---|---|
| `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` | Stücke W2–W6 (Anhang A); Konstanten nach Messung |
| `docs/werkzeuge/sitzungswaechter/LIESMICH.md` | E7–E10, nur einfügen |
| `docs/projektfuehrung/ARBEITSWEISE.md` | E1–E5, E12, E6 nur bei geänderter Startzeile, nur einfügen |
| `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/JOURNAL.md` | E11; Block der Sitzung samt J1; nur einfügen |
| neu: `docs/belege/TB-144/…`, `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md` | Belege, Werkzeug, Ergebnis |
| nicht in git: `docs/auftraege/_ausloeser/probe_<PID>`, `logs/sitzungswaechter/…` | Probe-Auslöser anlegen (bleibt er liegen: nach `_erledigt/` verschieben); der Wächter schreibt Log, `letztes_fenster_probe.txt` und `letztes_fenster_geschlossen.txt` (`letztes_fenster.txt` erst beim echten Start) |

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt; das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** `docs/belege/TB-142/`; `einschalten.sh` und die plist (V9; verlangt die Probe dort eine Änderung ⇒ melden, nicht ändern); `UEBERGABE.md`, `UMZUG.md`, Register, `research/`, `shared/`, `strategies/`; bestehende Zeilen der vier Dokumente ändern oder entfernen.

## Belegt · erschlossen · offen

- **Belegt** (Bestand, Abschnitte 1–2; am HEAD nachgemessen): `starte_sitzung.sh` Z. 325–329 meldet `id of window 1`, das von `do script` gelieferte `neu` bleibt ungenutzt; Z. 327 trägt `--permission-mode manual` (TB-143); Z. 337–339 feste Wartezeit 20 s; Z. 347–355 (TB-142, V4): kein Satz mehr ins Fenster, geprüft wird nichts. `waechter.log`: 20 Starts in Folge mit Fenster 15501 seit 29.09.2026, 15:39:35Z. `launchd_aus.log`: 51 Zeilen der Form `tab 1 of window id <n>`. 08.10.2026: Die Sitzung stand an „Claude in Chrome extension detected … Enter to confirm · Esc to keep browser tools off“, später an „Teach auto mode about your environment? … Enter to confirm · Esc to cancel“. launchd ruft `/bin/bash …/starte_sitzung.sh` aus dem Arbeitsbaum auf, ohne Umgebungsvariablen (plist Z. 15–19) — **eine gespeicherte Änderung ist sofort scharf.** `docs/auftraege/_ausloeser/.gitignore` deckt nur `starte_TB-*` und `_erledigt/`. TB-142 brach in Schritt B ab: Claude Code verwehrte im Auto-Modus zwei `osascript`-Aufrufe an Terminal über Skriptdateien (`docs/belege/TB-142/abbruch.txt` Z. 5–9; UEBERGABE Z. 2457, 2459, 2484).
- **Erschlossen:** `do script` ohne `in` liefert einen Tab derselben Textform. Die Automation-Berechtigung hängt am Aufrufer (LIESMICH Z. 239, 246–247 belegen nur den einmaligen Dialog beim ersten Lauf über launchd). Eine Sitzung ohne Auftrag schreibt nichts in den Arbeitsbaum. Die AppleScript-Wörter `contents`, `tty`, `busy`, `close`, `exists` in Anhang A kommen aus dem Gedächtnis des Helfers — M0 prüft sie.
- **Offen — misst die Sitzung, nie raten:** Modus der Sitzung (Schritt A) · Kennung des Fensters zu einem Tab (M1) · Text der Eingabezeile im Fensterinhalt (M2) · Wirkung von `--no-chrome` (M3) · ob Terminal ein Fenster mit beendetem Prozess ohne Rückfrage schliesst (M4) · ob „Teach auto mode“ auch beim Start erscheinen kann (M5) · ob Lesen und Schliessen unter launchd eine weitere Berechtigung verlangen (Schritt D). Vom Werkzeug abhängig, im Ergebnis beschreiben. Im Entwurf stehen dafür benannte Konstanten und Funktionen, kein geratener Wert.
- **Simulation des Helfers** (Kopien `git show HEAD:<pfad>`; Linux, bash 5.1 statt 3.2, Python 3.10 mit `ast.parse(feature_version=(3,9))`): jeder Anker genau 1; `bash -n` rc 0 nach W2–W6; `do script` 1 → 1, `--permission-mode manual` einmal; `keystroke`, `System Events` und bash-4-Mittel 0; zweiter Lauf je abgewiesen; Zeilenbilanzen wie unten; die Funktionen aus W2 mit Attrappen für `osascript` durchgespielt. **Nicht simuliert:** alles, was `osascript`, Terminal, launchd oder Claude Code wirklich tut, und bash 3.2. Die Sitzung zählt selbst nach; ihre Zahl gilt.

## Schranken — je mit dem, wovor sie schützen

1. **Kein Enter, kein `keystroke`, kein System Events, kein Abschicken** — weder im Wächter noch in dieser Sitzung, auch nicht, um ein Probefenster oder eine Rückfrage loszuwerden. *Schützt:* Betreiberentscheidung 23.09.2026 und Schranke der Geräteanbindung (ARBEITSWEISE 19; LIESMICH Z. 85–87, 208–211).
2. **Kein Text in ein bestehendes Fenster;** den Fensterinhalt nur lesen, über Terminal selbst. *Schützt:* vor dem Abschicken samt Zeilenende (V4) und vor jeder Wirkung auf die Sitzung.
3. **Das Skript gibt nie Umgebungsvariablen, Schlüssel oder Dateiinhalte aus** (Kopf von `starte_sitzung.sh`); ins Log gehen höchstens die letzten 8 Zeilen (je 160 Zeichen) des **neu geöffneten** Fensters, nur bei ⛔. Für Belege gilt dasselbe: Fensterinhalte zuerst nach `$TMPDIR`; vor dem Kopieren nach `docs/belege/TB-144/` jede Zeile mit Konto- oder Mailangaben durch `<<entfernt: Kontozeile>>` ersetzen und das in der Kopfdatei sagen. *Schützt:* Zugangs- und Kontodaten (Belege werden gepusht).
4. **Die sechs Wachen (Z. 157–284 am HEAD) und der Schliess-Auslöser mit HEAD-Gleichheit und 600 s (Z. 64–135) bleiben unverändert;** W3 fügt dort nur einen Aufruf ein. *Schützt:* „nie zwei Aufträge im selben Arbeitsbaum“, Abo statt API-Abrechnung, keine arbeitende Sitzung wird geschlossen.
5. **`/bin/bash` des Macs ist 3.2:** keine assoziativen Felder, kein `mapfile`, kein `${x,,}`. *Schützt:* vor einem Wächter, der unter launchd nicht startet.
6. **Vor jedem Speichern von `starte_sitzung.sh`: `bash -n`; gespeichert wird in einem Schritt** (fertige Kopie daneben, dann `mv`) — `WZ` tut beides. AppleScript-Stücke vorher auf dem Mac auf Syntax prüfen (C1). *Schützt:* launchd führt die Datei aus dem Arbeitsbaum aus; ein halber Stand wäre scharf.
7. **Probefenster** nur über die Startzeile, ohne Auftrag; beendet wird nur per `TERM` an eine PID, die nicht die eigene Sitzung ist (M0) und am Terminal des Probefensters hängt; kein `-KILL`. *Schützt:* die eigene Sitzung und fremde Fenster.
8. **Nie `git add -A`, nie `git add .` oder ein Ordner oberhalb von `docs/belege/TB-144/`;** jeder Commit nennt seine Dateien mit Namen — `probe_<PID>` ist von `.gitignore` nicht gedeckt. *Schützt:* vor einem Auslöser im Commit.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-144/` entsteht:** `git status --porcelain > "$TMPDIR/tb144_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `6415b899e084a4d202c676609bb4d122e8602030` und genau diese drei Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md
```

Dann das Werkzeug auslesen:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
i = z.index("### Werkzeug")
a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
t = "\n".join(z[a + 1:b]) + "\n"
open(sys.argv[2] + "/tb144_werkzeug.py", "w", encoding="utf-8").write(t)
print("tb144_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb144_werkzeug.py 11367fd86ad4d2568b9ad8e3baf2aeb13d1faedd8ae8240c7c09bdd814c2640b`; sonst ABBRUCH. Commit `TB-144 Schritt 0: Stand des steuernden Chats 09.10.2026` mit genau den drei Pfaden (mit Namen hinzufügen), pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb144_0a.txt` unverändert nach `docs/belege/TB-144/0a_status.txt` (`cmp` gleich) und das Werkzeug nach `docs/belege/TB-144/tb144_werkzeug.py` (sha256 noch einmal). **Für jede Rohausgabe gilt:** Sie bleibt roh; die Beschreibung (was, Befehl, Bytes, Zeilen, md5) steht in `<name>.kopf.txt`. Ausgaben von `WZ` tragen ihre Kopfzeile selbst.

**0b. Ausgang** ⇒ `0b_ausgang.txt`: md5 und Zeilen der fünf Zieldateien an ⟨S0⟩. Soll: `starte_sitzung.sh` 357 Z., `7d78764c75659b2fb9616dd4edf8a63d`, ein `do script`, einmal `--permission-mode` · `LIESMICH.md` 304, `502b3aee263da5a489b382d1b4c2ff81` · `ARBEITSWEISE.md` 2 471, `c5e0689a944394f9dfe3f3427ace4498` · `BACKLOG.md` 362, `cda13f78d4477e620da9901df6ba81a1` · `JOURNAL.md` 10 578, `1719db0d9c5ebef07cc0cb33984ce1c3`, letzte Kennung EJ. Weicht eine ab: vermerken; die Anker entscheiden.

## Schritt A — Modus messen, bevor gebaut wird

**Vor M0 und vor jedem anderen `osascript`-Aufruf** ⇒ `a_modus.txt` (roh), die Aussage ⇒ `a_modus.kopf.txt`:

**A1.** Prozesszeile der eigenen Sitzung: `EIGEN` mit der `while`-Zeile aus M0, dann `ps -o command= -p <EIGEN>`. Soll: Sie trägt `--permission-mode manual`; sonst **ABBRUCH** (**Lesart des Helfers, vorläufig**).
**A2.** Eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet.
**A3.** Genau ein lesender Aufruf über eine Skriptdatei, wie ihn Claude Code in TB-142 ablehnte (`docs/belege/TB-142/abbruch.txt` Z. 8–9): `/bin/bash "$TMPDIR/T" 'id of every window'` (`T` wie in Schritt B) — einmal, Zeitgrenze 30 s, keine Variante. Ausgänge wie in TB-143, Schritt B: **LÄUFT** ⇒ weiter · **ABGELEHNT** (Wortlaut in den Beleg) · **NACH BESTÄTIGUNG** (Claude Code fragt den Betreiber; seine Antwort wörtlich ins Ergebnis) · **FEHLER** (Fehlertext oder „Zeitgrenze“; **Lesart, vorläufig**) — die drei letzten: **ABBRUCH,** nichts ist gebaut.

## Schritt B — Messungen M0–M5 (vor dem Bau)

Rohausgaben nach `docs/belege/TB-144/` (Schranke 3). Die Befehle sind Vorschläge des Helfers; trägt einer auf dem Mac nicht, einen gleichwertigen nehmen und unter „Abweichungen“ nennen. Abkürzung: `T '<Ausdruck>'` steht für `/bin/bash "$TMPDIR/T" '<Ausdruck>'` (eine Shell-Funktion hielte nicht über getrennte Shell-Aufrufe der Sitzung); die Datei einmal anlegen: `printf '%s\n' 'osascript -e "tell application \"Terminal\" to return $1"' > "$TMPDIR/T"`.

**M0 Umgebung** (neu; berichtigt nach `docs/belege/TB-142/abbruch.txt` Z. 21–26) ⇒ `b_m0.txt`: `sw_vers -productVersion`; `/bin/bash --version | head -1`; `claude --version`; `echo "$TERM_PROGRAM"` (Soll `Apple_Terminal` — Aufrufer aller Messungen in Schritt B ist diese Sitzung: Terminal → claude → `osascript`; sonst melden, nicht messen); `claude --help | grep -n -- '--no-chrome'`; `grep -n -E 'name="(contents|history|busy|tty|processes|close|exists|do script)"' /System/Applications/Utilities/Terminal.app/Contents/Resources/Terminal.sdef`. Dazu die eigene Sitzung:

```
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done
echo "EIGEN=$p"; pgrep -a -x claude | grep -x "$p"; lsof -a -p "$p" -d cwd -Fn | grep '^n'
```

Soll: `pgrep -a` nennt die PID, ihr cwd ist `~/trading-bot`. Sonst melden — der Probe-Auslöser braucht genau diese PID.

**M1 Fenster zu einem Tab, M2 Eingabezeile** — Testfenster 1 mit der Startzeile vom HEAD ⇒ `b_m1.txt`, `b_m2_<s>.txt`:

```
T 'id of every window'
osascript -e 'tell application "Terminal"' -e 'set neu to do script "cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control"' -e 'return neu' -e 'end tell'
T 'id of every window'
T 'contents of tab <k> of window id <n>'      # nach 3, 6, 10, 15, 20, 30, 40, 50 und 60 s (wie STUFEN)
T 'tty of tab <k> of window id <n>'; T 'busy of tab <k> of window id <n>'
```

M1 ist beantwortet, wenn die Rückgabe `<k>` und `<n>` nennt, `<n>` vorher nicht in der Fensterliste stand und nachher drinsteht (die Form „tab <k> of window id <n>“ ist nur erschlossen). M2: aus den Lesungen **ein Merkmal aus ASCII-Zeichen** (ohne `|`, `"`, `$`, `\`, Backtick) wählen, das in jeder Lesung der wartenden Sitzung steht, in keiner davor (Shell, Ladeanzeige) und in keiner mit einer Frage ⇒ `MERKMAL_EINGABEZEILE`. Zeigt Testfenster 1 nur eine Frage, kommt das Merkmal aus den Lesungen von Testfenster 2 (M3). Zeigt auch Testfenster 2 keine wartende Sitzung: kein Merkmal raten, `waechter bau` nicht ausführen; der Wächter bleibt am Stand ⟨S0⟩, Schritte C, D0, D und E entfallen (`doku` braucht die Konstanten), und die Sitzung gibt eine **Teilabgabe** ab (Schritt F, „Teilabgabe“). Festhalten: ab welcher Lesung es steht, ob `Enter to confirm` vorkommt, wie die Zeilen getrennt sind, ob das Fenster „manual mode on“ zeigt (Beobachtung, kein Soll; UEBERGABE Z. 2476).

**M4 Schliessen** — am selben Fenster ⇒ `b_m4.txt`: `ps -t <tty ohne /dev/> -o pid=,comm=` ⇒ die PID von `claude` (ist es `EIGEN`: nichts beenden, melden); `ps -o tty= -p <pid>` (Soll: `/dev/` + Ausgabe = `tty of tab`; sonst Abweichung für die Zeilen mit `TTY_PID` in W4); `ps -o command= -p <pid>` (erwartet `--permission-mode manual`; fehlt der Schalter: melden, kein Abbruch); `kill -TERM <pid>`; nach 5 s `T 'busy of tab …'`. Nur bei `false`: `osascript -e 'tell application "Terminal" to close window id <n>'`, nach 1 s (wie `delay 1` in `fenster_zu`) `T 'exists window id <n>'`. Bei `busy` = `true`: nicht schliessen, melden, `FENSTER_SCHLIESSEN=nein`. `exists` = `false` ⇒ `FENSTER_SCHLIESSEN=ja`. `exists` = `true` ⇒ Terminal fragt nach oder schliesst nicht ⇒ `nein`; das Fenster bleibt offen und steht als Aufgabe für den Betreiber im Ergebnis (Schranke 1).

**M3 `--no-chrome`** — nur wenn M0 den Schalter in `--help` findet: Testfenster 2 wie oben, mit ` --no-chrome` am Ende der Startzeile ⇒ `b_m3_<s>.txt`; danach wie in M4 beenden — schliessen nur, wenn M4 `ja` ergab, sonst offen lassen und melden. Entscheid nach V2:

| Testfenster 1 (ohne) | Testfenster 2 (mit) | Startzeile |
|---|---|---|
| Chrome-Frage | keine Frage | `--no-chrome` anhängen |
| keine Frage | keine Frage | `--no-chrome` anhängen; im Ergebnis sagen, dass die Wirkung nicht zuzuordnen ist (**Lesart des Helfers, vorläufig:** V2 verlangt nur (a) und (b)) |
| gleich was | Chrome-Frage | unverändert; im Ergebnis: einmal `/chrome` durch den Betreiber |
| gleich was | eine andere Frage, nicht die Chrome-Frage | unverändert — (b) aus V2 ist so nicht gezeigt, die Chrome-Frage könnte dahinter noch kommen; die Frage wörtlich melden, im Ergebnis als Aufgabe für den Betreiber |
| `--help` nennt den Schalter nicht | — | unverändert, ebenso |

**M5 „Teach auto mode“:** in allen Lesungen aus M2 und M3 und in den Log-Zeilen aus Schritt D (`d_probe<i>_log.txt`; Fensterzeilen stehen dort nur bei ⛔) zählen, wie oft `Teach auto mode` vorkommt ⇒ `b_m5.txt` (je Datei eine Zeile: Name, Zahl). **Teilmessung:** Sie sagt nichts über die Zeit nach dem ersten Auftrag.

Ergebnis in `docs/belege/TB-144/messwerte.txt`: sechs Zeilen `M1: …` bis `M5: …` und (nach Schritt D) `PROBE: …`, je ein Satz, höchstens 400 Zeichen, ohne `|`. `WZ` setzt sie in LIESMICH ein.

## Schritt C — V1, V2, V3, V5 bauen

**C1. AppleScript-Syntax** ⇒ `c1_applescript.txt`: die fünf AppleScript-Stücke aus W2 (`fensterliste`, `fenster_starten`, `fenster_lesen`, `fenster_tty`, `fenster_zu`) mit Beispielwerten für die Shell-Variablen je in eine Datei im Scratch, übersetzen, nicht ausführen (z. B. `osacompile -o "$TMPDIR/x.scpt" <Datei>`; vom Werkzeug abhängig, den Aufruf nennen). Soll: je rc 0.

**C2. Bau** — die gemessenen Werte als `NAME=WERT` (ohne `"`, `$`, Backtick, `\`, `|`, `<<`; höchstens 400 Zeichen — sonst weist `doku` sie ab):

```
PY WZ waechter bau 'MERKMAL_EINGABEZEILE=<aus M2>' 'FENSTER_SCHLIESSEN=<ja|nein aus M4>' --probe; echo "rc $?"
```

⇒ `c2_bau_probe.txt`, dann ohne `--probe` ⇒ `c2_bau.txt`. Nach M3 dazu `'STARTZEILE=cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control --no-chrome'`; heisst die Leseeigenschaft nach M0 anders, `'LESE_EIGENSCHAFT=…'`. Soll je rc 0: `W2 · Anker Z. 43 · nach der Zeile · Zeilen +210`, `W3 · Anker Z. 133 · vor der Zeile · Zeilen +2`, `W4 · Anker Z. 141 · vor der Zeile · Zeilen +64`, `W5 · Anker Z. 324 · 16 Zeilen ersetzt durch 2`, `W6 · Anker Z. 342 · 16 Zeilen ersetzt durch 19`, je Wert `gesetzt · …`, `starte_sitzung.sh · 622 Zeilen · bash -n rc 0 · 'do script' in Befehlszeilen 1 · verbotene Woerter 0 · bash-4 0`. Ein zweiter Lauf: `ABGEWIESEN`, rc 2.

**Weicht eine Messung vom Entwurf ab** (Form des Tabs, Name einer Eigenschaft, Form des tty, weitere Merkmale einer Frage): die Stelle an einer Kopie im Scratch ändern, `bash -n`, die Kopie neben die Datei legen und mit `mv` ersetzen (Schranke 6), dann von Hand zählen: `/bin/bash -n` rc 0 · `do script` in Befehlszeilen 1 · `--permission-mode manual` in Befehlszeilen 1 · ` in window`, `keystroke`, `System Events` je 0 · kein Wert `="<<` (`PY WZ nachweis` trägt erst in F1: es verlangt `PROBE:` und die Einfügungen E); jede geänderte Zeile unter „Abweichungen vom Auftrag“. **Die Wortlaute der Log-Zeilen bleiben** (festgelegt in W2, W4, W6; für den Leser gesammelt im Codeblock von E7). Rückgabewert des Wächters: 0, 3 (Startfrage), 4 (keine Eingabezeile), 1 (Abbruch davor); nur die Probe: 5 (eingabebereit, aber eine Probe-Sitzung „NICHT beendet“). „Eingabebereit“ verlangt das Merkmal in zwei Lesungen hintereinander — **Lesart des Helfers, vorläufig** (eine Frage könnte kurz nach der Eingabezeile erscheinen; nicht gemessen).

Commit `TB-144 C: Waechter V1 V2 V3 V5 und Probe-Ausloeser`, pushen ⇒ **⟨C⟩**. numstat ⟨S0⟩..⟨C⟩ für `starte_sitzung.sh`: `294	29`, wenn nur Konstanten gesetzt sind (mit `diff` an Kopien gezählt; es gilt die Differenz: +265 Zeilen, 357 → 622).

## Schritt D0 — alte Fenster aufräumen (vor der Probe)

Fenster ohne Sitzung (UEBERGABE Z. 2481, Stand Umzug 09.10.2026, 11:06; die letzte Sitzung darin endete 11:04:40 MESZ, `logs/sitzungswaechter/waechter.log` Z. 1938: 09:04:40Z): `21040`, `21346`, `21349`, `21560`. Die Sitzung schliesst **nur Fenster aus dieser Liste,** nie das eigene (*schützt:* Fenster des Betreibers) ⇒ `d0_fenster.txt`: `T 'id of every window'` vorher und nachher; je Nummer mit `T`: `exists window id <n>`, `count of tabs of window id <n>`, `tty of tab 1 of window id <n>`, `busy of tab 1 of window id <n>`; dazu `ps -t <tty ohne /dev/> -o pid=,comm=`, `T 'history of tab 1 of window id <n>' | grep -c 'exec claude'` (nur die Zahl; der Verlauf selbst geht in keine Datei, Schranke 3) und einmal `pgrep -a -x Terminal` (mit `-a`: Terminal ist Vorfahr dieser Sitzung, `docs/belege/TB-142/abbruch.txt` Z. 21–22), dann `ps -o lstart= -p <diese PID>` (roh; nennt `pgrep` nicht genau eine PID: nichts schliessen, melden). Geschlossen wird `<n>` nur, wenn es existiert, einen Tab hat, auf seinem tty kein `claude` läuft, `busy` `false` ist, der Verlauf `exec claude` enthält (Zahl ≥ 1), Terminal seit vor dem 09.10.2026, 11:04 MESZ läuft (`lstart` ist Ortszeit des Macs; `date` roh dazu) (sonst können die Nummern neu vergeben sein: nichts schliessen, melden) und M4 `ja` ergab (Tab und M4: **Lesart des Helfers, vorläufig**): `osascript -e 'tell application "Terminal" to close window id <n>'`, nach 1 s `T 'exists window id <n>'`; steht es noch, kein weiteres schliessen (Schranke 1). Ist `tty` leer oder scheitert eine Abfrage: nicht schliessen, mit Grund melden. Was nicht zutrifft oder nicht mehr existiert, bleibt und steht mit Grund im Ergebnis; kein Abbruch.

## Schritt D — Probe V6 über den echten Weg

**Warum Auslöserdatei → launchd → Skript:** Berechtigung und Umgebung hängen am Aufrufer. LIESMICH Z. 239: „Terminalfenster 7963 offen <- 84 s: einmaliger Berechtigungsdialog“; Z. 246–247: „Die 84 Sekunden waren einmalig. Die Automation-Berechtigung gilt jetzt“. Belegt ist damit der Dialog beim ersten Lauf über launchd; dass die Berechtigung am Aufrufer hängt, sagt die LIESMICH nicht ausdrücklich (erschlossen). Ein Aufruf des Skripts aus dieser Sitzung bewiese für den echten Start nichts.

**Wie die Probe an der Wache „es arbeitet bereits eine Sitzung“ vorbeikommt — Vorgabe des steuernden Chats (09.10.2026), in der Einzelfreigabe genannt:** Diese Sitzung ist selbst `claude` mit cwd im Repo. Die Wache 4a für `starte_TB-*` bleibt unberührt. Die Probe ist ein **eigener Auslöser `probe_<PID>`** mit eigener Zählung (W4): Sie läuft nur, wenn im Repo genau **eine** `claude`-Sitzung arbeitet und es die im Dateinamen genannte ist; sie baut keinen Satz, liest keinen Zeiger, beendet die eine dabei entstandene Sitzung und schliesst ihr Fenster. Gelesen wird nur der Dateiname (eine Zahl). *Preis:* Wer Auslöser schreiben kann, kann so für rund 70 s eine zweite Sitzung **ohne Auftrag** im Repo öffnen. *Alternative:* `WAECHTER_PROBE=1 /bin/bash …/starte_sitzung.sh` aus dieser Sitzung — kein neuer Auslöser, aber anderer Aufrufer, also kein Beleg für Berechtigung und Umgebung unter launchd (die plist reicht keine Variablen durch; sie zu ändern schliesst V9 aus). Gebaut ist der erste Weg: Nur er belegt Berechtigung und Umgebung unter launchd.

**Ablauf, mindestens zwei Läufe** (Abstand mindestens 35 s: `ThrottleInterval` 30, plist Z. 36–37):
1. `T 'id of every window'` ⇒ `d_probe<i>_fenster.txt` (vorher); dazu `wc -l < logs/sitzungswaechter/waechter.log` (Z0).
2. `: > docs/auftraege/_ausloeser/probe_<EIGEN>` (PID aus M0).
3. Warten, bis `logs/sitzungswaechter/waechter.log` **hinter Zeile Z0** `----- fertig (probe), rc <r> -----`, `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN` oder `⛔ Konnte Probe-Ausloeser nicht wegraeumen` trägt (alle 10 s nachsehen, höchstens 200 s); dabei für jede `claude`-PID ≠ EIGEN mit cwd im Repo (wie M0) einmal `ps -o command= -p <pid>` an `d_probe<i>_fenster.txt` anhängen (erwartet `--permission-mode manual`; fehlt der Schalter: melden, kein Abbruch). Nach `⛔ Konnte Probe-Ausloeser nicht wegraeumen` oder wenn keine kommt: melden, nicht wiederholen; liegt `probe_<EIGEN>` dann noch in `_ausloeser/`, mit `mv` nach `_ausloeser/_erledigt/` legen (nicht löschen) und im Ergebnis nennen.
4. Die Log-Zeilen ab Z0+1 bis `fertig (probe)` ⇒ `d_probe<i>_log.txt` (Schranke 3); `T 'id of every window'` (nachher) und die `claude`-Prozesse mit cwd im Repo (`pgrep -a`) an die Fensterdatei anhängen.

**Soll je Lauf:** `Fenster <n> neu geoeffnet` mit einer Nummer, die vorher nicht in der Liste stand und je Lauf eine andere ist; `⭐ EINGABEBEREIT (PROBE)`; `Probe: beende PID <p> … PID <EIGEN> bleibt unberuehrt`; `Fenster <n> geschlossen` oder `bleibt offen: <Grund>` wie nach M4 erwartet; danach im Repo nur `EIGEN`; rc 0. **Befund, kein Abbruch:** `⛔ STARTFRAGE` oder `⛔ KEINE EINGABEZEILE` — die Fensterzeilen lesen, höchstens **einmal** Merkmal oder Startzeile nach Schritt C richten und neu proben; steht dort `Lesbar waren 0 von`, nichts richten, melden (Abbruchkriterien: `osascript` hängt oder verlangt eine neue Berechtigung); bleibt es dabei, so abgeben und im Ergebnis sagen, was der Betreiber einmal tun muss. Nach `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN` oder rc 1: Grund aus der Zeile lesen; steht eine andere `claude`-Sitzung ohne Auftrag im Repo, PID wie in M4 bestimmen, `TERM`, einmal neu proben; sonst (greift kein Abbruchkriterium) melden und mit `PROBE: nicht gelaufen, <Grund>` abgeben. Bleibt eine Probe-Sitzung stehen (`NICHT beendet`; die Probe endet dann mit rc 5 statt 0): PID wie in M4 bestimmen, `TERM`. Dann `PROBE:` in `messwerte.txt` nachtragen; der Satz sagt auch, ob die Prozesszeile der Probesitzung `--permission-mode manual` trug (Nr. 3) oder nicht gelesen wurde; ihre Statuszeile steht in keinem Beleg. Commit `TB-144 D: Probe`, pushen.

## Schritt E — Unterlagen (V7, V8)

`PY WZ doku --probe; echo "rc $?"` ⇒ `e_doku_probe.txt`, dann ohne `--probe` ⇒ `e_doku.txt`. `WZ` liest `STARTZEILE`, `STUFEN`, `MERKMAL_EINGABEZEILE`, `MERKMAL_FRAGE` und `FENSTER_SCHLIESSEN` aus `starte_sitzung.sh`, M1–M5 und PROBE aus `messwerte.txt`, die fünf Zeilen zur Abnahme TB-141 unverändert aus `UEBERGABE.md` (Nachtrag 08.10.2026, 21:47; md5 je Zeile in E11) und setzt alles ein; abgetippt wird nichts. Es prüft alle Anker, bevor es schreibt, und weist einen zweiten Lauf ab (rc 2). Soll rc 0, je Stück `… · ok` und:

| Zieldatei | Einfügungen (Anker am HEAD) | Zeilen + (numstat-Soll, entfernt 0) |
|---|---|---|
| `ARBEITSWEISE.md` | E1 (Z. 177, 2 Zeilen), E2 (1889), E3 (1989), E4 (2098), E5 (2232), E12 (2038); E6 (2038) nur bei geänderter Startzeile | **7** · mit E6 **8** |
| `LIESMICH.md` | E7 (vor Z. 10, Abschnitt „Gilt seit TB-144“), E8 (80), E9 (198), E10 (283) | **65** |
| `BACKLOG.md` | E11 (vor Z. 351) | **13** |

**Stellen, denen das neue Verhalten widerspricht** (am HEAD gemessen; je **eine** Zeile „⭐ Gilt seit TB-142 (…): …“ (oder TB-143, TB-144) direkt dahinter, keine Zeile entfernt): `ARBEITSWEISE.md` Z. 1888–1889 (19: „Anlaufzeit abwarten, den Auftragssatz einsetzen“) → E2 · Z. 1988–1989 und 1993 (21: „legt den Auftrag hinein“, „Text einfügen“) → E3 · Z. 2094–2096 (22.4: „bereits ins Terminalfenster gelegt“) → E4 · Z. 2231–2232 (22.9: die Zeile „Satz ins Fenster gelegt“ prüfen) → E5 · Z. 2031–2034 (22.1: Startzeile) → E12; E6 nur, wenn sie sich ändert. `LIESMICH.md` Z. 79–80, 89–92, 98 → E8 · Z. 197–198, 202 → E9 · Z. 279–283 (20 Sekunden, `WAECHTER_WARTESEKUNDEN`) → E10. **Ohne eigene Zeile — Lesart des Helfers, vorläufig:** `ARBEITSWEISE.md` Z. 78 (Abschnitt 0: „auch wenn der Sitzungswächter den Satz schon eingesetzt hat“) — die Regel gilt unverändert, E1 (b) sagt das Neue in derselben Checkliste; Z. 2241 und LIESMICH Z. 233–241 sind Geschichte. **Ausserhalb dieses Auftrags, nur gemeldet:** `docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md` Z. 79, 89, 98, 205 (ältere Fassung der LIESMICH); `docs/auftraege/_ausloeser/LIESMICH.md` und die `.gitignore` dort kennen weder `schliesse_` noch `probe_`.

Commit `TB-144 E: LIESMICH, ARBEITSWEISE, BACKLOG`, pushen.

## Schritt F — Nachweis, Ergebnis, Abgabe

**F1.** `PY WZ nachweis; echo "rc $?"` ⇒ `f1_nachweis.txt`. Soll rc 0: `bash -n rc 0`, `'do script' in Befehlszeilen 1`, verbotene Wörter 0, bash-4 0, kein offener Platzhalter, jede Log-Zeile in Skript und LIESMICH, jede Einfügung `Vorkommen 1 · GLEICH`; je Stück W2–W6 die Zahl der wörtlichen Zeilen (anders sind nur gesetzte Konstanten und gemeldete Abweichungen). Dazu von Hand gezählt: `--permission-mode manual` in Befehlszeilen genau 1.
**F2.** `git diff ⟨S0⟩ HEAD -- docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` ⇒ `f2_diff_waechter.txt` (roh). Soll: Änderungen nur an den Stellen der Stücke; Z. 44–132 und Z. 142–323 des Stands ⟨S0⟩ unverändert (Schranke 4).
**F3. Ergebnis** `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`: Kopf (Stand, Commits, ⟨S0⟩) · **„Kurz“** (Tabelle Soll | Ist je Schritt) · **„Gemessen (M1–M5)“** (je Messung: Befehl, Rohausgabe-Datei, Befund, was daraus im Skript steht; die Probeläufe mit Fensternummern und Sekunden) · **„Abweichungen vom Auftrag“** (jede, auch kleine; sonst „keine“ mit der Liste der geprüften Sollwerte) · **„Nicht getan“** (Ablage; die Posten unter „Nicht in TB-144“; offene Fenster und Aufgaben für den Betreiber; dazu der Satz, dass W5 und W6 in TB-144 nie liefen — die Probe nimmt W4 —, ihr erster Lauf ist der erste echte Start) · **„In einfacher Sprache“**. Ein Probefenster, das die Probe selbst nicht schliessen konnte, schliesst auch `schliesse_<HEAD>` nicht (es ist in `letztes_fenster_probe.txt` gemerkt, nicht in `letztes_fenster.txt`); es bleibt offen, das Log nennt seine Nummer, die Sitzung nennt es im Ergebnis als Aufgabe für den Betreiber.
**F4. Journal.** Die Sitzung schreibt ihren Block nach `docs/belege/TB-144/f4_journal_block.md`, Gliederung wie Block EJ: Kopfzeile `## <Kennung> — TB-144: …`, Quellenzeile, Absatz „**Quelle:**“, `### Was gemessen ist`, `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-144. Quellenvermerk: siehe Kopf.*`; kein `---`, nicht der Nachtrag J1 — was TB-144 selbst tat, schreibt die Sitzung in eigenen Worten. Dann `PY WZ journal docs/belege/TB-144/f4_journal_block.md --probe` ⇒ `f4_journal_probe.txt`, ohne `--probe` ⇒ `f4_journal.txt`. Soll: sechs Bedingungen `ja`, Kennung **EK**, `J1-Zeilen 8`, rc 0. rc 2: Bedingung lesen, Block richten, neu.
**F5.** Abgabe-Commit `TB-144 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Dann `git status --porcelain > "$TMPDIR/tb144_f5.txt"`, unverändert nach `f5_porcelain.txt` kopieren (`cmp` gleich; Soll 0 B), erst danach die Kopfdatei und `git diff --numstat ⟨S0⟩ <Abgabe>` roh ⇒ `f5_numstat.txt`. Soll: `starte_sitzung.sh` `294	29` (Differenz +265, siehe Schritt C) · `LIESMICH.md` `65	0` · `ARBEITSWEISE.md` `7	0` (mit E6 `8	0`) · `BACKLOG.md` `13	0` · `JOURNAL.md` `<n>	0` mit n = Zeilen des eigenen Blocks + 8 + 1 + 3 · sonst nur Ergebnis und Belege; ausser in `starte_sitzung.sh` nirgends eine entfernte Zeile. Kleiner letzter Commit `TB-144 F5: porcelain und numstat nach der Abgabe`, pushen; danach `git status --porcelain` noch einmal, Rohausgabe wörtlich in der Schlussmeldung.

**Teilabgabe — nur wenn in Schritt B kein Merkmal messbar ist;** ein eigener, erlaubter Ausgang, kein ABBRUCH. Der Wächter steht am Stand ⟨S0⟩; C, D0, D, E, F1, F2 und F4 entfallen. Die Sitzung führt **weder `WZ doku` noch `WZ journal` noch `WZ nachweis`** aus (ohne die Konstanten aus Schritt C enden alle drei mit rc 3); `LIESMICH.md`, `ARBEITSWEISE.md`, `BACKLOG.md` und `JOURNAL.md` bleiben unberührt — sie kommen mit dem Folgeauftrag. Sie schreibt das Ergebnis wie in F3, **als Erstes:** welche Frage der Betreiber einmal beantworten muss (wörtlich) und in welchem Fenster sie steht (Testfenster, Nummer, offen oder geschlossen). Commit `TB-144 Teilabgabe: Ergebnis, Waechter am Stand S0` mit Belegen und Ergebnis, jede Datei mit Namen, pushen; dann `porcelain` als Rohausgabe und numstat wie in F5 (kleiner letzter Commit, pushen). **numstat-Soll der Teilabgabe:** alle fünf Zieldateien `0	0` oder nicht in der Ausgabe, in keinem Commit der Sitzung · sonst nur Ergebnis und Belege.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab.
- Schritt A endet mit ABBRUCH: nichts ist gebaut — **das in der Meldung als Erstes sagen.**
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung** (ganze Sitzung): melden, nicht umgehen. Verlangt schon Schritt 0 oder der Abbruchweg selbst (Belege committen, pushen) eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden. *Schützt:* vor einem halben Bau wie in TB-142. Gesperrt: `rm`, `chmod`, `export`, `env`, `security` usw.
- Ein Schritt verlangte eine Taste, ein Enter, System Events oder Text in ein bestehendes Fenster.
- `osascript` hängt oder verlangt eine neue Berechtigung; eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Nach jedem Abbruch** steht `starte_sitzung.sh` am Stand ⟨S0⟩ oder an einem Stand, der `/bin/bash -n` besteht, in Befehlszeilen genau ein `do script` ohne ` in window` und genau einmal `--permission-mode manual` trägt und keinen Wert `<<M…>>` (ab Schritt E zusätzlich `nachweis` rc 0, wenn `doku` geschrieben hat); sonst zuerst ⟨S0⟩ zurückholen (`git show ⟨S0⟩:<pfad>` in eine Kopie, `bash -n`, `mv`). **Es bleibt kein Zustand, in dem ein Start-Auslöser Text in ein Fenster gibt.** Läuft dann noch eine Test- oder Probesitzung dieser Sitzung im Repo: per PID mit `kill -TERM` beenden — nur eine `claude`-PID ≠ EIGEN mit cwd im Repo (wie M0), die nach dieser Sitzung gestartet ist (`ps -o lstart= -p <pid>` gegen die eigene; sonst nicht beenden, melden); abweichend von Schranke 7 genügt hier cwd statt des tty, weil `osascript` ausgefallen sein kann; ihr Fenster bleibt offen und steht in der Meldung. *Schützt:* Die Wache „es arbeitet bereits eine Sitzung“ wiese sonst den nächsten Start ab. **Kein Abbruch:** `waechter bau`, `doku` oder `journal` mit rc ≠ 0 (nichts geschrieben; Grund lesen, richten wie in Schritt C oder auslassen und melden); eine Messung trägt nicht; eine Kennung ≠ EK. **Eigener, erlaubter Ausgang, kein ABBRUCH:** die **Teilabgabe** (Schritt F), wenn in Schritt B kein Merkmal messbar ist — keine `abbruch.txt`. Bei Abbruch: Belege committen, Grund in `docs/belege/TB-144/abbruch.txt`, pushen, melden.

## Nicht in TB-144 (V9)

Der übrige Regelwerk-Nachtrag (UEBERGABE, Umzug 08.10.2026, 19:58, Block 4 Nr. 6); das Abschicken des Satzes durch den Wächter; Änderungen an `einschalten.sh` und der plist; die Stellen „ausserhalb dieses Auftrags“ aus Schritt E; die Ablage.

## In einfacher Sprache

Der kleine Wächter auf dem Mac, der für dich die Claude-Code-Sitzung startet, hat seit Ende September ins falsche Fenster geschaut und trotzdem „alles gut“ gemeldet. Dieser zweite Anlauf richtet ihn (zuerst prüft die Sitzung, ob Claude Code ihr die Befehle erlaubt): Er öffnet ein neues Fenster, merkt sich genau dieses, sieht nach, ob Claude Code wirklich auf eine Eingabe wartet, und schreibt die Wahrheit ins Protokoll. Den Auftragssatz legt er nicht mehr ins Fenster — den schickst du wie bisher selbst ab. Vorher probiert die Sitzung den neuen Wächter mindestens zweimal aus, ohne einen Auftrag zu starten; dabei erscheinen in der Claude-App kurz Gerätesitzungen, die gleich wieder verschwinden.

## Anhang A — Wächterstücke W2–W6 (Entwurf der neuen Zeilen, wörtlich)

#### W2 — Konstanten und Funktionen (V1, V2, V3, V5)

Zieldatei: `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`
Art: nach
Form: Block
Anker: ⟦sage "----- Waechter geweckt -----"⟧

Am HEAD: Anker Z. 43.

~~~
# ⭐⭐ SEIT TB-144 (Waechter-Reparatur). Anlass: Fehler Nr. 23 - 20 Starts in
#    Folge meldeten das VORDERSTE Fenster (15501) statt des neu geoeffneten,
#    und der Satz ging samt Zeilenende in eine bash-Shell.
# ⛔ Der Waechter legt KEINEN Satz mehr in ein Fenster, schickt nichts ab und
#    drueckt keine Taste. Den Fensterinhalt LIEST er nur, ueber Terminal selbst.
# ⛔ Ins Log gehen hoechstens die letzten 8 Zeilen (je 160 Zeichen) des NEU
#    GEOEFFNETEN Fensters, und nur, wenn die Pruefung scheitert. Sonst gilt der
#    Kopf dieser Datei: keine Umgebungsvariablen, Schluessel, Dateiinhalte.
# ⚠️ /bin/bash des Macs ist 3.2: nur Mittel, die es dort gibt.
# ⚠️ Solange ein Wert mit <<M…>> dasteht, oeffnet der Waechter KEIN Fenster.
# --------------------------------------------------------------------------
STARTZEILE="cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control"
MERKMAL_FRAGE="Enter to confirm"
MERKMAL_EINGABEZEILE="<<M2_MERKMAL_EINGABEZEILE>>"
LESE_EIGENSCHAFT="contents"
STUFEN="3 3 4 5 5 10 10 10 10"
FENSTER_SCHLIESSEN="<<M4_JA_ODER_NEIN>>"
FENSTERDATEI="$LOGDIR/letztes_fenster.txt"
FENSTER=""
TABNR=""

ziffern() {
    case "$1" in ''|*[!0-9]*) return 1 ;; esac
    return 0
}

# PIDs aller claude-Prozesse mit cwd im Repo; gelesen wird nur das cwd (wie Wache 4a).
claude_im_repo() {
    local pid cwd
    for pid in $(pgrep -x claude 2>/dev/null); do
        cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
        case "$cwd" in "$REPO"|"$REPO"/*) echo "$pid" ;; esac
    done
}

fensterliste() {
    osascript <<OSA 2>>"$LOG"
tell application "Terminal" to return id of every window
OSA
}

fenster_starten() {
    osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    set neu to do script "$STARTZEILE"
    return neu
end tell
OSA
}

# Nur lesen. M2: LESE_EIGENSCHAFT am Funktionsverzeichnis von Terminal pruefen.
fenster_lesen() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal" to return $LESE_EIGENSCHAFT of tab $TABNR of window id $FENSTER
end timeout
OSA
}

fenster_tty() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal" to return tty of tab $TABNR of window id $FENSTER
end timeout
OSA
}

# M4: schliesst Terminal ein Fenster ohne laufenden Prozess ohne Rueckfrage?
fenster_zu() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal"
        if not (exists window id $1) then return "fehlt"
        if (count of tabs of window id $1) is not 1 then return "mehrere"
        if busy of tab 1 of window id $1 then return "arbeitet"
        close window id $1
        delay 1
        if exists window id $1 then return "offen"
        return "zu"
    end tell
end timeout
OSA
}

# V1: Die Fensternummer kommt aus dem Tab, den Terminal beim Oeffnen liefert.
# M1: Form der Rueckgabe "tab <k> of window id <n>" - belegt nur fuer den alten
#     zweiten Aufruf (launchd_aus.log, 51 Zeilen); fuers Oeffnen misst TB-144.
fenster_oeffnen() {
    local vorher nachher tab rest
    FENSTER=""
    TABNR=""
    case "$MERKMAL_EINGABEZEILE$FENSTER_SCHLIESSEN$STARTZEILE" in
        *"<<"*)
            sage "⛔ MESSWERTE FEHLEN in starte_sitzung.sh (TB-144). Kein Fenster geoeffnet."
            return 1 ;;
    esac
    vorher=$(fensterliste) || {
        sage "⛔ FENSTERLISTE NICHT LESBAR: Terminal nennt seine Fenster nicht. Kein Fenster geoeffnet."
        return 1
    }
    vorher=" $(printf '%s' "$vorher" | tr -c '0-9' ' ') "
    tab=$(fenster_starten) || {
        sage "⛔ osascript konnte Terminal nicht ansteuern. Fehlt die Automation-Berechtigung?"
        return 1
    }
    nachher=" $(fensterliste | tr -c '0-9' ' ') "
    case "$tab" in
        "tab "*" of window id "*)
            rest="${tab#tab }"
            TABNR="${rest%% of window id *}"
            FENSTER="${tab##* of window id }" ;;
    esac
    if ! ziffern "$TABNR" || ! ziffern "$FENSTER"; then
        sage "⛔ FENSTER NICHT BESTIMMBAR: Terminal lieferte keinen Tab der Form 'tab <k> of window id <n>'. Ein Fenster kann trotzdem offen sein."
        FENSTER=""
        return 1
    fi
    case "$vorher" in *" $FENSTER "*)
        sage "⛔ FENSTER NICHT NEU: Fenster $FENSTER gab es schon vor dem Oeffnen. Es wird weder gelesen noch gemerkt."
        FENSTER=""
        return 1 ;;
    esac
    case "$nachher" in *" $FENSTER "*) : ;; *)
        sage "⛔ FENSTER FEHLT: Fenster $FENSTER steht nach dem Oeffnen nicht in der Fensterliste."
        FENSTER=""
        return 1 ;;
    esac
    printf '%s\n' "$FENSTER" > "$FENSTERDATEI"
    sage "Fenster $FENSTER neu geoeffnet (Tab $TABNR). Gemerkt in $FENSTERDATEI"
    return 0
}

# ⛔ Begrenzt: hoechstens 8 Zeilen, je 160 Zeichen, nur vom neu geoeffneten Fenster.
fensterzeilen() {
    local z
    sage "   Letzte Zeilen von Fenster $FENSTER (hoechstens 8, je 160 Zeichen):"
    printf '%s\n' "$1" | tr '\r' '\n' | grep -v '^[[:space:]]*$' | tail -n 8 | cut -c1-160 | while IFS= read -r z; do
        sage "   | $z"
    done
}

# V3: Pruefung statt Wartezeit. $1 = Kennung fuers Log (TB-Nummer oder PROBE).
# Rueckgabe: 0 eingabebereit · 3 Startfrage · 4 keine Eingabezeile.
warte_auf_eingabezeile() {
    local kenn="$1" summe=0 lesung=0 gelesen=0 bereit=0 inhalt="" s
    for s in $STUFEN; do
        sleep "$s"
        summe=$((summe+s))
        lesung=$((lesung+1))
        inhalt=$(fenster_lesen) || { inhalt=""; bereit=0; continue; }
        gelesen=$((gelesen+1))
        case "$inhalt" in
            *"$MERKMAL_FRAGE"*)
                sage "⛔ STARTFRAGE ($kenn): Fenster $FENSTER zeigt nach $summe s eine Frage (\"$MERKMAL_FRAGE\"). Die Sitzung ist NICHT eingabebereit."
                fensterzeilen "$inhalt"
                return 3 ;;
            *"$MERKMAL_EINGABEZEILE"*)
                bereit=$((bereit+1))
                if [ "$bereit" -ge 2 ]; then
                    sage "⭐ EINGABEBEREIT ($kenn): Fenster $FENSTER, Eingabezeile steht, keine Frage offen (nach $summe s, Lesung $lesung). ⚠️ KEIN SATZ IM FENSTER."
                    return 0
                fi ;;
            *)  bereit=0 ;;
        esac
    done
    sage "⛔ KEINE EINGABEZEILE ($kenn): Fenster $FENSTER zeigt nach $summe s keine Eingabezeile von Claude Code (verlangt: zwei Lesungen in Folge). Die Sitzung gilt als NICHT eingabebereit."
    sage "   Lesbar waren $gelesen von $lesung Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal)."
    fensterzeilen "$inhalt"
    return 4
}

# V5: nur das EINE gemerkte Fenster; nur ohne claude-Sitzung im Repo (ausser der
# PID in $1, die die Probe ausloest), nur ein Tab, nur ohne laufenden Prozess.
fenster_aufraeumen() {
    local ausser="${1:-}" f pid antwort
    if [ ! -f "$FENSTERDATEI" ]; then
        sage "  Kein gemerktes Fenster. Nichts aufzuraeumen."
        return 0
    fi
    f=$(head -n 1 "$FENSTERDATEI" | tr -d '\r')
    if ! ziffern "$f"; then
        sage "  ⚠️ $FENSTERDATEI nennt keine Fensternummer. Nichts geschlossen."
        return 0
    fi
    for pid in $(claude_im_repo); do
        [ "$pid" = "$ausser" ] && continue
        sage "  ⚠️ Fenster $f bleibt offen: im Repo laeuft noch eine claude-Sitzung (PID $pid)."
        return 0
    done
    if [ "$FENSTER_SCHLIESSEN" != "ja" ] && [ "$FENSTER_SCHLIESSEN" != "nein" ]; then
        sage "  ⚠️ Fenster $f bleibt offen: FENSTER_SCHLIESSEN steht weder auf ja noch auf nein (Messwert M4 fehlt)."
        return 0
    fi
    if [ "$FENSTER_SCHLIESSEN" != "ja" ]; then
        sage "  ⚠️ Fenster $f bleibt offen: Terminal schliesst es nicht ohne Rueckfrage (gemessen in TB-144)."
        return 0
    fi
    antwort=$(fenster_zu "$f")
    case "$antwort" in
        zu)
            mv "$FENSTERDATEI" "$LOGDIR/letztes_fenster_geschlossen.txt" 2>/dev/null
            sage "  Fenster $f geschlossen (das beim Start gemerkte, kein laufender Prozess)." ;;
        fehlt)    sage "  Fenster $f gibt es nicht mehr. Nichts geschlossen." ;;
        arbeitet) sage "  ⚠️ Fenster $f bleibt offen: dort laeuft noch ein Prozess." ;;
        mehrere)  sage "  ⚠️ Fenster $f bleibt offen: es hat mehr als einen Tab." ;;
        *)        sage "  ⚠️ Fenster $f bleibt offen: Terminal hat das Schliessen nicht bestaetigt." ;;
    esac
    return 0
}
~~~

#### W3 — Schliess-Auslöser: gemerktes Fenster aufräumen (V5)

Zieldatei: `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`
Art: vor
Anker: ⟦    sage "----- fertig (schliessen) -----"⟧

Am HEAD: Anker Z. 133.

~~~
    # ⭐ Seit TB-144 (V5): das beim Start gemerkte Fenster aufraeumen.
    fenster_aufraeumen
~~~

#### W4 — Probe-Auslöser `probe_<PID>` (V6)

Zieldatei: `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`
Art: vor
Form: Block
Anker: ⟦DATEI=""⟧

Am HEAD: Anker Z. 141.

~~~
# ⭐ 1a. PROBE-AUSLOESER (seit TB-144): Datei probe_<PID>
#    Oeffnet ein Fenster wie ein echter Start (gleicher Ordner, gleiche
#    Startzeile, dieselben Funktionen), prueft die Eingabezeile, beendet GENAU
#    DIE EINE dabei entstandene Sitzung mit TERM und raeumt das Fenster auf.
#    KEIN Auftrag, KEIN Satz. <PID> ist die eine claude-Sitzung im Repo, die
#    die Probe ausloest; nur sie wird nicht gezaehlt. Laeuft im Repo eine
#    andere, oder ist <PID> keine claude-Sitzung im Repo: ABBRUCH, kein Fenster.
# ⚠️ Die Wache 4a fuer echte Starts steht unveraendert weiter unten.
# ⚠️ Auch hier wird nur der DATEINAME gelesen, nie der Inhalt.
PROBE=""
for f in "$AUSLOESER"/probe_*; do
    [ -e "$f" ] || continue
    PROBE="$f"
    break
done
if [ -n "$PROBE" ]; then
    EIGEN="$(basename "$PROBE")"
    EIGEN="${EIGEN#probe_}"
    STEMPEL="$(date -u '+%Y%m%dT%H%M%SZ')"
    if ! ziffern "$EIGEN" || [ ${#EIGEN} -gt 7 ]; then
        mv "$PROBE" "$ERLEDIGT/ABGEWIESEN_${STEMPEL}_probe" 2>/dev/null
        sage "⛔ ABGEWIESEN: Der Probe-Ausloeser nennt keine gueltige PID."
        exit 1
    fi
    mv "$PROBE" "$ERLEDIGT/${STEMPEL}_probe_$EIGEN" || { sage "⛔ Konnte Probe-Ausloeser nicht wegraeumen. Abbruch."; exit 1; }
    sage "----- Probe-Ausloeser: probe_$EIGEN -----"
    GENANNT=0
    ANDERE=0
    for pid in $(claude_im_repo); do
        if [ "$pid" = "$EIGEN" ]; then GENANNT=1; else ANDERE=$((ANDERE+1)); fi
    done
    if [ "$GENANNT" -ne 1 ] || [ "$ANDERE" -ne 0 ]; then
        sage "⛔ ABBRUCH (Probe): PID $EIGEN als claude-Sitzung im Repo: $GENANNT (verlangt 1), andere claude-Sitzungen im Repo: $ANDERE (verlangt 0). Kein Fenster geoeffnet."
        exit 1
    fi
    if ! security show-keychain-info "$HOME/Library/Keychains/login.keychain-db" > /dev/null 2>&1; then
        sage "⛔ ABBRUCH (Probe): Schluesselbund gesperrt. Kein Fenster geoeffnet."
        exit 1
    fi
    FENSTERDATEI="$LOGDIR/letztes_fenster_probe.txt"
    fenster_oeffnen || { sage "----- fertig (probe), rc 1 -----"; exit 1; }
    warte_auf_eingabezeile "PROBE"
    RC=$?
    # Beendet wird nur, was im Repo laeuft, NICHT die genannte PID ist und am
    # Terminal des neuen Tabs haengt.
    TTY_TAB="$(fenster_tty)"
    for pid in $(claude_im_repo); do
        [ "$pid" = "$EIGEN" ] && continue
        TTY_PID="$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')"
        if [ -n "$TTY_PID" ] && [ "/dev/$TTY_PID" = "$TTY_TAB" ]; then
            sage "  Probe: beende PID $pid ($TTY_PID) mit TERM. PID $EIGEN bleibt unberuehrt."
            kill -TERM "$pid" 2>/dev/null
        else
            sage "  ⚠️ Probe: PID $pid haengt nicht am neuen Tab (${TTY_PID:-?} gegen ${TTY_TAB:-?}). NICHT beendet."
            [ "$RC" -eq 0 ] && RC=5    # 5: eingabebereit, aber eine Probe-Sitzung steht noch
        fi
    done
    sleep 5
    fenster_aufraeumen "$EIGEN"
    sage "----- fertig (probe), rc $RC -----"
    exit "$RC"
fi
~~~

#### W5 — Start: Fenster öffnen, Nummer aus dem Tab (V1)

Zieldatei: `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`
Art: ersetze
Anker: ⟦sage "Starte Terminal-Fenster (Auftrag als Argument) ..."⟧
Bis: ⟦sage "$WARTE s gewartet."⟧

Am HEAD: Anker Z. 324, Bis Z. 339.

~~~
sage "Starte Terminal-Fenster (seit TB-142: ohne Satz) ..."
fenster_oeffnen || abbruch "Das neue Terminal-Fenster ist nicht offen oder nicht bestimmbar - siehe die Zeile davor im Protokoll."
~~~

#### W6 — Schluss: Eingabezeile prüfen, kein Satz (V3, V4)

Zieldatei: `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`
Art: ersetze-bis-ende
Anker: ⟦# 7. Hat der Auftrag gegriffen? Messen statt annehmen.⟧

Am HEAD: Anker Z. 342.

~~~
# 7. Steht die Eingabezeile? Lesen statt warten (seit TB-144).
# --------------------------------------------------------------------------
# ⛔ Der Satz wird NICHT mehr ins Fenster gelegt (V4): Der Terminal-Befehl,
#   der Text in ein vorhandenes Fenster gibt, schickt eine Befehlszeile samt
#   Zeilenende - im richtigen Fenster waere das das Abschicken, das
#   ARBEITSWEISE 19 ausschliesst. Der Satz steht in der Datei.
printf '%s\n' "$SATZ" > "$LOGDIR/letzter_satz.txt"
warte_auf_eingabezeile "$NUMMER"
RC=$?
sage "   Der Waechter legt keinen Satz ins Fenster. Wortlaut: $LOGDIR/letzter_satz.txt"
if [ "$RC" -eq 0 ]; then
    sage "   Der Betreiber schickt ihn ab - in der Claude-App unter der"
    sage "   Geraetesitzung (Laptop-Symbol) oder im Terminal-Fenster $FENSTER."
else
    sage "   Fenster $FENSTER bleibt offen. Schliessen: _ausloeser/schliesse_<HEAD> (ARBEITSWEISE 22.8)."
    printf '%s\n' "Start $NUMMER: Fenster $FENSTER ist nicht eingabebereit (Rueckgabe $RC). Siehe waechter.log." > "$LOGDIR/letzter_abbruch.txt"
fi
sage "----- fertig -----"
exit "$RC"
~~~

## Anhang B — Einfügungen E1–E12 und J1 (wörtlich)

#### E1 — ARBEITSWEISE Abschnitt 0, Gruppe „Wenn eine Mac-Sitzung startet, endet oder abbricht“: (a) Regel 08.10.2026, 21:26 · (b) Log-Zeilen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦| ☐ | Die Sonde `starte_TB-99` vor dem Zeigerwechsel legen⟧

Am HEAD: Anker Z. 177.

~~~
| ☐ | ⭐⭐ Den Start der Claude-Code-Sitzung führt der steuernde Chat immer selbst aus; der Betreiber bekommt lediglich den Text mit der Anweisung (Betreiber 08.10.2026, 21:26: „`cd ~/trading-bot && claude --effort high --remote-control` + enter sollst du zukünftig immer ausführen und mir lediglich den Text schicken mit der Anweisung. Merke dir das für die Zukunft“). Weg: der Sitzungswächter über `starte_TB-<Nr>` (Terminal bleibt für den steuernden Chat Stufe „click“); seine Startzeile steht in `starte_sitzung.sh` (`STARTZEILE`) | 19; 22.9; LIESMICH, „Gilt seit TB-144“; UEBERGABE, Nachtrag 08.10.2026, 21:47 |
| ☐ | Nach einem Start-Auslöser stützt sich der steuernde Chat auf die Zeile des Wächter-Logs für diese Nummer und auf den eigenen Blick ins Fenster (Fehler Nr. 23): „⭐ EINGABEBEREIT (TB-<Nr>)“ heisst Eingabezeile steht, keine Frage offen, kein Satz im Fenster; „⛔ STARTFRAGE (TB-<Nr>)“ und „⛔ KEINE EINGABEZEILE (TB-<Nr>)“ heissen nicht eingabebereit, die letzten Zeilen des Fensters stehen im Log; steht keine der drei Zeilen da (⛔ ABBRUCH davor), gilt dasselbe — dann „Satz abschicken“ nicht als Aufgabe geben. Die Zeile „Satz ins Fenster gelegt“ gibt es seit TB-142 nicht mehr; der Wächter legt keinen Satz mehr ins Fenster | 22.9; LIESMICH, „Gilt seit TB-144“; UEBERGABE, Umzug 08.10.2026, 19:58, Block 7 (Nr. 23) |
~~~

#### E2 — ARBEITSWEISE 19, „Was er dir abnimmt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦Auftragssatz einsetzen (zeichengleich, aus der geprüften Nummer selbst gebaut).⟧

Am HEAD: Anker Z. 1889.

~~~
⭐ **Gilt seit TB-142 (Wächter-Reparatur, Fehler Nr. 23):** Er setzt den Satz nicht mehr ein und gibt keinen Text mehr in ein bestehendes Fenster. Seit TB-144 wartet er keine feste Anlaufzeit ab: Er öffnet ein neues Fenster, liest dessen Inhalt bis höchstens 60 s und meldet „⭐ EINGABEBEREIT“, „⛔ STARTFRAGE“ oder „⛔ KEINE EINGABEZEILE“; der Satz steht in `logs/sitzungswaechter/letzter_satz.txt` (`docs/werkzeuge/sitzungswaechter/LIESMICH.md`, „Gilt seit TB-144“).
~~~

#### E3 — ARBEITSWEISE 21, Betreiberentscheidung 23.09.2026, 18:28

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦wird er vom Betreiber.** Das ist der Weg, keine Notlösung.⟧

Am HEAD: Anker Z. 1989.

~~~
⭐ **Gilt seit TB-142 (Wächter-Reparatur, Fehler Nr. 23):** Der Wächter legt den Auftrag nicht mehr ins Fenster; in der Tabelle darunter entfällt „Text einfügen“, und seit TB-144 prüft er statt der „Anlaufzeit“, ob die Eingabezeile steht. Abgeschickt wird weiter vom Betreiber.
~~~

#### E4 — ARBEITSWEISE 22.4

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦einfügen, und dann braucht er ihn im Chat.⟧

Am HEAD: Anker Z. 2098.

~~~
⭐ **Gilt seit TB-142 (Wächter-Reparatur, Fehler Nr. 23):** Der Wächter legt den Satz nicht mehr ins Terminalfenster, und die Meldung „Satz ins Fenster gelegt“ gibt es nicht mehr. Die Regel dieses Abschnitts gilt unverändert; der Satz erreicht den Betreiber jetzt nur noch über das Kopierfeld und über `logs/sitzungswaechter/letzter_satz.txt`.
~~~

#### E5 — ARBEITSWEISE 22.9, Punkt 2

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦**„Satz ins Fenster gelegt“** für diese Nummer.⟧

Am HEAD: Anker Z. 2232.

~~~
   ⭐ **Gilt seit TB-144 (Wächter-Reparatur, Fehler Nr. 23):** Die Zeile heisst jetzt „⭐ EINGABEBEREIT (TB-<Nr>)“. Steht dort „⛔ STARTFRAGE“ oder „⛔ KEINE EINGABEZEILE“, ist die Sitzung nicht eingabebereit. Dazu sieht der steuernde Chat selbst ins Fenster (Abschnitt 0, Gruppe „Wenn eine Mac-Sitzung startet, endet oder abbricht“).
~~~

#### E6 — ARBEITSWEISE 22.1 — nur wenn die Startzeile geändert ist

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Bedingung: nur wenn STARTZEILE vom HEAD abweicht
Anker: ⟦Beleg ist deshalb die Prozesszeile, nicht die Anzeige.⟧

Am HEAD: Anker Z. 2038.

~~~
⭐ **Gilt seit TB-144 (Wächter-Reparatur, Fehler Nr. 23):** Die Startzeile des Wächters lautet jetzt `⟦STARTZEILE⟧` (Konstante `STARTZEILE` in `starte_sitzung.sh`); die bisherigen Schalter bleiben. Was die Probe dazu gemessen hat: `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`, „Gemessen (M1–M5)“.
~~~

#### E7 — LIESMICH: neuer Abschnitt „Gilt seit TB-144“, ganz oben

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: vor
Form: Block
Anker: ⟦## ⭐ Der Befund, der dahintersteht (gemessen 23.09.2026)⟧

Am HEAD: Anker Z. 10.

~~~
## ⭐⭐ Gilt seit TB-144 (Wächter-Reparatur)

**Dieser Abschnitt geht allem vor, was weiter unten anders steht.** Das Alte bleibt als Geschichte stehen; wo es nicht mehr gilt, folgt ihm eine Zeile „⭐ Gilt seit TB-142“ (kein Satz), „… TB-143“ (Startzeile) oder „… TB-144“.

**Der Anlass (Fehler Nr. 23):** Seit dem 29.09.2026 meldeten 20 Starts in Folge „Terminal-Fenster 15501“ — das vorderste Fenster, nicht das neu geöffnete. Der Satz ging samt Zeilenende in eine bash-Shell („-bash: TB-141:: command not found“), die Sitzung stand in einem anderen Fenster an einer Startfrage, und das Log meldete „Satz ins Fenster gelegt“.

### Was der Wächter nach `starte_TB-<Nr>` jetzt tut

| | |
|---|---|
| **Öffnen** | ein **neues** Terminal-Fenster mit der Startzeile `⟦STARTZEILE⟧` |
| **Fenster** | Die Nummer kommt aus dem Tab, den Terminal beim Öffnen zurückgibt. Gab es sie schon vorher, bricht er ab |
| **Merken** | Die Nummer steht in `logs/sitzungswaechter/letztes_fenster.txt` |
| **Prüfen** | Er **liest** den Inhalt dieses Fensters über Terminal selbst, in Stufen von ⟦STUFEN⟧ Sekunden, zusammen höchstens 60 s |
| **Melden** | eine der drei Zeilen unten; bei ⛔ ist sein Rückgabewert 3 oder 4. Kann er das neue Fenster nicht bestimmen („⛔ MESSWERTE FEHLEN“, „⛔ FENSTERLISTE NICHT LESBAR“, „⛔ osascript konnte Terminal nicht ansteuern“, „⛔ FENSTER NICHT BESTIMMBAR“, „⛔ FENSTER NICHT NEU“, „⛔ FENSTER FEHLT“, danach „⛔ ABBRUCH“), prüft er nichts, Rückgabewert 1 — ein Fenster kann dann trotzdem offen sein |
| ⛔ **Kein Satz** | Er legt den Auftragssatz **nicht mehr** ins Fenster (schon seit TB-142). Der Satz steht in `logs/sitzungswaechter/letzter_satz.txt` und als Kopierblock in der Antwort des steuernden Chats; abgeschickt wird er vom Betreiber |

**Warum kein Satz mehr:** Der Terminal-Befehl, der Text in ein vorhandenes Fenster gibt (`do script … in window`), schickt eine Befehlszeile **samt Zeilenende**. Im richtigen Fenster wäre das das Abschicken, das die Betreiberentscheidung vom 23.09.2026 ausschliesst.

### Die Zeilen im Wächter-Log

```
⭐ EINGABEBEREIT (TB-<Nr>): Fenster <n>, Eingabezeile steht, keine Frage offen (nach <s> s, Lesung <i>). ⚠️ KEIN SATZ IM FENSTER.
⛔ STARTFRAGE (TB-<Nr>): Fenster <n> zeigt nach <s> s eine Frage ("Enter to confirm"). Die Sitzung ist NICHT eingabebereit.
⛔ KEINE EINGABEZEILE (TB-<Nr>): Fenster <n> zeigt nach <s> s keine Eingabezeile von Claude Code (verlangt: zwei Lesungen in Folge). Die Sitzung gilt als NICHT eingabebereit.
   Lesbar waren <g> von <i> Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal).
Fenster <n> neu geoeffnet (Tab <k>). Gemerkt in <Pfad>/letztes_fenster.txt
  Fenster <n> geschlossen (das beim Start gemerkte, kein laufender Prozess).
  ⚠️ Fenster <n> bleibt offen: <Grund>.
```

Bei ⛔ stehen darunter die letzten Zeilen des neu geöffneten Fensters (höchstens 8, je 160 Zeichen), und das Fenster bleibt offen. **Woran er die Eingabezeile erkennt (Merkmal gemessen; zwei Lesungen: Lesart, vorläufig):** Der Fensterinhalt enthält in zwei Lesungen hintereinander `⟦MERKMAL_EINGABEZEILE⟧` und in keiner `⟦MERKMAL_FRAGE⟧`.

### Fenster aufräumen

Nach `schliesse_<HEAD>` (beide Wachen unverändert: HEAD-Gleichheit, 600 s) schliesst der Wächter **genau das gemerkte Fenster** — nur wenn im Repo keine `claude`-Sitzung mehr läuft, das Fenster genau einen Tab hat und darin kein Prozess mehr läuft. Sonst bleibt es offen, und das Log nennt den Grund. Schalter im Skript: `FENSTER_SCHLIESSEN="⟦FENSTER_SCHLIESSEN⟧"`. Kein anderes Fenster wird angefasst. Ein Probefenster, das die Probe selbst nicht schliessen konnte, schliesst auch `schliesse_<HEAD>` nicht (es ist in `letztes_fenster_probe.txt` gemerkt, nicht in `letztes_fenster.txt`); es bleibt offen, das Log nennt seine Nummer, schliessen muss es der Betreiber.

### Probe ohne Auftrag: `probe_<PID>`

Eine Datei `docs/auftraege/_ausloeser/probe_<PID>` öffnet ein Fenster wie ein echter Start (gleicher Ordner, gleiche Startzeile, dieselben Funktionen), prüft die Eingabezeile, beendet genau die dabei entstandene Sitzung mit `TERM` und räumt das Fenster auf — kein Auftrag, kein Satz. `<PID>` ist die eine `claude`-Sitzung im Repo, die die Probe auslöst; läuft dort eine andere, bricht die Probe ab. Wache 3 für echte Starts ist unverändert; gelesen wird nur der Dateiname. Rückgabewert der Probe wie beim Start; dazu **5**, wenn die Eingabezeile stand, das Log aber „NICHT beendet“ meldet: Eine `claude`-Sitzung im Repo hing nicht am neuen Tab und läuft weiter.

### Gemessen in TB-144

| | |
|---|---|
| **M1** Fenster zu einem Tab | ⟦M1⟧ |
| **M2** Eingabezeile im Fensterinhalt | ⟦M2⟧ |
| **M3** `--no-chrome` | ⟦M3⟧ |
| **M4** Schliessen ohne Rückfrage | ⟦M4⟧ |
| **M5** „Teach auto mode“ beim Start | ⟦M5⟧ |
| **Probe** über Auslöser und launchd | ⟦PROBE⟧ |

Rohausgaben: `docs/belege/TB-144/`. Ergebnis: `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`.

### Was bleibt

Kein Enter, kein Tastendruck, kein Abschicken durch den Wächter; den Fensterinhalt liest er nur. Die sechs Wachen vor dem Start und die zwei Wachen des Schliess-Auslösers sind unverändert. Der steuernde Chat sieht nach jedem Start weiter selbst ins Fenster: Die Log-Zeile sagt, was der Wächter bis höchstens 60 s nach dem Öffnen gelesen hat — nicht, was danach erscheint.

**In einfacher Sprache:** Der Wächter öffnet ein neues Fenster, startet dort Claude Code und sieht dann selbst nach, ob Claude Code auf eine Eingabe wartet. Nur dann schreibt er „eingabebereit“ ins Protokoll. Steht dort eine Frage, schreibt er das hin. Den Auftragssatz legt er nicht mehr ins Fenster; den schickst du selbst ab, in der Claude-App oder im Fenster.

---
~~~

#### E8 — LIESMICH, „kein Return“

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: nach
Anker: ⟦NICHT ab.** Den letzten Tastendruck macht der Betreiber.⟧

Am HEAD: Anker Z. 80.

~~~
⭐ **Gilt seit TB-142 (Abschnitt „Gilt seit TB-144“ oben):** Der Wächter schreibt den Satz nicht mehr in die Eingabezeile und gibt keinen Text mehr an ein Fenster; er öffnet es, und seit TB-144 liest er es und meldet. „Kein Return“ gilt unverändert. Die Sätze weiter unten „er schickt den Satz per AppleScript an Terminal“ und „Text einfügen“ gelten nicht mehr.
~~~

#### E9 — LIESMICH, „So wird es gehandhabt“

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: nach
Anker: ⟦er vom Betreiber.** Das ist keine Notlösung mehr, sondern der Weg.⟧

Am HEAD: Anker Z. 198.

~~~
⭐ **Gilt seit TB-142 (Abschnitt „Gilt seit TB-144“ oben):** Der Wächter legt den Auftrag nicht mehr ins Fenster; in der Tabelle darunter entfällt „Text einfügen“, und seit TB-144 prüft er statt der „Anlaufzeit“, ob die Eingabezeile steht. Abgeschickt wird weiter vom Betreiber.
~~~

#### E10 — LIESMICH, „Was der Wächter NICHT kann“ (20 Sekunden)

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: nach
Anker: ⟦`WAECHTER_WARTESEKUNDEN=30` stellt die Wartezeit um.⟧

Am HEAD: Anker Z. 283.

~~~
⭐ **Gilt seit TB-144 (Abschnitt „Gilt seit TB-144“ oben):** Die feste Wartezeit von 20 Sekunden und `WAECHTER_WARTESEKUNDEN` gibt es nicht mehr. Der Wächter liest den Fensterinhalt in Stufen bis höchstens 60 s und legt (schon seit TB-142) keinen Satz mehr ins Fenster; `letzter_satz.txt` bleibt.
~~~

#### E11 — BACKLOG Abschnitt 5: Abnahme TB-141, Fehler Nr. 23, Regel 21:26, TB-142 bis TB-144

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit⟧

Am HEAD: Anker Z. 351.

~~~
### Aus der Abnahme TB-141 (08.10.2026), der Ursache von Fehler Nr. 23 und der Regel vom 08.10.2026, 21:26 — eingetragen mit TB-144

⟦UEBERGABE: - **TB-141:** |md5 fb9e57ee40d5⟧
⟦UEBERGABE: - **Anmerkungen zur Abnahme:** |md5 874066478224⟧
⟦UEBERGABE: - **Sitzung geschlossen** |md5 14f3d00416f2⟧
⟦UEBERGABE: - **Ursache von Fehler Nr. 23** |md5 859557e871ab⟧
⟦UEBERGABE: - **Neue Regel (Betreiber 08.10.2026, 21:26, |md5 01293cfa1051⟧
- **TB-142 (09.10.2026), Teilstand:** Schritt 0 und A (`4ed91da`, `02a8a53`), Abbruch in Schritt B (`a57d5c2`): Claude Code verwehrte im Auto-Modus zwei `osascript`-Aufrufe an Terminal über Skriptdateien (`docs/belege/TB-142/abbruch.txt` Z. 5–9; UEBERGABE Z. 2457, 2459, 2484).
- **TB-143 (09.10.2026):** Der Wächter startet Sitzungen mit `--permission-mode manual` (Commit `1636764`; UEBERGABE Z. 2476).
- **Mit TB-142 und TB-144 am Sitzungswächter geändert** (Handwerk mit Einzelfreigabe des Betreibers; Wortlaut in den Aufträgen TB-142 und TB-144 unter `docs/auftraege/`): Der Wächter legt keinen Satz mehr in ein Fenster (V4, seit TB-142); seit TB-144: die Fensternummer kommt aus dem Tab, den Terminal beim Öffnen zurückgibt (V1); statt 20 s zu warten, liest er den Fensterinhalt bis höchstens 60 s und meldet „⭐ EINGABEBEREIT“, „⛔ STARTFRAGE“ oder „⛔ KEINE EINGABEZEILE“ (V3); er merkt die Fensternummer, und der Schliess-Auslöser räumt genau dieses Fenster auf, soweit Terminal es ohne Rückfrage zulässt (V5); Probe ohne Auftrag über `probe_<PID>` (V6). Startzeile nach der Probe: `⟦STARTZEILE⟧` (V2). Gemessene Werte M1–M5 und Abweichungen: `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`; Beschreibung: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`, „Gilt seit TB-144“; Regelwerk: `ARBEITSWEISE.md` Abschnitt 0 (zwei Zeilen) und je eine Zeile „Gilt seit TB-142“, „… TB-143“ oder „… TB-144“ in 19, 21, 22.1, 22.4 und 22.9 (in 22.1 eine zweite, wenn die Startzeile geändert ist).
- **Nicht in TB-144:** der übrige Regelwerk-Nachtrag (UEBERGABE, Umzug 08.10.2026, 19:58, Block 4 Nr. 6; dazu Fehler Nr. 24 und die Regeln aus Block 7 des Umzugs 08.10.2026, 22:03, soweit TB-144 sie nicht trägt); das Abschicken des Satzes durch den Wächter; Änderungen an `einschalten.sh` und an der plist.
- Berichte: `logs/steuernder_chat/TB-141_ABNAHME_bericht.md`, `TB-141_ABLAGE_bericht.md`, `TB-142_BESTAND_WAECHTER_bericht.md`, `TB-142_VORGABEN.md` (nicht von git verfolgt).
~~~

#### E12 — ARBEITSWEISE 22.1: Modus-Schalter

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Anker: ⟦Beleg ist deshalb die Prozesszeile, nicht die Anzeige.⟧

Am HEAD: Anker Z. 2038.

~~~
⭐ **Gilt seit TB-143 (Commit `1636764`):** Der Wächter startet `claude --permission-mode manual --effort high --remote-control` (Betreiber, Karte 09.10.2026, 07:57; `docs/ERGEBNIS_TB-143_waechter_modus_schalter.md`).
~~~

#### J1 — JOURNAL: Nachtrag im Block der Sitzung (erste Zeile; es folgen aus E11 die fünf UEBERGABE-Zeilen und zwei weitere)

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

~~~
**Nachtrag des steuernden Chats zum Stand vor TB-144, wie in `BACKLOG.md` Abschnitt 5 eingetragen (wörtlich aus `UEBERGABE.md`, Nachtrag 08.10.2026, 21:47; dazu TB-142 und TB-143):**
~~~

## Anhang C — Werkzeug

### Werkzeug

sha256 des ausgelesenen Texts (mit abschliessendem Zeilenende): `11367fd86ad4d2568b9ad8e3baf2aeb13d1faedd8ae8240c7c09bdd814c2640b`.

```python
#!/usr/bin/env python3
# tb144_werkzeug.py - Werkzeug zum Auftrag TB-144, ausgelesen aus Anhang C.
# Liest Stuecke (W, E, J), Anker und Texte aus dem Auftrag; prueft alles, bevor
# es schreibt; weist einen zweiten Lauf ab; schreibt nur die Zieldateien.
import hashlib, os, re, subprocess, sys

D, P = "docs/werkzeuge/sitzungswaechter/", "docs/projektfuehrung/"
AUF = "docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md"
SH, LIES, UEB, JOU = D + "starte_sitzung.sh", D + "LIESMICH.md", P + "UEBERGABE.md", P + "JOURNAL.md"
MESS = "docs/belege/TB-144/messwerte.txt"
ZIELE = (SH, LIES, P + "ARBEITSWEISE.md", P + "BACKLOG.md", JOU)
START_HEAD = "cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control"
KONST = ("STARTZEILE", "STUFEN", "MERKMAL_EINGABEZEILE", "MERKMAL_FRAGE", "FENSTER_SCHLIESSEN", "LESE_EIGENSCHAFT")
LOGTEILE = ("⭐ EINGABEBEREIT (", "Eingabezeile steht, keine Frage offen (nach ", "⛔ STARTFRAGE (", "⛔ KEINE EINGABEZEILE (",
            "neu geoeffnet (Tab ", "geschlossen (das beim Start gemerkte, kein laufender Prozess).", "bleibt offen: ",
            "⛔ FENSTERLISTE NICHT LESBAR", " Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal).",
            "⛔ MESSWERTE FEHLEN", "⛔ FENSTER NICHT BESTIMMBAR", "⛔ FENSTER NICHT NEU", "⛔ FENSTER FEHLT", "⛔ ABBRUCH",
            "⛔ osascript konnte Terminal nicht ansteuern", "NICHT beendet")
VERBOTEN = ("keystroke", "System Events")
BASH4 = r"declare\s+-\w*A|\bmapfile\b|\breadarray\b|\$\{[^}]*(,,|\^\^)|&>>|\|&|\bcoproc\b|;;&|;&"
ZAUN, KL, KR = "~" * 3, "⟦", "⟧"


def zeilen(p):
    assert os.path.isfile(p), p + " fehlt"
    with open(p, encoding="utf-8") as f:
        t = f.read()
    assert t.endswith("\n"), p + ": kein Zeilenende am Schluss"
    return t[:-1].split("\n")


def stuecke():
    # Kopf '#### <Id> — …', Felder, dann der Text zwischen zwei Tilde-Zaeunen
    z, aus, i = zeilen(AUF), {}, 0
    while i < len(z):
        m = re.match(r"#### ([WEJ]\d+) — ", z[i])
        i += 1
        if not m:
            continue
        s = {"id": m.group(1), "bed": "", "for": "", "art": "", "bis": ""}
        while z[i] != ZAUN:
            for name in ("Zieldatei", "Art", "Form", "Bedingung", "Anker", "Bis"):
                if z[i].startswith(name + ": "):
                    v = z[i][len(name) + 2:]
                    if name in ("Anker", "Bis"):
                        assert v[0] == KL and v[-1] == KR, s["id"] + ": Anker ohne Klammern"
                    s[name[:3].lower()] = v.strip("`") if name == "Zieldatei" else v[1:-1] if name in ("Anker", "Bis") else v
            i += 1
        j = z.index(ZAUN, i + 1)
        s["text"] = z[i + 1:j]
        assert s["text"] and s["zie"] in ZIELE and s["id"] not in aus, s["id"]
        aus[s["id"]] = s
        i = j + 1
    return aus


def treffer(zl, anker, ganz):
    return [k for k, x in enumerate(zl) if (x == anker if ganz else anker in x)]


def wende_an(zl, s, text, ur):
    # .sh: der Anker ist die ganze Zeile; sonst ein Teil der Zeile. Jeder Anker genau einmal.
    # Gemeldet wird die Ankerzeile in der Datei vor dem Lauf (ur).
    ganz = s["zie"].endswith(".sh")
    t, u = treffer(zl, s["ank"], ganz), treffer(ur, s["ank"], ganz)
    assert len(t) == 1 and len(u) == 1, "%s: Anker trifft %d-mal statt 1" % (s["id"], len(t))
    a, art = t[0], s["art"]
    if art.startswith("ersetze"):
        b = treffer(zl, s["bis"], ganz) if art == "ersetze" else [len(zl) - 1]
        assert art in ("ersetze", "ersetze-bis-ende") and len(b) == 1 and b[0] >= a, s["id"] + ": Bis-Anker"
        return zl[:a] + text + zl[b[0] + 1:], "Anker Z. %d · %d Zeilen ersetzt durch %d" % (u[0] + 1, b[0] - a + 1, len(text))
    assert art in ("nach", "vor"), s["id"] + ": Art " + art
    k, ein = (a + 1 if art == "nach" else a), list(text)
    if s["for"] == "Block":  # genau eine Leerzeile davor und danach, keine verdoppelt
        ein = ([""] if k > 0 and zl[k - 1] != "" else []) + ein + ([""] if k < len(zl) and zl[k] != "" else [])
    return zl[:k] + ein + zl[k:], "Anker Z. %d · %s der Zeile · Zeilen +%d" % (u[0] + 1, art, len(ein))


def schreibe(p, zl):
    assert p in ZIELE, p + " ist keine Zieldatei"
    with open(p + ".tb144_neu", "w", encoding="utf-8") as f:
        f.write("\n".join(zl) + "\n")
    os.chmod(p + ".tb144_neu", os.stat(p).st_mode & 0o7777)
    os.replace(p + ".tb144_neu", p)  # ein Schritt: ein laufender Waechter liest seine alte Datei zu Ende


def pruefe_sh(zl, teil):
    # bash -n an einer Kopie im Scratch, dann die Schranken des Auftrags
    t = os.path.join(os.environ.get("TMPDIR", "/tmp"), "tb144_pruef.sh")
    with open(t, "w", encoding="utf-8") as f:
        f.write("\n".join(zl) + "\n")
    r = subprocess.run(["/bin/bash", "-n", t], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    code = [x for x in zl if not x.lstrip().startswith("#")]
    ds = [x for x in code if "do script" in x]
    vb = [w for w in VERBOTEN if any(w in x for x in zl)]
    b4 = [x for x in code if re.search(BASH4, x)]
    f = ["bash -n: " + r.stdout.decode("utf-8", "replace")[:300]] if r.returncode else []
    if len(ds) != 1 or " in window" in ds[0] or " in tab" in ds[0]:
        f.append("'do script' in %d Befehlszeilen (Soll 1, ohne 'in window')" % len(ds))
    f += ["verbotenes Wort: " + w for w in vb] + ["bash-4-Mittel: " + x.strip()[:60] for x in b4]
    if teil == "nachweis":
        f += ["Platzhalter offen: " + x[:50] for x in code if re.match(r'[A-Z_]+="<<', x)]
    f += ["Logzeile fehlt: " + w for w in LOGTEILE if not any(w in x for x in zl)]
    print("starte_sitzung.sh · %d Zeilen · bash -n rc %d · 'do script' in Befehlszeilen %d · verbotene Woerter %d · bash-4 %d"
          % (len(zl), r.returncode, len(ds), len(vb), len(b4)))
    return f


def waechter(teil, probe, setze):
    print("# TB-144 waechter %s%s — Stuecke aus Anhang A auf %s" % (teil, " (Probe)" if probe else "", SH))
    zl = zeilen(SH)
    ur = list(zl)
    ws = [s for s in stuecke().values() if s["id"][0] == "W"]
    schon = [s["id"] for s in ws if s["text"][0] in zl]
    if schon:
        print("ABGEWIESEN, nichts geschrieben: steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    for s in ws:
        zl, was = wende_an(zl, s, s["text"], ur)
        print("%s · %s · ok" % (s["id"], was))
    for paar in setze:
        n, v = paar.split("=", 1)
        t = [k for k, x in enumerate(zl) if x.startswith(n + '="') and x.endswith('"')]
        assert n in KONST and len(t) == 1 and v and not re.search(r'["$`\\\n]|<<', v) and (n != "STARTZEILE" or " --permission-mode manual " in v), "setze " + n
        zl[t[0]] = '%s="%s"' % (n, v)
        print("gesetzt · %s · Z. %d" % (n, t[0] + 1))
    fehler = pruefe_sh(zl, teil)
    for x in fehler:
        print("FEHLER, nichts geschrieben · " + x)
    if not fehler and not probe:
        schreibe(SH, zl)
        print("geschrieben · sha256 " + hashlib.sha256(("\n".join(zl) + "\n").encode("utf-8")).hexdigest())
    return 1 if fehler else 0


def werte():
    # Konstanten aus starte_sitzung.sh; M1–M5 und PROBE aus der Messwertdatei (je eine Zeile 'M1: …')
    w, zl = {}, zeilen(SH)
    for n in KONST:
        t = [x for x in zl if x.startswith(n + '="') and x.endswith('"')]
        assert len(t) == 1, "%s steht %d-mal in %s" % (n, len(t), SH)
        w[n] = t[0][len(n) + 2:-1]
    for x in zeilen(MESS):
        m = re.match(r"(M[1-5]|PROBE): (.+)$", x)
        if m:
            assert m.group(1) not in w, m.group(1) + " doppelt"
            w[m.group(1)] = m.group(2).strip()
    for n in ("M1", "M2", "M3", "M4", "M5", "PROBE"):
        assert n in w, n + " fehlt in " + MESS
    for n, v in w.items():
        assert v and "<<" not in v and KL not in v and "|" not in v and len(v) <= 400, n + ": leer, Platzhalter, '|' oder zu lang"
    return w


def fertig(s, w, nur_ueb=False):
    # Platzhalter fuellen; eine Zeile '⟦UEBERGABE: <Anfang> |md5 <12 Zeichen>⟧' kommt unveraendert aus dem Nachtrag 21:47
    aus = []
    for x in s["text"]:
        if x.startswith(KL + "UEBERGABE: "):
            anfang, soll = x[len(KL) + 11:-1].split(" |md5 ")
            zl = zeilen(UEB)
            a = treffer(zl, "## Nachtrag 08.10.2026, 21:47", False)
            assert len(a) == 1, "Nachtrag 21:47 trifft %d-mal" % len(a)
            e = next(k for k in range(a[0] + 1, len(zl)) if zl[k].startswith("## "))
            t = [y for y in zl[a[0]:e] if y.startswith(anfang)]
            assert len(t) == 1 and hashlib.md5(t[0].encode("utf-8")).hexdigest()[:12] == soll, "UEBERGABE-Zeile '%s': %d Treffer oder md5 anders" % (anfang, len(t))
            aus.append(t[0])
        elif not nur_ueb:
            for n, v in w.items():
                x = x.replace(KL + n + KR, v)
            assert KL not in x, s["id"] + ": Platzhalter offen: " + x[:60]
            aus.append(x)
    return aus


def gewaehlt(w):
    # ein Stueck mit Bedingung nur, wenn die Startzeile vom HEAD abweicht
    return [(s, fertig(s, w)) for s in stuecke().values() if s["id"][0] == "E" and not (s["bed"] and w["STARTZEILE"] == START_HEAD)]


def vorkommen(zl, text):
    return sum(1 for k in range(len(zl) - len(text) + 1) if zl[k:k + len(text)] == text)


def doku(probe):
    print("# TB-144 doku%s — Einfuegungen E aus Anhang B" % (" (Probe)" if probe else ""))
    w = werte()
    print("Startzeile: %s · %s" % (w["STARTZEILE"], "wie HEAD" if w["STARTZEILE"] == START_HEAD else "geaendert"))
    wahl, dat, vor = gewaehlt(w), {}, {}
    for s, text in wahl:
        if s["zie"] not in dat:
            dat[s["zie"]] = zeilen(s["zie"])
            vor[s["zie"]] = list(dat[s["zie"]])
    schon = [s["id"] for s, text in wahl if text[0] in dat[s["zie"]]]
    if schon:
        print("ABGEWIESEN, nichts geschrieben: steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    for s, text in wahl:
        dat[s["zie"]], was = wende_an(dat[s["zie"]], s, text, vor[s["zie"]])
        print("%s · %s · %s · ok" % (s["id"], s["zie"].split("/")[-1], was))
    for s, text in wahl:
        assert vorkommen(dat[s["zie"]], text) == 1, s["id"] + ": Text nachher nicht genau einmal"
    for p in sorted(dat):
        print("Datei %s · Zeilen vorher %d · nachher %d · +%d" % (p, len(vor[p]), len(dat[p]), len(dat[p]) - len(vor[p])))
        if not probe:
            schreibe(p, dat[p])
    print("Gesamt: %d Einfuegungen, %s" % (len(wahl), "nichts geschrieben (Probe)" if probe else "geschrieben, je genau einmal"))
    return 0


def journal(blockpfad, probe):
    print("# TB-144 journal%s — Block der Sitzung samt J1 vor '## Wiederkehrende Lehren'" % (" (Probe)" if probe else ""))
    w, zl, b, st = werte(), zeilen(JOU), zeilen(blockpfad), stuecke()
    j1 = fertig(st["J1"], w) + fertig(st["E11"], w, True) + [x for x in st["E11"]["text"] if x[:11] in ("- **TB-142 ", "- **TB-143 ")]
    k = treffer(zl, "## Wiederkehrende Lehren", True)
    assert len(k) == 1, "Schlussueberschrift trifft %d-mal" % len(k)
    k, was = k[0], "### Was gemessen ist"
    alt = [m.group(1) for m in (re.match(r"## ([A-Z]{2}) — ", x) for x in zl[:k]) if m][-1]
    neu = alt[0] + chr(ord(alt[1]) + 1) if alt[1] != "Z" else chr(ord(alt[0]) + 1) + "A"
    g = b.index(was) if was in b else 0
    bed = (("letzte Kennung %s, Kopfzeile beginnt mit '## %s — TB-144'" % (alt, neu), b[0].startswith("## %s — TB-144" % neu)),
           ("genau eine Zeile '%s', Leerzeile davor" % was, b.count(was) == 1 and g > 0 and b[g - 1] == ""),
           ("genau eine Zeile '### Was offen bleibt'", b.count("### Was offen bleibt") == 1),
           ("kein Trennstrich im Block, Schlusszeile beginnt mit '*Geschrieben'", "---" not in b and b[-1].startswith("*Geschrieben")),
           ("J1 weder im Journal noch im Block", j1[0] not in zl and j1[0] not in b),
           ("vor der Schlussueberschrift stehen '---' und eine Leerzeile", zl[k - 2:k] == ["---", ""]))
    for name, ok in bed:
        print("%s · %s" % (name, "ja" if ok else "NEIN"))
    if not all(ok for name, ok in bed):
        print("ABGEWIESEN, nichts geschrieben")
        return 2
    ein = b[:g] + j1 + [""] + b[g:] + ["", "---", ""]
    print("Kennung %s · Blockzeilen %d · J1-Zeilen %d · Zeilen +%d (= Block + J1 + 1 + 3)" % (neu, len(b), len(j1), len(ein)))
    if not probe:
        schreibe(JOU, zl[:k] + ein + zl[k:])
    return 0


def nachweis():
    print("# TB-144 nachweis — Zustand der Zieldateien gegen den Auftrag")
    zl, w, lies = zeilen(SH), werte(), zeilen(LIES)
    f = pruefe_sh(zl, "nachweis") + ["Logzeile fehlt in LIESMICH: " + t for t in LOGTEILE if not any(t in x for x in lies)]
    for n in KONST:
        print("Konstante %s = %s" % (n, w[n]))
    for s in stuecke().values():
        if s["id"][0] == "W":
            anders = [x for x in s["text"] if x not in zl]
            print("%s · %d von %d Zeilen woertlich in der Datei%s" % (s["id"], len(s["text"]) - len(anders), len(s["text"]), "".join("\n   anders: " + x[:90] for x in anders)))
    for s, text in gewaehlt(w):
        n = vorkommen(zeilen(s["zie"]), text)
        f += [] if n == 1 else [s["id"] + ": Vorkommen %d" % n]
        print("%s · %s · Vorkommen %d · %s" % (s["id"], s["zie"].split("/")[-1], n, "GLEICH" if n == 1 else "ABWEICHUNG"))
    for x in f:
        print("FEHLER · " + x)
    print("Gesamt: " + ("ABWEICHUNG" if f else "wie Soll"))
    return 1 if f else 0


def main(a):
    probe = "--probe" in a
    if a[:1] == ["waechter"] and a[1:2] == ["bau"]:
        return waechter(a[1], probe, [x for x in a[2:] if "=" in x])
    if a[:1] == ["doku"]:
        return doku(probe)
    if a[:1] == ["journal"] and len(a) >= 2:
        return journal(a[1], probe)
    if a[:1] == ["nachweis"]:
        return nachweis()
    print("Aufruf: waechter bau [NAME=WERT …] [--probe] | doku [--probe] | journal <Blockdatei> [--probe] | nachweis")
    return 64


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except AssertionError as fehler:
        print("ABBRUCH, nichts geschrieben · " + str(fehler))
        sys.exit(3)
```
