# Testauftrag TB-38 — Gemeinsame Abrufschicht

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht.

**Alle Befehle sind einzeilig.** Termius auf dem iPhone verliert
Zeilenumbrüche in Heredocs und Python-Blöcken — hier kommt keiner vor.

---

> # ⚠️ DIE EINE REGEL: DIE NEUN DATENBANKEN ZUERST SICHERN
>
> **Schritt 1 läuft, BEVOR irgendein Bot gestartet wird.**
>
> TB-38 ändert, auf welcher Kerze die Bots entscheiden. Bei fünf von neun ist
> das eine **andere** Kerze als bisher. Ein Lauf kann deshalb eine Position
> eröffnen oder schliessen, die der alte Stand nicht eröffnet oder
> geschlossen hätte — und die neun `paper_trading_*.db` sind die **einzige**
> Aufzeichnung des Papierpfads. Es gibt kein Rückgängig.
>
> Wer Schritt 1 überspringt, kann Schritt 12 (Rückweg) nicht gehen.

> # ⚠️ DIE ZWEITE REGEL: `data/` NICHT NEBENBEI AUFFRISCHEN
>
> Schritt 8 frischt `data/` auf. Das **ändert den Datenstand-Hash der
> Vorregistrierung** (`docs/VORREGISTRIERUNG_neuselektion.md`), weil neue
> Kerzen dazukommen. Schritt 8 ist deshalb **ausdrücklich optional** und
> entscheidet der Betreiber. Alle anderen Schritte lassen `data/` unberührt.

---

## Was gebraucht wird

* Zugang zum MacBook mit dem Repo unter `~/trading-bot`
* `python3`, `pandas`, `pandas_market_calendars` (aus `requirements.txt`)
* Netz zu Binance/yfinance nur für Schritt 7b und 8 — alles andere ist offline
* Rund 30 Minuten

**Ergebnis-Ordner anlegen, dorthin kommen alle Protokolle:**

```bash
mkdir -p ~/Downloads/TB-38_abrufschicht
```

---

## Schritt 1 — Sicherung. Zuerst. Vor allem anderen.

```bash
mkdir -p ~/Sicherungen/tb38_abrufschicht
```

```bash
cp -p ~/trading-bot/paper_trading_*.db ~/Sicherungen/tb38_abrufschicht/
```

```bash
ls -l ~/Sicherungen/tb38_abrufschicht/ | tee ~/Downloads/TB-38_abrufschicht/01_sicherung.txt
```

**Erwartet:** **neun** Dateien `paper_trading_*.db`.

**Weniger als neun?** Nicht weitermachen. Erst klären, welcher Bot keine
Datenbank hat — das wäre ein eigener Befund.

---

## Schritt 2 — Den Ist-Zustand erheben (beantwortet einen Nebenbefund)

```bash
cd ~/trading-bot && date "+%Y-%m-%d %H:%M:%S %Z (%z)" | tee ~/Downloads/TB-38_abrufschicht/02_zeitzone.txt
```

**Erwartet:** `CEST (+0200)` im Sommer bzw. `CET (+0100)` im Winter.

```bash
crontab -l 2>&1 | tee ~/Downloads/TB-38_abrufschicht/02_crontab.txt
```

**Worauf zu achten ist** — die Cloud-Auswertung sagt Folgendes voraus, und
genau das ist hier zu bestätigen oder zu widerlegen:

| Erwartung | woher |
|---|---|
| `elliott_wave` steht auf `0 * * * *` | `docs/DATENLUECKEN.md` |
| `t3_supertrend` steht auf **`0 */4 * * *`** (nicht `5 */4`) | `docs/DATENLUECKEN.md` |
| `5 */4 * * *` gehört zur **Broker-Brücke**, nicht zum Bot | `broker/README.md` |
| die vier Aktien-Bots stehen auf **22:15**, werktags | `docs/UEBERGABEPROTOKOLL.md` Abschnitt 2 |
| die drei täglichen Krypto-Bots auf `20 23`, `50 23`, `15 0` | `docs/DATENLUECKEN.md` |

⚠️ **Die Aufgabenbeschreibung zu TB-38 sagt, der `t3_supertrend`-Cron laufe
„zur Minute 5 nach der Vier-Stunden-Grenze", die gelesene Teilkerze sei also
fünf Minuten alt.** Nach Aktenlage stimmt das nicht: der Bot steht auf
`0 */4`, und Cron zündet in **Ortszeit**, das UTC-Kerzenraster liegt also
2 (Sommer) bzw. 3 Stunden (Winter) versetzt. Die Teilkerze war damit **2 bis
3 Stunden** alt, nicht 5 Minuten. Am Befund ändert das nichts, an seiner
Grössenordnung schon. **Bitte hier festhalten, was `crontab -l` wirklich
sagt** — das ist die einzige belastbare Quelle.

**Notieren:** welcher der drei täglichen Krypto-Einträge zu welchem Bot
gehört. Das wurde bisher **nie** erhoben und steht seither als Lücke im
Register.

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft; print(herkunft.datenstand())" | tee ~/Downloads/TB-38_abrufschicht/02_datenstand_vorher.txt
```

**Erwartet:** `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`
und `223` Dateien.

**Abweichend?** Notieren und weitermachen — für TB-38 ist nur wichtig, dass
sich der Wert bis Schritt 11 **nicht ändert**.

---

## Schritt 3 — Basislauf der Selbsttests auf dem ALTEN Stand

```bash
cd ~/trading-bot && git status --short | tee ~/Downloads/TB-38_abrufschicht/03_status.txt
```

**Erwartet:** leer oder nur bekannte lokale Dateien.

```bash
cd ~/trading-bot && for t in shared/test_*.py notifications/test_*.py system/test_*.py; do printf "%s " "$t"; python3 "$t" >/dev/null 2>&1; echo "rc=$?"; done | tee ~/Downloads/TB-38_abrufschicht/03_basislauf.txt
```

**Erwartet:** überall `rc=0` **ausser** bei den vier bekannt roten:
`test_drawdown_beide_masse.py`, `test_kursdaten.py`,
`test_stabile_sortierung.py`, `test_wellenauswahl.py`.

**Diese Datei ist die Vergleichsbasis für Schritt 5.** Ohne sie sagt Schritt 5
nichts aus.

---

## Schritt 4 — Den Zweig holen

```bash
cd ~/trading-bot && git fetch origin claude/new-session-xzh112 && git checkout claude/new-session-xzh112 && git pull origin claude/new-session-xzh112
```

```bash
cd ~/trading-bot && git log --oneline -3 | tee ~/Downloads/TB-38_abrufschicht/04_zweig.txt
```

```bash
cd ~/trading-bot && git diff origin/main HEAD --name-only | tee ~/Downloads/TB-38_abrufschicht/04_geaenderte_dateien.txt
```

**Erwartet:** ⚠️ **keine einzige Zeile beginnt mit `data/`.** Ist doch eine
dabei, sofort melden und nicht weitermachen.

---

## Schritt 5 — Selbsttests auf dem NEUEN Stand

```bash
cd ~/trading-bot && python3 shared/test_entscheidungskerze.py 2>&1 | tail -20 | tee ~/Downloads/TB-38_abrufschicht/05_entscheidungskerze.txt
```

**Erwartet:** `Alle 130 Prüfungen bestanden.`

⚠️ **Abschnitt 4 und Abschnitt 10 dürfen NICHT „übersprungen" melden.** Auf
dem Mac ist `pandas_market_calendars` installiert; steht dort „übersprungen",
fehlt das Paket — dann `pip3 install -r requirements.txt` und wiederholen.
Ohne diese beiden Abschnitte ist der Aktien-Teil ungeprüft.

```bash
cd ~/trading-bot && python3 shared/test_umstellungstag.py 2>&1 | tail -6 | tee ~/Downloads/TB-38_abrufschicht/05_umstellungstag.txt
```

**Erwartet:** `Alle 25 Prüfungen bestanden.`

```bash
cd ~/trading-bot && for t in shared/test_*.py notifications/test_*.py system/test_*.py; do printf "%s " "$t"; python3 "$t" >/dev/null 2>&1; echo "rc=$?"; done | tee ~/Downloads/TB-38_abrufschicht/05_nachlauf.txt
```

```bash
diff ~/Downloads/TB-38_abrufschicht/03_basislauf.txt ~/Downloads/TB-38_abrufschicht/05_nachlauf.txt | tee ~/Downloads/TB-38_abrufschicht/05_vergleich.txt
```

**Erwartet:** nur die beiden **neuen** Zeilen
(`test_entscheidungskerze.py rc=0`, `test_umstellungstag.py rc=0`). **Kein
Test, der vorher `rc=0` hatte, darf jetzt anders sein.**

---

## Schritt 6 — Welche Kerze nimmt jeder Bot jetzt? (rein lesend)

```bash
cd ~/trading-bot && python3 shared/entscheidungskerze.py 2>&1 | tee ~/Downloads/TB-38_abrufschicht/06_entscheidungskerzen.txt
```

**Das Werkzeug fasst nichts an.** Es sagt zweierlei:

1. **oben:** je Bot die Kerze, auf der ein Lauf **jetzt** entscheiden würde;
2. **unten:** welche Kursdateien diese Kerze in `data/` nicht tragen.

**Erwartet in der Cloud-Messung vom 15.09.2026:** 199 von 223 Dateien ohne die
erwartete Kerze — alle `_1h`, alle `_4h`, alle 150 Aktien-Tagesdateien; die 24
Krypto-Tagesdateien frisch.

**Auf dem Mac kann das anders aussehen**, falls `data/` dort zwischenzeitlich
von Hand aufgefrischt wurde. Die Zahl bitte notieren — sie ist die Grundlage
für die Entscheidung in Schritt 8.

```bash
cd ~/trading-bot && python3 shared/entscheidungskerze.py --json ~/Downloads/TB-38_abrufschicht/06_frische.json >/dev/null 2>&1; echo "JSON geschrieben"
```

---

## Schritt 7 — Einen Bot wirklich laufen lassen

> Ab hier wird geschrieben. Schritt 1 muss gelaufen sein.

### 7a — der Bot, um den es geht

```bash
cd ~/trading-bot && python3 strategies/t3_supertrend/forward_test.py 2>&1 | tee ~/Downloads/TB-38_abrufschicht/07a_t3_supertrend.txt
```

**Worauf zu achten ist:**

| Zeile in der Ausgabe | Bedeutung |
|---|---|
| `Rueckfall auf den Live-Abruf fuer …` | `data/` war nicht frisch → der Bot hat live abgerufen. **Kein Fehler** |
| `Hinweis: … Kerze(n) nach der Entscheidungskerze verworfen` | der Filter hat gegriffen — **genau das soll er** |
| keine der beiden Zeilen | `data/` war frisch und enthielt keine laufende Kerze |

**Erwartet:** der Lauf geht **ohne Traceback** durch und endet mit
`FORWARD-TEST STATUS`.

### 7b — einen Aktien-Bot, nach Börsenschluss

> Nur sinnvoll **nach 22:15 Ortszeit an einem Handelstag**. Sonst überspringen
> und notieren, dass er übersprungen wurde.

```bash
cd ~/trading-bot && python3 strategies/turtle_soup_stocks/forward_test.py 2>&1 | tee ~/Downloads/TB-38_abrufschicht/07b_turtle_soup_stocks.txt
```

⚠️ **Die entscheidende Beobachtung:** In der Ausgabe darf **keine** Zeile
stehen, die `Boersenkalender` erwähnt. Steht dort eine, konnte der Kalender
nicht antworten — dann fällt der Bot auf die konservative Schranke zurück und
entscheidet auf der Kerze von **gestern**. Abhilfe:
`pip3 install -r requirements.txt`.

---

## Schritt 8 — ⚠️ OPTIONAL: `data/` auffrischen

**Das ist eine Entscheidung des Betreibers, keine Testanweisung.**

**Dafür:** erst dann wirkt der beabsichtigte Datenweg („die Forward-Tests
lesen `data/`"), und die tägliche Rückfall-Meldung hört auf.

**Dagegen:** es **ändert den Datenstand-Hash der Vorregistrierung**. Der Wert
in `docs/VORREGISTRIERUNG_neuselektion.md` bezeugt den Bestand zum Zeitpunkt
der Selektion; kommen Kerzen dazu, stimmt er nicht mehr. Ob das gewollt ist,
entscheidet **nur** der Betreiber.

Wenn ja, zuerst sichern:

```bash
cd ~/trading-bot && python3 shared/abrufschutz.py --aufnehmen ~/Downloads/TB-38_abrufschicht/08_data_vorher.json
```

```bash
cd ~/trading-bot && python3 shared/fetch_multi_data.py 2>&1 | tail -20 | tee ~/Downloads/TB-38_abrufschicht/08_fetch_1h.txt
```

```bash
cd ~/trading-bot && python3 strategies/t3_supertrend/fetch_4h_data.py 2>&1 | tail -20 | tee ~/Downloads/TB-38_abrufschicht/08_fetch_4h.txt
```

```bash
cd ~/trading-bot && python3 strategies/volatility_breakout/fetch_stock_data.py 2>&1 | tail -20 | tee ~/Downloads/TB-38_abrufschicht/08_fetch_aktien.txt
```

```bash
cd ~/trading-bot && python3 shared/entscheidungskerze.py 2>&1 | head -25 | tee ~/Downloads/TB-38_abrufschicht/08_frische_danach.txt
```

**Erwartet danach:** deutlich weniger Dateien ohne die erwartete Kerze.

### Der Crontab-Vorschlag — **nicht eingetragen**

Damit `data/` von selbst frisch bleibt, müsste je Zeitrahmen **vor** dem
zugehörigen Bot-Lauf abgerufen werden. Vorschlag (Ortszeit), zu prüfen und
selbst einzutragen:

```cron
50 * * * * cd ~/trading-bot && /usr/bin/python3 shared/fetch_multi_data.py >> logs/system/fetch_1h.log 2>&1
50 */4 * * * cd ~/trading-bot && /usr/bin/python3 strategies/t3_supertrend/fetch_4h_data.py >> logs/system/fetch_4h.log 2>&1
5 22 * * 1-5 cd ~/trading-bot && /usr/bin/python3 strategies/volatility_breakout/fetch_stock_data.py >> logs/system/fetch_aktien.log 2>&1
```

⚠️ **TB-38 hat die Crontab nicht angefasst** und schlägt hier nur vor. Zu
bedenken: die Aktien-Zeile läuft 10 Minuten vor den vier Bot-Läufen um 22:15
und braucht für 150 Titel spürbar Zeit — wer sie einträgt, sollte danach
einmal prüfen, ob sie rechtzeitig fertig wird. **Siehe offener Punkt 24 im
Übergabeprotokoll.**

---

## Schritt 9 — ⚠️ Den Umstellungstag festhalten

**Dieser Schritt ist der Grund, warum der Vergleich Backtest gegen Live später
überhaupt auswertbar ist.** Erst ab diesem Zeitpunkt entsteht ein Papierpfad
nach denselben Regeln wie der Backtest.

```bash
cd ~/trading-bot && python3 shared/umstellungstag.py --festhalten --alle 2>&1 | tee ~/Downloads/TB-38_abrufschicht/09_umstellungstag.txt
```

**Erwartet:** neun Zeilen `festgehalten: …`.

```bash
cd ~/trading-bot && python3 shared/umstellungstag.py --zeigen 2>&1 | tee -a ~/Downloads/TB-38_abrufschicht/09_umstellungstag.txt
```

```bash
cd ~/trading-bot && python3 shared/umstellungstag.py --pruefen; echo "rc=$?"
```

**Erwartet:** `rc=0` und „Kein Befund".

```bash
cp -p ~/trading-bot/docs/umstellungstag_entscheidungskerze.json ~/Downloads/TB-38_abrufschicht/09_umstellungstag.json
```

**Ein zweiter Aufruf rückt den Zeitpunkt nicht vor** — er meldet dann
`unveraendert: …`. Das ist Absicht: der Umstellungstag ist eine Tatsache, kein
Zustand.

⚠️ **Diese Datei gehört ins Repo** (anders als der ZIP-Ordner). Sie wird in
Schritt 13 committet.

---

## Schritt 10 — Kommt die Meldung wirklich in Telegram an?

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import entscheidungskerze as e; s=e.Sammler(); s.erfasse('PROBE_TB38','veraltet','Probemeldung aus dem Testauftrag TB-38'); print('Anlass:', e.melde('probe_tb38', s))" 2>&1 | tee ~/Downloads/TB-38_abrufschicht/10_meldung.txt
```

**Erwartet:** `Anlass: neu` — **und eine Telegram-Nachricht auf dem iPhone**,
die mit `[ABRUFSCHICHT] probe_tb38:` beginnt.

**Kommt keine an?** Dann liegt es an `.env`/`telegram_config.py`, nicht an
TB-38 — der Meldeteil steht in einem `try` und hält den Bot nie an.

Denselben Befehl **ein zweites Mal**:

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import entscheidungskerze as e; s=e.Sammler(); s.erfasse('PROBE_TB38','veraltet','Probemeldung aus dem Testauftrag TB-38'); print('Anlass:', e.melde('probe_tb38', s))" 2>&1 | tee -a ~/Downloads/TB-38_abrufschicht/10_meldung.txt
```

**Erwartet:** `Anlass: gedaempft` — und **keine** zweite Telegram-Nachricht.
Das ist die Wiederholungsdämpfung aus TB-32.

Aufräumen (die Probe soll nicht im Zustand stehenbleiben):

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import entscheidungskerze as e; print('Anlass:', e.melde('probe_tb38', e.Sammler()))"
```

**Erwartet:** `Anlass: still` — und keine Nachricht.

---

## Schritt 11 — `data/` unberührt? (nur wenn Schritt 8 **übersprungen** wurde)

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft; print(herkunft.datenstand())" | tee ~/Downloads/TB-38_abrufschicht/11_datenstand_nachher.txt
```

```bash
diff ~/Downloads/TB-38_abrufschicht/02_datenstand_vorher.txt ~/Downloads/TB-38_abrufschicht/11_datenstand_nachher.txt && echo "IDENTISCH"
```

**Erwartet:** `IDENTISCH`.

**Wurde Schritt 8 ausgeführt**, ist eine Abweichung hier zu **erwarten** —
dann bitte den neuen Wert notieren und entscheiden, ob
`docs/VORREGISTRIERUNG_neuselektion.md` nachgezogen wird. Das ist ein eigener,
ausdrücklich freizugebender Schritt und **nicht** Teil von TB-38.

---

## Schritt 12 — Der Rückweg, falls etwas nicht stimmt

```bash
cd ~/trading-bot && git checkout main
```

```bash
cp -p ~/Sicherungen/tb38_abrufschicht/paper_trading_*.db ~/trading-bot/
```

Damit ist der Stand von vor Schritt 7 wiederhergestellt: alter Code, alte
Datenbanken. Der Umstellungstag in `docs/` bleibt stehen — das ist richtig,
er ist eine Aufzeichnung, kein Zustand, und `--erneut` korrigiert ihn, falls
später doch umgestellt wird.

---

## Schritt 13 — Den Umstellungstag committen

> Nur, wenn Schritt 12 **nicht** gebraucht wurde.

```bash
cd ~/trading-bot && git add docs/umstellungstag_entscheidungskerze.json && git commit -m "TB-38: Umstellungstag je Bot festgehalten" && git push -u origin claude/new-session-xzh112
```

---

## Schritt 14 — Ergebnisse einpacken

```bash
cd ~/Downloads && zip -r TB-38_abrufschicht.zip TB-38_abrufschicht && ls -l ~/Downloads/TB-38_abrufschicht.zip
```

⚠️ **Die ZIP-Datei liegt in `~/Downloads`, NICHT im Repo.** Sie enthält nur
Protokolle zum Zurückschicken.

---

## Zusammenfassung zum Melden

| Schritt | Was | Ergebnis |
|---|---|---|
| 1 | neun Datenbanken gesichert | …… Stück |
| 2 | Zeitzone des Mac | `CEST` / `CET` / andere |
| 2 | `t3_supertrend`-Cron | `0 */4` / `5 */4` / andere: …… |
| 2 | welcher tägliche Krypto-Eintrag zu welchem Bot | …………………… |
| 2 | Datenstand vorher | `d9449faf…` / abweichend |
| 3 | Basislauf: rote Tests | …… (erwartet 4) |
| 4 | `git diff` nennt eine Datei unter `data/` | **nein** / ja ⚠️ |
| 5 | `test_entscheidungskerze.py` | ……/130 |
| 5 | Abschnitt 4 und 10 übersprungen? | nein / ja ⚠️ |
| 5 | `test_umstellungstag.py` | ……/25 |
| 5 | Vergleich mit dem Basislauf | nur zwei neue Zeilen / abweichend |
| 6 | Dateien ohne die erwartete Kerze | ……/223 |
| 7a | `t3_supertrend` gelaufen | ohne Traceback / Fehler |
| 7a | Rückfall-Zeile in der Ausgabe | ja / nein |
| 7b | `turtle_soup_stocks` gelaufen (nach 22:15) | ja / übersprungen |
| 7b | „Boersenkalender"-Zeile in der Ausgabe | **nein** / ja ⚠️ |
| 8 | `data/` aufgefrischt? | nein / ja (bewusst) |
| 9 | Umstellungstag festgehalten | ……/9 Bots |
| 10 | Telegram-Nachricht angekommen | ja / nein |
| 10 | zweiter Aufruf gedämpft | ja / nein |
| 11 | Datenstand unverändert | IDENTISCH / abweichend |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob die Umstellung auf deinem MacBook wirklich funktioniert. Es geht um eine
einzige Frage: Schauen die neun Handelsprogramme jetzt auf einen **fertigen**
Zeitabschnitt des Kursverlaufs statt auf einen, der gerade erst angefangen
hat? Und laufen sie danach alle noch ganz normal?

**Was herauskam.**
Das steht nach dem Durchlauf in der Tabelle darüber. Vier Zeilen sind die
wichtigsten:

* **Schritt 4:** Es darf keine einzige Kursdatei verändert worden sein.
* **Schritt 5:** Alle Tests, die vorher funktionierten, müssen weiter
  funktionieren — plus zwei neue.
* **Schritt 7b:** Beim Aktien-Programm darf das Wort „Boersenkalender" nicht
  auftauchen. Taucht es auf, fehlt ein Zusatzpaket, und dann würden die
  Aktien-Programme jedes Signal einen Tag zu spät sehen.
* **Schritt 9:** Der Umstellungstag muss für alle neun aufgeschrieben sein.

**Warum das so ist.**
Ein Kursverlauf wird in „Kerzen" gezeichnet — jede fasst einen Zeitabschnitt
zusammen, etwa vier Stunden. Eine Kerze ist erst fertig, wenn der Abschnitt
vorbei ist. Fünf der neun Programme schauten bisher auf eine Kerze, die noch
lief. Beim Prüfen einer Strategie am Computer („Backtest") wird dagegen immer
mit fertigen Kerzen gerechnet. Es wurde also zwei Mal Verschiedenes
gerechnet, und der laufende Betrieb konnte die Prüfung gar nicht bestätigen —
obwohl er der einzige unabhängige Beweis ist, den es gibt.

**Was das für dich heisst.**
Die Schritte der Reihe nach abarbeiten und **Schritt 1 nicht überspringen** —
das ist die Sicherheitskopie der neun Handelsdatenbanken. Ab Schritt 7 wird
geschrieben, und rückgängig machen kann man das nur mit der Kopie.

Zwei Stellen verlangen **deine** Entscheidung, nicht die der Anleitung:

* **Schritt 8** frischt den gespeicherten Kursordner auf. Das ist nützlich,
  ändert aber eine Prüfsumme, die den Zustand zum Zeitpunkt der
  Strategie-Auswahl bezeugt. Wenn du unsicher bist: überspringen. Es geht
  auch ohne — die Programme holen sich die Kurse dann weiter aus dem
  Internet, wie bisher, und sagen dir per Telegram Bescheid, dass sie es tun.
* **Der Crontab-Vorschlag** in Schritt 8 ist ein Vorschlag. An deinem
  Zeitplan wurde bewusst nichts verändert.

**Schritt 9 ist der wichtigste Schritt der ganzen Anleitung**, auch wenn er
der kürzeste ist: Er schreibt auf, ab wann der Vergleich „Prüfung gegen
Wirklichkeit" gilt. Ohne ihn weiss später niemand mehr, ab welchem Tag die
Zahlen aus dem laufenden Betrieb überhaupt etwas bedeuten — und es bleiben
nur noch 89 Tage bis zum 13.12.2026.

Am Ende (Schritt 14) entsteht eine ZIP-Datei in `~/Downloads`, die alle
Protokolle enthält. Die gehört **nicht** ins Repo, sondern nur zum
Zurückschicken.
