# TB-114 — Register 45 (Fable 26a, R1–R8), dritte Öffnung von `herkunft.py`: eine Pfadregel mit der Sonde, die neun TB-24-Listen in `EINGEFROREN`, `datenstand(None)` endet mit 2; neues Abbild

**Sitzungstitel:** `TB-114` · **Angelegt:** 26.09.2026, 16:35, vom steuernden Chat
**Vorgänger:** TB-113 (`0df8c64`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md` (md5 `e2a49216…`, 22 331 Bytes, vom steuernden Chat übertragen, wird in Schritt 0 committet)

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 16:30, Auswahlkarte im steuernden Chat:** *„Was soll TB-114 umfassen? … Der Baustein R3 (die neun Handelslisten mit Prüfsumme festhalten) geht heute nicht. herkunft.py sucht jeden Pfad im Ordner research/vorregistrierung, die Prüfsonde ab dem Repo-Stamm. … Das lässt sich nur mit einer Code-Änderung lösen.“* ⇒ **„Regelwerk + Umsetzung (Empfohlen)“** — *„Abschnitt 45 mit R1–R8 wörtlich; herkunft.py öffnen: dieselbe Pfadregel wie die Sonde, die neun Listen aufnehmen, datenstand(None) endet mit 2; neues Abbild, alles nachgemessen“*

| freigegeben | Pfad / Handlung |
|---|---|
| ✔ | `docs/VORREGISTRIERUNG_neuselektion.md`: Abschnitt 45 **anhängen**, Marken additiv |
| ✔ | `research/vorregistrierung/herkunft.py`: **nur** B1, B3, B4 unten (dritte planmässige Öffnung) |
| ✔ | Testdateien, soweit sie eine Anzahl oder Liste von `EINGEFROREN` fest kodieren (Grundsatz 40: Testannahmen folgen dem Register), dazu neue Proben für B1 und B4; jede Änderung einzeln im Ergebnis |
| ✔ | ein **neues** Abbild unter neuem Dateinamen in `research/vorregistrierung/ergebnisse/` (erzeugt mit `sperrliste_abbild.py`) |
| ✔ | `docs/projektfuehrung/JOURNAL.md` (Block **DM**), `docs/belege/TB-114/`, `docs/ERGEBNIS_TB-114_…md` |

⛔ **Nicht freigegeben:**
- jede andere Code-Änderung, besonders `shared/sperrlistensonde.py`, `auswertung.py` (der Docstring aus R8 (a) bleibt bis zu dessen nächster Öffnung), `paths.py`;
- das Überschreiben eines vorhandenen Abbilds;
- jede Marke im Listentext von Abschnitt 10;
- ein Eintrag in Register 9 (der Verweis aus R8 (d) kommt **nach** dem Tag);
- `crontab`, Datenbanken.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger TB-114 |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md` | neu; md5 `e2a492165d44f6ee3d02eba99d2acf2c` prüfen |

Liegt eine weitere uncommittete Datei vor: **melden, nicht mitcommitten.** Commit-Text „TB-114 Schritt 0: Auftrag, Zeiger, Fable-Antwort 26a“, dann Push.

**0b — Ausgangswerte messen** (`0b_ausgang.txt`):
- `register()` (erwartet `a0e477fd…`);
- Hash `herkunft.py` (erwartet `5bbfc9e0…`);
- Sonde gegen `sperrliste_abbild_2026-09-26.json` `e655c1c8…` (erwartet 25/0/0, (ii) 0);
- die neun Dateien `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`: versioniert (`git ls-files`), je sha256, Zeilenzahl.

Weicht etwas ab: **Abbruch, melden.**

## Block A — Register 45 (Registertext aus Fable 26a)

`## 45. …` sinngemäss: „Messbitten nach dem Tag, Reichweite (iv), Eingaben im Abbild, Pflege der Pfadliste, Abnahmebedingungen des Erzeugers — die Einträge aus Fable 26a (TB-114, 26.09.2026)“.

- **45.0 Kopf:** Anlass (erste gesammelte Tagesanfrage 26a, Fable-Takt einmal je Tag); Quelle mit Dateiname; Verweis auf 43 und 44.
- **45.1 bis 45.8:** R1 bis R8 **zeichengleich** aus dem Codeblock „Registerblock“ am Ende der Fable-Antwort, je Baustein ein Unterabschnitt, samt seiner „Quelle des Grundes“. Nichts umformulieren.
- **45.9 Tatsachennotiz des steuernden Chats zu R3** (Fables „Unsicher“ Nr. 1, gemessen am 26.09.2026 über die Brücke am Stand `0df8c64`, nur lesend):
  - `herkunft.register()` löst jeden Eintrag von `EINGEFROREN` mit `os.path.join(_HIER, rel)` auf, also immer relativ zu `research/vorregistrierung/`.
  - `shared/sperrlistensonde.py::_aufloesen` löst einen Eintrag nur dann relativ zu `research/vorregistrierung/` auf, wenn er kein `/` enthält oder mit `ergebnisse/` beginnt; sonst repo-relativ (Feld `pfadregel` im Abbild).
  - Folge: Ein Eintrag für `research/tb24_haltedauern/daten/…` wäre in einem der beiden Programme nicht auffindbar. `register()` führt eine nicht gefundene Datei in `fehlend` und rechnet ohne sie weiter.
  - Die zehn heutigen Einträge sind von der Abweichung nicht betroffen.
  - Vollzug: Block B dieses Auftrags.
- **45.10 Was offen bleibt:** die drei Verfahrensmessungen (geschlossene Kerze, Adjustierung der 150 Aktienreihen, TB-85-Kette) ⇒ TB-115; Erzeuger; Faltenplan-Abbild; Stufe IV.

**Marken am alten Ort** (additiv; den Zielabschnitt vorher lesen; nie in einen zeichengleich zitierten Registertext hinein, sondern direkt darunter):

| Wo | Marke |
|---|---|
| **43.3** (Überschrift bleibt), unter dem Kasten | „von Fable bestätigt (26a 3 (1)), siehe 45.1“ |
| **42.2 E1** (Klasse (iv)) | „Reichweite: siehe 45.2“ |
| **30.2**, unter dem zitierten Text, und **33.3** | „Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11“ |
| **19**, unter der TB-113-Marke, und **42.2 E2** | „Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4“ |
| **41.1 A12** und **42.6** Zeile (5) | „Abnahmebedingungen des Erzeugers: siehe 45.5“ |
| **27**, am Ende des Abschnitts, und **7.1** | „Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7“ |
| **44.3** | „beantwortet in Fable 26a, siehe 45“ |

**Nachweise:**
- numstat, zweite Spalte 0;
- je R-Baustein `diff` gegen den Codeblock der Fable-Datei, rc 0 (8 Stück);
- Sonde vorher = nachher gegen `e655c1c8…`;
- `register()` alt/neu;
- `test_vorregistrierung` 196/196.

Commit „TB-114 Block A: Register 45 …“, Push.

## Block B — `herkunft.py`, dritte Öffnung

**B1 — eine Pfadregel.** `register()` löst die Einträge von `EINGEFROREN` nach **derselben Regel** auf wie `sperrlistensonde._aufloesen`: kein `/` oder Präfix `ergebnisse/` ⇒ relativ zu `research/vorregistrierung/`, sonst repo-relativ. `herkunft.py` importiert die Sonde nicht; die Gleichheit sichert eine Gegenprobe im Test: Für jeden Eintrag von `EINGEFROREN` liefern beide denselben absoluten Pfad. Dazu eine Mutationsprobe: Ein Eintrag mit `/` ausserhalb von `ergebnisse/` unter der alten Regel ⇒ Gegenprobe rot.
- ⭐ **Nachweis:** `register()` vor B1 = nach B1, bytegleich. Die zehn Einträge sind nicht betroffen, und `rel` geht unverändert in den Hash ein.

**B2 — nur messen, nichts ändern:** Wer liest `register()["fehlend"]`? Führt eine fehlende eingefrorene Datei irgendwo zu rc ≠ 0, im Modus und ohne? Suchmuster und Treffer in `b2_fehlend.txt`. Das ist eine Frage für Fable (A5-Klasse: ein Hash, der eine fehlende Datei still auslässt), keine Änderung.

**B3 — die neun Listen in `EINGEFROREN`** (R3), repo-relativ, in der Reihenfolge der Bots wie in `strategies/`:
- **Vorher lesen:** 40.6 und 41.1 A12. Schreibt der künftige Erzeuger die neuen Listen an **denselben** Pfad? Die Antwort kommt als Tatsachennotiz ins Ergebnis. Liegt der Pfad anders, gilt: `EINGEFROREN` folgt dem Pfad, den der Erzeuger schreibt, beim Einbau des Erzeugers (R5).
- Danach: `register()` neu (erwartet: anders als nach Block A), `fehlend` leer.

**B4 — `datenstand(None)` im Modus ⇒ 2** (R5 (c)). Ohne übergebenen Pfad endet `datenstand()` unter dem Modus mit `paths.RUECKGABEWERT_STARTPRUEFUNG`, bevor gelesen wird. Ohne Modus bleibt das Verhalten unverändert. Dazu eine Probe mit Mutationsgegenprobe.

**Tests:** grün.
- Wo ein Test die Anzahl 10 oder die Liste von `EINGEFROREN` fest kodiert, wird er dem Register nachgezogen; jede Änderung einzeln im Ergebnis.
- Neue Proben: B1 (Gegenprobe + Mutation), B4 (Probe + Mutation).

Commit „TB-114 Block B: herkunft.py - eine Pfadregel mit der Sonde (B1), neun TB-24-Listen in EINGEFROREN (B3), datenstand(None) im Modus 2 (B4)“, Push.

## Block C — Neues Abbild und Nachmessung

- **Abbild** mit `sperrliste_abbild.py`, **neuer Dateiname**: `sperrliste_abbild_2026-09-26_tb114.json` bzw. mit dem Datum des Laufs. Prüfen, dass kein vorhandenes Abbild überschrieben wird (`test -f` vorher).
- **Sonde gegen das neue Abbild:** 0 Befunde, (ii) 0. Die Gruppe `eingefroren` hat 19 Einträge.
- **Sonde gegen das alte Abbild `e655c1c8…`:** Befund **genau**:
  - der Hash von `herkunft.py`;
  - die neun neuen Einträge in `eingefroren`.
  
  Nichts sonst.
- **Unverändert:**
  - Benchmark im Modus, Repo **und** frischer Klon `64fb2912…`;
  - ohne Modus 8/8 Ausgaben bytegleich (`docs/belege/TB-109/g2_ausgaben.sh`);
  - Trockenlauf 9 × rc 0;
  - Hash von `ergebnisse/faltenplan.json` unverändert.
- **Tests:**
  - `test_vorregistrierung`, `test_ersatzwerte`, `test_startpruefungen`, `test_arbeitsbaum_laufbereich`, `test_sperrlistensonde`, dazu die übrigen Testdateien unter `research/vorregistrierung/` und `shared/`: rc 0;
  - der Laufbereich ist weiterhin 81 Module (`herkunft.py` gehört nicht dazu, R5 (a)).

## Block D — Register 45, Vollzug (Tatsachennotiz, am Ende anhängen)

**45.11 Vollzug in TB-114:**
- B1 mit dem Nachweis `register()` vorher = nachher;
- B2 als Messung (offen bei Fable);
- B3 mit dem Pfad-Befund zum Erzeuger;
- B4;
- Hash-Übergänge `herkunft.py` und `register()`;
- **gültiges Abbild** (Name, sha256);
- Sonde gegen das alte Abbild mit genau dem erwarteten Befund.

Nachweise wie Block A: numstat zweite Spalte 0, Sonde gegen das neue Abbild vorher = nachher, `test_vorregistrierung`.

## Block E — Journal, Ergebnis

- Journalblock `## DM — TB-114: …`.
- `docs/ERGEBNIS_TB-114_register_45_herkunft_pfadregel.md` mit „Für Fable“ und „In einfacher Sprache“. „Für Fable“ enthält:
  - B2 als Frage;
  - den Pfad-Befund zum Erzeuger aus B3;
  - jede Testannahme, die nachgezogen wurde.
- Belege unter `docs/belege/TB-114/`.

## Commits

1. Schritt 0;
2. Block A;
3. Block B;
4. Abbild und Nachmessung (Block C);
5. Block D;
6. Block E.

Nach jedem Commit Push.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- Ein Ausgangswert in 0b weicht ab, oder eine der neun Listen ist nicht versioniert.
- `diff` eines R-Bausteins rc ≠ 0; numstat des Registers mit zweiter Spalte ≠ 0.
- `register()` vor B1 ≠ nach B1.
- Nach B3: `fehlend` nicht leer.
- Die Sonde meldet gegen das neue Abbild einen Befund, oder gegen das alte mehr bzw. anderes als erwartet.
- Benchmark ≠ `64fb2912…`, eine Ausgabe ohne Modus verändert, der Trockenlauf nicht 9 × rc 0, ein Test rot.
- Ein vorhandenes Abbild würde überschrieben.

## In einfacher Sprache

Fable hat acht Textbausteine fürs Regelwerk geliefert; sie kommen wörtlich als Abschnitt 45 hinein. Der wichtigste sagt: Nach dem grossen Lauf dürfen nur vorher angemeldete Auswertungen gerechnet werden. Ein Baustein verlangt, die neun Handelslisten, aus denen der Faltenplan seine Längen ableitet, mit Prüfsumme festzuhalten. Das ging bisher nicht, weil zwei Programme Pfade unterschiedlich lesen. Die Sitzung gleicht das an, nimmt die neun Listen auf, schreibt ein neues Abbild und misst alles nach. Am Ergebnis des Laufs darf sich dabei nichts ändern.
