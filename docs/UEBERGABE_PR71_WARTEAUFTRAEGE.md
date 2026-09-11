# Übergabe: Warteaufträge für Aktien-Positionen (PR #71)

**Für die Review-Session.** Dieses Dokument fasst zusammen, was gebaut wurde,
warum es so gebaut wurde, was geprüft ist und was der Nutzer noch entscheiden
muss. Es ist so geschrieben, dass eine Sitzung ohne Vorwissen damit arbeiten
kann.

| | |
|---|---|
| **Pull Request** | https://github.com/Manisch2886/trading-bot/pull/71 |
| **Branch** | `claude/admiring-turing-74tohm` (von `main` nach Merge von PR #68) |
| **Commit** | `640cc55` |
| **Status** | offen, **nicht gemergt** — bewusst zurückgehalten bis zum Durchlauf der Testanleitung |
| **Stand** | 2026-09-11 |
| **Vorgeschichte** | PR #66 hatte den Befund aufgedeckt, aber nicht behoben |

---

## 1. Der Anlass

Bei den vier Aktien-Bots erschien der Schließen-Knopf auch außerhalb der
Börsenzeiten. Er schloss dann zum **letzten verfügbaren Tages-Schlusskurs**
aus yfinance — also zu einem Kurs, den es „gerade jetzt" gar nicht gibt: über
ein Wochenende zweieinhalb Tage alt, über Ostern vier.

Im Quelltext stand dazu seit PR #66 ausdrücklich, eine Handelszeiten-Sperre
sei „bewusst NICHT eingebaut", weil Zeitzonen, Feiertage und Halbtage eigene
Fallstricke wären. **Der Befund war richtig, die Folgerung nicht.** Die drei
Fallstricke sind nicht verschwunden — sie sind jetzt der Grund, warum die
Entscheidung an einem echten Börsenkalender hängt statt an einer Zeitregel.

## 2. Was jetzt passiert

| Lage | Verhalten |
|---|---|
| Krypto-Bot, immer | sofort schließen, aktueller Kurs — **unverändert** |
| Aktien-Bot, Börse offen | sofort schließen, aktueller Kurs — **unverändert** |
| Aktien-Bot, Börse geschlossen | **Warteauftrag** nach zusätzlicher Bestätigung; Ausführung bei der nächsten Öffnung |
| Aktien-Bot, Kalender nicht lesbar | **weder noch** — abgelehnt mit Begründung |

Ein Warteauftrag ist eine gespeicherte **Absicht**, kein Ergebnis: er nennt
Bot, Position, Symbol, Zeitpunkt und Quelle, aber ausdrücklich **keinen Kurs**
— den gibt es noch nicht.

## 3. ⚠️ Die neue Eigenschaft — bitte vor allem anderen lesen

**Dies ist der erste Schreibvorgang des Projekts ohne gleichzeitige
menschliche Bestätigung.**

Bisher galt ausnahmslos: ein Mensch bestätigt, und *daraufhin* wird
geschrieben. Ein Warteauftrag trennt beides.

| | bisher | mit Warteaufträgen |
|---|---|---|
| Wer löst den Schreibzugriff aus | ein Mensch, jetzt | ein Cronjob, später |
| Bestätigung im Moment des Schreibens | ja | **nein** |
| Ausstiegskurs beim Bestätigen bekannt | ja | **nein** |
| Zeit dazwischen | Sekunden | Stunden bis Tage |
| Abbruch | Dialog schließen | **Stornieren**, solange der Auftrag wartet |

Wer den Cronjob einrichtet, erteilt damit eine **Vorab-Erlaubnis für alle
künftigen Warteaufträge**, nicht für einen einzelnen. Eine Eröffnungslücke am
Montag trifft den Auftrag voll. Das ist der Preis dafür, zu einem **echten**
Kurs zu schließen statt zu einem veralteten.

**Ohne den Cronjob passiert nichts.** Aufträge werden angelegt, im Dashboard
angezeigt und nie ausgeführt — ein bewusst möglicher Zwischenschritt.

## 4. Was geändert wurde

### Neue Dateien

| Datei | Zweck |
|---|---|
| `notifications/boersenkalender.py` | echter NYSE-Kalender; beantwortet genau eine Frage, kennt weder Bots noch Positionen |
| `notifications/warteauftraege.py` | persistente Auftragsverwaltung: anlegen, auflisten, stornieren, abschließen |
| `dashboard/warteauftraege_ausfuehren.py` | eigenständiges Programm für den Cronjob — das einzige, das zeitversetzt schreibt |
| `dashboard/pruefe_warteauftraege_kopie.py` | Selbstprüfung gegen eine **Arbeitskopie**; läuft nur mit Markierungsdatei `.probe-kopie` |
| `requirements.txt` | bindet die bestehenden Listen ein, ergänzt den Kalender |
| `dashboard/TESTPLAN_WARTEAUFTRAEGE_AGENT.md` | Testplan zur autonomen Ausführung durch eine lokale Claude-Code-Sitzung |
| `docs/UEBERGABE_PR71_WARTEAUFTRAEGE.md` | dieses Dokument |

### Geänderte Dateien

| Datei | Änderung |
|---|---|
| `notifications/manual_close.py` | Quelle `warteauftrag` + eine Protokollfunktion für Auftragsereignisse. **Sonst unverändert** — die Schreiblogik selbst ist nicht angefasst |
| `dashboard/schliessen.py` | Fallunterscheidung offen/geschlossen/unbekannt, Vormerk-Schleife, Liste, Stornieren |
| `dashboard/app.py` | Bestätigungsfeld durchgereicht; zwei neue Routen (`GET /api/warteauftraege`, `POST /api/warteauftraege/stornieren`) |
| `dashboard/static/*` | zusätzlicher Warnschritt in allen drei Dialogen, zwei Auftragslisten, eigene Farbe |
| `dashboard/test_dashboard.py` | vier neue Abschnitte (16–19): 545 → 738 Prüfungen |
| `dashboard/README.md`, `dashboard/TESTANLEITUNG_SCHLIESSEN.md` | Dokumentation, gestaffelte Anleitung Schritte 13–18 |
| `.gitignore` | Auftragsdatei und ihre Nebendateien |

### Datenfluss

```
Dashboard (Dialog)                       Cronjob, alle 5 Minuten
      │                                          │
      │ vorbereiten  ── Kalender? ──┐            │ warteauftraege.json lesen
      │                             │            │        │ leer? → Ende
      │ ausfuehren + Bestätigung    │            │ Kalender? ── zu → Ende
      ▼                             ▼            ▼ offen
 sofort schließen            Warteauftrag   Kurs holen (monitor.fetch_stock_prices)
      │                       (JSON-Datei)        │
      └──────────────┬─────────────────────────────┘
                     ▼
    manual_close.schliesse_position()   ← die EINE schreibende Funktion
    (BEGIN IMMEDIATE, erneute Prüfung, rowcount==1, Protokoll)
```

## 5. Entscheidungsgrundlage

**1. Bibliothek `pandas_market_calendars`.** Eine Zeitregel („Mo–Fr,
15:30–22:00 deutscher Zeit") ist auf drei Arten falsch, die alle regelmäßig
eintreten: bewegliche Feiertage (Thanksgiving, Karfreitag), verschobene
Feiertage (4. Juli 2026 fällt auf Samstag), verkürzte Handelstage (Schluss
13:00 statt 16:00 Ortszeit) und die zwischen USA und Europa abweichende
Zeitumstellung. Abgelehnt: `USFederalHolidayCalendar` (kennt Bundes-, nicht
Börsenfeiertage, keine Halbtage), eine Kursdaten-API zu fragen
(Netzabhängigkeit an einer Stelle, an der eine Zeitüberschreitung bedeutet,
dass nichts passiert), `exchange_calendars` direkt (gleiche Datengrundlage,
wird ohnehin mitinstalliert; die Wahl fiel auf die verbreitetere Hülle).
Version nur als Untergrenze, damit pip auf Python 3.9 die 4.x-Reihe und auf
3.10+ die 5.x wählt.

**2. Drei Zustände statt zwei.** `offen` → schließen, `geschlossen` →
vormerken, **`unbekannt` → weder noch**. Ein Warteauftrag ohne funktionierenden
Kalender wäre eine Absicht, die niemand einlösen kann — das Ausführungsskript
hängt am selben Kalender. Er sähe aus wie ein Auftrag und wäre ein Stillstand.
Bewusst **keine Faustregel als Rückfallebene**: eine Näherung, die nur greift,
wenn die genaue Antwort fehlt, schlüge genau dann zu, wenn niemand hinsieht.

**3. Eine gemeinsame JSON-Datei statt einer je Bot.** Die Übersichtsseite
beantwortet „was steht an" in einer Abfrage; Nebenläufigkeit gibt es an einer
Stelle statt an neun; die Mengen sind winzig; der Nutzer kann die Datei im
Zweifel selbst lesen und löschen. Kein SQLite: der Gewinn wäre gering, der
Preis ein Binärformat, das man im Ernstfall nicht mit einem Texteditor
geradeziehen kann. Nebenläufigkeit über eine **eigene Sperrdatei** (die
Nutzdatei wird beim Schreiben ersetzt — eine Sperre auf ihr hinge danach an
einer Datei, die es nicht mehr gibt), atomares Schreiben über `os.replace`,
Lesen und Schreiben unter derselben Sperre.

**4. Der Server entscheidet, der Browser bestätigt nur.** Ob ein Tap schließt
oder vormerkt, legt `vorbereiten` serverseitig fest. Ein Frontend, das den Weg
selbst wählen könnte, wäre ein Frontend, das mit einer veralteten Annahme über
Börsenzeiten einen Schreibzugriff auslöst.

**5. Warum eine zweite Bestätigung, obwohl die Vorgangs-Kennung schon
vorliegt.** Die Kennung belegt, dass jemand *schließen* wollte. Sie belegt
nicht, dass er verstanden hat, dass daraus eine Ausführung *ohne erneute
Rückfrage* wird. Geprüft wird serverseitig auf genau `true` — wie der
`CRASH`-Text.

**6. Der Grenzfall Handelsschluss zwischen Übersicht und Tap.** *Offen →
geschlossen:* es wird weder geschrieben (der bestätigte Kurs ist jetzt ein
alter) noch stillschweigend vorgemerkt (der Warnschritt wurde nicht gezeigt) —
Abbruch mit Erklärung. *Geschlossen → offen:* der Auftrag entsteht wie
bestätigt und wird binnen Minuten ausgeführt. *Im Crash-Weg* je Bot geprüft:
Krypto wird trotzdem geschlossen, der betroffene Aktien-Bot als unberührt
ausgewiesen.

**7. Zwei Schleifen statt einer mit `if`.** `_bot_abarbeiten()` schreibt,
`_bot_vormerken()` fasst keine Datenbank an. Ein gemeinsamer Rumpf mit einer
Verzweigung hätte die Aussage „hier steht der einzige Schreibpfad" aufgeweicht
— und die trägt die gesamte Absicherung.

**8. Keine vierte Schreiblogik.** Das Ausführungsskript ruft
`manual_close.schliesse_position()` — dieselbe Kernfunktion wie Telegram und
Dashboard, mit derselben Transaktion, derselben erneuten Prüfung innerhalb der
Transaktion und demselben Protokoll. Kurse kommen aus
`monitor.fetch_stock_prices`, derselben Funktion wie im Dashboard.

**9. Stornieren ohne Rückfrage.** Es *verhindert* einen Schreibzugriff, statt
einen auszulösen. Ein zu Unrecht stornierter Auftrag ist mit zwei Klicks neu
angelegt; ein zu Unrecht ausgeführter ist eine Zeile in der Live-Datenbank.
Protokolliert wird trotzdem, klar als `WARTEAUFTRAG-STORNIERT`.

## 6. Testergebnisse

**`python3 dashboard/test_dashboard.py` → 738/738 Prüfungen bestanden**
(vorher 545), dazu 27/27, 23/23 und 24/24 in den Node-Verhaltenstests.

**Der Kalender (Abschnitt 16).** Gefälscht wird die **Uhr**, nicht der
Kalender — die echte Bibliothek rechnet mit echten NYSE-Regeln, nur an einem
Tag, den der Test kennt.

| Fall | Zeitpunkt (UTC) | Erwartet | |
|---|---|---|---|
| Normaler Handelstag | 2026-09-10 17:00 | offen | ✅ |
| Samstag | 2026-09-12 17:00 | zu | ✅ |
| Thanksgiving (beweglich) | 2026-11-26 17:00 | zu, obwohl Donnerstag 13:00 NY | ✅ |
| Karfreitag (osterabhängig) | 2026-04-03 15:00 | zu | ✅ |
| 4. Juli auf Samstag | 2026-07-03 17:00 | zu (Freitag davor) | ✅ |
| Verkürzter Tag, 12:30 NY | 2026-11-27 17:30 | offen | ✅ |
| Verkürzter Tag, 13:30 NY | 2026-11-27 18:30 | zu | ✅ |
| Bibliothek fehlt | – | weder schließen noch vormerken | ✅ |

**Abschnitte 17–19.** Warteaufträge (Anlegen, Ablehnen ohne Bestätigung —
auch bei `"ja"`, `1`, `"true"`, `0`, `None` —, Persistenz direkt von der
Platte gelesen, Stornieren, Krypto unberührt), das Ausführungsskript
(geschlossen/Feiertag/Halbtag → nichts; offen → schließt zum Kurs des
Ausführungszeitpunkts; Bot war schneller → übersprungen; gesperrte Datenbank →
sauberer Abbruch, Auftrag bleibt) und der gemischte Crash-Fall (Krypto sofort,
Aktien vorgemerkt, ohne Bestätigung passiert **gar nichts**).

**Gegenproben (Methodik-Grundsatz 12).** Fünf Mutationen, jede einzeln
eingebaut und wieder entfernt; jede macht die Suite rot:

| Mutation | rot bei |
|---|---|
| Bestätigung wird nicht mehr geprüft | „Ohne Bestätigung des Warnschritts: abgelehnt (409)" |
| Aktien immer handelbar (Kalender ignoriert) | „Aktien-Lage ist WEDER handelbar NOCH vormerkbar" |
| Ausführungsskript ignoriert den Kalender | „Bei geschlossener Börse wird nichts geschlossen" |
| Erster Tap sendet sofort | „Der erste Tap zeigt nur die Warnung und sendet nichts" |
| Stornieren protokolliert wie Ausführung | „Das Stornieren steht als 'STORNIERT' im Protokoll" |

**Bot-Code unverändert.** `git diff --stat main -- strategies/` liefert keine
Ausgabe; `forward_test.py` und `live_params.py` sind bei allen neun Bots
einzeln geprüft unverändert. `py_compile` über alle geänderten und neuen
Python-Dateien: fehlerfrei.

**Zusätzlich gegen eine echte Projektkopie:**
`dashboard/pruefe_warteauftraege_kopie.py` → **32/32**, plus Gegenprobe, dass
dasselbe Skript im echten Projektordner mit Rückgabewert 2 abbricht.

**Nicht geprüft:** die Oberfläche in echtem iOS-Safari, und der Cronjob im
Dauerbetrieb. Beides braucht den Mac des Nutzers.

## 7. Was der Nutzer noch tun muss

1. **Testanleitung ab Schritt 13** durchgehen
   (`dashboard/TESTANLEITUNG_SCHLIESSEN.md`, Teil 2) — oder eine lokale
   Claude-Code-Sitzung den Testplan
   `dashboard/TESTPLAN_WARTEAUFTRAEGE_AGENT.md` abarbeiten lassen. Schritte
   13–16 sind gefahrlos bzw. laufen gegen eine Kopie.
2. **Visuell prüfen**, einmal bei geschlossener und einmal bei offener Börse,
   und einmal auf dem iPhone.
3. **Entscheiden, ob der Cronjob eingerichtet wird** (Schritt 17). Das ist die
   eigentliche Freigabe, siehe Abschnitt 3.
4. **PR mergen** — oder bewusst offen lassen.

## 8. Der Rückweg, falls etwas schiefgeht

Ein von einem Warteauftrag geschlossener Trade ist an `result='manual_close'`
und der Protokollzeile `quelle=warteauftrag` erkennbar:

```bash
grep 'quelle=warteauftrag' ~/trading-bot/logs/notifications/manuelle_eingriffe.log
```

Zurücknehmen wie bei jedem manuellen Eingriff (Testanleitung Schritt 5):

```bash
sqlite3 ~/trading-bot/paper_trading_<bot>.db \
  "UPDATE trades SET status='open', result=NULL, exit_time=NULL, exit_price=NULL, pnl_pct=NULL WHERE id=<ID> AND result='manual_close';"
```

Cronjob abschalten: `EDITOR=nano crontab -e`, Zeile mit `#` auskommentieren.
Wartende Aufträge bleiben dann stehen und lassen sich stornieren.

Funktion ganz zurücknehmen: PR nicht mergen bzw. Branch verwerfen. Die
Auftragsdatei `notifications/warteauftraege.json` kann gelöscht werden; sie
enthält keine Handelsdaten, nur Absichten.

## 9. Bekannte Grenzen

1. **Die Vorab-Erlaubnis ist das eigentliche Risiko** — nicht ein Fehler im
   Code, sondern die Eigenschaft selbst.
2. **Der Kurs beim Ausführen ist nicht der beim Bestätigen.** Über ein
   Wochenende kann das ein deutlicher Unterschied sein.
3. **Ein dauerhaft scheiternder Auftrag bleibt stehen.** Absicht (eine
   gesperrte Datenbank ist in fünf Minuten wieder frei), fällt aber nur auf,
   wenn man hinsieht — die Liste zeigt Versuche und letzten Fehler.
4. **Die Auftragsdatei liegt nur lokal** und ist gitignored; sie überlebt
   Neustarts, aber keinen Rechnerwechsel.
5. **yfinance liefert während der Handelszeiten den laufenden Tageskurs** —
   ein echter, aktueller Kurs, aber keine Realtime-Anbindung mit
   Ausführungsgarantie. Für Paper-Trading richtig, für echtes Geld nicht.
6. **iOS-Safari ungeprüft** — dieselbe offene Frage wie bei PR #62
   (Übergabeprotokoll Abschnitt 9, Punkt 8), jetzt mit einer Dialogstufe mehr.

## 10. Was nach einem Merge im Übergabeprotokoll nachzuziehen ist

`docs/UEBERGABEPROTOKOLL.md` beschreibt den Stand von `main` und ist derzeit
korrekt. Nach einem Merge von PR #71 sind zu ergänzen:

- **Abschnitt 4.3** (Beobachtungsebene): Das Dashboard hat einen vierten,
  zeitversetzten Ausgang. Der Satz „beide lesen ausschließlich" gilt für
  Telegram weiterhin, für das Dashboard seit PR #60 nicht mehr.
- **Abschnitt 8** (Entscheidungen): neue Zeile „Zeitversetzte Ausführung ohne
  erneute Bestätigung eingeführt" mit der Begründung aus Abschnitt 3 hier.
- **Abschnitt 9** (offene Punkte): Cronjob-Status der Warteaufträge
  aufnehmen — analog zu Punkt 2 (Quartals-Reviews), dessen Einträge ebenfalls
  unbestätigt sind.
- **Architekturübersicht**: drei neue Dateien plus `requirements.txt`.
- **Abschnitt 2 / Bot-Tabelle**: unverändert — es kam kein Bot hinzu und keine
  Strategie wurde angefasst.
