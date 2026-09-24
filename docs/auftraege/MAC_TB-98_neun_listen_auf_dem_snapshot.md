# TB-98 — Die neun Handelslisten auf dem registrierten Snapshot neu erzeugen, und die Faltenlänge daraus ableiten

**Sitzungstitel:** `TB-98` · **Angelegt:** 24.09.2026 vom steuernden Chat
**Grundlage:** `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md` Abschnitt 3 · **Register 40.6, 40.8 (f)**
**Vorgänger:** TB-97 (`e87b06f`) · **Aufwand:** hoch
⭐ **Betreiberfreigabe 24.09.2026, 11:25 — für die Pfadkonstante in `faltenplan.py` (Sperrlistenpunkt 2, 37.3) und für EIN neues Sperrlisten-Abbild.** ⚠️ **Beides wird in diesem Auftrag NICHT verbraucht** (siehe Zuschnitt); die Freigabe gilt für den Folgeauftrag.

---

## ⭐⭐ Der Zuschnitt — und warum er so ist

Fables Registertext (40.6) verlangt fünf Dinge: neu erzeugen · Sperrlistenpunkt ·
`faltenplan.py` auf eine registrierte Pfadkonstante · Faltenlänge ableiten ·
gegen 33.2 vergleichen. Sein eigener Satz sagt aber auch:

> **Gleich ⇒ Tatsachennotiz. Verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt" — keine Wahl.**

⚠️⚠️ **Der Zweig „verschieden" ändert den Faltenplan — und damit die
Benchmark-Tabelle, das Abbild und Registertext 33.2.** Es wäre verkehrt,
`faltenplan.py` (Sperrlistenpunkt 2) auf die neuen Listen zu verdrahten und ein
neues Abbild zu ziehen, **bevor** man weiss, welcher Zweig gilt.

⇒ **TB-98 erzeugt und misst. Mehr nicht.**

| | |
|---|---|
| ✔ | Erzeuger nach 36.1, Modus-Lauf, neun Listen, Hashes, Notizen |
| ✔ | Faltenlänge je Bot nach 5.4 ableiten und **gegen 33.2 vergleichen** |
| ⛔ | **`faltenplan.py` wird NICHT geändert** — der Folgeauftrag tut das, mit der Freigabe |
| ⛔ | **Kein Sperrlistenpunkt eingetragen, kein Registerabschnitt, kein neues Abbild** |

⭐ *Das ist 24.3 in Anwendung: Die Regel steht (40.6), die Messung kommt, und
erst danach wird gebaut — nicht umgekehrt.*

---

## ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔⛔ | **Die neun alten Listen werden nicht berührt.** Sie bleiben nach 40.6 als historischer Stand liegen. ⚠️ Ihre Hashes werden vor **und** nach jedem Lauf gemessen |
| ⛔⛔ | **`python3 faltenplan.py` wird NIE direkt aufgerufen** — `main()` überschreibt den gesperrten `ergebnisse/faltenplan.json` (TB-83). Nur `import` und `fp.faltenplan(...)` im Speicher |
| ⛔ | **`positionen_holen.py` wird nicht unverändert aufgerufen.** Es schreibt fest nach `daten/` (`DATEN_DIR`, Z. 78/258) und überschriebe die alten Listen |
| ⛔ | Keine Sperrlistendatei ändern, kein Abbild schreiben, `ergebnisse/` unberührt |
| ⛔ | **Keine Trade-Zahlen melden** (27.1). Gemeldet wird die **Faltenlänge** je Bot (1 oder 2), sonst nichts |

---

## 0. Schritt 0

Arbeitsbaum committen (der steuernde Chat legt diesen Auftrag, die Anfrage 24c
und den Zeiger ab). `find .git -name '*.lock'` → keine. HEAD am Eingang:
**`e87b06f`**. ⚠️ **Fehlt Abschnitt 40 im Register, brich ab.**

---

## Block A — Messen, bevor gebaut wird

**A1 — Liest der Erzeuger überhaupt über den Selektionsmodus?**

⚠️⚠️ **Das ist die Frage, an der alles hängt.** TB-92 hat gemessen, dass
`benchmark.py` und `messgroessen.py` **an `shared/paths.py` vorbei** lesen. Wenn
`positionen_holen.py` das auch tut, greift `TB_SELEKTIONSWURZEL` nicht, und ein
Lauf „im Modus" läse trotzdem `data/`.

Miss statisch **und** dynamisch:

| | |
|---|---|
| statisch | Woher bezieht `positionen_holen.py` (und was es importiert) seine Kursdaten — `get_strategy_paths()`, eine eigene Variable, ein fester Pfad? Nenne Datei, Zeile |
| dynamisch | Lesehaken wie in TB-92/TB-95 (`sys.addaudithook`, `sitecustomize` für Kindprozesse), **ein** Probelauf für **einen** Bot in den Scratchpad. Protokolliere jede geöffnete Datei mit Aufrufstapel |

⭐ **Ergebnis:** Kommen die Kursdaten aus `snapshots/63e4b6c8…/` oder aus `data/`?
⚠️ **Wenn aus `data/`: Das ist ein Befund derselben Klasse wie bei `benchmark.py`
— melden, und den Erzeuger so bauen, dass er den Snapshot-Pfad explizit
übernimmt.** Nicht stillschweigend weiterrechnen.

**A2 — Was genau erzeugt die Liste.** `positionen_holen.py` schreibt drei Dateien
je Bot (`_positionen.csv`, `_alle_trades.csv`, `_meta.json`). **Nur
`_alle_trades.csv` geht in den Faltenplan** (`faltenplan.py` Z. 132). Miss,
welche Spalten es trägt und welche davon gelesen werden (TB-95: nur
`entry_time`).

**A3 — Der Parameterstand.** Hashes der neun `live_params.py`, der Bot-Dateien
und aller Module, die der Erzeuger lädt. ⭐ Das ist die Tatsachennotiz, die
Fables Unsicherheit verlangt (40.6).

**A4 — Hashes und Sonde am Eingang**, wie in TB-96/TB-97 (28 Pfade plus die neun
alten Listen). Sonde gegen `sperrliste_abbild_2026-09-23.json`.

Belege: `a1_lesequellen.txt`, `a2_spalten.txt`, `a3_parameterstand.txt`,
`a4_hashes_vorher.txt`, `a4_sonde_vorher.txt`.

---

## Block B — Der Erzeuger nach 36.1

⭐ **Bauart:** `positionen_holen.py` bekommt ein **Pflicht-Argument `--ziel`**
(Ordner) und die Einmal-Schreibsperre. ⛔ **Keine Voreinstellung** — wie
`sperrliste_abbild.py` es vormacht.

| | |
|---|---|
| **B1** | `--ziel` ist **Pflicht**. Ohne Argument bricht der Erzeuger ab, rc ≠ 0, schreibt nichts. ⭐ *Damit ist die Überschreibgefahr aus 40.6 dauerhaft weg, nicht nur für diesen Lauf* |
| **B2** | Je Zieldatei `O_CREAT\|O_EXCL`. Existiert sie, Abbruch mit rc ≠ 0, Pfad und Hash der vorhandenen Datei genannt, **nichts geschrieben, nichts gerechnet** — die Sperre greift **vor** der Rechnung (wie `messgroessen.py` seit TB-93) |
| **B3** | ⛔ **Die Rechenwege bleiben unverändert.** AST-Vergleich aller Funktionen gegen den Stand `e87b06f`: **nur** die Zielbestimmung darf sich unterscheiden. Beleg wie TB-92 A1a-4 |
| **B4** | `alle_bots.py` reicht `--ziel` durch |
| **B5** | ⭐ Der Erzeuger schreibt neben die Listen eine **Herkunftsnotiz**: Snapshot-Hash, Code-Commit, Modus, Zeit, und je Liste den Hash. Sichtschutz: keine Trade-Zahlen |

⚠️ **Prüfe vor dem Bauen, ob `positionen_holen.py` auf einer Sperrliste steht
oder in `EINGEFROREN`.** Nach heutigem Stand nicht — aber miss es, statt es
anzunehmen. Steht es drauf, **abbrechen und melden**.

---

## Block C — Der Lauf

**C1 — Neun Listen erzeugen**, im Selektionsmodus gegen
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/`,
`--ziel` auf einen **neuen** Ordner (Vorschlag:
`research/tb24_haltedauern/daten_2026-09-24_snapshot/`).

| | |
|---|---|
| ⚠️ | **Vor und nach dem Lauf:** Hashes der neun alten Listen. ⛔ Ändert sich einer, **sofort abbrechen** |
| ⚠️ | Laufzeit unbekannt. Läuft es länger als ~45 min, melde den Zwischenstand, statt es abzuwürgen |

**C2 — Der Reproduzierbarkeitsnachweis (23e): zweimal, bytegleich.** Zweiter Lauf
in den Scratchpad, `diff` je Liste gegen den ersten. ⭐ **Das ist der Nachweis,
den Fables Regel verlangt — und der Grund, warum sie trägt, obwohl TB-90 ihn
nicht erbracht hat** (Anfrage 24b, Abschnitt 2).

⚠️ **Nicht bytegleich ⇒ Befund.** Ursache ausmessen (Zeitstempel im Inhalt?
Reihenfolge? Zufall?), melden, ⛔ **nicht wegrechnen**.

**C3 — Vergleich gegen die alten Listen.** ⚠️ **Nur Ja/Nein je Bot** — sind die
neuen Listen byteweise gleich den alten? Sichtschutz 27.1: ⛔ keine Zeilenzahlen,
keine Trade-Zahlen. Erwartet: verschieden, weil die Krypto-Historie seit TB-31/34
weiter zurückreicht. **Aber erwartet ist nicht gemessen.**

Belege: `c1_erzeugung.txt`, `c2_determinismus.txt`, `c3_vergleich.txt`.

---

## Block D — ⭐⭐ Die Ableitung und der Vergleich gegen 33.2

**D1 — Faltenlänge je Bot nach 5.4 aus den NEUEN Listen.**

⚠️ **Rechne mit dem registrierten Weg, nicht mit einem eigenen:** `faltenplan.py`
im Speicher, `faltenlaenge_jahre` — aber mit dem neuen Datenordner. ⛔ **Ohne
`faltenplan.py` zu ändern** (die Freigabe gilt für den Folgeauftrag): Leite den
Pfad für diesen Lauf um, ohne die Datei zu schreiben. ⭐ Wie, ist Handwerk;
**schreib auf, wie du es gemacht hast**, und weise nach, dass `faltenplan.py`
danach denselben Hash hat.

Die Regel steht in 5.4: gefundene Trades je **vollem** Kalenderjahr, angeschnittene
Randjahre weg, Mittel gegen die Schwelle **30** (Festlegung 7).

**D2 — Gegen 33.2 vergleichen.** Je Bot: Faltenlänge aus den neuen Listen gegen
die registrierte in 33.2.

| Ausgang | was zu tun ist |
|---|---|
| ⭐ **9/9 gleich** | Tatsachennotiz. Der Folgeauftrag trägt sie ein, verdrahtet `faltenplan.py` und zieht das Abbild |
| ⚠️⚠️ **Einer oder mehr verschieden** | ⛔ **STOPP. Nichts verdrahten, nichts eintragen.** Melden: **welche Bots**, alt → neu, und **was daran hängt** (Faltengrenzen, Zellenzahl, N, Benchmark-Tabelle). Fable hat entschieden: Berichtigung, keine Wahl — aber ihr Umfang ist eine eigene Sitzung |

⚠️ **Gemeldet wird die Faltenlänge (1 oder 2), nicht die Zählung** — Fable
ausdrücklich: *„ich brauche danach nur das Ob je Bot"* (27.1 nennt „Anzahl
Trades").

**D3 — Die Folgen ausmessen, falls D2 abweicht.** Ohne etwas zu ändern: Welche
Falten bekäme der betroffene Bot? Ändert sich seine **Zellenzahl**? Ändert sich
**N** (Festlegung 10, heute 653)? ⭐ *Das ist die Vorarbeit, die dem
Folgeauftrag stundenlange Sucherei erspart — und Fable die Grundlage für den
Umfang der Berichtigung.*

Belege: `d1_ableitung.txt`, `d2_vergleich_33_2.txt`, `d3_folgen.txt`.

---

## Block E — Abgabe

| | |
|---|---|
| **E1** | Hashes nachher. ⛔ **Nur `positionen_holen.py` und `alle_bots.py` dürfen sich bewegt haben.** Die neun alten Listen, alle Sperrlistendateien, beide Abbilder, `faltenplan.py`, `faltenplan.json`, alle Tabellen: gleich |
| **E2** | Sonde gegen `sperrliste_abbild_2026-09-23.json`: unverändert 0 Befunde |
| **E3** | Ergebnisdokument `docs/ERGEBNIS_TB-98_neun_listen_auf_dem_snapshot.md` |
| **E4** | ⭐⭐ **Ein Abschnitt „Für Fable"**, der ohne Kontext lesbar ist: A1 (liest der Erzeuger über den Modus?), C2 (zweimal bytegleich?), **D2 (9/9 gleich oder nicht, je Bot 1 oder 2)**, und D3 falls nötig. ⚠️ Sichtschutz 27.1 |
| **E5** | Der Wortlaut für die **Tatsachennotiz zu 5.4** (Snapshot-Hash, Code-Commit, Modus, je Liste Hash, Parameterstand aus A3) — gemessen, nicht eingetragen |
| **E6** | „In einfacher Sprache" · „Für die Folgesitzung vorbereitet" · Journalblock |

**Commits:** (1) Schritt 0 · (2) Block B (Erzeuger) · (3) Block C+D (Listen,
Belege) · (4) Abgabe.

---

## ⚠️ Abbruchkriterien

1. Abschnitt 40 fehlt im Register.
2. **Der Hash einer alten Liste ändert sich** — sofort, alles stehen lassen.
3. `positionen_holen.py` steht doch auf einer Sperrliste oder in `EINGEFROREN`.
4. **C2 nicht bytegleich** — Ursache ausmessen, melden, nicht weiterbauen.
5. **D2 weicht ab** — Block D3 noch ausführen, dann Schluss. ⛔ Nichts verdrahten.
6. Eine Sperrlistendatei oder ein Abbild ändert sich.
7. `faltenplan.py` hat am Ende einen anderen Hash als am Anfang.

⭐ *4 und 5 sind keine Fehler, sondern Ergebnisse. Der Auftrag ist auch dann
abgearbeitet — nur dann nicht, wenn sie verschwiegen oder weggerechnet werden.*

---

## In einfacher Sprache

Neun Handelslisten vom 13. September entscheiden, ob ein Bot ein- oder
zweijährige Zeitabschnitte bekommt. Sie stammen aus der Zeit vor der Erweiterung
der Krypto-Daten und gehören nicht zum eingefrorenen Datenbestand. Der
Verfahrensprüfer hat entschieden, dass sie daraus **neu erzeugt** werden müssen.

Dieser Auftrag tut zwei Dinge. **Erstens** baut er das Erzeugerprogramm so um,
dass es nur noch in einen ausdrücklich genannten neuen Ordner schreibt und
niemals eine vorhandene Datei überschreibt — heute würde ein Aufruf die alten
Listen zerstören. **Zweitens** erzeugt er die neun Listen aus dem eingefrorenen
Bestand, zweimal, und prüft, dass beide Läufe Byte für Byte dasselbe ergeben.

Dann kommt die eigentliche Frage: Ergibt sich daraus dieselbe Abschnittslänge
wie im Regelwerk? Wenn ja, wird das nur vermerkt. Wenn nein, ändert sich der
Zeitplan eines Bots — und damit die Vergleichstabelle und der Umfang des ganzen
Suchraums. **Das wäre eine eigene Sitzung.** Deshalb hört dieser Auftrag genau
dort auf: Er misst und meldet, er baut nichts um, was von der Antwort abhängt.

Die eine Messung, die vorher kommt, ist die unauffälligste: **Liest das
Erzeugerprogramm den eingefrorenen Bestand überhaupt?** Bei zwei anderen
Programmen hat sich gezeigt, dass sie am dafür vorgesehenen Weg vorbeilesen.
Wäre es hier auch so, liefe alles Weitere auf den falschen Daten.
