# Testauftrag TB-30a — Vorregistrierung der Neuselektion

**Autonom ausführbar.** Jeder Schritt steht für sich, mit erwarteter Ausgabe.
Die Schritte 1 bis 7 laufen ohne Zutun; **8 und 9 muss der Betreiber selbst
ausführen** (GPG-Schlüssel bzw. Netzzugang).

> **Kein Befehl in diesem Dokument startet einen Selektionslauf.** Wer eine
> Rasterausgabe sieht, hat einen fremden Befehl erwischt.

**Ein Befehl nach dem anderen**, jeweils die Ausgabe prüfen, dann der
nächste.

---

## Vorbereitung

```bash
cd ~/trading-bot
source trading-env/bin/activate
```

Erwartet: die Eingabeaufforderung beginnt mit `(trading-env)`.

---

## Schritt 1 — Nichts Verbotenes angefasst

```bash
git diff origin/main HEAD --name-only | cut -d/ -f1 | sort -u
```

**Erwartet:** genau drei Zeilen — `docs`, `research`, `shared`. Nichts
anderes.

```bash
git diff origin/main HEAD --name-only | grep -E "live_params|forward_test|equity_simulation|multi_symbol_" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`. (`grep` gibt 1 zurück, wenn es
nichts findet — hier ist das die gute Nachricht.)

```bash
git diff origin/main HEAD --name-only | grep -E "^(results|broker|config|data)/|zuteilung|messkette" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`.

---

## Schritt 2 — Die Rastergrenzen: kein Grenzsatz nennt einen Live-Wert

```bash
python3 research/vorregistrierung/pruefe_grenzsaetze.py
echo "Rueckgabewert: $?"
```

**Erwartet:**

```
395/395 Pruefungen bestanden.

Kein Grenzsatz erwaehnt einen Live-Wert; jede Grenze ist gerechnet.
Rueckgabewert: 0
```

**Was hier geprüft wird** (vier Wachen, die unabhängig voneinander scheitern):

1. jede Grenze wird aus ihrer Regel **neu ausgerechnet** und mit dem
   ausgewiesenen Wert verglichen,
2. kein Begründungssatz enthält eine Zahl, die ein Live-Wert dieses Bots ist,
3. jede Grenze hat eine zugelassene Grundlage,
4. die Stufung ist die versprochene (geometrischer Faktor 1,5 bis 2,0,
   ganzzahlig-linear bei Zählparametern).

### Gegenprobe (die Wache muss rot werden können)

```bash
cp research/vorregistrierung/registerdaten.py /tmp/rd.bak
sed -i '' 's/"Ein Stop enger als ein halbes Tages-Sigma des Universums wird vom "/"Ein Stop enger als 8.0 Prozent wird vom "/' research/vorregistrierung/registerdaten.py
python3 research/vorregistrierung/pruefe_grenzsaetze.py > /tmp/gegenprobe.txt
echo "Rueckgabewert: $?"
tail -7 /tmp/gegenprobe.txt
```

**Erwartet:** `Rueckgabewert: 1` und genau **fünf** gemeldete Verstösse — bei
den fünf Bots, die 8,0 als Live-Wert führen:

```
390 bestanden, 5 GESCHEITERT:
  - elliott_wave_stocks/stop_loss_pct[unten]: Satz nennt keinen Live-Wert - nennt [8.0]
  - rsi2_crypto/stop_loss_pct[unten]: Satz nennt keinen Live-Wert - nennt [8.0]
  - turtle_soup_crypto/stop_mode[unten]: Satz nennt keinen Live-Wert - nennt [8.0]
  - volatility_breakout/stop_loss_pct[unten]: Satz nennt keinen Live-Wert - nennt [8.0]
  - volatility_breakout_crypto/stop_loss_pct[unten]: Satz nennt keinen Live-Wert - nennt [8.0]
```

**Dass es nur fünf sind, gehört zur Probe:** die vier übrigen Bots führen
keine 8,0, bei ihnen ist derselbe Satz unauffällig. Eine Wache, die immer
anschlägt, prüft nichts.

*(`echo "Rueckgabewert: $?"` steht bewusst VOR dem `tail` — hinter einer Pipe
meldete `$?` den Rückgabewert von `tail`, also immer 0.)*

**Danach unbedingt zurücksetzen:**

```bash
cp /tmp/rd.bak research/vorregistrierung/registerdaten.py
python3 research/vorregistrierung/pruefe_grenzsaetze.py | tail -2
```

**Erwartet:** wieder `395/395 Pruefungen bestanden.`

---

## Schritt 3 — Das Register stimmt mit dem Code überein

```bash
python3 research/vorregistrierung/registerbericht.py --pruefen
echo "Rueckgabewert: $?"
```

**Erwartet:**

```
Der Zahlenteil des Registers stimmt mit dem Code ueberein.
Rueckgabewert: 0
```

Der Zahlenteil von `docs/VORREGISTRIERUNG_neuselektion.md` (Abschnitt 3) ist
**erzeugt, nicht abgetippt**. Weicht er ab, ist das Register veraltet, und
dieser Befehl sagt es.

---

## Schritt 4 — Der Selbsttest der Vorregistrierung

```bash
python3 research/vorregistrierung/test_vorregistrierung.py
echo "Rueckgabewert: $?"
```

**Erwartet:** `150/150 Pruefungen bestanden.`, Rückgabewert 0. Läuft rund
zwei bis vier Minuten (Teil H startet acht eigene Prozesse).

**Was in den acht Teilen steckt:**

| Teil | Prüft |
|---|---|
| A | Das Auswertungsskript läuft gegen erzeugte Beispieldaten — ohne dass echte Ergebnisse existieren. Fehlt eine Zelle oder eine Tagesreihe, **bricht es ab** statt zu schätzen |
| B | Plateau-Regel: eine isolierte Spitze gewinnt **nicht**, ein Plateau gewinnt. Dazu: das Plateau-Mittel zählt den Punkt selbst mit, der Spitzentest **nicht** |
| C | Kantenregel: ein Gewinner auf der Kante wird markiert, das Raster wird **nicht** erweitert |
| D | Drawdown-Bedingung in **beide** Richtungen: die relative Grenze bindet in der Krisenfalte, `DD_Toleranz` rettet die ruhige |
| E | **Jedes** Abbruchkriterium (a)–(d) einzeln, jeweils mit einem Fall, in dem **nur** dieses greift — plus die Gegenprobe zu (c) und (d) |
| F | Falten ohne Trade zählen mit Sharpe 0 — auch wenn in der Datei ein schöner Wert steht |
| G | Maschinelle Prüfung der Grenzsätze, des Faltenplans, der Purge-Längen und der Zweijahres-Regel |
| H | **Mutationsproben am Ablauf**: der ganze Ordner wird kopiert, **eine** Zeile geändert, und der Lauf auf denselben Beispieldaten neu gestartet |

**Zu Teil H, weil es der Teil ist, auf den es ankommt.** Eine Probe, deren
Zustand der Test von Hand herstellt, bestätigt sich selbst. Hier wird
deshalb nichts im laufenden Prozess umgebogen; beobachtet wird, ob ein
anderer **Prozess** ein anderes **Urteil** fällt. Und: die Proben H5 und H6
zeigen, dass die beiden Wachen aus Schritt 2 sich **nicht gegenseitig
decken** — H6 entfernt die zweite Wache und weist nach, dass derselbe Fehler
dann durchkommt. Eine Wache, deren Wegfall nichts ändert, wäre keine.

---

## Schritt 5 — Die Regimewache (Befund AB2/U5)

```bash
python3 shared/test_regimewache.py
echo "Rueckgabewert: $?"
```

**Erwartet:** `16/16 Pruefungen bestanden.` und

```
Einbaustand: 0 von 3 Stellen - offen: ['strategies/t3_supertrend/equity_simulation.py',
 'strategies/t3_supertrend/multi_symbol_optimise.py',
 'strategies/volatility_breakout_crypto/equity_simulation.py']
```

**Der Einbaustand `0 von 3` ist richtig so.** TB-30a darf die drei Dateien
nicht anfassen; der Einbau ist TB-30b. Die Wache selbst ist fertig und
geprüft.

**Wichtig:** Teil C dieses Tests wird **rot**, sobald TB-30b den Einbau
gemacht hat — dann ist der Befund erledigt, und der Test stellt sich selbst
um (er prüft dann die andere Richtung). Das ist kein Fehlalarm.

---

## Schritt 6 — Agent 2 wählt auf dem führenden Mass

```bash
python3 shared/test_agent2_kapitalmass.py 2>&1 | tail -3
echo "Rueckgabewert: $?"
```

**Erwartet:** `34/34 Pruefungen bestanden.`, Rückgabewert 0.

```bash
python3 shared/test_agent2_zielfunktion.py 2>&1 | tail -3
```

**Erwartet:** `41 von 41 Pruefungen bestanden, 0 fehlgeschlagen.` — die
Zusicherungen aus TB-22 gelten unverändert weiter.

**Was sich geändert hat:** Der fest verdrahtete Satz *„es gilt das
chronologische"* ist weg. An seine Stelle tritt eine dreistufige Kaskade;
**heute greift Stufe 2** (der Stellvertreter), weil der Kapital-Drawdown noch
in keiner Rasterausgabe steht. Der Agent weist den Ersatz jetzt **als Ersatz
aus** und schaltet von selbst um, sobald TB-30b das Feld nachrüstet.

Sichtbar machen:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "shared")
import types
sys.modules["anthropic"] = types.ModuleType("anthropic")
import param_search_agent as a
print(a.zielmass_baustein("chronologisch"))
PY
```

**Erwartet:** ein Block, der mit `ZIELGROESSE DER AUSWAHL:` beginnt und
`ACHTUNG: max_drawdown_kapital_pct ... liegt in diesen Ergebnissen NICHT vor`
enthält.

---

## Schritt 7 — Herkunft und Verankerung

```bash
python3 research/vorregistrierung/herkunft.py
echo "Rueckgabewert: $?"
```

**Erwartet:** eine Übersicht mit Commit-, Datenstand- und Register-Hash und

```
  Verankerung:
    OFFEN  signierter_tag                   (Betreiber (GPG-Schluessel))
    OFFEN  zeitanker_opentimestamps         (Betreiber (Netzzugang))
    JA   herkunft_in_ergebnisdateien      (dieses Modul)
    JA   urteil_ist_code                  (dieses Repo)
```

Die beiden `OFFEN` sind die Schritte 8 und 9.

**Die drei Hashes notieren** — sie werden in Schritt 9 gebraucht:

```bash
python3 research/vorregistrierung/herkunft.py --json > /tmp/tb30a_herkunft.json
python3 -c "import json;d=json.load(open('/tmp/tb30a_herkunft.json'))['herkunft'];print('Register :',d['register']);print('Daten    :',d['datenstand']);print('Commit   :',d['commit'])"
```

---

## Schritt 8 — Signierter Tag (nur Betreiber, braucht den GPG-Schlüssel)

**Warum ein signierter Tag:** Er bindet den Zustand an einen **Schlüssel**
statt an einen editierbaren Zeitstempel. Ein gewöhnlicher Tag lässt sich
verschieben; ein signierter wäre danach ungültig.

Erst prüfen, ob ein Schlüssel da ist:

```bash
gpg --list-secret-keys --keyid-format LONG
```

**Erwartet:** mindestens ein `sec`-Eintrag. Steht dort nichts, ist zuerst ein
Schlüssel anzulegen (`gpg --full-generate-key`) und in git zu hinterlegen
(`git config --global user.signingkey <ID>`).

Dann — **nachdem der Pull Request gemergt ist** und `main` den Stand trägt:

```bash
git checkout main
git pull origin main
git tag -s TB-30a-vorregistrierung -m "Vorregistrierung der Neuselektion, eingefroren"
git tag -v TB-30a-vorregistrierung
```

**Erwartet bei `-v`:** `gpg: Good signature from "<Ihr Name>"`.

```bash
git push origin TB-30a-vorregistrierung
```

Gegenprobe:

```bash
python3 research/vorregistrierung/herkunft.py | grep signierter_tag
```

**Erwartet:** die Zeile beginnt jetzt mit `JA`.

---

## Schritt 9 — Externer Zeitanker (nur Betreiber, braucht Netz)

**Warum:** Ein Hash im eigenen Repo belegt, *dass* etwas zusammengehört, aber
nicht, *wann* es entstand. OpenTimestamps verankert einen Hash in der
Bitcoin-Blockchain — ein Zeitpunkt, den niemand nachträglich verschieben
kann, auch nicht der Betreiber.

Einmalig installieren:

```bash
pip install opentimestamps-client
```

Zwei Dateien mit den beiden Hashes anlegen und stempeln:

```bash
python3 -c "import json;d=json.load(open('/tmp/tb30a_herkunft.json'))['herkunft'];open('research/vorregistrierung/ergebnisse/register.hash','w').write(d['register']+'\n');open('research/vorregistrierung/ergebnisse/datenstand.hash','w').write(d['datenstand']+'\n')"
ots stamp research/vorregistrierung/ergebnisse/register.hash
ots stamp research/vorregistrierung/ergebnisse/datenstand.hash
```

**Erwartet:** je eine Zeile `Submitting to remote calendar …` und zwei neue
Dateien `*.hash.ots`.

**Der Stempel braucht einige Stunden, bis er bestätigt ist.** Danach:

```bash
ots verify research/vorregistrierung/ergebnisse/register.hash.ots
```

**Erwartet:** `Success! Bitcoin block <Nummer> attests existence as of <Datum>`.

Die vier Dateien (`*.hash`, `*.hash.ots`) gehören in einen eigenen, kleinen
Commit auf `main`. Gegenprobe:

```bash
python3 research/vorregistrierung/herkunft.py | grep zeitanker
```

**Erwartet:** die Zeile beginnt jetzt mit `JA`.

---

## Schritt 10 — Das append-only-Protokoll

Für jeden künftigen Lauf **eine** Zeile:

```bash
python3 research/vorregistrierung/herkunft.py --anhaengen "einfrieren"
```

**Erwartet:** ein JSON-Block mit `commit`, `datenstand`, `register`,
`vorgaenger` und `kette`.

Die Kette prüfen:

```bash
python3 research/vorregistrierung/herkunft.py | tail -2
```

**Erwartet:** `Protokoll     keine Kettenfehler`.

**Warum append-only:** Ein überschreibbares Protokoll beantwortet die einzige
Frage nicht, für die es da ist — *wurde zwischendurch noch einmal gerechnet?*
Jede Zeile trägt den Hash der vorigen; eine entfernte oder geänderte Zeile
bricht die Kette sichtbar.

---

## Schritt 11 — Der Basislauf auf unverändertem `main`

**Bevor Sie einen Fehlschlag der übrigen Tests dieser Aufgabe zuschreiben:**
mehrere Tests des Repos scheitern in dieser Umgebung schon ohne jede
Änderung. Nachweisen:

```bash
git stash --include-untracked
for t in $(find . -name "test_*.py" | sort); do d=$(dirname $t); b=$(basename $t);
  (cd $d && python3 $b >/dev/null 2>&1); printf "%-60s rc=%s\n" "$t" "$?"; done
git stash pop
```

**Erwartet auf `main` (gemessen am 14.09.2026, 12 Fehlschläge):**

| Test | Grund |
|---|---|
| `broker/test_ibkr.py` | Zeitzone `US/Eastern` fehlt |
| `dashboard/test_dashboard.py` | `fastapi` fehlt |
| `dashboard/test_portfolio_sicht.py` | 66 von 68 — vorbestehend |
| `research/drawdown_reihenfolge/test_drawdown.py` | Bot-Abhängigkeiten |
| `research/elliott_wave_params/test_params.py` | Bot-Abhängigkeiten |
| `research/fib_score_stufen/test_stufen.py` | Bot-Abhängigkeiten |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt |
| `shared/test_kursdaten.py` | 62 von 66 — vorbestehend |
| `shared/test_stabile_sortierung.py` | 45 von 46 — vorbestehend |
| `shared/test_wellenauswahl.py` | 322 von 323 — vorbestehend |
| `system/test_dienst_plists.py` | `StandardErrorPath ist absolut` — vorbestehend |

**Dieselben elf, keiner mehr**, müssen auch auf dem Branch scheitern. Ohne
`node` meldet `dashboard/test_dashboard.py` ausserdem 780 statt 784
Prüfungen — hier fällt es ohnehin an `fastapi` aus.

### Ein zwölfter, der nicht zählt: `system/test_log_rotation.py`

Dieser Test startet einen **nebenläufigen Schreiberprozess** und wartet
darauf, dass die Protokolldatei eine Mindestgrösse erreicht
(`_warte_auf_groesse`). Unter Last — etwa wenn wie oben die ganze Testreihe
hintereinander läuft — erreicht sie die Grösse nicht rechtzeitig, und drei
Prüfungen schlagen fehl. Einzeln aufgerufen besteht er zuverlässig:

```bash
cd system && python3 test_log_rotation.py | tail -2
```

**Erwartet:** `117 von 117 Pruefungen bestanden, 0 fehlgeschlagen.`

Er ist damit **zeitabhängig, nicht kaputt** — und er hängt an nichts, was
TB-30a anfasst (`system/` ist unberührt). Wer ihn in einer Reihe scheitern
sieht, ruft ihn einzeln auf, bevor er daraus etwas schliesst.

---

## Schritt 12 — Was NICHT passiert sein darf

```bash
ls research/vorregistrierung/ergebnisse/
```

**Erwartet:** `benchmark_drawdowns.json`, `faltenplan.json`,
`messgroessen.json` — und **kein** Rasterergebnis, keine `*_raster.csv`,
keine Zelle mit einem Sharpe eines echten Bots.

```bash
git status --porcelain results/
```

**Erwartet:** keine Zeile. Die abgelegten Ergebniskurven sind unberührt.

> **Hinweis, damit daraus nicht der falsche Schluss gezogen wird:** Auf `main`
> sind die `results/*/equity_curve.csv` veraltet, weil ein lokaler Commit
> nicht gepusht ist; auf Ihrem Mac melden sie `9x AKTUELL`. Daraus folgt
> **nicht**, dass hier etwas nachzuziehen wäre.

---

## Wenn etwas nicht stimmt

| Beobachtung | Bedeutung |
|---|---|
| Schritt 2 meldet einen Verstoss | Eine Rastergrenze oder ein Grenzsatz wurde verändert. **Das Register ist dann nicht mehr eingefroren** — nachsehen, was sich geändert hat, bevor irgendetwas läuft |
| Schritt 3 meldet ein veraltetes Register | Der Code hat sich bewegt, das Dokument nicht. Neu erzeugen mit `registerbericht.py` und den Block im Register ersetzen |
| Schritt 4 scheitert in Teil H | Eine Mutationsprobe hat **nicht** angeschlagen: eine Wache trägt nicht mehr. Das ist ernster als ein gescheiterter Sachtest |
| Schritt 5 meldet `3 von 3 Stellen` eingebaut | TB-30b ist gelaufen. Dann darf der Selektionslauf starten |
| Schritt 7 meldet `Arbeitsbaum GEAENDERT` | Auf einem schmutzigen Baum ist kein Lauf reproduzierbar. Erst committen |
