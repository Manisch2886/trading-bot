# Testauftrag: Positionsanzahl je Bot + Notbremse zu Beginn

**Für eine lokale Claude-Code-Sitzung.** Dieses Dokument ist so gebaut, dass es
**ohne Rückfragen** abgearbeitet werden kann: jeder Schritt nennt den Befehl,
die Erwartung und — wo es darauf ankommt — die Gegenprobe.

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `main`.

> **Nichts an diesem Auftrag verändert Handelsparameter, Trades oder
> Datenbanken.** Alle Schritte laufen gegen Wegwerf-Verzeichnisse bzw. reine
> Textprüfungen. Die einzigen Schreibvorgänge sind die Mutationsproben in
> Schritt 5 — sie stellen den Urzustand selbst wieder her und werden in
> Schritt 6 gegengeprüft.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short            # muss LEER sein, sonst erst aufräumen
git rev-parse --abbrev-ref HEAD
pip3 install -r requirements.txt
node --version
```

Erwartet:
* `git status --short` gibt nichts aus
* Branch ist `claude/new-session-uqjk8h`
* `node` ist vorhanden (ohne Node laufen die Verhaltenstests nicht, und
  `test_dashboard.py` überspringt sie stillschweigend)

*Hinweis:* `dashboard/test_dashboard.py` braucht seit PR #71
`pandas_market_calendars`. Fehlt es, schlägt die Suite **auch auf `main`**
fehl — das wäre kein Befund dieses Auftrags. `broker/test_ibkr.py` prüft
32 Zusicherungen zusätzlich, wenn `ib_async` installiert ist
(`pip3 install ib_async`); ohne das Paket überspringt sie diesen Block
absichtlich.

---

## Schritt 1 — Alle Suiten, unverändert grün

```bash
python3 broker/test_broker.py      | tail -2
python3 broker/test_ibkr.py        | tail -2
python3 dashboard/test_dashboard.py | tail -2
node dashboard/test_gewichtung.js  | tail -1
```

| Suite | Erwartet | Auf `main` war es |
|---|---|---|
| `broker/test_broker.py` | `163 von 163` | 149 |
| `broker/test_ibkr.py` | `200 von 200` mit `ib_async`, `168 von 168` ohne | 186 / 154 |
| `dashboard/test_dashboard.py` | `753/753` | 738 |
| `dashboard/test_gewichtung.js` | `35/35` | 27 |

**Kein bestehender Test wurde geändert** — jede Zahl oben ist die alte plus
die neuen Prüfungen. Nachweisbar, und zwar hart:

```bash
git fetch origin main
git diff origin/main HEAD -- broker/test_broker.py broker/test_ibkr.py \
                             dashboard/test_dashboard.py \
                             dashboard/test_gewichtung.js \
  | grep -c '^-[^-]'
```

Erwartet: **`0`**. Keine einzige Zeile wurde aus einer Testdatei entfernt —
alle Änderungen dort sind Hinzufügungen. Eine höhere Zahl heißt, dass eine
bestehende Zusicherung abgeschwächt wurde, und ist ein Befund.

*(`main` lokal kann veraltet sein; deshalb überall `origin/main` als Basis.)*

Zusätzlich die übrigen Suiten, die nichts mit dieser Änderung zu tun haben und
das auch belegen sollen:

```bash
python3 notifications/test_manual_close.py | tail -1
python3 shared/test_empfehlung_format.py   | tail -1
python3 system/test_caffeinate_plist.py    | tail -2
node dashboard/test_zustandsmaschine.js    | tail -1
node dashboard/test_zeitzone.js            | tail -1
```

Erwartet: alle grün (`118`, `70/70`, `52 von 52`, `27/27`, `24/24`).

---

## Schritt 2 — Teil 1: die Anzeige, wirklich erzeugt

Nicht die Quelltextsuche ist der Test, sondern die **erzeugte Ausgabe**. So
sieht sie aus:

```bash
node -e '
const fs=require("fs"),path=require("path"),vm=require("vm");
const s=path.join("dashboard","static");
const app=fs.readFileSync(path.join(s,"app.js"),"utf8");
function f(q,k){const a=q.indexOf(k);return q.slice(a,q.indexOf("\n}",a)+2);}
const ctx={};
vm.runInNewContext([f(app,"function zahl("),f(app,"function prozent("),
 app.match(/const GEWICHTUNG_ERLAEUTERUNG =[\s\S]*?;\n/)[0],
 f(app,"function positionsgroesse("),
 app.match(/const POSITIONSANZAHL_ERLAEUTERUNG =[\s\S]*?;\n/)[0],
 f(app,"function positionsanzahlZeilen("),f(app,"function gewichtungsZeilen("),
 "this.g=gewichtungsZeilen;"].join("\n"),ctx);
console.log(ctx.g({wert_pct:-8.05,ungewichtet_schnitt_pct:-7.4,anzahl:8,
 gewichte:[{bot:"elliott_wave",anzeigename:"Elliott Wave (Krypto)",allokation_pct:5.0,anzahl:7},
           {bot:"turtle_soup_stocks",anzeigename:"Turtle Soup (Aktien)",allokation_pct:2.0,anzahl:1}],
 nicht_gewichtbar:[]}).join("\n")
 .replace(/<[^>]+>/g,"").replace(/&nbsp;/g," "));'
```

Erwartet, drei Zeilen:

```
Ø gewichtet-8.05%  (Positionsgröße 5 % / 2 %; dieselben Positionen ungewichtet -7.40%)
Gewichtet nach der je Bot im Backtest angenommenen Positionsgröße – keine echte Kapitalbindung und keine Portfolio-Rendite.
Eingegangene Positionen je Bot – Elliott Wave (Krypto): 7; Turtle Soup (Aktien): 1. Bots ohne Obergrenze für gleichzeitige Positionen können die gewichtete Zahl allein tragen.
```

Zu prüfen ist genau das, was die Aufgabe verlangt:

1. Die dritte Zeile steht **da** — die gewichtete Zahl −8,05 % wird
   ersichtlich von einem Bot getragen (7 von 8 Positionen).
2. Sie ist **sichtbarer Text**, kein `title`-Tooltip: im Rohausgang steht
   `class="hinweis-gewichtung"` und nirgends `title="Eingegangene`.
3. Die **Gewichtungsformel ist unberührt**: −8,05 % ist weiterhin
   (5·(−8,5…) + 2·(−1)) / (5·7 + 2·1) und nicht etwa ein Mittel über Bots.

```bash
git diff origin/main HEAD -- dashboard/schliessen.py | wc -l   # erwartet: 0
```

Die Anzeige kommt ohne jede Backend-Änderung aus — `gewichte[].anzahl` gab es
schon, es wird nur ausgewiesen.

---

## Schritt 3 — Teil 1: **je Funktion**, nicht im ganzen Dokument

Das ist die Fehlerklasse, die in PR #62, #66 und #67 dreimal aufgetreten ist:
eine Suche über die ganze Datei bleibt grün, solange **eine** der beiden
Ansichten den Text noch enthält.

```bash
python3 dashboard/test_dashboard.py 2>&1 | grep -E "Uebersicht|Ergebnis (bot-weit|global)|EINMAL, in app.js|title-Tooltip"
```

Erwartet: fünf Ansichten, jede einzeln geprüft, alle `[OK ]`:

| Ansicht | Weg | Datei |
|---|---|---|
| `gewichtungsZeilen` | Übersicht bot-weit **und** global | `app.js` |
| `notfallZeilen` | Übersicht bot-weit (`alle-schliessen`) | `bot.html` |
| `notfallErgebnisAnzeigen` | Ergebnis bot-weit | `bot.html` |
| `crashListe` | Übersicht global (`alle-bots-schliessen`) | `index.html` |
| `crashErgebnisAnzeigen` | Ergebnis global | `index.html` |

`notfallErgebnisAnzeigen()` baut sein HTML **selbst** auf und ruft
`gewichtungsZeilen()` nicht auf. Wäre die Anzahl nur dort eingehängt, bliebe
genau diese Ansicht ohne sie — deshalb prüft der Test das ausdrücklich mit.

---

## Schritt 4 — Teil 2: Notbremse

```bash
python3 broker/test_broker.py 2>&1 | sed -n '/11\. Notbremse/,/^12\./p' | grep -E "OK |FEHLER"
python3 broker/test_ibkr.py   2>&1 | sed -n '/11\. Bot-Datenbank/,/^12\./p' | grep -E "OK |FEHLER"
```

Erwartet, je Brücke (`broker/STOP` bzw. `broker/STOP_IBKR`):

* **Bei NULL offenen Aufgaben** erscheint eine sichtbare Zeile `NOTBREMSE
  aktiv (…)`, sie nennt den Pfad der Datei und sagt, dass der Lauf beendet
  wird.
* **Testnet bzw. TWS werden gar nicht erst kontaktiert** (Binance:
  `boerse.anfragen` ist leer; IBKR: `z["konto"] is None`, weil ohne
  Verbindungsaufbau kein Konto zu melden ist).
* **Rückgabewert 0** bei gezogener Bremse ohne offene Aufgabe, **1** mit
  offener Aufgabe (Begründung siehe Übergabe-Zusammenfassung).
* **Ohne Bremse steht die Zeile nicht da** — sie ist keine Deko.
* Offene Aufgaben stehen mit Grund in der Nachverfolgung, statt spurlos zu
  verschwinden.
* **Die Prüfung je Aufgabe greift weiterhin**, mit einer *echt mitten im Lauf*
  angelegten Datei geprüft: die erste Order ist draußen, die zweite wird
  gestoppt — und zwar von der mittleren Ebene, nicht von der untersten.

Zu dem letzten Punkt, weil er sonst leicht falsch gelesen wird: es gibt
**drei** Ebenen, die die Bremse prüfen.

| Ebene | Wo | Greift wann |
|---|---|---|
| 1 (**neu**) | `lauf(echt=True)`, zu Beginn | Bremse lag schon vor dem Lauf |
| 2 (unverändert) | `spiegle_eine()`, je Aufgabe | Bremse wird **mitten im Lauf** gezogen |
| 3 (unverändert) | `binance_testnet.marktorder()` / `ibkr_paper.marktorder()` | letzte Rückfallebene |

Ebene 3 verdeckt Ebene 2 in einem naiven Test: nimmt man Ebene 2 heraus,
bleibt trotzdem jede Order aus. Der Test unterscheidet deshalb **wie oft die
Verbindung überhaupt gefragt wurde** und ob der Grund der Wortlaut von Ebene 2
ist. Die Gegenprobe dazu ist M7 bzw. M12 in Schritt 5.

Und die Ansage, wie sie im Betrieb aussieht:

```bash
python3 broker/test_broker.py 2>&1 | grep "Offene Aufgaben: 0"
```

Erwartet:

```
NOTBREMSE aktiv (/tmp/broker_test_…/STOP) - dieser Lauf wird sofort beendet,
ohne das Testnet auch nur zu kontaktieren. Offene Aufgaben: 0. Datei
entfernen gibt den Weg wieder frei.
```

---

## Schritt 5 — Mutationsproben

Eine Prüfung, die eine kaputte Fassung nicht rot macht, prüft nichts. Dieses
Skript baut je Mutation **einen** Fehler ein, lässt die zugehörige Suite laufen
und stellt die Datei danach byteweise wieder her.

```bash
cat > /tmp/mutation_pr.py <<'PYEOF'
import subprocess, os
WURZEL = os.path.expanduser("~/trading-bot")
M = [
 ("M1  Anzahl-Zeile aus gewichtungsZeilen() entfernt", "dashboard/static/app.js",
  "  zeilen.push(...positionsanzahlZeilen(g));", "  /* entfernt */",
  ["node", "dashboard/test_gewichtung.js"]),
 ("M2  Anzahl-Zeile aus notfallErgebnisAnzeigen() entfernt", "dashboard/static/bot.html",
  '  html += positionsanzahlZeilen(g).join("");', "  /* entfernt */",
  ["node", "dashboard/test_gewichtung.js"]),
 ("M3  positionsanzahlZeilen() liefert immer nichts", "dashboard/static/app.js",
  "  if (!g || !Array.isArray(g.gewichte) || !g.gewichte.length) return [];",
  "  return [];", ["node", "dashboard/test_gewichtung.js"]),
 ("M4  Anzahl als title-Tooltip statt sichtbarer Zeile", "dashboard/static/app.js",
  '  return [`<div class="hinweis-gewichtung">Eingegangene Positionen je Bot – `',
  '  return [`<div title="Eingegangene Positionen je Bot"><span>`',
  ["python3", "dashboard/test_dashboard.py"]),
 ("M5  fehlende Anzahl wirft statt Strich", "dashboard/static/app.js",
  '    const wieviele = (w && w.anzahl !== null && w.anzahl !== undefined)\n      ? w.anzahl : "–";',
  "    const wieviele = w.anzahl.toFixed(0);", ["node", "dashboard/test_gewichtung.js"]),
 ("M6  Binance: Pruefung zu Beginn entfernt", "broker/spiegel.py",
  "        notbremse = echt and zugang.notbremse_aktiv()", "        notbremse = False",
  ["python3", "broker/test_broker.py"]),
 ("M7  Binance: Pruefung JE AUFGABE entfernt", "broker/spiegel.py",
  '    if zugang.notbremse_aktiv():\n        grund = notbremse_grund()\n        logger.warning(f"{grund}. Unerledigt: {kopf}")',
  '    if False:\n        grund = notbremse_grund()\n        logger.warning(f"{grund}. Unerledigt: {kopf}")',
  ["python3", "broker/test_broker.py"]),
 ("M8  Binance: Notbremse gilt als Fehlschlag (Cron-Fehlalarm)", "broker/spiegel.py",
  '    return 1 if z["fehlgeschlagen"] else 0\n\n\nif __name__',
  '    return 1 if z["fehlgeschlagen"] or z.get("notbremse") else 0\n\n\nif __name__',
  ["python3", "broker/test_broker.py"]),
 ("M9  Binance: offene Aufgaben verschwinden aus der Nachverfolgung", "broker/spiegel.py",
  '                notiere_versuch(conn, bot, aufgabe["trade_id"], aufgabe["seite"],\n                                aufgabe["symbol"], "echt", "fehlgeschlagen",\n                                grund)',
  "                pass", ["python3", "broker/test_broker.py"]),
 ("M10 Binance: keine sichtbare Meldung, nur stiller Abbruch", "broker/spiegel.py",
  '            logger.warning(\n                f"NOTBREMSE aktiv ({zugang.NOTBREMSE_DATEI}) - dieser Lauf "',
  '            logger.debug(\n                f"nichts ({zugang.NOTBREMSE_DATEI}) - dieser Lauf "',
  ["python3", "broker/test_broker.py"]),
 ("M11 IBKR: Pruefung zu Beginn entfernt", "broker/ibkr_spiegel.py",
  "        notbremse = echt and zugang.notbremse_aktiv()", "        notbremse = False",
  ["python3", "broker/test_ibkr.py"]),
 ("M12 IBKR: Pruefung JE AUFGABE entfernt", "broker/ibkr_spiegel.py",
  '    if zugang.notbremse_aktiv():\n        grund = notbremse_grund()\n        logger.warning(f"{grund}. Unerledigt: {kopf}")',
  '    if False:\n        grund = notbremse_grund()\n        logger.warning(f"{grund}. Unerledigt: {kopf}")',
  ["python3", "broker/test_ibkr.py"]),
 ("M13 IBKR: Notbremse gilt als Fehlschlag (Cron-Fehlalarm)", "broker/ibkr_spiegel.py",
  '    return 1 if z["fehlgeschlagen"] else 0\n\n\nif __name__',
  '    return 1 if z["fehlgeschlagen"] or z.get("notbremse") else 0\n\n\nif __name__',
  ["python3", "broker/test_ibkr.py"]),
]
for name, datei, alt, neu, befehl in M:
    pfad = os.path.join(WURZEL, datei)
    urtext = open(pfad, encoding="utf-8").read()
    if urtext.count(alt) != 1:
        print(f"[SETUP-FEHLER] {name}: {urtext.count(alt)} Fundstellen")
        continue
    open(pfad, "w", encoding="utf-8").write(urtext.replace(alt, neu, 1))
    try:
        lauf = subprocess.run(befehl, cwd=WURZEL, capture_output=True, text=True)
        erste = [z for z in lauf.stdout.splitlines() if "[FEHLER]" in z][:1]
        print(f"[{'ERKANNT' if lauf.returncode else 'UNENTDECKT'}] {name}")
        if erste:
            print(f"      -> {erste[0].strip()[:130]}")
    finally:
        open(pfad, "w", encoding="utf-8").write(urtext)
PYEOF
python3 /tmp/mutation_pr.py
```

**Erwartet: 13 von 13 `[ERKANNT]`.** Ein einziges `[UNENTDECKT]` ist ein
Befund und gehört gemeldet — es hieße, die zugehörige Zusicherung ist nicht
wirklich abgesichert.

Was jede Probe belegt:

| Probe | Belegt |
|---|---|
| M1, M3 | Die Anzahl kommt wirklich aus der Anzeige, nicht nur aus dem Quelltext |
| M2 | Die Ergebnisanzeige des bot-weiten Wegs ist mit abgedeckt (die dreimal vergessene Stelle) |
| M4 | Sie ist sichtbare Zeile, kein Tooltip |
| M5 | Eine fehlende Angabe blockiert den Notfallweg nicht |
| M6, M11 | Die neue Prüfung zu Beginn wird wirklich geprüft |
| M7, M12 | Die alte Prüfung je Aufgabe wird wirklich geprüft — und zwar *sie*, nicht die unterste Ebene |
| M8, M13 | Der Rückgabewert 0 ist eine geprüfte Entscheidung, kein Zufall |
| M9 | Offene Aufgaben verschwinden nicht aus der Nachverfolgung |
| M10 | Die Meldung ist sichtbar (WARNING), nicht in DEBUG versteckt |

---

## Schritt 6 — Urzustand

```bash
git status --short          # muss wieder LEER sein
```

Ist hier etwas zu sehen, hat eine Mutationsprobe nicht sauber
zurückgeschrieben: `git checkout -- <datei>` und den Befund melden.

Danach die Suiten noch einmal, als Abschluss:

```bash
python3 broker/test_broker.py       | tail -2
python3 broker/test_ibkr.py         | tail -2
python3 dashboard/test_dashboard.py | tail -2
```

---

## Schritt 7 — Was NICHT angefasst sein darf

```bash
git diff origin/main HEAD --name-only
```

Erwartet, genau diese zehn Dateien:

```
broker/README.md
broker/README_IBKR.md
broker/ibkr_spiegel.py
broker/spiegel.py
broker/test_broker.py
broker/test_ibkr.py
dashboard/static/app.js
dashboard/static/bot.html
dashboard/test_dashboard.py
dashboard/test_gewichtung.js
```

(plus die drei Dokumente unter `docs/`.)

Gegenprobe, dass die Sperrliste der Aufgabe eingehalten ist:

```bash
git diff origin/main HEAD --name-only \
  | grep -E "live_params|forward_test|equity_simulation|crontab|launchd|\.plist"
```

Erwartet: **keine Ausgabe**. Ebenso unberührt: das Schema der `trades`-Tabelle
(`git diff origin/main HEAD -- strategies/` ist leer) und `dashboard/schliessen.py`.

---

## Was zu melden ist

Ein kurzer Bericht mit: Schritt-Nummer, erwartet, tatsächlich — und bei jedem
Abweichler die vollständige Ausgabe der betroffenen Prüfung. Grüne Schritte in
einer Zeile zusammenfassen genügt.
