# Kursdaten: Neuaufbau und Zeitabdeckung (TB-34)

Zwei Werkzeuge, die zusammengehören, aber getrennt bleiben:

| Werkzeug | Was es tut | Schreibt es? |
|---|---|---|
| [`shared/kursdaten_neuaufbau.py`](kursdaten_neuaufbau.py) | lädt den Krypto-Kursdatenbestand **nativ** neu — 1h, 4h und 1d | ja, nur mit `--schreiben` |
| [`shared/zeitabdeckung.py`](zeitabdeckung.py) | prüft, ob die **erste und letzte Kerze** jeder Kursdatei ihren Zeitraum abdeckt | nein, nie |
| [`shared/abrufschutz.py`](abrufschutz.py) **(TB-35)** | hält die **laufende Kerze** aus den acht Abrufskripten heraus und wacht darüber, dass ein Abruf keine Datei **verkürzt** | nein, nie — es schreibt nur, wer es benutzt |

Beide gehören zur Familie der eigenständigen Prüf- und Pflegewerkzeuge
(`ergebniskurven.py`, `determinismus.py`, `kursdaten.py`, `binance_historie.py`)
und werden von **keinem** Bot importiert.

---

## 1. Warum es sie gibt

Drei Befunde aus TB-31, in TB-34 unabhängig nachgerechnet:

1. **Alle 72 Krypto-Kursdateien enden mit einer Teilkerze.** Der letzte Abruf
   von Hand lief am 2026-08-31 gegen 13:00 UTC. Die letzte Tageskerze jeder
   `*_1d.csv` deckt deshalb **13 von 24 Stunden** ab, die letzte 4h-Kerze
   **1 von 4**.
2. **Die 24 Tagesdateien sind abgeleitet, nicht abgerufen.**
   `shared/build_daily_crypto_data.py` hat sie aus den 1h-Daten resampelt —
   ausdrücklich als Sandbox-Ersatz. Ihre **erste** Tageskerze deckt je nach
   Symbol **6 bis 16 von 24 Stunden** ab.
3. **Kein Cronjob aktualisiert `data/`.** Die neun `forward_test.py` holen
   ihre Daten live beim Lauf; `data/` wird nur von Hand gefüllt.

`shared/kursdaten.py` findet davon **nichts**: es prüft auf *fehlende* Werte,
und eine Teilkerze hat vier gefüllte Kursspalten. Sie ist nicht leer, sie ist
falsch.

---

## 2. `zeitabdeckung.py` — die Wache

```bash
python3 shared/zeitabdeckung.py                       # prüft data/
python3 shared/zeitabdeckung.py --datei data/BTCUSDT_1d.csv
python3 shared/zeitabdeckung.py --stand 2026-08-31T13:00:00
python3 shared/zeitabdeckung.py --datenbeginn neuaufbau.json
python3 shared/zeitabdeckung.py --json bericht.json
```

Rückgabewert **1** bei Befund, 0 sonst, 2 bei Aufruffehler. Nur
Standardbibliothek, streamt die Dateien zeilenweise.

### Drei Zeugen, jeder mit benannter Reichweite

| | Zeuge | Immer möglich? |
|---|---|---|
| **R** | **Raster** — jede `open_time` sitzt auf dem Raster ihres Intervalls, jeder Abstand ist ein ganzes Vielfaches | ja |
| **D** | **Deckung** — die feinere Datei desselben Symbols belegt den Zeitraum der ersten und letzten groben Kerze (`1d`←`1h`, `4h`←`1h`) | nur wo es eine feinere Datei gibt |
| **S** | **Stand** — der Zeitraum der letzten Kerze muss zum Stichzeitpunkt abgelaufen sein | ja |

Die Deckungsprüfung vergleicht zusätzlich die grobe Kerze mit dem **Aggregat
genau der vorliegenden** feineren Kerzen. Stimmt es auf die letzte Stelle, ist
die grobe Kerze daraus **abgeleitet** — das ist ein Nachweis, kein Verdacht.

### Was sie nicht kann — und warum das dasteht

Die letzte Kerze der **feinsten** Datei eines Symbols (`X_1h.csv`) hat keinen
feineren Zeugen. War sie beim Abruf angeschnitten, steht das nirgends in den
Dateien. Der Bericht sagt deshalb je Datei, welche Zeugen greifen konnten:
**eine Datei ohne Befund ist nicht dasselbe wie eine geprüft vollständige.**

Dagegen helfen nur zwei Dinge, beide ausserhalb dieses Programms: der
Stand-Zeuge, wenn kurz **nach** dem Abruf geprüft wird, und
`kursdaten_neuaufbau.py`, das eine laufende Kerze gar nicht erst schreibt.

### Die erste Kerze einer Historie

Eine kurze **erste** Kerze kann zwei Ursachen haben — ein beschneidendes
Abruffenster (Fehler) oder den Listing-Tag (richtig). Offline ist das nicht
entscheidbar. Voreinstellung: **melden**. Mit `--datenbeginn <bericht.json>`
(dem JSON-Bericht des Neuaufbaus, der den gemessenen Datenbeginn je Symbol
enthält) gilt eine kurze erste Kerze **am gemessenen Datenbeginn** als
richtig, sonst weiterhin als Befund.

### Warum sie nicht in `kursdaten.py` gehört

1. `kursdaten.entferne_unvollstaendige()` läuft in **allen neun Bots** bei
   jedem Laden, zeilenweise auf einem DataFrame im Speicher. Die
   Deckungsprüfung braucht **andere Dateien** und einen Stichzeitpunkt —
   beides wäre in einer Zeilenmaske fehl am Platz und kostete jeden Botlauf
   zusätzliche Lesevorgänge.
2. `kursdaten.py` **streicht und zählt**. Eine Teilkerze darf nicht
   stillschweigend gestrichen werden: die letzte Tageskerze zu streichen
   verschöbe das Ende jedes Backtests. Sie gehört gemeldet und von einem
   Menschen entschieden.
3. **Der Live-Betrieb darf nie an einer Datenprüfung hängenbleiben.**

---

## 3. `kursdaten_neuaufbau.py` — der Neuaufbau

```bash
python3 shared/kursdaten_neuaufbau.py                         # Trockenlauf
python3 shared/kursdaten_neuaufbau.py --schreiben
python3 shared/kursdaten_neuaufbau.py --symbole BTCUSDT --zeitrahmen 1d
python3 shared/kursdaten_neuaufbau.py --stand 2026-09-15T00:00:00
python3 shared/kursdaten_neuaufbau.py --bericht neuaufbau.json
python3 shared/kursdaten_neuaufbau.py --zurueckspielen data_sicherung/<lauf>
```

Rückgabewerte: 0 in Ordnung, 1 Befund, 2 Aufruffehler, 3 Abbruch (HTTP 418).

### Die fünf Zusicherungen

**1. Nur `/api/v3/klines`** — öffentlich, ohne Schlüssel, kein `/sapi/`, kein
`/fapi/`. Das gitignorierte `shared/fetch_binance_data.py` (enthält
Zugangsdaten) wird nicht eingebunden; der Selbsttest sieht sich die wirklich
gestellten Anfragen an.

**2. Keine angeschnittene Kerze — strukturell.** Übernommen wird nur, was der
Endpunkt als abgeschlossen meldet (`close_time <= Stand`). Der Fehler, der
diese Aufgabe ausgelöst hat, ist damit nicht vermieden, sondern *unmöglich*.

**3. Sicherung vor dem Schreiben.** Jede Datei wird kopiert, **bevor** sie
ersetzt wird — nach `data_sicherung/<JJJJ-MM-TT_HHMMSS>/` neben `data/`, mit
SHA-256 je Datei im `MANIFEST.json`. Das Manifest wird nach jeder Datei
fortgeschrieben, damit auch ein abgebrochener Lauf eine gültige Sicherung des
bereits Ersetzten hinterlässt. Ein **belegter** Sicherungsordner wird
abgelehnt statt überschrieben.

**4. Vergleich alt gegen neu, Zeile für Zeile.** Je Datei: Zeilenzahl,
Zeitraum und die Zahl der Zeilen, die sich im gemeinsamen Bereich
unterscheiden. Eine Abweichung an den **Rändern** (erste oder letzte Zeile des
Altbestands) ist die erwartete Teilkerze. Jede Abweichung **dazwischen** ist
ein Befund, verhindert das Schreiben dieser Datei und steht am **Anfang** der
Zusammenfassung. Dafür gibt es **keinen** Schalter.

**5. Wiederholbar.** Zwei Läufe mit demselben `--stand` liefern
byte-identische Dateien.

### Wohin die Sicherung geht, und wie lange sie bleibt

`data_sicherung/<Zeitstempel>/` neben `data/`, in `.gitignore` eingetragen.
Der volle Krypto-Bestand sind rund **184 MB** je Lauf.

**Es wird nichts automatisch gelöscht.** Die Log-Rotation (Protokoll 4.6) hält
fünf Stände und löscht ältere; dort ist das richtig, weil ein verlorener
Logeintrag ärgerlich ist. Hier fällt dieselbe Abwägung anders aus: ein
Kursdatenstand ist **nicht wiederherstellbar**, wenn der Endpunkt ihn nicht
mehr so liefert. Der Lauf meldet am Ende die Grösse und den Pfad.

**Vorschlag für die Aufbewahrung:** die Sicherung eines Laufs behalten, bis
der neue Bestand angenommen ist — also bis `zeitabdeckung.py` sauber meldet,
`research/krypto_historie/faltenplan.py` neu gerechnet ist und die
Ergebniskurven bewusst neu erzeugt wurden. Danach von Hand löschen:

```bash
rm -rf data_sicherung/<Zeitstempel>
```

### Warum ein eigenes Modul neben `binance_historie.py`

`binance_historie.py` (TB-31) **verlängert** nach vorn und schreibt jede
vorhandene Zeile zeichengleich zurück. Sein ganzer Wert liegt darin, niemals
zu überschreiben. Beides in eine Datei zu legen hiesse, diese Zusicherung von
einem Laufzeitschalter abhängig zu machen — genau die Bauform, die das Projekt
bei der Binance-Brücke schon einmal verworfen hat (`testnet=True` als Flag im
Aufrufpfad, Protokoll 4.4).

Geteilt wird trotzdem alles, was sich teilen lässt, und zwar durch
**Benutzung**: `Drossel`, `Abrufer`, `kerzen_laden`, `erste_kerze_ms`,
`als_dataframe`, `zeilen_aus_dataframe`, `schreibe_datei`, `ZEITFORMAT`,
`Kursdatei` und die 418-Behandlung kommen aus `binance_historie`. Es gibt nur
**eine** Netzstelle und nur **eine** Schreibweise im Projekt.

### Ratenbegrenzung

Unverändert aus `binance_historie.Drossel`: Mindestpause 0,25 s, Auswertung
von `x-mbx-used-weight-1m` mit Pause ab 70 % des Budgets (6000/min, `klines`
wiegt 2), `429` mit `Retry-After` abwarten und wiederholen, **`418` bricht den
Lauf ab**. Ein voller Neuaufbau über 72 Dateien stellt rund **3000** Anfragen.

---

## 4. Selbsttests

```bash
python3 shared/test_zeitabdeckung.py            # 40/40
python3 shared/test_kursdaten_neuaufbau.py      # 67/67
python3 research/kursdaten_neuaufbau/probelauf.py   # 295/295, gegen die echten Dateien
```

Der Probelauf fährt den Neuaufbau im Trockenlauf gegen **alle 72 echten
Kursdateien** des Repos — mit einer Gegenstelle, die aus der jeweiligen Datei
selbst gebaut wird. Er fasst keine Datei im Repo an; die Schreibprobe läuft auf
einer Kopie in einem temporären Ordner.

---

## 5. Cron

### Vorschlag, **nicht eingetragen**

```cron
0 4 * * * cd ~/trading-bot && /usr/bin/python3 shared/zeitabdeckung.py >> logs/system/zeitabdeckung.log 2>&1
```

Einmal täglich um 4:00 Uhr, also nach Log-Rotation (3:30), Portfolio-Sicht
(3:40) und Ergebniskurven (3:50), und mit Abstand zu den 4-Stunden-Läufen der
Bots. Den Ordner vorher anlegen: `mkdir -p logs/system`.

Begründung: die Prüfung ist rein lesend, braucht kein Netz und läuft in rund
40 Sekunden über alle 242 Kursdateien. Ihr Wert liegt im **Stand-Zeugen** —
sie meldet eine Kerze, deren Zeitraum noch läuft, und findet damit genau die
Art Fehler, die den Altbestand erzeugt hat, am Tag nach dem Abruf statt zwei
Wochen später.

> **Hinweis wie bei den Ergebniskurven:** Die Crontab des Nutzers liess sich am
> 12.09.2026 nicht ändern (`crontab -`, `Operation not permitted`). Das
> Werkzeug ist deshalb bewusst auch von Hand sinnvoll aufrufbar — es hat keinen
> Zustand. Der passende Zeitpunkt von Hand ist: **nach jedem Datenabruf** und
> **vor jeder Auswertung, die `data/` liest.**

### Und der tägliche Abruf? — berichtet, nicht entschieden

Für die Frage, ob `data/` täglich aktualisiert werden soll, siehe
[`research/kursdaten_neuaufbau/BERICHT.md`](../research/kursdaten_neuaufbau/BERICHT.md),
Abschnitt 4. Die Kurzfassung:

* **Dafür** spricht viel: `data/` ist heute zwei Wochen alt, und **101 Module**
  rechnen darauf, ohne dass irgendetwas den Stand prüft.
* **Dagegen** spricht die Form, in der ein Abruf heute stattfände. Alle acht
  Abrufskripte **überschreiben** ihre Dateien vollständig (`df.to_csv(...)`),
  und keines von ihnen schliesst die **laufende** Kerze aus. Die vier
  Krypto-Skripte holen ausserdem aus einem **relativen** Zeitfenster; zwei
  davon stehen weiterhin auf `"3650 day ago UTC"`. Täglich per Cron
  ausgeführt, würden sie den Fehler, den TB-34 gerade behebt, zur **täglichen
  Gewohnheit** machen.
* Ein Werkzeug, das die Dateien **hinten verlängert**, gibt es in diesem
  Projekt **nicht** — `binance_historie.py` verlängert nur nach vorn,
  `kursdaten_neuaufbau.py` baut vollständig neu.

Deshalb steht hier **keine** Cron-Zeile für den Abruf. Eine solche Zeile
einzutragen, bevor es ein Werkzeug gibt, das anfügt statt zu ersetzen, wäre die
falsche Reihenfolge.

---

# Nachtrag TB-35 — die offene Frage von oben ist beantwortet

Der letzte Abschnitt dieses Dokuments endete mit drei Gründen, warum es
**keine** Cron-Zeile für den Abruf gibt. Zwei davon sind seit TB-35 erledigt,
einer bleibt bewusst stehen.

## Was sich geändert hat

| Befund von TB-34 | Stand nach TB-35 |
|---|---|
| „keines schliesst die **laufende** Kerze aus" | **erledigt** — alle acht filtern sie **vor** dem Schreiben |
| „zwei stehen weiterhin auf `3650 day ago UTC`" | **erledigt** — beide auf `1 Jan, 2017`, die widerlegte Begründung ist entfernt |
| „ein Werkzeug, das die Dateien **hinten verlängert**, gibt es nicht" | **bleibt so — mit Absicht.** Siehe unten |

## Warum weiterhin überschrieben wird

Der Einwand, an dem die Entscheidung hängt:

> Ein anhängendes Werkzeug, das sich irrt, verlängert eine Datei mit falschen
> Zeilen, und der Fehler bleibt **dauerhaft** stehen. Ein überschreibendes, das
> sich irrt, ist beim **nächsten Lauf** wieder in Ordnung.

**Überschreiben war nie das Problem — die Teilkerze am Ende war es.** Mit dem
Filter ist die Ursache weg. Dazu: `binance_historie.py` führt für „verlängern"
bereits einen Vertrag, dessen ganzer Wert darin liegt, **nie** zu
überschreiben; ein drittes Werkzeug mit einem vierten Vertrag wäre genau die
Unübersichtlichkeit, die TB-34 beklagt hat. Und Anhängen bräuchte eine
Konfliktregel für den Fall, dass der Endpunkt eine gespeicherte Kerze anders
liefert als beim letzten Mal — die kann niemand allgemein richtig festlegen.

Der Preis des Überschreibens ist abgesichert, nicht weggeredet: dafür gibt es
die Wache.

## Die Wache

```bash
python3 shared/abrufschutz.py --aufnehmen /tmp/vorher.json
#   ... hier den Abruf laufen lassen ...
python3 shared/abrufschutz.py --vergleiche /tmp/vorher.json    # 1 bei Befund

python3 shared/abrufschutz.py --aufnehmen X --ordner ANDERER_ORDNER
python3 shared/abrufschutz.py --vergleiche X --json bericht.json
```

Rückgabewert **1** bei Befund, 0 sonst, 2 bei Aufruffehler. Sie schlägt an,
wenn eine Datei nach dem Abruf **weniger Zeilen** hat, **später beginnt**,
**früher endet** oder **verschwunden** ist — und ausdrücklich **nicht**, wenn
sie nur verlängert wurde, gleich geblieben ist oder neu hinzukommt.

**Drei Kriterien, weil eines nicht reicht.** Eine Datei kann bei *gleicher*
Zeilenzahl später beginnen (vorne fehlt etwas, hinten kam etwas dazu) oder
früher enden. Wer nur zählt, sieht beides nicht.
`shared/test_abrufschutz.py` Abschnitt 6 schaltet die Kriterien einzeln ab und
weist nach, dass dann genau der eine zugehörige Fall verlorengeht — und die
anderen beiden nicht.

**Sie meldet und stoppt nie.** Die acht Abrufskripte rufen sie selbst auf (sie
brauchen einen Vergleichswert von **vor** dem Lauf, den es hinterher nicht mehr
gibt) und setzen bei Befund den Rückgabewert auf 1 — dieselbe Hausregel wie
`kursdaten.py`: *ein Befund ist kein Fehler des Programms, aber etwas, das ein
Cronjob-Aufruf sichtbar machen soll.* Geschrieben wird trotzdem; zurückgenommen
wird nichts.

## Und die Cron-Zeile?

**Steht hier weiterhin nicht.** Die zwei technischen Hindernisse sind weg, aber
die Entscheidung, ob `data/` täglich mitwachsen soll, ist eine des Betreibers —
und sie berührt den **Datenstand-Hash der Vorregistrierung**
(`docs/VORREGISTRIERUNG_neuselektion.md`), der sich dann täglich änderte. Das
ist kein Abrufthema mehr, sondern eines der Vorregistrierung.

Was sich geändert hat, ist die Gefahrenlage: ein Abruf von Hand ist jetzt
**verlustfrei**. Er verlängert oder lässt gleich; er verkürzt nicht, und er
schreibt keine Teilkerze mehr.

Einzelheiten: Kopf von [`shared/abrufschutz.py`](abrufschutz.py),
[`docs/UEBERGABE_TB-35_abrufskripte.md`](../docs/UEBERGABE_TB-35_abrufskripte.md),
[`research/abrufskripte/BERICHT.md`](../research/abrufskripte/BERICHT.md).
