# Testauftrag: Portfolio-Sicht im Dashboard

**Für eine lokale Claude-Code-Sitzung auf dem Mac.** Ablegeort neben
`TESTANLEITUNG_SCHLIESSEN.md`, weil dasselbe Verzeichnis betroffen ist.

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`d5be46e`, nach Merge von #79), **PR #80**.

> ## Was diese Sitzung darf
>
> **Alle Schritte laufen ohne Rückfragen durch.** Diese Änderung fasst keine
> Bot-Datenbank an: der einzige neue schreibende Endpunkt schreibt
> ausschliesslich seinen eigenen Zwischenspeicher
> (`results/portfolio_overview/dashboard_snapshot.json`).
>
> **Nicht anfassen:** Crontab, launchd-Vorlagen, `broker/`, `strategies/`,
> `live_params.py`, `forward_test.py`, `equity_simulation.py`,
> `shared/portfolio_overview.py`. Kein `--echt` irgendwo. Keine Zugangsdaten in
> Ausgaben übernehmen.
>
> **Die Dashboard-Adresse ist `http://100.106.38.8:8787`** (Tailscale), nicht
> `localhost`. Das Token steht in der laufenden Konfiguration; in dieser
> Anleitung steht es bewusst nirgends.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short              # muss LEER sein
git rev-parse --abbrev-ref HEAD
python3 --version
command -v node || echo "node fehlt"
```

**Wenn `node` fehlt, bitte zuerst installieren** (`brew install node`). Ohne
`node` überspringt `test_portfolio_sicht.py` **67 Frontend-Prüfungen** — und
genau die prüfen die Quellenkennzeichnung in der Ausgabe. Der Test sagt das
dann ausdrücklich; ein Lauf ohne `node` ist kein grünes Ergebnis, sondern ein
unvollständiges. Dasselbe gilt für `test_dashboard.py`: ohne `node` meldet es
**780/780** statt 784, und das sieht grün aus, obwohl 143 Zusicherungen nicht
gelaufen sind.

---

## Schritt 1 — Selbsttests

```bash
python3 dashboard/test_portfolio_sicht.py | tail -3
python3 dashboard/test_portfolio_anzeige.js 2>/dev/null || node dashboard/test_portfolio_anzeige.js | tail -2
python3 dashboard/test_dashboard.py | tail -1
```

| Suite | Erwartet |
|---|---|
| `dashboard/test_portfolio_sicht.py` | **90 von 90** (mit `node`) |
| `dashboard/test_portfolio_anzeige.js` | **67 von 67** |
| `dashboard/test_dashboard.py` | **784/784** (780 ohne `node`) |

Abschnitt 9 des ersten Tests startet das echte
`shared/portfolio_overview.py` — das dauert je nach Datenlage eine Weile und
ist kein Hänger. Er darf die Arbeitskopie **nicht** verändern:

```bash
git status --short        # nach dem Testlauf wieder LEER
```

Ist sie nicht leer, ist das ein Befund.

---

## Schritt 2 — Die Rechnung auf der Kommandozeile

```bash
python3 dashboard/portfolio_sicht.py
```

Beim ersten Mal erwartet: „Noch nicht berechnet."

```bash
time python3 dashboard/portfolio_sicht.py --berechnen
```

**Bitte die Zeit notieren.** In der Cloud-Sitzung wurden 2,9 s für sieben Bots
auf dem Live-Weg gemessen, 134 ms wenn alle auf der Backtest-Kurve liegen. Auf
dem Mac sind die echten Live-Datenbanken dabei — weicht die Zeit stark ab
(etwa über 15 s), gehört das gemeldet, weil davon die Entscheidung
„Zwischenspeicher statt direkt rechnen" abhängt.

Erwartete Ausgabe: je Bot eine Zeile mit `live` oder `backtest`, dann zwei
Gruppen. **Bitte vollständig zurückmelden** — das ist die echte Datenlage, die
ich hier nicht sehen kann.

```bash
python3 dashboard/portfolio_sicht.py      # zeigt jetzt den Stand mit Alter
ls -l results/portfolio_overview/dashboard_snapshot.json
git status --short                        # LEER: der Stand ist in .gitignore
```

---

## Schritt 3 — Die Zahlen gegen die Quelle prüfen

Die Portfolio-Sicht darf nicht anders rechnen als die Montags-Mail.

```bash
python3 shared/portfolio_overview.py 2>&1 | grep -E "Vergleichsfenster|Rendite im Fenster|Max Drawdown kombiniert"
python3 -c "
import json
d = json.load(open('results/portfolio_overview/dashboard_snapshot.json'))
for name, g in d['gruppen'].items():
    if g['moeglich']:
        print(f\"{name:20} {g['von']} bis {g['bis']}  Rendite {g['rendite_pct']:+.2f} %  DD {g['max_drawdown_pct']:.2f} %\")
    else:
        print(f\"{name:20} keine Zahl: {g['grund']}\")
"
```

**Erwartet:** die Werte der Gruppe `alle` stimmen mit dem ersten
„LIVE-PORTFOLIO"-Block der Originalausgabe überein (Rendite, Drawdown,
Fenster).

> **Achtung, das ist die Stelle mit der Wortfalle:** die Gruppe, die das
> Original „LIVE-PORTFOLIO" nennt, meint *Bots mit `live_params.py`* — also
> alle neun. Die Entsprechung ist deshalb `alle`, **nicht**
> `nur_echte_trades`. Genau deshalb heisst die Gruppe im Dashboard anders.

Hinweis: `shared/portfolio_overview.py` schreibt beim direkten Aufruf seine
Kurven-CSVs neu. Danach:

```bash
git status --short results/    # ggf. mit: git checkout -- results/
```

---

## Schritt 4 — Die Seite im Browser

```bash
open "http://100.106.38.8:8787/"        # oder am iPhone öffnen
```

1. Auf der **Übersichtsseite**: der Link „→ Portfolio-Sicht" steht **unterhalb**
   des Crash-Bereichs, direkt über der Bot-Tabelle. **Der Crash-Knopf darf
   nicht nach unten gerutscht sein.**
2. Link antippen. Die Seite `/portfolio` zeigt: Stand mit Alter, offene
   Positionen, zwei Gruppenblöcke, dann die Bot-Tabelle.

**Bitte diese fünf Punkte einzeln bestätigen:**

| # | Zu prüfen |
|---|---|
| 1 | **Jeder** Bot in der Tabelle trägt eine Quellenmarke — keine leere Zelle |
| 2 | Bots unter der Schwelle zeigen `Backtest (N von 10)`, nicht nur „Backtest" |
| 3 | **Jeder** Gruppenblock hat einen Satz darunter, woraus er besteht |
| 4 | Die Backtest-Gruppe sagt wörtlich „das ist keine erzielte Rendite" |
| 5 | Der Zeitpunkt steht als `TT.MM., HH:MM` — **nicht** als „Sat Sep 12 2026 … GMT" |

Punkt 5 ist eine echte Regression aus der Entwicklung dieser Änderung; er ist
durch einen Test abgesichert, aber am Gerät sieht man es unmittelbar.

3. **„Neu berechnen"** antippen. Erwartet: der Knopf wird kurz inaktiv, danach
   steht „gerade eben" im Stand. Rechenzeit vergleichen mit Schritt 2.

---

## Schritt 5 — Der Notfallweg (der wichtigste Schritt)

Die Portfolio-Sicht darf den Crash-Weg unter keinen Umständen behindern.

```bash
# Wie lange braucht die Übersichtsseite? Vorher und nachher gleich schnell.
time curl -s -o /dev/null "http://100.106.38.8:8787/api/portfolio" -H "X-Dashboard-Token: $TOKEN"
```

Dann im Browser: **`/portfolio` in einem Tab, „Neu berechnen" antippen und
während die Rechnung läuft** in einem zweiten Tab die Übersichtsseite laden.

**Erwartet:** die Übersicht lädt normal schnell und der Crash-Knopf ist
bedienbar, *während* die Portfolio-Rechnung läuft. Hängt die Übersicht, ist das
der schwerste mögliche Befund dieses Auftrags — bitte melden und nicht
weitermachen.

Zusätzlich: den Zwischenspeicher unlesbar machen und prüfen, dass nur die
Portfolio-Seite betroffen ist.

```bash
cp results/portfolio_overview/dashboard_snapshot.json /tmp/snapshot_sicherung.json
echo "{kaputt" > results/portfolio_overview/dashboard_snapshot.json
```

Übersichtsseite neu laden → muss normal funktionieren.
`/portfolio` neu laden → muss „Noch nicht berechnet" zeigen, **nicht** abstürzen.

```bash
cp /tmp/snapshot_sicherung.json results/portfolio_overview/dashboard_snapshot.json
```

---

## Schritt 6 — iPhone, 390 px

Am Gerät, nicht im Simulator:

| # | Zu prüfen |
|---|---|
| 1 | Die drei Kennzahlen je Gruppe **brechen um**, statt seitlich zu scrollen |
| 2 | Die Bot-Tabelle ist lesbar; die Quellenmarke bricht nicht mitten im Wort |
| 3 | Die Marken sind auch ohne Farbwahrnehmung unterscheidbar (jede trägt ihren Text) |
| 4 | Der „Neu berechnen"-Knopf ist mit dem Daumen erreichbar |
| 5 | Der Zurück-Pfeil oben links führt zur Übersicht |

---

## Schritt 7 — Mutationsproben

Baut 22 plausible Fehler ein und prüft, dass der Selbsttest jeden erkennt. Der
Urzustand wird in jedem Fall wiederhergestellt. Dauer: je nach Rechner
20–40 Minuten, weil jede Mutation die ganze Suite laufen lässt.

Das Skript liegt bewusst nicht im Repo — es verändert vorübergehend
Quelldateien. Hier vollständig zum Herauskopieren:

```bash
cat > /tmp/mut_portfolio.py <<'PY'
"""Mutationsproben der Portfolio-Sicht. Jede muss vom Selbsttest erkannt
werden - sonst ist die Zusicherung nur behauptet."""
import subprocess, sys

TEST = "dashboard/test_portfolio_sicht.py"
PY = "dashboard/portfolio_sicht.py"
JS = "dashboard/static/app.js"
APP = "dashboard/app.py"

MUTATIONEN = [
    (PY, "M1  Bots ohne Kurve fallen stillschweigend weg",
     '    zeilen = []\n    for name in sorted(bots):',
     '    zeilen = []\n    for name in sorted(curves):'),

    (PY, "M2  Gruppe 'nur echte Trades' enthaelt doch alle Bots",
     '    aus_echten_trades = {n: d for n, d in curves.items()\n'
     '                         if bots[n].get("using_live_data")}',
     '    aus_echten_trades = dict(curves)'),

    (PY, "M3  enthaelt_backtest immer False",
     '        gruppe["enthaelt_backtest"] = bool(\n'
     '            [n for n in gruppe.get("bots", []) if not bots[n].get("using_live_data")])',
     '        gruppe["enthaelt_backtest"] = False'),

    (PY, "M4  gemeinsames Fenster als Vereinigung statt Schnittmenge",
     '    beginn = max(d["series"].index.min() for d in curves.values())\n'
     '    ende = min(d["series"].index.max() for d in curves.values())',
     '    beginn = min(d["series"].index.min() for d in curves.values())\n'
     '    ende = max(d["series"].index.max() for d in curves.values())'),

    (PY, "M5  Quelle 'live' schon unter der Schwelle",
     '        elif quellen.get("using_live_data"):',
     '        elif True:'),

    (PY, "M6  sicht() rechnet selbst, wenn kein Stand da ist",
     '    daten, alter = lese_snapshot()\n    if daten is None:\n        return {"vorhanden": False,',
     '    daten, alter = lese_snapshot()\n    if daten is None:\n        berechne()\n        return {"vorhanden": False,'),

    (PY, "M7  keine Sperre - zwei Rechnungen gleichzeitig",
     '    _sperre_nehmen()\n    try:\n        daten = berechne()',
     '    try:\n        daten = berechne()'),

    (PY, "M8  Zwischenspeicher wird direkt geschrieben, nicht atomar",
     '    neben = SNAPSHOT_DATEI + ".neu"\n'
     '    with open(neben, "w", encoding="utf-8") as datei:',
     '    neben = SNAPSHOT_DATEI\n'
     '    with open(neben, "w", encoding="utf-8") as datei:'),

    (PY, "M9  Arbeitsordner nicht umgelenkt - Kollision mit der Montags-Mail",
     '    po.RESULTS_DIR = ARBEITSORDNER          # siehe Modulkopf: Kollisionsschutz',
     '    pass                                    # Umlenkung entfernt'),

    (PY, "M10 veraltet wird nie gemeldet",
     '            "veraltet": alter > MAX_ALTER_SEKUNDEN,',
     '            "veraltet": False,'),

    (PY, "M11 fehlt_bis_schwelle wird nicht mitgeliefert",
     '            "fehlt_bis_schwelle": (max(po.MIN_LIVE_CLOSED_TRADES - anzahl, 0)\n'
     '                                   if quelle == QUELLE_BACKTEST else None),',
     '            "fehlt_bis_schwelle": None,'),

    (PY, "M12 pandas auf Modulebene - ein fehlendes Paket nimmt das Dashboard mit",
     'import argparse\nimport json',
     'import argparse\nimport pandas\nimport json'),

    (PY, "M13 der Hinweis 'in KEINER Summe' verschwindet",
     '            quelle_text = ("keine verwertbare Kurve - dieser Bot ist in KEINER "\n'
     '                           "der Summen unten enthalten")',
     '            quelle_text = "keine Kurve"'),

    (JS, "M14 Quellenmarke ohne Trade-Zahlen",
     '  if (bot.quelle === "live") {\n'
     '    text += ` (${bot.geschlossene_trades})`;\n'
     '  } else if (bot.quelle === "backtest") {\n'
     '    text += ` (${bot.geschlossene_trades} von ${schwelle})`;\n'
     '  }',
     '  /* mutiert */'),

    (JS, "M15 unbekannte Quelle faellt auf 'live' zurueck",
     '  const art = PORTFOLIO_QUELLEN[bot.quelle] || PORTFOLIO_QUELLEN.fehlt;',
     '  const art = PORTFOLIO_QUELLEN[bot.quelle] || PORTFOLIO_QUELLEN.live;'),

    (JS, "M16 Gruppenblock ohne Herkunftssatz",
     '    <p class="portfolio-herkunft">${herkunft}</p>',
     '    '),

    (JS, "M17 Backtest-Gruppe sagt nicht, dass es keine erzielte Rendite ist",
     '       ? "Enthält Bots, deren Kurve aus dem <strong>Backtest</strong> stammt – das ist keine erzielte Rendite."',
     '       ? "Mehrere Bots."'),

    (JS, "M18 fehlende Bots werden in der Gesamtansicht nicht gemeldet",
     '  const fehlenderHinweis = fehlend.length\n'
     '    ? `<p class="warnzeile">⚠ ${fehlend.length} Bot(s) sind in KEINER Summe unten enthalten:',
     '  const fehlenderHinweis = false\n'
     '    ? `<p class="warnzeile">⚠ ${fehlend.length} Bot(s) sind in KEINER Summe unten enthalten:'),

    (JS, "M19 Zeitpunkt als rohes Date-Objekt (der Fehler der ersten Fassung)",
     '  return `<p class="portfolio-stand">Berechnet ${zeit(stand.daten.berechnet_am)}',
     '  return `<p class="portfolio-stand">Berechnet ${zeitpunkt(stand.daten.berechnet_am)}'),

    (JS, "M20 fehlender Beitrag wird als 0 dargestellt",
     '  const beitrag = bot.beitrag_pp === null || bot.beitrag_pp === undefined\n'
     '    ? \'<span class="gedaempft">–</span>\'\n'
     '    : prozent(bot.beitrag_pp);',
     '  const beitrag = prozent(bot.beitrag_pp || 0);'),

    (APP, "M21 Fehlschlag der Rechnung wird als Erfolg gemeldet",
     '            raise HTTPException(status_code=503,\n'
     '                                detail=f"Berechnung fehlgeschlagen: {fehler}")',
     '            return {"berechnet": False}'),

    (APP, "M22 laufende Rechnung ergibt 500 statt 409",
     '            raise HTTPException(status_code=409, detail=str(fehler))\n'
     '        except Exception as fehler:                            # noqa: BLE001\n'
     '            logger.exception("Portfolio-Sicht konnte nicht berechnet werden")',
     '            raise HTTPException(status_code=500, detail=str(fehler))\n'
     '        except Exception as fehler:                            # noqa: BLE001\n'
     '            logger.exception("Portfolio-Sicht konnte nicht berechnet werden")'),
]


def main():
    urzustand = {d: open(d, encoding="utf-8").read() for d in (PY, JS, APP)}
    erkannt, entgangen = [], []
    try:
        for datei, name, alt, neu in MUTATIONEN:
            if urzustand[datei].count(alt) != 1:
                entgangen.append(f"{name} (Vorlage {urzustand[datei].count(alt)}x)")
                print(f"[?        ] {name}: Vorlage nicht eindeutig")
                continue
            open(datei, "w", encoding="utf-8").write(urzustand[datei].replace(alt, neu))
            lauf = subprocess.run([sys.executable, TEST], capture_output=True,
                                  text=True, timeout=1800)
            open(datei, "w", encoding="utf-8").write(urzustand[datei])
            if lauf.returncode != 0:
                erkannt.append(name)
                print(f"[erkannt  ] {name}")
                for z in [z for z in lauf.stdout.splitlines() if "[FEHLER]" in z][:2]:
                    print(f"            {z.strip()[:150]}")
            else:
                entgangen.append(name)
                print(f"[ENTGANGEN] {name}")
    finally:
        for datei, inhalt in urzustand.items():
            open(datei, "w", encoding="utf-8").write(inhalt)

    print(f"\n{len(erkannt)} von {len(MUTATIONEN)} Mutationen erkannt.")
    for n in entgangen:
        print(f"  NICHT erkannt: {n}")
    return 1 if entgangen else 0


if __name__ == "__main__":
    sys.exit(main())
PY
python3 /tmp/mut_portfolio.py
git status --short              # muss wieder LEER sein
```

Erwartet: **22 von 22 erkannt**, danach `git status --short` wieder leer.

Die Proben M1, M13 und M18 prüfen den Befund „ein Bot kann lautlos
verschwinden", M14 bis M17 die Quellenkennzeichnung in der Ausgabe, M19 das
Datumsformat und M6 bis M9 den Zwischenspeicher samt Sperre.

Entgeht eine Mutation, ist das die wichtigste Rückmeldung dieses Auftrags.

---

## Schritt 8 — Keine Regression

```bash
python3 dashboard/test_dashboard.py           | tail -1
python3 notifications/test_schliess_benachrichtigung.py | tail -2
python3 system/test_log_rotation.py           | tail -2
python3 broker/test_broker.py                 | tail -1
python3 broker/test_ibkr.py                   | tail -1
python3 shared/test_empfehlung_format.py      | tail -1
python3 system/test_caffeinate_plist.py       | tail -1
python3 notifications/test_manual_close.py    | tail -1
```

| Suite | Erwartet |
|---|---|
| `dashboard/test_dashboard.py` | 784/784 (780 ohne `node`) |
| `notifications/test_schliess_benachrichtigung.py` | 99 von 99 |
| `system/test_log_rotation.py` | 117 von 117 |
| `broker/test_broker.py` | 163 von 163 |
| `broker/test_ibkr.py` | 200 von 200 (168 ohne `ib_async`) |
| `shared/test_empfehlung_format.py` | 70/70 |
| `system/test_caffeinate_plist.py` | 52 von 52 |
| `notifications/test_manual_close.py` | alle bestanden |

---

## Rückmeldung

1. Zahlen aus Schritt 1 (erwartet 90/90, 67/67, 784/784) und Schritt 7 (22/22).
2. **Aus Schritt 2: die vollständige Ausgabe von `--berechnen`** samt
   gemessener Zeit. Das ist die echte Datenlage — wie viele Bots stehen auf
   `live`, wie viele auf `backtest`?
3. Aus Schritt 3: ob die drei Werte mit dem Original übereinstimmen.
4. Aus Schritt 4: die fünf Punkte einzeln, besonders Punkt 5 (Datumsformat).
5. **Aus Schritt 5: ob die Übersichtsseite während einer laufenden Rechnung
   normal lädt.** Die wichtigste Einzelaussage des Auftrags.
6. Aus Schritt 6: die fünf iPhone-Punkte.
7. Jede entgangene Mutation, wörtlich.
