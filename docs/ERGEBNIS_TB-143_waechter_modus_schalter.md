# ERGEBNIS TB-143 — Wächter: Modus-Schalter in der Startzeile, Vorprobe `osascript`

**Sitzung:** `TB-143`, Mac, Claude Code 2.1.295, Modell Opus 5.5 · **Datum:** 09.10.2026, 09:2x–09:3x CEST
**Auftrag:** `docs/auftraege/MAC_TB-143_waechter_modus_schalter.md` (mitcommittet in ⟨S0⟩)
**Commits:** ⟨S0⟩ `9f7befe` (Schritt 0) · ⟨A⟩ `1636764a3d6bc4d6a568432aeaf2ee2b7e1f641d` (Schalter) · Abgabe (dieser Commit)
**Belege:** `docs/belege/TB-143/` — je Rohausgabe `<name>.txt` und Beschreibung `<name>.kopf.txt`
**Rückfragen an den Betreiber:** keine.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `a57d5c2…6371`, genau drei Einträge; `cmp` gleich | HEAD `a57d5c2ee2282a3bb5d6ee4331810fd6aaea6371`, genau die drei Einträge; ⟨S0⟩ `9f7befe` gepusht; `cmp` gleich |
| 0b | 357 Zeilen, md5 `03649f5cdebe6b478e5353e92a044d13` | 357 Zeilen, md5 `03649f5cdebe6b478e5353e92a044d13` |
| A1 | mindestens eine Hilfezeile zu `--permission-mode` | Z. 150–153: `--permission-mode <mode>`, choices `"acceptEdits", "auto", "bypassPermissions", "manual", "dontAsk", "plan"` — nennt `manual`, nicht `default` ⇒ **WERT = `manual`** |
| A2 | die zwei Soll-Zeilen wörtlich | wörtlich gleich: `357 Zeilen | Z. 327 ersetzt | alt 0 | neu 1 | bash -n rc 0` und `'do script' 1 | ' in window' 0 | 'keystroke' 0 | 'System Events' 0 | '--permission-mode' 1`; rc 0; `starte_sitzung.sh.tb143.neu` liegt nicht mehr |
| A3 | eine Zahlenzeile `1 1 <Pfad>` | `1	1	docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`; ⟨A⟩ `1636764` gepusht |
| B | einer von vier Ausgängen | **LÄUFT** — Ausgabe `21040, 21346, 21349`, ohne Rückfrage, ohne Fehler |

Zeile 327 lautet jetzt:

```
    set neu to do script "cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control"
```

## Abweichungen vom Auftrag

- **WERT ist `manual`, nicht `default`.** Der Titel des Auftrags nennt `--permission-mode default`; A1 schreibt aber vor, bei einer Werteliste mit `manual` und ohne `default` `manual` zu nehmen. Das ist hier der Fall. Commit-Text von ⟨A⟩ entsprechend: „… (--permission-mode manual)“. Ob die Befehlszeile auch `default` angenommen hätte, ist nicht gemessen.
- **`a1_hilfe.txt` trägt eine Zusatzzeile** `rc grep 0` (Rückgabewert von `grep`) und zwei Überschriftzeilen `## …`; in `a1_hilfe.kopf.txt` vermerkt.
- **`b_vorprobe.txt` ist übertragen, nicht umgeleitet.** Der Befehl in B1 lief wörtlich ohne Umleitung (keine Variante); die Ausgabe steht unverändert aus dem Werkzeugergebnis im Beleg. In `b_vorprobe.kopf.txt` vermerkt; dort steht auch die Aussage aus B0.

## Beobachtungen (nicht verlangt, nicht gedeutet)

- **B0, Aussage, keine Messung:** Diese Sitzung lief nach eigener Kenntnis im **Auto-Modus** — gestartet mit der alten Zeile 327, und die Hinweise, die Claude Code ihr mitgibt, lauten „While auto mode is active“.
- **Der direkte lesende Aufruf lief also im Auto-Modus durch**, während TB-142 zwei Aufrufe über Skriptdateien verwehrt wurden (`docs/belege/TB-142/abbruch.txt`). Die Vermutung im Auftrag („dass Claude Code auch einen direkten Aufruf `osascript -e …` ablehnt, ist naheliegend“) trifft für diesen einen lesenden Aufruf **nicht** zu. Was das für die Aufrufe von TB-144 heisst, die Fenster öffnen oder lesen, ist nicht gemessen.
- Drei Terminal-Fenster: `21040`, `21346` (laut UEBERGABE die wartende TB-142-Sitzung, PID 40587), `21349`. Welches Fenster diese Sitzung trägt, ist nicht gemessen.
- **Die neue Zeile 327 ist ab ⟨A⟩ scharf** (launchd ruft das Skript aus dem Arbeitsbaum auf). Ob eine so gestartete Sitzung wirklich startet und im Modus „Manual“ steht, misst erst TB-144.

## Nicht getan

- Keine zweite Sitzung gestartet, kein Auslöser gelegt, keine Messung M1–M5, keine Stücke W2–W6, keine Unterlagen, kein Journalblock (alles TB-144).
- Keine AppleScript-Prüfung der neuen Zeile (`bash -n` prüft den AppleScript-Rumpf nicht; Auftrag „Offen“).
- Keine Einstellungsdatei von Claude Code angefasst; `--no-chrome` nicht gesetzt.

## In einfacher Sprache

Der Wächter startet neue Claude-Code-Sitzungen ab jetzt mit dem Schalter `--permission-mode manual`. Die installierte Version kennt den Namen `default` in ihrer Hilfe nicht, nur `manual` — das ist laut Dokumentation derselbe Modus, und der Auftrag hatte genau diesen Fall vorgesehen. In diesem Modus gilt wieder unsere eigene Liste: alles erlaubt ausser der Sperrliste. Danach hat diese Sitzung — die selbst noch im Auto-Modus lief — einen einzigen harmlosen Befehl ausprobiert, der nur die Nummern der offenen Terminal-Fenster liest. Er lief ohne Ablehnung und ohne Rückfrage. Ob die nächste Sitzung tatsächlich im neuen Modus startet, zeigt erst TB-144.
