# Ergebnis TB-49 — Die Ausnahme ins Werkzeug, der Prüfer ins Repo

**Cloud-Sitzung, 18.09.2026.** Vorgänger: TB-48 (gemergt `db8913a`).
Zweig: `claude/new-session-kfbw56`.

**Klein und scharf umrissen.** Ein Werkzeug lernt eine Regel, seine Wache zieht
mit, ein Prüfer kommt ins Repo, eine offene Zahl wird geklärt. **Kein Bot-Code,
kein Parameter, kein Registertext, kein Snapshot.**

---

## Die fünf Fragen des Auftrags, zuerst

| Frage | Antwort |
|---|---|
| ⭐ **Zieht das Werkzeug jetzt — an einem Wegwerf-Bestand mit denselben 36 Befunden?** | **Ja.** Rückgabewert **0**, 225 Dateien, 211,0 MB, jede byteweise gegen die Quelle geprüft. Am Stand von TB-48 brach derselbe Lauf mit **2** ab. Beleg in Teil 1 |
| ⚠️ **Bricht es weiterhin ab bei `rand_letzte`, bei einem nicht-abgeleiteten `rand_erste` und bei einem Befund an einer späteren Kerze?** | **Ja, alle drei — je mit genannter Datei und Rückgabewert 2.** Die ersten beiden **am vollen Bestand von 223 Dateien** gemessen, der dritte an einem gestellten Befund, weil die heutige Prüfung ihn nicht vergibt. Teil 1 und 2 |
| ⚠️ **Wie verhält sich die Regel bei `kein_zeuge` — und warum so?** | ⭐ **Nicht belegbar ist nicht zugelassen.** An `data/` ist das **folgenlos**: die **175** Dateien mit `kein_zeuge` tragen **null** Befunde. Vollständige Begründung in Teil 2, Abschnitt „Der fünfte Fall" |
| **Führt das Manifest die zugelassenen Befunde samt Registerverweis?** | **Ja.** `zugelassene_befunde` mit **36** Einträgen (Datei, Art, erste Kerze), `zugelassene_befunde_anzahl: 36` und `zugelassene_befunde_herkunft` → **Registertext 5a, Zusatz · Abschnitt 17.3**. Wörtlich in Teil 1 |
| **Früheste Falte je Bot — und trägt die Vermutung aus Teil 4?** | ⚠️ **Die Vermutung trägt NICHT.** Alle **neun** Bots haben erstes Faltenjahr **2019** — Krypto wie Aktien. Die **2022 ist die falsche Zahl**, und sie widerspricht dem Register an einer **zweiten** Stelle (15.6). Teil 4 |

---

## 0. Datenstand — vorher und nachher

| | |
|---|---|
| **vorher** | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien |
| **nachher** | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien |
| **identisch** | ⭐ **ja** — `data/` ist in dieser Arbeit ausschliesslich gelesen worden |
| **Snapshot gezogen** | ⭐ **nein.** Weder `snapshots/` noch `data/snapshots/` entstanden — geprüft am Ende des Laufs |

⭐ **Gezogen wurde ausschliesslich in Wegwerf-Verzeichnisse** unter dem
Sitzungs-Ablagepfad, aus einer **Kopie** von `data/`. `data/` selbst ist in
dieser Arbeit nur gelesen worden.

---

## Teil 1 — Die Ausnahme in `shared/snapshot.py`

### 1.1 Was der Code jetzt kann — und was sich ausdrücklich nicht geändert hat

**Zugelassen ist ein Befund genau dann, wenn alle drei Bedingungen zutreffen**
(`shared/snapshot.py::_zulassung`):

| | Bedingung | Wie sie geprüft wird |
|---|---|---|
| **(a)** | Art ist `rand_erste` | gegen `ZUGELASSENE_ART` |
| **(b)** | Der Befund betrifft die **erste** Kerze der Datei | die Kerze aus der Deckungsprüfung wird gegen `eintrag["erste"]` gehalten |
| **(c)** | Die Kerze ist das Aggregat genau der vorhandenen feineren Kerzen | Urteil `ABGELEITETE_TEILKERZE` **und** `aggregat_passt is True` |

⭐ **Es ist eine Regel, keine Liste der 36 Dateien.** Die Begründung des
Auftrags ist übernommen: eine Liste veraltet, jedes neu gelistete Symbol bringt
denselben Befund mit, und eine ungepflegte Liste blockiert entweder zu Unrecht
oder — schlimmer — lässt zu Unrecht durch.

⚠️ **(b) wird eigens nachgestellt, obwohl die heutige Prüfung `rand_erste` nur
an der ersten Kerze vergibt.** Die Bedingung des Registers lautet „die erste
Kerze der Datei", nicht „ein Befund, der sich so nennt". *Wer die Herkunft des
Namens für den Nachweis nimmt, prüft nichts* — und Probe `3z` zeigt, dass das
kein theoretischer Einwand ist.

⚠️ **(c) holt das Urteil aus dem geladenen Modul, statt es abzuschreiben.**
Kennt `shared/zeitabdeckung.py` den Namen `ABGELEITETE_TEILKERZE` eines Tages
nicht mehr, ist die Bedingung **nicht mehr prüfbar** und es wird nicht gezogen
— Rückgabewert **2**. Eine Abschrift liefe gegen ein Urteil, das die Prüfung
gar nicht mehr vergibt: die Ausnahme griffe dann entweder nie oder immer.

**Was sich nicht geändert hat — gemessen, nicht behauptet:**

| | Gemessen |
|---|---|
| Die Prüfung schlägt weiter an | `36 Datei(en) mit Befund (223 Datei(en) geprüft)`. `teilkerzen()["befunde"]` führt unverändert **alle** 36 |
| ⚠️ `rand_letzte` bricht ab | am vollen Bestand gemessen, **eine** Datei genügt — siehe 1.4 |
| ⚠️ Ein Befund, der (a)–(c) nicht erfüllt, bricht ab | ebenfalls am vollen Bestand — siehe 1.4 |
| ⚠️ **Keine Übergehen-Flagge** | `--trotzdem`, `--erzwingen`, `--force` gibt es nicht; jede ergibt **2**. Probe `3ad` hält die Befehlszeile dagegen und durchsucht zusätzlich den Quelltext |

### 1.2 ⭐ Der Vorher-Nachher-Beleg am selben Bestand

**Am Stand von TB-48** (`git show db8913a:shared/snapshot.py`, gegen dasselbe
`data/`):

```
ABBRUCH: Die Teilkerzen-Pruefung hat 36 Datei(en) mit Befund gefunden:
AAVEUSDT_1d.csv, AAVEUSDT_4h.csv, ADAUSDT_1d.csv, BMTUSDT_1d.csv, … und 28
weitere. Es wird NICHT gezogen …
RC_ALT=2
```

**Mit diesem Zweig**, derselbe Bestand, Trockenlauf:

```
  ⚠️ Teilkerzen     36 Datei(en) mit Befund (223 Datei(en) geprueft)
      davon zugelassen   36 Befund(e) in 36 Datei(en) - docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3
      ⚠️ Die Pruefung schlaegt weiter an - gezogen wird gegen den Registereintrag, nicht gegen ihr Schweigen.

  TROCKENLAUF - nichts kopiert. Mit --ziehen wirklich ziehen.
RC_TROCKENLAUF=0
```

⭐ **Das ist die ganze Änderung in zwei Zahlen: 2 → 0, bei unveränderten 36
Befunden.**

### 1.3 Das Ziehen am Wegwerf-Bestand mit denselben 36 Befunden

`data/` wurde in ein Wegwerf-Verzeichnis kopiert (223 Dateien, 202 MB) und der
Snapshot **von dort nach dort** gezogen — `data/` blieb unberührt.

```
  snapshot_hash    63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2   ⭐ der Name
  datenstand_hash  d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84
  Kursdateien      223   (Dateien gesamt: 225)
  ⚠️ Teilkerzen     36 Datei(en) mit Befund (223 Datei(en) geprueft)
      davon zugelassen   36 Befund(e) in 36 Datei(en) - docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3

  GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft.
RC=0
```

⭐ **Der Anker hielt, ohne `--kein-anker`:** die Kopie trägt denselben
`datenstand_hash` `d9449faf…` bei 223 Dateien wie die Tatsachennotiz vom
15.09.2026. Und das Nachprüfen des entstandenen Snapshots meldet
**`UNVERAENDERT`**, Rückgabewert **0**.

⚠️ **Zwei Hashes, zwei Fragen — und sie sind nicht verwechselbar.**
`63e4b6c8…` ist der `snapshot_hash` über die **225 Dateien des Laufs** (223
Kursdateien plus die zwei Symbollisten); `4fee547d…` aus Abschnitt 17 läuft nur
über die **223 Kursdateien**. Beide sind richtig; der Prüfer aus Teil 3 rechnet
ausdrücklich den zweiten nach, weil TB-48 ihn so gemessen hat.

### 1.4 Das Manifest führt auf, was erlaubt wurde — samt Herkunft

Aus dem `MANIFEST.json` des gezogenen Snapshots:

```json
"zugelassene_befunde_anzahl": 36,
"zugelassene_befunde_herkunft": {
  "beschlossen": "18.09.2026",
  "fundstelle": "docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3",
  "registertext": "5a, Zusatz - Ausnahme `rand_erste`",
  "umgesetzt_in": "shared/snapshot.py::_zulassung (TB-49)",
  "wortlaut": "Diese Befundart ist fuer das Ziehen eines Snapshots zugelassen, wenn alle drei Bedingungen erfuellt sind: (a) … (b) … (c) …"
},
"zugelassene_befunde": [
  {
    "art": "rand_erste",
    "datei": "AAVEUSDT_1d.csv",
    "erste_kerze": "2020-10-15",
    "urteil": "abgeleitete_teilkerze",
    "text": "Erste Kerze 2020-10-15: AAVEUSDT_1h.csv belegt 21 von 24 1h-Kerzen …"
  },
  …  /* 36 Einträge, 36 verschiedene Dateien */
]
```

| | |
|---|---|
| **Einträge** | **36** — je Datei **Name, Art und erste Kerze**, wie Bedingung (c) des Registereintrags es verlangt |
| **Dateien** | 36 verschiedene: **24** Tagesdateien (`_1d`) und **12** Vier-Stunden-Dateien (`_4h`), zu 24 Symbolen |
| **Arten** | ausschliesslich `rand_erste` |
| ⭐ **Herkunft der Erlaubnis** | ein eigenes Feld auf oberster Ebene — *ein Prüfer kann nachlesen, worauf die Zulassung sich stützt, ohne den Code zu kennen* |
| **daneben unverändert** | `teilkerzen` mit allen **36** Befunden und `frei_von_teilkerzen: false` — der Snapshot verschweigt nicht, dass die Prüfung angeschlagen hat |

### 1.5 Die Abbrüche, am vollen Bestand von 223 Dateien gemessen

Zweimal wurde die Wegwerf-Kopie gezielt beschädigt — **`data/` nicht**:

| Fall | Was gemacht wurde | Ergebnis |
|---|---|---|
| ⚠️ **ein `rand_letzte`** | `BTCUSDT_1h.csv` am **letzten** Tag auf 12 Stunden gekürzt, die letzte Tageskerze auf deren Aggregat gesetzt | **rc=2.** `… NICHT zulaesst: BTCUSDT_1d.csv (Art \`rand_letzte\` - zugelassen ist allein \`rand_erste\`) … (Zugelassen waren daneben 36 Befund(e).)` — **kein Snapshot entstanden** |
| ⚠️ **ein nicht-abgeleiteter `rand_erste`** | `close` der **ersten** Tageskerze von `BTCUSDT_1d.csv` um 1,0 verschoben | **rc=2.** `… NICHT zulaesst: BTCUSDT_1d.csv (Urteil \`unbelegt\` - zugelassen ist allein \`abgeleitete_teilkerze\`: die Kerze muss nachweislich das Aggregat genau der vorhandenen feineren Kerzen sein)` — **kein Snapshot entstanden** |

⭐ **Beide Male genügte eine einzige Datei** neben 36 zugelassenen Befunden.
Die Abbruchmeldung nennt die Datei **und den Grund**, nicht nur die Zahl.

⚠️ **Entschieden wird je BEFUND, nicht je Datei** — und das ist im ersten Fall
sichtbar: `BTCUSDT_1d.csv` trägt dort **beides**, einen zugelassenen
`rand_erste` an ihrer ersten Kerze **und** den `rand_letzte`. Der zugelassene
Befund steht weiter in der Zählung (*„Zugelassen waren daneben 36 Befund(e)"*),
**die Datei bricht trotzdem ab.** *Eine Zulassung je Datei hätte den
gefährlichen Rand mit durchgelassen, sobald derselbe Name auch einen erlaubten
Befund trägt.* Probe `3x` misst genau diesen Fall.

---

## Teil 2 — Die Wache ist mitgezogen

**`shared/test_snapshot.py` ist erweitert, nicht ersetzt: 110 → 164
Prüfungen.** Die 110 bestehenden laufen unverändert. Neu ist **Abschnitt 3c**
mit acht Proben.

⚠️ **Jede Probe, die einen Abbruch erwartet, führt ihre Mutation mit** —
dieselbe Bauform wie bisher: die Fassung mit **entfernter Bedingung** muss die
Abweichung **übersehen**. Findet sie sie auch, prüft die Probe eine andere
Stelle als angenommen, und das wäre ein Befund über den Test, nicht über das
Werkzeug. **Sechs der acht Proben sind so gebaut.** Die beiden übrigen können
es nicht sein und sollen es nicht: `3ac` ist die **Negativprobe** (sie erwartet
gerade keinen Abbruch), `3ad` misst die **Abwesenheit** einer Flagge — eine
Wache, die man entfernen könnte, gibt es dort nicht.

| Probe | Fall | Erwartet | Die Mutation, die beisst |
|---|---|---|---|
| **3w** | 36 Befunde, alle `rand_erste`, alle Bedingungen erfüllt | ⭐ **zieht**, Manifest führt alle **36** auf, mit Registerverweis | `_zulassung` gibt immer `False` zurück — der Stand **vor** TB-49 → es wird nicht gezogen |
| **3x** | ⚠️ ein **`rand_letzte`** kommt dazu | **Abbruch**, Datei genannt; die vier `rand_erste` daneben bleiben zugelassen | Bedingung **(a)** entfernt → der Snapshot entsteht trotz `rand_letzte` |
| **3y** | ein `rand_erste`, der **nicht** das Aggregat ist | **Abbruch**, Datei genannt, Grund nennt `unbelegt` | Bedingung **(c)** entfernt → der Snapshot entsteht trotz widersprechender Kerze |
| **3z** | ein `rand_erste` an einer **anderen als der ersten** Kerze | **Abbruch**, Grund nennt **beide** Kerzen | Bedingung **(b)** entfernt → der Snapshot entsteht |
| **3aa** | eine Datei **ohne feineren Zeugen** mit `rand_erste` | **Abbruch** — „nicht belegbar" | die fehlende Deckung wird als „war schon in Ordnung" eingesetzt → der Snapshot entsteht auf einem unbelegten Befund |
| **3ab** | Bedingung (c) ist **nicht ausführbar** | **Rückgabewert 2**, nie 0 | das Urteil wird **abgeschrieben** statt geholt → der Snapshot entsteht doch |
| **3ac** | ⭐ **Negativprobe**: ein Bestand **ohne jeden Befund** | zieht weiterhin unverändert, **0** zugelassene Befunde, Herkunftsfeld trotzdem da | — (eine Probe, die nur rot sein kann, beweist nichts) |
| **3ad** | ⚠️ **keine Übergehen-Flagge** | drei erfundene Flaggen ergeben **2**; der Quelltext kennt keine | — |

⚠️ **Zwei Fälle lassen sich aus Kursdateien nicht herstellen** — ein
`rand_erste` an einer späteren Kerze (3z) und einer ohne Deckungsprüfung (3aa).
Die heutige `zeitabdeckung.py` vergibt beides nicht. Sie werden deshalb
**gestellt**: `snapshot.py` darf sich nicht darauf verlassen, dass seine
Eingabe wohlgeformt ist. Dass die Proben dennoch beissen, zeigen ihre
Mutationen.

**Der Bestandsbauer der Proben** (`_teilkerzen_quelle`) erzeugt je Symbol eine
`_1h.csv` als Zeugen und eine `_1d.csv`, deren Tageskerzen genau die Aggregate
der jeweiligen Stunden sind. Der erste Tag ist angeschnitten — daraus entsteht
ein echter `rand_erste` mit Urteil `abgeleitete_teilkerze`, kein gestellter.
Die Werte sind so gewählt, dass Summen und Extremwerte **exakt** in Gleitkomma
aufgehen; *eine Probe, die an einem Rundungsrest scheitert, sagt nichts über
ihre Wache aus.*

### ⚠️ Der fünfte Fall — `kein_zeuge`. Die Entscheidung und ihre Begründung

**Entschieden: nicht belegbar ist nicht zugelassen.** Ein behaupteter
`rand_erste` ohne Deckungsprüfung bricht ab, mit der Begründung *„für diese
Datei liegt keine Deckungsprüfung der ersten Kerze vor (kein feinerer Zeuge) —
Bedingung (b)/(c) ist hier nicht belegbar, und nicht belegbar ist nicht
zugelassen"*.

**Warum so:**

1. ⭐ **Bedingung (c) ist ein Nachweis, keine Vermutung.** Der Registertext
   sagt: *„Die Kerze ist nachweislich das Aggregat genau der vorhandenen
   feineren Kerzen … Die Prüfung stellt das je Datei fest."* Ohne Zeugen stellt
   sie gar nichts fest. Eine Zulassung wäre dann keine Anwendung der Regel,
   sondern eine Ausnahme von ihr.
2. ⚠️ **Es ist genau die Fehlerfamilie aus TB-45.** Dort haben zwei Wachen
   „bestanden" gemeldet, ohne etwas gemessen zu haben — ein gescheiterter
   Nachweis und ein geführter Nachweis sahen gleich aus. Dieses Projekt trennt
   beides seither mit einem eigenen Rückgabewert. *Wer nicht messen konnte,
   sagt es.*

⭐ **Und die Antwort auf die eigentliche Frage des Auftrags: an `data/` ist das
folgenlos, und das ist gemessen.**

| | |
|---|---|
| Dateien mit `kein_zeuge` | **175** von 223 — **150** Aktien-Tagesdateien und **25** Krypto-Stundendateien |
| davon mit **irgendeinem** Befund | ⭐ **null** |

**Der Grund liegt im Aufbau von `pruefe_datei`:** fehlt der feinere Zeuge,
kehrt die Funktion **vor** der Deckungsprüfung um und hinterlässt einen
**Hinweis**, keinen Befund. Die Art `rand_erste` entsteht **ausschliesslich**
aus dieser Deckungsprüfung. **Wo `kein_zeuge` steht, kann es also gar keinen
`rand_erste` geben** — die Regel greift dort nie.

⚠️ **Streng wird sie erst in dem Fall, für den sie gedacht ist:** wenn eine
Eingabe von aussen einen Befund ohne Deckung behauptet, oder wenn einer Datei,
die heute einen Zeugen hat, der Zeuge künftig abhandenkommt. Dann soll nicht
gezogen werden — und genau das prüft Probe `3aa`.

> ⭐ Die **25** Krypto-Stundendateien sind übrigens per Aufbau ohne Zeugen:
> `1h` ist der feinste geführte Zeitrahmen, unter ihm gibt es nichts. Die
> **150** Aktien-Tagesdateien haben keine Intraday-Dateien im Bestand. *Beides
> ist kein Mangel, sondern der Zuschnitt des Bestandes.*

---

## Teil 3 — Der Prüfer für Abschnitt 17 liegt im Repo

**`research/registernachtrag_tb48/`** — `pruefe_abschnitt17.py`,
`test_abschnitt17.py`, `BERICHT.md`.

### ⚠️ Ein Befund zur Herkunft, der in die Beurteilung gehört

**Der Auftrag sagt: *„`pruefe_abschnitt17.py` aus dem TB-48-Paket kommt nach
`research/registernachtrag_tb48/`."*** ⚠️ **In den Unterlagen dieser Sitzung lag
die Datei nicht bei** — die ZIP-Datei enthielt **allein den Auftragstext**
(`CLOUD_TB-49_ausnahme_ins_werkzeug.md`, eine Datei). Auch im Repo war sie
nirgends; TB-48 hat sie ausdrücklich unversioniert in seiner eigenen ZIP-Datei
abgelegt.

**Behandlung:** Das Werkzeug ist aus der Belegtabelle in
`docs/ERGEBNIS_TB-48_registernachtrag.md`, Abschnitt 4, **neu geschrieben** —
dieselben neunzehn Zahlen, dieselben Quellen, dieselbe Erwartung.

⚠️ **Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes**, und das
steht so auch im Kopf der Datei und im `BERICHT.md`. Die Auflage „unverändert
in der Sache, nicht in seinen Prüfungen beschnitten" ist am **Ergebnis**
geprüft, nicht am Quelltext: alle neunzehn Zahlen sind geprüft, genau eine
Abweichung wird gemeldet, der Rückgabewert ist **1**. Wer die TB-48-ZIP-Datei
noch hat, kann beide Fassungen nebeneinanderlegen; für das Ergebnis ist das
nicht nötig.

### Der Lauf

```
  geprueft:  19 von 19

  [OK ]  1 nicht_kurs_eingaben              Soll genau zwei                   Ist 2: sp500_top150.txt, top25_symbols.txt
  [OK ]  2 datenstand_hash                  Soll d9449faf51bffaaa…            Ist d9449faf51bffaaa…
  [OK ]  3 kursdateien                      Soll 223                          Ist 223
  [OK ]  4 snapshot_hash                    Soll 4fee547dccd4c5e4…            Ist 4fee547dccd4c5e4… (223 Dateien)
  [OK ]  5 teilkerzen_befunde               Soll 36 von 223                   Ist 36 von 223
  [OK ]  6 arten_der_befunde                Soll {'rand_erste': 36}           Ist {'rand_erste': 36}
  [OK ]  7 letzte_kerze_frei                Soll keine Datei                  Ist 0: []
  [OK ]  8 erste_kerze_2017_2020            Soll 20                           Ist 20
  [OK ]  9 erste_kerze_ab_2023              Soll 16                           Ist 16
  [OK ] 10 luecke_2021_2022                 Soll 0, und 20 + 16 = 36          Ist 0 in 2021/2022, Summe 36
  [OK ] 11 elf_symbole                      Soll 11, Differenz beidseitig leer Ist gemessen 11, T34.9 11, nur gemessen [], nur T34.9 []
  [OK ] 12 kein_zeuge                       Soll 175 von 223                  Ist 175 von 223
  [OK ] 13 kein_zeuge_aktien                Soll 150                          Ist 150
  [OK ] 14 kein_zeuge_krypto_1h             Soll 25                           Ist 25
  [!! ] 15 frueheste_selektionsfalte        Soll 2022 (Wortlaut in 17.3)      Ist 2019 (faltenplan.json; erstes Faltenjahr je Bot: [2019])
  [OK ] 16 kurze_kerze_in_geladener_falte   Soll 0                            Ist 0
  [OK ] 17 schwelle_18_von_19               Soll unter 95 %                   Ist 94.7 %
  [OK ] 18 schwelle_19_von_20               Soll nicht unter 95 %             Ist 95.0 %
  [OK ] 19 mindestzahl_n                    Soll 20                           Ist 20

  1 ABWEICHUNG(EN):
    [15 frueheste_selektionsfalte] Soll 2022 (Wortlaut in 17.3) / Ist 2019 …
```

**Rückgabewert 1** — ⭐ **genau eine Abweichung, und es ist die erwartete.**
Alle 18 übrigen Zahlen treffen die TB-48-Messung.

**Drei Eigenschaften, die der Auftrag „aufgeräumt, aber nicht beschnitten"
meint:**

| | |
|---|---|
| ⭐ **Die Jahreszahl 2022 wird aus dem Registertext gelesen**, nicht im Werkzeug hinterlegt | Sonst prüfte es seine eigene Abschrift und meldete nach einer Berichtigung des Wortlauts weiter die alte Abweichung |
| ⚠️ **Verschwindet der Satz aus dem Register, ist das `nicht pruefbar`** — Rückgabewert **2** | Nicht „in Ordnung". Dieselbe Trennung wie in `snapshot.py` |
| **Zwei Zahlen aus Abschnitt 17 fasst er gar nicht erst an** | `pandas_market_calendars` 4.6.1 (17.5, ausdrücklich „auf dem Betriebsrechner") und die Drift-Messung aus 17.8 (braucht einen echten yfinance-Abruf). Erstere steht im Mac-Testauftrag, letztere ist selbst nicht reproduzierbar — **das ist der Inhalt des Befunds, nicht seine Umgehung** |

### Der Selbsttest

`research/registernachtrag_tb48/test_abschnitt17.py` — **24 von 24**,
Rückgabewert 0, Laufzeit rund zwei Minuten.

⭐ **Er zeigt, dass der Prüfer beisst**, an gestellten Quellen: ein Faltenplan
mit 2022 macht Prüfung 15 grün, einer mit 2017 rot; ein Register ohne den Satz
ergibt `nicht pruefbar`; ein vertauschtes Symbol im Backlog wird trotz gleicher
Anzahl gefunden; ein gestelltes `rand_letzte` und eine kurze Kerze in einer
geladenen Falte werden gefunden. **Und am Ende der echte Bestand: 19
Prüfungen, eine Abweichung, Rückgabewert 1.**

⭐ **Der TB-41-Prüfer ist nicht angefasst worden.** Er kennt Abschnitt 17
weiterhin nicht; ob er erweitert wird, bleibt die eigene Entscheidung, als die
TB-48 sie gemeldet hat. **Diese Arbeit legt ein zweites Werkzeug daneben, sie
baut das erste nicht um.**

---

## Teil 4 — Die eine offene Zahl, geklärt

**Zu prüfen war die Vermutung:** *2022 ist die früheste **Krypto**-Falte (so in
T34.9), 2019 die über **alle neun** Bots.*

### ⚠️ Die Vermutung trägt nicht

`research/registernachtrag_tb48/pruefe_abschnitt17.py --falten-je-bot`, gelesen
aus `research/faltenplan_neun/daten/faltenplan.json`:

| Bot | Markt | 1. Faltenjahr | ohne Registerschranke | Falten | erstes Fenster |
|---|---|---:|---:|---:|---|
| `elliott_wave` | krypto | **2019** | 2018 | 3 | 2019-01-01 … 2021-01-01 |
| `elliott_wave_stocks` | aktien | **2019** | 2017 | 7 | 2019-01-01 … 2020-01-01 |
| `rsi2_crypto` | krypto | **2019** | 2019 | 7 | 2019-01-01 … 2020-01-01 |
| `rsi2_mean_reversion` | aktien | **2019** | 2018 | 7 | 2019-01-01 … 2020-01-01 |
| `t3_supertrend` | krypto | **2019** | 2018 | 7 | 2019-01-01 … 2020-01-01 |
| `turtle_soup_crypto` | krypto | **2019** | 2018 | 7 | 2019-01-01 … 2020-01-01 |
| `turtle_soup_stocks` | aktien | **2019** | 2017 | 7 | 2019-01-01 … 2020-01-01 |
| `volatility_breakout` | aktien | **2019** | 2018 | 7 | 2019-01-01 … 2020-01-01 |
| `volatility_breakout_crypto` | krypto | **2019** | 2018 | 7 | 2019-01-01 … 2020-01-01 |

```
  erstes Faltenjahr ueber alle neun Bots:        [2019]
  erstes Faltenjahr ueber die fuenf Krypto-Bots: [2019]
```

⚠️ **Krypto und Gesamtheit liefern dieselbe Zahl.** Eine Trennung „Krypto 2022
/ alle neun 2019" gibt dieser Faltenplan nicht her. **Es sind nicht zwei
Fragen, sondern eine Frage und zwei Antworten aus zwei Faltenplan-Generationen.**

### ⭐ Woher die 2022 wirklich stammt

| | |
|---|---|
| **2019** | `research/faltenplan_neun/daten/faltenplan.json` — **alle neun** Bots, nach der Registerschranke `ERSTE_MOEGLICHE_FALTE = 2019`. Symbole ohne Historie tragen 0 bei und werden **nicht** ausgeschlossen |
| ⚠️ **2022** | `research/krypto_historie/daten/faltenplan_nach_tb34.json` — ⚠️ **`mindesttraining: 4`, und nur die fünf Krypto-Bots.** Dort steht `erstes_faltenjahr: 2022` bei allen fünf, Symbolzahlen je Falte `[3, 6, 9, 13]` |

⭐ **Die Symbolreihe „3 (2022) → 6 → 9 → 13 (2025)" aus T34.9 stimmt Zeichen
für Zeichen mit diesem überholten Plan überein.** Die 2022 ist also weder ein
Tippfehler noch eine Krypto-Eigenheit, sondern **die Zahl eines anderen
Faltenplans** — desjenigen mit vier Jahren Mindesttraining.

⚠️ **Und dass das offen ist, steht schon im Backlog:** **T34.10** führt
*„Mindesttraining: 4 Jahre oder 2?"* ausdrücklich als **Betreiberentscheidung
vor TB-30b** und rechnet beide Fälle vor — *„Mit 4 Jahren beginnt die erste
Falte 2022 → 4 Selektionsfalten, bei `elliott_wave` nur 2."* **Das ist genau
die 2022.**

### ⚠️⚠️ Welche der beiden Zahlen ist die falsche — und wo steht sie?

**Die 2022, und sie steht an drei Stellen:**

| Stelle | |
|---|---|
| `docs/VORREGISTRIERUNG_neuselektion.md`, **17.3** | im wörtlich übernommenen, **beschlossenen** Registereintrag: *„Die erste Selektionsfalte beginnt 2022 — reiner Vorlauf"* |
| `docs/projektfuehrung/BACKLOG.md`, **T34.9** | *„Symbole je Falte: 3 (2022) → 6 → 9 → 13 (2025)"* — ⭐ **dort ist sie richtig**, denn sie bezieht sich auf den Plan, aus dem sie stammt |
| *(mittelbar)* der beigefügte `REGISTEREINTRAG_rand_erste.md` | die Quelle des Wortlauts in 17.3 |

⭐ **Der entscheidende Beleg steht im Register selbst.** Abschnitt **15.6,
Registertext 4 — Falten**, führt als **Tatsachennotiz zu 4d** eine Faltenliste
je Bot:

```
| `elliott_wave`               | krypto | 2 J | 2019–2020, 2021–2022, 2023–2024 | 3 | …
| `t3_supertrend`              | krypto | 1 J | 2019, 2020, 2021, 2022, …       | 7 | …
| `rsi2_crypto`                | krypto | 1 J | 2019, 2020, 2021, 2022, …       | 7 | …
| `turtle_soup_crypto`         | krypto | 1 J | 2019, 2020, 2021, 2022, …       | 7 | …
| `volatility_breakout_crypto` | krypto | 1 J | 2019, 2020, 2021, 2022, …       | 7 | …
```

⚠️ **Das Register nennt für die Krypto-Bots selbst 2019.** Die 2022 in 17.3
widerspricht damit nicht nur einer Datei unter `research/`, sondern **dem
eigenen Registertext an einer zweiten Stelle**. *Damit ist die Frage „welche
der beiden ist falsch" nicht mehr Auslegung, sondern abgelesen.*

### Was daraus folgt — und was nicht

| | |
|---|---|
| ❌ **Kein Registertext ist geändert worden** | Der Auftrag sagt: berichten. Die Befundnotiz zu 17.3 steht seit TB-48 im Register und trägt die Sache bereits; sie wird durch diesen Bericht **genauer**, nicht ersetzt |
| ⭐ **Die Schlussfolgerung trägt weiterhin** | Prüfung 16 rechnet sie maschinell nach: über alle neun Bots und alle Falten gibt es **null** Fälle, in denen eine der 36 kurzen ersten Kerzen in ein Faltenfenster fällt, in dem ihr Symbol geladen ist |
| ⚠️ **Offen bleibt T34.10** | Solange die Mindesttrainings-Frage nicht entschieden ist, gibt es **zwei** Faltenpläne im Repo, die verschiedene erste Falten liefern. ⭐ **Das ist der eigentliche Gehalt dieses Befunds** — nicht eine Jahreszahl, sondern zwei nebeneinander liegende Pläne, von denen nur einer im Register steht |

---

## Teil 5 — Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ❌ | **Kein Snapshot gezogen.** Weder `snapshots/` noch `data/snapshots/` existiert. Gezogen wurde ausschliesslich in Wegwerf-Verzeichnisse, aus einer **Kopie** von `data/` |
| ❌ | **`data/` nicht angefasst** — Datenstand vorher und nachher gemessen, siehe Abschnitt 0 |
| ❌ | **`strategies/*/live_params.py`, `forward_test.py`, `equity_simulation.py`, `shared/entscheidungskerze.py`, `shared/paths.py`: unberührt.** Keine dieser Dateien ist geändert worden; `git diff --numstat` über den Zweig nennt sie nicht |
| ❌ | **Kein Registertext geändert** — `docs/VORREGISTRIERUNG_neuselektion.md` ist nicht angefasst |
| ❌ | **Keine Übergehen-Flagge** in `snapshot.py` — Probe `3ad` misst das |
| ❌ | **Kein `--echt`, keine Order, kein Broker-Endpunkt, kein Netzabruf** |
| ❌ | **Kein Secret gelesen.** `config/email_config.py` ist weder mit `cat` noch mit `git show` geöffnet worden |
| ❌ | **Kein Datencron, keine Gleichheitsprüfung** |
| ❌ | **Keine Zahl abgeschrieben** — jede in diesem Bericht steht, weil sie in dieser Sitzung an ihrer Quelle gerechnet wurde |
| ❌ | **Der TB-41-Registerprüfer nicht erweitert** — er kennt Abschnitt 17 weiterhin nicht |

---

## Umgebung — was diese Cloud-Sitzung vorgefunden hat

⭐ **Abweichungen von `docs/UMGEBUNGEN.md` sind zu melden. Hier sind sie.**

| | Mac (laut `UMGEBUNGEN.md`) | **diese Cloud-Sitzung** | |
|---|---|---|---|
| Python | 3.9.6 | **3.11.15** | wie erwartet |
| `pandas` / `numpy` | 2.3.3 / 2.0.2 | ⚠️ **3.0.6 / 2.4.6** | **eine Hauptversion über dem Mac** |
| `pandas_market_calendars` | **4.6.1** | ⚠️ **5.4.0** | ⚠️ betrifft Registertext 5f (17.5) unmittelbar |
| `scipy` | fehlt | **1.17.1** vorhanden | bekannt wechselnd |
| `dateparser` | 1.2.2 | 1.4.3 | wie dokumentiert |
| `node` | vorhanden | **v22.22.2** vorhanden | — |
| `yfinance` / `binance` | erreichbar | ⚠️ **Netzsperre** | wie dokumentiert |

⚠️ **Alle Fremdpakete fehlten beim Sitzungsstart** und mussten nachinstalliert
werden — `pandas`, `numpy`, `scipy`, `fastapi`, `uvicorn`, `httpx`, `yfinance`,
`python-binance`, `dateparser`, `pandas_market_calendars`. **Derselbe Fall wie
in TB-48**, und genau der in `docs/UMGEBUNGEN.md` beschriebene: *„die Cloud ist
nicht EINE Umgebung, sondern eine je Sitzung."*

⭐ **Für die Arbeit dieser Sitzung war das folgenlos:** `shared/snapshot.py`,
`shared/zeitabdeckung.py`, `research/vorregistrierung/herkunft.py` und der neue
`pruefe_abschnitt17.py` kommen mit **reiner Standardbibliothek** aus. Keine der
gemessenen Zahlen hängt an einem Fremdpaket — ⚠️ **mit der einen bekannten
Ausnahme**, der Fassung des Handelskalenders, und genau die steht deshalb im
Mac-Testauftrag.

⚠️ **Strukturell nicht prüfbar in der Cloud, unverändert seit TB-47/TB-48:**
das Verhalten auf **Python 3.9.6**, die Fassung von `pandas_market_calendars`
auf dem Betriebsrechner, die neun Live-Datenbanken und der laufende Cron.
**Deshalb wird der Mac-Testauftrag vor dem Merge angefordert, nicht danach.**

---

## Basislauf

**65 Testdateien, Zeitgrenze 900 s je Datei** (`trading-env/` ausgeschlossen).
⚠️ **65, nicht 64** — hinzu kommt `research/registernachtrag_tb48/test_abschnitt17.py`.

| | | |
|---|---:|---|
| **grün** | **58** | ⭐ **einer mehr als in TB-48** — und es ist genau der neue: `research/registernachtrag_tb48/test_abschnitt17.py` (123,4 s) |
| **rot** | **3** | **alle drei erklärt** — siehe unten |
| **ungeprüft** | **3** | ⚠️ **nicht rot** — sie verlangen ein Bot-Argument |
| **Zeitgrenze** | **1** | `shared/test_drawdown_beide_masse.py` (bekannt) |

58 + 3 + 3 + 1 = **65**.

### Die drei roten — keiner gehört diesem Zweig

| Datei | rc | Ursache |
|---|---:|---|
| `shared/test_stabile_sortierung.py` | 1 | **bekannt rot** (Mac 17.09.: 3 Fehler), unverändert |
| `shared/test_wellenauswahl.py` | 1 | **bekannt rot** (Mac 17.09.: 1 Fehler), unverändert |
| `shared/test_zuteilung.py` | 1 | ⚠️ **Netzsperre** — `ProxyError … api.binance.com`. Auf dem Mac ist die Datei grün |

### Die drei ungeprüften

`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/elliott_wave_params/test_params.py` ·
`research/fib_score_stufen/test_stufen.py` — ⚠️ **ungeprüft, nicht rot.**
Ohne Bot-Argument nur die Nutzungszeile und `rc=1`.

### ⭐ Die beiden Dateien, um die es in dieser Aufgabe geht

| Datei | | |
|---|---|---|
| `shared/test_snapshot.py` | **grün**, 4,6 s | **164 von 164** Prüfungen — 110 bestehende plus 54 neue |
| `research/registernachtrag_tb48/test_abschnitt17.py` | **grün**, 123,4 s | **24 von 24** Prüfungen. ⭐ Die Laufzeit ist Absicht: er rechnet am Ende den **echten** Bestand durch |

### ⭐ Der Nebenbeweis aus TB-47 hält

`shared/test_drawdown_beide_masse.py` lief wie erwartet in die Zeitgrenze
(`rc=-15`, *„erwartet: terminiert nicht (bekannt)"*). Nach dem Lauf gemessen:

```
$ ps -eo pid,etime,args | grep -i "drawdown_beide" | grep -v grep
KEINE ueberlebenden Prozesse
```

**Überlebende Prozesse: 0.** Die Prozessgruppen-Reparatur aus TB-47 trägt auch
in dieser Sitzung.

### ⭐ Vier „UNERWARTET" — alle vier erklärt, keiner ein Befund

| Datei | gemeldet | tatsächlich |
|---|---|---|
| `dashboard/test_portfolio_sicht.py` | bekannt rot (Mac) | **grün, 91/91** |
| `research/exposure_messung/test_exposure_kern.py` | bekannt rot (Mac) | **grün** |
| `research/hrp_portfolio/test_hrp_core.py` | bekannt rot (`scipy` fehlt, Mac) | **grün** — `scipy` ist hier vorhanden |
| `shared/test_zuteilung.py` | auf dem Mac grün | **rot** — Netzsperre |

⚠️ **Alle vier sind Rechnerunterschiede, keine Befunde** — dieselben vier wie
in TB-48. Die `BEKANNT_ROT`-Liste des Runners führt **Mac-Werte**; die
Markierung ist richtig, die Fälle sind erklärt.

⭐ **`system/test_log_rotation.py` war grün** (4,5 s), wie in der
Aufgabenstellung angekündigt.

**⭐ Keine Abweichung von der Erwartungsliste der Aufgabenstellung.** Die dort
genannten bekannt roten, die drei ungeprüften und der Grün-Vermerk zu
`system/test_log_rotation.py` sind alle eingetroffen. ⚠️ **Der einzige
Unterschied zum TB-48-Basislauf ist der eine zusätzliche grüne Test** — und der
gehört diesem Zweig.

---

## Arbeitsbaum

**Vor dem letzten Commit gemessen — und danach erneut**, weil TB-46 und TB-48
die Ausgabe im Beleg *vor* dem letzten Commit stehen hatten.

**Stand nach den Commits von Teil 1–3, vor dem Commit der beiden Dokumente:**

```
$ git status --porcelain
 M shared/test_snapshot.py
?? docs/ERGEBNIS_TB-49_ausnahme.md
?? docs/TESTAUFTRAG_TB-49_ausnahme.md
```

*(Die Änderung an `shared/test_snapshot.py` ist die Beschriftung einer
Prüfung in Probe `3x` — sie geht mit dem letzten Commit mit.)*

**Stand nach dem letzten Commit:**

```
GITSTATUS_NACHHER
```

```
$ git diff --numstat db8913a
GITDIFF_NACHHER
```

⭐ **Keine der Sperrlisten-Dateien steht im Diff** — weder
`strategies/*/live_params.py` noch `forward_test.py`, `equity_simulation.py`,
`shared/entscheidungskerze.py`, `shared/paths.py`, `data/` oder
`docs/VORREGISTRIERUNG_neuselektion.md`. Maschinell geprüft:

```
$ git diff --name-only db8913a | grep -E "live_params|forward_test|equity_simulation|entscheidungskerze|paths\.py|^data/|VORREGISTRIERUNG"
KEINE - wie verlangt
```

---

## Was als Nächstes ansteht

| | |
|---|---|
| ⚠️ **Zuerst** | Der **Mac-Testauftrag** (`docs/TESTAUFTRAG_TB-49_ausnahme.md`) — ⚠️ **vor dem Merge**, nicht danach. Er trägt diesmal wirklich etwas: die Ausnahme im Verhalten auf 3.9.6, die neunzehn Zahlen auf dem Betriebsrechner, `pandas_market_calendars` |
| ⭐ **Danach ist der Snapshot nicht mehr blockiert** | Zeile 2 der Tabelle 17.10 (*„der Snapshot lässt sich heute nicht ziehen"*) ist mit diesem Zweig erledigt. **Ob und wann er gezogen wird, ist eine eigene Entscheidung mit eigener Freigabe** — diese Aufgabe hat ihn ausdrücklich nicht gezogen |
| **Offen, Betreiber** | ⚠️ **T34.10 — Mindesttraining 4 Jahre oder 2.** Solange das offen ist, liegen zwei Faltenpläne mit verschiedenen ersten Falten im Repo. Teil 4 |
| **Offen, Betreiber** | Ob der **TB-41-Prüfer** um Abschnitt 17 erweitert wird, oder ob die beiden Werkzeuge nebeneinander bleiben |
| **Offen, Betreiber** | Die sechs übrigen Zeilen aus 17.10 — Lese-Audit, `requirements.lock`, Kein-Entscheid-Tag, Vergleichswerkzeug, Drift-Protokoll |
| ⭐ **Nebenbefund, unverändert seit TB-47** | Die Datenstand-Berechnung steht **zweimal zeichengleich** im Repo (`research/vorregistrierung/herkunft.py` und `research/registernachtrag_tb41/pruefe_register.py:319`). Heute liefern beide dasselbe. *Wer eines von beiden ändert, merkt den Unterschied nicht.* Nicht behoben — ausserhalb dieses Auftrags |

---

## In einfacher Sprache

**Worum ging es?** Bevor die grosse Auswertung läuft, soll eine eingefrorene
Kopie aller Kursdaten gezogen werden — ein „Snapshot". So lässt sich später
nachsehen, womit gerechnet wurde. **Das ging bis gestern nicht.**

**Warum ging es nicht?** Das Programm, das die Kopie zieht, prüft vorher, ob
die Kursdaten vollständig sind. Bei **36 von 223** Dateien meldet es dabei
etwas: die **allererste** Kerze ist kürzer als die anderen. Das ist kein
Fehler, sondern hat einen banalen Grund — an diesem Tag wurde das Symbol erst
mittags zum ersten Mal gehandelt. Trotzdem hat das Programm jedes Mal
abgebrochen.

**In den Regeln des Projekts steht seit gestern ausdrücklich, dass diese 36
Fälle in Ordnung sind.** Das Programm wusste davon noch nichts. **Diese Aufgabe
hat es ihm beigebracht.**

**Und zwar als Regel, nicht als Liste.** Man hätte die 36 Dateien einfach
aufschreiben können. Das wäre die schlechtere Lösung gewesen: sobald ein neues
Symbol dazukommt, bringt es denselben Fall mit, und eine Liste, die niemand
pflegt, blockiert dann entweder grundlos — oder, schlimmer, lässt eines Tages
etwas durch, das sie nicht durchlassen sollte. **Die Regel sagt: erlaubt ist
das nur, wenn es die allererste Kerze betrifft und wenn nachweisbar ist, dass
sie genau die Summe der vorhandenen feineren Kerzen ist.** Drei Bedingungen,
alle drei müssen zutreffen.

**Wird jetzt weniger geprüft?** Nein — und das war die wichtigste Auflage. Die
Prüfung läuft unverändert und meldet weiterhin alle 36 Fälle. Nur bricht sie
nicht mehr deswegen ab. **Und eine Abkürzung, mit der man die Prüfung einfach
übergehen könnte, gibt es ausdrücklich nicht.** Es wurde eigens nachgemessen,
dass es sie nicht gibt.

**Woher weiss man, dass die Regel wirklich scharf ist?** Weil sie an einer
gezielt beschädigten Kopie der echten Kursdaten ausprobiert wurde. Wird eine
**letzte** Kerze angeschnitten — der gefährliche Fall, wo ein Abruf
mittendrin geschrieben haben könnte —, bricht das Programm ab und nennt die
Datei. Stimmt eine erste Kerze nicht mit ihren Stundenkerzen überein, bricht es
ebenfalls ab. **Die Originaldaten wurden dafür nicht angefasst**, nur eine
Kopie, die danach weggeworfen wurde.

**Der Snapshot wurde trotzdem nicht gezogen.** Das war nicht die Aufgabe.
Geprüft wurde nur, dass es ginge — an einer Wegwerf-Kopie. Die Entscheidung,
ihn wirklich zu ziehen, gehört ausdrücklich freigegeben.

**Was war noch zu tun?** Zwei Dinge.

Erstens: Ein kleines Prüfprogramm, das **19 Zahlen** in den Projektregeln
nachrechnet, war in der letzten Aufgabe entstanden, aber nie im Projekt
abgelegt worden. Es liegt jetzt dort. ⚠️ **Es lag den Unterlagen dieser Sitzung
allerdings nicht bei** — es musste aus der Ergebnistabelle der letzten Aufgabe
neu geschrieben werden. Das steht so auch in der Datei selbst, damit niemand es
später für das Original hält. Es liefert dieselben Ergebnisse: 18 Zahlen
stimmen, **eine nicht**.

Zweitens: **genau diese eine Zahl zu klären.** In den Regeln steht „die erste
Auswertungsperiode beginnt 2022". Die Planungsdatei sagt **2019**. Die Vermutung
war, dass beide recht haben — 2022 für die Kryptowährungen, 2019 für alle neun
Programme zusammen.

⚠️ **Die Vermutung stimmt nicht.** Es wurde für jedes der neun Programme
einzeln nachgesehen: **alle neun** beginnen 2019, die fünf Krypto-Programme
eingeschlossen. Die 2022 stammt aus einer **älteren, überholten Planung**, die
noch mit einer anderen Vorgabe rechnete (vier Jahre Mindestvorlauf statt der
heutigen Regel). Beide Planungen liegen noch im Projekt nebeneinander, und
**welche gelten soll, ist eine offene Entscheidung des Betreibers** — sie steht
als solche schon im Projektplan.

⭐ **Der schlagende Beweis stand im Regeldokument selbst:** an anderer Stelle
führt es eine Tabelle mit allen neun Programmen und ihren Auswertungsjahren —
und nennt dort für die Krypto-Programme **ebenfalls 2019**. Die 2022
widerspricht also dem eigenen Dokument.

**Der falsche Satz wurde nicht heimlich ausgebessert.** Das war ausdrücklich so
verlangt. Er steht weiter da; was nachgerechnet wurde, steht daneben — und
jetzt auch, woher die falsche Zahl kommt.

**Ist etwas kaputtgegangen?** Nein. Die Kursdaten sind vorher und nachher
nachweislich unverändert (dieselbe Prüfsumme, dieselben 223 Dateien). Die Wache
über das geänderte Programm ist von **110 auf 164 Prüfungen** gewachsen, und
jede neue weist eigens nach, dass sie wirklich anschlägt — indem die Prüfung
versuchsweise entfernt und gezeigt wird, dass der Fehler dann durchrutscht.

**Was fehlt noch?** Der Nachweis auf dem MacBook. Dort läuft eine ältere
Python-Fassung, und „grün in der Cloud" heisst dort erfahrungsgemäss nicht
automatisch „grün" — dreimal an einem Tag hat der Mac etwas gefunden, das die
Cloud gar nicht sehen konnte. **Diesmal trägt dieser Lauf wirklich etwas:** er
misst das neue Verhalten auf der alten Python-Fassung, lässt das Prüfprogramm
zum ersten Mal auf dem Betriebsrechner laufen und klärt eine Paketfassung, die
in den Regeln steht. **Er wird vor dem Zusammenführen abgearbeitet, nicht
danach.**
