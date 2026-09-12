# Ergebnis — Echte Portfolio-Sicht im Dashboard

**PR #80** · Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`d5be46e`, nach Merge von #79).

---

## Was es jetzt gibt

Eine eigene Seite **`/portfolio`**, verlinkt von der Übersicht. Sie beantwortet
die Frage, die neun Karten nebeneinander nicht beantworten: läuft das
Portfolio?

Gerechnet wird mit `shared/portfolio_overview.py` — demselben Programm, das die
Montags-Mail füllt. Es wurde **nur gelesen und aufgerufen**, nicht umgebaut;
ein Test vergleicht die Zahlen mit dessen Textausgabe und prüft gegen
`origin/main`, dass die Datei unverändert ist.

---

## Die Ehrlichkeit der Zahlen — beides, nicht eines von beiden

| | |
|---|---|
| Je Bot | `echte Trades (25)` · `Backtest (3 von 10)` · `keine Kurve` |
| Gruppe 1 | **Nur echte Trades** |
| Gruppe 2 | **Alle Bots (teils Backtest)** |

Warum beides: die Marke allein sagt nicht, *welche* Zahl man glauben darf; zwei
Zahlen allein sagen nicht, *welcher Bot* die zweite verwässert.

Jede Gruppe trägt einen Satz, woraus sie besteht — bei der Backtest-Gruppe
wörtlich „das ist keine erzielte Rendite". **Eine Rendite ohne diesen Satz gibt
es auf der Seite nicht**, und der Frontend-Test prüft genau das: Zahl der
gezeigten Renditen ≤ Zahl der Herkunftssätze.

Die Marke nennt bei Backtest auch den Abstand zur Schwelle (`3 von 10`) —
„Backtest" allein lässt offen, ob das ein Dauerzustand ist oder in sieben
Trades vorbei.

---

## ⚠️ Zwei Befunde, die über die Anzeige hinausreichen

**1. Die Montags-Mail nennt eine reine Backtest-Zahl „LIVE-PORTFOLIO".**

`shared/portfolio_overview.py` gruppiert nach „hat eine `live_params.py`" und
beschriftet diese Gruppe „LIVE-PORTFOLIO (nur aktivierte Bots)". Alle neun Bots
haben eine `live_params.py`, und keiner erreicht die Schwelle von zehn
geschlossenen Trades. **Die Zahl stammt heute zu 100 % aus Backtest-Kurven,
obwohl sie „live" heisst.**

Genau die Verwechslung, die diese Aufgabe verhindern soll — sie steckt schon im
Bestand. Die Gruppen im Dashboard heissen deshalb nicht „live", sondern „echte
Trades". Die Mail selbst ist unverändert (durfte nicht angefasst werden); der
Befund steht als offener Punkt 15 im Übergabeprotokoll.

**2. Ein Bot kann lautlos aus der Summe verschwinden.**

`load_all_curves()` fängt Lesefehler ab, gibt eine `print`-Warnung aus und
lässt den Bot fallen — die Summe läuft dann über weniger Bots. Im Terminal
sieht man es, in einer Oberfläche nicht. Aufgefallen praktisch: hier scheiterte
der Live-Subprozess von `t3_supertrend` (Paket `binance` fehlt im Container),
und der Bot war einfach weg.

Die Seite führt jeden solchen Bot jetzt mit `keine Kurve` und einem Hinweis
oben: „N Bot(s) sind in KEINER Summe unten enthalten".

---

## Eigene Seite, nicht Block auf der Übersicht

Auf der Übersicht liegt der **Crash-Knopf**, und die Rechnung dauert Sekunden.
Eine eigene Seite macht es **strukturell** unmöglich, dass diese Rechnung je in
den Ladepfad des Notfallwegs gerät — aus einer Frage der Sorgfalt wird eine der
Architektur. Auf der Übersicht steht nur ein Link, unterhalb des
Crash-Bereichs, der nichts nachlädt.

Belegt mit **wirklich blockierter Abhängigkeit**: der Rechen-Endpunkt meldet
503, während Übersichtsseite, `/api/portfolio` und der Crash-Weg weiter
antworten.

---

## Laufzeit: gemessen, dann entschieden

| Fall | Zeit |
|---|---|
| `import portfolio_overview` (pandas) | **5,2 s**, einmalig je Prozess |
| alle Bots auf Backtest-Kurve | **134 ms** |
| **7 Bots auf dem Live-Weg** | **2,9 s** (≈ 0,42 s je Bot) |
| hochgerechnet auf 9 | **≈ 3,8 s** |

Je Live-Bot startet ein eigener Python-Subprozess — genau der Mechanismus, mit
dem `portfolio_overview` die `sys.modules`-Kollision der neun gleichnamigen
`equity_simulation.py` umgeht.

**Entscheidung: Zwischenspeicher. Das Dashboard rechnet nie von selbst.** `GET`
liest nur; neu gerechnet wird per Knopf, Skript oder Cronjob. Das Alter steht
immer dabei, über 24 Stunden als *veraltet* markiert.

Den Ausschlag gab nicht das Tempo, sondern die **Richtigkeit**:
`portfolio_overview` legt seine Zwischendateien unter einem *festen* Namen ab.
Dashboard und Montags-Mail gleichzeitig hätten sich diese Datei gegenseitig
überschrieben — beide Ergebnisse falsch. Die Rechnung läuft deshalb in einem
eigenen Ordner und ist über eine Sperrdatei serialisiert.

---

## Tests

| Suite | Ergebnis |
|---|---|
| `dashboard/test_portfolio_sicht.py` *(neu)* | **90 / 90** ✅ |
| davon `test_portfolio_anzeige.js` *(neu, node)* | **67 / 67** ✅ |
| `dashboard/test_dashboard.py` | 784 / 784 ✅ |
| `notifications/test_schliess_benachrichtigung.py` | 99 / 99 ✅ |
| `system/test_log_rotation.py` | 117 / 117 ✅ |
| `broker/test_broker.py` · `test_ibkr.py` | 163 · 200 ✅ |
| `shared/test_empfehlung_format.py` · `system/test_caffeinate_plist.py` | 70 · 52 ✅ |

Alle fünf geforderten Datenlagen geprüft (alle über der Schwelle, alle
darunter, gemischt, ein Bot ohne Trades, ein Bot ohne Datenbank) — dazu der
ausgefallene Bot. Der Abgleich mit dem echten `portfolio_overview` stimmt Zahl
für Zahl: Rendite **80,52 %**, Drawdown **−6,24 %**, Fenster
**2022-03-18 bis 2026-06-27**.

**22 Mutationsproben, alle 22 im ersten Durchlauf erkannt.** Die beiden
wiederkehrenden Fallen wurden vorab adressiert: die Endpunkt-Tests zählen echte
Aufrufe statt Ergebnisse, und der Notfallweg wird mit echt blockiertem Import
geprüft, nicht mit einer Attrappe.

### Drei Fehler, die die Tests gefunden haben

- **Ein symmetrisches Fixture prüfte nichts.** Steigungen 4/5/6 % ergeben in
  beiden Gruppen denselben Mittelwert — der Vergleich war wertlos.
- **Der Zeitpunkt war ein rohes `Date`-Objekt:** „Sat Sep 12 2026 09:00:00
  GMT+0000" auf einem deutschen iPhone. `zeitpunkt()` gibt ein Date zurück,
  formatiert wird mit `zeit()`.
- **Mein eigener Test veränderte das Repo:** der Abgleichlauf überschrieb
  eingecheckte Kurven-CSVs. Jetzt mit umgelenktem Ausgabeordner.

---

## Was du noch tun musst

**1. Nichts Dringendes.** Die Seite funktioniert ohne weitere Einrichtung. Beim
ersten Aufruf steht „Noch nicht berechnet"; ein Tap auf **Neu berechnen** füllt
sie.

**2. Cronjob eintragen, wenn gewünscht** (Zeile im README, **nicht**
eingetragen):

```cron
40 3 * * * cd ~/trading-bot && /usr/bin/python3 dashboard/portfolio_sicht.py --berechnen >> logs/dashboard/portfolio_sicht.log 2>&1
```

Vorher `mkdir -p logs/dashboard`. 3:40 Uhr liegt nach der Log-Rotation (3:30).

**3. `node` installieren** (`brew install node`) — unabhängig von dieser
Änderung, aber hier besonders relevant: ohne `node` laufen **67** der 90
Prüfungen nicht, und genau die prüfen die Quellenkennzeichnung in der Ausgabe.

Der vollständige Ablauf steht in
`dashboard/TESTAUFTRAG_PORTFOLIO_SICHT.md`; **Schritt 5** (Übersichtsseite lädt
während laufender Rechnung) ist die wichtigste Einzelaussage.

---

## Offene Punkte

- **„LIVE-PORTFOLIO" in der Montags-Mail** bleibt irreführend — eine Zeile in
  `portfolio_overview.py`, hier ausdrücklich nicht erlaubt (Punkt 15).
- **Kein Test gegen eine echte Live-Datenbank über der Schwelle.** Es gibt im
  Repo keine; der Testauftrag holt das auf dem Mac nach.
- **Nie in echtem iOS-Safari geöffnet** — geprüft ist, was die Funktionen
  *erzeugen*, nicht wie Safari es darstellt.

## Geänderte Dateien

```
dashboard/portfolio_sicht.py              (neu)
dashboard/static/portfolio.html           (neu)
dashboard/test_portfolio_sicht.py         (neu, 90 Prüfungen)
dashboard/test_portfolio_anzeige.js       (neu, 67 Prüfungen)
dashboard/TESTAUFTRAG_PORTFOLIO_SICHT.md  (neu)
docs/UEBERGABE_portfolio_sicht.md         (neu)
docs/ERGEBNIS_portfolio_sicht.md          (neu, dieses Dokument)
dashboard/app.py                          (2 Endpunkte, 1 Seitenroute)
dashboard/static/app.js                   (5 Anzeigefunktionen)
dashboard/static/index.html               (ein Link)
dashboard/static/style.css                (Marken, Kennzahlen)
dashboard/static/sw.js                    (/portfolio in die Hülle)
dashboard/test_dashboard.py               (Positivliste: zehnte Nicht-GET-Route)
dashboard/README.md                       (Abschnitt Portfolio-Sicht)
docs/UEBERGABEPROTOKOLL.md                (4.3b neu, offene Punkte 15/16)
.gitignore                                (Zwischenspeicher)
```

Nicht angefasst: `shared/portfolio_overview.py` (nur gelesen/aufgerufen, per
`git diff` geprüft), keine `live_params.py`, `forward_test.py`,
`equity_simulation.py`, kein `trades`-Schema, nichts unter `broker/` oder
`strategies/`, keine Crontab, keine launchd-Vorlage, kein Schliess- oder
Crash-Weg.
