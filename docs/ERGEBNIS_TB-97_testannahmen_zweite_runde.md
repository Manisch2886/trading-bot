# TB-97 — Ergebnis: Testannahmen, zweite Runde — die Mutationsproben benannt und mit Gegenprobe, `F4` beisst, die vier Literale aus Plan und Register, die Sonde liest ihre Gruppen aus dem Abbild

**Sitzungstitel:** `TB-97` · **Stand:** 24.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-97_testannahmen_zweite_runde.md` · **Belege:** `docs/belege/TB-97/`
**Eingang:** `4777d18` (TB-96-Abgabe) · Commits: `79eda3c` (Schritt 0), `ae8db0b` (Block B+C+D,
Test), `3b60ca8` (Block E, Sonde), Abgabe-Commit (Belege, dieses Dokument, Journalblock CY).
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`,
Abschnitte 5–7; Register 40.7 und 40.8 (a)–(e).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** Der Test läuft **188/188, rc 0**, in 781 s (vorher 165/165; in dieser Sitzung
am Eingang 504 s gemessen, TB-95 534 s). **23 Prüfungen sind dazugekommen**, alle
Gegenproben. Keine Prüfung ist entfallen, keine abgeschwächt, keine Ausnahme für einen
Bot, keine Toleranz. Kein Sperrlistenhash hat sich bewegt, und kein Abbild ist
geschrieben worden. Die Sonde meldet gegen das echte Abbild weiter 0 Befunde.

**Drei Befunde, die der Auftrag nicht erwartet hat:**

- ⚠️⚠️ **Es sind sieben Mutationsproben, nicht acht**, und `F4` ist keine davon (A1).
  Teil H hat acht Prüfungen, H0 bis H7. H0 ist der Grundlauf ohne Mutation.
  Abbruchkriterium 2: gemeldet, mit der gemessenen Menge weitergearbeitet.
- ⚠️ **Alle sieben beissen heute** (A2). `F4` ist der einzige bekannte Fall, der nie
  gebissen hat. H6 trägt nur zusammen mit H5.
- ⚠️⚠️ **Fables Einordnung von `beispieldaten.py` Z. 69 („irgendeine Selektionsfalte")
  trifft nicht zu** (A4). Die Krisenfalten brauchen einen tiefen Benchmark-Drawdown.
  Mit Fables Beispiel, der zweiten Selektionsfalte, wären die Beispieldaten für
  `rsi2_mean_reversion` und `volatility_breakout` in jeder Zelle unzulässig. Umgestellt ist
  deshalb auf die Jahre aus 5.1 Nr. 4. **Das braucht Fables Kenntnisnahme** (Abschnitt 7).

Dazu ein Umstand an der Grenze des Auftrags: Das echte Abbild führt die Gruppen
„bestimmt" und `EINGEFROREN` **nicht** (A5). Der Erzeuger musste mit umgebaut werden,
und `shared/test_sperrlistensonde.py` ebenfalls, eine Datei ausserhalb der Liste in G5.
**Ein echtes Abbild mit den Gruppen steht aus** und braucht Freigabe (Abbruchkriterium 4:
gemeldet, nicht erzeugt).

---

## 0. Schritt 0

| | |
|---|---|
| Arbeitsbaum | vier Dateien des steuernden Chats (Auftrag TB-97, Fable-Anfrage 24b, Zeiger, Berichtigung in `starte_sitzung.sh`) → **`79eda3c`**; danach leer |
| Git-Sperrdateien | `find .git -name '*.lock'` → keine |
| HEAD am Eingang | `4777d18` ✔ |
| Abschnitt 40 | vorhanden (Register Z. 7632) — Abbruchkriterium 1 greift nicht |

## 1. Block A — erst benennen, dann prüfen

### A1 — die Mutationsproben, benannt (`a1_mutationsproben.txt`)

Gesucht nach dem Kriterium des Auftrags: Die Probe verändert den **Code** (Kopie des
Ordners, `_ersetze`), wertet neu aus und prüft, dass sich das Ergebnis ändert.

| Name | Teil | Zeile (am Eingang) | was mutiert wird | woran gemessen |
|---|---|---|---|---|
| H1 | H | 624 / `_ersetze` 621 | `registerdaten.py`: `SPITZEN_SCHWELLE` 0,50 → 99,0 | „Spitze" in der Ausgabe, Kopie gegen Original |
| H2 | H | 635 / 631 | `auswertung.py`: Plateau-Mittel ohne den Punkt selbst | Gewinnerzeile, Kopie gegen Original |
| H3 | H | 654 / 595 (`_h3_lauf`) | `auswertung.py`: die Null für Falten ohne Trade entfernt | Zeile „Netto-Sharpe (Med.)" vorher gegen nachher, strikte Mehrheit ohne Trade |
| H4 | H | 666 / 663 | `registerdaten.py`: `DD_RELATIVER_FAKTOR` 1,25 → 0,01 | Zulässigkeitszeile, Kopie gegen Original |
| H5 | H | 681 / 676 | `registerdaten.py`: eine Live-Zahl (8,0 %) in einen Grenzsatz | `pruefe_grenzsaetze.py` rc 1 und „Live-Wert" |
| H6 | H | 689 / 684 | **zusätzlich** zu H5, in derselben Kopie: Wache 2 entfernt | `pruefe_grenzsaetze.py` rc 0 (der Fehler kommt durch) |
| H7 | H | 704 / 697 | `registerdaten.py`: eine Stufung 4 → 3 | rc ≠ 0 und „ausserhalb 1,5 bis 2,0" |

**Nicht gezählt:** H0, der Grundlauf ohne Mutation. A9, A10 und E-a/E-c ändern Daten,
nicht Code. **`F4` ändert nichts**: Es vergleicht im selben Prozess zwei Mediane
derselben Werte.

⚠️⚠️ **Befund: sieben, nicht acht.** Die Zahl „acht" (Abschnitt 12, `BERICHT.md:29`)
stammt aus TB-30a. Am Stand `a2fcf01` stehen dieselben acht `pruefe("H…")`-Aufrufe
H0–H7. Gezählt waren also offenbar die **Prüfungen von Teil H**, einschliesslich des
Grundlaufs. Der TB-30a-Testauftrag sagt dazu „Teil H startet acht eigene Prozesse"
(`TESTAUFTRAG_TB-30a_vorregistrierung.md:143`). Das zählt Prozesse, keine Mutationen.
Weiter gemessen:

- **H5 und H6 teilten sich eine Kopie.** H6 ist eine Doppelmutation.
- **Register 40.7 und die Auftragsprosa zählen `F4` zu den acht.** Gemessen gehört `F4`
  nicht dazu. Es bekommt seine Gegenprobe trotzdem (Block B).
- Der Kopf des Tests beschreibt die Bauart richtig („ändern dort EINE Zeile"), bis auf H6,
  das zwei Stellen ändert.

### A2 — beisst jede heute? (`a2_beissen_vorher.txt`, Werkzeug `a2_beissen.py`)

Gemessen am **unveränderten** Test. Für jede Mutation k lief `teil_h()` einmal, wobei nur
diese eine Mutation weggelassen war: `_ersetze` prüfte weiter, dass die Stelle existiert,
schrieb aber nicht. Die übrigen Mutationen blieben.

| Probe | Mutation weggelassen ⇒ | |
|---|---|---|
| H1 | H1 scheitert, sonst nichts | **beisst** |
| H2 | H2 scheitert (Gewinnerzeile gleich) | **beisst** |
| H3 | H3 scheitert (`0.0000` / `0.0000`); mit **leerer Menge** ebenfalls (`0.1000` / `0.1000`) | **beisst**, beide Gegenproben |
| H4 | H4 scheitert | **beisst** |
| H5 | H5 scheitert (rc 0, „395/395") | **beisst** |
| H6 | H6 scheitert (rc 1, Wache 2 meldet `8.0`) | **beisst** |
| H7 | H7 scheitert (rc 0) | **beisst** |
| `F4` | Bedingung mit `<=` bleibt wahr, auch ohne jede Falte ohne Trade | ⚠️ **beisst nicht** |

⚠️ **Zusatz zu H6:** Sind die Mutationen von H5 **und** H6 weggelassen, **besteht H6**. Es
prüft nur rc 0, und ohne die Live-Zahl aus H5 ist rc 0 trivial. **H6 trägt nur zusammen
mit H5.** Die Gegenprobe von H6 lässt deshalb nur H6s eigene Mutation weg. Die Live-Zahl
bleibt immer eingesetzt (Konstante `_LIVE_ZAHL`).

Laufzeit von A2: 1985 s, sieben volle Durchläufe von Teil H plus Zusätze.

### A3 — `F4` ausgemessen (`a3_f4.txt`)

| | |
|---|---|
| Text | „der Median mit der Null liegt **unter** dem Median ohne sie" |
| Code am Eingang | `median(werte) <= median(ohne die Falte)`, also `<=` |
| auf null gesetzt | **1 von 9** Selektionsfalten (`2022`) |
| Mediane heute | `0.1000` / `0.1000` → `<=` wahr, `<` falsch |
| kleinstes wirksames k | **5** bei n = 9 (k = 0…4: gleich; ab k = 5 `0.0000` gegen `0.1000`) = `len(sel)//2 + 1` |
| Ablauf mit Mehrheit `2017`–`2021` | `0.0000` / `0.1000`, `<` wahr |
| Ablauf mit leerer Menge | `0.1000` / `0.1000`, `<` falsch: die Gegenprobe scheitert, wie sie soll |

Dieselbe Rechnung wie bei `H3` in TB-95: Das kleinste wirksame k ist ⌈(n+1)/2⌉.

### A4 — die vier Literale (`a4_literale.txt`)

| Stelle | was sie tut | braucht sie … | gemessen |
|---|---|---|---|
| Teil D `ruhig, krise = "2021", "2020"` | D1/D2: In einer ruhigen Falte bindet `DD_Toleranz`, in einer Krisenfalte die relative Grenze. D6/D7 am Ablauf in der ruhigen Falte | **die Regel aus 4.4, kein bestimmtes Jahr**: ruhigste und schwerste Selektionsfalte des heutigen Plans | heute ruhigste **2017** (−1,18 %, Toleranz bindet), schwerste **2020** (−18,93 %, relativ). 2021 bindet ebenfalls Toleranz |
| Teil F `ohne = "2022"` | F1–F4: Falten ohne Trade zählen mit 0 | **irgendeine** Selektionsfalte, für `F4` aber eine **strikte Mehrheit** | Mehrheit aus dem Plan: `2017`–`2021` |
| `beispieldaten.py` Z. 69 Krisen-Drawdown | −11 % statt −3 % in den Krisenfalten, bei Exposure 0,60 | ⚠️ **weder ein beliebiges Jahr noch irgendeine Falte**: eine Falte, in der −11 % bei 0,60 die Bedingung besteht | bei `turtle_soup_stocks` nur **4 von 9** (2018, 2020, 2022, 2025). **Zweite Selektionsfalte** (Fables Beispiel): bei **`rsi2_mean_reversion` und `volatility_breakout` 2019 → unzulässig**. Die Falten, die **2020/2022 aus 5.1 Nr. 4** abdecken, bestehen bei **allen neun** |
| `beispieldaten.py` Z. 77 Exposure | 0,60 in Krisenfalten, sonst 0,40; sonst ist der Zufalls-Timing-Test entartet | irgendeine Selektionsfalte (nicht alle) | das Literal traf bei `elliott_wave` **nie** (keine Falte heisst `2020`), die Exposure war dort konstant |

⇒ **Z. 69 und Z. 77 hängen an derselben Menge.** Ihre Bedingung ist die von Z. 69.

### A5 — die Sonde und das Abbild

| | |
|---|---|
| `BESTIMMT_NICHT_EINGETRAGEN` | `shared/sperrlistensonde.py` Z. 104–107 am Eingang: ein Eintrag, `ergebnisse/benchmark_drawdowns_vt.json`, Grund „Vollzug steht aus". Nur **genannt**, nicht geprüft |
| `EINGEFROREN` | kennt die Sonde nicht (eigener Kopf Z. 69–70) |
| Felder des Abbilds `sperrliste_abbild_2026-09-23.json` | `art`, `erzeugt`, `pfadregel`, `punkte`, `quelle`, **sonst nichts**. Weder „bestimmt" noch `EINGEFROREN` |
| ⇒ | ⚠️ **Der Erzeuger muss mit** (`sperrliste_abbild.py`), und das heutige Abbild kennt die Gruppen nicht. Gemeldet, gebaut, an einer Kopie im Scratchpad nachgewiesen (Block E). **Ein echtes Abbild steht aus** |

### A6 — Hashes und Sonde am Eingang (`a6_hashes_vorher.txt`, `a6_sonde_vorher.txt`)

28 Pfade (Liste `pfade_28.txt`, dieselbe wie TB-96), **28/28 gleich TB-96 nachher**. Sonde
gegen `sperrliste_abbild_2026-09-23.json`: **0 Befunde, 15/15 gleich, (ii) 0, rc 2**. Wie
erwartet. Der ganze Test am Eingang: 165/165 in 504 s (`a6_test_vorher.txt`).

## 2. Block B — `F4` beisst wieder

| | |
|---|---|
| **B1** | `<=` → `<` |
| **B2** | `ohne = set(sel[:len(sel) // 2 + 1])` aus dem Plan (`_selektionsfalten`), also fünf von neun |
| **B3** | `F4-G`: derselbe Weg (`_f_lauf`) mit **leerer Menge** ⇒ `0.1000` / `0.1000` ⇒ `F4` scheitert, die Gegenprobe besteht. Im Test bei jedem Lauf. Beide Ausgaben stehen in `f_test.txt` bzw. `a3_f4.txt` |
| **B4** | Der Kommentar nennt die Regel, den Grund (Median, `<=`) und den Stand: „Beim Plan von TB-97 für turtle_soup_stocks: fünf von neun Selektionsfalten (2017-2021)" |

Name und Stelle von `F4` sind geblieben (Teil F, vierte Prüfung). F1–F3 prüfen jetzt jede
Falte der Menge. F1 verlangt eine nicht leere Menge, damit `all([])` nicht wahr wird.

## 3. Block C — die vier Literale

| Stelle | umgestellt auf | Gegenprobe (im Test, bei jedem Lauf) |
|---|---|---|
| Teil D | `_ruhig_und_krise`: ruhigste und schwerste **Selektionsfalte des heutigen Plans** nach Benchmark-Drawdown bei 0,50. D1/D2 als Aussagen `_toleranz_rettet` / `_relativ_bindet` | **D1-G:** die schwerste Falte als ruhige gelesen ⇒ D1 scheitert. **D2-G:** die ruhigste als Krisenfalte ⇒ D2 scheitert |
| Teil F | die strikte Mehrheit aus dem Plan (siehe B2) | **F1-G:** die Bestätigungsperiode als „Falte ohne Trade" (umgewidmet) ⇒ F1 findet sie nicht. **F4-G** siehe B3 |
| `beispieldaten.py` Z. 69 und 77 | `krisenfalten(falten, jahre)`: die Selektionsfalten, die eines der Jahre aus **5.1 Nr. 4** voll abdecken, gerechnet aus `von`/`bis`. `standard_drawdown`/`standard_exposure` sind Fabriken über diese Menge | **neue Prüfung `G11`** je Bot: Krisenfalten vorhanden, Exposure nicht konstant, der Standard-Drawdown besteht die Bedingung in jeder Selektionsfalte. **G11-G1:** Krisenfalten zu Bestätigungsfalten umgewidmet ⇒ scheitert. **G11-G2:** die Krise auf die ruhigste Falte verbogen ⇒ −11 % reisst die Grenze ⇒ scheitert |

⚠️ **Zu `beispieldaten.py` — eine Abweichung von Fables Wortlaut, begründet mit A4.** Fable
ordnete Z. 69/77 als „irgendeine Selektionsfalte" ein, „z. B. die zweite Selektionsfalte
des Bots". Gemessen braucht Z. 69 eine Falte mit tiefem Benchmark-Drawdown. Die zweite
Selektionsfalte fällt bei zwei Bots durch. Die Stelle bildet 4.4 ab („Ist die Bedingung in
2020 und 2022 überhaupt erfüllbar?") und liest deshalb, nach der **ersten** Hälfte seiner
Regel, die Jahre aus der Registerstelle. Das ist 5.1 Nr. 4, die Zeile, die `G6` schon
liest.

⭐ **Folge: 5.1 Nr. 4 hat jetzt zwei Leser, aber weiter nur einen Parser.** Das Muster steht
genau einmal, in `beispieldaten.jahre_aus_register_5_1_nr_4`. `G6`
(`_testjahre_aus_register`) ruft diesen Parser auf, statt ein zweites Muster zu führen.
**`G6` hat sein Verhalten nicht geändert**: dasselbe Muster, genau ein Treffer, sonst
`None`. Die Marke bei 5.1 Nr. 4 nennt nur den Test und gehört ergänzt (Vorschlag 41.4).
`_abgedeckte_jahre` wandert aus demselben Grund mit.

Nach der Umstellung stehen Jahreszahlen in beiden Dateien **nur noch in Kommentaren und
Docstrings** (`grep`, siehe `c_literale_nachher.txt`).

## 4. Block D — Gegenproben für alle sieben

**Bauart:** eine Hilfsfunktion `_mit_gegenprobe(name, text, lauf, bedingung, zusatz)`. Sie
führt die Probe einmal **mit** Mutation aus (`<name>`, muss bestehen) und einmal **ohne**
(`<name>-G`, muss scheitern), über dieselbe Funktion `lauf(mutieren)`. `_ersetze` hat
dazu einen Schalter `mutieren`. Mit `False` prüft es weiter, dass die Stelle existiert,
schreibt aber nicht. So kann eine Gegenprobe nicht still ins Leere laufen, wenn sich der
Code unter ihr ändert. **Sie läuft bei jedem Lauf mit, von Hand anstossen muss man nichts.**
H5 und H6 bekommen je eine eigene Kopie. H6 setzt die Mutation von H5 immer ein (A2).

| Name | Teil | was mutiert wird | beisst **vorher** (A2) | beisst **nachher** (Gegenprobe im Test) |
|---|---|---|---|---|
| H1 | H | `SPITZEN_SCHWELLE` 0,50 → 99,0 | ja | ja — `H1-G` bestanden |
| H2 | H | Plateau-Mittel ohne den Punkt | ja | ja — `H2-G` bestanden |
| H3 | H | Null für Falten ohne Trade entfernt | ja (auch leere Menge) | ja — `H3-G` und `H3-L` bestanden |
| H4 | H | `DD_RELATIVER_FAKTOR` 1,25 → 0,01 | ja | ja — `H4-G` bestanden |
| H5 | H | Live-Zahl im Grenzsatz | ja | ja — `H5-G` bestanden |
| H6 | H | Wache 2 entfernt (mit H5-Mutation) | ja (nur mit H5) | ja — `H6-G` bestanden |
| H7 | H | Stufung 4 → 3 | ja | ja — `H7-G` bestanden |
| *`F4`* | *F* | *keine Code-Mutation; Mehrheit ohne Trade* | ***nein*** (`<=`) | *ja — `F4-G` bestanden* |

⭐ **Diese Tabelle ist der Nachweis zu 40.7.** Die Spalte „nachher" gilt für den Lauf in
`f_test.txt`.

**Laufzeit:** 781 s gegen 504 s am Eingang (`a6_test_vorher.txt`; dort lief eine 81-s-Messung parallel, Block F lief ohne Parallellast) und 534 s
in TB-95. Weit unter der Schranke von ~25 min. Block D ist vollständig.

## 5. Block E — die Sonde

**E1 — getrennte Schlusszeilen.** Die Zeile „Bilanz: … Punkte …" ist durch zwei Zeilen
ersetzt. Am echten Abbild:

```
Pfad-Bestandteile: 15 geprueft, davon 15 mit 0 / 0 mit 1 / 0 mit 2  (punkte 15; nicht im Abbild (2): bestimmt, eingefroren)
Regel-Bestandteile: 12 nicht pruefbar (2), je mit Verweis auf die Tatsachennotiz: Punkt 1 -> keine im Abbild; … Punkt 14 -> keine im Abbild
```

Der **Gesamtwert ist unverändert** nach 36.5 gebildet: 1 schlägt 2 schlägt 0. Die
Rückgabezeile bleibt. Der Verweis je Punkt kommt aus einem optionalen Feld
`tatsachennotiz` des Abbilds. **Heute trägt kein Punkt eines, deshalb steht bei allen zwölf
„keine im Abbild".** Damit ist ablesbar, dass die Tag-Vorbedingung „jede 2 mit Notiz"
(23c) **nicht** erfüllt ist. Das war schon vorher so (39.9: „hier nicht geprüft"), jetzt
steht es in der Ausgabe.

**E2 — die Gruppen kommen aus dem Abbild.** `BESTIMMT_NICHT_EINGETRAGEN` ist entfernt. Die
Sonde liest `punkte`, `bestimmt` und `eingefroren` aus dem Abbild und prüft die zwei neuen
Gruppen wie die Punkte, Hash gegen Abbild (37.2). **Eine im Abbild fehlende Gruppe ist 2,
eine leere Gruppe ist 0.** Das sind verschiedene Aussagen. Der **Erzeuger** schreibt beide
Gruppen:

- `bestimmt` aus `--bestimmt PFAD=GRUND`. Ohne Angabe ist die Gruppe **leer**, der
  Registerstand nach 39.3.
- `eingefroren` aus `herkunft.py::EINGEFROREN`. Gelesen wird mit `ast`, **ohne
  `herkunft.py` auszuführen oder zu ändern** (Punkte 11/12). Die Pfade werden nach R5
  aufgelöst.

Nachweis an einem **Probe-Abbild im Scratchpad** (`e2_e3_sonde.txt`): rc 0, `bestimmt`
leer, `eingefroren` zehn Einträge. Ein zweiter Aufruf auf dasselbe Ziel gibt rc 1 (36.1
(2)). Die Sonde dagegen: alle **25** Pfad-Bestandteile gleich, beide Gruppen 0, rc 2.

**E3 — Gegenprobe.** Eine Kopie des echten Abbilds im Scratchpad bekam einen **erfundenen**
bestimmt-Pfad. Die Sonde meldet ihn: Gruppe 2, `FEHLT`, und nennt ihn im Grund.
**Gegenprobe:** dieselbe Kopie mit leerer Gruppe, dann 0 und der Pfad kommt 0-mal vor. Der
**Nullpunkt gegen das echte Abbild** ergibt 0 Befunde, 15/15 gleich, (ii) 0, rc 2.
`sperrliste_abbild_2026-09-23.json` ist vorher und nachher `2f23f76c…`. In `ergebnisse/`
ist nichts neu.

**Dauerhaft** stehen dieselben Proben in `shared/test_sperrlistensonde.py`, Fall 8
(8a–8i). Dazu kommen `H7f` (Schlusszeilen) und das neu gefasste `H7c`. **59/59** (`e_sondentest.txt`), vorher
49/49.

⚠️ **Zwei Dinge, die sich daraus ergeben:**

- **Gegen das heutige Abbild sind beide Gruppen 2 („nicht im Abbild").** Am Gesamtwert
  ändert das nichts, er war schon 2. Schliessen lässt es sich nur mit einem **neuen echten
  Abbild**, und das gehört zum Sperrlisten-Vollzug und braucht Freigabe (36.6/37.3).
  Gemeldet, nicht erzeugt (Abbruchkriterium 4).
- Die Ausgabe nennt `benchmark_drawdowns_vt.json` **nicht mehr**. 39.3 und 39.9 beschreiben
  die alte Ausgabe („nennt weiter `_vt.json` mit ‚Vollzug steht aus'"). Das ist jetzt
  überholt, und die Sätze bleiben zeichengleich (Vorschlag 41.5).

## 6. Block F — der ganze Test (`f_test.txt`)

| | |
|---|---|
| Befehl | `trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py` |
| Schlusszeile | `188/188 Pruefungen bestanden.` erreicht |
| Ergebnis | ⭐ **188/188, rc 0** |
| Zahl | **188** (vorher 165), **+23**: D1-G, D2-G · F1-G, F4-G · G11 × 9, G11-G1, G11-G2 · H1-G … H7-G, H3-L |
| Laufzeit | **781 s** (Eingang 504 s, TB-95 534 s) |
| rot gewordene Prüfungen | **keine** |

Danach (`g5_hashes_nachher.txt`, `g5_sonde_nachher.txt`): Von den 28 Pfaden haben sich **genau
vier** bewegt: `test_vorregistrierung.py`, `beispieldaten.py`, `sperrlistensonde.py` und
`sperrliste_abbild.py`. Die übrigen **24** sind gleich, darunter **alle Sperrlistendateien**,
beide Abbilder, `faltenplan.json` und alle Benchmark-Tabellen. Die Sonde meldet 0 Befunde.

## 7. Abweichungen und Befunde, zusammengefasst

| | |
|---|---|
| 1 ⚠️⚠️ | **Sieben Mutationsproben, nicht acht** (A1). „Acht" zählte die Prüfungen von Teil H einschliesslich des Grundlaufs H0. `F4` ist keine Mutationsprobe. Register 12 („davon acht Mutationsproben") und 40.7 („alle acht") tragen eine Zahl, die als **Aussage** nicht stimmt. Vorschlag 41.1 |
| 2 ⚠️ | **H6 trägt nur zusammen mit H5** (A2, Zusatz). Ohne die H5-Mutation besteht H6 trivial. Im Test festgehalten (`_LIVE_ZAHL` immer eingesetzt) |
| 3 ⚠️⚠️ | **`beispieldaten.py` Z. 69 braucht nicht irgendeine Selektionsfalte** (A4). Fables Beispiel „zweite Selektionsfalte" machte die Beispieldaten für zwei Bots unzulässig. Umgestellt auf die Jahre aus 5.1 Nr. 4, per Abdeckung. **Abweichung vom Wortlaut seiner Regel, braucht seine Kenntnisnahme** |
| 4 ⚠️ | **5.1 Nr. 4 hat einen zweiten Leser** (`beispieldaten.py`), aber weiter nur einen Parser. Die Marke bei 5.1 Nr. 4 nennt nur `G6` |
| 5 ⚠️ | **Das echte Abbild führt die Gruppen nicht** (A5). Der Erzeuger ist umgebaut, ein echtes Abbild steht aus (Freigabe). Gegen das heutige Abbild zeigt die Sonde beide Gruppen als 2 |
| 6 ⚠️ | **Datei ausserhalb der Liste in G5 geändert:** `shared/test_sperrlistensonde.py`. Ohne die Änderung wäre er gebrochen (`sonde.BESTIMMT_NICHT_EINGETRAGEN` in `baue_kopie`, `H7c` prüfte die alte Konstante). Er trägt jetzt die dauerhafte E3-Gegenprobe. Er gehört nicht zu den 28 gemessenen Pfaden |
| 7 | **Die Regelzeile der Sonde zeigt „keine im Abbild" für alle zwölf Punkte.** Die Tag-Vorbedingung „jede 2 mit Tatsachennotiz" (23c) ist offen. Neu ist das nicht, aber jetzt steht es in der Ausgabe |
| 8 | **Register 4.4 weicht vom heutigen Tabellenstand ab** (A4): 2019 −3,69 % gegen heute −3,66 %, 2025 −8,89 % gegen −8,77 %. 2021 1,25 × −2,98 gegen −2,97 (Rundung). Die Werte in 4.4 sind der Stand vom 14.09. Gehört in die Tatsachennotiz zu 4.4 (Abschnitt 8) |
| 9 | Der Auftrag sagt in G5 „ggf. `sperrliste_abbild.py` und `beispieldaten.py`". **Beide mussten mit**: der Erzeuger wegen A5, `beispieldaten.py` wegen der Literale Z. 69/77 |

## 8. G3 — Wortlaut für die Tatsachennotiz zu 4.4 (gemessen, nicht eingetragen)

Als Marke unter der Tabelle von 4.4, **nach** dem Absatz „`test_vorregistrierung.py` Teil D
prüft beide Richtungen …":

> ⚠️ **Tatsachennotiz zu 4.4 (40.8 (b), Fable 24a, TB-97, 24.09.2026) — die Jahre dieser
> Tabelle sind Beispieljahre vom Stand 14.09.2026.** 2021 als ruhige Falte, in der
> `DD_Toleranz` bindet, und 2020/2022 als Krisenfalten sind der Stand von TB-30a (Falten
> 2019–2025, Tabellen aus Abschnitt 3 bei 50 % Exposure). `test_vorregistrierung.py` Teil D
> prüft seit TB-97 nicht mehr diese Jahre, sondern **die Regel am heutigen Plan**: In der
> **ruhigsten** Selektionsfalte (flachster Benchmark-Drawdown) muss `DD_Toleranz` binden
> (D1), in der **schwersten** die relative Grenze (D2). Gegenproben D1-G/D2-G: vertauscht
> scheitern beide. Beim Plan von TB-97 für `turtle_soup_stocks` sind das **2017** und
> **2020**. Die Werte der Tabelle sind ebenfalls der Stand vom 14.09.: Die heute gelesene
> Tabelle (`ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`) weicht in 2019
> (−3,66 % statt −3,69 %) und 2025 (−8,77 % statt −8,89 %) ab
> (`docs/belege/TB-97/a4_literale.txt`). Die Tabelle oben bleibt zeichengleich.

## 9. G4 — Vorschlag für Registerabschnitt 41 (gemessen, nicht eingetragen)

**41. Die Mutationsproben benannt und mit Gegenprobe, `F4` beisst, die vier Literale aus
Plan und Register, die Sonde liest ihre Gruppen aus dem Abbild (TB-97, 24.09.2026)**

- **41.1 Tatsachennotiz zu 12 und 40.7: die Mutationsproben.** Die Tabelle aus Abschnitt 4
  dieses Dokuments (Name, Teil, Mutation, vorher, nachher). ⚠️ **Sieben**, nicht acht; H0
  ist der Grundlauf; `F4` keine Mutationsprobe. Die Zahl in 12 bleibt zeichengleich. Marke
  bei 12: „davon acht Mutationsproben" lies „sieben Mutationsproben (H1–H7) und der
  Grundlauf H0 (41.1)". **Frage an Fable:** Soll 40.7 („für alle acht") als Berichtigung
  auf „alle sieben" lauten, oder zählt er `F4` bewusst mit? Die Gegenprobe ist für alle
  acht geführt, sieben und `F4`.
- **41.2 `F4`:** `<` statt `<=`, strikte Mehrheit aus dem Plan (5 von 9), Gegenprobe
  `F4-G`. Vollzug von 40.8 (a).
- **41.3 Die vier Literale** (Vollzug von 40.8 (b)): Teil D ruhigste/schwerste Falte,
  Teil F Mehrheit aus dem Plan, `beispieldaten.py` Krisenfalten aus 5.1 Nr. 4 per Abdeckung,
  jede Stelle mit Gegenprobe. ⚠️ **Abweichung von 24a Abschnitt 6 bei `beispieldaten.py`**,
  mit A4 begründet, zur Kenntnisnahme.
- **41.4 Marke bei 5.1 Nr. 4 ergänzen:** „Zweiter Leser seit TB-97: `beispieldaten.py`
  (Krisenfalten der Beispieldaten, `G11`). Der Parser steht einmal, in
  `beispieldaten.jahre_aus_register_5_1_nr_4`; `G6` ruft ihn auf."
- **41.5 Sonde:** getrennte Schlusszeilen (Vollzug 40.8 (d)) und die Gruppen aus dem Abbild
  (Vollzug 40.8 (e), mit Gegenprobe E3). Fehlende Gruppe 2, leere Gruppe 0. Tatsachennotiz:
  Das gültige Abbild (`2f23f76c…`) führt die Gruppen nicht, **ein neues Abbild steht aus**
  (Freigabe). Marken bei 39.3 und 39.9: Die Sonde nennt `_vt.json` nicht mehr, die Gruppe
  kommt aus dem Abbild. Marke bei 39.7: Die „dritte Gruppe" führt die Sonde seit TB-97,
  sofern das Abbild sie trägt.
- **41.6 Tatsachennotiz zu 4.4:** Wortlaut aus Abschnitt 8.
- **41.7 Was NICHT getan wurde:** kein Abbild, kein Registertext, kein Faltenplan,
  `auswertung.py`/`registerdaten.py`/`benchmark.py`/`registerbericht.py` unberührt, keine
  Liste neu erzeugt.

## 10. Was NICHT geschah

Keine Prüfung gelöscht oder abgeschwächt, keine Ausnahme für einen Bot, keine Toleranz.
`faltenplan.py`, `faltenplan.json`, `auswertung.py`, `registerdaten.py`, `benchmark.py`,
`registerbericht.py` und `herkunft.py` nicht angefasst, Hashes gleich. Keine Trade-Liste
erzeugt, keine Faltenlänge abgeleitet. **Kein Abbild in `ergebnisse/`**: Das Probe-Abbild
und die Kopie liegen nur im Scratchpad. Kein Registertext geschrieben. `python3
faltenplan.py` nicht aufgerufen. Keine Zeile mit dem Anfang von 5.1 Nr. 4 geschrieben:
Der Test (`G6`) ist grün, und `grep` über alle geänderten Dateien findet 0 Treffer
(`g5_g6_wache.txt`).

## 11. Für die Folgesitzung vorbereitet

| | |
|---|---|
| **TB-98** | ⭐ Teil D bricht nicht mehr mit `KeyError`, wenn `BOT` Zweijahresfalten bekommt, **solange die Benchmark-Tabelle dem Plan folgt**. Die Faltennamen kommen aus dem Plan und werden als Schlüssel in die Tabelle gelesen. Ändert TB-98 den Plan, ohne die Tabelle neu zu rechnen, bricht Teil D weiter mit `KeyError` (dann ist es eine Berichtigung von 33.2 samt Tabelle, 40.6). `G11` prüft die Krisenfalten je Bot gegen die Tabelle und macht dasselbe sichtbar |
| **Abbild** | Ein neues echtes Abbild mit den Gruppen (`sperrliste_abbild.py --ziel …_JJJJ-MM-TT.json`, ohne `--bestimmt` = Gruppe leer) schliesst die zwei Gruppen-2 der Sonde. Braucht Freigabe. Am sinnvollsten zusammen mit dem Abbild, das TB-98 ohnehin braucht (Punkt 2 bekommt eine Pfadkonstante) |
| **Register** | Abschnitt 41 nach Abschnitt 9 dieses Dokuments, Tatsachennotiz zu 4.4 nach Abschnitt 8. Frage an Fable: sieben oder acht (41.1), Z. 69 (41.3) |
| **Tag** | Die Regelzeile der Sonde zeigt je Punkt „keine im Abbild". Für die Tag-Vorbedingung braucht jeder der zwölf Punkte eine Tatsachennotiz **und** deren Verweis im Abbild (Feld `tatsachennotiz`) |

---

## In einfacher Sprache

Das Prüfprogramm enthält Proben, die absichtlich eine Stelle im Programm verfälschen und
schauen, ob sich das Ergebnis ändert. Diese Sitzung hat zuerst gezählt, welche das sind.
**Es sind sieben, nicht acht, wie das Regelwerk sagt.** Die achte war ein gewöhnlicher
Startlauf. Die Prüfung, die letzte Woche aufgefallen war, weil sie nie anschlagen konnte,
gehörte gar nicht zu diesen Proben.

Dann wurde für jede der sieben gemessen, ob sie anschlagen kann: Man nimmt ihr die
Verfälschung weg, dann muss sie durchfallen. **Alle sieben tun das.** Seit heute macht das
Prüfprogramm diese Gegenprobe bei jedem Lauf selbst. Die Prüfung, die nie anschlug, prüft
jetzt, was ihr Text sagt, und hat ebenfalls eine Gegenprobe.

Vier eingetippte Jahreszahlen sind ersetzt, durch Werte aus dem Abschnittsplan oder aus
dem Regelwerk. Bei einer davon hatte der Verfahrensprüfer gesagt, es genüge irgendein
Abschnitt. **Nachgerechnet stimmt das nicht:** Bei zwei Bots wären die Testdaten dann
unbrauchbar geworden. Genommen sind deshalb die beiden Krisenjahre aus dem Regelwerk. Das
muss er noch zur Kenntnis nehmen.

Die Wache über die geschützten Dateien trug eine eingetippte Liste. Jetzt liest sie alles
aus ihrer Vorlagedatei. **Die heutige Vorlagedatei kennt diese Listen aber noch nicht.**
Eine neue darf nur mit Freigabe geschrieben werden. Bis dahin meldet die Wache ehrlich
„nicht prüfbar", statt still „in Ordnung".
