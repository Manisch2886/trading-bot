# Ergebnis — Handelszeiten im Dashboard

**PR #77** · Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`445fbf2`, nach Merge von #76).

## Das Problem

Seit #71 wird außerhalb der Handelszeiten vorgemerkt statt geschlossen — der
Nutzer erfuhr das aber erst **im Bestätigungsdialog**. Die NYSE öffnet in
Berlin erst um 15:30; den halben Tag über war jeder „Schließen"-Knopf auf den
Aktien-Bots in Wahrheit ein „Vormerken"-Knopf.

---

## Teil A — Statuszeile

Auf **beiden** Seiten, weit oben, in der Zeitzone des Geräts:

```
NYSE geöffnet – schließt Donnerstag, 22:00 Uhr
NYSE geschlossen – öffnet Freitag, 15:30 Uhr
NYSE geschlossen (Wochenende) – öffnet Montag, 15:30 Uhr
NYSE geschlossen (Feiertag) – öffnet Freitag, 15:30 Uhr  [verkürzter Handelstag]
NYSE geöffnet – schließt Freitag, 19:00 Uhr              [verkürzter Handelstag]
Börsenstatus unbekannt – der Kalender gibt gerade keine Auskunft. …
```

Krypto-Bot-Seite: **keine Zeile**, dort ändert sich nichts.

**Halbtag** kommt direkt aus dem Kalender. Bei offener Börse meint das Feld den
laufenden Tag, bei geschlossener den nächsten — beides ist im Text
berücksichtigt.

**Feiertag** wird abgeleitet, ohne zweite Kalenderquelle: liegt zwischen
Handelsschluss und nächster Öffnung ein **Werktag** ohne Sitzung, war das ein
Feiertag. Gerechnet in UTC-Daten, weil eine NYSE-Sitzung nie eine
UTC-Datumsgrenze überschreitet — auf Berliner Zeit umgerechnet läge ein
Handelsschluss je nach Jahreszeit nach Mitternacht und der Wochentag wäre um
einen daneben.

## Teil B — Knopfbeschriftungen

| Weg | Börse offen | Börse zu |
|---|---|---|
| Einzelposition | `Schließen` | `Vormerken` *(war schon da)* |
| bot-weit | `⚠ Notfall: alle 2 Positionen schließen` | `⚠ Notfall: alle 2 Positionen zur Börsenöffnung vormerken` |
| global (Crash) | `⚠ ALLE 12 Positionen in 5 Bots schließen` | `⚠ 7 Krypto sofort schließen · 5 Aktien vormerken` |

### Die zu begründende Wahl: der Crash-Knopf

Er trifft als einziger beide Welten. **Gewählt: getrennte Zahlen je Bereich.**

Verworfen:
- **„ALLE 12 schließen bzw. vormerken"** — eine Zahl für zwei Vorgänge. Wer sie
  liest, weiß hinterher nicht, wie viele Positionen nach dem Tap noch offen
  sind, und genau das ist im Crash-Fall die Frage.
- **Nur den Hinweis darunter erweitern** — das war der Zustand vorher. Der
  Hinweis wird im Ernstfall nicht gelesen, der Knopftext schon.

Randfälle: ist nur **eine** Welt betroffen, steht auch nur eine Zahl da.
Stimmt die Aufteilung nicht mit der Gesamtzahl überein, bleibt der bisherige,
sicher richtige Text.

---

## Architektur

- **Der Kalender wird benutzt, nicht nachgebaut.** `/api/portfolio` liefert
  `schliessen.boersenlage("aktien")` mit — dieselbe Funktion, an der auch das
  Schließen hängt. Eine Prüfung schlägt fehl, wenn `app.py` daran vorbeigreift.
- **Krypto/Aktien werden an EINER Stelle unterschieden** (`kalender_gilt`),
  nicht je Ansicht.
- **Darstellungslogik einmal in `app.js`**, wie `gewichtungsZeilen()` und
  `positionsanzahlZeilen()`.
- **Sichtbarer Text, kein `title`-Tooltip** — am iPhone gibt es kein Hover.
- **Auto-Refresh:** Statuszeile *und* Knopftext laufen im 60-s-Takt mit; der
  Übergang geschlossen → offen springt ohne Neuladen um.

**Keine Sperre.** Der Knopf bleibt außerhalb der Handelszeiten bedienbar, der
Warteauftrag entsteht wie bisher. Eine Prüfung hält das fest.

---

## Tests

| Suite | vorher | nachher |
|---|---|---|
| `dashboard/test_dashboard.py` | 753 | **784 / 784** ✅ |
| `dashboard/test_boersenstatus.js` *(neu)* | – | **53 / 53** ✅ |
| `dashboard/test_gewichtung.js` | 35 | 35 / 35 ✅ |
| `dashboard/test_zeitzone.js` | 24 | 24 / 24 ✅ |
| `dashboard/test_zustandsmaschine.js` | 27 | 27 / 27 ✅ |
| `broker/test_broker.py` | 163 | 163 ✅ |
| `broker/test_ibkr.py` | 200 / 168 | 200 ✅ |
| `notifications/test_manual_close.py` | – | alle ✅ |
| `shared/test_empfehlung_format.py` | 70 | 70 ✅ |
| `system/test_caffeinate_plist.py` | 52 | 52 ✅ |

Keine bestehende Zusicherung abgeschwächt: `git diff origin/main HEAD --
dashboard/test_dashboard.py | grep -c '^-[^-]'` → **0**.

**Je Funktion geprüft**, acht Einhängepunkte einzeln (die Fehlerklasse aus
#62/#66/#67/#73). **Erzeugte Ausgabe** für sieben Lagen, darunter Thanksgiving
*und* Karfreitag.

**Zeitzonen-Gegenprobe:** derselbe Test in `TZ=America/New_York` zeigt
`16:00 Uhr` statt `22:00 Uhr` — die Umrechnung findet wirklich statt.

**Mit echt entfernter Abhängigkeit geprüft** (Import-Blocker, nicht
deinstalliert): ohne `pandas_market_calendars` antwortet `/api/portfolio`
weiter mit HTTP 200, die Bot-Liste ist vollständig, die Lage wird als
*unbekannt benannt* statt behauptet, Krypto bleibt handelbar.

> Einordnung: für **Aktien** lehnt #71 das Schließen bei unbekanntem Kalender
> ausdrücklich ab (fail closed) — bestehende Entscheidung, nicht angetastet.
> „Nicht blockiert" heißt: **die Anzeige** ist nie die Ursache.

**12 Mutationsproben, 12 erkannt.** Eine (M6, `wirdVorgemerkt` ohne
`kalender_gilt`) ging zuerst durch — die Zusicherung fehlte und wurde
nachgeschärft: entschieden wird an `kalender_gilt`, nicht am Folgefeld.

---

## 👁 Was noch am iPhone anzusehen ist

Automatisiert ist, **was der Code erzeugt** — nicht, wie es aussieht. Drei
Punkte stehen als eigener Schritt 7 im Testauftrag:

1. **Platz der Statuszeile** — kollidiert sie mit dem Ladeindikator, drückt sie
   die Kacheln zu weit nach unten?
2. **Der längere Crash-Knopftext** — bricht er auf 390 px um statt
   überzulaufen, und fällt der Umbruch nicht zwischen Zahl und Wort?
3. **Die Farbe der „geschlossen"-Zeile** — Bernstein, nicht Rot. Liest sich das
   als Hinweis oder als Fehler? Eine Beurteilung, keine Messung.

Dazu die eine Prüfung, die den Aufwand lohnt: Dashboard **kurz vor 15:30**
öffnen, liegen lassen — innerhalb einer Minute müssen Statuszeile **und**
Knopfbeschriftung von selbst umspringen.

---

## Geänderte Dateien

```
dashboard/app.py                  (+ Börsenlage in /api/portfolio)
dashboard/static/app.js           (+ die gesamte Darstellungslogik)
dashboard/static/bot.html         (+ Zeile, Notfallknopf, gemeinsame Quelle)
dashboard/static/index.html       (+ Zeile, Crash-Knopf)
dashboard/static/style.css        (+ .boersenstatus)
dashboard/test_dashboard.py       (+ Abschnitt 16b und 17)
dashboard/test_boersenstatus.js   (neu)
```

Nicht angefasst: keine `live_params.py`, keine `forward_test.py`, keine
`equity_simulation.py`, kein `trades`-Schema, keine Crontab, keine
launchd-Vorlage, nichts unter `broker/` — und nichts aus der #71-Logik
(`boersenkalender.py`, `warteauftraege.py`, `schliessen.py`,
`warteauftraege_ausfuehren.py`), die nur **gelesen** wurde.
