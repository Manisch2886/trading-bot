# Nachtragswächter — die Bringschuld der Nachträge

**Angelegt 21.09.2026 (TB-64).** `system/nachtragswaechter.py` ist ein Wächter
wie die vier aus TB-32: rein lesend, Rückgabewert 1 bei Befund, gemeldet über
`notifications/waechter_melden.py nachtraege`.

## Warum

Notizen an Backlog und Journal entstehen zuerst als Datei unter
`docs/projektfuehrung/nachtraege/` und werden *irgendwann* eingearbeitet. Der
zweite Schritt kann ausfallen, ohne dass es jemand merkt: Nachtrag `(m)` vom
19.09.2026 wurde übersprungen, seine sechs Nummern wurden an andere Inhalte
vergeben, aufgefallen ist es zwei Tage später durch Zufall. Die einzige Wache
dagegen war, dass jemand daran denkt.

## Was er prüft

**Der Zustand wird durch den Ort ausgedrückt:** eingearbeitete Nachträge liegen
unter `nachtraege/_eingearbeitet/`, was im Hauptordner liegt, ist offen.

| | Prüfung | Befund, wenn |
|---|---|---|
| **A** | Was liegt offen? | eine Datei im Hauptordner ist älter als die Frist (Standard **1 Tag**, `--frist-tage`) — auch wenn alle Nummern angekommen sind (dann lautet der Rat: verschieben) |
| **B** | Ist von den verschobenen wirklich alles angekommen? | eine Datei unter `_eingearbeitet/` hat eine Nummer, die nicht im Ziel steht — *falsch verschoben* |
| **C** | Doppelbelegung | eine Nummer steht im Ziel mehr als einmal (gezählt **ohne `sort -u`**) |

**Nummern eines Backlog-Nachtrags:** K-Nummern `| **K2p**`, Blockbezeichner
`## 2s`, Kettenzeilen `| **0,86b**` — die Muster haben **keinen schliessenden
Balken**, sonst fällt jede Zeile mit Vergabevermerk heraus. **Angekommen**
heisst nicht nur „die Nummer steht im Ziel": geprüft wird der **Kern des
Textes** (die ersten 40 Zeichen hinter der Nummernzelle) in der Zielzeile
derselben Nummer, sonst irgendwo im Ziel (Nummer bei der Einarbeitung
geändert), sonst ein **Vergabevermerk, der den Nachtrag selbst nennt**
(`(m)`, `(19m)` oder der Dateiname, dazu die Nummer in Backticks und
„vorgeschlagen"/„vergeben"). Ziel: `BACKLOG.md` und `BACKLOG_ARCHIV.md`.

**Kennung eines Journal-Nachtrags:** sein Dateiname in einer Zeile
`*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*`
in `JOURNAL.md` — verglichen über den Dateinamen, nicht den Pfad;
`*Messprotokoll: …*`-Zeilen zählen nicht.

**Nicht prüfbar (A2):** ein Backlog-Nachtrag ohne Nummer der drei Formen wird
getrennt gemeldet — nicht grün, nicht rot. Im Hauptordner zählt er trotzdem als
offen.

## Ausgabe und Meldung

Die Zeilen `Zusammenfassung:` und `BEFUND:` gehen per Telegram (Marken in
`waechter_melden.py`). Sie nennen **kein Alter in Tagen** — der Wrapper dämpft
Wiederholungen über den Fingerabdruck der gesendeten Zeilen, und ein täglich
wachsendes Alter wäre jeden Tag ein „geänderter Befund". Das Alter je Datei
steht in den Zeilen darüber, die vollständig im Log
(`logs/system/nachtraege.log`) landen.

```
python3 system/nachtragswaechter.py                # gegen das Repo, rc 0/1/2
python3 system/nachtragswaechter.py --knapp        # ohne Einzelzeilen je Nummer
python3 system/nachtragswaechter.py --json PFAD    # Ergebnis zusätzlich als JSON
python3 system/test_nachtragswaechter.py           # Selbsttest, 62 Prüfungen
```

## Die Cron-Zeile (Vorschlag — **nicht eingetragen**, Betreiberarbeit)

```cron
50 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py nachtraege >> logs/system/nachtraege.log 2>&1
```

## Was er nicht tut

Er arbeitet nichts ein, verschiebt nichts und ändert keine Datei. Das
Verschieben nach `_eingearbeitet/` ist Sache der einarbeitenden Sitzung — und
Prüfung B ist die Wache dagegen, dass verschoben wird, ohne einzuarbeiten.
