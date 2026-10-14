# TB-158 Probe des Wächters: EIGEN mit `pgrep -a`, cwd und Elternkette, dann mindestens zwei Probeläufe — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 14.10.2026, 06:53** (Helfer BAU158, per Skript aus Bausteinen, `$HOME/sc/tb158/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an einer Kopie simuliert. Urteil und Freigabe liegen beim steuernden Chat; zwei frische Gegenleser sind Pflicht. **Gebaut am HEAD `882b487`.**

**Sitzungstitel:** `TB-158` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `882b487c8c93513580cb2ad8aad1b96ecd704a23` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-158`), nicht von Hand; der Satz geht erst nach der Karte „Senden?“ (UEBERGABE, Umzug 13.10.2026, 18:51, Block 4 Nr. 1).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-158_waechter_probe.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), kurz `PY`. **Werkzeuge:** `docs/belege/TB-156/tb156_werkzeug.py` (am HEAD, aus TB-156; nur `warte` und `beleg`), kurz `WZ6`; `docs/belege/TB-158/tb158_werkzeug.py` (Anhang A; nur `backlog` und `journal`), kurz `WZ`. **Belege:** `docs/belege/TB-158/`. **Ergebnis:** `docs/ERGEBNIS_TB-158_waechter_probe.md`. **Journal:** Kennung EV erwartet (nennt `WZ journal` eine andere, gilt die von `WZ journal`; Schritt D).
**Ziel:** Die Probe des Wächters, offen seit TB-155: zuerst EIGEN (die PID dieser Sitzung) so messen, dass die Sitzung sich selbst sieht; dann mindestens zwei Probeläufe über den echten Weg wie TB-156 Schritt B; dazu eine Zeile im Backlog hinter „`pgrep` ohne `-a`“ (`BACKLOG.md` Z. 483).
**Bauart:** Messauftrag; Vorbild `docs/auftraege/MAC_TB-156_waechter_fensterinhalt_fortsetzung.md`, nur Schritt B (dort Z. 94–110) mit Schritt 0, D, Abbruchkriterien und Anhang; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen. **Kein Bau am Wächter:** nichts unter `docs/werkzeuge/` wird geändert. **Keine Kopfdateien** (`WZ6 kopf` kennt nur `docs/belege/TB-156/`, `tb156_werkzeug.py` Z. 342 und 491–494); an ihre Stelle tritt die Tabelle „Belege“ im Ergebnis, wie in TB-157.
**Reihenfolge:** Schritt 0 → A (EIGEN) → B (Probe) → C (Journal-Probe, dann Backlog) → D (Ergebnis, Journal, Abgabe). **Jede Datei, die die Sitzung schreibt, entsteht mit dem Befehl aus dem Anhang „Dateien und ihre Befehle“** — kein anderer Weg.

## Lage nach dem Auslegen

Am Bau-HEAD `882b487` gemessen: geändert nichts; unverfolgt: nichts. Das Auslegen durch den steuernden Chat ändert dazu nur den Zeiger in `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab (unverfolgt; keinen Nachtrag in `UEBERGABE.md`, Betreiber 13.10.2026, 22:53: „Große Sammeldateien nicht nach jedem Schritt nachziehen, sondern einmal gebündelt beim Umzug.“). **Beim Start liegen daher genau zwei Einträge vor: eine geänderte Datei und dieser Auftrag** (Soll in 0a). `logs/` ist nicht in git (`.gitignore` Z. 27); `probe_*` und `_erledigt/` sind es auch nicht (`docs/auftraege/_ausloeser/.gitignore`).

## Die Sitzung darf ändern, und nichts sonst

- neu: `docs/belege/TB-158/…` und `docs/ERGEBNIS_TB-158_waechter_probe.md`;
- `docs/projektfuehrung/BACKLOG.md` — eine Zeile hinter Z. 483, nur über `PY WZ backlog`;
- `docs/projektfuehrung/JOURNAL.md` — der Block der Sitzung, nur über `PY WZ journal`;
- nicht in git: `docs/auftraege/_ausloeser/probe_<EIGEN>` (Probe-Auslöser anlegen).

**Nicht erlaubt:** alles unter `docs/werkzeuge/` (Wächter, Test, LIESMICH, plist, einschalten.sh), `ARBEITSWEISE.md`, `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` (auch in Schritt 0), Register; bestehende Zeilen in `BACKLOG.md` und `JOURNAL.md` ändern oder entfernen.

## Schranken — je mit dem, wovor sie schützen

1. **Kein Enter, kein `keystroke`, kein System Events, kein Text in ein Fenster** — weder im Wächter noch in dieser Sitzung. *Schützt:* Betreiberentscheidung 23.09.2026 (ARBEITSWEISE 19).
2. **Diese Sitzung ruft weder `osascript` noch `launchctl` auf, meldet sich nicht ab und ruft kein `/login` auf;** das Fenster liest nur der Wächter, über die Probe. *Schützt:* die Anmeldung des Betreibers.
3. **Kontodaten:** Rohausgaben zuerst nach `$TMPDIR`, dann nur über `WZ6 beleg` nach `docs/belege/TB-158/` (es ersetzt Kontozeilen, `/Users/<name>` in jeder Zeile durch `~` und die Zeile der Ablaufwarnung). Vor jedem Beleg sieht die Sitzung in der Rohausgabe nach Konto, Personenname, Mailadresse, Organisation und Schlüssel (Schritt A, Schritt B Nr. 3); ein Name nur im Pfad `/Users/<name>` ist kein Fund (ihn ersetzt `WZ6 beleg`). *Schützt:* Kontodaten (Belege werden gepusht).
4. **Kommandozeilen werden nie gelesen:** nur `pgrep` (die Ausgabe ist eine PID-Liste), je PID das cwd über `lsof -a -p <pid> -d cwd -Fn` und die Elternkette über `ps -o ppid=,comm= -p <pid>`; für EIGEN und jede `claude`-PID mit cwd im Repo dazu `LC_ALL=C ps -o lstart= -p <pid>` (englische Ausgabe; am Mac sonst deutsch, `docs/belege/TB-145/w_fenster.txt` Z. 11–12: `Di 15 Sep 09:14:08 2026`; Vergleich der Startzeiten, Schritt A und B). Keine anderen Schalter an `pgrep` und `ps` als die hier genannten. *Schützt:* Rüge ABN156 A2 (`ps -o command` liest Kommandozeilen).
5. **Der Wächter bleibt unverändert;** die Sitzung liest ihn nicht einmal für die Probe, sie liest nur sein Log. *Schützt:* launchd führt `starte_sitzung.sh` aus dem Arbeitsbaum aus.
6. **Nie `git add -A`, nie `git add .`;** jeder Commit nennt seine Dateien mit Namen. *Schützt:* vor Auslöser oder Log im Commit.
7. **Jede Datei nur mit ihrem Befehl.** Keine eigenen Hilfsskripte, keine eigenen Dateien im Scratchpad oder in `$TMPDIR` ausser den genannten, kein Ändern von Dateirechten. **Ein schreibender Befehl, den der Auftrag nicht nennt, ist ein Abbruchgrund vor der Ausführung: melden, nicht ausführen.** Frei sind nur lesende Befehle: `ls`, `cat`, `head`, `tail`, `wc`, `md5`, `shasum`, `cmp`, `date`, git `log`, `show`, `rev-parse`, `status`, `diff`. *Schützt:* TB-146 und TB-155 brachen an einem Hilfsskript ab (`docs/belege/TB-155/abbruch.txt`).

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-158/` entsteht:** `git status --porcelain > "$TMPDIR/tb158_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `882b487c8c93513580cb2ad8aad1b96ecd704a23` und genau diese 2 Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-158_waechter_probe.md
```

Dann das Werkzeug aus Anhang A holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-158_waechter_probe.md "$TMPDIR/tb158_werkzeug.py" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2], "w", encoding="utf-8").write(t)
print("tb158_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb158_werkzeug.py f0a3c21b1709be864cfee0aa67b9f092def3d27e0aae707309a06940078dc896`; sonst **ABBRUCH** (vor ⟨S0⟩: nur melden, siehe Abbruchweg). Commit `TB-158 Schritt 0: Stand des steuernden Chats vor TB-158` mit genau den zwei Pfaden aus 0a (Block unten), pushen ⇒ **⟨S0⟩** (der Push wird nicht wiederholt; scheitert er: ABBRUCH, Abbruchweg vor ⟨S0⟩). **Unmittelbar nach dem gepushten ⟨S0⟩:** `mkdir -p docs/belege/TB-158`; erst ab hier gibt es `abbruch.txt` (Abbruchweg). Dann `cp "$TMPDIR/tb158_0a.txt" docs/belege/TB-158/0a_status.txt` (`cmp` gleich), `cp "$TMPDIR/tb158_werkzeug.py" docs/belege/TB-158/tb158_werkzeug.py`, dann `shasum -a 256 docs/belege/TB-158/tb158_werkzeug.py` (Soll wie oben).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/auftraege/MAC_TB-158_waechter_probe.md
```

**0b. Ausgang** ⇒ `0b_ausgang.txt`, Befehl:

```
{ wc -l docs/werkzeuge/sitzungswaechter/starte_sitzung.sh docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; md5 docs/werkzeuge/sitzungswaechter/starte_sitzung.sh docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; shasum -a 256 docs/belege/TB-156/tb156_werkzeug.py; } > docs/belege/TB-158/0b_ausgang.txt
```

Soll (am Bau-HEAD `882b487`): `starte_sitzung.sh` 723 Z., `8ea9eaaa2b6a1be8ca5587b21a7fcd7f` · `BACKLOG.md` 497 Z., `c803f0d6d58a9a7f19fcf762b81f0cc4` · `JOURNAL.md` 10977 Z., `f305e8ee4d8cdfa695c989eabb238b76` · `tb156_werkzeug.py` sha256 `86521eba71f56f81d735f3281ad07cbd6c65a528c8568d49d6dbdc25a93dc0ea` (= Soll TB-156). **Weicht `starte_sitzung.sh` oder der sha256 von `WZ6` ab: ABBRUCH** (dann probte die Sitzung einen anderen Wächter oder ein anderes Werkzeug). Weicht `BACKLOG.md` oder `JOURNAL.md` ab: vermerken; die Anker entscheiden (Schritt C, D). Commit `TB-158 0: Ausgang und Werkzeug`, pushen ⇒ **⟨0⟩**.

```
git add docs/belege/TB-158/0a_status.txt
git add docs/belege/TB-158/tb158_werkzeug.py
git add docs/belege/TB-158/0b_ausgang.txt
```

## Schritt A — EIGEN, zuerst gemessen

Gemessen wird, bevor geprobt wird: (a) `pgrep -x claude` und (b) `pgrep -a -x claude`, je PID nur das cwd (`lsof -a -p <pid> -d cwd -Fn`), nie die Kommandozeile; (c) die Elternkette ab `$$` mit `ps -o ppid=,comm= -p <pid>` bis PID 1. **EIGEN** ist die eine PID aus (b) mit cwd im Repo, die auch in (c) liegt. Weitere `claude`-PIDs mit cwd im Repo zählen nicht gegen die Eindeutigkeit; Der Befehl liest dafür die Startzeit von EIGEN und jeder weiteren PID aus (b) mit cwd im Repo (`LC_ALL=C ps -o lstart= -p <pid>`, je eine Zeile in `a_eigen.txt`) und vergleicht sie mit `datetime.strptime(…, "%a %b %d %H:%M:%S %Y")`; die gleiche Sekunde zählt als nicht später, eine nicht lesbare Startzeit auch. Ist die Startzeit von EIGEN selbst nicht lesbar, steht als letzte Zeile `Probe: nein (Startzeit nicht lesbar)` ⇒ kein Auslöser, keine Probe, Befund. Ist eine solche Sitzung nicht später als EIGEN gestartet, steht als letzte Zeile `Probe: nein, frühere Sitzung im Repo: <PIDs>` ⇒ **kein Auslöser**, keine Probe; eine früher gestartete wird nie beendet (ebenso eine in derselben Sekunde gestartete). Eine später gestartete wird nur nach Schritt B beendet („Probe nicht gelaufen“ und „Bleibt eine Probe-Sitzung stehen“); Nr. 5 vergleicht nur. Genau dieser Befehl (er schreibt nur `$TMPDIR/tb158_a_eigen.txt`, roh, und zeigt die Auswertung ab `(a) pgrep -x claude:`):

```
trading-env/bin/python3 -B - "$$" "$TMPDIR/tb158_a_eigen.txt" <<'EOF'
import os, subprocess, sys
from datetime import datetime
repo, aus = os.getcwd(), []
def lauf(*b, env=None):
    r = subprocess.run(list(b), capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr
def pids(*b):
    rc, o, e = lauf(*b)
    z = [s.strip() for s in o.split("\n") if s.strip()]
    rein = all(s.isdigit() for s in z)
    aus.append("$ " + " ".join(b) + " · rc %d · %d Zeilen" % (rc, len(z)))
    aus.extend(z if rein else ["(keine reine PID-Liste: Ausgabe nicht abgelegt)"])
    if e.strip():
        aus.append("Fehlerausgabe: " + e.strip()[:200])
    return z if rein else None
a = pids("pgrep", "-x", "claude")
b = pids("pgrep", "-a", "-x", "claude")
im = []
for p in sorted(set((a or []) + (b or [])), key=int):
    rc, o, e = lauf("lsof", "-a", "-p", p, "-d", "cwd", "-Fn")
    n = [s[1:] for s in o.split("\n") if s.startswith("n")]
    aus.append("$ lsof -a -p %s -d cwd -Fn · rc %d" % (p, rc))
    aus.extend(o.rstrip("\n").split("\n") if o.strip() else [])
    if n and (n[0] == repo or n[0].startswith(repo + "/")) and p in (b or []):
        im.append(p)
kette, p = [], sys.argv[1]
for _ in range(40):
    rc, o, e = lauf("ps", "-o", "ppid=,comm=", "-p", p)
    aus.append("$ ps -o ppid=,comm= -p %s · rc %d" % (p, rc))
    aus.append(o.rstrip("\n"))
    kette.append(p)
    t = o.split()
    if rc or not t or not t[0].isdigit() or t[0] in ("0", "1"):
        break
    p = t[0]
ei = [p for p in im if p in kette]
gut = a is not None and b is not None and len(ei) == 1
def start(p):
    rc, o, e = lauf("ps", "-o", "lstart=", "-p", p, env=dict(os.environ, LC_ALL="C"))
    aus.append("$ LC_ALL=C ps -o lstart= -p %s · rc %d · %s" % (p, rc, o.strip()))
    try:
        return datetime.strptime(" ".join(o.split()), "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None
frueher, t0 = [], None
if gut:
    t0 = start(ei[0])
    for p in im:
        if p != ei[0]:
            t = start(p)
            if t0 is None or t is None or t <= t0:
                frueher.append(p)
nur_b = sorted(set(b or []) - set(a or []), key=int)
nur_a = sorted(set(a or []) - set(b or []), key=int)
k0 = len(aus)
aus.append("(a) pgrep -x claude: " + (" ".join(a) if a else ("keine" if a is not None else "keine reine PID-Liste")))
aus.append("(b) pgrep -a -x claude: " + (" ".join(b) if b else ("keine" if b is not None else "keine reine PID-Liste")))
aus.append("(a) gegen (b): nur in (b) %s · nur in (a) %s" % (" ".join(nur_b) or "keine", " ".join(nur_a) or "keine"))
aus.append("(b) mit cwd im Repo: " + (" ".join(im) or "keine"))
aus.append("(c) Elternkette ab $$: " + " ".join(kette))
aus.append("(b) mit cwd im Repo, nicht in (c): " + (" ".join(p for p in im if p not in kette) or "keine"))
aus.append("EIGEN: %s" % ei[0] if gut else "EIGEN: nicht eindeutig ((b) mit cwd im Repo: %d, davon in (c): %d). Keine Probe." % (len(im), len(ei)))
aus.append("Probe: nein, EIGEN nicht eindeutig" if not gut else "Probe: nein (Startzeit nicht lesbar)" if t0 is None else ("Probe: nein, frühere Sitzung im Repo: " + " ".join(frueher)) if frueher else "Probe: ja")
with open(sys.argv[2], "x", encoding="utf-8") as f:
    f.write("\n".join(aus) + "\n")
print("\n".join(aus[k0:]))
EOF
```

Soll: rc 0, eine Zeile `EIGEN: <PID>` und als letzte Zeile `Probe: ja`. **Handbuchstelle** (Nachtrag 13.10.2026, 15:57, aus pgrep(1) gelesen, nicht gemessen): ohne `-a` schliesst `pgrep` den eigenen Prozess und alle Vorfahren aus; erwartet ist daher EIGEN in (b), nicht in (a). Die Zeile `(a) gegen (b)` ist der Messbeleg dazu; widerspricht sie der Erwartung: Befund, kein Abbruch. **Steht `EIGEN: nicht eindeutig …` (der Schnitt von (b) mit cwd im Repo und (c) hat nicht genau eine PID): keine Probe** — Befund; in Schritt B nur die Zeile `PROBE: nicht gelaufen, <die Zeile EIGEN>` nach `b_probe.txt` (Schreibwerkzeug von Claude Code), dann der Commit `TB-158 B: Probe` mit nur `b_probe.txt`, pushen, weiter mit Schritt C. **Steht `Probe: nein, frühere Sitzung im Repo: …`: kein Auslöser, keine Probe** — Befund; in Schritt B nur die Zeile `PROBE: nicht gelaufen (frühere Sitzung im Repo)` nach `b_probe.txt` (Schreibwerkzeug von Claude Code), dann der Commit `TB-158 B: Probe` mit nur `b_probe.txt`, pushen, weiter mit Schritt C. Ebenso bei `Probe: nein (Startzeit nicht lesbar)`, mit der Zeile `PROBE: nicht gelaufen (Startzeit nicht lesbar)`. **Vor dem Beleg nachsehen** (Schranke 3): Fund ⇒ kein Beleg, nichts zitieren, Abbruchweg. Sonst `PY WZ6 beleg "$TMPDIR/tb158_a_eigen.txt" docs/belege/TB-158/a_eigen.txt`. Commit `TB-158 A: EIGEN gemessen`, pushen ⇒ **⟨A⟩**.

```
git add docs/belege/TB-158/a_eigen.txt
```

## Schritt B — Probe über den echten Weg

Auslöserdatei → launchd → Skript (wie TB-144, Schritt D): Die Probe ruft dieselbe `warte_auf_eingabezeile` wie ein echter Start.

**Mindestens zwei Läufe** (Abstand mindestens 35 s: `ThrottleInterval` 30, plist Z. 36–37): Zwischen zwei Läufen wartet die Sitzung genau mit `trading-env/bin/python3 -B -c 'import time; time.sleep(35); print("35 s gewartet")'`.
1. `wc -l < logs/sitzungswaechter/waechter.log` (Z0), dann `: > docs/auftraege/_ausloeser/probe_<EIGEN>`.
2. `PY WZ6 warte <Z0> "$TMPDIR/tb158_b_probe<i>.txt"` — sieht alle 10 s nach (höchstens 100 s), ob das Log **hinter Zeile Z0** `----- fertig (probe), rc <r> -----`, `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN: Der Probe-Ausloeser …` oder `⛔ Konnte Probe-Ausloeser nicht wegraeumen` trägt (eine fremde `⛔ ABGEWIESEN` beendet das Warten nicht), und schreibt dann die Log-Zeilen ab Z0+1 roh in die Datei. rc 3: **einmal** wiederholen. Kommt dann keine: melden, nicht wiederholen; liegt `probe_<EIGEN>` noch in `_ausloeser/`, mit `mv docs/auftraege/_ausloeser/probe_<EIGEN> docs/auftraege/_ausloeser/_erledigt/` legen (nicht löschen).
3. **Dort nachsehen, vor jedem Beleg:** Steht in einer Zeile `   | …` ein Konto, ein Personenname (auch als Teil eines Rechner- oder Ordnernamens; `~/trading-bot` und die Ordner des Repos sind kein Fund), eine Mailadresse, eine Organisation oder ein Schlüssel unersetzt? **Fund ⇒ kein Beleg von diesem Lauf, nichts committen, was die Zeile trägt, nichts zitieren; Abbruchweg (Abbruchkriterien).** Sonst `PY WZ6 beleg "$TMPDIR/tb158_b_probe<i>.txt" docs/belege/TB-158/b_probe<i>_log.txt`; `WZ6 beleg` nennt die Zahl zerschnittener Zeichen (> 0: Befund).
4. **Danach im Repo nur EIGEN** — nur nach einem Lauf, der als Lauf zählt (Soll je Lauf, unten); nach rc 3 und nach „Probe nicht gelaufen“ kein `b_nach<i>`. Geprüft mit `{ pgrep -a -x claude; for p in $(pgrep -a -x claude); do lsof -a -p "$p" -d cwd -Fn; done; } > "$TMPDIR/tb158_b_nach<i>.txt" 2>&1`; dann, nach dem Nachsehen wie in Nr. 3, `PY WZ6 beleg "$TMPDIR/tb158_b_nach<i>.txt" docs/belege/TB-158/b_nach<i>.txt`. Soll: genau eine PID mit cwd im Repo, und das ist EIGEN; sonst Befund, kein Abbruch.
5. **Startvergleich** — für jede weitere `claude`-PID im Repo, bevor sie beendet wird: genau dieser Befehl (je PID ein Aufruf, Ausgabe angehängt an `$TMPDIR/tb158_b_start<i>.txt`), dann nach dem Nachsehen wie in Nr. 3 `PY WZ6 beleg "$TMPDIR/tb158_b_start<i>.txt" docs/belege/TB-158/b_start<i>.txt`; beendet wird nur bei `PID <pid> später als EIGEN <EIGEN>: ja` (gleiche Sekunde zählt als nicht später, eine nicht lesbare Startzeit auch):

```
trading-env/bin/python3 -B - <EIGEN> <pid> >> "$TMPDIR/tb158_b_start<i>.txt" 2>&1 <<'EOF'
import os, subprocess, sys
from datetime import datetime
def start(p):
    r = subprocess.run(["ps", "-o", "lstart=", "-p", p], capture_output=True, text=True, env=dict(os.environ, LC_ALL="C"))
    print("$ LC_ALL=C ps -o lstart= -p %s · rc %d · %s" % (p, r.returncode, r.stdout.strip()))
    try:
        return datetime.strptime(" ".join(r.stdout.split()), "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None
e, p = start(sys.argv[1]), start(sys.argv[2])
spaeter = e is not None and p is not None and e < p
print("PID %s später als EIGEN %s: %s" % (sys.argv[2], sys.argv[1], "ja" if spaeter else "nein"))
EOF
```

**Soll je Lauf:** `Fenster <n> neu geoeffnet`; `⭐ EINGABEBEREIT (PROBE)`; darunter `   Anmeldung: Abo`, `   Ablaufwarnung: nein` oder `   Ablaufwarnung: ja | …`, `   Letzte Zeilen von Fenster <n> (hoechstens 12, je 160 Zeichen, Kontozeilen ersetzt):`, höchstens 12 Zeilen `   | …`, davon mindestens eine `   | <<entfernt: Kontozeile>>` und keine mit `@`; `Probe: beende PID <p> …`; `Fenster <n> geschlossen`; `----- fertig (probe), rc 0 -----`; danach im Repo nur EIGEN. Bei leerem oder nicht lesbarem Fensterinhalt steht unter „⛔ KEINE EINGABEZEILE“ nur `   Fensterinhalt leer oder nicht lesbar: …` (Befund). Die Probe versucht bei jeder Rückgabe der Prüfung, ihr Fenster zu schliessen; ob es geschlossen ist oder offen bleibt, steht im Log (`Fenster <n> geschlossen` oder `bleibt offen: <Grund>`).

**Befund, kein Abbruch — ins Ergebnis, nichts richten:** `Anmeldung: unklar` (dazu, ohne zu zitieren: ob eine Zeile `   | …` das Wort `Claude` trägt); keine ersetzte Zeile; die Adresse `https://claude.ai/code/session_` fehlt; zerschnittene Zeichen am Zeilenende; `⛔ NICHT ANGEMELDET (PROBE)`, rc 6 (**kein `/login`**; im Ergebnis als Erstes sagen, dass der Betreiber sich anmelden muss); `⛔ API-ABRECHNUNG (PROBE)`, rc 7 (im Ergebnis als Erstes sagen; nichts umstellen); `⛔ STARTFRAGE`; `⛔ KEINE EINGABEZEILE`. **Probe nicht gelaufen — kein Abbruch, zählt nicht als Lauf** (wie TB-144, dort Z. 157): nach `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN` oder `----- fertig (probe), rc 1 -----` im Log den Grund aus der Zeile lesen; steht eine andere `claude`-Sitzung ohne Auftrag im Repo: ist sie nach EIGEN gestartet (Startvergleich, Nr. 5), sie beenden wie eine stehen gebliebene Probe-Sitzung (nächster Satz) und **einmal** neu proben, mit dem nächsten `<i>` (`<i>+1`); ist sie nicht nach EIGEN gestartet (gleiche Sekunde zählt als nicht später; der Fall fällt meist schon in Schritt A auf, dann gibt es keinen Auslöser), wird sie nie beendet: melden, `PROBE: nicht gelaufen, <Grund>` nach `b_probe.txt`, keine weitere Probe, Befund; sonst, und nach `⛔ Konnte Probe-Ausloeser nicht wegraeumen`: melden, `PROBE: nicht gelaufen, <Grund>` nach `b_probe.txt`. Bleibt eine Probe-Sitzung stehen (`NICHT beendet`, rc 5): ihre PID bestimmen wie EIGEN in Schritt A (`pgrep -a -x claude`, je PID `lsof -a -p <pid> -d cwd -Fn`; cwd im Repo, ≠ EIGEN, nach EIGEN gestartet: Startvergleich, Nr. 5; sonst nicht beenden, melden), dann `kill -TERM <pid>`; ihr Fenster bleibt offen und steht im Ergebnis.

Je Lauf eine Zeile nach `docs/belege/TB-158/b_probe.txt`: `PROBE:` Fensternummer, Sekunden, Anmeldung, Ablaufwarnung ja oder nein, Zeilen `   | …`, davon ersetzt, Adresse ja oder nein, rc. **Jede Zeile von `b_probe.txt`** schreibt die Sitzung mit dem Schreibwerkzeug von Claude Code (die erste Zeile) und dem Edit-Werkzeug (jede weitere), in genau einer dieser Formen: `PROBE: <Werte wie oben>` (ein Lauf) · `PROBE: nicht gelaufen, <Grund>` (Probe nicht gelaufen) · `PROBE: nicht gelaufen (rc 3)` (`warte` endet nach der einen Wiederholung wieder mit rc 3; zählt nicht als Lauf; kein weiterer Lauf) · `PROBE: nicht gelaufen, <die Zeile EIGEN>` (Schritt A) · `PROBE: nicht gelaufen (frühere Sitzung im Repo)` (Schritt A) · `PROBE: nicht gelaufen (Startzeit nicht lesbar)` (Schritt A). Dann Commit `TB-158 B: Probe` — **in jedem Zweig**, auch ohne Lauf (je vorhandenen `b_probe<i>_log.txt`, `b_nach<i>.txt` und `b_start<i>.txt` eine Zeile `git add` mit dem Namen), pushen ⇒ **⟨B⟩**. **„Mindestens zwei Läufe“ ist das Ziel; wird es nicht erreicht (`warte` zweimal rc 3, „Probe nicht gelaufen“, eine früher gestartete Sitzung im Repo), ist das ein Befund im Ergebnis, kein Abbruch.**

```
git add docs/belege/TB-158/b_probe.txt
git add docs/belege/TB-158/b_probe<i>_log.txt
git add docs/belege/TB-158/b_nach<i>.txt
git add docs/belege/TB-158/b_start<i>.txt
```

## Schritt C — Journal-Probe, dann Backlog

**C1. Journal-Probe — zuerst**, vor Backlog und Ergebnis (so nimmt ein Abbruch nichts Halbfertiges mit). Block nach `docs/belege/TB-158/d_block.md` (Schreibwerkzeug von Claude Code): Wortlaut aus Anhang B, Teil „Journal“, jede Stelle `<…>` durch den Wert der Sitzung ersetzt. Dann `PY WZ journal docs/belege/TB-158/d_block.md --probe > docs/belege/TB-158/d_journal_probe1.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal_probe1.txt`. Soll: neun Bedingungen `ja`, `Kennung <Kennung> (erwartet EV)`, `Zeilen +<n>` mit n = Zeilen des Blocks + 3, `rc 0`. **Endet `PY WZ journal docs/belege/TB-158/d_block.md --probe > docs/belege/TB-158/d_journal_probe1.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal_probe1.txt` mit rc 2** (eine Bedingung `NEIN`): den Block mit dem Edit-Werkzeug richten, dann `PY WZ journal docs/belege/TB-158/d_block.md --probe > docs/belege/TB-158/d_journal_probe2.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal_probe2.txt` (der erste Lauf bleibt als Beleg, nichts wird überschrieben); Soll wie oben. Endet auch dieser mit rc 2: ABBRUCH (Abbruchweg), kein Lauf ohne `--probe`. Die Stellen `<Kennung>` (Kopfzeile, Satz zu ⟨Abgabe⟩) trägt die Sitzung zuerst mit EV ein; nennt `WZ journal` eine andere Kennung (Bedingung der Kopfzeile `NEIN`, rc 2): diese an beiden Stellen mit dem Edit-Werkzeug eintragen, dann der Neulauf nach `d_journal_probe2.txt` wie oben, melden; der Abgabe-Commit trägt dieselbe Kennung.

**C2. Backlog.** Die Sitzung schreibt genau eine Zeile nach `docs/belege/TB-158/c_backlog_zeile.md` (Schreibwerkzeug von Claude Code), Wortlaut aus Anhang B, Teil „Backlog“, jede Stelle `<…>` durch den Wert der Sitzung ersetzt. Dann `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md --probe > docs/belege/TB-158/c_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/c_backlog_probe.txt` und `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md > docs/belege/TB-158/c_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/c_backlog.txt`. Soll je: sechs Bedingungen `ja`, `Zeilen +1`, `rc 0`. **Rückgabewerte von `backlog` und `journal`:** 0 gut · 2 eine Bedingung `NEIN`, nichts geschrieben — die Bedingung lesen, die Datei mit dem Edit-Werkzeug von Claude Code richten, beide Läufe neu, kein Abbruch; endet der zweite Versuch wieder mit rc 2, **ABBRUCH** (für `backlog` und `journal` gleich; kein Lauf ohne `--probe`) · 64 falscher Aufruf — **ABBRUCH** · eine Python-Ausnahme (Traceback, rc 1) — **ABBRUCH**. Endet `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md > docs/belege/TB-158/c_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/c_backlog.txt` (ohne `--probe`, nach einer Probe mit rc 0) mit rc ≠ 0: **ABBRUCH**.

## Schritt D — Ergebnis, Journal, Abgabe

**Ergebnis** `docs/ERGEBNIS_TB-158_waechter_probe.md` (Schreibwerkzeug von Claude Code): Kopf (Stand; Commits ⟨S0⟩, ⟨0⟩, ⟨A⟩, ⟨B⟩ je mit Hash; ⟨Abgabe⟩ ohne Hash — der Abgabe-Commit enthält das Ergebnis und kann seinen eigenen Hash nicht nennen) · „Kurz“ (Schritt · Soll · Ist) · „EIGEN“ ((a), (b), (c) und `(a) gegen (b)` aus `a_eigen.txt`; ob die Handbuchstelle bestätigt ist) · „Probe“ (je Lauf die Werte aus `b_probe.txt`) · „Belege“ (Datei · was · Befehl · Bytes · Zeilen · md5; `d_porcelain.txt` und `d_numstat.txt` entstehen erst nach ⟨Abgabe⟩ und stehen nicht in dieser Tabelle) · „Abweichungen vom Auftrag“ (jede; sonst „keine“ mit den geprüften Sollwerten) · „Nicht getan“ (die Posten unter „Nicht in TB-158“; der Zweig des echten Starts) · „In einfacher Sprache“.

**Journal.** Erst jetzt, nach einer Journal-Probe mit rc 0 (C1): `PY WZ journal docs/belege/TB-158/d_block.md > docs/belege/TB-158/d_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal.txt`. Soll wie in C1. Endet er mit rc ≠ 0: **ABBRUCH**.

**Abgabe.** Commit `TB-158 Abgabe: Ergebnis, Backlog, Journal <Kennung>` (erster Block unten; die Zeile für `d_journal_probe2.txt` nur, wenn es ihn gibt), pushen ⇒ **⟨Abgabe⟩**. Dann `git status --porcelain > "$TMPDIR/tb158_d.txt"`, `cp "$TMPDIR/tb158_d.txt" docs/belege/TB-158/d_porcelain.txt` (`cmp` gleich; Soll 0 B), erst danach `git diff --numstat ⟨S0⟩ ⟨Abgabe⟩ > docs/belege/TB-158/d_numstat.txt`. Soll: `1	0	docs/projektfuehrung/BACKLOG.md`, `<n>	0	docs/projektfuehrung/JOURNAL.md`, das Ergebnis, sonst nur Dateien unter `docs/belege/TB-158/`. Letzter Commit `TB-158 D: porcelain und numstat nach der Abgabe` (zweiter Block unten), pushen. **Danach** `git status --porcelain` noch einmal (genau dieser Befehl, keine Datei); die Rohausgabe steht wörtlich in der Schlussmeldung (Soll: leer).

```
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-158_waechter_probe.md
git add docs/belege/TB-158/c_backlog_zeile.md
git add docs/belege/TB-158/c_backlog_probe.txt
git add docs/belege/TB-158/c_backlog.txt
git add docs/belege/TB-158/d_block.md
git add docs/belege/TB-158/d_journal_probe1.txt
git add docs/belege/TB-158/d_journal_probe2.txt
git add docs/belege/TB-158/d_journal.txt
```

```
git add docs/belege/TB-158/d_porcelain.txt
git add docs/belege/TB-158/d_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab; in 0b weicht `starte_sitzung.sh` oder der sha256 von `WZ6` ab.
- Schritt A: der Befehl endet mit rc ≠ 0 oder einer Python-Ausnahme. (`EIGEN: nicht eindeutig` ist kein Abbruch.)
- Schritt C: der Neulauf `journal --probe` nach dem Edit (`d_journal_probe2.txt`) endet wieder mit rc 2; ebenso der zweite Lauf `backlog --probe` nach dem Edit.
- `backlog` oder `journal` ohne `--probe` enden mit rc ≠ 0 nach einer Probe mit rc 0.
- `WZ6 warte` endet mit rc 1 (nichts geschrieben: Z0 keine Zahl, Ziel nicht in `$TMPDIR` oder schon da; `tb156_werkzeug.py` Z. 452–453) oder einer Python-Ausnahme; rc 3 von `warte` (Z. 459) ist kein Abbruch (Schritt B Nr. 2). `WZ6 beleg` endet mit rc 2 (Beleg gibt es schon, Z. 434) oder einer Python-Ausnahme; `beleg` prüft keinen Ordner. Beide enden mit rc 1 bei falschem Aufruf oder wenn `starte_sitzung.sh` fehlt (Z. 512; Liste der Rückgaben Z. 6). `WZ backlog` oder `WZ journal` enden mit rc 64 oder einer Python-Ausnahme.
- **Kontofund** (Schranke 3; Schritt A, Schritt B Nr. 3): kein Beleg, nichts zitieren; im Abbruchweg nennt der Grund in `abbruch.txt` die Art der Angabe, ohne sie zu zitieren (Form `<Schritt>: <Grund>`). *Grund:* Belege werden gepusht.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen; verlangt schon Schritt 0 oder der Abbruchweg eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage im Chat melden.
- **Ein schreibender Befehl oder eine Datei, die der Anhang „Dateien und ihre Befehle“ nicht nennt (Schranke 7):** vor der Ausführung melden, nicht ausführen.
- Ein Schritt verlangte `osascript`, `launchctl`, eine Taste, ein Abmelden oder `/login`.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal (gilt **nicht** für ⟨S0⟩ — dort wird nicht wiederholt — und nicht für den Abbruch-Commit, siehe Abbruchweg).

**Kein Abbruch:** `EIGEN: nicht eindeutig`; `Probe: nein` in Schritt A; `warte` mit rc 3; weniger als zwei Läufe; jeder Befund aus Schritt B; „Probe nicht gelaufen“; der erste Lauf `backlog --probe` mit rc 2; der erste Lauf `journal --probe` mit rc 2; eine andere Kennung als EV; in 0b weicht `BACKLOG.md` oder `JOURNAL.md` ab; in D weicht `d_porcelain.txt` oder `d_numstat.txt` ab — je weiter, unter „Abweichungen“ nennen.

**Abbruchweg — so wenig wie möglich.** **Solange ⟨S0⟩ nicht gepusht ist** (0a weicht ab, der sha256 des Werkzeugs weicht ab, Commit oder Push von ⟨S0⟩ scheitert): nichts schreiben, nichts committen, nur im Chat melden (die Abweichung wörtlich). **Ab dem gepushten ⟨S0⟩:** genau eine neue Datei, `printf '%s\n' '<Schritt>: <Grund, ein Satz>' > docs/belege/TB-158/abbruch.txt` (in einfachen Anführungszeichen; der Grund enthält kein einfaches Anführungszeichen, keinen Backtick und kein Dollarzeichen; sie beschreibt sich selbst, keine Kopfdatei); dann `git add docs/belege/TB-158/abbruch.txt` und je eine Zeile `git add <Pfad>` mit dem Namen jeder Datei unter `docs/belege/TB-158/` aus dem Anhang, die schon entstanden und noch nicht committet ist — **Belege und schon geänderte Zieldateien:** ist `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/JOURNAL.md` oder `docs/ERGEBNIS_TB-158_waechter_probe.md` schon geändert oder angelegt, je eine Zeile `git add <Pfad>` dazu (Betreiber 14.10.2026: mitcommitten, damit der Arbeitsbaum sauber bleibt; ein halber Eintrag wird im nächsten Auftrag bereinigt); die Meldung nennt diese Zieldateien als Erstes; dann genau ein Commit `TB-158 Abbruch: <Schritt>` und genau ein Push. **Scheitert der Commit oder der Push des Abbruch-Commits: nicht wiederholen, keinen Ersatzbefehl, nichts zurücksetzen;** den Fehlertext wörtlich melden; **die Sitzung hält an.** **Gelingt der Push des Abbruch-Commits: melden; die Sitzung endet.** Kein Rückweg: nichts zurückdrehen, nichts löschen, nichts verschieben ausser dem Probe-Auslöser nach Schritt B Nr. 2; die Dateien unter `$TMPDIR` bleiben liegen.

## Nicht in TB-158

- Kein Bau am Wächter, nichts an `docs/werkzeuge/` (auch wenn die Probe einen Befund zeigt: nur melden).
- Regelwerk-Nachtrag zu Fassung 2 und Fehler ab Nr. 74 — eigener Auftrag danach.
- Bereinigung der Heimordner-Pfade.
- Der Zweig des echten Starts (Wache 4a, `starte_sitzung.sh` Z. 573–622) wird nicht geprobt.

## In einfacher Sprache

Der Wächter auf dem Mac startet Claude-Code-Sitzungen und schreibt ins Protokoll, was im neuen Fenster steht. Ob das wirklich klappt, wurde noch nie über den echten Weg ausprobiert: TB-156 sollte es tun, fand aber die eigene Sitzung nicht, weil `pgrep` auf dem Mac ohne `-a` die eigenen Vorfahren auslässt. TB-158 misst deshalb zuerst, wer die eigene Sitzung ist — mit `-a`, über den Ordner und über die Kette der Elternprozesse — und probt dann mindestens zweimal. Dabei erscheinen in der Claude-App kurz Gerätesitzungen, die gleich wieder verschwinden. Am Wächter selbst wird nichts geändert; die Sitzung meldet sich nie selbst an.

## Anhang — Dateien und ihre Befehle

Jede Datei, die die Sitzung schreibt, mit dem einzigen erlaubten Befehl (Einzelheiten im Schritt). `WZ6 beleg` schreibt kurz `<ziel>.tb156_neu` und ersetzt dann in einem Schritt das Ziel.

| Datei | Befehl | Schritt |
|---|---|---|
| `$TMPDIR/tb158_0a.txt` | `git status --porcelain > "$TMPDIR/tb158_0a.txt"` | 0a |
| `$TMPDIR/tb158_werkzeug.py` | der Holbefehl aus 0a, wörtlich | 0a |
| `docs/belege/TB-158/` (Ordner) | `mkdir -p docs/belege/TB-158` | 0a, nach ⟨S0⟩ |
| `docs/belege/TB-158/0a_status.txt` | `cp "$TMPDIR/tb158_0a.txt" docs/belege/TB-158/0a_status.txt` | 0a |
| `docs/belege/TB-158/tb158_werkzeug.py` | `cp "$TMPDIR/tb158_werkzeug.py" docs/belege/TB-158/tb158_werkzeug.py` | 0a |
| `docs/belege/TB-158/0b_ausgang.txt` | der Block aus 0b, wörtlich | 0b |
| `$TMPDIR/tb158_a_eigen.txt` | der Befehl aus Schritt A, wörtlich | A |
| `docs/belege/TB-158/a_eigen.txt` | `PY WZ6 beleg "$TMPDIR/tb158_a_eigen.txt" docs/belege/TB-158/a_eigen.txt` | A |
| `docs/auftraege/_ausloeser/probe_<EIGEN>` (nicht in git) | `: > docs/auftraege/_ausloeser/probe_<EIGEN>`; liegt er nach dem Warten noch dort: `mv docs/auftraege/_ausloeser/probe_<EIGEN> docs/auftraege/_ausloeser/_erledigt/` | B |
| `$TMPDIR/tb158_b_probe<i>.txt` | `PY WZ6 warte <Z0> "$TMPDIR/tb158_b_probe<i>.txt"` | B |
| `docs/belege/TB-158/b_probe<i>_log.txt` | `PY WZ6 beleg "$TMPDIR/tb158_b_probe<i>.txt" docs/belege/TB-158/b_probe<i>_log.txt` | B |
| `$TMPDIR/tb158_b_nach<i>.txt` | `{ pgrep -a -x claude; for p in $(pgrep -a -x claude); do lsof -a -p "$p" -d cwd -Fn; done; } > "$TMPDIR/tb158_b_nach<i>.txt" 2>&1` | B |
| `docs/belege/TB-158/b_nach<i>.txt` | `PY WZ6 beleg "$TMPDIR/tb158_b_nach<i>.txt" docs/belege/TB-158/b_nach<i>.txt` | B |
| `$TMPDIR/tb158_b_start<i>.txt` | der Befehl aus Schritt B Nr. 5, wörtlich | B |
| `docs/belege/TB-158/b_start<i>.txt` | `PY WZ6 beleg "$TMPDIR/tb158_b_start<i>.txt" docs/belege/TB-158/b_start<i>.txt` | B |
| `docs/belege/TB-158/b_probe.txt` | Schreibwerkzeug (erste Zeile), danach Edit-Werkzeug von Claude Code (jede weitere); die Formen nennt Schritt B | A, B |
| `docs/belege/TB-158/c_backlog_zeile.md` | Schreibwerkzeug von Claude Code (Anhang B); bei rc 2 Edit-Werkzeug | C |
| `docs/belege/TB-158/c_backlog_probe.txt` | `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md --probe > docs/belege/TB-158/c_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/c_backlog_probe.txt` | C |
| `docs/belege/TB-158/c_backlog.txt` | `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md > docs/belege/TB-158/c_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/c_backlog.txt` | C |
| `docs/projektfuehrung/BACKLOG.md` | `PY WZ backlog docs/belege/TB-158/c_backlog_zeile.md` (im Befehl zu `c_backlog.txt`) | C |
| `docs/ERGEBNIS_TB-158_waechter_probe.md` | Schreibwerkzeug von Claude Code, Gliederung Schritt D | D |
| `docs/belege/TB-158/d_block.md` | Schreibwerkzeug von Claude Code (Anhang B); bei rc 2 Edit-Werkzeug | D |
| `docs/belege/TB-158/d_journal_probe1.txt` | `PY WZ journal docs/belege/TB-158/d_block.md --probe > docs/belege/TB-158/d_journal_probe1.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal_probe1.txt` | D |
| `docs/belege/TB-158/d_journal_probe2.txt` | nur nach rc 2 des ersten Laufs: `PY WZ journal docs/belege/TB-158/d_block.md --probe > docs/belege/TB-158/d_journal_probe2.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal_probe2.txt` | D |
| `docs/belege/TB-158/d_journal.txt` | `PY WZ journal docs/belege/TB-158/d_block.md > docs/belege/TB-158/d_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-158/d_journal.txt` | D |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal docs/belege/TB-158/d_block.md` (im Befehl zu `d_journal.txt`) | D |
| `$TMPDIR/tb158_d.txt` | `git status --porcelain > "$TMPDIR/tb158_d.txt"` | D |
| `docs/belege/TB-158/d_porcelain.txt` | `cp "$TMPDIR/tb158_d.txt" docs/belege/TB-158/d_porcelain.txt` | D |
| `docs/belege/TB-158/d_numstat.txt` | `git diff --numstat ⟨S0⟩ ⟨Abgabe⟩ > docs/belege/TB-158/d_numstat.txt` | D |
| `docs/belege/TB-158/abbruch.txt` | nur bei Abbruch: `printf '%s\n' '<Schritt>: <Grund, ein Satz>' > docs/belege/TB-158/abbruch.txt` | Abbruchweg |

Die Dateien unter `$TMPDIR` bleiben liegen — nicht löschen (`deny`: `Bash(rm:*)`), nicht committen. Sonst schreibt die Sitzung nur über git: hinzufügen mit Namen, `git commit`, `git push`.

## Anhang A — Werkzeug

### Werkzeug

```python
#!/usr/bin/env python3
# TB-158 Werkzeug (Python 3.9): fuegt eine Zeile in BACKLOG.md und den Block der Sitzung in JOURNAL.md ein; sonst nichts.
# Prueft alles, bevor es schreibt. Aufruf im Repo: PY WZ backlog <zeile.md> [--probe] | PY WZ journal <block.md> [--probe]
# rc 0 gut · 2 eine Bedingung NEIN, nichts geschrieben · 64 falscher Aufruf. Der Journal-Teil ist der von TB-157 (Kennung EV).
import hashlib, re, sys
JOU = "docs/projektfuehrung/JOURNAL.md"
BAC = "docs/projektfuehrung/BACKLOG.md"
ANKER = "- **`pgrep` ohne `-a`** (UEBERGABE, Nachtrag 13.10.2026, 15:57):"
VOR = "  - **Nachtrag TB-158 ("
ERG = "docs/ERGEBNIS_TB-158_waechter_probe.md"

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5(p):
    return hashlib.md5(lies(p).encode("utf-8")).hexdigest()

def backlog(a):
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(BAC).split("\n")
    k = [i for i, s in enumerate(z) if s.startswith(ANKER)]
    be = [("genau eine Zeile mit Zeilenende", b.endswith("\n") and b.count("\n") == 1),
          ("beginnt mit '%s'" % VOR, b.startswith(VOR)),
          ("nennt %s" % ERG, ERG in b),
          ("keine offene Stelle (kein '<', kein '>')", "<" not in b and ">" not in b),
          ("Anker genau einmal", len(k) == 1),
          ("Nachtrag noch nicht da", not any(s.startswith(VOR) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Ausgang %s · %d Zeilen · md5 %s" % (BAC, len(z) - 1, md5(BAC)))
    if not all(v for _, v in be):
        return 2
    print("Anker Z. %d · Zeilen +1" % (k[0] + 1))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[k[0] + 1:k[0] + 1] = [b[:-1]]
    t = "\n".join(z)
    with open(BAC, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (BAC, md5(BAC), "gleich" if lies(BAC) == t else "UNGLEICH"))
    return 0

def journal(a):
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(JOU).split("\n")
    bz = b.split("\n")
    L = [i for i, s in enumerate(z) if s == "## Wiederkehrende Lehren"]
    k = [re.match(r"^## ([A-Z]{2}) — TB-", s).group(1) for s in z[:L[0] if L else 0] if re.match(r"^## ([A-Z]{2}) — TB-", s)]
    letzte = k[-1] if k else "??"
    n2 = chr(ord(letzte[1]) + 1) if letzte[1] != "Z" else "A"
    nk = (letzte[0] if letzte[1] != "Z" else chr(ord(letzte[0]) + 1)) + n2
    be = [("endet mit Zeilenende", b.endswith("\n") and not b.endswith("\n\n")),
          ("Kopfzeile ## %s — TB-158: …" % nk, bz[0].startswith("## %s — TB-158: " % nk)),
          ("### Was gemessen ist genau einmal, Leerzeile davor", bz.count("### Was gemessen ist") == 1 and bz[bz.index("### Was gemessen ist") - 1] == ""),
          ("### Was offen bleibt genau einmal", bz.count("### Was offen bleibt") == 1),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", bz[-2].startswith("*Geschrieben ") if len(bz) > 1 else False),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(s.startswith("## %s — " % nk) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (erwartet %s) · letzte %s" % (nk, "EV", letzte))
    if not all(v for _, v in be):
        return 2
    neu = bz[:-1] + ["", "---", ""]
    print("Zeilen +%d" % len(neu))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[L[0]:L[0]] = neu
    t = "\n".join(z)
    with open(JOU, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (JOU, md5(JOU), "gleich" if lies(JOU) == t else "UNGLEICH"))
    return 0

def main(a):
    f = {"backlog": backlog, "journal": journal}.get(a[0] if a else "")
    if not f:
        print("Aufruf: PY WZ backlog <zeile.md> [--probe] | PY WZ journal <block.md> [--probe]")
        return 64
    return f(a)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Anhang B — Wortlaute (die Sitzung ersetzt nur die Stellen `<…>`)

**Backlog** (eine Zeile, nach `c_backlog_zeile.md`):

~~~
  - **Nachtrag TB-158 (<TT.MM.JJJJ>):** EIGEN in der Sitzung: (a) `pgrep -x claude` <PIDs oder keine>, (b) `pgrep -a -x claude` <PIDs>, EIGEN <PID oder nicht eindeutig>; Probe <gelaufen, Läufe und rc, oder nicht gelaufen und der Grund>. Beleg `docs/belege/TB-158/a_eigen.txt`, Ergebnis `docs/ERGEBNIS_TB-158_waechter_probe.md`.
~~~

**Journal** (nach `d_block.md`; erlaubte Stelle: der Satz zu ⟨Abgabe⟩ bleibt wörtlich bis auf `<Kennung>` (die Kennung, die `WZ journal` nennt) — der Abgabe-Commit enthält diesen Block und kann seinen eigenen Hash nicht nennen, wie ET, `JOURNAL.md` Z. 10596):

~~~
## <Kennung> — TB-158: Probe des Wächters; EIGEN mit `pgrep -a`, cwd und Elternkette
*Quelle: `docs/ERGEBNIS_TB-158_waechter_probe.md`, Commits ⟨S0⟩ `<Hash>`, ⟨0⟩ `<Hash>`, ⟨A⟩ `<Hash>`, ⟨B⟩ `<Hash>`, ⟨Abgabe⟩ = der Commit „TB-158 Abgabe: Ergebnis, Backlog, Journal <Kennung>“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** <ein Satz: was gemessen ist, wo>

### Was gemessen ist
- <je Schritt eine Zeile mit Soll und Ist>

### Was offen bleibt
- <offene Posten, mindestens: der Zweig des echten Starts; Regelwerk-Nachtrag zu Fassung 2 und Fehler ab Nr. 74>

*Geschrieben <Datum, Uhrzeit aus date> von der Mac-Sitzung TB-158. Quellenvermerk: siehe Kopf.*
~~~
