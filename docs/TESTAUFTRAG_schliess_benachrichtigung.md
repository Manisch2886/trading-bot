# Testauftrag: Telegram-Nachricht bei jedem geschlossenen Trade

**Für eine lokale Claude-Code-Sitzung auf dem Mac.** Die Schritte 0–4 und 6–8
laufen **ohne Rückfragen** durch.

> ## ⚠️ Schritt 5 ist anders als alle anderen
>
> **Schritt 5 ist der Erstlauf. Er lässt sich nicht wiederholen** und muss vom
> Nutzer **ausdrücklich bestätigt** werden, bevor er ausgeführt wird. Er
> vermerkt die hunderte bereits geschlossenen Trades unwiderruflich als
> erledigt. Danach werden sie nie nachgemeldet — das ist beabsichtigt, aber es
> ist eine Einbahnstraße.
>
> **Führe Schritt 5 NICHT von selbst aus.** Arbeite die Schritte 0–4 ab, lege
> dann das Ergebnis vor und frage nach der Freigabe. Schritt 6–8 folgen erst
> nach Schritt 5.

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`3c1fbbf`), PR #78.

> Die Schritte 0–4 verändern **nichts**: die Selbsttests laufen gegen
> Wegwerf-Projekte unter `/tmp`, kein echter Netzaufruf, keine Telegram-Nachricht.
> Die Mutationsproben in Schritt 4 stellen den Urzustand selbst wieder her und
> werden in Schritt 8 gegengeprüft.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short            # muss LEER sein
git rev-parse --abbrev-ref HEAD
pip3 install -r requirements.txt
```

Erwartet: keine Ausgabe bei `git status`, Branch
`claude/new-session-uqjk8h`.

---

## Schritt 1 — Alle Suiten

```bash
python3 notifications/test_schliess_benachrichtigung.py | tail -2
python3 notifications/test_manual_close.py  | tail -1
python3 dashboard/test_dashboard.py         | tail -1
python3 broker/test_broker.py               | tail -1
python3 broker/test_ibkr.py                 | tail -1
python3 shared/test_empfehlung_format.py    | tail -1
python3 system/test_caffeinate_plist.py     | tail -1
```

| Suite | Erwartet |
|---|---|
| `notifications/test_schliess_benachrichtigung.py` *(neu)* | **99 von 99** |
| `notifications/test_manual_close.py` | alle bestanden |
| `dashboard/test_dashboard.py` | 784/784 (780 ohne `node`) |
| `broker/test_broker.py` | 163 von 163 |
| `broker/test_ibkr.py` | 200 von 200 (168 ohne `ib_async`) |
| `shared/test_empfehlung_format.py` | 70/70 |
| `system/test_caffeinate_plist.py` | 52 von 52 |

Kein echter Netzaufruf in der neuen Suite — der Sendeweg ist ein Parameter.
Gegenprobe, dass nicht heimlich doch `notify` benutzt wird:

```bash
grep -n "from notify import\|import notify" notifications/test_schliess_benachrichtigung.py || echo "OK: die Testsuite importiert notify nicht"
```

---

## Schritt 2 — Die Nachricht ansehen, ohne zu senden

`--trockenlauf` zeigt, **was** gesendet würde. Es sendet nichts und vermerkt
nichts:

```bash
python3 notifications/schliess_benachrichtigung.py --trockenlauf
```

Erwartet **vor** dem Erstlauf genau eine Zeile:

```
ERSTLAUF: N bestehende Trades wuerden stillschweigend vermerkt, eine Bestaetigung gesendet.
```

Die Zahl `N` notieren — sie muss in Schritt 5 wieder auftauchen.

Und so sieht eine einzelne Nachricht aus (ohne jede Datenbank, reine
Formatierung):

```bash
python3 - <<'PYEOF'
import sys
sys.path[:0] = ["notifications", "broker"]
import schliess_benachrichtigung as sb
print(sb.nachricht_fuer("turtle_soup_stocks", {
    "id": 42, "symbol": "AAPL", "entry_price": 200.0, "exit_price": 190.4,
    "result": "stop_loss", "pnl_pct": -4.8,
    "entry_time": "2026-09-08 00:00:00", "exit_time": "2026-09-11 05:00:00"}))
print()
print(sb.sammelnachricht([
    ("t3_supertrend", {"symbol": "BTCUSDT", "pnl_pct": 1.7, "result": "trend_flip"}),
    ("volatility_breakout", {"symbol": "MSFT", "pnl_pct": -3.2, "result": "stop_loss"}),
]))
PYEOF
```

Erwartet:

```
🔴 *Trade geschlossen* – Turtle Soup (Aktien)
*AAPL*  ·  *-4.80 %*
Einstieg 200 → Ausstieg 190.4
Gehalten: 3 Tage 5 Std.
Grund: Stop-Loss ausgelöst

*2 Trades geschlossen*

🟢 T3/ADX/SuperTrend (Krypto) · *BTCUSDT* *+1.70 %* – Trendwechsel (SuperTrend hat gedreht)
🔴 Volatility Breakout (Aktien) · *MSFT* *-3.20 %* – Stop-Loss ausgelöst
```

Sechs Dinge prüfen: verständlicher Bot-Name (nicht `turtle_soup_stocks`),
Symbol, **Prozent mit Vorzeichen**, Ein- **und** Ausstiegskurs, Haltedauer,
Grund als Satz (**nicht** `stop_loss`). Und: **kein €, kein $** — die Bots
tracken kein echtes Kapital.

---

## Schritt 3 — Die alte, dünne Meldung ist wirklich weg

Das ist der Teil, der einen bestehenden Sendeweg entfernt — also der, den man
am genauesten ansehen sollte.

```bash
python3 notifications/test_schliess_benachrichtigung.py 2>&1 | sed -n '/10\. Die alte/,$p'
```

Erwartet, alle `[OK ]`:

- `monitor.py` erzeugt keine Schließ-Meldung mehr
- die **Eröffnungs**-Meldung ist unberührt
- die **Cronjob-Warnung** ist unberührt
- die **Staleness-Warnung** ist unberührt
- der Zustand wird weiter geführt (er trägt die Erkennung *neuer* Trades)
- an der Stelle steht, wohin die Meldung umgezogen ist
- **am Verhalten:** eine Schließung erzeugt kein Ereignis mehr, eine Eröffnung
  schon

Dass wirklich nur die 13 Zeilen weg sind und nichts anderes:

```bash
git fetch origin main
git diff origin/main HEAD -- notifications/monitor.py | grep '^-[^-]'
```

Erwartet: genau die 13 entfernten Zeilen (die `newly_closed_ids`-Schleife und
die alte `events.append(...)`) plus die eine ersetzte `known_open_ids`-Zeile.
Kommt dort mehr, ist das ein Befund.

---

## Schritt 4 — Mutationsproben

```bash
cat > /tmp/mutation_meldung.py <<'PYEOF'
import subprocess, os
W = os.path.expanduser("~/trading-bot")
T = ["python3", "notifications/test_schliess_benachrichtigung.py"]
SB = "notifications/schliess_benachrichtigung.py"
MON = "notifications/monitor.py"
M = [
 ("M1  UNIQUE wirkungslos gemacht", SB,
  "            UNIQUE(bot, trade_id)\n", "            UNIQUE(bot, trade_id, zeitpunkt)\n", T),
 ("M2  Anspruch erst NACH dem Senden", SB,
  "        if not anspruch_nehmen(conn, bot, trade, jetzt):\n            continue\n        if senden(nachricht_fuer(bot, trade)):\n            bestaetigen(conn, bot, trade[\"id\"])",
  "        if senden(nachricht_fuer(bot, trade)):\n            anspruch_nehmen(conn, bot, trade, jetzt)\n            bestaetigen(conn, bot, trade[\"id\"])", T),
 ("M3  Fehlgeschlagener Versand wird trotzdem vermerkt", SB,
  "            anspruch_freigeben(conn, bot, trade[\"id\"])\n            fehlgeschlagen += 1",
  "            bestaetigen(conn, bot, trade[\"id\"])\n            fehlgeschlagen += 1", T),
 ("M4  Erstlauf sendet den ganzen Bestand einzeln", SB,
  "        if lage[\"erstlauf\"]:\n            ergebnis = erstlauf_durchfuehren(conn, paare, senden, jetzt)",
  "        if False:\n            ergebnis = erstlauf_durchfuehren(conn, paare, senden, jetzt)", T),
 ("M5  Erstlauf-Marke wird nicht geschrieben", SB,
  "        conn.execute(\"INSERT OR REPLACE INTO zustand (schluessel, wert) \"\n                      \"VALUES (?,?)\", (MARKE_ERSTLAUF, zeitpunkt))",
  "        pass", T),
 ("M6  Erstlauf greift auch bei vorhandenen Vermerken", SB,
  "    if anzahl:\n        # Marke fehlt, Zeilen sind da.", "    if False:\n        # Marke fehlt, Zeilen sind da.", T),
 ("M7  Obergrenze wirkungslos (Rest faellt weg)", SB,
  "    einzeln, rest = paare[:grenze], paare[grenze:]", "    einzeln, rest = paare[:grenze], []", T),
 ("M8  Ausstiegsgrund als roher Feldwert", SB,
  "    bekannt = AUSSTIEGSGRUENDE.get(str(result))\n    return bekannt if bekannt else f\"{result} (unbekannter Ausstiegsweg)\"",
  "    return str(result)", T),
 ("M9  PnL ohne Vorzeichen", SB,
  "        return f\"{float(wert):+.2f} %\"", "        return f\"{float(wert):.2f} %\"", T),
 ("M10 Haltedauer faellt weg", SB,
  "        f\"Gehalten: {haltedauer_text(trade.get('entry_time'), trade.get('exit_time'))}\\n\"", "        f\"\"\n", T),
 ("M11 Ein- und Ausstiegskurs fallen weg", SB,
  "        f\"Einstieg {_kurs(trade.get('entry_price'))} → \"\n        f\"Ausstieg {_kurs(trade.get('exit_price'))}\\n\"", "        f\"\"\n", T),
 ("M12 Ordnername statt Anzeigename", SB,
  "        f\"{_sauber(monitor.display_name(bot))}\\n\"", "        f\"{bot}\\n\"", T),
 ("M13 Markdown-Zeichen bleiben in Werten stehen", SB,
  "    for zeichen in MARKDOWN_WIRKSAM:\n        text = text.replace(zeichen, \"\")", "    pass", T),
 ("M14 Gebuendelter Modus sendet einzeln", SB,
  "        if modus == MODUS_GEBUENDELT:\n            ergebnis = _gebuendelt(conn, paare, senden, jetzt)",
  "        if False:\n            ergebnis = _gebuendelt(conn, paare, senden, jetzt)", T),
 ("M15 Bot-DB nicht mehr ueber bot_db gelesen", SB,
  "        alle = bot_db.lies_trades(bot, base_dir or BASE_DIR)",
  "        import sqlite3 as _s; _c = _s.connect(os.path.join(base_dir or BASE_DIR, f'paper_trading_{bot}.db')); _c.row_factory=_s.Row; alle=[dict(z) for z in _c.execute('SELECT * FROM trades')]; _c.close()", T),
 ("M16 Die alte Meldung in monitor.py wieder eingebaut", MON,
  "        # HIER STAND BIS 2026-09-12 DIE MELDUNG \"Trade geschlossen\".",
  "        newly_closed_ids = set(bot_state.get(\"known_open_ids\", [])) - currently_open_ids\n        for _tid in sorted(newly_closed_ids):\n            events.append(f\"STOP-LOSS ausgeloest {_tid}\")\n        # HIER STAND BIS 2026-09-12 DIE MELDUNG \"Trade geschlossen\".", T),
]
for name, datei, alt, neu, befehl in M:
    pfad = os.path.join(W, datei)
    urtext = open(pfad, encoding="utf-8").read()
    if urtext.count(alt) != 1:
        print(f"[SETUP-FEHLER] {name}: {urtext.count(alt)} Fundstellen"); continue
    open(pfad, "w", encoding="utf-8").write(urtext.replace(alt, neu, 1))
    try:
        lauf = subprocess.run(befehl, cwd=W, capture_output=True, text=True, timeout=600)
        erste = [z for z in lauf.stdout.splitlines() if "[FEHLER]" in z][:1]
        print(f"[{'ERKANNT' if lauf.returncode else 'UNENTDECKT'}] {name}")
        if erste: print(f"      -> {erste[0].strip()[:120]}")
    finally:
        open(pfad, "w", encoding="utf-8").write(urtext)
PYEOF
python3 /tmp/mutation_meldung.py
```

**Erwartet: 16 von 16 `[ERKANNT]`.** Ein einziges `[UNENTDECKT]` ist ein Befund.

Die wichtigsten:

| Probe | Belegt |
|---|---|
| **M1, M2** | Die Sperre gegen Doppelversand ist strukturell und der Anspruch wird **vor** dem Senden genommen |
| **M3** | Ein fehlgeschlagener Versand wird nicht als gemeldet vermerkt |
| **M4, M5, M6** | Der Erstlauf überspringt, greift kein zweites Mal, und wird beim Widerspruch abgelehnt |
| **M7** | Die Obergrenze verliert keinen Trade |
| **M8–M12** | Jede der sechs Inhaltsangaben ist wirklich geprüft |
| **M15** | Die Bot-DB wird nur über `broker/bot_db.py` gelesen |
| **M16** | Die alte Meldung bleibt weg |

---

# ⚠️ Schritt 5 — DER ERSTLAUF (nicht wiederholbar, Freigabe nötig)

**HIER ANHALTEN.** Lege das Ergebnis der Schritte 0–4 vor und frage den Nutzer
ausdrücklich, ob der Erstlauf ausgeführt werden soll.

## Warum das eine Einbahnstraße ist

In den neun Datenbanken liegen hunderte bereits geschlossene Trades. Der erste
Lauf vermerkt sie **unwiderruflich** als erledigt und schickt genau **eine**
Bestätigungsnachricht. Danach werden sie nie nachgemeldet.

Das ist gewollt — die Alternative wären hunderte Push-Nachrichten. Aber es
lässt sich nicht zurücknehmen, ohne die Nachverfolgungsdatenbank zu löschen,
und dann würden beim nächsten Lauf genau diese hunderte Nachrichten rausgehen.

## Vorher: zeigen, was passieren wird

```bash
cd ~/trading-bot
mkdir -p logs/notifications
python3 notifications/schliess_benachrichtigung.py --status
python3 notifications/schliess_benachrichtigung.py --trockenlauf
```

Erwartet bei `--status`:

```
Nachverfolgung: /Users/…/trading-bot/benachrichtigungen_schliessung.db
Erstlauf: noch offen
  gesendet                 0
  wird_gesendet            0
  erstlauf_uebersprungen   0

Noch nicht gemeldet: N
```

Die Zahl `N` muss mit der aus Schritt 2 übereinstimmen. **Weicht sie ab, nicht
weitermachen** — dann hat sich zwischenzeitlich etwas verändert, und das gehört
erst verstanden.

## Die Freigabe

Dem Nutzer genau das vorlegen:

> Der Erstlauf vermerkt **N** bereits geschlossene Trades unwiderruflich als
> erledigt und schickt **eine** Telegram-Nachricht. Diese N Trades werden
> danach nie nachgemeldet. Soll ich ausführen?

**Nur bei ausdrücklichem Ja:**

```bash
python3 notifications/schliess_benachrichtigung.py
echo "Rückgabewert: $?"
```

Erwartet:
- Rückgabewert **0**
- Log-Zeile `Erstlauf: N bestehende Trades als erledigt vermerkt, keine Nachmeldung. Bestaetigung gesendet.`
- **Auf dem iPhone genau EINE Telegram-Nachricht:**

```
✅ *Schliess-Benachrichtigung aktiv*
N bereits geschlossene Trades wurden als erledigt vermerkt und werden NICHT nachgemeldet.
Ab jetzt kommt je geschlossenem Trade eine Nachricht.
```

**Kommen mehr als eine Nachricht, sofort melden.** Das wäre der Fall, den der
Erstlauf-Modus verhindern soll.

## Danach: prüfen, dass er nicht wieder greift

```bash
python3 notifications/schliess_benachrichtigung.py --status
```

Erwartet: `Erstlauf: bereits erfolgt am JJJJ-MM-TT HH:MM:SS`, und
`erstlauf_uebersprungen` zeigt `N`.

```bash
python3 notifications/schliess_benachrichtigung.py
echo "Rückgabewert: $?"
```

Erwartet: Rückgabewert 0, Log `0 Meldung(en) gesendet (einzeln).`, und **keine**
weitere Telegram-Nachricht.

---

## Schritt 6 — Der erste echte Lauf im Betrieb

Jetzt geht es darum, dass eine **echte** Schließung ankommt. Das braucht
Geduld: der schnellste Bot (`elliott_wave`) läuft stündlich und schließt nur,
wenn ein Ausstieg fällig ist.

**Ohne warten** lässt sich prüfen, dass das Skript im Leerlauf richtig
reagiert:

```bash
python3 notifications/schliess_benachrichtigung.py --status | tail -3
```

Erwartet: `Noch nicht gemeldet: 0`, solange nichts Neues geschlossen wurde.

**Mit warten:** sobald ein Bot einen Trade schließt, muss innerhalb von 15
Minuten (nach Einrichtung des Cronjobs, Schritt 7) eine Nachricht kommen. Bis
dahin von Hand:

```bash
python3 notifications/schliess_benachrichtigung.py
```

Prüfen, wenn eine Nachricht kam:
- [ ] Bot-Name ist der verständliche, nicht der Ordnername
- [ ] Prozent mit Vorzeichen
- [ ] Ein- und Ausstiegskurs plausibel (mit `/positions` bzw. dem Dashboard vergleichen)
- [ ] Haltedauer plausibel
- [ ] Grund als Satz, nicht `stop_loss`
- [ ] **kein zweiter Push** vom Telegram-Dienst zum selben Trade — das ist die
      Prüfung, dass die alte Meldung wirklich weg ist

---

## Schritt 7 — Cronjob eintragen (optional, Entscheidung des Nutzers)

```bash
crontab -l > ~/crontab-sicherung-$(date +%Y%m%d).txt
EDITOR=nano crontab -e
```

Zeile anhängen — den Pfad zu `python3` vollständig, Cron hat ein anderes
`PATH`:

```cron
*/15 * * * * cd ~/trading-bot && /usr/bin/python3 notifications/schliess_benachrichtigung.py >> logs/notifications/schliess_benachrichtigung.log 2>&1
```

```bash
crontab -l | grep schliess_benachrichtigung    # steht der Eintrag?
which python3                                   # stimmt der Pfad?
```

Nach 15–30 Minuten:

```bash
tail -20 logs/notifications/schliess_benachrichtigung.log
```

Erwartet: Zeilen `0 Meldung(en) gesendet (einzeln).` im Leerlauf.

**Wieder abschalten:** `EDITOR=nano crontab -e`, Zeile mit `#` auskommentieren.
Wartende Meldungen bleiben dann stehen und kommen, sobald er wieder läuft.

---

## Schritt 8 — Urzustand und Abgrenzung

```bash
git status --short     # muss LEER sein (die .db ist gitignored)
```

Ist hier etwas zu sehen, hat eine Mutationsprobe nicht zurückgeschrieben:
`git checkout -- <datei>` und melden.

```bash
git diff origin/main HEAD --name-only
```

Erwartet, genau diese vier Dateien (plus die Dokumente unter `docs/`):

```
notifications/README.md
notifications/monitor.py
notifications/schliess_benachrichtigung.py
notifications/test_schliess_benachrichtigung.py
```

```bash
git diff origin/main HEAD --name-only \
  | grep -E "live_params|forward_test|equity_simulation|crontab|\.plist|^broker/|^strategies/|^dashboard/"
```

Erwartet: **keine Ausgabe**. `broker/bot_db.py` wird benutzt, nicht verändert.

Und der Nachweis, dass die Bot-Datenbanken unberührt sind — der steht in der
Suite selbst (Abschnitt 7: byteweise gleich, `mode=ro` verweigert aktiv), aber
zur Sicherheit auch hier:

```bash
python3 notifications/test_schliess_benachrichtigung.py 2>&1 | sed -n '/7\. Bot-Datenbank/,/^8\./p'
```

---

## Was zu melden ist

Ein kurzer Bericht: Schritt-Nummer, erwartet, tatsächlich. Grüne Schritte in
einer Zeile zusammenfassen genügt.

**Zu Schritt 5 bitte ausdrücklich sagen**, ob er ausgeführt wurde, mit welcher
Zahl `N`, und ob genau eine Nachricht ankam. Wurde er nicht ausgeführt, das
klar als offen benennen — die Schritte 6 und 7 setzen ihn voraus.
