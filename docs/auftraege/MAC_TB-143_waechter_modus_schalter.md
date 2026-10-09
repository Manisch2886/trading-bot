# TB-143 Wächter: Sitzungen starten im Modus „Manual“ — Schalter `--permission-mode default` in der Startzeile, dazu eine Vorprobe mit `osascript` — an: Mac-Sitzung (Claude Code)

**Stand: 09.10.2026**, gebaut vom steuernden Chat ausserhalb des Repos (kleiner Auftrag: eine Zeile, ein lesender Aufruf), das Skript aus Schritt A an einer Kopie simuliert; gegengelesen von zwei frischen Helfern (GEGEN143, Nachlese GEGEN143b); die Befunde der Nachlese hat der steuernde Chat eingearbeitet, diese letzte Fassung ist nicht noch einmal gegengelesen.

**Sitzungstitel:** `TB-143` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `a57d5c2ee2282a3bb5d6ee4331810fd6aaea6371` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-143`); den Satz fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-143_waechter_modus_schalter.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15).
**Ziel:** Der Sitzungswächter startet Claude-Code-Sitzungen künftig im Modus „Manual“ (Konfigurationswert `default`). Dort gelten die Regeln aus `.claude/settings.local.json` wieder nach dem Grundsatz aus ARBEITSWEISE 6d: alles erlaubt ausser der Sperrliste (die Zahlen dort sind Stand 22.09.2026). Dazu misst diese Sitzung mit genau einem lesenden Aufruf, ob sie selbst `osascript` an Terminal richten darf.
**Bauart wie TB-142** (`docs/auftraege/MAC_TB-142_waechter_reparatur.md`); die Schranken 1, 2 und 5 von dort gelten auch hier; bei Widerspruch gilt dieser Auftrag. **Für jede Rohausgabe gilt:** Sie bleibt roh, samt Fehlertext; die Beschreibung (was, Befehl, Bytes, Zeilen, md5) steht in `<name>.kopf.txt`. In Belege gehen keine Umgebungsvariablen, Schlüssel oder Kontoangaben (TB-142, Schranke 3). **Nie `git add -A`, nie `git add .`;** jeder Commit nennt seine Dateien mit Namen. **Anders als TB-142:** kein Werkzeug aus einem Anhang, kein Journalblock, keine Unterlagen.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**Freigabeklasse: Handwerk mit Einzelfreigabe** — der Wächter wird geändert (wie TB-142, dort Abschnitt „Freigabe des Betreibers, wörtlich“).

**Karte vom 09.10.2026, gestellt 07:57, beantwortet vor 07:58.** Frage, wörtlich: „In welchem Modus sollen die Mac-Sitzungen starten, damit die Wächter-Messungen (osascript an Terminal) laufen?“ Antwort, wörtlich die gewählte Möglichkeit: „Wächter startet in „Manual“ (Empfohlen)“ — mit ihrer Beschreibung auf der Karte: „TB-143 setzt als ersten Schritt den Schalter --permission-mode default in die Startzeile des Wächters, hält an, ich starte neu, dann laufen Messungen und Bau. Preis: Für Wächter-Sitzungen entfällt der zweite Prüfer, Schutz ist wieder allein die Sperrliste (70 Verbote, 14 Fragen). Du fügst den Satz zweimal ein.“
**Vorgaben des steuernden Chats dazu (Handwerk, nicht Teil der Karte):** Der zweite Durchgang (Messungen und Bau, der Rest von TB-142) trägt die Nummer TB-144. Die Vorprobe in Schritt B kommt aus der Lehre in UEBERGABE, Umzug 09.10.2026, 07:23, Block 7 (steht im Arbeitsbaum und wird in Schritt 0 committet): den heikelsten Befehl kurz proben, bevor der grosse Auftrag gebaut wird.

**Die Sitzung darf ändern, und nichts sonst:**

| Datei | was |
|---|---|
| `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` | genau eine Zeile (Z. 327), mit dem Skript aus Schritt A; dabei entsteht daneben kurz `starte_sitzung.sh.tb143.neu` (bleibt sie liegen: nicht löschen — `rm` ist gesperrt —, in keinen Commit nehmen und melden) |
| neu: `docs/belege/TB-143/…`, `docs/ERGEBNIS_TB-143_waechter_modus_schalter.md` | Belege, Ergebnis |
| nicht in git: `$TMPDIR/tb143_0a.txt` | Zwischenablage für 0a |

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt; das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** `.claude/settings.local.json` und jede andere Einstellungsdatei von Claude Code; `LIESMICH.md` des Wächters, `ARBEITSWEISE.md`, `BACKLOG.md`, `JOURNAL.md`; `einschalten.sh`, die plist, `UEBERGABE.md`, `UMZUG.md`, Register, `research/`, `shared/`, `strategies/`. Unterlagen und Journalblock schreibt TB-144 mit dem Werkzeug von TB-142, das die Kennung EK für seinen Block erwartet. Das weicht von der Checkliste in ARBEITSWEISE Abschnitt 0 ab (Gruppe „Wenn ich einen Auftrag schreibe“, Zeile „Mac-Auftrag: Auftrag und Belege werden mitcommittet, der Journalblock geht direkt ins Journal“) und ist Vorgabe des steuernden Chats.

## Belegt · erschlossen · offen

- **Belegt:** TB-142 brach am 09.10.2026 in Schritt B ab, weil Claude Code der Sitzung zwei Aufrufe verwehrte, die über Skriptdateien `osascript` an Terminal richteten (`docs/belege/TB-142/abbruch.txt` Z. 5–9). `docs/belege/TB-142/b_m0.txt` Z. 5–6: `claude` 2.1.295. `.claude/settings.local.json` (gemessen 09.10.2026, 07:30): kein `permissions.defaultMode`, `allow` 83 Einträge mit `Bash(*)`, `ask` 14, `deny` 70. `starte_sitzung.sh` am HEAD: 357 Zeilen, md5 `03649f5cdebe6b478e5353e92a044d13`; Z. 327 ist die einzige Zeile, die `claude` startet, und trägt keinen Modus-Schalter. Dokumentation von Claude Code, Seite „Choose a permission mode“ (https://code.claude.com/docs/en/permission-modes, gelesen 09.10.2026): Terminal-Sitzungen starten ohne andere Vorgabe im Auto-Modus; beim Eintritt in den Auto-Modus fallen breite Erlaubnisregeln weg, ausdrücklich `Bash(*)`, und kommen beim Verlassen zurück; der Schalter `--permission-mode` geht `permissions.defaultMode` und dem eingebauten Standard vor; der Modus „Manual“ hat den Konfigurationswert `default`, die Befehlszeile nimmt auch `manual` an; das Beispiel der Seite lautet `claude --permission-mode default`.
- **Erschlossen:** `claude --help` der Version 2.1.295 nennt `--permission-mode` (A1 misst es). Der Schalter verträgt sich mit `--effort high --remote-control`. Im Modus „Manual“ läuft `osascript` unter der Regel `Bash(*)` ohne Rückfrage. Dass Claude Code auch einen direkten Aufruf `osascript -e …` ablehnt, ist nach `abbruch.txt` naheliegend, nicht belegt.
- **Offen — misst die Sitzung, nie raten:** ob diese Sitzung selbst `osascript` ausführen darf (Schritt B). Ob eine vom geänderten Wächter gestartete Sitzung wirklich startet und im Modus „Manual“ steht, misst erst der nächste Start (TB-144); diese Sitzung startet keine zweite. `bash -n` prüft die neue Zeile nicht, denn sie steht im AppleScript-Rumpf (Z. 326–329); eine AppleScript-Prüfung gibt es in diesem Auftrag nicht. Dafür ist die neue Zeile ein fester Wortlaut, den das Skript gegen die alte prüft (einzige Abweichung: ` --permission-mode <WERT>`, zwei Anführungszeichen).

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-143/` entsteht:** `git status --porcelain > "$TMPDIR/tb143_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `a57d5c2ee2282a3bb5d6ee4331810fd6aaea6371` und genau diese drei Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-143_waechter_modus_schalter.md
```

Commit `TB-143 Schritt 0: Stand des steuernden Chats 09.10.2026` mit genau den drei Pfaden, pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb143_0a.txt` unverändert nach `docs/belege/TB-143/0a_status.txt` (`cmp` gleich; sonst **ABBRUCH**).

**0b. Ausgang** ⇒ `0b_ausgang.txt`: md5 und Zeilen von `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` an ⟨S0⟩. Soll: 357 Zeilen, `03649f5cdebe6b478e5353e92a044d13`; sonst **ABBRUCH**.

## Schritt A — der Schalter, als eigener Commit

**A1.** `claude --version` (nur festhalten, kein Soll) und `claude --help | grep -n -A 3 -- '--permission-mode'` ⇒ `a1_hilfe.txt`. Soll: mindestens eine Zeile aus der Hilfe, die den Schalter nennt. Keine Zeile ⇒ **ABBRUCH**. Daraus folgt der Wert für A2, kurz `WERT`: Nennt die Hilfe `default`, oder zählt sie keine Werte auf ⇒ `default`. Zählt sie Werte auf und nennt `manual`, aber nicht `default` ⇒ `manual` (derselbe Modus; Dokumentation, oben). Zählt sie Werte auf und nennt keinen von beiden ⇒ **ABBRUCH**. In beiden Abbruchfällen ist nichts geändert. Das Ergebnis nennt den gewählten Wert.

**A2.** Genau dieser Aufruf, mit `default` oder `manual` an der Stelle von `WERT`; die Ausgabe samt Fehlertext roh ⇒ `a2_schalter.txt`:

```
trading-env/bin/python3 -B - docs/werkzeuge/sitzungswaechter/starte_sitzung.sh WERT <<'EOF'
import os, shutil, subprocess, sys
P, W = sys.argv[1], sys.argv[2]
assert W in ("default", "manual"), "Wert"
ALT = '    set neu to do script "cd ~/trading-bot && exec claude --effort high --remote-control"\n'
NEU = '    set neu to do script "cd ~/trading-bot && exec claude --permission-mode %s --effort high --remote-control"\n' % W
assert NEU == ALT.replace("exec claude ", "exec claude --permission-mode %s " % W) and NEU.count('"') == 2, "Wortlaut"
z = open(P, encoding="utf-8").read().splitlines(True)
assert len(z) == 357, "Zeilen %d" % len(z)
assert z.count(ALT) == 1 and z.count(NEU) == 0, "alt %d neu %d" % (z.count(ALT), z.count(NEU))
i = z.index(ALT)
assert i + 1 == 327, "Zeile %d" % (i + 1)
z[i] = NEU
tmp = P + ".tb143.neu"
open(tmp, "w", encoding="utf-8").write("".join(z))
shutil.copymode(P, tmp)
rc = subprocess.call(["/bin/bash", "-n", tmp])
if rc != 0:
    os.remove(tmp)
    sys.exit("bash -n rc %d - nichts gespeichert" % rc)
os.replace(tmp, P)
n = open(P, encoding="utf-8").read().splitlines(True)
b = [x for x in n if not x.lstrip().startswith("#")]
print("starte_sitzung.sh | %d Zeilen | Z. 327 ersetzt | alt %d | neu %d | bash -n rc %d" % (len(n), n.count(ALT), n.count(NEU), rc))
print("in Befehlszeilen: 'do script' %d | ' in window' %d | 'keystroke' %d | 'System Events' %d | '--permission-mode' %d" % tuple(sum(w in x for x in b) for w in ("do script", " in window", "keystroke", "System Events", "--permission-mode")))
EOF
```

Soll, wörtlich (Simulation des steuernden Chats an einer Kopie von HEAD; Linux, bash 5.1, Python 3.10):

```
starte_sitzung.sh | 357 Zeilen | Z. 327 ersetzt | alt 0 | neu 1 | bash -n rc 0
in Befehlszeilen: 'do script' 1 | ' in window' 0 | 'keystroke' 0 | 'System Events' 0 | '--permission-mode' 1
```

Endet das Skript mit einem `AssertionError` oder mit `bash -n rc …`, ist nichts gespeichert ⇒ **ABBRUCH**. Endet es anders als mit genau diesen zwei Zeilen ⇒ **ABBRUCH**; dann zuerst messen, welche Zeile 327 die Datei trägt. ⚠️ launchd ruft `starte_sitzung.sh` aus dem Arbeitsbaum auf: Die gespeicherte Zeile ist sofort scharf.

**A3.** Commit `TB-143 A: Waechter startet Sitzungen im Modus Manual (--permission-mode <WERT>)` mit genau einem Pfad (`docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`), pushen ⇒ **⟨A⟩**. `git show --numstat --format=%h HEAD` ⇒ `a3_numstat.txt`; Soll: genau eine Zahlenzeile, mit `1`, `1` und dem Pfad des Skripts; sonst **ABBRUCH**.

## Schritt B — Vorprobe: genau ein lesender Aufruf

**B0.** Schreib in `b_vorprobe.kopf.txt`, in welchem Berechtigungsmodus diese Sitzung nach deiner eigenen Kenntnis läuft (Auto, Manual, …) — als Aussage gekennzeichnet, nicht als Messung; weisst du es nicht, steht dort „nicht bekannt“. Kein Befehl dafür.

**B1.**

```
osascript -e 'tell application "Terminal" to get id of every window'
```

**Genau einmal,** mit einer Zeitgrenze von 30 Sekunden am Bash-Werkzeug. Keine Variante, kein zweiter Versuch, kein Umweg über eine Skriptdatei oder einen anderen Interpreter. *Schützt:* vor dem Umgehen einer Ablehnung und vor der Pause, die Claude Code nach wiederholten Ablehnungen einlegt. Der Aufruf liest nur Fensternummern; er öffnet nichts und schreibt nichts in ein Fenster.

Jeder der vier Ausgänge ist ein gültiges Ergebnis, **keiner ist ein Abbruch** ⇒ `b_vorprobe.txt`:

- **LÄUFT:** Die Ausgabe (Fensternummern) steht roh im Beleg.
- **ABGELEHNT:** Claude Code führt den Aufruf nicht aus. Dann steht der Wortlaut der Ablehnung im Beleg, als Text gekennzeichnet.
- **FEHLER:** Der Aufruf läuft, endet aber mit einem Fehler oder überschreitet die Zeitgrenze (etwa weil macOS eine Berechtigung verlangt). Fehlertext oder „Zeitgrenze“ in den Beleg.
- **NACH BESTÄTIGUNG:** Claude Code fragt den Betreiber, und er stimmt zu. Seine Antwort steht wörtlich im Ergebnis, die Ausgabe im Beleg. Lehnt er ab, heisst der Ausgang ABGELEHNT, mit dem Zusatz „durch den Betreiber“.

## Schritt C — Ergebnis, Abgabe

`docs/ERGEBNIS_TB-143_waechter_modus_schalter.md` mit: Kopf · „Kurz“ (Tabelle Soll | Ist für 0a, 0b, A1, A2, A3, B) · „Abweichungen vom Auftrag“ · „Nicht getan“ · „In einfacher Sprache“. Commit `TB-143 Abgabe: Belege und Ergebnis` mit den Dateien unter `docs/belege/TB-143/` und dem Ergebnis, je mit Namen, pushen. Danach `git status --porcelain` (Soll: leer) und `git rev-parse HEAD origin/main` (Soll: gleich) in die Schlussmeldung, nicht mehr committen.

**Schlussmeldung, eine Zeile:** `TB-143 fertig: Schalter gesetzt mit <Hash von ⟨A⟩>, Vorprobe <LÄUFT | ABGELEHNT | FEHLER | NACH BESTÄTIGUNG>`. Danach nichts mehr tun: Der steuernde Chat schliesst diese Sitzung und lässt den Wächter für TB-144 eine neue starten.

## Abbruchkriterien — melden, nicht reparieren

- 0a oder 0b weicht ab, oder `cmp` in 0a ist ungleich.
- A1: keine Zeile aus der Hilfe, oder die Hilfe zählt Werte auf und nennt weder `default` noch `manual`.
- A2: `AssertionError`, `bash -n rc …` oder eine andere Ausgabe als die zwei Soll-Zeilen.
- A3: `numstat` weicht ab.
- Claude Code lehnt einen anderen Befehl ab als den aus Schritt B — melden, nicht umgehen.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Verfahren bei Abbruch:** `docs/belege/TB-143/abbruch.txt` schreiben (Schritt, Grund im Wortlaut, Stand von `starte_sitzung.sh`); die Belege mit Namen committen (`TB-143 Abbruch in Schritt <x>: <Grund>`) und pushen, soweit das geht; dann melden, in einer Zeile: `TB-143 ABBRUCH in Schritt <x>: <Grund>`. Gibt es den Belegordner noch nicht (Abbruch in 0a wegen der Einträge oder des HEAD), genügt die Meldung. **Nichts zurückdrehen.** Ab Schritt A trägt Zeile 327 nach jedem Abbruch entweder den alten oder den neuen Wortlaut, sonst ist am Skript nichts geändert. Ist die neue Zeile gespeichert, aber nicht committet oder nicht gepusht (Abbruch zwischen A2 und A3), steht das **als Erstes** in der Meldung — sie ist dann scharf, ohne im Repo zu stehen.

## Nicht in TB-143

Messungen M1–M5, die Stücke W2–W6, die Probe über launchd, Unterlagen und Journalblock (alles TB-144, aus den Bausteinen von TB-142); `--no-chrome`; jede Einstellungsdatei von Claude Code.

## In einfacher Sprache

Claude Code startet neue Sitzungen seit einiger Zeit von sich aus in einem Modus, in dem ein zweiter Prüfer über jeden Befehl entscheidet. Dieser Prüfer hat die Wächter-Reparatur heute früh gestoppt. Dieser kleine Auftrag schreibt in die eine Zeile, mit der der Wächter Claude Code startet, einen Schalter: Künftige Sitzungen starten im Modus „Manual“, in dem wieder unsere eigene Liste gilt — alles erlaubt ausser der Sperrliste. Danach probiert die Sitzung einen einzigen harmlosen Befehl aus, der nur Fensternummern liest, und schreibt auf, ob sie ihn ausführen durfte. Die eigentliche Reparatur folgt in einer neuen Sitzung (TB-144).
