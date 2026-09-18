# Ergebnis TB-51 — Startdatei, Flackerstufe, Nachtrag (c)

**Mac-Sitzung, 18.09.2026, 14:58–15:10Z, direkt auf `main`** (kein Zweig, kein
PR — `ARBEITSWEISE.md` §5b). Ausgangsstand `58c0ab9` (der Auftrag nennt
`93eb894`; `58c0ab9` ist der Folgecommit, der den Nachtrag (c) selbst ins Repo
legte — Voraussetzung erfüllt). Interpreter durchgehend `trading-env/bin/python3`
(3.9.6). Kein Bot, kein Abruf, kein Broker-Endpunkt, **kein Snapshot**, kein
voller Basislauf.

**Commit 1: `7cbf33a`** (die Arbeit). **Commit 2** (dieses Dokument und der
Beleg-Kopf in der Nachtragsdatei, siehe Abschnitt 7) — Hash im ZIP
(`26_commit2.txt`), Status danach in `27_status_nach_letztem_commit.txt`.

---

## Die Fragen des Auftrags, zuerst

| Frage | Antwort |
|---|---|
| **Gab es `START_HIER.md` wider Erwarten doch schon?** | **Nein.** Weder `docs/START_HIER.md`, noch irgendwo im Arbeitsbaum (`find`, `trading-env/` ausgeschlossen), noch in `git ls-files`. Teil 1 wurde ausgeführt: **95 / 0** |
| **Wie heisst die neue Stufe, wie sieht ihre Zeile aus?** | Liste **`FLACKERND`**, Stufe **`flackernd`**, Zeichen `[~~~~]`. Die echte Zeile (Basislauf auf diese eine Datei beschränkt, `fuehre_aus` lief echt): `[~~~~] system/test_log_rotation.py  6.4s flackernd (Mac ~30 %, 18.09.2026, TB-49-Maclauf: 3 von 10 rot, immer 116/117): heute gruen` — bei rot steht `heute rot`. Unter dem Strich: `flackernd 1` und `SUMME 1 von 1 Testdateien` |
| **Beisst jede neue Probe?** | **Ja, alle fünf** — je eine Mutante, in der die Probe fällt (Abschnitt 5). Zusätzlich fallen Probe 1 und 2 gegen die **wirkliche** Vorgängerfassung (`git show 58c0ab9:…basislauf.py`). Selbsttest **24 / 24, rc 0** |
| **Geht die Summenzeile weiterhin auf?** | **Ja.** `gruen + rot + flackernd + ungeprueft + zeitgrenze` = Zahl der Dateien, nachgerechnet aus den **gedruckten** Zahlen (gestellt: 2/1/2/1/1 = 7), plus eine eigene `SUMME`-Zeile, die `<-- GEHT NICHT AUF` schreibt und rc 1 liefert, wenn sie es je nicht täte |
| **Wie viele Zeilen je Datei, jede entfernte erklärt?** | `START_HIER.md` 95/0 · `ARBEITSWEISE.md` 6/**5** · `BACKLOG.md` 27/2 · `basislauf.py` 43/**1** · `test_flackerstufe.py` 497/0 · Nachtrag (c) 5/0 (Commit 2). **Neun entfernte Zeilen, jede zugeordnet** (Abschnitt 1). ⚠️ Zwei Abweichungen von der Erwartung des Auftrags, beide erklärt: ARBEITSWEISE 5 statt 4, basislauf 1 statt 0 |
| **Beobachtungen, NICHT ausgeführt** | Abschnitt 8 |

---

## 0. Schritt 0 — Datenbanken und Datenstand

| | vorher (14:58:36Z) | nachher (15:07:23Z) |
|---|---|---|
| neun `paper_trading_*.db`, SHA-256 | `01_db_vorher.txt` | `22_db_nachher.txt` — **`diff` leer (0 Zeilen), byteweise identisch** |
| Sicherungskopie | `~/Sicherungen/tb51_datenbanken_20260918T145836Z/` (neun Dateien, `cp -p`) | — |
| Datenstand (`herkunft.py::datenstand`) | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** | **identisch, 223** |
| Snapshot-Ordner (`snapshots/`, `data/snapshots/`) | nicht vorhanden | nicht vorhanden |
| Crontab gesichert | `03_crontab.txt` (40 Zeilen) | keine Abweichung zu erklären |

Kein Cron-Lauf fiel in das Fenster (Aktien-Bots ab 22:15 Ortszeit,
Krypto-Bots zu vollen Stunden ausserhalb 16:58–17:07 Ortszeit).

---

## 1. `git diff --numstat` je Datei — und jede entfernte Zeile zugeordnet

```
95	0	docs/START_HIER.md
6	5	docs/projektfuehrung/ARBEITSWEISE.md
27	2	docs/projektfuehrung/BACKLOG.md
43	1	research/datenordner_schnitt/basislauf.py
497	0	research/datenordner_schnitt/test_flackerstufe.py
5	0	docs/projektfuehrung/BACKLOG_NACHTRAG_2026-09-18c.md   (Commit 2)
```

Alle entfernten Zeilen (`14_alle_entfernten_zeilen.txt`, Diff in `15_diff_gesamt.patch`):

| # | Datei | entfernte Zeile (Anfang) | Ursache |
|---|---|---|---|
| 1 | ARBEITSWEISE | `2. **Ich formuliere die Aufgabe** (\`CLOUD_TB-<Nr>_…` | Berichtigung 3, Schritt 2, Zeile 1 |
| 2 | ARBEITSWEISE | `   der Numstat-Auflage je Datei und der ausdrücklichen Regel, …` | Berichtigung 3, Schritt 2, Zeile 2 |
| 3 | ARBEITSWEISE | `   inhaltlich umformuliert** wird.` | Berichtigung 3, Schritt 2, Zeile 3 |
| 4 | ARBEITSWEISE | `3. **Der Nutzer startet die Cloud-Sitzung** und legt parallel …` | Berichtigung 3, Schritt 3, Zeile 1 |
| 5 | ARBEITSWEISE | `   Weg 1 selbst ab.` | Berichtigung 3, Schritt 3, Zeile 2 |
| 6 | BACKLOG | `⚠️ **Mac-Lauf vor dem Merge, nicht danach.** Datenstand \`d9449faf…\`/223 vorher =` | Berichtigung 2 |
| 7 | BACKLOG | `\| ~~0,82~~ \| ~~TB-49 — die Ausnahme ins Werkzeug~~ \| ⭐ **CLOUD FERTIG 18.09.**, …` | Berichtigung 1 |
| 8 | basislauf.py | `    for art in ("gruen", "rot", "ungeprueft", "zeitgrenze"):` | Teil 3: das Stufen-Tupel der Summenzeile um `"flackernd"` erweitert |

### Warum ARBEITSWEISE 5 und nicht 4

Der alte Block aus Berichtigung 3 ist **fünf** Zeilen lang (Schritt 2 drei
Zeilen, Schritt 3 zwei), der neue sechs. **Keine** der fünf alten Zeilen ist
zeichengleich mit einer neuen — git kann also keine behalten. Die 4 des
Auftrags ist eine Zählung aus dem Gedächtnis; die 5 steht in
`14_alle_entfernten_zeilen.txt`.

### Warum BACKLOG genau 2 — und wie Berichtigung 2 gesetzt wurde

Berichtigung 2 nennt als Suchtext nur `⚠️ **Mac-Lauf vor dem Merge, nicht
danach.**`. In der Datei geht die Zeile weiter (`… Datenstand \`d9449faf…\`/223
vorher =`). Ersetzt wurde **der benannte Satz innerhalb der Zeile**, der Rest
der Zeile blieb wörtlich stehen — deshalb eine entfernte und eine hinzugefügte
Zeile, nichts vom Restsatz verloren. Berichtigung 1 traf zeichengleich (der
Wortlaut wich nicht ab).

### Warum basislauf.py 1 und nicht 0

Alles Neue ist eingefügt (Docstring-Absatz, Liste, `elif`-Stufe, Zeichen,
`SUMME`, Rückgabewert). Die **eine** entfernte Zeile ist das Tupel der
Stufen, das die Zahlen unter dem Strich druckt — es muss `"flackernd"`
enthalten, sonst zählt die Summenzeile die Stufe nicht (genau das misst
Mutante M3). Eine Fassung mit null entfernten Zeilen (eigener `print` hinter
der Schleife) hätte die Stufe ans Ende der Liste gestellt; die Reihenfolge
`gruen, rot, flackernd, ungeprueft, zeitgrenze` ist die des Auftrags. ⚠️ Der
TB-50-Kommentar über `BEKANNT_ROT` steht **vollständig** (`git diff` zeigt dort
keine Zeile).

---

## 2. Teil 1 — `docs/START_HIER.md` (95 / 0)

Der Text wurde **maschinell** zwischen den Markern `--- ANFANG DATEI …` und
`--- ENDE DATEI …` aus der Auftragsdatei geschnitten (`awk`), nicht
abgetippt — Emoji, Fettung, Tabellenstriche und Zeilenumbrüche sind damit
zeichengleich. 95 Zeilen, keine Markerzeile in der Datei.

⭐ **`ARBEITSWEISE.md` Abschnitt 10, Schritt 2 führt `START_HIER.md` weiterhin
als Paketbestandteil** (Zeile 702: `| \`START_HIER.md\` | ✅ Einstieg, auf den
aktuellen Stand gebracht |`, dazu Zeile 726 in der Prompt-Vorlage) — **jetzt zu
Recht. Nichts geändert.** Alle fünf Verweise in `17_…`.

---

## 3. Teil 2 — Nachtrag (c) in `BACKLOG.md` (27 / 2) und `ARBEITSWEISE.md` (6 / 5)

Die Texte wurden per Skript **aus der Nachtragsdatei gelesen** (die sechs
Codeblöcke, der Block 2i, die vier K1-Zeilen) und mit Anker-Prüfung eingesetzt
(jeder Suchtext genau einmal, sonst Abbruch): `nachtrag_c.py` im ZIP.

| Stelle | Ergebnis |
|---|---|
| Berichtigung 1 (Kette 0,82) | ersetzt, zeichengleicher Treffer |
| Berichtigung 2 (Kopf 2h) | Satz innerhalb der Zeile ersetzt, Restzeile erhalten (Abschnitt 1) |
| Block 2i | **nach 2h**, vor `## 3 — Die Kette`, mit `---`-Trenner wie 2e–2h |
| K1n–K1q | hinter K1m in Abschnitt 4 |
| Berichtigung 3 | in `ARBEITSWEISE.md` 5b, „Der feste Ablauf", Schritte 2 und 3 |

⚠️ **Eine Formentscheidung, offen benannt:** Der Nachtrag schreibt den Block als
`### 2i`. Die Blöcke 2e–2h stehen in der Datei als `## …` (T50.10: sonst
Unterabschnitte von 2d). Block 2i wurde **als `## 2i — …`** eingefügt — die
Überschriftsebene der Nachbarn, der Text selbst unverändert.

---

## 4. Teil 3 — `basislauf.py` (43 / 1): die Stufe `flackernd`

| | |
|---|---|
| **Liste** | `FLACKERND = {"system/test_log_rotation.py": "Mac ~30 %, 18.09.2026, TB-49-Maclauf: 3 von 10 rot, immer 116/117"}` — Rate, Datum, Herkunft |
| **Verhalten** | Datei in `FLACKERND` **und** Ergebnis `gruen` oder `rot` ⇒ `art = "flackernd"`, `heute = gruen/rot`, `unerwartet = False`. Zeitgrenze oder Nutzungszeile bleiben, was sie sind (Probe 1.6: an der Zeitgrenze weiterhin UNERWARTET) |
| **Reihenfolge** | die Stufe steht **vor** `BEKANNT_ROT` und **nach** `UNGEPRUEFT`/`LAEUFT_WEITER`; eine Datei, die in beiden Listen stünde, wäre flackernd — Probe 4.6 sichert, dass `test_log_rotation.py` in keiner anderen Liste steht |
| **Zählung** | eigene Zahl `flackernd`, **nicht** in `gruen`, **nicht** in `rot`; auch im JSON (`je_art`) |
| **Summenzeile** | `SUMME  n  von N Testdateien`, Vermerk `<-- GEHT NICHT AUF` und rc 1, falls je ungleich (A5: ein Werkzeug, das falsch zählt, sagt es) |
| **Zeichen** | `[~~~~]` — das Ergebnis dieses Laufs steht im Text dahinter |
| **Rückgabewert** | wie bisher 0/1 nach UNERWARTET; zusätzlich 1, wenn die Summe nicht aufgeht |

Der Basislauf zählt damit **66** Testdateien (65 in T49.11 + der neue
Selbsttest). Der Selbsttest druckt `… Pruefungen bestanden` und wird vom
Basislauf als gemessen erkannt, nicht als Nutzungszeile.

---

## 5. Der Nachweis — `test_flackerstufe.py`, 24 / 24, jede Probe beisst

**Am Verhalten, ohne Basislauf:** `basislauf.main()` läuft mit **gestellten**
Ergebnissen (`testdateien` und `fuehre_aus` im geladenen Modul ersetzt, Listen
durch eine Probeliste). Sieben gestellte Dateien, jede Stufe vertreten. Gelesen
wird die Ausgabe, wie ein Mensch sie liest: Zeile je Datei, `<-- UNERWARTET`,
die Zahlen unter dem Strich, dazu das JSON.

| Probe | erwartet | Werkzeug | Mutante | Ausgang in der Mutante |
|---|---|---|---|---|
| **1** FLACKERND, grün | nicht UNERWARTET, eigens gezählt, Zeile sagt es | OK (7 Bedingungen) | **M1** `elif False:` — die Stufe abgeschaltet | **fällt**: Zeile ohne `flackernd (`, ohne `heute gruen`, ohne Rate; unter `gruen` gezählt; JSON ohne eigene Zahl. *Nicht* gefallen: „nicht UNERWARTET" — ohne Eintrag war grün schon immer still, das ist genau die 70-%-Hälfte des Befunds |
| **2** FLACKERND, rot | nicht UNERWARTET, eigens gezählt | OK (6) | **M1** | **fällt**: `<-- UNERWARTET`, unter `rot` gezählt, steht in der UNERWARTET-Liste — die 30-%-Hälfte |
| **3** BEKANNT_ROT, grün | **weiterhin** UNERWARTET | OK (4) | **M2** die Stufe fängt **jeden** grünen/roten Lauf ab | **fällt**: nicht mehr UNERWARTET, als flackernd eingeordnet. **Kontrolle in M1: besteht unverändert** — die alte Stufe ändert sich nicht mit |
| **4** keine Liste, rot | **weiterhin** UNERWARTET, rc 1 | OK (4) | **M2** | **fällt**: nicht UNERWARTET, rc 0. **Kontrolle in M1: besteht unverändert** |
| **5** Summenzeile | fünf gedruckte Zahlen = 7, `SUMME 7 von 7` | OK (7) | **M3** Tupel ohne `"flackernd"` | **fällt**: nur vier Stufen gedruckt, Summe 5 ≠ 7 |

Jede Mutante ist eine **Ersetzung im Speicher, die genau einmal treffen
muss** (sonst Abbruch — sie könnte sonst etwas anderes verändern als gedacht).

⭐ **Gegenprobe gegen die wirkliche Vorgängerfassung:** `git show
58c0ab9:research/datenordner_schnitt/basislauf.py`, geprüft, dass sie
`FLACKERND` nicht kennt — Probe 1 und 2 fallen dort mit denselben Bedingungen,
und der rote Lauf ist dort UNERWARTET (3.3): der Befund T50.4, reproduziert.
Ist git nicht erreichbar, ist Teil 3 **rot, nicht übersprungen** (A1).

⚠️ **Prüfprinzip B1 hat sofort gegriffen — ein Fehler im ersten Entwurf des
Tests, benannt statt still korrigiert:** Die gestellten Dateien hiessen
`probe/test_flackernd_heute_gruen.py`. Die Bedingung *„Zeile nennt
`flackernd`"* war damit **blind** — der Dateiname enthielt das Wort. Aufgefallen
an Probe 1.6 (Zeitgrenze), die deshalb rot war, und daran, dass diese Bedingung
in Mutante M1 **nicht** fiel. Behoben: Dateinamen `test_wechselhaft_…`, geprüft
wird die Einordnungsform `flackernd (`. Erst danach 24 / 24
(`10_test_flackerstufe.txt`).

**Nebenprüfung:** `test_prozessgruppe.py` (TB-47) läuft mit dem geänderten
`basislauf.py` weiter **11 / 11**, kein Prozess bleibt zurück (`12_…`).

---

## 6. Gegenproben

| Prüfung | vorher | nachher |
|---|---|---|
| `pruefe_register.py --basis a1e7fb4` | **KEIN BEFUND, rc 0** (`04_…`) | **KEIN BEFUND, rc 0** (`18_…`) |
| neun Datenbanken | `01_…` | byteweise identisch (`23_db_diff.txt` leer) |
| Datenstand | `d9449faf…`/223 | `d9449faf…`/223 |
| Sperrliste | — | keine Sperrlisten-Datei im Status (`live_params`, `forward_test`, `equity_simulation`, `multi_symbol_optimise`, `entscheidungskerze`, `paths`) |
| Wegwerf-Verzeichnisse `tb51_*` in `/tmp` und `$TMPDIR` | — | **0** |

Ehrlich benannt: der Lauf „vorher" von `pruefe_register.py` (>2 min) lief im
Hintergrund, **während** Teil 1 und 2 schon schrieben. Er vergleicht das
Register gegen `a1e7fb4`; das Register wurde nicht berührt, das Ergebnis ist
davon unabhängig — und der Lauf „nachher" bestätigt es.

---

## 7. Ablauf, Commits, Belege

1. Commit 1 `7cbf33a`: die fünf Dateien aus Abschnitt 1.
2. **Commit 2: Beleg-Kopf in `BACKLOG_NACHTRAG_2026-09-18c.md` (5 / 0) und dieses
   Dokument.** ⚠️ Der Beleg-Kopf steht **nicht** im Auftrag. Er folgt dem
   Verfahren aus TB-50 (`93eb894`: alle fünf Nachtragsdateien tragen
   `EINGEARBEITET am … Commit …`); ohne ihn wäre (c) die einzige Nachtragsdatei
   ohne Vermerk, und niemand sähe ihr an, dass sie eingearbeitet ist. Fünf
   hinzugefügte Zeilen, nichts entfernt — wenn unerwünscht, in einer Minute
   rückgängig.
3. `git push` und `git status --porcelain` **nach** dem letzten Commit
   (`26_commit2.txt`, `27_status_nach_letztem_commit.txt`).

| Schritt | Beleg im ZIP |
|---|---|
| Schritt 0 | `00_…`, `01_db_vorher.txt`, `02_datenstand_vorher.txt`, `03_crontab.txt` |
| Gegenprobe vorher / nachher | `04_pruefe_register_vorher.txt`, `18_pruefe_register_nachher.txt` |
| Skripte, die Texte aus den Quellen lesen und einfügen | `nachtrag_c.py`, `teil3_basislauf.py` |
| Selbsttest, echte Zeile, Nebenprüfung | `10_test_flackerstufe.txt`, `11_basislauf_eine_datei_echt.txt`, `12_test_prozessgruppe.txt` |
| numstat, entfernte Zeilen, Diff, Sperrliste, Status vor Commit | `13_…`, `14_…`, `15_diff_gesamt.patch`, `16_…` |
| `START_HIER`-Verweise in ARBEITSWEISE | `17_…` |
| Commit 1, Beleg-Kopf, DBs/Datenstand nachher | `19_commit1.txt`, `20_numstat_belegkopf.txt`, `21_…`–`24_…` |
| Commit 2, Push, Status nach dem letzten Commit | `25_push.txt`, `26_commit2.txt`, `27_status_nach_letztem_commit.txt` |

Keine Konfigurationsdatei geöffnet, kein `cat`/`git show` auf `.env` oder
`config/`.

---

## 8. Beobachtungen, die NICHT ausgeführt wurden

1. **`basislauf.py`, Docstring Zeile 6: *„Dazu muss er drei Dinge
   auseinanderhalten"*** — die Aufzählung hatte schon vor TB-51 vier Punkte
   (rot, bekannt rot, ungeprüft, Zeitgrenze) und jetzt fünf. Zahl im Text
   gealtert; **nicht geändert** (nicht freigegeben, hätte eine Zeile entfernt).
2. **Die gealterten Zahlen `1312` / `62` im selben Docstring** (K1o, T50.6) —
   heute **66** Testdateien mit Ausschluss, laut T50.6 1 315 ohne. **Berichtet,
   nicht geändert**, wie verlangt.
3. **`STRATEGIEN_uebersicht.md` existiert weiterhin nirgends im Repo** (K1q) —
   `find` und `git ls-files` leer. `ARBEITSWEISE.md` §10 führt sie im Paket.
   Dieselbe Betreiberentscheidung wie bei T50.3: anlegen oder streichen.
4. **Kette 0,84 steht jetzt an zwei Stellen mit verschiedenem Ton:**
   `START_HIER.md` §3 sagt *„wird erst am Tag des signierten Tags gezogen
   (Registertext 5, Backlog F1a)"*, `BACKLOG.md` §3 sagt *„nach dem Merge nicht
   mehr blockiert. Eigene Entscheidung mit eigener Freigabe"*. Kein Widerspruch,
   aber die Betreiberentscheidung vom 18.09. steht **nur** in der Startdatei
   und im Auftrag, nicht in der kanonischen Quelle. Nichts geändert (nicht
   beauftragt; der Backlog ist Weg 2).
5. **Die `SUMME`-Wache ist nach heutigem Aufbau unerreichbar** — jede Datei
   bekommt genau eine `art`, `je_art` summiert alle. Sie beisst erst, wenn
   jemand eine Stufe hinzufügt, die nicht in `je_art` landet. Das ist
   gewollt (A5), aber kein Nachweis über heute — deshalb misst Probe 5 die
   **gedruckten** Zahlen, nicht die `SUMME`-Zeile.
6. **`test_flackerstufe.py` Teil 3 braucht die git-Historie** (`git show
   58c0ab9:…`). In einem Export ohne `.git` wäre Teil 3 rot — absichtlich rot,
   nicht still übersprungen. Auf beiden Rechnern liegt die Historie.
7. **Der Auftrag nennt als Ausgangsstand `93eb894`**, `main` stand auf
   `58c0ab9` (der Commit, der den Nachtrag (c) selbst legte). Kein Problem,
   nur genannt — die Voraussetzungsdatei existiert genau deshalb.
8. Die drei Läufe von `test_log_rotation.py` aus TB-50 plus der eine hier
   (6,4 s, grün) sind **vier Einzelmessungen, alle grün** — bei ~30 % mit 24 %
   zu erwarten, **kein** Beleg gegen die Rate (A6). Kein weiterer Lauf
   gestartet.

---

## In einfacher Sprache

**Drei Dinge waren offen, drei sind erledigt.**

**Erstens** gab es seit Wochen eine Datei nur auf dem Papier: die
Einstiegsseite, die jede neue Arbeitssitzung zuerst lesen soll. Sie steht jetzt
wirklich im Ordner — wortgleich mit der Vorlage, nicht abgetippt, sondern
maschinell herausgeschnitten.

**Zweitens** wurden vier Stellen in den Projektunterlagen berichtigt, in denen
ein alter Satz einem neuen widersprach — zum Beispiel stand in einer Zeile
zugleich „gemergt" und „Merge offen". Jede entfernte Zeile ist einzeln
aufgelistet und einer Berichtigung zugeordnet; es sind neun, und keine davon
ist unerklärt. Wo die Zählung im Auftrag nicht stimmte (vier statt fünf), steht
der Grund dabei.

**Drittens** hat das Prüfwerkzeug, das alle Tests des Projekts durchlaufen
lässt, eine neue Schublade bekommen. Bisher kannte es nur „grün", „rot" und
„bekannt rot". Ein Test, der **manchmal** rot ist — hier: drei von zehn
Läufen, wegen einer Zeitabhängigkeit —, passte in keine: Ohne Eintrag schlug
das Werkzeug bei jedem roten Lauf Alarm, mit Eintrag bei jedem grünen. Jetzt
gibt es „flackernd": beide Ausgänge sind erwartet, die Datei wird eigens
gezählt, und die Zeile sagt, was heute herauskam und wie oft es rot ist.

**Und das Wichtigste:** Dass die neue Schublade wirklich tut, was sie soll,
ist nicht behauptet, sondern gemessen — mit einem Selbsttest, der das Werkzeug
mit erfundenen Ergebnissen füttert, und mit Gegenproben, in denen die
Schublade absichtlich kaputtgemacht wird: Dort **muss** der Test fehlschlagen,
sonst würde er gar nichts prüfen. Das hat er in allen fünf Fällen getan. Dabei
ist ein Fehler im ersten Entwurf des Tests selbst aufgefallen und behoben
worden — das steht oben, nicht versteckt.

Die neun Datenbanken der Bots und der Kursdatenstand sind unverändert, kein
Snapshot wurde gezogen, und die Prüfung, die gar nicht zu dieser Aufgabe
gehört, ist vorher wie nachher ohne Befund.
