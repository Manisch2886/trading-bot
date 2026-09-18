# Ergebnis TB-48 — Registernachtrag: Abschnitt 17

**Cloud-Sitzung, 18.09.2026.** Vorgänger: TB-47 (gemergt `a1e7fb4`).
Zweig: `claude/new-session-e63hx4`.

**Eine Schreibaufgabe am Register.** Kein Code, keine Messung am Live-Pfad,
kein Umbau, kein Snapshot.

---

## Die fünf Fragen des Auftrags, zuerst

| Frage | Antwort |
|---|---|
| **Null entfernte Zeilen?** | ⭐ **Ja.** `506	0	docs/VORREGISTRIERUNG_neuselektion.md` |
| **Welche Stellen sind jetzt als ersetzt gekennzeichnet?** | **Drei in Abschnitt 16.3** — (a) ersetzt durch 17.1, (c) ersetzt durch 17.2, (b) *präzisiert* durch 17.9. Dazu **zwei Fortschreibungsvermerke** (Abschnitt 10 und 16.11) und **ein Ergänzungsvermerk** (16.5). ⚠️ **In Abschnitt 15 ist nichts neu gekennzeichnet — und das ist ein Befund**, siehe unten |
| **Welche Zahl wurde wo nachgerechnet — stimmte jede?** | **19 Zahlen, je an ihrer Quelle. 18 stimmten. Eine nicht** — die „erste Selektionsfalte beginnt 2022". Tabelle unten |
| ⚠️ **Sieht der Registerprüfer Abschnitt 17?** | **Nein.** Er ist das TB-41-Werkzeug und kennt Abschnitt 17 nicht. Was er trotzdem leistet und was nicht: eigener Abschnitt unten |
| **Welche Stellen beschreiben etwas, das der Code noch nicht kann?** | **Sieben**, eingetragen als neue Tabelle **17.10**. ⚠️ **Eine davon blockiert den nächsten Schritt:** der Snapshot lässt sich mit dem heutigen Code **nicht ziehen** |

---

## 1. Was geschrieben wurde

**Eine einzige Datei geändert:** `docs/VORREGISTRIERUNG_neuselektion.md`,
2 065 → 2 571 Zeilen.

```
$ git diff --numstat a1e7fb4 -- docs/VORREGISTRIERUNG_neuselektion.md
506	0	docs/VORREGISTRIERUNG_neuselektion.md
```

⭐ **Die zweite Spalte ist die Auflage dieses Auftrags: `0`.** Jede ersetzte
Fassung steht wörtlich an ihrem Platz und trägt einen **eingefügten** Vermerk —
dieselbe Form, die 15.7 und 16.1/16.3/16.6 schon benutzen.

### Abschnitt 17 im Überblick

| | Inhalt | Art |
|---|---|---|
| **17.0** | Was das ist — kein Amendment, Herkunft der Zahlen | Rahmen |
| **17.1** | Registertext 5a, neu: Bestand und Snapshot, zwei Hashes, `asof` | **ersetzt 16.3 (a)** |
| **17.2** | Registertext 5c, korrigiert: Snapshot **vor** dem Tag | **ersetzt 16.3 (c)** |
| **17.3** | Registertext 5a, Zusatz: Ausnahme `rand_erste` | neu, mit Herleitung |
| **17.4** | Registertext 5e, neu: der Lese-Audit | neu |
| **17.5** | Registertext 5f, neu: die registrierte Umgebung | neu |
| **17.6** | Registertext 7, Ergänzung I: der Kein-Entscheid-Tag | ergänzt 16.5 |
| **17.7** | Registertext 7, Ergänzung II: Ereignismenge, n ≥ 20 | ergänzt 16.5, **schliesst 16.11 Zeile 5** |
| **17.8** | Registertext 7, Ergänzung III: Drift | ergänzt 16.5 |
| **17.9** | Nachtrag zur Tatsachennotiz vom 15.09.2026 | **präzisiert 16.3 (b)** |
| **17.10** | Wo Registertext und Umsetzung auseinanderfallen — **sieben neue Zeilen** | Befundtabelle |
| **17.11** | Was dieser Nachtrag nicht tut | Rahmen |

---

## 2. ⚠️ Befund zur Fundstelle: „Abschnitt 15" gibt es nicht

**Der Auftrag nennt für 17.1 und 17.2 als ersetzte Stelle „Abschnitt 15".
Dort steht sie nicht.**

| | |
|---|---|
| **15.7** führt Registertext 5 **ohne Untergliederung** — es gibt dort **kein (a) und kein (c)** | und 15.7 ist seit TB-41 **selbst schon vollständig ersetzt**, mit Vermerk an Ort und Stelle: *„⚠️ ERSETZT durch Abschnitt 16 …, 16.3."* |
| Die Fassung mit **(a)** — `data/live/` gegen `data/snapshots/<hash>/` — steht in **16.3** | Die Fassung **„am Tag des signierten Tags"** steht in **16.3 (c)** |

**Entscheidung:** Die Vermerke sind **dort** gesetzt, wo der abgelöste Text
tatsächlich steht — in 16.3. Ein Vermerk in Abschnitt 15 hätte auf eine Stelle
gezeigt, die es nicht gibt, und hätte den bereits dort stehenden
TB-41-Vermerk verdoppelt. **Der Befund selbst steht mit im Register** (17.1,
Absatz „Befund zur Fundstelle"), damit die Abweichung vom Auftragstext nicht
nur in diesem Bericht steht.

---

## 3. ⚠️⚠️ Der sachliche Befund: „die erste Selektionsfalte beginnt 2022"

**Das ist die eine Zahl von 19, die ihrer Quelle nicht standhält** — und sie
steht im **beigefügten, beschlossenen** `REGISTEREINTRAG_rand_erste.md`, nicht
in einer Zutat dieser Sitzung.

Der Wortlaut lautet: *„20 von 36 — erste Kerze **2017–2020**. Die erste
Selektionsfalte beginnt **2022** — reiner Vorlauf."*

**Beide Hälften der Begründung stimmen nicht:**

| Behauptung | Nachgerechnet | Quelle |
|---|---|---|
| „Die erste Selektionsfalte beginnt 2022" | ⚠️ **2019.** Die erste Falte läuft bei **allen neun** Bots von `2019-01-01` bis `2021-01-01` | `research/faltenplan_neun/daten/faltenplan.json`, `frueheste_falte: 2019` |
| „reiner Vorlauf" (für alle 20) | ⚠️ **Trifft auf 6 der 13 Symbole zu.** Vor dem 01.01.2019 beginnt nur `ADA BNB BTC ETH TRX XRP`. Bei **sieben** — `AAVE DOGE LINK NEAR SOL UNI ZEC` — liegt die erste Kerze **innerhalb** des ersten Faltenfensters | dieselbe Quelle, gegen die Teilkerzen-Befunde gestellt |

### ⭐ Die Schlussfolgerung trägt trotzdem — aus einem anderen Grund

Nachgerechnet über **alle neun Bots und alle Falten**:

```
TREFFER: kurze erste Kerze LIEGT IN einer Falte, in der das Symbol GELADEN ist
Anzahl Treffer: 0
```

Die sieben Symbole stehen in der ersten Falte bei **allen fünf Krypto-Bots** in
`symbole_ohne_historie` — der Loader lässt sie dort gar nicht erst zu.
**Nicht der Vorlauf schützt, sondern die Mindesthistorie des Loaders**
(Registertext 3b (a)). Der Satz *„Kein Symbol-Jahr-Beitrag des Selektionslaufs
hängt an einer der 36 kurzen ersten Kerzen"* ist damit **bestätigt** — und zwar
maschinell über den Faltenplan statt über eine Jahreszahl.

⚠️ **Warum das mehr ist als ein Tippfehler.** Eine Begründung, die an einer
**Jahreszahl** hängt, wird beim nächsten Faltenplan lautlos falsch. Eine, die an
einer **Regel im Register** hängt, lässt sich nachrechnen. Genau diese Prüfung
meint auch der Vorbehalt am Ende des Zusatzes (*„fällt ein `rand_erste`-Befund
an einer Datei an, deren Symbol in einer Selektionsfalte vorkommt…"*).

**Behandlung nach den Regeln des Auftrags:** *gemeldet, nicht stillschweigend
korrigiert.* Der beschlossene Wortlaut **bleibt unverändert stehen**; direkt
darunter steht im Register die Befundnotiz mit der nachgerechneten Fassung —
dieselbe Behandlung wie bei der „vierten falschen Zahl" in 16.7
(*„Der Wortlaut bleibt unverändert stehen, weil er der registrierte ist;
massgeblich ist die Tabelle."*).

---

## 4. Welche Zahl wurde an welcher Quelle nachgerechnet

**19 Zahlen, je eine Zeile, je mit Datei und Fundstelle. Keine ist
abgeschrieben.**

| # | Zahl in Abschnitt 17 | Quelle (Datei · Fundstelle) | Soll | Ist | |
|---:|---|---|---|---|---|
| 1 | Nicht-Kurs-Eingaben im Snapshot: **genau zwei** | `research/snapshotgrenze/ergebnisse/eingaben.json:73,85` | `sp500_top150.txt`, `top25_symbols.txt` | dieselben | ✅ |
| 2 | `datenstand_hash` | `research/vorregistrierung/herkunft.py::datenstand` über `data/` | `d9449faf…` | `d9449faf…` | ✅ |
| 3 | Kursdateien | dieselbe Funktion | 223 | 223 | ✅ |
| 4 | `snapshot_hash` | `shared/snapshot.py::snapshot_hash` über `data/` — ⭐ **in der Cloud neu gerechnet, nicht aus dem Maclauf übernommen** | `4fee547d…` | `4fee547d…` | ✅ |
| 5 | Teilkerzen-Befunde | `shared/snapshot.py::teilkerzen` über `data/` | 36 von 223 | 36 von 223 | ✅ |
| 6 | Arten der Befunde | dieselbe Funktion | `{'rand_erste': 36}` | identisch | ✅ |
| 7 | letzte Kerze betroffen | dieselbe Funktion (keine Art `rand_letzte`) | nein | nein | ✅ |
| 8 | erste Kerze **2017–2020** | ⭐ **selbst nachgezählt** aus den 36 Befunden | 20 | 20 | ✅ |
| 9 | erste Kerze **ab 2023** | ⭐ **selbst nachgezählt** | 16 | 16 | ✅ |
| 10 | erste Kerze 2021/2022 | ⭐ **selbst nachgezählt** (Zusatzprüfung: 20 + 16 = 36 lückenlos) | 0 | 0 | ✅ |
| 11 | **die 11 Symbole** | ⭐ **Mengengleichheit gezeigt** gegen `docs/projektfuehrung/BACKLOG.md:264` (T34.9) — Differenz in **beide** Richtungen leer, je 11 Elemente | identisch | identisch | ✅ |
| 12 | Dateien mit `kein_zeuge` | `shared/zeitabdeckung.py::pruefe_ordner` über `data/` | 175 von 223 | 175 | ✅ |
| 13 | davon Aktien | dieselbe Funktion | 150 | 150 | ✅ |
| 14 | davon Krypto-1h | dieselbe Funktion | 25 | 25 | ✅ |
| 15 | **früheste Selektionsfalte** | `research/faltenplan_neun/daten/faltenplan.json`, `frueheste_falte` | **2022** | ⚠️ **2019** | ❌ |
| 16 | kurze erste Kerze in einer **geladenen** Falte | `faltenplan.json` × Teilkerzen-Befunde, alle 9 Bots × alle Falten | 0 | 0 | ✅ |
| 17 | 18/19 reisst die 95-%-Schwelle | nachgerechnet: 94,7 % | ja | ja | ✅ |
| 18 | 19/20 reisst sie nicht | nachgerechnet: 95,0 % | nein | nein | ✅ |
| 19 | `1 / (1 − 0,95)` | nachgerechnet | 20 | 20 | ✅ |

**Zwei Zahlen aus Abschnitt 17 sind in der Cloud strukturell NICHT
nachrechenbar** und stehen deshalb als übernommene Mac-Messungen:

| Zahl | Warum nicht hier | Wo sie belegt ist | Nachholung |
|---|---|---|---|
| ⚠️ **`pandas_market_calendars` 4.6.1** (17.5) | In **dieser** Cloud-Sitzung ist **5.4.0** installiert. Der Registertext sagt ausdrücklich „**auf dem Betriebsrechner**" | `docs/MACLAUF_TB-47_snapshotgrenze.md:26,46` | **Mac-Testauftrag, Schritt 3** |
| **9 766 von ~11 000 Zeilen, max. 1,2e-6** (17.8) | Setzt einen **echten yfinance-Abruf** voraus. In der Cloud gesperrt (403) — und nach T35.4 ohnehin **bis TB-30b untersagt** | `docs/projektfuehrung/BACKLOG.md:241` (T35.4) | ⚠️ **gar nicht** — die Quelle ist selbst nicht reproduzierbar, das ist der Inhalt des Befunds |

---

## 5. ⚠️ Sieht der Registerprüfer Abschnitt 17?

**Nein.** `research/registernachtrag_tb41/pruefe_register.py` ist das
**TB-41**-Werkzeug; im ganzen Quelltext kommt Abschnitt 17 nicht vor
(`grep -c "Abschnitt 17\|17\.[0-9]"` → **0**).

*Ein Prüfer, der die neuen Texte nicht sieht, meldet grün über den alten
Stand.* Deshalb hier ausdrücklich, **was er prüft und was nicht**:

| ✅ **prüft er — und es ist grün** | ❌ **prüft er nicht** |
|---|---|
| Symbolzahl je Falte, Faltenevidenz, `MIN_HISTORY_*`, Umstellungstag, Universumsdateien — alles **Abschnitt 15 und 16** | **Keine einzige Zahl aus Abschnitt 17.** Die 19 Zahlen oben sind in dieser Sitzung von Hand an ihre Quellen gestellt worden, nicht von ihm |
| Datenstand `d9449faf…` / 223 und dass `data/` unberührt ist | den **`snapshot_hash`** — er kennt nur den Datenstand-Hash |
| ⭐ **0 entfernte Zeilen über das ganze Register** — **das schliesst Abschnitt 17 mit ein**, weil es über `git diff --numstat` auf die Datei geht | ob die Ersetzungsvermerke **sachlich am richtigen Ort** stehen |
| dass die **fünf** in TB-41 ersetzten Fassungen ihren Vermerk tragen (Suchtext `ERSETZT durch Abschnitt 16`) | die **drei neuen** Vermerke in 16.3 — sie sagen `ERSETZT durch Abschnitt 17` und stehen in **keiner** seiner Listen |

```
$ python3 research/registernachtrag_tb41/pruefe_register.py --basis a1e7fb4
  Quelle numstat:     ['506\t0\tdocs/VORREGISTRIERUNG_neuselektion.md']
  geprueft: symbolzahl, faltenevidenz, min_history, umstellungstag,
            universumsdatei, datenstand, daten_unberuehrt,
            null_entfernte_zeilen, ersetzt_gekennzeichnet
  KEIN BEFUND - jede eingetragene Zahl stimmt mit ihrer Quelle ueberein.
```

⚠️ **Sein „KEIN BEFUND" ist ein Nachweis über Abschnitt 15 und 16 und über die
Null — nicht über die Richtigkeit von Abschnitt 17.**

⭐ **Und er hätte den Befund aus Teil 3 nicht gefunden**, selbst wenn er
Abschnitt 17 kennte: Er prüft Symbolzahlen je Falte, nicht den **Beginn** der
ersten Falte. **Ob er um Abschnitt 17 erweitert wird, ist eine eigene
Entscheidung** — diese Aufgabe durfte `research/` nicht anfassen. Der dafür
geschriebene Prüfer liegt **unversioniert in der ZIP-Datei**
(`pruefe_abschnitt17.py`), nicht im Repo.

⭐ **Nebenbefund, unverändert seit TB-47:** Die Datenstand-Berechnung steht
**zweimal zeichengleich** im Repo — `research/vorregistrierung/herkunft.py` und
`research/registernachtrag_tb41/pruefe_register.py:319`. Heute liefern beide
dasselbe. *Wer eines von beiden ändert, merkt den Unterschied nicht.* Nicht
behoben — TB-48 ändert keinen Code.

---

## 6. Welche Stellen beschreiben etwas, das der Code noch nicht kann

**Sieben neue Zeilen, eingetragen als 17.10** — in der Form, die 16.11 dafür
schon benutzt. Die elf Zeilen aus 16.11 bleiben unberührt; **Zeile 5 dort
(Mindestzahl Signale, „offen — Betreiber") ist mit 17.7 erledigt** und im
Register als Fortschreibung vermerkt.

| # | Registertext | Was der Code heute tut |
|---:|---|---|
| 1 | **5a (17.1)** — Snapshot neben dem Bestand | Es gibt **einen** Ordner `data/`; kein Snapshot. Unverändert 16.11 Zeile 1 |
| 2 | ⚠️⚠️ **5a-Zusatz (17.3)** — `rand_erste` zugelassen | **Der Snapshot lässt sich heute nicht ziehen** — siehe unten |
| 3 | **5e (17.4)** — Lese-Audit | **Nicht vorhanden.** Kein Modul führt Buch über gelesene Dateien |
| 4 | **5f (17.5)** — registrierte Umgebung, Abbruch rc=2 | **Nicht vorhanden.** Es gibt **kein `requirements.lock`**, keine Fassungsprüfung, keinen Abbruchpfad |
| 5 | **7-I (17.6)** — Kein-Entscheid-Tag | **Nicht vorhanden.** Die neun `forward_test.py` kennen den Begriff nicht |
| 6 | **7-II (17.7)** — Ereignismenge, n ≥ 20 | **Kein Vergleichswerkzeug** (16.11 Zeile 4). Die Mindestzahl ist jetzt da, das Werkzeug nicht |
| 7 | **7-III (17.8)** — Drift | **Nicht vorhanden.** Kein `forward_test.py` protokolliert Datenstand-Hash oder Entscheidungskerzenwerte |

### ⚠️⚠️ Zeile 2 ist die dringendste — und sie blockiert den nächsten Schritt

**`shared/snapshot.py::ziehen` wirft bei *jedem* Teilkerzen-Befund**, vor dem
Kopieren:

```python
kerzen = teilkerzen(quelle, zeitabdeckung)
if kerzen["befunde"]:
    raise Snapshotfehler(
        "Die Teilkerzen-Pruefung hat %d Datei(en) mit Befund gefunden: ... "
        "Es wird NICHT gezogen ...")
```

**Es gibt 36 Befunde. Also bricht `--ziehen` heute immer ab.** Registertext 5a,
Zusatz (17.3) lässt `rand_erste` an der ersten Kerze ausdrücklich zu — der Code
kennt diese Ausnahme nicht, und eine Übergehen-Flagge soll es nach 17.3 auch
**nicht** geben (*„Die Prüfung selbst wird nicht abgeschwächt"*).

⭐ **Das Manifest ist schon vorbereitet:** `schreibe_manifest` führt das Feld
`teilkerzen` mit Art und Text je Datei — genau das, was 17.3 (c) verlangt. Es
wird nur nie geschrieben, weil der Lauf vorher abbricht.

**Die Lücke ist damit klein und genau benannt:** die Ausnahme muss **gegen den
Registereintrag** geprüft werden (Art `rand_erste`, **erste** Kerze,
nachgewiesenes Aggregat), nicht gegen eine Flagge. ⚠️ **Das ist eine eigene
Aufgabe mit eigener Freigabe** — TB-48 hat keinen Code angefasst.

*Der Auftrag sagt: „Der Snapshot soll unmittelbar danach gezogen werden." Mit
dem heutigen Stand von `shared/snapshot.py` geht das nicht.*

---

## 7. Datenstand und Arbeitsbaum

| | |
|---|---|
| **vorher** | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien |
| **nachher** | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien |
| **identisch** | ⭐ **ja** — `data/` ist nicht angefasst worden |
| `snapshot_hash` | `4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608` — ⭐ **in der Cloud neu gerechnet, trifft den TB-47-Maclauf exakt** |
| **Snapshot gezogen** | **nein.** Kein Ordner `snapshots/` entstanden |

---

## 8. Umgebung — was diese Cloud-Sitzung vorgefunden hat

⭐ **Abweichungen von `docs/UMGEBUNGEN.md` sind zu melden.** Hier sind sie.

| | Mac (laut `UMGEBUNGEN.md`) | **diese Cloud-Sitzung** | |
|---|---|---|---|
| Python | 3.9.6 | **3.11.15** | wie erwartet |
| `pandas` / `numpy` | 2.3.3 / 2.0.2 | ⚠️ **3.0.6 / 2.4.6** | **eine Hauptversion über dem Mac** |
| `pandas_market_calendars` | **4.6.1** | ⚠️ **5.4.0** | ⚠️ **betrifft Registertext 5f (17.5) unmittelbar** |
| `scipy` | fehlt | **1.17.1** vorhanden | bekannt wechselnd |
| `dateparser` | 1.2.2 | 1.4.3 | wie dokumentiert |
| `node` | vorhanden | **v22.22.2** | vorhanden |
| `yfinance` / `binance` | erreichbar | ⚠️ **Netzsperre (403)** | wie dokumentiert |

⚠️ **Alle Fremdpakete fehlten beim Sitzungsstart und mussten nachinstalliert
werden** — `pandas`, `numpy`, `scipy`, `fastapi`, `uvicorn`, `httpx`,
`yfinance`, `python-binance`, `dateparser`, `pandas_market_calendars`.
**Genau der in `docs/UMGEBUNGEN.md` beschriebene Fall in Reinform:** *„die Cloud
ist nicht EINE Umgebung, sondern eine je Sitzung."*

⭐ **Für die Zahlen dieses Nachtrags war das folgenlos:** `shared/snapshot.py`,
`shared/zeitabdeckung.py` und `research/vorregistrierung/herkunft.py` kommen mit
**reiner Standardbibliothek** aus. Die 19 nachgerechneten Zahlen hängen an
keinem Fremdpaket. ⚠️ **Mit einer Ausnahme:** die Fassung des
Handelskalenders — und genau die ist deshalb in den Mac-Testauftrag gewandert.

⚠️ **Eine Einschränkung des Registerprüfers, die daraus folgt:** Sein
Trockenlauf-Beleg braucht `pandas` und war beim ersten Aufruf nicht lauffähig
(`Trockenlauf nicht lauffaehig: ModuleNotFoundError: No module named 'pandas'`).
Er ist dann auf den **Dokument-Beleg** ausgewichen und hat das **im Bericht
gesagt** — richtig so; die Prüfung blieb aussagekräftig, weil sie ihre Quelle
nennt.

