# Übergabe TB-38 — Gemeinsame Abrufschicht

**Stand: 15.09.2026.** Basis `main` (`0f696b0` — TB-37/PR #110 enthalten, vor
Arbeitsbeginn mit `git merge-base --is-ancestor` geprüft).
Zweig: `claude/new-session-xzh112`.
Ergebnis: `docs/ERGEBNIS_TB-38_abrufschicht.md` · Testauftrag:
`docs/TESTAUFTRAG_TB-38_abrufschicht.md`.

---

# Die drei Antworten, um die gebeten wurde

## 1. Welche Kerze nahm jeder der neun Bots vorher — und welche jetzt?

Cron zündet in **Ortszeit** (Europe/Berlin), die Kerzen liegen auf dem
**UTC**-Raster. „Füllstand" sagt, wie weit die alte Entscheidungskerze zum
Laufzeitpunkt gefüllt war.

| Bot | Takt | **vorher** | Füllstand | **jetzt** | geändert? |
|---|---|---|---|---|---|
| `elliott_wave` | 1 h | die **laufende** Stundenkerze | **0 %** | die vorige, abgeschlossene | **ja** |
| `t3_supertrend` | 4 h | die **laufende** 4-h-Kerze | **50 % / 75 %** ¹ | die vorige, abgeschlossene | **ja** |
| `rsi2_crypto` | 1 d | die **laufende** Tageskerze | **89 – 97 %** | die Tageskerze des **Vortags** | **ja** |
| `turtle_soup_crypto` | 1 d | dito | dito | dito | **ja** |
| `volatility_breakout_crypto` | 1 d | dito | dito | dito | **ja** |
| `elliott_wave_stocks` | 1 d | die Tageskerze von **heute** | **100 %** | **dieselbe** | **nein** |
| `rsi2_mean_reversion` | 1 d | dito | **100 %** | **dieselbe** | **nein** |
| `turtle_soup_stocks` | 1 d | dito | **100 %** | **dieselbe** | **nein** |
| `volatility_breakout` | 1 d | dito | **100 %** | **dieselbe** | **nein** |

**Fünf Krypto-Bots entschieden auf einer Teilkerze und tun es nicht mehr. Vier
Aktien-Bots entschieden schon vorher richtig — aber durch Timing, nicht durch
Regel.** Dass sie sich jetzt nicht ändern, ist der Nachweis, dass der Filter
richtig gebaut ist.

¹ ⚠️ **Nebenbefund, und er widerspricht der Aufgabenbeschreibung.** Dort steht,
der `t3_supertrend`-Cron laufe „zur Minute 5 nach der Vier-Stunden-Grenze", die
Teilkerze sei also fünf Minuten alt. Nach Aktenlage stimmt das nicht:
`5 */4 * * *` ist die Zeile der **Broker-Brücke** (`broker/README.md`), der Bot
steht auf `0 */4 * * *` (`docs/DATENLUECKEN.md`, `crontab -l` vom 11.09.2026).
Und weil Cron in Ortszeit zündet, fällt `0 */4` in Europe/Berlin auf die
**UTC**-Stunden 22/02/06/10/14/18 — **nicht** auf das UTC-Raster 00/04/08/…
Die gelesene Teilkerze war damit **2 bis 3 Stunden** alt, nicht fünf Minuten.
Am Befund ändert das nichts, an seiner Grössenordnung schon. Schritt 2 des
Testauftrags bestätigt oder widerlegt es mit `crontab -l` und `date +%Z`.

## 2. Wie gross ist der Diff je `forward_test.py`?

**+14 / −1 Zeilen** (Krypto), **+15 / −1** (Aktien). **9 davon sind
Kommentar** — die eigentliche Änderung sind 5 bis 6 Zeilen, und sie betrifft
ausschliesslich den Datenbezug:

```diff
  from fetch_binance_data import fetch_historical_data
+ import entscheidungskerze

-         df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
+         df = entscheidungskerze.lade(
+             symbol, INTERVAL, entscheidungskerze.KRYPTO,
+             abruf=lambda: fetch_historical_data(symbol, INTERVAL, LOOKBACK))

+     entscheidungskerze.melde()
      print_summary(conn)
```

Keine Signallogik, keine Schwelle, keine Positionsgrösse, kein Stop,
`live_params.py` unberührt. `df.iloc[-1]` bleibt in allen neun Dateien stehen
und bedeutet ab jetzt das, was es immer bedeuten sollte.

## 3. Laufen die Aktien-Crons nach US-Schluss?

**Ja — mit 15 Minuten Abstand, in beiden Zeitzonenlagen.**

| | Sommer | Winter |
|---|---|---|
| NYSE-Schluss | 20:00 UTC | 21:00 UTC |
| Cron (22:15 Ortszeit) | 20:15 UTC | 21:15 UTC |
| **Abstand** | **+15 min** | **+15 min** |

In den zwei bis drei Wochen im Jahr, in denen die Umstellungstermine
auseinanderliegen, wird der Abstand +75 Minuten — **nie negativ**. Verkürzte
Handelstage (Schluss 13:00 Ortszeit) liegen erst recht davor. Gegen den echten
NYSE-Kalender nachgerechnet in `shared/test_entscheidungskerze.py`,
Abschnitt 4, für Sommer **und** Winter.

⚠️ **Und genau hier hing die Aufgabe:** Hätte der Filter die konservative
`D 23:59:59`-Schranke aus `abrufschutz` benutzt, wären die vier Aktien-Bots
auf die Kerze von **gestern** gefallen — jedes Signal einen Handelstag zu
spät. Deshalb der echte Börsenkalender statt einer Schranke.

---

# Was gebaut wurde

| Datei | Art |
|---|---|
| `shared/entscheidungskerze.py` | **neu** — die Schicht, gut die Hälfte davon Begründung im Kopf |
| `shared/test_entscheidungskerze.py` | **neu** — 130 Prüfungen, 3 wirklich gestartete Bots, 9 Mutationsproben |
| `shared/umstellungstag.py` | **neu** — hält den Umstellungstag je Bot fest |
| `shared/test_umstellungstag.py` | **neu** — 25 Prüfungen |
| `shared/README_ENTSCHEIDUNGSKERZE.md` | **neu** |
| `docs/TESTAUFTRAG_TB-38_abrufschicht.md` | **neu** |
| `docs/ERGEBNIS_TB-38_abrufschicht.md` | **neu** |
| `docs/UEBERGABE_TB-38_abrufschicht.md` | **neu** (dieses Dokument) |
| 9 × `strategies/*/forward_test.py` | je +14/−1 bzw. +15/−1 |
| `shared/abrufschutz.py` | +17, **additiv ohne Verhaltensänderung** (ein öffentlicher Name für eine vorhandene private Funktion) |
| `docs/DATENLUECKEN.md` | neuer Abschnitt + Zäsur-Eintrag |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 4.8, offene Punkte 24–26, Fussnote zur Bot-Tabelle |
| `CLAUDE.md` | eine Zeile |
| `.gitignore` | Laufzeitzustand der Meldungen |

**Nicht angefasst:** `live_params.py` (alle neun), `broker/` (alles), die
Crontab, `data/` (alle 223 Dateien), `results/*.csv`,
`research/vorregistrierung/auswertung.py`,
`docs/VORREGISTRIERUNG_neuselektion.md`, `equity_simulation.py`,
`multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`,
`shared/zuteilung.py`, `messkette.py`, `regimewache.py`, `binance_historie.py`,
`kursdaten_neuaufbau.py`, `zeitabdeckung.py`, `fetch_binance_data.py`.

---

# Die vier Entscheidungen, um die gebeten wurde

### Wo gehört die Schicht hin? → **eigenes Modul in `shared/`, das `abrufschutz` benutzt**

Die **Regel** steht weiter genau einmal: `abrufschutz.abgeschlossen_maske`
(TB-35), zeichengleich mit `kursdaten_neuaufbau.abgeschlossene_kerzen`
(TB-34). Für Krypto ruft die Schicht sie auf und rechnet sie **nicht nach**.
Neu ist nicht die Regel, sondern die **Tür**.

Getrennt gehalten, weil die beiden Module **entgegengesetzte Fehlerrichtungen**
bewachen: `abrufschutz` schützt den Schreibpfad der acht `fetch_*.py` (zu
langes Warten kostet nichts, der teure Fehler ist eine Teilkerze in der CSV);
diese Schicht den Lesepfad der neun Bots (zu langes Warten kostet einen
Handelstag). Genau dieser Unterschied trägt auch die Aktien-Entscheidung unten
— in einem Modul liesse er sich nicht sauber begründen.

Nicht in `shared/kursdaten.py`, weil das eine andere Frage beantwortet
(„fehlen dieser Kerze die Kurse?"). Beide Fragen werden in `lade()`
nacheinander gestellt — über die **vorhandenen** Funktionen. Aus drei Wegen zu
denselben Daten ist damit **einer** geworden, kein vierter dazu.

### Wie kommt die Startzeit herein? → **Argument, im Prozess einmal eingefroren**

`laufbeginn()` merkt sich den Zeitpunkt beim ersten Gebrauch. Ein Wert, der
sich während des Laufs ändert, gäbe den ersten Symbolen Kerze N und den
restlichen N+1 — und weil alle neun Bots `open_count += 1` laufend hochzählen,
hinge das Ergebnis dann von der **Symbolreihenfolge** ab.

**Bewusst keine Umgebungsvariable.** Ein `export`, das jemand ins Shell-Profil
schreibt und vergisst, fröre alle neun Bots dauerhaft auf einer alten Kerze
ein — lautlos, denn ein eingefrorener Lauf sieht in den Zahlen aus wie „kein
Signal". Für Selbsttests gibt es `setze_laufbeginn()` und das Argument
`startzeit`; ein Test hält fest, dass die Schicht nie `os.getenv` benutzt.

### Wie kommt die Meldung im Wächter-Telegram an? → **`notify.send_alert()`, mit der Dämpfung aus TB-32**

Dieselbe und einzige Telegram-Leitung des Projekts. Keine zweite Anbindung,
keine Änderung an `notify.py`, kein Crontab-Eintrag (den es für diese Aufgabe
auch nicht geben durfte).

Gedämpft mit den **Funktionen** aus `notifications/waechter_melden.py` — nicht
mit einer zweiten Fassung derselben vier Regeln. Ohne Dämpfung wären es bei
dauerhaft veraltetem `data/` bis zu sechs Nachrichten am Tag, dauerhaft; nach
einer Woche wäre das dasselbe wie keine Meldung.

**Genau einmal je Lauf**, alle betroffenen Symbole in einer Nachricht. Der
Meldeteil steht vollständig in einem `try` und bringt den Bot nie zum
Scheitern; ein fehlgeschlagener Versand gilt als **nicht zugestellt** und wird
nachgeholt. Fehlt `waechter_melden`, wird **ungedämpft** gemeldet statt gar
nicht — eine Nachricht zu viel, nie eine verschluckte.

### Wohin gehört die maschinenlesbare Fassung des Umstellungstags? → **`docs/umstellungstag_entscheidungskerze.json`**

Nicht `shared/` oder `strategies/`: eine Datei neben dem Bot-Code lockt den
nächsten Leser dazu, sie im Live-Pfad zu benutzen — dann wäre eine Aufzeichnung
*über* den Betrieb zu einem Eingang *des* Betriebs geworden. Nicht `data/`:
das sind Kursdateien, und ihr SHA-256 bezeugt etwas anderes. Nicht `results/`:
das überschreibt der nächste Lauf.

In `docs/`, weil die Prosa-Fassung derselben Zäsur ein Verzeichnislisting
weiter in `docs/DATENLUECKEN.md` steht. Geschrieben von
`shared/umstellungstag.py` (Schritt 9 des Testauftrags), gelesen **vom
Vergleich, nicht von den Bots**.

Ein zweiter Aufruf rückt den Zeitpunkt **nicht** vor — der Umstellungstag ist
eine Tatsache, kein Zustand.

---

# Was geprüft wurde

| | |
|---|---|
| `shared/test_entscheidungskerze.py` | **130/130** |
| `shared/test_umstellungstag.py` | **25/25** |
| alle bestehenden Selbsttests | **unverändert** gegen den Basislauf auf `main` |

**Der Nachweis, der zählt:** Drei der neun `forward_test.py` werden im Test
**wirklich ausgeführt** — `t3_supertrend` (4 h), `turtle_soup_crypto` (1 d
Krypto) und `turtle_soup_stocks` (1 d Aktien) —, in einem Miniatur-Abbild des
Projekts unter `/tmp`, gegen erzeugte Beispieldaten. Beobachtet wird, was
danach in ihrer **Datenbank** steht. Der Zustand wird nicht von Hand
hergestellt: die Kursreihe trägt eine laufende Kerze mit einem Tief, das einen
Stop reissen *würde*, und ein Signal, das ein Bot eröffnen *würde*. Ob das
passiert, entscheidet der **Ablauf**.

**Dieselben Prüfungen gegen die unveränderten Bots von `main`: 7 von 13 fallen
durch** — `t3_supertrend` schliesst die Position als `stop_loss` mit
Ausstiegszeit `2026-09-15 20:00:00` (der laufenden Kerze), `turtle_soup_crypto`
eröffnet einen Trade auf der laufenden Tageskerze, `turtle_soup_stocks` auf der
Tageszeile von morgen. Genau der Befund, um den es geht.

**„Backtest und Forward-Test wählen dieselbe Kerze"** ist nicht gegen eine
nachgebaute Backtest-Regel geprüft, sondern gegen den **echten Schreibweg**:
was der Backtest liest, ist die CSV, die `fetch_*.py` schreibt, und die
schreibt seit TB-35 genau das, was `abrufschutz.nur_abgeschlossene`
durchlässt — eine Regel, die unabhängig von dieser Schicht entstanden ist.
Über rund **1 500 Zeitpunkte** (drei Intervalle × 95–195 Kerzen × 4
Zeitversätze) nennen beide Wege dieselbe letzte Kerze.

**Neun Mutationsproben.** Jede schaltet **eine** Absicherung ab und prüft
nach, dass genau die zugehörige Prüfung fehlschlägt — darunter die beiden
Fallen, die in diesem Projekt wiederkehren: der Filter wird **nur im
Rückfallweg** abgeschaltet (Normalfall bleibt grün, Rückfall fällt durch — die
eine Wache verdeckt das Fehlen der anderen nicht), und `entscheidung()` wird
auf „immer melden" gestellt (es *wird* dann gemeldet, also gibt es keine
zweite Wache daneben). Vorher wird geprüft, dass alle Proben ohne Mutation
grün sind.

---

# ⚠️ Der Befund, der an den Anfang gehört

**`data/` wird von keinem Cronjob aktuell gehalten — deshalb greift der
Rückfall heute bei sechs von neun Bots.**

Die Entscheidung des Betreibers lautet „die Forward-Tests lesen `data/` statt
live abzurufen". Das setzt voraus, dass etwas `data/` frisch hält. Das tut
derzeit nichts: für **keinen** der acht `fetch_*.py` gibt es einen
Crontab-Eintrag — sie wurden nur von Hand für Backtests gestartet, weil die
Bots ohnehin live abriefen.

Gemessen am 15.09.2026 (`python3 shared/entscheidungskerze.py`):

| | Dateien | Stand | Folge |
|---|---|---|---|
| `_1h` | **25/25 veraltet** | endet `2026-09-15 08:00`, erwartet `19:00` | `elliott_wave` fällt zurück |
| `_4h` | **24/24 veraltet** | endet `2026-09-15 04:00`, erwartet `16:00` | `t3_supertrend` fällt zurück |
| `_1d` Krypto | **24/24 frisch** | endet `2026-09-14` | drei Bots lesen `data/` |
| `_1d` Aktien | **150/150 veraltet** | endet `2026-09-01` | vier Bots fallen zurück |
| **gesamt** | **199 von 223 ohne die erwartete Kerze** | | |

**Das ist kein Schaden** — die Bots laufen weiter, rufen live ab wie bisher,
und der Filter greift auf **beiden** Wegen gleich. Es heisst nur, dass der
beabsichtigte Datenweg noch nicht wirkt und stattdessen eine (gedämpfte)
Telegram-Meldung je Bot entsteht.

**Zu entscheiden vom Betreiber:** Crontab-Einträge für die `fetch_*.py`,
zeitlich **vor** den zugehörigen Bot-Läufen. Ein Vorschlag steht in Schritt 8
des Testauftrags; TB-38 durfte die Crontab nicht anfassen und hat es nicht
getan. → Offener Punkt **24** im Übergabeprotokoll.

⚠️ Und der Grund, warum das nicht nebenbei erledigt wurde: `data/`
aufzufrischen **ändert den Datenstand-Hash der Vorregistrierung**. Das ist eine
Entscheidung, keine Aufräumarbeit.

---

# Was sonst offen bleibt

| # | Punkt |
|---|---|
| **25** | Schreibpfad (`<=`) und Lesepfad (`<`) unterscheiden sich um **eine Millisekunde** je Kerze. Das strikte `<` ist die Vorgabe der Aufgabe; kein Cron-Eintrag trifft diesen Zeitpunkt. Bewusst nicht angeglichen — eine Änderung an `abrufschutz` wäre eine Änderung am Datenstand-Hash. Als Test festgehalten (11.2), damit es niemand für eine Panne hält |
| **26** | Die **Lesart von `close_time`** ist eine Auslegung. Mit der Binance-Lesart (`open + Länge − 1 ms`, Feld 6) nimmt ein Lauf um 12:00:00 die soeben fertige 08:00-Kerze; mit der „natürlichen" Lesart dürfte er das nicht und wäre acht Stunden alt. Gebaut ist die Binance-Lesart. **Sollte einmal bewusst bestätigt werden** |
| — | Der **Nebenbefund zum Cron-Takt** (Fussnote 1 oben) ist aus der Cloud nur nach Aktenlage belegt. Schritt 2 des Testauftrags klärt ihn |
| — | Wie viele Trades der bisherige Papierpfad durch die Teilkerze anders eröffnet oder geschlossen hat, ist **nicht rekonstruierbar**: welche Werte eine Teilkerze im Augenblick des Laufs hatte, steht nirgends |

---

# Was als Nächstes zu tun ist

1. **`docs/TESTAUFTRAG_TB-38_abrufschicht.md` abarbeiten** — Schritt 1
   (Sicherung der neun Datenbanken) zuerst.
2. ⚠️ **Schritt 9 nicht überspringen:** `python3 shared/umstellungstag.py
   --festhalten --alle`. Er schreibt den Beginn des einzigen verwertbaren
   Vergleichsfensters auf. **Bis zum 13.12.2026 sind es 89 Tage, und ein
   zweites Fenster gibt es nicht.**
3. **Offenen Punkt 24 entscheiden**: Crontab-Einträge für die `fetch_*.py` —
   ja oder nein, und wenn ja, mit welchen Zeiten.
4. **Offenen Punkt 26 bestätigen**: ist die Binance-Lesart von `close_time`
   die gemeinte?

---

## In einfacher Sprache

**Was wir wissen wollten.**
Neun Handelsprogramme schauen sich Kursverläufe an und entscheiden dann:
kaufen, verkaufen oder nichts tun. Ein Kursverlauf wird in **Kerzen**
gezeichnet — jede fasst einen Zeitabschnitt zusammen, etwa vier Stunden oder
einen Tag. Fertig ist eine Kerze erst, wenn der Abschnitt vorbei ist. Die
Frage war: Schauen die Programme auf eine **fertige** Kerze — oder auf eine,
die gerade erst angefangen hat?

**Was herauskam.**
Fünf der neun schauten auf eine unfertige. Beim Vier-Stunden-Programm war
etwa die Hälfte des Zeitabschnitts noch gar nicht passiert. Die vier
Aktien-Programme machten es zufällig richtig — aber nur, weil sie zu einer
günstigen Uhrzeit laufen, nicht weil es ihnen jemand vorgeschrieben hätte.
Jetzt schauen alle neun auf die zuletzt fertige Kerze, und zwar nach einer
Regel, die an genau **einer** Stelle im Programm steht.

**Warum das so ist.**
Wenn man eine Strategie am Computer prüft, geht man die Vergangenheit durch —
dort ist jede Kerze fertig. Im laufenden Betrieb war es anders. Es wurde also
zwei Mal Verschiedenes gerechnet. Das ist deshalb schlimm, weil der laufende
Betrieb der **einzige** unabhängige Beweis dafür ist, dass eine Strategie
taugt: Prüfung und Wirklichkeit sollen dieselbe Sache messen, sonst kann die
Wirklichkeit die Prüfung gar nicht bestätigen.

**Was das für dich heisst.**
Drei Dinge:

1. **Der Vergleich „Prüfung gegen Wirklichkeit" fängt neu an.** Was vorher im
   laufenden Betrieb passiert ist, zählt dafür nicht mehr. Deshalb ist
   Schritt 9 der Testanleitung der wichtigste: er schreibt den Stichtag auf.
   Bis zum 13.12.2026 sind es 89 Tage.
2. **Die Programme sollen ihre Kurse aus einem gespeicherten Ordner lesen**
   statt jedes Mal im Internet nachzufragen. Dieser Ordner wird aber von
   nichts automatisch aufgefrischt. Solange das so bleibt, fragen sechs der
   neun weiter im Internet nach — **sie laufen also ganz normal weiter** —,
   und du bekommst eine Telegram-Nachricht, die dich darauf hinweist. Höchstens
   eine je Programm, und bei gleichbleibender Lage erst nach einer Woche
   wieder. Wie man den Ordner automatisch auffrischt, steht als Vorschlag in
   der Testanleitung; eintragen musst du das selbst.
3. **Nichts wurde an deinen Einstellungen geändert.** Keine Zahl, keine
   Schwelle, kein Stop, kein Zeitplan, keine Kursdatei. Nur die Frage „welche
   Kerze schaue ich an" wird jetzt überall gleich beantwortet.
