# Journal-Nachtrag 18.09.2026 (b) — TB-49

> ⚠️ EINGEARBEITET am 18.09.2026 in `docs/projektfuehrung/JOURNAL.md` (als Block BF — um zwei Stellen verschoben, wie die fünf aus Nachtrag (a)), Commit 02de1f7.
> Dieses Dokument bleibt als Beleg des Nachtrags stehen und wird nicht
> mehr fortgeschrieben.

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`, NACH den Blöcken aus
Nachtrag (a).** Nichts wird umgeschrieben.

> ⚠️ **Zum Blockbuchstaben:** Nachtrag (a) bringt die Blöcke **AY–BC** (oder, je
> nach gemessenem Stand, fünf verschobene). **Dieser Block ist der
> nächstfolgende** — nach AY–BC also **BD**. ⚠️ **Vor dem Einfügen prüfen,
> welcher Buchstabe wirklich der letzte ist.**

---

## Block BD — TB-49: das Werkzeug lernt die Ausnahme

**18.09.2026. Cloud-Zweig `claude/new-session-kfbw56`, Mac-Lauf und Merge offen.**

**Die Lage vorher, in einem Satz:** *Das Register erlaubt die Ausnahme. Das
Werkzeug weiss nichts davon.*

### Der Nachweis in zwei Zahlen

| | |
|---|---|
| **am Stand von TB-48**, gegen dasselbe `data/` | `ABBRUCH: … 36 Datei(en) mit Befund …` · **`RC_ALT=2`** |
| **mit diesem Zweig**, derselbe Bestand | `36 Datei(en) mit Befund … davon zugelassen 36 … Abschnitt 17.3` · **`RC_TROCKENLAUF=0`** |

> ⭐ **2 → 0, bei unverändert 36 gemeldeten Befunden.** Die Prüfung ist nicht
> weicher geworden; sie bricht nur nicht mehr deswegen ab. **Und es gibt keine
> Übergehen-Flagge** — drei erfundene ergeben **2**, der Quelltext kennt keine.

**Am Wegwerf-Bestand wirklich gezogen:** 225 Dateien, 211,0 MB, **jede byteweise
gegen die Quelle geprüft**, beim Nachprüfen `UNVERAENDERT`. ⭐ **Der Anker hielt
ohne `--kein-anker`:** die Kopie trägt `d9449faf…` bei 223 Kursdateien.

### Die Regel, und die drei Bedingungen

**Zugelassen ist ein Befund genau dann, wenn alle drei zutreffen**
(`shared/snapshot.py::_zulassung`): Art `rand_erste` · **erste** Kerze der
Datei · Urteil `ABGELEITETE_TEILKERZE` **und** `aggregat_passt is True`.

⭐ **Als Regel, nicht als Liste der 36 Dateien** — ein neu gelistetes Symbol ist
damit automatisch gedeckt, ein `rand_letzte` nie.

**Das Manifest führt auf, was erlaubt wurde:** `zugelassene_befunde` mit **36**
Einträgen (Datei, Art, erste Kerze, Urteil, Text), `zugelassene_befunde_anzahl`
und ⭐ **`zugelassene_befunde_herkunft`** mit `fundstelle` → *Abschnitt 17.3* und
dem **Wortlaut des Registereintrags im Klartext**. Daneben unverändert
`teilkerzen_befunde` mit allen 36 und `frei_von_teilkerzen: false` — *der
Snapshot verschweigt nicht, dass die Prüfung angeschlagen hat.*

### ⭐⭐ Entschieden wird je BEFUND, nicht je DATEI

**Im `rand_letzte`-Versuch trägt `BTCUSDT_1d.csv` beides:** einen zugelassenen
`rand_erste` an ihrer ersten Kerze **und** den gestellten `rand_letzte`. Der
zugelassene bleibt in der Zählung (*„Zugelassen waren daneben 36 Befund(e)"*),
**die Datei bricht trotzdem ab.**

> ⚠️ **Eine Zulassung je Datei hätte den gefährlichen Rand durchgelassen, sobald
> derselbe Name auch einen erlaubten Befund trägt.** Das stand nicht im Auftrag.
> Probe `3x` misst genau diesen Fall.

**Zwei weitere Entscheidungen, die niemand verlangt hatte:**

**(b) wird eigens nachgestellt**, obwohl `rand_erste` heute nur an der ersten
Kerze entsteht — *„die Bedingung des Registers lautet ‚die erste Kerze der
Datei', nicht ‚ein Befund, der sich so nennt'. Wer die Herkunft des Namens für
den Nachweis nimmt, prüft nichts."*

**(c) holt das Urteil aus dem geladenen Modul**, statt es abzuschreiben — kennt
`zeitabdeckung.py` den Namen künftig nicht mehr, ist die Bedingung **nicht
prüfbar** ⇒ Rückgabewert **2**. *Eine Abschrift liefe gegen ein Urteil, das die
Prüfung gar nicht mehr vergibt: die Ausnahme griffe dann entweder nie oder
immer.*

### Der fünfte Fall: `kein_zeuge`

**Entschieden: nicht belegbar ist nicht zugelassen.** Und es ist **folgenlos**:

| | |
|---|---|
| Dateien mit `kein_zeuge` | **175** von 223 — 150 Aktien, 25 Krypto-1h |
| davon mit **irgendeinem** Befund | ⭐ **null** |

**Der Grund liegt im Aufbau von `pruefe_datei`:** Fehlt der feinere Zeuge, kehrt
die Funktion **vor** der Deckungsprüfung um und hinterlässt einen **Hinweis**,
keinen Befund. `rand_erste` entsteht ausschliesslich aus dieser Deckungsprüfung.
**Wo `kein_zeuge` steht, kann es keinen `rand_erste` geben.**

⚠️ **Streng wird die Regel erst in dem Fall, für den sie gedacht ist:** wenn eine
Eingabe von aussen einen Befund ohne Deckung behauptet, oder wenn einer Datei der
Zeuge künftig abhandenkommt. Probe `3aa`.

### Die Wache

**`shared/test_snapshot.py`: 110 → 164 Prüfungen**, rc=0. Acht neue Proben,
⭐ **sechs mit beissender Mutation** (die Fassung mit entfernter Bedingung muss
den Fehler **übersehen**). ⭐ **Die beiden übrigen ausdrücklich nicht, mit
Begründung:** `3ac` ist die Negativprobe — *„eine Probe, die nur rot sein kann,
beweist nichts"* —, `3ad` misst die **Abwesenheit** einer Flagge: *„eine Wache,
die man entfernen könnte, gibt es dort nicht."*

**Zwei Fälle liessen sich aus echten Kursdateien nicht herstellen** (ein
`rand_erste` an einer späteren Kerze, einer ohne Deckungsprüfung) — die heutige
`zeitabdeckung.py` vergibt beides nicht. **Sie werden gestellt**, weil
`snapshot.py` sich nicht darauf verlassen darf, dass seine Eingabe wohlgeformt
ist. Dass sie dennoch beissen, zeigen ihre Mutationen.

### ⚠️ Der Prüfer für Abschnitt 17 — und der Preis eines Fehlers von gestern

**Der Auftrag sagte: die Datei aus dem TB-48-Paket kommt ins Repo.** ⚠️ **Sie lag
den Unterlagen der Sitzung nicht bei** — das Archiv enthielt allein den
Auftragstext, und im Repo war sie nirgends, **weil die TB-48-Auflage sie draussen
gehalten hat.**

**Sie wurde aus der Belegtabelle des TB-48-Ergebnisses neu geschrieben**, und das
steht in der Datei selbst:

> ⭐ ***„Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes."***

**Die Auflage „unverändert in der Sache" ist am Ergebnis geprüft, nicht am
Quelltext:** 19 Zahlen, `uebersprungen` leer, `nicht_pruefbar` leer, **genau eine
Abweichung**, Rückgabewert **1** — wie in TB-48. Selbsttest **24/24**.

⭐ **Zwei Zahlen fasst der Prüfer bewusst nicht an**, und das ist der Befund, nicht
seine Umgehung: `pandas_market_calendars` (17.5 sagt *„auf dem
Betriebsrechner"*) und die Drift-Messung aus 17.8 (braucht einen echten
yfinance-Abruf, nach T35.4 untersagt). ⭐ **Und die Jahreszahl 2022 wird aus dem
Registertext gelesen, nicht im Werkzeug hinterlegt** — sonst prüfte es seine
eigene Abschrift und meldete nach einer Berichtigung weiter die alte Abweichung.
**Verschwindet der Satz, ist das `nicht pruefbar` (2), nicht „in Ordnung".**

### ⚠️ Die 2019/2022-Frage — die Vermutung trägt nicht

**Vermutet war:** 2022 ist die früheste **Krypto**-Falte, 2019 die über alle
neun.

```
erstes Faltenjahr ueber alle neun Bots:        [2019]
erstes Faltenjahr ueber die fuenf Krypto-Bots: [2019]
```

⚠️ **Alle neun beginnen 2019, Krypto eingeschlossen.** Es sind nicht zwei
Fragen, sondern **eine Frage und zwei Antworten aus zwei
Faltenplan-Generationen.**

| | |
|---|---|
| **2019** | `research/faltenplan_neun/daten/faltenplan.json` — alle neun Bots, nach der Schranke `ERSTE_MOEGLICHE_FALTE = 2019` |
| ⚠️ **2022** | `research/krypto_historie/daten/faltenplan_nach_tb34.json` — **`mindesttraining: 4`, nur Krypto**, Symbolreihe `[3, 6, 9, 13]` — ⭐ **zeichengleich die Reihe aus T34.9** |

> ⭐ **Der schlagende Beleg stand im Register selbst.** Abschnitt **15.6** führt
> eine Faltenliste je Bot und nennt für die Krypto-Bots **ebenfalls 2019**. **Die
> 2022 in 17.3 widerspricht nicht einer Datei unter `research/`, sondern dem
> eigenen Registertext an einer zweiten Stelle.** *Damit ist „welche der beiden
> ist falsch" nicht mehr Auslegung, sondern abgelesen.*

⭐ **Der eigentliche Gehalt ist nicht die Jahreszahl, sondern dass zwei
Faltenpläne mit verschiedenen ersten Falten im Repo liegen und nur einer im
Register steht.** Das ist **T34.10**, seit dem 15.09. offen.

⭐ **Und die Schlussfolgerung trägt unabhängig davon:** Prüfung 16 rechnet
maschinell nach — **null** der 36 kurzen ersten Kerzen fällt in ein
Faltenfenster, in dem ihr Symbol geladen ist, über alle neun Bots und alle
Falten.

⚠️ **Eine Nebenbeobachtung, nicht aufgelöst:** `erstes_faltenjahr_ohne_schranke`
steht bei **acht von neun** Bots auf **2017 oder 2018**. Die 2019 kommt also aus
einer Schranke, nicht aus den Daten. **Ob diese Schranke im Register steht, ist
nicht nachgesehen.**

⚠️ **Kein Registertext ist geändert worden.** Der Auftrag sagte berichten.

### Die Randbedingungen

| | |
|---|---|
| Datenstand vorher = nachher | ✅ `d9449faf…`, 223 |
| Snapshot gezogen | ✅ **nein** — nur in Wegwerf-Verzeichnisse, aus einer **Kopie** von `data/` |
| Sperrlisten-Dateien | ✅ maschinell geprüft, **keine im Diff** |
| Basislauf | **58 grün / 3 rot / 3 ungeprüft / 1 Zeitgrenze = 65** — ⭐ einer mehr grün als in TB-48, und es ist der neue Test |
| ⭐ `git status --porcelain` | **zweimal genommen, vor und nach dem letzten Commit, beide im Beleg** — die zweite leer. *Dritter Versuch nach TB-46 und TB-48, erstes Mal richtig* |
| ⭐ Nebenbeweis aus TB-47 | überlebende Prozesse nach der Zeitgrenze: **0** |

### Der Mac-Lauf, 18.09. 15:05–15:57, Python 3.9.6

**Alles bestätigt, in jedem Punkt:**

| | |
|---|---|
| Trockenlauf | **rc 0**, 36 zugelassene Befunde mit Registerverweis |
| `rand_letzte` · nicht-abgeleiteter `rand_erste` | je **rc 2**, Datei genannt, **kein Snapshot** |
| `shared/test_snapshot.py` | **164/164**, ⭐ kein einziges `[FEHL` in der Ausgabe |
| ⭐ **die neunzehn Zahlen, erstmals auf dem Betriebsrechner** | **19 von 19 geprüft, genau eine Abweichung (Nr. 15), rc 1 — zeichengleich zur Cloud**, keine `nicht pruefbar` |
| Selbsttest des Prüfers | **24/24** |
| ⭐ `pandas_market_calendars` | **4.6.1** — Registertext 5f (17.5) trifft zu |
| Früheste Falte je Bot | **alle neun 2019** |
| Neun Datenbanken | ⭐ `diff vorher/nachher` **leer**, 9 Zeilen |
| Datenstand, `git status`, Snapshot-Ordner | identisch · leer · existiert nicht |

### ⚠️⚠️ Und der Mac fand einen Fehler, den die Cloud nicht sehen konnte — meinen

**In TB-47 hatte ich `system/test_log_rotation.py` aus `BEKANNT_ROT` gestrichen:**
*„auf BEIDEN Rechnern grün, 117/117. Ein falscher Eintrag in dieser Liste ist
teurer als gar keiner."*

**Zehn Einzelläufe auf dem Mac:**

| Lauf | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| | ⚠️ **116** | 117 | ⚠️ **116** | 117 | ⚠️ **116** | 117 | 117 | 117 | 117 | 117 |

**Immer `116 von 117`, immer eine zeitabhängige Probe zum Restfenster beim
Rotieren, ein bis zwei fehlende Zeilen von 238–512 — und die gefallene Probe
wechselt.** Rate **~30 %**.

> ⭐ ***„Die Streichung stützt sich auf je EINE Messung pro Rechner; bei ~30 %
> Flackerrate trifft eine Einzelmessung mit 70 % Wahrscheinlichkeit grün."***

⚠️ **Und es stand längst im Backlog — T38.10, seit dem 15.09.:** *„flattert —
Rennbedingung zwischen Sichern und Leeren."* **Ich habe einen dokumentierten
Befund mit einer Einzelmessung überstimmt, ohne im Backlog nachzusehen.**

**Beide Listen sind damit falsch, in entgegengesetzte Richtungen:**
`UMGEBUNGEN.md` sagt „bekannt rot", `basislauf.py` sagt „auf beiden Rechnern
gruen". ⭐ **Richtig: grün im Regelfall, zeitabhängig flackernd — kein
Zweigbefund, aber auch nicht „grün".**

⭐ **Daraus das neue Prüfprinzip A6: Eine Einzelmessung kann die Abwesenheit
eines flackernden Fehlers nicht belegen.**

### Drei Stellen, an denen der Lauf die Vorgabe korrigiert hat

| | |
|---|---|
| ⭐ **`$TMPDIR` statt nur `/tmp`** | Mein Testauftrag prüfte nur `/tmp` auf Wegwerf-Reste; die Sitzung mass zusätzlich `/var/folders/b_/…/T/`, *„wo `mkdtemp` auf dem Mac wirklich liegt"*. **Beide null.** *Ohne die Ergänzung hätte die Prüfung an der falschen Stelle gesucht und „sauber" gemeldet* — **A1** |
| **62 → 65 Testdateien** | die Zahl in `UMGEBUNGEN.md` stammt aus TB-45 und ist gealtert |
| **`pandas_market_calendars` fehlt in der Paketzeile** | obwohl Registertext 5f darauf verweist. Mac **4.6.1**, Cloud **5.4.0** |

⭐ **Gegenrichtung ebenfalls belegt:** `shared/test_zuteilung.py` ist auf dem Mac
**grün** — der Cloud-Rotbefund war eine Netzsperre, kein Fehler. Und nach der
Zeitgrenze von `test_drawdown_beide_masse.py`: **null überlebende Prozesse**,
wie seit TB-47.

### In einfacher Sprache

**Was wir wissen wollten:** Kann die eingefrorene Kopie der Kursdaten jetzt
gezogen werden — und bleibt die Prüfung dabei so streng wie vorher?

**Was herauskam:** Ja zu beidem. Der Nachweis ist eine einzige Zahl, die von 2
auf 0 gesprungen ist, **bei unverändert 36 gemeldeten Fällen.** Die Prüfung ist
also nicht weicher geworden, nur klüger. Eine Abkürzung zum Übergehen gibt es
ausdrücklich nicht; es wurde eigens nachgemessen, dass es sie nicht gibt.

**Warum das trägt:** Die Regel wurde an einer **absichtlich beschädigten Kopie**
der echten Daten ausprobiert. Wird die **letzte** Kerze angeschnitten — der
gefährliche Fall —, bricht das Programm ab und nennt die Datei. Die
Originaldaten wurden nicht angefasst.

⚠️ **Was falsch war:** Die Vermutung, die Jahreszahl 2022 in den Regeln sei für
die Kryptowährungen richtig. **Alle neun Programme beginnen 2019.** Die 2022
stammt aus einer älteren Planung mit einer anderen Vorgabe. ⭐ **Der Beweis stand
im Regeldokument selbst**, das an anderer Stelle für die Krypto-Programme
ebenfalls 2019 nennt.

**Der eigentliche Punkt ist nicht die Jahreszahl**, sondern dass zwei Planungen
mit verschiedenen Jahren im Projekt liegen — und welche gelten soll, ist eine
offene Entscheidung des Betreibers.

⚠️ **Und der Lauf auf dem MacBook hat noch einen zweiten Fehler von mir
gefunden.** Gestern hatte ich einen Testeintrag aus einer Liste gestrichen mit
der Begründung, dieser Test sei „auf beiden Rechnern grün". **Von zehn Läufen
waren drei rot** — jedes Mal an einer zeitabhängigen Stelle, jedes Mal an einer
anderen. Ich hatte **eine** Messung je Rechner; bei einem Fehler, der in drei von
zehn Fällen auftritt, sieht eine einzelne Messung mit 70 Prozent
Wahrscheinlichkeit gut aus. **Und im Projektplan stand seit dem 15. September,
dass dieser Test flattert.**

⭐ **Daraus wird eine Regel, und sie fehlte: Eine einzelne Messung kann nicht
belegen, dass ein sprunghafter Fehler nicht da ist.** Sie zeigt nur, dass er
diesmal nicht auftrat.
