# Testauftrag TB-37 — Zugangsdaten trennen

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht.

**Alle Befehle sind einzeilig.** Termius auf dem iPhone verliert
Zeilenumbrüche in Heredocs und Python-Blöcken — hier kommt keiner vor.

---

> # ⚠️ DIE EINE REGEL: SICHERUNG VOR GIT
>
> **Schritt 0 und 1 laufen, BEVOR irgendein `git`-Befehl ausgeführt wird.**
>
> Das ist keine Vorsicht. Wir haben es nachgemessen: Wenn ein Commit eine
> Datei an einem Pfad hinzufügt, an dem lokal eine **gitignorierte** Datei
> liegt, überschreibt `git pull` sie **kommentarlos** — keine Rückfrage, keine
> Warnung, nur `create mode 100644` im Protokoll.
>
> `shared/fetch_binance_data.py` ist genau so eine Datei, und TB-37 fügt sie
> dem Repo hinzu. **Ein `git pull` ohne vorherige Sicherung löscht die einzige
> Kopie der Zugangsdaten.** Genau den Verlust, den TB-37 verhindern soll.
>
> Wer Schritt 0 überspringt, kann nichts davon rückgängig machen.

> # ⚠️ DIE ZWEITE REGEL: NIE ANZEIGEN
>
> Kein Befehl in diesem Testauftrag gibt einen Schlüssel aus. Geprüft wird
> immer mit **`grep -c`** (zählt) oder über das **Verhalten** — nie mit `cat`,
> nie mit `head`, nie mit `less`, nie mit einem Editor, dessen Inhalt im
> Terminal landet.
>
> Falls doch einmal etwas anders gemacht werden soll: **erst nachfragen.** Das
> Übergabeprotokoll hält zwei Vorfälle fest, bei denen ein echter Schlüssel im
> Chat landete und widerrufen werden musste.

---

## Was gebraucht wird

* Zugang zum MacBook mit dem Repo unter `~/trading-bot`
* `python3`, `pandas` und `python-binance` (im Betrieb vorhanden)
* Netz zu Binance (Schritt 7 und 9 rufen wirklich ab — **nur lesend**)
* Rund 25 Minuten

**Ergebnis-Ordner anlegen, dorthin kommen alle Protokolle:**

```bash
mkdir -p ~/Downloads/TB-37_zugangsdaten
```

---

## Schritt 0 — Sicherung. Zuerst. Vor allem anderen.

**Vorschlag für den Ort:** `~/Sicherungen/tb37_zugangsdaten/` — **außerhalb
des Repos**, damit kein `git`-Befehl und kein `.gitignore` sie je berühren
kann, und mit Rechten nur für den eigenen Benutzer.

```bash
mkdir -p ~/Sicherungen/tb37_zugangsdaten
```

```bash
chmod 700 ~/Sicherungen/tb37_zugangsdaten
```

```bash
cp -p ~/trading-bot/shared/fetch_binance_data.py ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt
```

```bash
cp -p ~/trading-bot/.env ~/Sicherungen/tb37_zugangsdaten/env.alt 2>/dev/null; echo "fertig (Fehlermeldung hier ist in Ordnung, falls es noch keine .env gibt)"
```

```bash
chmod 600 ~/Sicherungen/tb37_zugangsdaten/*
```

**Erwartet:** keine Ausgabe außer `fertig`.

**Falls `cp` meldet, dass `shared/fetch_binance_data.py` nicht existiert:**
**hier abbrechen und melden.** Dann ist die Ausgangslage eine andere als
angenommen, und der Rest dieses Testauftrags setzt sie voraus.

---

## Schritt 1 — Die Sicherung prüfen, ohne sie anzusehen

```bash
ls -l ~/Sicherungen/tb37_zugangsdaten/ > ~/Downloads/TB-37_zugangsdaten/01_sicherung.txt; cat ~/Downloads/TB-37_zugangsdaten/01_sicherung.txt
```

**Erwartet:** `fetch_binance_data.py.alt` mit einer Größe **größer als 0**.

```bash
grep -c "" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt
```

**Erwartet:** eine Zahl **größer als 0** — die Zeilenzahl. `grep -c ""` zählt
Zeilen und zeigt **keine** davon an.

```bash
shasum -a 256 ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt | cut -c1-16 | tee -a ~/Downloads/TB-37_zugangsdaten/01_sicherung.txt
```

**Erwartet:** 16 Zeichen. **Diese Zeichenfolge aufschreiben** — Schritt 11
(Rückweg) vergleicht dagegen. Eine Prüfsumme lässt sich nicht zurückrechnen;
sie verrät nichts über den Inhalt.

**Weicht etwas ab, oder ist die Datei leer:** **hier abbrechen und melden.**
Ab Schritt 3 ist die alte Datei weg.

---

## Schritt 2 — Wie heißen die Namen in der alten Datei?

Das ist der eine Punkt, den die Cloud nicht beantworten konnte. Geprüft wird
**nur gezählt**, nie angezeigt.

```bash
for n in BINANCE_API_KEY BINANCE_API_SECRET API_KEY API_SECRET api_key api_secret; do printf "%-22s %s\n" "$n" "$(grep -c "$n" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt)"; done | tee ~/Downloads/TB-37_zugangsdaten/02_namen.txt
```

**Erwartet — einer von zwei Fällen:**

| Fall | Zeigt sich als | Weiter mit |
|---|---|---|
| **A** (erwartet) | `BINANCE_API_KEY` und `BINANCE_API_SECRET` haben eine Zahl **≥ 1** | Schritt 5, Variante A |
| **B** | nur `API_KEY` / `API_SECRET` haben eine Zahl ≥ 1 | Schritt 5, Variante B |

Fall A ist der wahrscheinliche: `broker/zugang.py:101` führt seit jeher
`DATENABRUF_VARIABLEN = ("BINANCE_API_KEY", "BINANCE_API_SECRET")` und
bezeichnet sie ausdrücklich als die Schlüssel von
`shared/fetch_binance_data.py`.

**Zeigt keine der sechs Zeilen eine Zahl ≥ 1:** **hier anhalten und melden**,
mit dieser Tabelle — aber **ohne** die Datei zu öffnen. Dann sind die Namen
andere, und Schritt 5 muss angepasst werden.

---

## Schritt 3 — Der Datenstand VOR allem anderen

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft; print(herkunft.datenstand())" | tee ~/Downloads/TB-37_zugangsdaten/03_datenstand_vorher.txt
```

**Erwartet exakt:**

```
{'datenstand': 'd9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84', 'dateien': 223}
```

**Diese Zeile aufschreiben.** Schritt 10 vergleicht dagegen.

**Weicht sie ab:** **hier abbrechen und melden** — `data/` ist dann nicht der
Stand, auf den sich die Vorregistrierung bezieht.

---

## Schritt 4 — Basislauf und Stand herstellen

Erst der Basislauf auf dem **jetzigen** Stand, damit hinterher unterscheidbar
ist, was TB-37 verursacht hat und was vorher schon rot war.

```bash
cd ~/trading-bot && for f in $(find . -name "test_*.py" -not -path "./trading-env/*" | sort); do d=$(dirname "$f"); b=$(basename "$f"); out=$(cd "$d" && timeout 300 python3 "$b" 2>&1); printf "%-4s %-58s %s\n" "$?" "$f" "$(echo "$out" | grep -Ei 'bestanden|OK' | tail -1 | cut -c1-50)"; done | tee ~/Downloads/TB-37_zugangsdaten/04_basislauf_vorher.txt
```

**Erwartet:** 52 Zeilen. Welche rot sind, ist hier egal — die Datei ist der
Vergleichsmaßstab für Schritt 8.

Jetzt — **und erst jetzt, Schritt 0 und 1 müssen erledigt sein** — der Stand:

```bash
cd ~/trading-bot && git fetch origin && git checkout claude/new-session-d2nlap && git pull origin claude/new-session-d2nlap && git log --oneline -1
```

**Erwartet:** der jüngste TB-37-Commit.

**Falls `git checkout` wegen lokaler Änderungen scheitert:** `git stash` —
**nicht** `git checkout -- .`, solange unklar ist, was dort liegt.

```bash
grep -c "os.environ" ~/trading-bot/shared/fetch_binance_data.py
```

**Erwartet:** eine Zahl **≥ 1**. Das ist die neue, versionierte Datei — die
alte ist jetzt überschrieben. **Ihre Sicherung liegt in
`~/Sicherungen/tb37_zugangsdaten/`.**

---

## Schritt 5 — Übertragen, ohne durch den Chat oder den Bildschirm zu gehen

Die `.env` wird **ergänzt, nicht überschrieben** — dort stehen bereits die
Telegram- und Testnet-Angaben.

Zuerst nachsehen, ob schon etwas da ist:

```bash
grep -c "^BINANCE_API_KEY=" ~/trading-bot/.env 2>/dev/null; echo "(0 = noch nicht vorhanden, weiter; 1 = schon da, Schritt 5 überspringen)"
```

**Variante A** (Namen sind `BINANCE_API_*`, der erwartete Fall) — zwei Zeilen,
jede einzeln:

```bash
sed -n "s/^[[:space:]]*BINANCE_API_KEY[[:space:]]*=[[:space:]]*['\"]\([^'\"]*\)['\"].*/BINANCE_API_KEY=\1/p" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt >> ~/trading-bot/.env
```

```bash
sed -n "s/^[[:space:]]*BINANCE_API_SECRET[[:space:]]*=[[:space:]]*['\"]\([^'\"]*\)['\"].*/BINANCE_API_SECRET=\1/p" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt >> ~/trading-bot/.env
```

**Variante B** (Namen sind `API_KEY` / `API_SECRET`) — dieselben zwei Zeilen,
nur der gesuchte Name ist kürzer; geschrieben wird trotzdem der lange:

```bash
sed -n "s/^[[:space:]]*API_KEY[[:space:]]*=[[:space:]]*['\"]\([^'\"]*\)['\"].*/BINANCE_API_KEY=\1/p" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt >> ~/trading-bot/.env
```

```bash
sed -n "s/^[[:space:]]*API_SECRET[[:space:]]*=[[:space:]]*['\"]\([^'\"]*\)['\"].*/BINANCE_API_SECRET=\1/p" ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt >> ~/trading-bot/.env
```

`sed -n … >> datei` schreibt **ausschließlich in die Datei**. Auf dem
Bildschirm erscheint nichts.

```bash
chmod 600 ~/trading-bot/.env
```

---

## Schritt 6 — Prüfen, ohne anzuzeigen

```bash
grep -c '^BINANCE_API_KEY=.\{8,\}$' ~/trading-bot/.env; grep -c '^BINANCE_API_SECRET=.\{8,\}$' ~/trading-bot/.env
```

**Erwartet:** zweimal `1`. Gezählt wird, dass hinter dem Namen **mindestens
acht Zeichen** stehen — der Wert selbst erscheint nicht.

**Kommt zweimal `0`:** die Extraktion hat nichts gefunden (andere
Schreibweise in der alten Datei, etwa über mehrere Zeilen). **Nicht die Datei
öffnen** — melden, mit dem Ergebnis aus Schritt 2. Der Betrieb läuft
inzwischen weiter (siehe Schritt 7): fehlende Schlüssel blockieren nichts.

**Kommt `2` oder mehr:** Schritt 5 wurde doppelt ausgeführt. Kein Schaden —
der erste Treffer gewinnt —, aber aufräumen:
`grep -n '^BINANCE_API' ~/trading-bot/.env | cut -d: -f1` zeigt die
Zeilennummern (nur die Nummern, nicht die Werte).

```bash
cd ~/trading-bot && python3 shared/fetch_binance_data.py | tee ~/Downloads/TB-37_zugangsdaten/06_selbstbericht.txt
```

**Erwartet:**

```
.env erwartet unter: /Users/<name>/trading-bot/.env
.env vorhanden:      True
BINANCE_API_KEY        gesetzt
BINANCE_API_SECRET     gesetzt

Der Kursabruf braucht keinen Schluessel - er laeuft auch, wenn hier FEHLT steht.
```

Dieser Bericht sagt **ob**, nie **was**. Die Datei darf ins ZIP.

---

## Schritt 7 — Prüfen am Verhalten: der öffentliche Pfad **ohne** Schlüssel

Der eigentliche Nachweis. Der Abruf läuft hier **bewusst unangemeldet** —
läuft er durch, ist der Codepfad in Ordnung, und zwar unabhängig davon, ob
Schritt 5 geklappt hat.

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import fetch_binance_data as f; c=f.erzeuge_client(umgebung={}, pfad='/dev/null'); d=f.fetch_historical_data('BTCUSDT','1d','10 day ago UTC', client=c); print('Zeilen:', len(d)); print('Spalten:', list(d.columns)); print('letzte open_time:', d['open_time'].iloc[-1])" 2>&1 | tee ~/Downloads/TB-37_zugangsdaten/07_ohne_schluessel.txt
```

**Erwartet:**

* eine Zeile `[fetch_binance_data] HINWEIS: BINANCE_API_KEY, BINANCE_API_SECRET fehlt in der Umgebung…`
  — **genau einmal**, das ist die gewählte Meldung
* `Zeilen: 10` oder `11` (die laufende Kerze kommt mit)
* `Spalten: ['open_time', 'open', 'high', 'low', 'close', 'volume']`
* ein Zeitstempel von heute oder gestern

**Das ist der Befund:** der Kursabruf **braucht die Schlüssel nicht**. Der
Live-Betrieb kann durch fehlende Zugangsdaten nicht blockiert werden.

Zum Vergleich derselbe Abruf **mit** den Schlüsseln aus der `.env`:

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import fetch_binance_data as f; d=f.fetch_historical_data('BTCUSDT','1d','10 day ago UTC'); print('Zeilen:', len(d)); print('letzte open_time:', d['open_time'].iloc[-1]); print('letzter close:', d['close'].iloc[-1])" 2>&1 | tee ~/Downloads/TB-37_zugangsdaten/07b_mit_schluessel.txt
```

**Erwartet:** **dieselbe** Zeilenzahl und **dieselbe** letzte `open_time` wie
oben — und **keine** HINWEIS-Zeile.

**Weichen die Zeilenzahlen ab:** melden, mit beiden Dateien. Das wäre der
einzige Fall, in dem die Schlüssel für den Datenpfad doch eine Rolle spielen.

Und die Gegenprobe zum Verhalten bei einem unbekannten Symbol:

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); import fetch_binance_data as f; f.fetch_historical_data('GIBTESNICHTUSDT','1d','10 day ago UTC')" 2>&1 | tail -2 | tee ~/Downloads/TB-37_zugangsdaten/07c_leer.txt
```

**Erwartet:** die letzte Zeile nennt `AbrufLeer` (oder ein
`BinanceAPIException`, falls Binance das Symbol schon vorher zurückweist).
Der Abbruch mit einer Fehlermeldung ist hier das **gewünschte** Verhalten.
**Nicht** erwartet: eine leere Tabelle ohne Meldung — genau das soll nicht
mehr vorkommen.

---

## Schritt 8 — Gegenprobe: alle neun Aufrufer

### 8a — Die Selbsttests

```bash
cd ~/trading-bot && python3 shared/test_fetch_binance_data.py 2>&1 | tail -20 | tee ~/Downloads/TB-37_zugangsdaten/08a_selbsttest.txt
```

**Erwartet:** `77 von 77 Pruefungen bestanden, 0 fehlgeschlagen.`

Abschnitt 1 dieses Tests liest die **neun Aufrufer mechanisch** ein und prüft
die Signatur gegen sie — nicht gegen eine Liste von Hand.

### 8b — Das Gerüst, diesmal mit installiertem `python-binance`

```bash
cd ~/trading-bot && python3 research/zugangsdaten/geruest.py 2>&1 | tee ~/Downloads/TB-37_zugangsdaten/08b_geruest.txt | grep -E "Modul\(e\) binden|Gegen das installierte|ABWEICHEND|Zusammenfassung"
```

**Erwartet:** `9 Modul(e) binden sie ein, mit 9 Aufrufstelle(n).` und
`Gegen das installierte python-binance geprueft: stimmt ueberein.`

In der Cloud war die Zuordnung `KLINE_INTERVAL_* → '1h'/'4h'/'1d'`
**ungeprüft** (das Paket fehlt dort). Hier wird sie zum ersten Mal gegen das
Paket selbst nachgerechnet.

### 8c — Die vier `fetch_*.py` laufen wirklich — ohne `data/` anzufassen

```bash
cd ~/trading-bot && python3 research/abrufskripte/echtlauf.py --alle-krypto --symbole BTCUSDT 2>&1 | tail -30 | tee ~/Downloads/TB-37_zugangsdaten/08c_echtlauf.txt
```

**Erwartet:** Rückgabewert 0, alle vier Skripte durchgelaufen, letzte Kerze
jeweils **abgeschlossen**.

Das Werkzeug ist aus TB-35 und legt ein Miniatur-Abbild unter `mktemp -d` an,
in dem `DATA_DIR` woanders hinzeigt — **`data/` kann davon nicht erreicht
werden.** Es lädt `shared/fetch_binance_data.py` über eine Weiterleitung an
ihrem Ort; nach TB-37 ist das die neue Datei, und dass die Weiterleitung
weiterhin funktioniert, ist Teil dessen, was dieser Schritt zeigt.

### 8d — Die fünf `forward_test.py` werden **NICHT** ausgeführt

Sie würden Papier-Positionen eröffnen. Was hier geprüft wird, ist genau das,
was TB-37 an ihnen kaputtmachen könnte: dass der Import auflöst.

```bash
cd ~/trading-bot && for f in strategies/elliott_wave/forward_test.py strategies/rsi2_crypto/forward_test.py strategies/t3_supertrend/forward_test.py strategies/turtle_soup_crypto/forward_test.py strategies/volatility_breakout_crypto/forward_test.py; do python3 -m py_compile "$f" && printf "%-58s compile OK\n" "$f"; done | tee ~/Downloads/TB-37_zugangsdaten/08d_forward_tests.txt
```

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'shared'); from fetch_binance_data import fetch_historical_data as g; import inspect; print('Pflichtargumente:', [p.name for p in inspect.signature(g).parameters.values() if p.default is inspect.Parameter.empty])" | tee -a ~/Downloads/TB-37_zugangsdaten/08d_forward_tests.txt
```

**Erwartet:** fünfmal `compile OK` und
`Pflichtargumente: ['symbol', 'interval', 'lookback']`.

### 8e — Der volle Testlauf gegen den Basislauf

```bash
cd ~/trading-bot && for f in $(find . -name "test_*.py" -not -path "./trading-env/*" | sort); do d=$(dirname "$f"); b=$(basename "$f"); out=$(cd "$d" && timeout 300 python3 "$b" 2>&1); printf "%-4s %-58s %s\n" "$?" "$f" "$(echo "$out" | grep -Ei 'bestanden|OK' | tail -1 | cut -c1-50)"; done | tee ~/Downloads/TB-37_zugangsdaten/08e_testlauf_nachher.txt
```

```bash
diff ~/Downloads/TB-37_zugangsdaten/04_basislauf_vorher.txt ~/Downloads/TB-37_zugangsdaten/08e_testlauf_nachher.txt | tee ~/Downloads/TB-37_zugangsdaten/08f_diff.txt; echo "--- Ende diff"
```

**Erwartet:** als einziger Unterschied die **neue** Zeile
`shared/test_fetch_binance_data.py` mit Rückgabewert `0`. **53 Tests statt 52.**

**Steht dort ein Test, der vorher grün war und jetzt rot ist:** melden, mit
`08f_diff.txt`.

---

## Schritt 9 — Nachweisen, dass `data/` unberührt ist

```bash
cd ~/trading-bot && python3 -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft; print(herkunft.datenstand())" | tee ~/Downloads/TB-37_zugangsdaten/09_datenstand_nachher.txt
```

```bash
diff ~/Downloads/TB-37_zugangsdaten/03_datenstand_vorher.txt ~/Downloads/TB-37_zugangsdaten/09_datenstand_nachher.txt && echo "IDENTISCH - data/ unberuehrt"
```

**Erwartet:** `IDENTISCH - data/ unberuehrt`, Hash
`d9449faf51bffaaa…`, 223 Dateien.

**Weicht er ab:** melden. Dann hat ein Schritt entgegen der Absicht nach
`data/` geschrieben — das wäre ein Befund über den Testauftrag, nicht über
TB-37.

```bash
cd ~/trading-bot && git status --porcelain | grep -v "^??" | tee ~/Downloads/TB-37_zugangsdaten/09b_git_status.txt; echo "--- Ende"
```

**Erwartet:** **leer.** Keine geänderte verfolgte Datei.

---

## Schritt 10 — Die Frage dahinter, am echten Rechner

```bash
cd ~/trading-bot && python3 research/zugangsdaten/gitignoriert.py 2>&1 | tee ~/Downloads/TB-37_zugangsdaten/10_gitignoriert.txt | tail -25
```

**Erwartet:** `Ignorierten Quelltext gibt es noch: config/email_config.py` —
also **einen** statt vorher zwei.

```bash
ls -l ~/trading-bot/*.db ~/trading-bot/strategies/*/*.db 2>/dev/null | wc -l; echo "Handelsdatenbanken gefunden (gitignoriert, existieren nur hier)"
```

**Erwartet:** eine Zahl um 9. **Diese Zahl bitte melden** — es ist der Posten,
den der Bericht als größten offenen Punkt nennt.

---

## Schritt 11 — Der Rückweg, falls etwas klemmt

**Er funktioniert zu jedem Zeitpunkt** — die Sicherung aus Schritt 0 ist
unabhängig vom Repo.

Nur die Zugangsdaten zurückholen (der häufigere Fall):

```bash
cp -p ~/Sicherungen/tb37_zugangsdaten/env.alt ~/trading-bot/.env 2>/dev/null; echo fertig
```

Den **alten Zustand vollständig** wiederherstellen:

```bash
cd ~/trading-bot && git checkout main && git pull origin main
```

```bash
cp -p ~/Sicherungen/tb37_zugangsdaten/fetch_binance_data.py.alt ~/trading-bot/shared/fetch_binance_data.py
```

```bash
shasum -a 256 ~/trading-bot/shared/fetch_binance_data.py | cut -c1-16
```

**Erwartet:** **dieselben 16 Zeichen wie in Schritt 1.** Stimmen sie überein,
ist die alte Datei zeichengenau zurück.

> ⚠️ Auf `main` steht `shared/fetch_binance_data.py` wieder in `.gitignore` —
> die zurückgelegte Datei ist dort also wieder unversioniert, und alles ist
> wie vorher. **Die Sicherung in `~/Sicherungen/tb37_zugangsdaten/` erst
> löschen, wenn TB-37 endgültig angenommen ist.**

---

## Schritt 12 — Ergebnisse einpacken

```bash
cd ~/Downloads && zip -r TB-37_zugangsdaten_ergebnisse.zip TB-37_zugangsdaten && ls -l ~/Downloads/TB-37_zugangsdaten_ergebnisse.zip
```

**Erwartet:** eine ZIP-Datei in `~/Downloads` — **nicht** im Repo.

> ⚠️ **Vor dem Verschicken:** Das ZIP enthält keine Schlüssel — kein Befehl
> dieses Testauftrags gibt einen aus. Zur Sicherheit einmal gegenzählen:

```bash
v=$(grep -m1 '^BINANCE_API_KEY=' ~/trading-bot/.env | cut -d= -f2-); if [ -n "$v" ]; then grep -rl -- "$v" ~/Downloads/TB-37_zugangsdaten/ 2>/dev/null | wc -l; else echo "kein Schluessel gesetzt - nichts zu pruefen"; fi; unset v
```

**Erwartet:** `0` — keine Datei im Ergebnis-Ordner enthält den Schlüssel.

Der Befehl zeigt ihn nicht an: er reicht ihn in einer Variablen direkt an
`grep` weiter, gibt nur die **Anzahl** der Treffer aus und löscht die Variable
danach wieder. Die Abfrage `[ -n "$v" ]` ist wichtig — wäre der Wert leer,
passte das Suchmuster auf **jede** Zeile und meldete falschen Alarm.

---

## Zusammenfassung zum Melden

| Schritt | Was | Ergebnis |
|---|---|---|
| 1 | Sicherung angelegt und geprüft | Prüfsumme: ……………… |
| 2 | Namen in der alten Datei | Fall A / Fall B / anders |
| 3 | Datenstand vorher | `d9449faf…` / abweichend |
| 6 | `.env` ergänzt, beide Namen gesetzt | ja / nein |
| 7 | Abruf **ohne** Schlüssel | Zeilen: …… |
| 7b | Abruf **mit** Schlüssel | Zeilen: …… (gleich?) |
| 8a | Selbsttests | ……/77 |
| 8c | vier `fetch_*.py` echt gelaufen | rc = …… |
| 8e | 53 Tests, nichts neu rot | ja / nein |
| 9 | `data/` unberührt | IDENTISCH / abweichend |
| 10 | Handelsdatenbanken gefunden | …… Stück |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob die Umstellung auf dem MacBook wirklich funktioniert. Wir haben sie in der
Cloud gebaut und dort geprüft, so weit es ging — aber die Datei mit den
Passwörtern konnten wir von dort nie sehen. Ob die Passwörter da
hineinkommen, wo sie hin sollen, und ob danach alle neun Programme weiter
funktionieren, kann nur der Rechner beantworten, auf dem sie liegen.

**Was herauskam.**
Das steht nach dem Durchlauf in der Tabelle darüber. Zwei Zahlen sind die
wichtigsten: In Schritt 7 soll der Kursabruf **auch ohne Passwort** Daten
liefern — dann kann ein vergessenes Passwort den Betrieb nie stoppen. Und in
Schritt 8e sollen alle Tests, die vorher funktionierten, weiter funktionieren.

**Warum das so ist.**
Die Passwörter zogen bisher in derselben Datei mit wie das Programm. Deshalb
durfte die ganze Datei nicht gesichert werden — und existierte nur einmal.
Jetzt wohnen sie getrennt: Programm im Sicherungssystem, Passwörter in einer
eigenen kleinen Datei namens `.env`, die auf dem Rechner bleibt.

**Was das für dich heißt.**
Die Schritte der Reihe nach abarbeiten und **Schritt 0 nicht überspringen** —
das ist die Sicherheitskopie. Wir haben nachgemessen, dass das Update die alte
Datei **ohne Rückfrage und ohne Meldung** überschreibt; wer zuerst kopiert,
kann jederzeit zurück (Schritt 11), wer es vergisst, nicht. Kein Befehl in
dieser Anleitung zeigt jemals ein Passwort auf dem Bildschirm — und wenn
irgendwo doch eines auftauchen sollte, ist das ein Fehler in dieser Anleitung
und bitte zu melden. Am Ende (Schritt 12) entsteht eine ZIP-Datei in
`~/Downloads`, die alle Protokolle enthält; die gehört **nicht** ins
Sicherungssystem, sondern nur zum Zurückschicken.
