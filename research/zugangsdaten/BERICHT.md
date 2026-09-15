# TB-37 — Zugangsdaten trennen: Code ins Repo, Schlüssel hinaus

**Stand:** 15.09.2026 · **Basis:** `main` bei `e23e38f` (TB-36, PR #109)
**Werkzeuge:** `geruest.py` (was muss der versionierte Teil können?),
`gitignoriert.py` (woran hängt das System, das es nur einmal gibt?)

---

## 0. Die zwei Dinge zuerst

### Die neun Module, die an der Datei hängen

Mechanisch über den Syntaxbaum ermittelt (`python3 research/zugangsdaten/geruest.py`),
nicht aus dem Gedächtnis. **Alle neun** binden sie identisch ein
(`from fetch_binance_data import fetch_historical_data`) und rufen sie mit
**genau drei Argumenten der Reihe nach** auf — keines benannt, keines mit
`*`/`**`:

| # | Modul | Import | Aufruf | Intervall | Lookback | Was mit dem Ergebnis geschieht |
|---|---|---|---|---|---|---|
| 1 | `shared/fetch_multi_data.py` | Z. 40 | Z. 64 | `1h` | `1 Jan, 2017` | → CSV (Z. 77) |
| 2 | `strategies/elliott_wave/forward_test.py` | Z. 42 | Z. 208 | `1h` | `90 day ago UTC` | **Handelsentscheidung** (Z. 157/158) |
| 3 | `strategies/rsi2_crypto/fetch_1d_data.py` | Z. 51 | Z. 82 | `1d` | `1 Jan, 2017` | → CSV (Z. 95) |
| 4 | `strategies/rsi2_crypto/forward_test.py` | Z. 40 | Z. 229 | `1d` | `400 day ago UTC` | **Handelsentscheidung** (Z. 160) |
| 5 | `strategies/t3_supertrend/fetch_4h_data.py` | Z. 45 | Z. 66 | `4h` | `1 Jan, 2017` | → CSV (Z. 79) |
| 6 | `strategies/t3_supertrend/forward_test.py` | Z. 31 | Z. 193 | `4h` | `120 day ago UTC` | **Handelsentscheidung** (Z. 132/207) |
| 7 | `strategies/turtle_soup_crypto/forward_test.py` | Z. 48 | Z. 234 | `1d` | `400 day ago UTC` | **Handelsentscheidung** (Z. 157) |
| 8 | `strategies/volatility_breakout_crypto/fetch_1d_data.py` | Z. 47 | Z. 78 | `1d` | `1 Jan, 2017` | → CSV (Z. 91) |
| 9 | `strategies/volatility_breakout_crypto/forward_test.py` | Z. 45 | Z. 242 | `1d` | `400 day ago UTC` | **Handelsentscheidung** (Z. 170/258) |

**Vier** schreiben das Ergebnis nach `data/` — dort bleibt ein Fehler dauerhaft
stehen. **Fünf** hängen eine Handelsentscheidung an `df.iloc[-1]`, die jüngste
Kerze — das sind die fünf Bots des täglichen Live-Betriebs.

Daraus folgt die Signatur, die der versionierte Teil erfüllen **muss**, damit
kein Aufrufer angefasst werden muss:

```python
def fetch_historical_data(symbol, interval, lookback)
```

Mehr Stellen dürfen dahinter stehen, solange sie Vorgaben haben — weniger
nicht.

### Die Zusicherungen, die an ihr hängen

| Zusicherung | Woher belegt |
|---|---|
| **Spalten** `open_time, open, high, low, close, volume`, in dieser Reihenfolge, **ohne** `close_time` | Nachgerechnet an den Dateien unter `data/` (223 Stück) — `close_time` kommt in keiner vor. `shared/abrufschutz.py` rechnet den Kerzenschluss deshalb aus `open_time` + Intervall aus. |
| **Schreibweise** `2017-08-17 04:00:00` (1h/4h), `2017-08-17` (1d) | Ebenfalls an den Dateien. Der Selbsttest schreibt eine erzeugte Kerze durch `to_csv` und vergleicht **zeichengleich** gegen die erste Zeile von `data/BTCUSDT_{1h,4h,1d}.csv`. |
| **Zahlen als `float`**, nicht als Zeichenkette | In den Dateien steht `4427.3`, Binance liefert `"4427.30000000"`. Als Zeichenkette durchgereicht stünde letzteres in der CSV — jede Zeile zeichenverschieden, **Datenstand-Hash neu, kein Kurs anders.** |
| **Reihenfolge** aufsteigend nach `open_time` | Jeder der fünf Aufrufer, der `df.iloc[-1]` als „die jüngste Kerze" liest, setzt es voraus. |
| **Die laufende Kerze IST enthalten** | TB-35-Befund. `abrufschutz.nur_abgeschlossene` schneidet sie in den vier `fetch_*.py` **vor** dem Schreiben ab; die fünf `forward_test.py` **wollen** sie. Würde der Abruf selbst filtern, wäre `abrufschutz` wirkungslos und die Bots handelten auf einer anderen Kerze. |
| **Vollständigkeit** über die 1000-Kerzen-Grenze hinaus | `1 Jan, 2017` bei 1h sind rund 80 000 Kerzen; die Dateien enthalten sie. Der Abruf blättert also. |

### Und was **nicht** erschließbar war

Fünf Punkte. Sie stehen so auch im Werkzeug (`geruest.py`, Abschnitt 6) und
sind dort als **unbekannt** ausgewiesen, nicht als Vermutung:

1. **Ratenbegrenzung** — ob die alte Datei drosselt. `fetch_multi_data.py`
   pausiert selbst (`PAUSE_BETWEEN_REQUESTS_SEC = 0.5`); daraus folgt weder
   das eine noch das andere.
2. **Wiederholversuche** — ob sie HTTP 429/418 oder Netzfehler abfängt. Kein
   Aufrufer verlässt sich sichtbar darauf.
3. **Zeitzone** — ob sie UTC-naiv oder zonenbehaftet zurückgibt. Aus dem
   Ergebnis in `data/` lässt sich nur ablesen, was **nach** `to_csv`
   herauskommt.
4. **Schlüsselnutzung** — ob die enthaltenen Zugangsdaten für den Kursabruf
   überhaupt gebraucht werden (siehe Abschnitt 3 — es gibt starke Indizien,
   aber keinen Beweis).
5. **Fehlerverhalten** bei unbekanntem Symbol — werfen oder leere Tabelle?
   Alle neun Aufrufer fangen `Exception` je Symbol ab; beide Verhalten sehen
   von außen gleich aus.

Die Punkte 1–3 und 5 entscheiden sich **am Mac**, nicht hier: erst der
Vergleich des alten und des neuen Laufs zeigt sie. Der Testauftrag
(`docs/TESTAUFTRAG_TB-37_zugangsdaten.md`) führt genau diesen Vergleich.

---

## 1. Was gebaut wurde

| Datei | Was |
|---|---|
| `shared/fetch_binance_data.py` | **Neu im Repo.** Der Code; Schlüssel ausschließlich aus `os.environ`. |
| `.env.beispiel` | Die zwei Namen, **ohne Werte**. |
| `.gitignore` | Der Eintrag `shared/fetch_binance_data.py` ist **entfernt**; `.env` bleibt ausgeschlossen. |
| `shared/test_fetch_binance_data.py` | 77 Prüfungen, davon 5 Mutationsproben. |
| `research/zugangsdaten/geruest.py` | Was muss der versionierte Teil können? |
| `research/zugangsdaten/gitignoriert.py` | Woran hängt das System, das es nur einmal gibt? |

**Kein Aufrufer wurde angefasst.** `forward_test.py` ist unverändert — die
Signatur passt, weil sie aus den Aufrufern erschlossen und nicht gesetzt
wurde.

---

## 2. Die drei Entscheidungen — und warum

### 2.1 Ersetzung, nicht eine zweite Datei

**Entschieden: Ersetzung am selben Pfad, unter demselben Modulnamen.**

Die Aufgabe stellte es als Abwägung. Sie ist bei genauem Hinsehen keine: die
neun Aufrufer binden `fetch_binance_data` als **Top-Level-Modul** ein,
aufgelöst über `shared/` in `sys.path`. Ein zweites Modul daneben würde von
keinem von ihnen gefunden — es müssten **alle neun geändert werden**, darunter
die fünf `forward_test.py`, und genau das schließt die Aufgabe aus.

Der zweite Grund ist der, den die Aufgabe selbst nennt: zwei Wege zu denselben
Daten. Übergabeprotokoll Abschnitt 7 — jeder Handelsparameter steht genau
einmal, weil doppelt geführte Zahlen hier schon einmal unbemerkt
auseinandergelaufen sind. Für den einzigen Datenweg ins Projekt gilt das erst
recht.

**Der Preis der Ersetzung** ist ein Schnitt in einem Zug — und ein Risiko, das
Abschnitt 4.1 beschreibt und der Testauftrag entschärft.

### 2.2 Fehlende Schlüssel: der Abruf läuft, aber er schweigt nicht

**Entschieden: vier Regeln.**

Die Aufgabe stellt die Spannung genau: *„Der Live-Betrieb darf nie blockiert
werden. Aber ein Abruf ohne Schlüssel, der still ein leeres Ergebnis liefert,
ist schlimmer als einer, der laut scheitert."*

Für den Datenpfad **löst sich die Spannung auf**, statt abgewogen werden zu
müssen: `/api/v3/klines` ist ein **öffentlicher** Endpunkt und verlangt keinen
Schlüssel. Zwei Nachbarmodule dieses Repos bauen ihren Client seit jeher ohne
(`shared/get_top_symbols.py:15`, `shared/fetch_multi_data.py:46`). Daraus:

1. **Fehlt ein Schlüssel, läuft der Abruf trotzdem** — unangemeldet, mit
   vollem Ergebnis. Blockiert wird nie.
2. **Er tut es nicht stillschweigend.** Einmal je Prozess geht eine Meldung
   nach `stderr` — einmal, nicht je Symbol: 25 Symbole × 5 Bots wären Lärm,
   und Lärm wird überlesen.
3. **Eine leere Antwort wird geworfen (`AbrufLeer`), nie geliefert.** Das ist
   der eigentliche Punkt der Aufgabe. Ein leeres Ergebnis sieht in jedem der
   neun Aufrufer genauso aus wie „kein Signal". Weil alle neun `Exception`
   **je Symbol** abfangen, bricht der Lauf davon nicht ab — die Zeile steht
   aber im Protokoll.
4. **Wer wirklich einen Schlüssel braucht**, bekommt von
   `verlange_zugangsdaten()` sofort ein `ZugangsdatenFehlen`. Im Live-Betrieb
   ruft das derzeit niemand auf.

> ⚠️ **Warum eine Ausnahme im Abruf selbst nicht reichen würde:** alle neun
> Aufrufer fangen `except Exception` je Symbol ab und drucken „Fehler bei
> {symbol}". Ein `raise` allein ist also **nicht** laut genug, um einen
> systematischen Ausfall sichtbar zu machen — deshalb die eigene Meldung nach
> `stderr` zusätzlich.

### 2.3 `.env.beispiel` gehört ins Repo

**Entschieden: ja.**

Sie nennt die zwei Namen und beantwortet damit die Frage, die sonst nur die
verlorene Datei beantworten konnte: *wie heißen die Dinger?* Sie enthält keine
Werte, und der Selbsttest hält das nach (Abschnitt 5.2).

`*.env` in `.gitignore` trifft sie **nicht** — das Muster verlangt die Endung
`.env`, nicht den Anfang. Mit `git check-ignore` nachgeprüft, nicht angenommen.

---

## 3. Berichtet, nicht entschieden: `python-binance` gegen stdlib

**Die Frage:** Wäre der versionierte Teil besser auf
`shared/binance_historie.py` aufzusetzen, statt `python-binance`
weiterzuführen?

**Gebaut wurde mit `python-binance`** — also so, wie es war. Das ist keine
Entscheidung gegen die stdlib, sondern die Weigerung, eine Frage nebenbei zu
entscheiden, die ausdrücklich zur Berichterstattung gestellt war.

**Was für `binance_historie.py` als Unterbau spräche:**

* Es macht heute schon genau das Richtige und **nur mit der stdlib**: Blättern
  in 1000er-Schritten (`kerzen_laden`), und `als_dataframe` liefert bereits
  **exakt dieselben sechs Spalten in derselben Schreibweise**.
* Es hat eine **echte Ratenbegrenzung**, die `python-binance` nicht hat:
  Mindestpause, Auswertung von `x-mbx-used-weight-1m`, `Retry-After` bei
  HTTP 429, sofortiger Abbruch bei HTTP 418. Das ist genau Punkt 1 und 2 der
  Unbekannten oben.
* Eine Abhängigkeit weniger. `python-binance` zieht `dateparser` nach.

**Was dagegen spricht — und es ist gewichtig:**

* **Die Lookback-Grammatik.** Die neun Aufrufer übergeben `"400 day ago UTC"`
  und `"1 Jan, 2017"`. Das ist die Schreibweise von `python-binance`, die es
  über `dateparser` auflöst. `binance_historie` rechnet in Millisekunden und
  kennt sie nicht. Sie **nachzubauen** hieße, die eine Stelle nachzubauen, an
  der eine stille Abweichung teuer wird: wie weit zurück geladen wird,
  entscheidet, was in `data/` landet — und damit über den Datenstand-Hash der
  Vorregistrierung. Ändern ließe sich die Schreibweise nur, indem man
  **alle neun Aufrufer anfasst** — ausgeschlossen.
* **Zweitrolle.** `binance_historie.py` ist ein TB-31-Werkzeug zum
  *Zurückladen*, mit sehr bewussten Eigenschaften (schreibt vorhandene Zeilen
  im Original-Text zurück, verweigert bei Abweichung). Es zusätzlich zum
  **Live-Pfad** zu machen, gäbe einer sorgfältig gebauten Sache eine zweite
  Aufgabe.
* **Der Hinweis in der Aufgabe selbst**: `binance_historie.py` nutzt bewusst
  nur stdlib, weil bei `python-binance` ein `testnet=True` ein Laufzeit-Flag
  im Aufrufpfad gewesen wäre. Das betraf den **Order**-Pfad. Hier geht es um
  Marktdaten; `get_historical_klines` sendet nichts.

**Empfehlung zur Entscheidung durch den Betreiber:** *nicht jetzt.* Der Schnitt
Code/Schlüssel ist für sich schon ein Eingriff in den Live-Pfad von fünf Bots.
Den Transport im selben Zug zu tauschen, machte zwei Änderungen ununterscheidbar,
wenn danach etwas klemmt. **Wenn** getauscht wird, dann als eigener Schritt,
und die Lookback-Auflösung zuerst gegen die alte Antwort nachgemessen — Schritt 7
des Testauftrags legt dafür die Messlatte (er hält fest, wie viele Kerzen der
alte Weg liefert).

---

## 4. Vier Befunde

### 4.1 ⚠️ `git pull` überschreibt eine gitignorierte Datei **ohne Warnung**

Das ist der wichtigste Befund dieser Sitzung, weil er den Testauftrag
bestimmt.

Wenn ein Commit eine Datei an einem Pfad hinzufügt, an dem lokal eine
**gitignorierte** Datei liegt, wird diese beim `git pull` **kommentarlos
überschrieben**. Kein Prompt, keine Rückfrage, keine Meldung außer
`create mode 100644`. Nachgestellt und bestätigt:

```
--- vorher: <Datei mit den Schlüsseln>
Fast-forward
 secret.py | 1 +
 create mode 100644 secret.py
--- nachher: <Inhalt aus dem Commit>
```

**Folge:** Ein `git pull` des TB-37-Zweigs auf dem MacBook **löscht die
einzige Kopie der Zugangsdaten** — genau den Verlust, den TB-37 verhindern
soll.

Deshalb ist Schritt 0 des Testauftrags die **Sicherung**, und zwar *vor jeder
git-Operation*, und Schritt 1 prüft sie nach. Das ist keine Vorsicht, sondern
die Bedingung dafür, dass der Rest überhaupt stattfinden darf.

### 4.2 Die Namen waren nie unbekannt — und eine Wache wird dadurch scharf

`broker/zugang.py:101` führt seit jeher:

```python
DATENABRUF_VARIABLEN = ("BINANCE_API_KEY", "BINANCE_API_SECRET")
```

und beschreibt sie als *„die bestehenden Schlüssel für den Kursdatenabruf
(`shared/fetch_binance_data.py`) — sie gehören zu einem **ECHTEN**
Binance-Konto"*. Die Namen in `.env.beispiel` sind also die im Repo bereits
dokumentierten, nicht geraten. Der Selbsttest rechnet das gegen
`broker/zugang.py` nach, damit es nicht auseinanderläuft.

**Und daran hängt mehr:** `broker/zugang.py.get_zugang()` bricht ab, wenn ein
**Testnet**-Schlüssel mit einem dieser beiden übereinstimmt — eine
Verwechslungssperre gegen den schlimmsten denkbaren Fehlgriff (echter
Schlüssel an einer Handelsbrücke). Diese Sperre konnte **bisher nicht
greifen**: die echten Schlüssel standen in einer Python-Datei, nicht in der
Umgebung, und `_aus_umgebung("BINANCE_API_KEY", …)` fand nichts. Stehen sie in
der `.env`, findet die Sperre sie — und tut zum ersten Mal, wofür sie
geschrieben wurde.

TB-37 fasst `broker/` dafür **nicht** an. Die Wirkung entsteht allein dadurch,
dass die Schlüssel dort ankommen, wo der Code sie schon immer gesucht hat.

### 4.3 Der Kursabruf braucht diese Schlüssel vermutlich gar nicht

Indizien, alle im Repo nachlesbar:

* `/api/v3/klines` ist öffentlich; `shared/binance_historie.py` holt darüber
  die gesamte Historie seit 2017, **ohne Schlüssel**.
* `shared/get_top_symbols.py:15` und `shared/fetch_multi_data.py:46` bauen
  `Client()` **ohne** Zugangsdaten — letzteres in **derselben Datei**, die
  `fetch_historical_data` aufruft.
* Der `grep -c`-Befund aus TB-35 (Ergebnis **2**) sagt, dass zwei Zeilen auf
  ein Zugangsdaten-Muster passen — nicht, dass sie benutzt werden.

**Kein Beweis** (die Datei ist von hier nicht lesbar), aber stark genug für
eine Empfehlung: Schritt 6 des Testauftrags prüft **am Verhalten**, ob der
Abruf ohne Schlüssel dieselben Daten liefert. Fällt er positiv aus, kann der
Betreiber erwägen, die Schlüssel eines **echten** Kontos gar nicht erst in die
`.env` zu schreiben — der sicherste Schlüssel ist der, der nirgends liegt.

### 4.4 Die Liste dahinter: woran hängt das System noch, das es nur einmal gibt?

`python3 research/zugangsdaten/gitignoriert.py` — **13 von 22** Einträgen in
`.gitignore` werden von Betriebscode gelesen. Vier davon wären bei Verlust
nicht oder nur schwer zu ersetzen:

| Eintrag | Einschätzung | Warum |
|---|---|---|
| `*.db` | **UNERSETZLICH** | Die Handelsdatenbanken **aller neun Bots** — der gesamte Forward-Test-Verlauf seit Beginn, jede Papier-Position, jeder Ausstieg. Neu berechnen lässt sich das nicht: die Signale entstanden zu Zeitpunkten, die vorbei sind. **Nach Umfang der größte Posten dieser Liste — größer als der, der TB-37 ausgelöst hat.** |
| `config/email_config.py` | **UNERSETZLICH** | Zugangsdaten im Klartext, gelesen von **17 Betriebsmodulen**. Dieselbe Risikoklasse wie `fetch_binance_data.py` vor TB-37 — und **derselbe Schnitt wäre möglich**. Nicht Teil von TB-37. |
| `.env` | **UNERSETZLICH** | Trägt seit TB-37 die Binance-Schlüssel. Das ist Absicht — aber sie ist damit die neue einzige Kopie. Sie gehört zusätzlich in die Passwortverwaltung, nicht nur auf die Platte. |
| `notifications/warteauftraege.json` | **HEIKEL** | Wartende Ausstiegsaufträge, die ein Cronjob später **ohne Rückfrage** ausführt. Geht die Datei verloren, verschwindet der Auftrag — **ohne Meldung**, weil „keine Warteaufträge" der Normalfall ist. |

**Wurde versehentlich etwas ausgeschlossen, das ins Repo gehört?** Geprüft
wurde die **Form**: ein `.gitignore`-Eintrag, der eine **Quelltextdatei**
nennt, ist der Geruch, um den es geht — Zustandsdateien und Protokolle
entstehen neu, Quelltext nicht.

* Vor TB-37: **zwei** solche Einträge — `shared/fetch_binance_data.py` und
  `config/email_config.py`.
* Nach TB-37: **einer** — `config/email_config.py`.
* Die Erweiterungen aus TB-34 und TB-35 (`data_sicherung/`,
  `notifications/waechter_zustand.json*`, die `dashboard_snapshot`-Einträge)
  betreffen **ausschließlich Laufzeitzustand und Sicherungen**. Dort wurde
  nichts versehentlich ausgeschlossen. Alle 22 Muster wurden zusätzlich mit
  `git check-ignore` gegengeprüft.

**Empfehlung (nicht Teil von TB-37):** `config/email_config.py` nach demselben
Muster schneiden — der Weg ist jetzt gebaut und einmal am Mac erprobt. Und für
`*.db` eine Sicherung einrichten; das ist eine andere Aufgabe als diese, aber
die größere.

---

## 5. Wie geprüft wurde

### 5.1 Ohne Netz, ohne `python-binance`

Binance ist aus der Cloud gesperrt (HTTP 403) und `python-binance` dort nicht
installiert. Der Netzzugriff wird an **genau einer** Stelle ersetzt — dort, wo
python-binance sein Ergebnis abliefert. Alles davor und danach läuft echt:
Umgebung lesen, Schlüssel entscheiden, umwandeln, leeres Ergebnis erkennen,
melden. Deshalb ist der `binance`-Import **im Modul lazy**: `shared/fetch_binance_data.py`
lässt sich auch dort importieren, wo das Paket fehlt.

### 5.2 Die Prüfung, dass nirgends ein Schlüssel steht

Zwei unabhängige Prüfungen, jede mit einem eigenen Fall:

1. **Hinter dem Namen steht nie ein Wert** — über **791** vom Repo verfolgte
   und neu hinzugekommene Textdateien (`git ls-files --cached --others
   --exclude-standard`; die echte `.env` ist ignoriert und wird dadurch nie
   gelesen).
2. **Kein schlüsselförmiges Wort** in einer TB-37-Datei — mindestens 32
   Zeichen, Buchstaben und Ziffern gemischt, mit Großbuchstaben. Reines
   Kleinhex ist ausgenommen, sonst schlüge die Prüfung bei jedem erwähnten
   Datenstand-Hash an und wäre binnen einer Woche abgeschaltet.

Beide wurden **mit einem eingepflanzten Schlüssel gegengeprüft** und schlagen
dann einzeln an. Die Probe, mit der die Prüfung sich selbst belegt, **entsteht
zur Laufzeit** (SHA-256 über ein Salz) — ein hineingeschriebener Platzhalter
wäre genau das, was hier verboten ist, und würde die Prüfung auslösen, die er
belegen soll.

Ebenfalls geprüft: der Selbstbericht des Moduls
(`python3 shared/fetch_binance_data.py`) gibt bei gesetzten Schlüsseln
**keinen Wert** aus, und die Ausnahme `ZugangsdatenFehlen` verrät den
vorhandenen Schlüssel nicht.

### 5.3 Die zwei wiederkehrenden Fallen

**Falle 1 — eine selbst hergestellte Probe bestätigt sich selbst.** Deshalb
fünf **Mutationsproben**: jede Absicherung wird an einer Kopie des Moduls
einzeln ausgeschaltet, und danach muss genau die Prüfung, die sie bewacht,
**fehlschlagen**. Beobachtet wird der **Ablauf** (die Funktion wird wirklich
aufgerufen), nicht ein von Hand hergestellter Zustand.

| # | Ausgeschaltet | Fällt dann |
|---|---|---|
| M1 | `if not kerzen: raise AbrufLeer` | Leeres Ergebnis kommt still zurück |
| M2 | Der `_GEWARNT`-Kurzschluss | Die Meldung steht bei jedem Aufruf da |
| M3 | `float(k[4])` in `als_dataframe` | CSV-Zeile nicht mehr zeichengleich mit `data/` |
| M4 | `raise ZugangsdatenFehlen` | Fehlende Schlüssel werden still hingenommen |
| M5 | `ziel.get(name) or aus_datei.get(name)` | Die `.env` überstimmt die Umgebung |

**Falle 2 — eine zweite Wache verdeckt das Fehlen der ersten.** Jede Mutation
prüft zusätzlich, dass die **übrigen vier** Prüfungen **stehen bleiben**.
Fiele bei einer Mutation alles, sagte die Probe nichts über die einzelne
Absicherung. Diese Falle ist in dieser Sitzung auch **real aufgetreten**: die
Prüfung „hinter dem Namen steht kein Wert" lief zunächst über `git ls-files`
und übersah dadurch **neu hinzugekommene, noch nicht verfolgte** Dateien —
ein eingepflanzter Schlüssel in `.env.beispiel` wurde nur von der *zweiten*
Prüfung gefunden. Behoben mit `--cached --others --exclude-standard`; danach
schlagen beide an.

### 5.4 Ergebnis

`python3 shared/test_fetch_binance_data.py` → **77 von 77 Prüfungen
bestanden.**

Und im Vergleich zum Basislauf auf unverändertem `main` (`e23e38f`, eigener
git-Arbeitsbaum): **52 Tests / 41 grün** vorher, **53 Tests / 42 grün**
nachher. Der einzige Unterschied ist die neue Zeile — kein Test, der vorher
grün war, ist rot geworden. Die 11 roten sind auf beiden Seiten dieselben
(fehlende Cloud-Abhängigkeiten, Tests die ein Argument verlangen, und die
bekannten TB-37-fremden Fälle).

---

## 6. Was am Mac geschieht (und nur dort geschehen kann)

Die Datei ist aus der Cloud nicht lesbar. Sie wurde **nicht** nachgebaut und
**nicht** geraten. Was hier steht, ist aus den **Aufrufern** erschlossen; der
Schnitt selbst gehört an den Mac:

`docs/TESTAUFTRAG_TB-37_zugangsdaten.md` — 11 Schritte, **jeder Befehl eine
Zeile** (Termius vom iPhone verliert Zeilenumbrüche in Heredocs und
Python-Blöcken). Sicherung zuerst, Prüfen nur mit `grep -c`, kein `cat`, kein
`head`, kein Editor, dessen Inhalt im Terminal landet. Kein Befehl darin kann
einen Schlüssel ausgeben.

---

## 7. In einfacher Sprache

**Was wir wissen wollten.**
In diesem Projekt gab es eine einzige Datei, die auf keinem Server und in
keiner Sicherung lag — nur auf dem MacBook. Fünf von neun Handels-Programmen
brauchten sie jeden Tag. Wäre das MacBook kaputtgegangen, hätten fünf
Programme gestanden, und niemand hätte die Datei wiederherstellen können. Wir
wollten wissen: Was genau muss diese Datei können? Und wie bekommen wir sie
ins Sicherungssystem, ohne die Passwörter mit hineinzulegen, die darin
stehen?

**Was herauskam.**
Der Text der Datei (das „Programm") liegt jetzt im Sicherungssystem. Die
Passwörter darin nicht — die kommen aus einer eigenen kleinen Datei namens
`.env`, die weiterhin nur auf dem MacBook liegt. Die neun Programme merken
davon nichts: **kein einziges von ihnen musste geändert werden.** Nebenbei kam
heraus, dass das Programm die Passwörter zum Kursdaten-Holen wahrscheinlich
gar nicht braucht — die Kurse sind öffentlich abrufbar.

**Warum das so ist.**
Ein Programm und ein Passwort sind zwei verschiedene Dinge, auch wenn sie in
derselben Datei stehen. Das Programm darf jeder sehen — es soll gesichert
werden. Das Passwort darf niemand sehen — es darf nicht gesichert werden. Weil
beides in einer Datei lag, musste die ganze Datei ungesichert bleiben. Jetzt
sind sie getrennt, und jedes kann behandelt werden, wie es soll.

**Was das für dich heißt.**
Am MacBook sind ein paar Schritte nötig, und die Reihenfolge ist wichtig:
**zuerst eine Sicherheitskopie der alten Datei anlegen, erst danach das Update
holen.** Wir haben nachgemessen: das Update überschreibt die alte Datei
**ohne zu fragen und ohne es zu melden**. Wer zuerst die Kopie macht, ist auf
der sicheren Seite; wer es vergisst, verliert die Passwörter. Die Anleitung in
`docs/TESTAUFTRAG_TB-37_zugangsdaten.md` führt Schritt für Schritt durch —
jeder Befehl passt in eine Zeile, damit er auch vom iPhone aus funktioniert,
und kein Befehl zeigt jemals ein Passwort auf dem Bildschirm an.

Zwei Dinge sind uns dabei noch aufgefallen, die **nicht** zu dieser Aufgabe
gehören, aber wichtiger sein könnten als sie: Die **Handelsdatenbanken** aller
neun Programme — also die gesamte Aufzeichnung jedes Test-Geschäfts seit
Beginn — liegen ebenfalls nur auf dem MacBook und lassen sich nicht neu
berechnen. Und die Datei mit den **E-Mail-Zugangsdaten** hat genau dasselbe
Problem wie die, die wir gerade repariert haben. Für beides wäre der nächste
Schritt derselbe Weg, den wir jetzt einmal gegangen sind.
