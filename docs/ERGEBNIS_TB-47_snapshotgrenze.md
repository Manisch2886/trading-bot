# TB-47 — Die Snapshot-Grenze: alle Eingaben, zwei Hashes

**Ergebnis der Cloud-Sitzung vom 18.09.2026.**
Vorgänger: TB-46b (gemergt `c5ad722`). Zweig: `claude/new-session-ebo6mm`.

---

## ⚠️ Das Wichtigste zuerst

**Der Snapshot lässt sich heute nicht ziehen — und das ist kein Fehler dieser
Arbeit, sondern ihr wichtigster Befund.**

Registertext 5a verlangt, dass vor dem Ziehen die Teilkerzen-Prüfung über die
Quelle läuft und dass **nicht gezogen wird, wenn sie etwas findet**. Genau das
ist jetzt eingebaut. Zum ersten Mal gemessen:

> **`data/` ist NICHT frei von Teilkerzen. 36 der 223 Dateien haben einen
> Befund.**

Ein Trockenlauf gegen den echten Bestand bricht deshalb mit Rückgabewert 2 ab:

```
ABBRUCH: Die Teilkerzen-Pruefung hat 36 Datei(en) mit Befund gefunden:
AAVEUSDT_1d.csv, AAVEUSDT_4h.csv, ADAUSDT_1d.csv, … und 28 weitere.
Es wird NICHT gezogen.
```

**Alle 36 Befunde sind von derselben Art** (`rand_erste`) und betreffen
**ausschliesslich die ERSTE Kerze** einer Krypto-Datei. Es ist der seit TB-31
bekannte Sachverhalt: die Krypto-Tages- und 4h-Dateien wurden aus den
1h-Daten abgeleitet, und ihre erste Kerze deckt 2 bis 20 statt 24 Stunden ab.

⭐ **Die letzte Kerze ist bei allen 223 Dateien sauber.** Das ist der Rand, der
für einen Snapshot gefährlich wäre — eine Kerze, in die ein Abruf mitten
hineingeschrieben hat. Diesen Fall gibt es hier nicht.

**Was daraus folgt, ist eine Entscheidung des Betreibers, nicht dieser
Sitzung.** Drei Wege stehen offen, und keiner davon wurde hier gegangen:

1. die 36 ersten Kerzen reparieren (sie abschneiden oder aus 1h neu
   aufbauen) — danach zieht das Werkzeug ohne Weiteres;
2. eine ausdrückliche, dokumentierte Ausnahme für `rand_erste` beschliessen —
   das wäre eine Änderung an Registertext 5a und braucht einen eigenen
   Eintrag, denn 5a sieht die Prüfung ohne Einschränkung vor;
3. den Snapshot auf einem bereinigten Bestand ziehen.

⚠️ **Eine stille Abschwächung der Prüfung wäre hier das Schlechteste.** Sie
stünde im Manifest als „geprüft" neben einem Hash, den sie nicht deckt — genau
die Bauform, gegen die dieses Modul geschrieben ist. Deshalb gibt es auch
**keine** Übergehen-Flagge.

---

## Die gestellten Fragen, direkt beantwortet

| Frage | Antwort |
|---|---|
| **Welche Nicht-Code-Dateien gehören in den Snapshot?** | Neben den Kursdateien **genau zwei**: `config/top25_symbols.txt` und `config/sp500_top150.txt`. Beide versioniert. Tabelle unten. |
| **Kommt der Handelskalender aus einer Datei oder aus einem Paket?** | ⭐ **Aus einem Paket.** `pandas_market_calendars`, `mcal.get_calendar()`. Keine Datei. Er ist **Umgebung**, gehört ins Lock — und er liegt **nicht** in der Hülle der 90. |
| **Ergibt `datenstand_hash` weiterhin `d9449faf…`?** | **Ja**, gezeigt: `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` bei 223 Dateien, vor und nach der Arbeit. |
| **Ist der Bestand frei von Teilkerzen?** | ⚠️ **Nein** — 36 von 223, alle `rand_erste`. An der Quelle geprüft, nicht an einer Kopie. Siehe oben. |
| **Beendet der Runner jetzt die ganze Prozessgruppe?** | **Ja**, mit Nachweis **und** Gegenprobe (11 Prüfungen, alle grün). |

---

## Teil 1 — Erhebung: was gehört in den Snapshot?

**Werkzeug:** `research/snapshotgrenze/erhebung_eingaben.py` (misst, ändert
nichts). **Rohdaten:** `research/snapshotgrenze/ergebnisse/eingaben.json`.

**Ausgangsmenge:** die **90 Selektionsmodule** aus TB-46
(`research/datenordner_schnitt/ergebnisse/erhebung.json`, Rolle
`Selektion/Backtest`). ⚠️ Die **Rollenzuordnung wurde übernommen**, die
**Dateiliste neu erhoben** — TB-46 hat nach `data/` gefragt, nicht nach
Nicht-Code-Eingaben.

⚠️ Erhoben wurde über die **transitive Hülle**: die 90 plus alles, was sie
importieren — **142 Module**. Ohne diesen Schritt wäre die wichtigste Datei
durchgerutscht: `config/top25_symbols.txt` wird nicht von einem der 90
gelesen, sondern von `shared/symbols_config.py`, das sie importieren.

### Die Tabelle

| Datei | Leser | Herkunft | versioniert | Einstufung |
|---|---|---|---|---|
| `config/top25_symbols.txt` | `shared/symbols_config.py:28` | Repo, `config/` | **ja** | **Eingabe** |
| `config/sp500_top150.txt` | vier `stocks_symbols_config.py` (Aktien-Bots) | Repo, `config/` | **ja** | **Eingabe** |
| `data/*.csv` (223) | die neun Bots, der Selektionslauf | Repo, `data/` | ja | **Eingabe** (schon bisher im Snapshot) |
| NYSE-Handelskalender | `notifications/boersenkalender.py:81` | ⭐ **`pandas_market_calendars`** | — | **Umgebung** |
| `BTCUSDT_zigzag.csv` | `strategies/elliott_wave/elliott_wave_counter.py:367` | `results/` | nein | **erzeugt** (Zwischenstand) |
| `AAPL_zigzag.csv` | `…_stocks/elliott_wave_counter.py:367` | nicht auffindbar | — | **unklar** — derselbe Fall wie oben, nur liegt die Datei im Checkout nicht vor |
| `_vb_trades_cache.csv` | zwei `experiment_volatility_breakout_overlap.py` | nicht auffindbar | — | **unklar** — Name und Ort sprechen für einen zur Laufzeit gebauten Zwischenspeicher |

**Summe:** 5 × Eingabe · 0 × Umgebung (unter den *Dateien*) · 1 × erzeugt ·
2 × unklar.

⚠️ **„unklar" ist hier ein Ergebnis, kein Versäumnis.** Beide unklaren Fälle
werden unter `if __name__ == "__main__"` bzw. aus einem Ergebnisordner
gelesen; alles spricht dafür, dass es Zwischenstände sind. **Bewiesen ist das
nicht**, und deshalb steht es so da.

### ⭐ Der Handelskalender im Besonderen

**Er kommt aus einem Paket, nicht aus einer Datei.** Die einzige Fundstelle im
ganzen Repo ist `notifications/boersenkalender.py:81`:

```python
import pandas_market_calendars as mcal
...
_KALENDER = mcal.get_calendar(KALENDER_NAME)
```

Daraus folgt zweierlei:

1. **Er gehört ins Lock, nicht in den Snapshot.** Eine Datei aus einem
   Fremdpaket ist Umgebung.
2. ⚠️ **Das Ergebnis des Laufs hängt damit an einer Paketfassung, nicht an
   einer Eingabe — und ein Snapshot kann das nicht einfangen.** Ändert
   `pandas_market_calendars` seine Feiertagstabelle, ändert sich das
   Ergebnis, ohne dass `snapshot_hash` oder `datenstand_hash` sich rühren.
   **Das ist eine Eigenschaft des Aufbaus, keine Lücke dieses Moduls** — aber
   es gehört benannt, und in der Cloud war die Fassung **5.4.0**.

⭐ **Und ein Befund dazu:** der Kalender liegt **nicht in der Hülle der 90**.
Der Selektionslauf erreicht ihn überhaupt nicht; er hängt am Live-Pfad
(`shared/entscheidungskerze.py` → `notifications/boersenkalender.py`), und der
ist Betrieb, nicht Selektion. Für den Selektionssnapshot stellt sich die Frage
also gar nicht — für die Vergleichbarkeit der **Forward-Test-Zahlen** dagegen
schon.

### Wo Registertext 5a unscharf ist (berichtet, nicht geändert)

1. **„Eingaben des Laufs" trennt nicht zwischen Eingabe und Zwischenstand.**
   Eine Datei, die der Lauf erst schreibt und dann liest, ist wörtlich eine
   „Eingabe", gehört aber offensichtlich nicht in den Snapshot. Dieses
   Ergebnis führt sie deshalb als eigene Klasse **erzeugt**.
2. **5a sagt nichts über Umgebung, die keine Datei ist.** Der Kalender ist der
   praktische Fall: er ist eine Eingabe im Sinne der Sache und liegt trotzdem
   nirgends als Datei. Ein Snapshot allein stellt Reproduzierbarkeit deshalb
   **nicht** her; es braucht das Lock daneben.
3. **5a sagt nicht, welcher Lauf gemeint ist.** Hier wurde der
   **Selektionslauf** genommen (so steht es in Registertext 5). Die
   Live-Pfade der neun Bots lesen **mehr** — etwa
   `config/groessenfaktor.json`, das nur `forward_test.py` liest und das
   dementsprechend **nicht** in der Liste steht.

### Zwei Befunde am Rande

* ⚠️ **`config/sp500_top25.txt` und `config/sp500_top50.txt` werden von
  niemandem gelesen.** Beide sind versioniert und liegen im Repo. Die
  Dokumentation von `stocks_symbols_config.py` sagt sogar *„Liest die
  Top-25-Liste aus `config/sp500_top25.txt`"* — der Code daneben liest
  `sp500_top150.txt`. **Der Kommentar widerspricht dem Code**; gelesen wird,
  was der Code sagt. Hier wurde nichts geändert.
* Die Hash-Berechnung steht **weiterhin zweimal** im Repo (Duplikat in
  `research/registernachtrag_tb41/pruefe_register.py:319`). Der Befund aus
  TB-46 besteht unverändert fort.

---

## Teil 2 — Das Werkzeug

`shared/snapshot.py`, drei Änderungen. **Die acht Abbruchgründe und die drei
Rückgabewerte sind unverändert geblieben**; drei Abbruchgründe sind
hinzugekommen.

### 1. Die Snapshot-Grenze

Die Eingabemenge aus Teil 1 wird **mit ihrer Ordnerstruktur** aufgenommen:

```
<snapshot_hash>/
    AAPL_1d.csv            die Kursdateien - flach, wie bisher
    BTCUSDT_1h.csv         ⭐ damit bleibt `datenstand_hash` rechenbar:
    ...                       das Verfahren ist NICHT rekursiv
    config/
        top25_symbols.txt  die übrigen Eingaben, mit ihrem Ordner
        sp500_top150.txt
    MANIFEST.json
```

⚠️ **Welche Dateien aufgenommen werden, steht in einer LISTE** (`EINGABEN` in
`snapshot.py`), **die im Manifest mitgeführt wird** — nicht in einer Regel.
Eine Regel („alles unter `config/`") hätte beim nächsten hinzugefügten
Konfigurationsschnipsel stillschweigend ihren Umfang geändert.

### 2. Zwei Hashes, zwei Funktionen, zwei Felder

| Feld | Verfahren | beantwortet |
|---|---|---|
| `snapshot_hash` | **neu**, `snapshot.py::snapshot_hash` — SHA-256 über die sortierten (Pfad, Inhalts-Hash)-Paare **der Dateien** | *„ist das derselbe Eingabesatz?"* — und er ist der **Name** |
| `datenstand_hash` | ⚠️ **unverändert** `herkunft.py::datenstand` | *„sind das dieselben Kursdateien?"* |

⚠️ **Der Snapshot-Hash läuft über die DATEIEN, nicht über das Manifest.**
Probe 3p zeigt das, statt es zu behaupten: ein ergänztes Manifestfeld lässt
den Namen unverändert — und dieselbe Probe rechnet zum Vergleich einmal über
das Manifest, wo dieselbe Lage als VERÄNDERT gälte.

⚠️ **Das Feld hiess bisher `datenstand`** und heisst jetzt `datenstand_hash`.
Neben einem zweiten Hash war „`datenstand`" nicht mehr unverwechselbar — es
hiess wie die Sache, die es misst, nicht wie die Frage, die es beantwortet.
Eine Verträglichkeits-Zweitschreibung wurde **bewusst nicht** angelegt: zwei
Felder mit demselben Inhalt sind genau die Doppelführung, die dieses Projekt
schon zweimal eingesammelt hat.

### 3. Die Teilkerzen-Prüfung im Manifest

Vor dem Ziehen läuft die **bestehende** Prüfung (`shared/zeitabdeckung.py`,
über den Dateipfad geladen — keine zweite Fassung) über die **Quelle**, nicht
über die Kopie. Ihr Ergebnis steht im Manifest:

```json
"teilkerzen": {
  "werkzeug": "shared/zeitabdeckung.py::pruefe_ordner",
  "stand": "…", "dateien_geprueft": 223,
  "befunde": [...], "frei_von_teilkerzen": false
}
```

⚠️ **Findet sie etwas, wird nicht gezogen.** Ist sie **nicht ausführbar**, ist
der Ausgang **2**, nie 0 — beides in Probe 3s und 3t nachgewiesen.

### Die drei neuen Abbruchgründe

| | |
|---|---|
| Eine Eingabedatei der Liste **fehlt** | Abbruch, die Datei wird namentlich genannt |
| Die Quelle enthält eine Datei **ausserhalb der Liste** | ⭐ **ABBRUCH** — siehe unten |
| **Teilkerzenbefund** oder Prüfung nicht ausführbar | Abbruch, kein Snapshot |

Dazu: `--ziehen` bricht ab, wenn `datenstand_hash` **nicht** `d9449faf…`
ergibt (`--kein-anker` schaltet das für Wegwerf-Verzeichnisse ab).

### ⭐ Die verlangte Entscheidung: Abbruch, nicht Meldung

**Entschieden wurde: Abbruch.** Begründung: der Name des Ordners ist der Hash
über **genau die Dateien der Liste**. Eine Datei daneben hat nur zwei mögliche
Ausgänge, und **beide sind still**:

* sie wird nicht mitkopiert → der Snapshot ist unvollständig und **sieht
  vollständig aus**;
* sie wird mitkopiert → die **Liste im Manifest lügt**.

Genau dieses „sieht gültig aus" bricht das Modul an allen vergleichbaren
Stellen schon ab (leere Quelle, Unterordner, vorhandenes `MANIFEST.json`).
Eine blosse Meldung wäre hier die einzige Ausnahme gewesen — und sie stünde im
Manifest neben einem Hash, der sie nicht deckt.

---

## Teil 3 — Die Wache

`shared/test_snapshot.py`: **69 → 110 Prüfungen, alle grün.**

Die **69 bestehenden Prüfungen sind erhalten**. Angepasst wurden nur ihre
Ankerpunkte, und zwar dort, wo TB-47 die bewachte Stelle verändert hat:

* der Feldname `datenstand` → `datenstand_hash` in vier Mutationsankern;
* ⚠️ **wo TB-47 eine zweite, unabhängige Wache an dieselbe Stelle gestellt
  hat, entfernen die Proben jetzt beide.** Sonst zeigte eine Probe nur noch,
  dass *irgendeine* Wache greift, nicht mehr *ihre eigene* — sie hätte
  aufgehört, das zu messen, wofür sie da ist. Betrifft 3a, 3b, 3d, 3f, 3g,
  3h, 3i, 3m.
* `abschnitt_2` legt seine Nicht-Kursdatei jetzt in die **Wurzel** statt in
  die Quelle (seit 3r ist eine Datei in der Quelle ein Abbruchgrund) und
  prüft dieselbe Aussage — Vollständigkeit inklusive Nicht-`.csv` — nun
  **mit** Ordnerstruktur.

### Die neun neuen Proben (3n–3v)

| Probe | Fall | Ergebnis |
|---|---|---|
| **3n** | Nicht-Kursdatei im Snapshot verändert | ⭐ `datenstand_hash` **bleibt gleich**, `snapshot_hash` **ändert sich** — genau dafür gibt es zwei |
| **3o** | Kursdatei verändert | **beide** ändern sich, beide werden genannt |
| **3p** | Feld im Manifest ergänzt | `snapshot_hash` **bleibt gleich**; über das Manifest gerechnet wäre dieselbe Lage VERÄNDERT |
| **3q** | Eingabedatei der Liste fehlt | Abbruch (2), Datei namentlich genannt |
| **3r** | Datei in der Quelle ausserhalb der Liste | Abbruch (2), Datei genannt |
| **3s** | Teilkerzen-Prüfung schlägt an | Abbruch (2), **kein** Snapshot |
| **3t** | Teilkerzen-Prüfung nicht ausführbar | **Rückgabewert 2**, nie 0 — in zwei Varianten (fehlt / wirft) |
| **3u** | `datenstand_hash` weicht von `d9449faf…` ab | Abbruch (2), der verankerte Wert wird genannt |
| **3v** | das Manifest führt beide Hashes, die Liste und die Teilkerzen | alle Felder vorhanden und getrennt |

⚠️ **Jede neue Probe zeigt, dass sie beisst** — dieselbe Bauform wie bisher:
die Wache im Speicher entfernen, das Ergebnis als eigenes Modul ausführen,
dieselbe Probe erneut laufen lassen. Ohne die jeweilige Wache gilt dieselbe
Lage als unverändert bzw. entsteht der Snapshot.

**Die Negativprobe** (unberührter Snapshot → UNVERÄNDERT, 0) ist unverändert
grün.

---

## Teil 4 — Der Enkelprozess im Basislauf

**Der Befund:** `basislauf.py` schickte nach der Zeitgrenze `kill()` an den
**Kindprozess**. Ein Test, der sich selbst einen Unterprozess startet, liess
damit einen **Enkel** zurück — er verlor nur seinen Elternprozess, hängte sich
an PID 1 und rechnete weiter. In **beiden** Mac-Läufen beobachtet, zuletzt
**22 Minuten bei 99 % CPU**, bis ihn ein Mensch von Hand beendete.

**Die Abhilfe** hat zwei Hälften, und beide sind nötig:

* `start_new_session=True` beim Start — der Kindprozess wird Anführer einer
  **eigenen Prozessgruppe**, und jeder Enkel landet in derselben Gruppe. Ohne
  das zeigte `os.killpg` auf die Gruppe des Runners selbst — er brächte sich
  um.
* `os.killpg` statt `kill()` — erst `SIGTERM` (damit ein Test seine
  Wegwerf-Verzeichnisse noch aufräumen kann), nach kurzer Frist `SIGKILL`.

**Der Nachweis:** `research/datenordner_schnitt/test_prozessgruppe.py`,
**11 von 11 Prüfungen grün**. Ein Wegwerf-Programm startet sich selbst ein
Kind, beide rechnen endlos.

```
1.5 ⭐ DER ENKELPROZESS LEBT EBENFALLS NICHT MEHR
2.3 ⭐ der Enkelprozess ueberlebt das alte Verfahren - genau das war der Befund
```

⚠️ **Zeile 2.3 ist der Grund, warum der Nachweis etwas wert ist.** Ohne die
Gegenprobe könnte der Test grün sein, weil der Enkel aus einem ganz anderen
Grund stirbt. Er stirbt aber nur mit der Reparatur.

*Nebenbei repariert: `lebt()` prüft nicht nur `os.kill(pid, 0)`, sondern auch
auf **Zombie**. Ein beendetes Kind bleibt stehen, bis jemand es abholt, und
nimmt Signal 0 noch an — ein Zombie rechnet aber nicht.*

---

## Datenstand vorher und nachher

| | Hash | Dateien |
|---|---|---|
| **vor** der Arbeit | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | 223 |
| **nach** der Arbeit | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | 223 |

**Unverändert.** `git status --porcelain -- data` ist leer. Es wurde **kein
Snapshot gezogen** und **nichts nach `data/` geschrieben**; das Werkzeug wurde
ausschliesslich an Wegwerf-Verzeichnissen unter `tempfile.mkdtemp()` geprüft.

---

## Umgebung — jede Abweichung von der Tabelle

*Gemessen in dieser Sitzung, nicht übernommen.*

| | Auftragstabelle | **hier vorgefunden** |
|---|---|---|
| Python | 3.11+ | **3.11.15** ✅ |
| Pakete | „in TB-46 fehlten sie fast alle" | ⚠️ **bestätigt** — `pandas`, `numpy`, `yfinance`, `binance`, `dateparser`, `scipy`, `pandas_market_calendars`, `pytz`, `matplotlib` fehlten **alle**. Nur `requests` (2.33.1) war da |
| `pandas` | „wechselnd; 3.x verlangt `>=3.11`" | ⚠️ **nachinstalliert: 3.0.6** — also die 3.x-Reihe, **nicht** die 2.3.3 des Macs |
| `node` | Mac v24.21.0 | **v22.22.2** in der Cloud |
| `timeout` (GNU) | Mac: fehlt | in der Cloud **vorhanden** (`/usr/bin/timeout`) — der Python-Runner wurde trotzdem benutzt, denn er ist der, der auf dem Mac läuft |
| Netz | gesperrt | **bestätigt** (nur der Paketspiegel war erreichbar) |

**Nachinstalliert wurde** (`pip install`, in zwei Runden):

| Runde | Pakete |
|---|---|
| für Teil 1–4 | `pandas 3.0.6`, `numpy 2.4.6`, `pandas_market_calendars 5.4.0`, `pytz 2026.3.post1`, `dateparser 1.4.3` |
| für den Basislauf | `fastapi`, `uvicorn`, `httpx`, `yfinance 1.7.0`, `python-binance 1.0.37` |

⚠️ **`scipy` wurde bewusst NICHT nachinstalliert.** Es fehlt auf dem Mac
ebenfalls, und `research/hrp_portfolio/test_hrp_core.py` ist dort deshalb
bekannt rot. Ein Grün, das der Betriebsrechner nicht erreichen kann, wäre
irreführend.

⚠️ **`pandas 3.0.6` gegen `pandas 2.3.3` auf dem Mac ist ein struktureller
Unterschied**, keine Kleinigkeit. Er berührt diese Arbeit allerdings an
**keiner** Stelle: `shared/snapshot.py`, `shared/zeitabdeckung.py`,
`research/snapshotgrenze/erhebung_eingaben.py` und
`research/datenordner_schnitt/basislauf.py` kommen **alle ohne `pandas` aus**
(nur Standardbibliothek). Der Mac-Testauftrag prüft das auf 3.9.6 nach.

---

## Basislauf

**64 Testdateien, Zeitgrenze 900 s je Datei** (`trading-env/` ausgeschlossen).

| | | |
|---|---|---|
| **grün** | **56** | darunter `shared/test_snapshot.py` (110/110) und `research/datenordner_schnitt/test_prozessgruppe.py` (11/11) |
| **rot** | **4** | 3 bekannt, 1 erklärt — siehe unten |
| **ungeprüft** | **3** | ⚠️ **nicht rot** — sie verlangen ein Bot-Argument |
| **Zeitgrenze** | **1** | `shared/test_drawdown_beide_masse.py` (bekannt) |

### Die vier roten

| Datei | Ursache |
|---|---|
| `shared/test_stabile_sortierung.py` (3) | **bekannt rot**, unverändert |
| `shared/test_wellenauswahl.py` (1) | **bekannt rot**, unverändert |
| `research/hrp_portfolio/test_hrp_core.py` | **bekannt rot** — `scipy` fehlt auch in dieser Cloud |
| `shared/test_zuteilung.py` | ⚠️ **Netzsperre** — `ProxyError … api.binance.com`. Genau der in der Aufgabenstellung als „nur Cloud" genannte Fall. *Der Runner markiert ihn als „UNERWARTET", weil seine `BEKANNT_ROT`-Liste **Mac-Werte** führt und dieser Test dort grün ist — die Markierung ist richtig, der Befund ist trotzdem erklärt.* |

### Die drei ungeprüften

`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py` — ⚠️ **ungeprüft, nicht rot**,
wie in der Aufgabenstellung vermerkt.

### ⭐ Zwei Tests sind besser als erwartet

`dashboard/test_portfolio_sicht.py` (91/91) und
`research/exposure_messung/test_exposure_kern.py` sind hier **grün**, obwohl
sie als bekannt rot geführt werden. Beide Einträge sind **Mac-Messungen**
(dort liegen die Live-Datenbanken) — kein Widerspruch, aber es zeigt einmal
mehr, dass die Liste ihre Rechnerangabe braucht.

### ⚠️ Ein erster Lauf war rot, und zwar an der Paketlage

Der **erste** Basislauf dieser Sitzung meldete **10 rot**, davon 6
unerwartet. Alle sechs lagen an fehlenden Fremdpaketen, nicht an dieser
Arbeit. Nach dem Nachinstallieren einzeln nachgemessen:

| Datei | vorher | nachher |
|---|---|---|
| `dashboard/test_dashboard.py` | `ModuleNotFoundError: fastapi` | **784/784** ✅ |
| `shared/test_kursdaten.py` | `ModuleNotFoundError: yfinance` | **82/82** ✅ |
| `shared/test_leeres_symbol.py` | `ModuleNotFoundError: binance` | **45/45** ✅ |
| `shared/test_groessenfaktor.py` | `ModuleNotFoundError` | **171** ✅ |
| `shared/test_ladeprotokoll.py` | `ModuleNotFoundError` | **182** ✅ |
| `research/universum_trockenlauf/…` | `ModuleNotFoundError: yfinance`/`binance` | **306** ✅ |

Der oben berichtete Basislauf ist der **zweite**, mit vollständiger
Paketlage. ⚠️ **Das ist der in `docs/UMGEBUNGEN.md` beschriebene Fall in
Reinform:** „die Cloud ist nicht EINE Umgebung, sondern eine je Sitzung."

### ⭐ Und der Nebenbeweis für Teil 4

`shared/test_drawdown_beide_masse.py` lief in **beiden** Basisläufen in die
Zeitgrenze — und startete dabei, wie auf dem Mac, einen Enkelprozess
`--bot elliott_wave`. Beide Male gemessen, direkt nach dem Abbruch:

```
Ueberlebende Prozesse: 0
```

Der Befund, der auf dem Mac zweimal 22 Minuten CPU gekostet hat, ist damit
**im echten Basislauf** und nicht nur im Prüfprogramm erledigt.

---

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ❌ | **Kein Snapshot gezogen.** Das Werkzeug wurde an Wegwerf-Verzeichnissen geprüft |
| ❌ | `data/` nicht angefasst, nicht umbenannt, nichts hineingeschrieben |
| ❌ | `forward_test.py`, `live_params.py`, `equity_simulation.py`, `entscheidungskerze.py`, `paths.py` — **unberührt** |
| ❌ | Kein Modul auf einen neuen Pfad umgestellt |
| ❌ | Kein Registertext geändert — Teil 1 **berichtet**, wo 5a unscharf ist |
| ❌ | Kein Datencron, keine Gleichheitsprüfung |
| ❌ | Kein Netzabruf, kein Broker-Endpunkt, kein `--echt` |
| ❌ | Keine Konfigurationsdatei mit Zugangsdaten gelesen (nur `test -f` / `grep -c`) |

---

## Was geändert wurde

| Datei | |
|---|---|
| `shared/snapshot.py` | Grenze, zwei Hashes, Teilkerzen-Prüfung (637 → 1085 Zeilen) |
| `shared/test_snapshot.py` | 69 → **110** Prüfungen |
| `research/datenordner_schnitt/basislauf.py` | `start_new_session=True`, `beende_gruppe()` |
| `research/datenordner_schnitt/test_prozessgruppe.py` | **neu** — der Nachweis zu Teil 4 |
| `research/snapshotgrenze/erhebung_eingaben.py` | **neu** — das Erhebungswerkzeug zu Teil 1 |
| `research/snapshotgrenze/ergebnisse/eingaben.json` | **neu** — die Rohdaten der Erhebung |
| `docs/ERGEBNIS_TB-47_snapshotgrenze.md` | dieses Dokument |
| `docs/TESTAUFTRAG_TB-47_snapshotgrenze.md` | der Mac-Testauftrag |

⚠️ **Unberührt geblieben:** `strategies/*/live_params.py`,
`strategies/*/forward_test.py`, `strategies/*/equity_simulation.py`,
`shared/entscheidungskerze.py`, `shared/paths.py`, `data/`, jede Crontab,
jeder Registertext.

### `git status --porcelain`

Nach dem letzten Commit dieser Sitzung: **leer**. Die Ausgabe ist unten im
Rohdaten-Archiv (`git_status_ende.txt`) abgelegt.

---

## In einfacher Sprache

Ein „Snapshot" ist eine eingefrorene Kopie von allem, womit gerechnet wurde.
Er trägt einen langen Zahlen-Namen, der aus seinem Inhalt errechnet ist —
ändert sich der Inhalt, passt der Name nicht mehr. So lässt sich später
zeigen, dass niemand nachträglich etwas verändert hat.

Bisher hat unser Werkzeug nur die **Kursdaten** eingefroren. Das war zu wenig.
Wir haben deshalb erst einmal **nachgesehen**, was der Rechenlauf noch alles
liest — nicht geraten, sondern den Programmtext von 142 Dateien systematisch
durchgegangen. Heraus kamen **zwei weitere Dateien**: die Listen, welche
Kryptowährungen und welche Aktien überhaupt gehandelt werden. Die wandern
jetzt mit in die Kopie. Welche Dateien dazugehören, steht dabei ausdrücklich
**aufgeschrieben** in der Kopie selbst — damit später niemand raten muss.

Der **Börsenkalender** (welcher Tag ein Handelstag ist) kommt nicht aus einer
Datei, sondern aus einem fremden Programmpaket. Den kann eine Kopie nicht
einfrieren. Das ist keine Schlamperei, sondern eine Eigenschaft des Aufbaus —
aber man sollte es wissen.

Neu gibt es **zwei** Zahlen-Namen statt einem. Der eine beantwortet „sind das
dieselben Kursdaten?", der andere „ist das derselbe Satz an Eingaben
insgesamt?". Man braucht beide: ändert jemand nur die Symbolliste, bleibt die
erste Zahl gleich und nur die zweite schlägt aus.

**Und dann der wichtigste Punkt:** Bevor eine Kopie gezogen wird, prüft das
Werkzeug jetzt, ob alle Kurskerzen vollständig sind — eine „halbe" Kerze
verfälscht jede Rechnung. Diese Prüfung ist zum ersten Mal über den echten
Bestand gelaufen, und sie **hat etwas gefunden**: bei 36 von 223 Dateien ist
die **allererste** Kerze unvollständig. Das ist ein alter, bekannter Umstand.
Es bedeutet aber: **die Kopie lässt sich heute nicht ziehen**, das Werkzeug
verweigert es. Ob man die 36 ersten Kerzen repariert oder ausdrücklich
beschliesst, sie hinzunehmen, ist eine Entscheidung, die der Betreiber treffen
muss — nicht diese Sitzung. Die gute Nachricht: die **letzte** Kerze, die
eigentlich gefährliche, ist bei allen 223 Dateien sauber.

Zuletzt eine kleine, lästige Reparatur: Wenn ein Test zu lange lief, hat der
Testlauf ihn abgebrochen — aber ein von diesem Test selbst gestartetes
Unterprogramm lief munter weiter und verbrauchte zuletzt 22 Minuten lang
einen ganzen Rechnerkern. Das passiert nicht mehr. Und wir haben es nicht nur
behauptet, sondern beides vorgeführt: dass es jetzt aufhört — und dass es
vorher wirklich weiterlief.
