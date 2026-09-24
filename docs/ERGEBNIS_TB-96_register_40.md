# TB-96 — Ergebnis: Registerabschnitt 40 nach Fable 24a — Test grün als Tag-Vorbedingung, die Kopplung von `G6` an 5.1 Nr. 4, die neun Handelslisten als Eingabedateien nach 23d, jede Mutationsprobe mit Gegenprobe

**Sitzungstitel:** `TB-96` · **Stand:** 24.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-96_register_40.md` · **Belege:** `docs/belege/TB-96/`
**Eingang:** `2938145` (TB-95-Abgabe) · Commits: `fc8d44c` (Schritt 0), **`d0dc890`**
(Block B und C in einem Commit), Abgabe-Commit (Belege D1–D3, dieses Dokument,
Journalblock CX).
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`.
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** Abschnitt 40 steht im Register (40.1–40.10), dazu ein Nachtrag am Ende von
**39.8** und **neun Marken** am alten Ort, zusammen zehn Stellen. `numstat` **463/0**, im
Gesamtdiff **0** entfernte Zeilen. Alle **30 Zitate** sind eingesetzt statt abgetippt und
per `diff` geprüft: 30 × rc 0. Gerechnet wurde nichts und keine `.py` geändert. Alle 28
gemessenen Hashes sind vorher und nachher gleich, und ausserhalb von `docs/` hat sich
nichts bewegt. Die Sonde meldet vorher und nachher 0 Befunde. Einzige Änderung in ihrer
Ausgabe: Abschnitt 10 steht jetzt 23 Zeilen tiefer.

**Alle sechs Vormessungen stimmen.** Dazu kommen **drei eigene Funde**:

- Fables Satz „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren" trifft
  auf den Erzeuger der Listen nicht zu (Abschnitt 6, Punkt 1).
- Der Erzeuger der Listen überschreibt die alten Listen, wenn man ihn unverändert aufruft.
- Die Nummer von `messgroessen.json` ist erneut gerückt, von TB-96 auf **TB-101**.

---

## 0. Schritt 0 und Freigabe

| | |
|---|---|
| Arbeitsbaum | sechs Dateien des steuernden Chats (Fable 24a Anfrage und Antwort, `ARBEITSWEISE.md` 22.5–22.7, `starte_sitzung.sh`, Zeiger, dieser Auftrag) → **`fc8d44c`**; danach leer |
| Git-Sperrdateien | `find .git -name '*.lock'` → keine |
| ⭐ Freigabe | `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md` liegt im Repo (87 Zeilen) — Abbruchkriterium 1 greift nicht |

## 1. Block A — gemessen vor dem Schreiben (`a_messungen.txt`)

| | Vormessung | gemessen | |
|---|---|---|---|
| **A1** | Register endet bei 39.10, nächster Abschnitt 40 | ✔ letzte Überschrift `### 39.10` (Z. 7511), kein `40`, 7530 Zeilen | gleich |
| **A2** | `73c9b837…`, `9e2a071` | ✔ | gleich |
| **A3** | Sperrliste und Abbilder unverändert, Sonde 0 / 15/15 / (ii) 0 / Ausgang 2 | ✔ alle 28 Hashes aus `docs/belege/TB-95/c_hashes.txt` gleich (`diff` rc 0); Sonde 0 Befunde, 15/15, (ii) 0, rc 2 | gleich |
| **A4** | Schwelle registriert: Festlegung 7 (Z. 62), 5.1 Nr. 6 (Z. 574), `rd.ZWEIJAHRES_SCHWELLE_TRADES` | ✔ alle drei; in `faltenplan.py` **0** Vergleiche mit einem Literal `30` | gleich |
| **A5** | 5.4 nennt den Parameterstand nicht | ✔ 5.4: 0 Treffer für „heutige Parameter", `live_params`, `78e2bc6` im ganzen Register 0. **Dazu gemessen:** Der TB-24-Bericht sagt „mit den heutigen `live_params.py`" (Stand 13.09.). Die `<bot>_meta.json` enthalten **keine** Strategieparameter. Die neun `live_params.py` haben sich seit `78e2bc6` nur in **drei Kommentarzeilen** geändert, **keine Zuweisung** | gleich, ergänzt |
| **A6** | `G6` liest 5.1 Nr. 4 maschinell | ✔ Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`, **zeilenweise am Zeilenanfang verankert**, genau ein Treffer (Z. 565), `_testjahre_aus_register()` = `[2020, 2022]`. ⚠️ **Zusätzlich gemessen:** Auch eine **zweite** Zeile mit diesem Anfang, irgendwo im Register, macht `G6` rot | gleich, ergänzt |

⇒ Abbruchkriterium 6 greift nicht. 40.2 folgt dem Gemessenen, einschliesslich der
Zweitzeilen-Gefahr. Deshalb steht in TB-96 **jedes** Zitat dieser Zeile eingerückt oder
in Backticks. Das Einsetzskript prüft das vor dem Schreiben selbst: Mit dem Muster aus
`G6` muss es genau einen Treffer finden.

## 2. Block B — Nachtrag zu 39.8

Am Ende von 39.8, **nach** dem letzten Satz („… nicht für diesen Eintrag."), 27 Zeilen.
39.8 selbst ist zeichengleich geblieben. Inhalt:

- **Wer die Listen öffnet:** `benchmark.py::je_bot` → `faltenplan.py::faltenplan` →
  `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr`. Jede Liste wird genau
  einmal geöffnet, nur im Hauptprozess.
- **Ob sie eingehen:** Ja, aber nur über die Faltenlänge.
- **Störprobe in beide Richtungen:** Eine Zeile weg ⇒ bytegleich. Zwei von drei weg ⇒
  ein Bot kippt, die anderen acht bleiben gleich.
- **Herkunft:** `78e2bc6`, 13.09.2026, TB-24. Die Listen liegen nicht im Snapshot und
  stehen nicht auf der Sperrliste. 5.4 nennt sie als Quelle, ohne Hash.
- **Der methodische Satz:** Die Probe „eine Zeile genügt" hätte allein das falsche „nein"
  ergeben.
- **Ende:** Der Nachtrag verweist auf 40.6. Er endet also nicht mit „Einordnung steht aus".

⚠️ **Nicht von Fable:** Den Satz „Eine Störprobe nach ‚geht es ein?' wird in **beide**
Richtungen geführt …" hat die Sitzung formuliert. Er verallgemeinert den Satz aus dem
Auftrag und ist **kein** Registertext des Verfahrensprüfers. Er gehört zur nächsten
Vorlage bei Fable (Abschnitt 7).

## 3. Block C — Abschnitt 40 und die Marken

| | Inhalt | Fable-Zitate |
|---|---|---|
| Kopf | Herkunft, Regel aus 34, zehn Stellen | Z. 9 |
| **40.1** | Test 165/165, rc 0 ⇒ Tag-Vorbedingung für diesen Test erfüllt. ⚠️ Zusatz: Das gilt für den heutigen Stand. Die Änderungen aus 40.8 müssen den Test wieder grün hinterlassen | Z. 11 |
| **40.2** | `G6` wie gebaut; gemessen war die Sache erfüllt, rot war nur die Formulierung. ⭐⭐ **Die Kopplung** mit beiden Folgen: umformulieren **oder** eine zweite Zeile ⇒ rot | — |
| **40.3** | `H3`: strikte Mehrheit, ⌈n/2⌉, Probe beisst, Gegenprobe scheitert. Fables Einordnung | 2 Teilzitate aus Z. 11 |
| **40.4** | Die vier Literale als Tabelle, Zeilennummern nur mit Commit (38.2), dazu `F4` | Z. 49, Z. 57 |
| **40.5** | entfällt, Verweis auf den Nachtrag in 39.8 | Z. 45 |
| **40.6** | ⭐⭐ Registertext 23d/5.4, Grund, Einwand, beide Umstände, Quelle, Folge für 5.4. Dazu Fables Unsicherheit und die **Tatsachennotiz zu 5.4** aus A4/A5. **Zwei weitere Tatsachennotizen:** TB-90 B6 (Abschnitt 6, Punkt 1) und der Erzeuger ohne `--ziel`. Dann die Folge für den Plan: Punkt 7 rückt vor, das Abbild entsteht nach der Ableitung | Z. 33, 29, 31, 35, 39, 37, 41, 81 |
| **40.7** | ⭐ Registertext zu 12, Quelle, Anlass `F4`. ⚠️ **Welche acht Prüfungen die „acht Mutationsproben" sind, ist nicht gemessen** | Z. 51, Z. 53 |
| **40.8** | Tabelle (a)–(h), Aufträge TB-97/98/100/101, Reihenfolge (b) vor (f) und (g) nach (f); TB-99 reserviert | Z. 59, Z. 63, Z. 65 |
| **40.9** | Die drei Berichtigungen, jeweils mit Fables Annahme. ⚠️⚠️ **(c) ist erneut gerückt:** Für `messgroessen.json` gilt jetzt TB-101. Der vierte Fall (TB-90) ist vorgelegt, nicht berichtigt | 3 Teilzitate, Z. 15, 17, 19, 21 |
| **40.10** | Was nicht getan wird; offen | — |

**Marken — neun, jeder Zielabschnitt vorher gelesen; dazu der Nachtrag in 39.8:**

| Ort | Marke | Form |
|---|---|---|
| **5.1 Nr. 4** | ⭐⭐ `G6` liest diese Zeile maschinell, Wortlaut nicht ändern | eingerücktes Blockzitat im Listenpunkt, Leerzeile davor und danach, damit „5." ein Listenpunkt bleibt |
| **5.4** | Listen sind Eingabedateien, werden neu erzeugt; Parameterstand fehlt; Regeltext bleibt | Blockzitat nach „Abschnitt 3." |
| **12** | Jede Mutationsprobe hat eine Gegenprobe; heute 165 Prüfungen | Blockzitat nach dem Absatz über den Schalter |
| **21.9** | Tag-Vorbedingung erfüllt, erste Zeile der Tabelle für den 23.09. geschlossen | nach der TB-94-Marke |
| **33.2** | Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen; verschieden ⇒ Berichtigung | nach der TB-94-Marke |
| **33.5** | Plan-Punkt 7 rückt vor; das Abbild entsteht **nach** der Ableitung | unter der Tabelle |
| **36.6** | Die Sonde liest alle drei Gruppen aus dem Abbild | `> >` im Registertext-Zitat, wie 37.2/37.3 |
| **37.2** | Die feste Konstante ist ein Befund, der vor dem Tag behoben werden muss (TB-97) | nach der TB-94-Marke |
| **39.6** | zweiter Anwendungsfall von 23d; Nummer `messgroessen.json` → TB-101 | nach der Tatsachennotiz |

⚠️ **Eine Marke ging nicht wörtlich an den Ort aus dem Auftrag:**
„**23d**-Abschnitt im Register". Einen Abschnitt 23d gibt es im Register nicht; 23d ist
eine Antwortdatei von Fable. Der Auftrag nennt als Ort selbst 39.6, „wo die Notiz ‚nicht
eingetragen' steht", und genau dort steht die Marke.

Keine Marke weggelassen.

## 4. Block D — Nachweise

**D1** (`d1_numstat.txt`), zeichengleich:

```
$ git --no-optional-locks log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md
d0dc890eb0e804019a8e4410184107c9c9f89926 TB-96 Block B und C: …

463	0	docs/VORREGISTRIERUNG_neuselektion.md
$ git diff fc8d44c d0dc890 -- docs/VORREGISTRIERUNG_neuselektion.md | grep -c '^-[^-]'   (entfernte Zeilen)
0
```

Elf Hunks, alle `-n,0`, also reine Einfügungen: zehn Stellen und der neue Abschnitt am
Ende. Das Register hat jetzt **7993** Zeilen (vorher 7530).

**D2** (`d2_zitate.txt`): **30 Zitate**, 22 ganze Zeilen und 8 Teilzitate, **30 × `diff`
rc 0**. Die Quellzeile und die Registerzeile liest das Skript jeweils unabhängig aus der
Datei. Teilzitate müssen wortgleich in der Quellzeile **und** an ihrer eigenen
Fundstelle im Register stehen, nicht in einem Vollzitat derselben Zeile. Das Einsetzen
erledigt `eintrag_register_40.py`: Es liest die Quelle, setzt die Platzhalter
`⟦Z:n⟧`/`⟦T:n|…⟧` und bricht ab, wenn eine Ankerzeile im Zielabschnitt nicht genau einmal
vorkommt oder `G6` danach nicht genau einen Treffer fände.

**D3** (`d3_hashes.txt`, `d3_sonde.txt`):

| | |
|---|---|
| Hashes | 28 Pfade: Sperrlistendateien, beide Abbilder, `faltenplan.json`, alle Benchmark-Tabellen, `herkunft.py`, `beispieldaten.py`, `messgroessen.py`, `kennzahlen.py`, `sperrlistensonde.py`, `sperrliste_abbild.py`, `test_vorregistrierung.py` und die neun Listen. **vorher = nachher** (rc 0) und **= TB-95 nachher** (rc 0) |
| ausserhalb `docs/` | `git diff --name-only 2938145 HEAD` ohne `docs/`: **0**; `git status` ohne `docs/`: **0** |
| Sonde vorher / nachher | beide **0 Befunde**, 15/15 gleich, (ii) `0`, Bilanz 2/0/12, rc **2**. Unterschied **nur** in der Angabe „Z. 845–958" → „Z. 868–981": Die Marken in 5.1 (10 Zeilen) und 5.4 (13 Zeilen) stehen vor Abschnitt 10. Die Sonde vergleicht den **Listentext** („wie bei Erzeugung: ja"), nicht die Zeilennummern (gemessen am Code, `lies_abschnitt_10`/`listentext_wie_bei_erzeugung`) |
| `G6` nach dem Eintrag | `_testjahre_aus_register()` = `[2020, 2022]` (Funktion des Tests, nicht der ganze Test) |

⛔ Der Test selbst ist **nicht** erneut gelaufen, weil der Auftrag nichts rechnen lässt.
Die einzige Stelle, an der der Eintrag ihn berühren konnte, ist `G6`, und die ist oben
nachgewiesen.

## 5. Was NICHT geschah

Keine `.py` ausserhalb von `docs/belege/TB-96/` geändert. Die zwei Skripte dort sind
Werkzeuge dieser Sitzung. Nichts gerechnet, nichts in `ergebnisse/` geschrieben, kein
neues Abbild; das gültige bleibt `sperrliste_abbild_2026-09-23.json` (`2f23f76c…`).
Kein alter Registersatz geändert. `positionen_holen.py`, `alle_bots.py`, `faltenplan.py`
und `benchmark.py` nicht aufgerufen.

## 6. Abweichungen und Befunde, zusammengefasst

| | |
|---|---|
| 1 ⚠️ | **Fables Voraussetzung „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren"** (24a Abschnitt 3) stützt sich auf **TB-90 B6**. B6 hat die Backtest-Skripte der Bots **vor und nach dem Kostenmodul** verglichen (`cmp` 9/9), am selben Tag und auf `data/`. Der Erzeuger der **TB-24-Listen** (`alle_bots.py` → `positionen_holen.py`, gefundene Trades) war nicht beteiligt, und auf dem Snapshot lief nichts. Die Regel trägt trotzdem, weil sie ihren eigenen Modus-Nachweis verlangt (zweimal bytegleich, 23e). **In 40.6 und 40.9 als Tatsachennotiz vorgelegt, nicht berichtigt.** Das ist dieselbe Klasse wie die drei angenommenen Fälle |
| 2 ⚠️⚠️ | **`positionen_holen.py` schreibt fest nach `research/tb24_haltedauern/daten/`** (`DATEN_DIR`, `to_csv`, kein Schalter). Ein unveränderter Aufruf **überschriebe die alten Listen**, die nach Fables Registertext liegen bleiben sollen. Für TB-98 ist deshalb ein Erzeuger nach 36.1 Voraussetzung (40.6) |
| 3 ⚠️ | **Nummer:** Nach 39.8 hiess es „`messgroessen.json` = TB-96". Jetzt ist **TB-96 Abschnitt 40**, und `messgroessen.json` ist **TB-101**. In 40.9 (c) und an der Marke 39.6 festgehalten; 39.6/39.8/39.10 bleiben zeichengleich |
| 4 | **A6 ergänzt:** Nicht nur Umformulieren, auch eine **zweite** Zeile mit demselben Anfang macht `G6` rot. Das steht in 40.2 und in der Marke |
| 5 | **A5 ergänzt:** Ausserhalb des Registers steht der Parameterstand im TB-24-Bericht („heutige `live_params.py`", 13.09.). Die Werte der neun `live_params.py` sind seit `78e2bc6` unverändert (nur Kommentare). Nicht gemessen ist der übrige Code (Bots, Simulation, TB-38, TB-90) |
| 6 | **40.7:** Abschnitt 12 nennt „acht Mutationsproben", aber keine Namen. Welche acht es sind, ist **nicht** gemessen; die Liste gehört in die Tatsachennotiz von TB-97 |
| 7 | **Zeilennummern im Auftrag** (Festlegung 7 Z. 62, 5.1 Nr. 6 Z. 574, 5.1 Nr. 4 Z. 565) waren am Eingang richtig. Seit `d0dc890` liegt 5.1 Nr. 6 **10 Zeilen** tiefer (Z. 584, wegen der Marke unter Nr. 4). 5.1 Nr. 4 steht unverändert in Z. 565, Festlegung 7 unverändert in Z. 62 |
| 8 | Das `H3`-Zitat in 40.3 ist **ohne** Auslassungszeichen gesetzt, als zusammenhängender Ausschnitt aus Z. 11 einschliesslich „(vier reichten bei sieben, nicht bei neun)". Der Auftrag hatte die Stelle mit „…" gekürzt |

## 7. Für die Folgesitzung vorbereitet (gemessen, nicht eingetragen)

| | |
|---|---|
| **TB-97** | (1) Die **Liste der acht Mutationsproben** aus Abschnitt 12 zuerst im Test benennen (Namen, Teil), erst dann Gegenproben. (2) `F4`: Die Mehrheit folgt aus der Faltenzahl wie bei `H3` (`len(sel)//2 + 1`), Gegenprobe mit leerer Menge. (3) Die Sonde führt heute `BESTIMMT_NICHT_EINGETRAGEN` mit `_vt.json`, das Abbild führt „bestimmt" nicht als eigenes Feld (39.3). Die Gegenprobe braucht ein **Kopie**-Abbild mit erfundenem Pfad, nie ein neues echtes Abbild. (4) ⚠️ Jede Änderung an `test_vorregistrierung.py` hält die Marke bei 5.1 Nr. 4 ein |
| **TB-98** | (1) Ein neuer Erzeuger nach 36.1 (`--ziel`, Einmal-Schreibsperre) statt `positionen_holen.py`, das fest in `daten/` schreibt. Er muss **im Modus** vom Snapshot lesen (`TB30A_BASE_DIR`-Muster, 39.6) und die Lesequellen protokollieren. (2) Fables Registertext verlangt, dass `faltenplan.py` die neuen Listen **über eine registrierte Pfadkonstante** liest. `faltenplan.py` ist Sperrlistenpunkt 2. Das ist ein Hash-Übergang nach 37.3 (Auftrag, Freigabe, alter und neuer Hash) und braucht ein **neues Sperrlisten-Abbild**. (3) ⚠️ **`python3 faltenplan.py` nie direkt aufrufen**, weil `main()` den gesperrten `faltenplan.json` überschreibt (TB-83). (4) Die Tatsachennotiz zu 5.4 nennt je Bot die Hashes der Parameterdateien, den Code-Commit, den Snapshot-Hash, den Modus und den Hash der Liste. (5) Gemeldet wird nur die Faltenlänge je Bot, keine Trade-Zahlen (27.1). (6) Vergleich gegen 33.2: gleich ⇒ Notiz; verschieden ⇒ Berichtigung, keine Wahl |
| **TB-100** | erst nach TB-98 |
| **TB-101** | `messgroessen.json`; die Nummer im Register steht in 39.6/39.8/39.10 noch als TB-96 (siehe 40.9 (c)) |
| Fable | Vorzulegen: der vierte Fall (TB-90 B6, Abschnitt 6, Punkt 1) und der methodische Satz im Nachtrag zu 39.8 (Block B) als möglicher Registertext |
| Kopf von Abschnitt 10 | nennt als Abbild weiter `…_2026-09-22.json` (Kandidat aus TB-94, unverändert offen) |

---

## In einfacher Sprache

Der Verfahrensprüfer hatte geantwortet, und diese Sitzung hat seine Antwort ins
Regelwerk eingetragen. Umgeschrieben wurde dabei nichts, nur angefügt: 463 neue Zeilen,
keine gelöschte, und jedes seiner Zitate ist maschinell mit dem Original verglichen.

**Drei Dinge stehen jetzt fest:**

- Das Prüfprogramm ist grün. Damit ist eine Bedingung für den Stichtag erfüllt.
- Die neun alten Handelslisten, aus denen berechnet wird, ob ein Bot ein- oder
  zweijährige Abschnitte bekommt, werden aus dem eingefrorenen Datenbestand neu erzeugt.
  Danach wird die Abschnittslänge neu abgeleitet und mit dem Regelwerk verglichen. Ob
  dabei etwas anderes herauskommt, weiss niemand, und genau deshalb steht die Regel
  vorher fest.
- Jede Gegenprobe im Prüfprogramm braucht selbst eine Gegenprobe.

**Neu gefunden:** Das Prüfprogramm liest eine Zeile des Regelwerks wörtlich. Wer sie
umformuliert, oder wer irgendwo eine zweite Zeile mit demselben Anfang schreibt, macht
das Programm rot. An dieser Zeile steht jetzt ein Warnhinweis.

**Zwei Dinge für die nächsten Aufträge:**

- Das alte Programm, das die Handelslisten erzeugt hat, würde die alten Listen beim
  nächsten Aufruf überschreiben. Für die Neu-Erzeugung braucht es daher ein Programm,
  das in eine neue Datei schreibt.
- Der Verfahrensprüfer hatte angenommen, die Reproduzierbarkeit dieser Listen sei schon
  gezeigt. Gezeigt war sie nur für verwandte Programme. Die Regel verlangt aber ohnehin
  einen eigenen Nachweis, deshalb ändert das an der Entscheidung nichts. Es wird ihm
  vorgelegt.
