# TB-104 — Alle Leser des Laufbereichs auf den Resolver, die Verfahren-A-Felder aus dem Faltenplan, und der Laufbereich gemessen

**Sitzungstitel:** `TB-104` · **Angelegt:** 25.09.2026, 08:10, vom steuernden Chat
**Grundlage:** Fable 24c Abschnitt 2 (Resolver-Pflicht), 24d Abschnitt 3 (nur der Resolver-Modus ist ein Modus-Lauf; „alle Leser auf den Resolver“), 25a Abschnitte 1 (1), 3 (A), 3 (C), 4 (Laufbereich, `herkunft.py`)
**Vorgänger:** TB-103 (`836865f`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)

> **In einfacher Sprache, vorweg:** Mehrere Rechenprogramme bauen ihre Dateipfade noch selbst, statt sie von der zentralen Pfadstelle zu holen. Diese Sitzung stellt sie um. Ausserdem entfernt sie aus dem Zeitplan-Programm Werte aus einem abgeschafften Verfahren, die niemand liest. Und sie misst, welche Programme ein geschützter Lauf überhaupt lädt.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 07:52, Auswahlkarte im steuernden Chat.** Gefragt war: *„TB-104 (Fables Plan-Punkt 2 und die Altfelder): Welche Dateien dürfen geändert werden?“* Die Antwort: **„Alle freigeben (Empfohlen)“**. Die Option lautete:

> benchmark.py (Sperrlistenpunkte 4/6), faltenplan.py (Punkt 2, Altfelder purge/embargo/training entfernen), faltenplan_neun.py, erste_falte_trockenlauf.py, universum_trockenlauf.py, loaderlauf.py, dazu deren Tests und test_vorregistrierung.py (G8). Die Freigabe vom 24.09., 11:25 für faltenplan.py und ein neues Abbild wird dabei verbraucht. Eine Sitzung, ein neues Abbild. Die Benchmark-Tabelle muss bytegleich bleiben.

| freigegeben | Pfad | Sperrliste |
|---|---|---|
| ✔ | `research/vorregistrierung/benchmark.py` | **Punkte 4 und 6** — planmässig nach 37.3 |
| ✔ | `research/vorregistrierung/faltenplan.py` | **Punkt 2** — planmässig nach 37.3; verbraucht die Freigabe vom 24.09., 11:25 |
| ✔ | `research/faltenplan_neun/faltenplan_neun.py`, `research/faltenplan_neun/erste_falte_trockenlauf.py` | messen (A8) |
| ✔ | `research/universum_trockenlauf/universum_trockenlauf.py`, `research/universum_trockenlauf/loaderlauf.py` | messen (A8) |
| ✔ | die Tests dieser Module: `research/faltenplan_neun/test_*.py`, `research/universum_trockenlauf/test_universum_trockenlauf.py`, `research/vorregistrierung/test_vorregistrierung.py` (u. a. `G8`) | — |
| ✔ | **ein** neues Sperrlisten-Abbild unter neuem Namen (`sperrliste_abbild.py --ziel`) | 36.6 |

⚠️ **Nicht freigegeben, aber absehbar betroffen:** `research/vorregistrierung/registerbericht.py` zeigt `p['purge_tage']` an (Funktion, die die Faltentabelle schreibt; am Stand `836865f` Z. 147). Nach dem Entfernen der Felder bricht es dort ab. ⇒ **Frag den Betreiber per Auswahlkarte, wie in TB-103 bei `test_strategy_paths.py`**, mit dem genauen Umfang (nur diese Anzeige). Ohne Freigabe: `registerbericht.py` nicht ändern, den Abbruch messen und melden.

⛔ **Nicht freigegeben und nicht anzufassen:** `herkunft.py` (Punkte 11/12, Fable 22d „nicht öffnen“ gilt weiter, siehe A5), `registerdaten.py` (Punkt 1), `auswertung.py` (Punkte 3/5/14), `shared/paths.py`, `shared/strategy_paths.py`, `shared/symbols_config.py`, `shared/ladeprotokoll.py`, alle `strategies/`, `notifications/`, `research/faltenplan_neun/embargo_neun.py`, das Register, `ergebnisse/faltenplan.json` (registrierter historischer Stand).

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet (Vormessung 25.09., 08:05):

| Datei | Stand |
|---|---|
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25a_tagblocker_weg_zwei_lesarten.md` | neu |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md` | neu, aus der Projektablage abgelegt |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md` | neu, aus der Projektablage abgelegt |
| `docs/projektfuehrung/UEBERGABE_2026-09-25.md` | neu |
| `docs/projektfuehrung/UMZUG.md` | geändert: Zeiger im Eröffnungstext auf die neue Übergabe |
| `docs/auftraege/MAC_TB-104_leser_auf_resolver_und_altfelder.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-104 |

Liegt etwas anderes im Arbeitsbaum: mitcommitten, wenn es eine Datei des steuernden Chats unter `docs/` ist, sonst melden.

**0b — nach 7c:** `.git/*.lock` keine; HEAD am Eingang **`836865f`**; Datenstand vorher (Soll `d9449faf…`); Quersummen der neun `*.db` vorher; Hashes aller freigegebenen **und** aller gesperrten Dateien vorher (`docs/belege/TB-103/hashes.sh` als Vorlage); Hash von `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Soll `64fb2912…`); Sonde gegen `sperrliste_abbild_2026-09-23.json` vorher.

Belege: `docs/belege/TB-104/0_*.txt`.

---

## Block A — Vormessung nachmessen, und die Fragen, die Fable offen hat

⚠️ Alles unten ist **Vormessung** des steuernden Chats (25.09., 07:45–08:05, Textsuche über `*.py` ausserhalb `docs/`, `HEAD 836865f`). Nach `A8`: Weicht deine Messung ab, **gilt deine**.

| | zu prüfen | Vormessung |
|---|---|---|
| **A1** | Eigene Pfadlogik für **Kurs- oder Universumsdateien** haben: `benchmark.py` (`BASE_DIR` aus `TB30A_BASE_DIR`, `DATA_DIR = BASE_DIR/data`; Universum über `BASE_DIR + registerdaten.UNIVERSUM[markt]`), `faltenplan_neun.py` (`TB36_BASE_DIR`; `data/<symbol>_<zeitrahmen>.csv`, Universum `config/…`), `universum_trockenlauf.py` und `loaderlauf.py` (`TB40_BASE_DIR`; `loaderlauf` setzt `modul.DATA_DIR` der Loader von aussen). `erste_falte_trockenlauf.py`: nicht gemessen | 4 sicher, 1 offen |
| **A2** | `TB30A_BASE_DIR` kommt ausserdem vor in `registerdaten.py`, `registerbericht.py`, `pruefe_grenzsaetze.py`, `herkunft.py`, `auswertung.py`, `faltenplan.py`, `messgroessen.py`. **Welche davon lesen Kurs- oder Universumsdateien?** Vormessung: `registerdaten.py` hält `UNIVERSUM` nur als **Konstante** (Pfadtexte), liest selbst nicht; `auswertung.py` liest `zellen.csv`/Tagesreihen (Ergebnisdateien, keine Kurse); `faltenplan.py` liest die neun TB-24-Listen (Ergebnisdateien) | nachmessen, je Modul eine Zeile |
| **A3** | `faltenplan.py::_plan` schreibt je Plan `purge_tage`, `embargo_tage` (= `purge_tage`) und je Falte `training_bis_ausschliesslich`; `purge_tage()` rechnet aus `mess["haltedauer"][bot]["max_tage"]`. Leser dieser Felder: nur `registerbericht.py` (Anzeige) und `test_vorregistrierung.py` `G8`. `benchmark.py`, `auswertung.py`, `registerdaten.py` lesen keins davon | TB-103-Zeit gemessen, Textsuche |
| **A4** | ⭐ **Fable 25a, Unsicherheit (3):** Ruft der Trockenlauf den Loader „am Datenende“ auf, so wie 16.1.1 (Spalte Bestätigung) gemessen wurde? Vormessung: `load_all_symbol_data()` hat **keinen** Datumsparameter; der Loader sieht den ganzen Snapshot bis zu dessen Ende. Die in TB-103 geladenen Mengen 18/18/20/20/20/147/147/147/147 sind **zahlengleich** mit 16.1.1 Spalte Bestätigung. **Miss nach, ob TB-40 die Bestätigungsspalte ebenfalls ohne Datumsgrenze (am Datenende) gemessen hat** (`docs/belege/TB-40/`, Ergebnisdokument TB-40) | Zahlen gleich; Verfahren TB-40 offen |
| **A5** | ⭐ **Fable 25a, Unsicherheit (1):** `herkunft.py::datenstand(daten_dir=None)` nimmt das Verzeichnis **als Argument**; Voreinstellung `BASE_DIR/data`. ⚠️ Aber `herkunft.py::block()` ruft `datenstand()` **ohne** Argument. ⇒ Nach Fable 25a bleibt `herkunft.py` zu; wer den Datenstand-Hash des Snapshots braucht, ruft `datenstand(<Resolver-DATA_DIR>)` selbst, nicht `block()`. **Nur messen und melden**, nichts ändern | Argument ja; `block()` ohne |
| **A6** | ⭐ **Fable 25a, Unsicherheit (2):** Legt ein Modus-Lauf eines Bots Ordner unter `results/<bot>/` oder `logs/<bot>/` an? Vormessung: `strategy_paths.get_strategy_paths()` ruft `os.makedirs(…, exist_ok=True)` für beide; alle 18 Ordner existieren, Änderungszeiten **vor** TB-103 (letzte `logs/elliott_wave` 24.09., 01:30). ⇒ Heute legt `makedirs` nichts an; in einem frischen Checkout legte es sie an. **Mit einem Wegwerfbaum ohne diese Ordner und dem Haken für Verzeichnisanlage (`os.mkdir`-Audit-Ereignis) messen**, im Modus, für einen Bot | heute: nichts angelegt |
| **A7** | ⭐ **Fable 25a, Unsicherheit (4):** Die `.get(…, default)`-Stellen in `auswertung.py` (Vormessung Z. 284/286 `statistik.get(zid, 0.0)`, Z. 380, 500–518): Ist ein Ersatzwert mit den **registrierten** Eingaben je erreichbar? **Nur lesen und messen, `auswertung.py` nicht ändern** | nicht gemessen |
| **A8** | Sperrlistenprüfung wie TB-103: Welche freigegebenen Dateien stehen auf einem der 14 Punkte, in `herkunft.py::EINGEFROREN`, im Abbild? | `benchmark.py` 4/6, `faltenplan.py` 2; übrige nicht gemessen |

Belege: `a_vormessung.txt`, `a4_datenende.txt`, `a5_datenstand.txt`, `a6_ordner.txt`, `a7_get.txt`, `a8_sperrliste.txt`.

---

## Block B — Die Leser auf den Resolver (Fable 24c Abschnitt 2, 24d Abschnitt 3, 25a (C))

**Die Regel, jetzt mit Fables angenommenem Wortlaut (25a (C)):** Jedes Modul des Laufbereichs, das Kurs- oder Universumsdateien liest, bezieht seine Pfade **über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)**. Für Module ausserhalb `strategies/<bot>/`: **direkt** über `shared/paths.py` (Grund: TB-103 Abschnitt 5 (5), `get_strategy_paths()` legt Ordner an).

**B1 — `benchmark.py`:** Kurse über `paths.DATA_DIR`, Universum über `paths.CONFIG_DIR` + Dateiname aus `registerdaten.UNIVERSUM` (`os.path.basename`, **keine** zweite Namensliste). `TB30A_BASE_DIR` bleibt nur, wofür es sonst gebraucht wird (Repo-Wurzel für Ergebnisdateien und Mutationsproben), und ist **kein** Weg zum Snapshot mehr.
**B2 — `faltenplan_neun.py`:** dasselbe für Kurs- und Universumsdateien; `TB36_BASE_DIR` wie oben.
**B3 — `universum_trockenlauf.py`, `loaderlauf.py`:** `TB40_BASE_DIR` darf den Loadern **keinen** Datenordner mehr von aussen setzen, wenn der Modus aktiv ist; unter dem Modus kommt `DATA_DIR` der Loader aus dem Resolver. Ohne Modus darf das bisherige Verhalten für Messwerkzeuge bleiben.
**B4 — `erste_falte_trockenlauf.py`:** nach A1 entscheiden; liest es Kurs- oder Universumsdateien selbst, dasselbe.

⛔ **Ohne Modus ändert sich kein Ergebnis.** ⭐ **Fable 24d Abschnitt 3:** Ein Hilfsordner oder eine Ersatzwurzel ist **kein** Modus-Lauf und trägt keinen Nachweisteil (b); als Messwerkzeug bleibt es zulässig und wird als solches benannt (Kommentar, `--help`).

**B5 — Proben je Modul**, Bauart TB-103 Teil I (Wegwerfbaum mit echtem `paths.py`, erfundenen Kursreihen in `data/`, Snapshot-Attrappe, eigener Audit-Haken):
- Probe „im Modus 0 Kursdateien aus `data/`, 0 Universumsdateien aus `config/`“
- Mutationsprobe „Resolver-Umstellung zurückgenommen“ ⇒ Probe rot
- Gegenprobe der Mutationsprobe. Jede Mutationsprobe beisst **allein** (24b B3).

Namen vergeben, im Ergebnisdokument mit Namen nennen.

**Commit (2):** Block B mit Tests.

---

## Block C — Die Verfahren-A-Felder aus dem Faltenplan (Fable 25a Abschnitt 1 (1))

**Fables Präzisierung zu 33.3/35.4, zeichengleich:**

> Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die 33.2/33.3 nicht kennt. Die Faltenplan-Sonde vergleicht den ganzen gerechneten Plan gegen das Abbild, nicht eine Auswahl seiner Felder. Verfahren-A-Felder (`purge_tage`, `embargo_tage`, `training_bis_ausschliesslich`) werden vor dem Tag aus `faltenplan.py` entfernt — Berichtigung des Codes an 2c/4a, planmässig nach 37.3 (Sperrlistenpunkt 2, Freigabe, alter und neuer Hash, neues Abbild). `G8` wird nicht gelöscht, sondern angepasst (23a): es prüft künftig, dass der gerechnete Plan je Falte keine Felder ausserhalb der Feldliste trägt — dieselbe Stelle, die registrierte Erwartung.

**C1 — `faltenplan.py`:** die drei Felder aus `_plan` entfernen; die Funktion `purge_tage` und ihr Lesen von `mess["haltedauer"]` entfallen damit, **wenn** sonst niemand sie ruft (A3). Nichts anderes ändern.
**C2 — Ausgabevergleich wie TB-86/TB-90**, nur im Speicher (⛔ `python3 faltenplan.py` nie direkt, TB-83): der gerechnete Plan vor und nach C1 je Bot. Soll: **genau die drei Felder weniger, jeder andere Schlüssel und Wert zeichengleich**, alle Faltengrenzen gleich.
**C3 — `G8` anpassen**, nicht löschen: Er prüft künftig, dass der gerechnete Plan je Plan und je Falte **keine Felder ausserhalb der Feldliste** trägt. Die Feldliste kommt aus der registrierten Quelle (33.3); gibt es keine maschinenlesbare, nimm die Schlüssel des gerechneten Plans **nach** C1 und schreib ins Ergebnisdokument, dass die Feldliste bis zum Abbild (33.3) aus dem Code kommt, nicht aus dem Register. Mutationsprobe: ein Verfahren-A-Feld wieder eingefügt ⇒ `G8` rot; Gegenprobe.
**C4 — `registerbericht.py`:** siehe Freigabe-Abschnitt (Auswahlkarte).
**C5 — ⭐⭐ Die Benchmark-Tabelle bleibt bytegleich.** Nach B **und** C: `benchmark.py --ziel <scratchpad>` im Modus (`TB_SELEKTIONS*`, nicht Hilfsordner) **zweimal** ⇒ Soll bytegleich `64fb2912…`. Mit Lesehaken, Aufrufstapel und den **drei Klassen aus Fable 25a (A)**:

| Klasse | Soll |
|---|---|
| (i) Eingaben | Kurse und Universum **nur** aus `snapshots/63e4b6c8…/`; ausserhalb erwartet nur die neun TB-24-Listen und `messgroessen.json` (39.8). Jeder weitere Zugriff ist ein Befund |
| (ii) Umgebung | als Liste je Lauf-Typ mit Aufrufstapel (Tatsachennotiz); Vergleich mit den 5 aus TB-103 |
| (iii) Schreibziele | nur `--ziel` und Belegpfade. ⚠️ `logs/notifications/manuelle_eingriffe.log` im Modus `a` (39.8, Fable 25a (3)): **messen, welcher Import es öffnet, nichts ändern** (`notifications/` ist nicht freigegeben) |

⛔ **Der Nachweis bleibt 2** (zwei Eingaben ausserhalb, 39.8). Bytegleich ist hier eine **Wache** dafür, dass B und C das Ergebnis nicht bewegen, kein Nachweis.

**Commit (3):** Block C mit Tests.

---

## Block D — Der Laufbereich, gemessen (Fable 25a Abschnitt 4)

**Fables Registertext-Entwurf, zeichengleich:**

> Der Laufbereich ist die Menge der Module, die ein Modus-Lauf lädt oder ausführt (Trockenlauf aller neun Bots, Erzeuger, `benchmark.py`, `faltenplan.py`, `auswertung.py` und ihre Kindprozesse), gemessen am Aufrufstapel des Lese-Audits.

**D1** — Die Menge der geladenen **Repo-Module** (Import-Audit, auch Bytecode aus dem Cache auf die Quelldatei zurückgeführt) für: (a) den Trockenlauf aller neun Bots im Modus (Skript aus `docs/belege/TB-103/d_trockenlauf.py`, unverändert wiederverwenden), (b) `benchmark.py` im Modus aus C5, (c) `auswertung.py` im Modus **nur als Import** (es gibt noch keine Ergebnisse, die es auswerten könnte — wenn ein Aufruf nicht möglich ist, nur `import` und die Module melden). Ausgabe: eine Liste je Lauf-Typ, und die Vereinigung.
**D2** — Das Rückfall-Inventar aus TB-103 (`docs/belege/TB-103/a4_rueckfaelle.txt`, gut 50 Fundstellen) gegen D1 legen: **je Fundstelle „im Laufbereich ja/nein“**. Nichts ändern.
**D3** — Stehen die vier Rückfälle aus Fable 25a Abschnitt 4 im Laufbereich? (b) `t3_supertrend` BTC-Regimefilter (`equity_simulation.py`, `multi_symbol_optimise.py`; Register 11.1, `shared/regimewache.py::pruefe_einbau()`), (c) `exit()` mit rc 0 in den Backtest-Skripten, (d) Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py`, (a) `symbols_config.py` bei nach `EXCLUDE_SYMBOLS` leerer Liste. **Je Rückfall: Datei, Stelle, im Laufbereich ja/nein, welcher Lauf-Typ lädt sie.** ⭐ Das ist die Grundlage für die nächste Freigabekarte des Betreibers (TB-105); **nichts davon ändern**, ausser wo es in einer freigegebenen Datei steht **und** Block B/C es ohnehin berührt — dann melden, nicht still mitnehmen.

⛔ Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl.

Belege: `d1_laufbereich_<lauftyp>.txt`, `d2_rueckfaelle_im_laufbereich.txt`, `d3_vier_rueckfaelle.txt`.

---

## Block E — Abgabe

| | |
|---|---|
| **E1** | Hashes nachher. Geändert nur freigegebene Dateien (dazu `registerbericht.py`, falls freigegeben) und `docs/`. Datenstand, Snapshot, `*.db` (bis auf Cron), `ergebnisse/` unverändert — **ausser** dem neuen Abbild |
| **E2** | ⭐ **Neues Abbild** nach dem letzten Code-Commit: `research/vorregistrierung/sperrliste_abbild.py --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-25.json` (Name frei, wenn belegt). Sonde gegen das **alte** Abbild: Befund an 2, 4, 6 erwartet (planmässig nach 37.3). Sonde gegen das **neue**: kein Pfad-Bestandteil `1`. Alter und neuer Hash von `faltenplan.py` und `benchmark.py` als Tatsachennotiz |
| **E3** | Tests am Ende: `test_vorregistrierung.py` (Soll 191 + neue, alle grün), `test_faltenplan_neun.py`, `test_erste_falte_trockenlauf.py`, `test_universum_trockenlauf.py`, `test_paths.py` 35/35 |
| **E4** | Ergebnisdokument `docs/ERGEBNIS_TB-104_leser_auf_resolver_und_altfelder.md` mit **„Für Fable“** (ohne Kontext lesbar, 27.1): A4–A7 als Antworten auf seine vier Unsicherheiten aus 25a · B mit Probenamen · C mit Ausgabevergleich und `G8` · C5 mit den drei Klassen · D mit der Laufbereichsliste und den vier Rückfällen |
| **E5** | „Für die Folgesitzung vorbereitet“ (TB-105: die vier Rückfälle mit Dateiliste; Register 41/42) · „In einfacher Sprache“ · Journalblock · `git --no-optional-locks status --porcelain` nach dem letzten Commit leer |

**Commits:** (1) Schritt 0 · (2) Block B · (3) Block C · (4) Abbild · (5) Belege und Ergebnis. Nach jedem fertigen Teil pushen.

---

## ⚠️ Abbruchkriterien

1. Die Benchmark-Tabelle ist nach B oder C **nicht** bytegleich `64fb2912…` ⇒ nicht weiterbauen, Ursache messen, melden. **Keine** neue Tabelle erzeugen.
2. Der Ausgabevergleich in C2 zeigt mehr als die drei Felder ⇒ C zurücknehmen, melden.
3. Ohne Modus ändert sich ein Ergebnis irgendeines der umgestellten Module ⇒ zurücknehmen, melden.
4. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ Auswahlkarte an den Betreiber, wie TB-103; ohne Antwort nicht ändern.
5. ⭐ Block D findet mehr, als erwartet ⇒ **das ist ein Ergebnis**, kein Abbruch.

## ⛔ Was NICHT geschieht

Kein Registertext. Keine neuen Handelslisten, kein Erzeuger (Plan-Punkt 3). Keiner der vier Rückfälle wird behoben (TB-105). `herkunft.py`, `registerdaten.py`, `auswertung.py` bleiben zu. `faltenplan.json` bleibt, wie es ist. `python3 faltenplan.py` nie direkt.

---

## In einfacher Sprache

Gestern ist die zentrale Pfadstelle repariert worden. Einige Rechenprogramme fragen sie aber gar nicht: Sie bauen ihre Pfade selbst und lesen deshalb im geschützten Modus womöglich am falschen Ort. Diese Sitzung stellt sie auf die zentrale Stelle um.

Ausserdem schreibt das Programm für den Zeitplan der Auswertung noch drei Werte aus einem Verfahren hinein, das es nicht mehr gibt. Niemand liest sie, aber eine künftige Prüfung würde daran scheitern. Sie kommen raus.

Zur Sicherheit wird die Vergleichstabelle danach neu gerechnet. Sie muss Byte für Byte gleich bleiben, sonst hat die Umstellung etwas bewegt.

Zum Schluss misst die Sitzung, welche Programme ein geschützter Lauf überhaupt lädt. Nur für diese gilt die Regel „keine Notlösungen“. Dann ist klar, welche der vier übrigen Notlösungen vor dem Stichtag wirklich betroffen sind.
