# Testauftrag: Handelszeiten im Dashboard

**Für eine lokale Claude-Code-Sitzung auf dem Mac.** Die Schritte 0–6 laufen
**ohne Rückfragen** durch. Schritt 7 ist eine **Sichtprüfung am iPhone** und
kann nicht automatisiert werden — er ist ausdrücklich als solcher markiert.

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`445fbf2`), PR #77.

> **Nichts an diesem Auftrag verändert Handelsparameter, Trades oder
> Datenbanken.** Die Selbsttests laufen gegen ein Wegwerf-Projekt unter
> `/tmp`. Die einzigen Schreibvorgänge sind die Mutationsproben in Schritt 5
> und der Import-Blocker in Schritt 4 — beide stellen den Urzustand selbst
> wieder her und werden in Schritt 6 gegengeprüft.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short            # muss LEER sein
git rev-parse --abbrev-ref HEAD
pip3 install -r requirements.txt
node --version
```

Erwartet: kein Ausgabetext bei `git status`, Branch
`claude/new-session-uqjk8h`, `node` vorhanden.

*Ohne `node`* überspringt `test_dashboard.py` die Verhaltenstests **still** —
dann ist die halbe Zusicherung dieses PRs ungeprüft. `node --version` ist
deshalb kein Formalismus.

---

## Schritt 1 — Alle Suiten

```bash
python3 dashboard/test_dashboard.py | tail -1
node dashboard/test_boersenstatus.js | tail -1
node dashboard/test_gewichtung.js    | tail -1
node dashboard/test_zeitzone.js      | tail -1
node dashboard/test_zustandsmaschine.js | tail -1
python3 broker/test_broker.py | tail -1
python3 broker/test_ibkr.py   | tail -1
python3 notifications/test_manual_close.py | tail -1
python3 shared/test_empfehlung_format.py   | tail -1
python3 system/test_caffeinate_plist.py    | tail -1
```

| Suite | Erwartet | auf `main` |
|---|---|---|
| `dashboard/test_dashboard.py` | **784/784** | 753 |
| `dashboard/test_boersenstatus.js` | **53/53** | *(neu)* |
| `dashboard/test_gewichtung.js` | 35/35 | 35 |
| `dashboard/test_zeitzone.js` | 24/24 | 24 |
| `dashboard/test_zustandsmaschine.js` | 27/27 | 27 |
| `broker/test_broker.py` | 163 von 163 | 163 |
| `broker/test_ibkr.py` | 200 von 200 (bzw. 168 ohne `ib_async`) | 200 / 168 |
| `notifications/test_manual_close.py` | alle bestanden | — |
| `shared/test_empfehlung_format.py` | 70/70 | 70 |
| `system/test_caffeinate_plist.py` | 52 von 52 | 52 |

Dass keine bestehende Zusicherung abgeschwächt wurde:

```bash
git fetch origin main
git diff origin/main HEAD -- dashboard/test_dashboard.py | grep -c '^-[^-]'
```

Erwartet: **`0`**. Jede Änderung an der bestehenden Testdatei ist eine
Hinzufügung. Eine höhere Zahl ist ein Befund.

---

## Schritt 2 — Die Statuszeile, wirklich erzeugt

Nicht die Quelltextsuche ist der Test, sondern die **Ausgabe**:

```bash
node dashboard/test_boersenstatus.js
```

Erwartet, Abschnitt 1 — sieben Lagen, jede mit ihrem Satz:

```
NYSE geöffnet – schließt Donnerstag, 22:00 Uhr
NYSE geschlossen – öffnet Freitag, 15:30 Uhr
NYSE geschlossen (Wochenende) – öffnet Montag, 15:30 Uhr
NYSE geschlossen (Feiertag) – öffnet Freitag, 15:30 Uhr   verkürzter Handelstag
NYSE geöffnet – schließt Freitag, 19:00 Uhr               verkürzter Handelstag
Börsenstatus unbekannt – …
(Krypto: gar keine Zeile)
```

Worauf es dabei ankommt:

1. **Feiertag steht als solcher da**, nicht bloß „geschlossen" — geprüft an
   Thanksgiving (beweglich) **und** Karfreitag (osterabhängig).
2. **Wochenende wird davon unterschieden.** Die Rechnung dahinter
   (`werktageDazwischen`) wird in Abschnitt 1 einzeln an vier Fällen mit
   bekannter Antwort geprüft.
3. **Halbtag erscheint in beiden Richtungen** — bei offener Börse für den
   laufenden Tag, bei geschlossener für den nächsten.
4. **Zeiten in Gerätezeit.** 15:30 Berlin = 9:30 New York, 22:00 = 16:00.
   Steht dort 13:30 oder 20:00, kommt die Zeit in UTC durch — Befund.

Gegenprobe, dass die Zeiten wirklich umgerechnet werden:

```bash
TZ=America/New_York node dashboard/test_boersenstatus.js | grep "NYSE geöffnet – schließt"
```

Erwartet: dort steht **16:00 Uhr** statt 22:00 — dieselbe ISO-Angabe, andere
Zeitzone. Kommt beide Male dieselbe Uhrzeit, wird nicht umgerechnet.

---

## Schritt 3 — Beide Ansichten, je Funktion

Die Fehlerklasse aus PR #62, #66, #67 und #73: eine Suche über das ganze
Dokument bleibt grün, solange **eine** der beiden Ansichten die Angabe zeigt.

```bash
python3 dashboard/test_dashboard.py 2>&1 | sed -n '/16b) Boersenstatus/,/^17)/p' | grep -E "OK |FEHLER"
```

Erwartet, alle `[OK ]` — acht Einhängepunkte einzeln:

| Ansicht | Funktion | muss enthalten |
|---|---|---|
| `index.html` | `zeichneBoersenstatus` | `boersenstatusZeile(` |
| `index.html` | `zeichneUebersicht` | `zeichneBoersenstatus(` |
| `index.html` | `zeichneUebersicht` | `crashKnopfText(` |
| `bot.html` | `zeichneBoersenstatus` | `boersenstatusZeile(` |
| `bot.html` | `ladeSchliessInfo` | `zeichneBoersenstatus(` |
| `bot.html` | `positionsZeile` | `boerseGeschlossen(` |
| `bot.html` | `zeichnePositionen` | `boerseGeschlossen(` |
| `bot.html` | `boerseGeschlossen` | `wirdVorgemerkt(` |

Dazu in derselben Ausgabe:

* **Die Darstellungslogik steht EINMAL, in `app.js`** — nicht in `bot.html`,
  nicht in `index.html`.
* **Krypto wird an EINER Stelle unterschieden** (`kalender_gilt`), nicht je
  Ansicht.
* **Der Endpunkt liest `schliessen.boersenlage()`** und baut nichts nach.
* **Der Knopf wird NICHT gesperrt** — das ist die Entscheidung aus PR #71 und
  sie steht hier unter Test.

Und die Knopftexte, erzeugt (Abschnitt 3 des Node-Tests):

```
Börse zu:    ⚠ Notfall: alle 2 Positionen zur Börsenöffnung vormerken
Börse offen: ⚠ Notfall: alle 2 Positionen schließen
Krypto:      ⚠ Notfall: alle 2 Positionen schließen   (unverändert)
```

---

## Schritt 4 — Der Notfallweg darf nie blockiert werden

**Mit echt entfernter Abhängigkeit, nicht behauptet.** Dieses Skript blockiert
`pandas_market_calendars` wirklich beim Import und fasst nichts an der
Installation an:

```bash
mkdir -p /tmp/ohne_kalender
cat > /tmp/ohne_kalender/sitecustomize.py <<'PYEOF'
import sys
class _Blocker:
    def find_module(self, name, path=None):
        return self if name.split(".")[0] == "pandas_market_calendars" else None
    def load_module(self, name):
        raise ImportError(f"blockiert fuer die Gegenprobe: {name}")
sys.meta_path.insert(0, _Blocker())
PYEOF

cat > /tmp/probe_ohne_kalender.py <<'PYEOF'
import os, sys
W = os.path.expanduser("~/trading-bot")
sys.path[:0] = [os.path.join(W, "dashboard"), os.path.join(W, "notifications"), W]
os.chdir(W)
try:
    import pandas_market_calendars
    print("[SETUP-FEHLER] Paket ist doch importierbar"); sys.exit(2)
except ImportError as e:
    print(f"[OK ] Das Paket ist wirklich blockiert: {e}")
import boersenkalender, schliessen
z = boersenkalender.status()
print(f"[{'OK ' if z['offen'] is None else 'FEHLER'}] status() wirft nicht, offen={z['offen']}")
a, k = schliessen.boersenlage("aktien"), schliessen.boersenlage("krypto")
print(f"[{'OK ' if a['unbekannt'] else 'FEHLER'}] Aktien-Lage: unbekannt=True")
print(f"[{'OK ' if k['handelbar_jetzt'] and not k['kalender_gilt'] else 'FEHLER'}]"
      f" KRYPTO bleibt handelbar - der Notfallweg dort ist unberuehrt")
from app import erzeuge_app
from fastapi.testclient import TestClient
os.environ.setdefault("DASHBOARD_ACCESS_TOKEN", "probe-token-0123456789")
import konfig; konfig.ACCESS_TOKEN = os.environ["DASHBOARD_ACCESS_TOKEN"]
klient = TestClient(erzeuge_app())
klient.post("/login", data={"token": konfig.ACCESS_TOKEN}, follow_redirects=False)
antwort = klient.get("/api/portfolio")
print(f"[{'OK ' if antwort.status_code == 200 else 'FEHLER'}] /api/portfolio "
      f"antwortet trotzdem: HTTP {antwort.status_code}")
d = antwort.json(); b = d.get("boerse") or {}
print(f"[{'OK ' if b.get('unbekannt') else 'FEHLER'}] und benennt die Lage als unbekannt")
print(f"[{'OK ' if d.get('bots') is not None else 'FEHLER'}] Die Bot-Liste ist vollstaendig da")
PYEOF

PYTHONPATH=/tmp/ohne_kalender python3 /tmp/probe_ohne_kalender.py
```

Erwartet: **sieben Zeilen, alle `[OK ]`.** Ein einziges `[FEHLER]` ist ein
Befund.

> **Richtig lesen:** Für **Aktien**-Bots lehnt PR #71 das Schließen bei
> unbekanntem Kalender ausdrücklich ab (fail closed) — bestehende, bewusste
> Entscheidung, hier nicht angetastet. „Nicht blockiert" heißt: **die Anzeige**
> ist nie die Ursache. Die Seite rendert, die Liste ist vollständig, Krypto
> bleibt schließbar.

Und in der Anzeige selbst (Abschnitt 1 des Node-Tests, läuft in Schritt 2 mit):

```
[OK ] Fehlende oder kaputte Angaben werfen NICHT - die Anzeige blockiert nie
[OK ] Ohne Angabe bleibt die Zeile leer statt falsch
[OK ] Und ohne Angabe wird NICHT vorgemerkt - der Knopf bleibt "Schließen"
```

---

## Schritt 5 — Mutationsproben

Eine Prüfung, die eine kaputte Fassung nicht rot macht, prüft nichts.

```bash
cat > /tmp/mutation_boerse.py <<'PYEOF'
import subprocess, os
W = os.path.expanduser("~/trading-bot")
NODE = ["node", "dashboard/test_boersenstatus.js"]
PY_T = ["python3", "dashboard/test_dashboard.py"]
M = [
 ("M1  Statuszeile liefert immer nichts", "dashboard/static/app.js",
  "  const lage = boersenLage(b);\n  if (lage === \"krypto\") return \"\";",
  "  const lage = boersenLage(b);\n  return \"\";", NODE),
 ("M2  index.html zeichnet die Zeile nicht mehr", "dashboard/static/index.html",
  "  letzteBoerse = daten.boerse || null;\n  zeichneBoersenstatus();",
  "  letzteBoerse = daten.boerse || null;", NODE),
 ("M3  bot.html zeichnet die Zeile nicht im Datentakt", "dashboard/static/bot.html",
  "  zeichneBoersenstatus();\n  zeichnePositionen();\n}",
  "  zeichnePositionen();\n}", PY_T),
 ("M4  bot-weiter Notfallknopf ignoriert die Lage", "dashboard/static/bot.html",
  "    document.getElementById(\"alle-schliessen\").textContent = boerseGeschlossen()\n      ? `⚠ Notfall: alle ${offen} Positionen zur Börsenöffnung vormerken`\n      : `⚠ Notfall: alle ${offen} Positionen schließen`;",
  "    document.getElementById(\"alle-schliessen\").textContent =\n      `⚠ Notfall: alle ${offen} Positionen schließen`;", NODE),
 ("M5  Crash-Knopf ignoriert die Lage", "dashboard/static/app.js",
  "  if (!wirdVorgemerkt(boerse)) return unveraendert;", "  return unveraendert;", NODE),
 ("M6  wirdVorgemerkt beachtet Krypto nicht mehr", "dashboard/static/app.js",
  "  return !!(boerse && boerse.kalender_gilt && boerse.warteauftrag_noetig);",
  "  return !!(boerse && boerse.warteauftrag_noetig);", NODE),
 ("M7  Feiertag nicht mehr vom Wochenende unterschieden", "dashboard/static/app.js",
  "    if (wochentag !== 0 && wochentag !== 6) werktage += 1;",
  "    if (false) werktage += 1;", NODE),
 ("M8  Halbtag wird nicht mehr ausgewiesen", "dashboard/static/app.js",
  "  const kurz = b.verkuerzter_handelstag\n    ? ' <span class=\"boersenstatus-marke\">verkürzter Handelstag</span>' : \"\";\n  return `<div class=\"boersenstatus zu\">",
  "  const kurz = \"\";\n  return `<div class=\"boersenstatus zu\">", NODE),
 ("M9  Statuszeile als title-Tooltip statt sichtbarem Text", "dashboard/static/app.js",
  "    return `<div class=\"boersenstatus offen\"><strong>${boersenname} geöffnet</strong>`",
  "    return `<div title=\"${boersenname} geöffnet\"><span>`", PY_T),
 ("M10 /api/portfolio liefert die Lage nicht mehr mit", "dashboard/app.py",
  "            uebersicht[\"boerse\"] = _boersenlage_aktien()\n            return uebersicht",
  "            return uebersicht", PY_T),
 ("M11 Statuszeile wirft bei fehlender Angabe", "dashboard/static/app.js",
  "function boersenstatusZeile(boerse) {\n  const b = boerse || {};",
  "function boersenstatusZeile(boerse) {\n  const b = boerse; b.kalender_gilt;", NODE),
 ("M12 Endpunkt baut die Lage selbst nach", "dashboard/app.py",
  "            return schliessen.boersenlage(\"aktien\")",
  "            return {\"anlageklasse\": \"aktien\", \"kalender_gilt\": True,\n                    \"offen\": True, \"unbekannt\": False, \"kalender\": \"XXX\",\n                    \"warteauftrag_noetig\": False, \"naechster_schluss\": None,\n                    \"naechste_oeffnung\": None, \"letzter_schluss\": None,\n                    \"letzter_handelstag\": None, \"verkuerzter_handelstag\": None}",
  PY_T),
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
python3 /tmp/mutation_boerse.py
```

**Erwartet: 12 von 12 `[ERKANNT]`.** Läuft ein paar Minuten (mehrere Mutationen
starten die volle Dashboard-Suite). Ein einziges `[UNENTDECKT]` ist ein Befund.

| Probe | Belegt |
|---|---|
| M1, M2, M3 | Die Zeile kommt wirklich in der Ausgabe an — in beiden Ansichten, und sie läuft im Takt mit |
| M4, M5 | Die Knopftexte hängen wirklich an der Lage |
| M6 | Krypto wird an `kalender_gilt` erkannt, nicht am Folgefeld *(ging in der ersten Fassung durch — die Zusicherung fehlte)* |
| M7, M8 | Feiertag und Halbtag werden wirklich unterschieden bzw. ausgewiesen |
| M9 | Sichtbare Zeile, kein Tooltip |
| M10, M12 | Der Endpunkt liefert die Lage, und zwar aus `boersenlage()` |
| M11 | Eine fehlende Angabe blockiert nichts |

---

## Schritt 6 — Urzustand

```bash
git status --short          # muss wieder LEER sein
python3 dashboard/test_dashboard.py | tail -1     # 784/784
node dashboard/test_boersenstatus.js | tail -1    # 53/53
```

Ist hier etwas zu sehen, hat eine Mutationsprobe nicht sauber
zurückgeschrieben: `git checkout -- <datei>` und den Befund melden.

Und was nicht angefasst sein darf:

```bash
git diff origin/main HEAD --name-only
```

Erwartet, genau diese sieben Dateien (plus die Dokumente unter `docs/`):

```
dashboard/app.py
dashboard/static/app.js
dashboard/static/bot.html
dashboard/static/index.html
dashboard/static/style.css
dashboard/test_boersenstatus.js
dashboard/test_dashboard.py
```

```bash
git diff origin/main HEAD --name-only \
  | grep -E "live_params|forward_test|equity_simulation|crontab|\.plist|^broker/|^strategies/|boersenkalender|warteauftraege|schliessen\.py"
```

Erwartet: **keine Ausgabe**. Insbesondere ist die Logik aus PR #71
(`boersenkalender.py`, `warteauftraege.py`, `schliessen.py`,
`warteauftraege_ausfuehren.py`) nur **gelesen** worden.

---

## Schritt 7 — 👁 SICHTPRÜFUNG AM iPHONE (nicht automatisierbar)

**Dieser Schritt lässt sich nicht abarbeiten, sondern nur anschauen.** Was der
Code *erzeugt*, ist in den Schritten 1–5 vollständig geprüft; wie es *aussieht*,
zeigt nur das Gerät. Dashboard am iPhone öffnen (PWA oder Safari).

Am aussagekräftigsten ist der Zeitpunkt: **vormittags** ist die NYSE
geschlossen, **ab 15:30** offen. Wer beides sehen will, schaut zweimal —
oder einmal um etwa 15:28 und lässt die Seite offen liegen.

### 7.1 Die Statuszeile

- [ ] Sie ist **ohne Scrollen** zu sehen, auf der Übersicht **und** auf einer
      Bot-Seite.
- [ ] Sie kollidiert nicht mit dem **Ladeindikator** in der Kopfzeile und
      drückt die Kacheln nicht unangenehm weit nach unten.
- [ ] Der Text **bricht um** statt überzulaufen — die längste Fassung ist
      `NYSE geschlossen (Feiertag) – öffnet Freitag, 15:30 Uhr` plus die Marke
      `verkürzter Handelstag`.
- [ ] Die Marke `verkürzter Handelstag` bleibt als Ganzes zusammen
      (`white-space: nowrap`), rutscht aber nicht aus dem Bild.
- [ ] **Die Farbe:** „geschlossen" trägt Bernstein, nicht Rot. Liest sich das
      als Hinweis — oder wirkt es wie ein Fehler? Das ist eine Beurteilung,
      keine Messung, und der Punkt, an dem dein Urteil gefragt ist.
- [ ] Auf einer **Krypto**-Bot-Seite (z. B. `t3_supertrend`) steht **gar keine**
      Zeile. Kein leerer Kasten, kein Abstand.

### 7.2 Die Knöpfe

Bei **geschlossener** Börse, auf einem Aktien-Bot (z. B.
`volatility_breakout`):

- [ ] Der Knopf in der Positionszeile heißt **„Vormerken"**.
- [ ] Der Notfallknopf darunter heißt **„⚠ Notfall: alle N Positionen zur
      Börsenöffnung vormerken"** — und der längere Text **bricht sauber um**.
- [ ] Auf der Übersicht heißt der Crash-Knopf **„⚠ N Krypto sofort schließen ·
      M Aktien vormerken"**. Der Mittelpunkt `·` sollte als Trennung lesbar
      sein, nicht als Schmutz.
- [ ] Der Umbruch fällt **nicht zwischen Zahl und Wort** („5\nAktien").

Bei **offener** Börse (ab 15:30):

- [ ] Alle drei Knöpfe sagen wieder **„schließen"**.

### 7.3 Der Übergang, ohne Neuladen

Das ist die Zusicherung, die am schwersten zu glauben und am leichtesten zu
prüfen ist:

- [ ] Dashboard **kurz vor 15:30** öffnen, Statuszeile zeigt „geschlossen",
      Knöpfe sagen „vormerken".
- [ ] Seite **offen liegen lassen** (Bildschirm an, App im Vordergrund).
- [ ] **Innerhalb einer Minute nach 15:30** müssen Statuszeile **und**
      Knopfbeschriftung von selbst umspringen — ohne Nachladen, ohne Wischen.

Springt nur eines von beiden um, ist das ein Befund.

### 7.4 Was NICHT passieren darf

- [ ] Der Knopf ist zu **keinem** Zeitpunkt gesperrt oder ausgegraut. Außerhalb
      der Handelszeiten entsteht wie bisher ein Warteauftrag — eine Sperre wäre
      eine Rücknahme von PR #71.

---

## Was zu melden ist

Ein kurzer Bericht: Schritt-Nummer, erwartet, tatsächlich. Grüne Schritte in
einer Zeile zusammenfassen genügt. Bei jedem Abweichler die vollständige
Ausgabe der betroffenen Prüfung.

**Für Schritt 7 bitte ausdrücklich sagen, ob er durchgeführt wurde** — und
wenn nicht, dass er offen ist. Er ist der einzige Teil dieses PRs, für den es
keinen automatischen Nachweis gibt.
