# TB-52 — Resolver-Modus und die zwei AST-Masse

**Sitzung 18.09.2026, Cloud.** Zweig `claude/new-session-7xve52`, Basis `062bacf`.
Schichten **(1)** und **(2)** aus Backlog **T46.3**. ⚠️ **Die 90 Module sind
NICHT verdrahtet** — das ist TB-53.

---

## Die Kurzfassung

| | |
|---|---|
| **Pfadvergleich alt/neu, ohne Modus** | ⭐ **99 Pfade, 0 Unterschiede** |
| **Wie wird der Modus gesetzt** | zwei **Umgebungsvariablen**, die den **Snapshot-Hash** tragen |
| **Kindprozess** | erbt ihn, auch zwei Ebenen tief — gemessen an echten Unterprozessen |
| **Wirft bei fehlendem Snapshot / falschem Hash** | **ja**, beides, schon beim Import |
| **T46.8** | behoben — der Import legt **kein** Verzeichnis mehr an |
| **Mass 1 (Wanduhr)** | Ausgangszahl **6**, alle in Protokollzeilen, ⭐ **null im Datenschnitt** |
| **Mass 2 (eigener Datenpfad)** | Ausgangszahl **29** |
| **Datenstand vorher = nachher** | `d9449faf…`, **223** Dateien ✅ |
| **Neue Proben** | **24** in `shared/test_paths.py`, jede mit Mutationsgegenprobe |

> ⚠️⚠️ **Der grösste Befund steht nicht in dieser Tabelle:**
> **Keines der 90 Selektionsmodule importiert `shared/paths.py`.** Der gebaute
> Modus erreicht heute **kein einziges** davon. Siehe unten.

---

## Teil 1 — Der Resolver-Modus

### Wie er gesetzt wird, und warum so

**Zwei Umgebungsvariablen:**

```
TB_SELEKTIONSWURZEL   absoluter Pfad zur Snapshot-Wurzel
TB_SELEKTIONSHASH     der erwartete snapshot_hash aus deren MANIFEST.json
```

**Warum nicht prozesslokal.** Der Selektionslauf startet **einen Prozess je
Bot** (TB-40). Ein prozesslokaler Modus wird nicht vererbt — **gemessen**, nicht
vermutet:

> **Messung 4** (`research/resolver_selektion/kindprozess.py`): Elternprozess im
> Modus, Kind ohne. Das Kind liest `/home/user/trading-bot/data` — **ohne
> Fehler, ohne Meldung.** ⚠️ Genau die Ausfallform, gegen die diese Schicht
> gebaut wird, nur eine Ebene tiefer.

**Der Vorschlag aus dem Auftrag ist übernommen:** der Modus trägt **den
Snapshot-Hash**, nicht nur „an/aus". Ein Kind, das einen **anderen** Hash erbt,
**wirft** (Messung 5, `rc=1`) statt still danebenzugreifen.

### Was im Kindprozess passiert — sieben Messungen

| # | Frage | Gemessen |
|---|---|---|
| 1 | Kind **ohne** Modus | Live-Bestand ✅ |
| 2 | Kind **mit** Modus | Snapshot ✅ — die Variable wird vererbt |
| 3 | **Enkel** mit Modus | Snapshot ✅ — auch zwei Ebenen tief |
| 4 | **prozesslokaler** Modus | ⚠️ Kind liest **still** den Live-Bestand |
| 5 | Kind erbt **anderen** Hash | `rc=1`, `Selektionsfehler` ✅ |
| 6 | **übriggebliebener** Modus | eine Zeile auf `stderr` ✅ |
| 7 | **Cron-Nachbildung** (magere Umgebung) | Live-Bestand ✅ |

### ⚠️ Was passiert, wenn der Modus übrigbleibt — und welches Loch bleibt

**Drei Dinge halten dagegen, keines davon eine Umgehungsflagge:**

1. **Der Hash benennt den Zustand.** Ein übriggebliebener Modus zeigt nicht
   irgendwohin, sondern auf einen **benannten** Snapshot; passt der Hash nicht,
   bricht der Lauf ab.
2. **Zeigt der Modus ins Leere, wirft er sofort beim Import.**
3. ⭐ **Ein Lauf unter dem Modus SAGT es** — eine Zeile auf `stderr`, bei jedem
   Import (**D1**: *„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."*).

**Und der Cron-Pfad ist strukturell geschützt:** Cron erbt die interaktive Shell
nicht. Messung 7 bildet das mit einer mageren Umgebung nach — der Modus kommt
dort nicht an.

> ⚠️ **Das benannte Restloch:** Stünde der Modus in der **Crontab-Zeile selbst**
> oder in einem von dort gesourcten Profil, dann rechnete dieser Lauf gegen den
> Snapshot. Er **sagt** es dann (Punkt 3), aber niemand hindert ihn.
> ⭐ *Ein benanntes Loch ist ein Backlog-Punkt; ein unbenanntes ist eine Falle.*
> **Der Nachweis gehört auf den Betriebsrechner** und steht als Schritt 3 im
> Mac-Testauftrag: `crontab -l | grep -c "TB_SELEKTION"` — erwartet **0**.

### Der Nachweis: 99 Pfade, 0 Unterschiede

| | |
|---|---|
| **Bezugscommit** | `062bacf…`, **festgenagelt** (**B3**) |
| **Verglichen** | **99** = 9 Bots × 11 Pfadarten |
| **Unterschiede** | ⭐ **0** |
| **Zugänge in der neuen Fassung** | 5 neue Namen — keine Unterschiede |

Alte Fassung aus `git show 062bacf:shared/paths.py`, beide in **je einem eigenen
Prozess** und **je einem eigenen Wegwerfbaum** gleicher Form, je Bot **aus der
Sicht dieses Bots**. Nicht „sieht gleich aus", nicht am Quelltext, nicht
stichprobenartig.

⭐ **Und der Vergleich prüft sich selbst** (**A5**): gegen eine absichtlich
verstellte alte Fassung findet er **9** Unterschiede. Fände er dort keinen, wäre
der Ausgang **NICHT PRÜFBAR**, nicht grün.

### T46.8 — der Import legt kein Verzeichnis mehr an

Die zwei `os.makedirs(..., exist_ok=True)` sind entfernt. **Gemessen an einem
Wegwerf-Ordner, der vorher nicht existiert und danach immer noch nicht
existiert** (Probe F). ⚠️ Der Baum wird dafür **ohne** `data/` gebaut — existierte
es schon, sagte die Probe nichts (**A1**).

---

## Teil 2 — Die zwei Masse

**Bauform Sperrklinke** (**A4**): grün, solange der Stand **nicht grösser** wird
als die Ausgangszahl. Nachgemessen, nicht behauptet:

| Ausgangszahl gegen Stand 29 | rc | |
|---|---|---|
| 29 | **0** | grün |
| 28 | **1** | ⚠️ rot — *sie beisst* |
| 30 | **0** | grün, mit Hinweis zu senken |
| Erhebung fehlt | **2** | NICHT PRÜFBAR |

### Mass 1 — Wanduhren: Ausgangszahl 6

**Alle sechs `datetime.utcnow()`, alle in drei `quarterly_review.py`:**

| Datei | Zeile | Verwendung |
|---|---|---|
| `strategies/elliott_wave/quarterly_review.py` | 119 / 205 | Berichtskopf / `print` |
| `strategies/elliott_wave_stocks/quarterly_review.py` | 124 / 210 | Berichtskopf / `print` |
| `strategies/t3_supertrend/quarterly_review.py` | 146 / 232 | Berichtskopf / `print` |

> ⭐ **Im Datenschnitt: 0. Nur in Protokoll-/Berichtszeilen: 6.**

⚠️ Der Test stuft drei davon als `zu prüfen` ein, nicht als „harmlos" — er sieht
`lines.append(…)` und weiss nicht, wohin `lines` geht. **Von Hand nachgesehen:**
`build_report` fügt `lines` mit `"\n".join(lines)` zu einem Textbericht. *Der
Test unterscheidet das nicht — der Bericht tut es.*

**Über die Auftragsliste hinaus gesucht** (und gemeldet, wie verlangt):
`datetime.today` · `Timestamp.utcnow` · `date.fromtimestamp` ·
`datetime.fromtimestamp` · **`os.path.getmtime`/`getctime`** · `time.time_ns` ·
`time.monotonic`, dazu `np.datetime64("now")`/`pd.Timestamp("today")` und die
**blosse Referenz** ohne Aufruf.

### Mass 2 — eigener Datenpfad: Ausgangszahl 29

**29 Fundstellen in 29 Modulen**, alle von einer Art: `DATA_DIR = _P["DATA_DIR"]`
aus `shared/strategy_paths.py`. ⭐ **Null Modul setzt einen Datenpfad im eigenen
Quelltext zusammen.**

---

## ⚠️⚠️ Der Befund, der grösser ist als die Aufgabe

> **Keines der 90 Selektionsmodule importiert `shared/paths.py`. Nicht eines.**

**71 von 90** beziehen ihre Pfade aus `shared/strategy_paths.py` — und das leitet
`DATA_DIR` **selbst** ab, ohne `paths.py` je zu berühren:

```python
"DATA_DIR": os.path.join(base_dir, "data")     # strategy_paths.py:49
```

| Wie die 90 an Pfade kommen | |
|---|---|
| `strategy_paths`, ohne Datenpfad | 42 |
| `strategy_paths`, **mit** Datenpfad ⇒ die 29 Treffer | 29 |
| weder noch | 18 |
| nennt `DATA_DIR` ohne beide Quellen | 1 |
| ⭐ **über `shared/paths.py`** | **0** |

⚠️ **Der Modus wäre gesetzt, und alle 90 läsen weiter aus dem Live-Bestand —
still.** Das ist Fables Einwand eine Ebene höher: *die Wache steht nicht dort, wo
gefragt wird.*

> ⭐ **Das entwertet Schicht (1) nicht.** Der Modus ist die Stelle, an der ein
> Pfad zentral umgebogen werden **kann**; dass heute niemand dort fragt, ist
> genau der Umbau, den Mass 2 misst — **und misst, bevor er stattfindet.**
>
> ⚠️ **Für TB-53 ist das die erste zu treffende Entscheidung:** die 90 auf
> `paths.py` umziehen, **oder** `strategy_paths.py` an den Resolver hängen.
> **Hier wurde nichts davon getan** — `strategy_paths.py` ist unberührt.

---

## Wo unsere Zahlen von den Erhebungen abweichen

**Übereinstimmend nachgerechnet:**

| Erhebung | Soll | Gemessen |
|---|---|---|
| `eingaben.json` Hülle | 142 | **142** ✅ |
| `eingaben.json` Selektionsmodule | 90 | **90** ✅ |
| `erhebung.json` erreichen `data/` | 182 | **182** ✅ |
| `erhebung.json` bauen selbst | 29 | **29** ✅ |
| Datenstand | `d9449faf…` / 223 | **trifft** ✅ |

### ⚠️ Abweichung 1 — die 29 des Auftrags sind nicht die 29 dieses Masses

Der Auftrag sagt zu Mass 2: *„die Erhebung nennt **29** Module, die den Pfad
selbst bauen. **Das ist die Ausgangszahl**."*

**Nachgerechnet trifft das nicht zu.** Von jenen 29 ist **kein einziges** ein
Selektionsmodul:

| | Erhebung `datenordner_schnitt` | dieses Mass |
|---|---|---|
| **Frage** | wer baut einen Pfad **selbst**? | welche **Selektionsmodule** beziehen einen Datenpfad **ausserhalb `paths.py`**? |
| **Anzahl** | 29 | 29 |
| **Wer** | 16 Untersuchung · 7 Prüfwerkzeug · 6 Betrieb | **90/90 Selektion** |
| **Schnittmenge mit den 90** | ⭐ **0** | — |

⚠️ **Die Mengen sind disjunkt; dass beide Male 29 herauskommt, ist Zufall.**
Hätte die Zahl ungeprüft gepasst, wäre der Befund darüber verlorengegangen
(**C7**, **C1**).

### ⚠️ Abweichung 2 — „145 Module importieren `paths.py`"

Dieser Satz steht in **`CLAUDE.md`**, **`ARBEITSWEISE.md` §7**, **Backlog T46.3**
und im Auftragstext. **Er verwechselt drei Fragen:**

| Zahl | Frage |
|---|---|
| ⭐ **10** | Module, die `paths` **direkt importieren** — es sind die **Abruf- und Symbolskripte** (`fetch_*`, `get_top_symbols`, `symbols_config`), also die **schreibende** Seite |
| ⭐ **163** | Module, die **transitiv** daran hängen, weit überwiegend über `shared/symbols_config.py` |
| **145** | `beziehen_zentral` aus der Erhebung — Module, die ihre Pfade aus **einer der beiden** zentralen Quellen beziehen, also weit überwiegend aus `strategy_paths.py` |

> ⭐ **Die Vorsicht bleibt berechtigt** — 163 transitiv Betroffene und der Cron
> sind Grund genug. **Die Begründung gehört berichtigt.**
>
> ⚠️ Und die Zahl passt zum grossen Befund: `paths.py` ist das Modul der
> **Abrufseite**. Dass die Selektionsseite es nie anfasst, ist kein Zufall,
> sondern die Bauform des Projekts.

**Registertexte wurden nicht angefasst.** Die Berichtigung steht im Kopf von
`shared/paths.py` und hier.

---

## Beisst jede neue Probe? (Prüfprinzip B1)

**24 Proben in `shared/test_paths.py`, jede mit Gegenprobe.** Die Mutationen und
ihr Ausgang ohne die Bedingung:

| Probe | Mutation | Ausgang **ohne** die Bedingung |
|---|---|---|
| **A** ohne Modus wie vorher | `"data"` → `"daten_verstellt"` | **9** Unterschiede statt 0 |
| **B** Modus zeigt in den Snapshot | `DATA_DIR = _MODUS[0]` → `_LIVE_DATA_DIR` | `DATA_DIR` bleibt live |
| **C** Live-Anfrage wirft | `LIVE_DATA_DIR` auch unter dem Modus als Global | liefert **still** den Live-Pfad |
| **D** fehlender Snapshot wirft | `raise` → `return None` (stiller Rückfall) | Modus schaltet sich stumm ab |
| **E** Kindprozess erbt | `_MODUS = None` (prozesslokal gedacht) | Kind liest **still** live |
| **F** T46.8 | die zwei `makedirs`-Zeilen zurück | `data/` entsteht beim Import |

**Dazu die Selbstproben der beiden Masse:** Mass 1 findet **7 von 7** eingebauten
Wanduhren und **0** im sauberen Modul; Mass 2 findet **5 von 5** in allen fünf
Bauarten und **0** im sauberen Modul. **Beissen sie nicht, ist der Ausgang NICHT
PRÜFBAR** (rc 2), nicht grün.

---

## ⚠️ Zwei Proben, die im ersten Entwurf falsch gebaut waren

**Benannt statt still berichtigt** — beide Male dieselbe Falle:

1. **`kindprozess.py`, Messung 5** stand auf „trifft nicht zu", obwohl der
   Resolver richtig warf. Der Probeprozess **fing die Ausnahme selbst ab**, um
   sie melden zu können, und lieferte damit **immer `rc=0`** — geprüft wurde aber
   der Rückgabewert. Behoben mit einem zweiten Prozess **ohne** `try`.
2. **`test_paths.py`, Probe E1** meldete „der Enkel erbt den Modus nicht". In
   Wahrheit brach der Enkel mit `TypeError` ab: eine Vorlage formatierte Kind-
   und Enkelquelltext in **einem** Durchgang und ersetzte zweimal. **Leere
   Ausgabe wurde als Messergebnis gelesen.**

> ⭐ **Prüfprinzip A1, zweimal an einem Tag:** *ein gescheiterter Aufruf und ein
> leeres Ergebnis sehen gleich aus.* **Gefunden nur, weil zwei Werkzeuge
> dieselbe Frage beantworteten** (**C2**) und einander widersprachen. Probe E1
> sagt jetzt **NICHT PRÜFBAR**, wenn der Enkel nichts liefert.

**Und ein dritter Fall, im Mass selbst:** Mass 2 meldete zuerst **127** statt 29
Treffer — `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` galten nicht als zentral bezogen,
und innere Knoten wurden doppelt gezählt. ⚠️ **Hätte niemand hingesehen, wäre 127
die festgeschriebene Ausgangszahl für TB-53 geworden.**

---

## Basislauf

`research/datenordner_schnitt/basislauf.py --grenze 300`, **69 Testdateien:**

| Stufe | |
|---|---|
| **grün** | **53** |
| **rot** | 11 |
| **flackernd** | 1 — `system/test_log_rotation.py`, heute grün |
| **ungeprüft** | 3 — verlangen ein Bot-Argument (**A3**) |
| **Zeitgrenze** | 1 — `shared/test_drawdown_beide_masse.py` (bekannt) |
| **UNERWARTET** | 8 |

**Die drei neuen Dateien sind grün:** `shared/test_paths.py` (24/24),
`research/selektionsmasse/test_wanduhr.py`, `…/test_eigener_pfadbau.py`.

### ⚠️ Die 8 unerwarteten — alle gegen die Basis gegengeprüft

**Keiner stammt von diesem Zweig.** Jeder wurde zusätzlich in einem
`git worktree` auf **`062bacf`** ausgeführt:

| Test | Zweig | Basis | Ursache |
|---|---|---|---|
| `broker/test_ibkr.py` | rc=1 | **rc=1** | `tzdata` fehlt (`US/Eastern`) |
| `dashboard/test_dashboard.py` | rc=1 | **rc=1** | `fastapi` fehlt |
| `research/universum_trockenlauf/…` | rc=1 | **rc=1** | `binance` fehlt |
| `shared/test_groessenfaktor.py` | rc=1 | **rc=1** | Bot-Lauf ohne `binance`/`yfinance` |
| `shared/test_kursdaten.py` | rc=1 | **rc=1** | `yfinance` fehlt |
| `shared/test_ladeprotokoll.py` | rc=1 | **rc=1** | `binance`/`yfinance` fehlen |
| `shared/test_leeres_symbol.py` | rc=1 | **rc=1** | `binance`/`yfinance` fehlen |
| `research/exposure_messung/test_exposure_kern.py` | **grün** | grün | steht in `BEKANNT_ROT` für den **Mac** — hier grün, kein Widerspruch |

---

## ⚠️ Abweichungen von `docs/UMGEBUNGEN.md` — gemeldet, wie verlangt

*„Die Cloud ist nicht EINE Umgebung, sondern eine je Sitzung."* Diese Sitzung:

| | `UMGEBUNGEN.md` | **diese Sitzung** |
|---|---|---|
| **Python** | 3.11 oder neuer (zuletzt 3.11.15) | **3.11.15** ✅ |
| **pandas / numpy** | „wechselnd", Mac 2.3.3 / 2.0.2 | ⚠️ **fehlten ganz**, nachinstalliert: **3.0.6 / 2.4.6** |
| **`binance`, `yfinance`** | nicht aufgeführt | ⚠️ **fehlen** — Ursache von 5 der 8 unerwarteten Roten |
| **`fastapi`** | nicht aufgeführt | ⚠️ **fehlt** |
| **`tzdata`** | nicht aufgeführt | ⚠️ **fehlt** (`US/Eastern` nicht auflösbar) |
| **`node`** | „wechselnd" | nicht geprüft |

⭐ **Vorschlag für die Pflege der Datei:** `binance`, `yfinance`, `fastapi` und
`tzdata` als eigene Zeilen aufnehmen. **Fünf der acht unerwarteten Roten dieses
Laufs sind nichts weiter als ihr Fehlen** — ohne die Gegenprobe gegen die Basis
hätte das nach einem kaputten Zweig ausgesehen.
*(Eine Sitzung trägt das nicht selbst ein — sie meldet den Messwert.)*

---

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ✅ | **Kein Snapshot gezogen** (F1a). Wo einer gebraucht wurde, stand eine **Attrappe** im Wegwerfordner — zwei erfundene Dateien, nie `data/` |
| ✅ | **Die 90 Module nicht verdrahtet** |
| ✅ | `data/` nur gelesen — `d9449faf…` / 223 **vorher und nachher** |
| ✅ | **Sperrlisten-Dateien unberührt** — `entscheidungskerze.py`, `live_params.py`, `forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py` |
| ✅ | **Kein bestehender Aufruf von `paths.py` geändert** — keine Signatur, kein Rückgabetyp, kein Name |
| ✅ | **`strategy_paths.py` unberührt** — obwohl der Befund dorthin zeigt |
| ✅ | **Kein Registertext angefasst** |
| ✅ | Kein Netzabruf, kein Broker-Endpunkt, keine Order |
| ✅ | **Keine Umgehungsflagge** für den Resolver |

---

## Der Diff

```
 docs/ERGEBNIS_TB-52_resolver.md                      | neu
 docs/TESTAUFTRAG_TB-52_resolver.md                   | neu
 research/datenordner_schnitt/ergebnisse/basislauf_tb52.json | neu
 research/resolver_selektion/BERICHT.md               | neu
 research/resolver_selektion/ergebnisse/*.json        | neu
 research/resolver_selektion/kindprozess.py           | neu
 research/resolver_selektion/pfadvergleich.py         | neu
 research/selektionsmasse/BERICHT.md                  | neu
 research/selektionsmasse/ergebnisse/*.json           | neu
 research/selektionsmasse/masse.py                    | neu
 research/selektionsmasse/test_eigener_pfadbau.py     | neu
 research/selektionsmasse/test_wanduhr.py             | neu
 shared/test_paths.py                                 | neu
 shared/paths.py                                      | 227 +, 4 -
```

⭐ **Genau eine bestehende Datei geändert.** Die **vier entfernten Zeilen**, jede
zugeordnet:

| entfernte Zeile | wohin |
|---|---|
| `DATA_DIR = os.path.join(BASE_DIR, "data")` | → `_LIVE_DATA_DIR`; `DATA_DIR` wird im Zweig **ohne Modus** mit **demselben Wert** gesetzt |
| `CONFIG_DIR = os.path.join(BASE_DIR, "config")` | → `_LIVE_CONFIG_DIR`, ebenso |
| `os.makedirs(DATA_DIR, exist_ok=True)` | ⭐ **entfernt — T46.8** |
| `os.makedirs(CONFIG_DIR, exist_ok=True)` | ⭐ **entfernt — T46.8** |

> ⚠️ **Dass die ersten beiden Umbenennungen nichts verschieben, ist genau das,
> was der 99-Pfade-Vergleich misst.**

---

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **`strategy_paths.py` hängt nicht am Resolver** — der Kern des grossen
   Befunds. **Nicht angefasst**: die Freigabe gilt für `paths.py`, und das
   Verdrahten ist TB-53.
2. ⚠️ **`strategy_paths.get_strategy_paths()` legt bei jedem Aufruf `results/`
   und `logs/` an** (`os.makedirs`) — **dasselbe T46.8-Muster**, eine Datei
   weiter, und dort **nicht** behoben. ⭐ *Ein Import ist keine Leseoperation*
   (**B6**) gilt dort genauso.
3. ⚠️ **`CONFIG_DIR` zeigt unter dem Modus in den Snapshot.** Für die
   Symbollisten ist das richtig; `config/` enthält aber auch `email_config.py`.
   **Heute kein Loch** — ein Selektionslauf verschickt keine E-Mail. ⭐ Genau die
   Bauform aus **D4**: *stabil aus Zufall der Umstände, nicht aus Entwurf.*
4. **Der Modus deckt `DATA_DIR`/`CONFIG_DIR` ab, nicht einzelne Dateinamen.**
   Ein Modul, das eine Kursdatei **ausserhalb** von `data/` liest, sähe ihn nie
   — heute tut das keines der 90 (Mass 2, Klasse „eigener Pfadbau": **0**).
5. **Die drei `quarterly_review.py` schreiben ihren Berichtskopf mit der
   Wanduhr.** Harmlos, aber: **zwei Läufe über denselben Snapshot ergeben zwei
   verschiedene Berichtsdateien.** Für einen byteweisen Reproduktionsvergleich
   auf Berichtsebene müsste das bekannt sein.
6. ⚠️ **`basislauf.py` nennt im Kopf „62 Testdateien", misst aber 69.** Eine
   Zahl im Fliesstext, die mitaltert.
7. ⚠️ **`main` im Repo ist `6bec79c`, nicht `062bacf`** — siehe unten.

---

## ⚠️ Zur Basis dieser Sitzung

Der Auftrag nennt *„Base `main` (**`062bacf`**), frisch von `main` aufsetzen"*.
**Im Repo trifft das nicht zu:**

| | |
|---|---|
| `origin/main` | **`6bec79c`** (Merge PR #108, 15.09.2026) |
| `062bacf` | liegt **66 Commits davor** auf `claude/new-session-7xve52` |
| `062bacf` Vorfahr von `main`? | **nein** |

**Gearbeitet wurde auf `062bacf`**, dem ausdrücklich benannten Commit — er trägt
alle Dateien, auf die der Auftrag sich stützt (`PRUEFPRINZIPIEN.md`,
`ARBEITSWEISE.md`, beide Erhebungen). ⚠️ Von `main` aufzusetzen hätte sie
**nicht** vorgefunden. **Wäre dieser Zweig gegen `main` gemergt, sähen die 66
Commits wie Löschungen aus** — der Merge-Basis-Vergleich aus `ARBEITSWEISE.md` §7
ist hier also nicht optional.

---

## In einfacher Sprache

**Worum es ging.** Wenn wir eine Strategie auswählen, sollen die Bots aus einem
**eingefrorenen** Datenstand rechnen, nicht aus den laufend nachgeladenen
Kursdaten. Sonst weiss man hinterher nicht, ob ein gutes Ergebnis an der
Strategie lag oder daran, dass die Daten sich zwischendurch geändert haben.

**Was gebaut wurde.** Eine zentrale Stelle, die Pfade herausgibt, hat einen
**Schalter** bekommen. Ist er aus — und das ist er immer, auch nachts beim
automatischen Lauf — passiert **exakt** dasselbe wie vorher. Ist er an, bekommt
jeder, der nach den Kursdaten fragt, den eingefrorenen Stand. Und wer
ausdrücklich nach den *lebenden* Daten fragt, bekommt eine **Fehlermeldung**, in
der steht, wer gefragt hat und was er hätte fragen sollen.

**Warum das so heikel war.** Diese Stelle wird überall benutzt und läuft
automatisch. Geht sie kaputt, stehen neun Bots still — und ihre Datenbanken sind
die einzigen echten Messwerte, die das Projekt hat. Deshalb wurde **nachgemessen
statt versprochen**: 99 Pfade, einmal mit der alten und einmal mit der neuen
Fassung, **kein einziger Unterschied**. Und damit dieser Vergleich nicht bloss
schweigt, wurde er absichtlich an einer kaputten Fassung erprobt — dort findet er
sofort neun Abweichungen.

**Und der unangenehme Fund.** Der Schalter sitzt in einer Datei, die von den 90
Auswahl-Programmen **kein einziges benutzt**. Sie holen ihre Pfade aus einer
**anderen** Datei, die den Datenordner selbst zusammensetzt. Der Schalter würde
also umgelegt — und alle 90 läsen munter weiter aus den lebenden Daten, ohne dass
jemand etwas merkt.

> **Das ist kein Fehlschlag, sondern der eigentliche Ertrag dieser Aufgabe.** Der
> Schalter ist die Stelle, an der man das später **umbiegen kann**. Und es gibt
> jetzt ein Messgerät, das genau zählt, wie viele der 90 noch am Schalter
> vorbeigreifen: **29**. Wird eines mehr daraus, schlägt es sofort an. Wird der
> Umbau gemacht, muss die Zahl sinken — und wer sie heimlich hochsetzt, tut das
> in einer Zeile, die jeder im Vergleich sieht.

**Was nicht passiert ist:** Es wurde kein Datenstand eingefroren, keine der
Kursdateien angefasst, keine Bot-Datei geändert und keine Order verschickt. Die
Kursdaten sind vorher und nachher **byteweise dieselben**.

**Was der Mac noch prüfen muss.** Hier lief alles auf Python 3.11; der
Betriebsrechner hat 3.9.6. Und nur dort lässt sich nachsehen, ob der
Nachtbetrieb den Schalter wirklich nicht kennt — und ob die neun Datenbanken
unberührt geblieben sind. Das steht in `docs/TESTAUFTRAG_TB-52_resolver.md`.
