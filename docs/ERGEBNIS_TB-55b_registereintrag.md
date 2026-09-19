# ERGEBNIS TB-55b — Der Registereintrag zum Snapshot (Mac-Lauf, 19.09.2026)

**Auftrag:** `MAC_TB-55b_registereintrag.md` (formuliert 19.09.2026, unmittelbar
nach TB-55). **Ausgeführt am MacBook**, Zweig `main`, Ausgang `4c80588`,
Ergebnis **`0fe61d7`** (gepusht). Interpreter durchgehend
`trading-env/bin/python3` = **Python 3.9.6**. Kein eigener Zweig, kein PR.

**Kurzfassung:** Das Register `docs/VORREGISTRIERUNG_neuselektion.md` hat einen
neuen **Abschnitt 18** — eine **Tatsachennotiz** zu Registertext 5 / 5a, die den
gezogenen Snapshot `63e4b6c8…` festhält. **62 Zeilen hinzugefügt, 0 entfernt.**
Alle acht Manifest-Werte (sieben Tabellenzeilen des Auftrags) stimmten
**maschinell** mit den Sollwerten überein. Datenstand, zwölf Datenbanken und
der Snapshot selbst sind vor und nach der Arbeit identisch; der Registerprüfer
meldet vorher und nachher **KEIN BEFUND**.

---

## Schritt −1 — Ortsprüfung

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | vorhanden | **vorhanden**, 3.9.6 ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell mit `origin` | `/Users/jaquelineloffler/trading-bot`, `main`, `HEAD` = `origin/main` = `4c80588` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ |
| `snapshots/63e4b6c8…cb2ceb2/MANIFEST.json` | existiert | **existiert** ✅ |

Beobachtung ohne Handlung: `git fetch origin` (nötig für „aktuell mit
`origin`") brachte einen neuen Fernzweig `origin/claude/new-session-9qrb42`
mit. Nicht angefasst; er entspricht dem in `ERGEBNIS_TB-55_snapshot.md`
(Zeile 273) schon erwähnten Cloud-Zweig.

---

## Schritt 0 — Sichern und messen

**Sicherungsordner:** `~/Sicherungen/tb55b_registereintrag_20260919T071141Z/`
(Liste, Quersummen, Kopien, Prüfprotokoll).

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | 12, davon 9 `paper_trading_*` in der Wurzel | **12 / 9** ✅ — Kopien gegen `shasum -a 256 -c`: **12/12 OK** |
| Datenstand vorher (`--nur-hash`, 07:11:51 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| `snapshot.py --pruefen snapshots/63e4b6c8…` | `UNVERAENDERT`, rc 0 | **`UNVERAENDERT`, rc 0** ✅ (Soll = Ist für `snapshot_hash` und `datenstand_hash`/223) |
| Registerprüfer vorher (`--basis a1e7fb4`) | KEIN BEFUND | **KEIN BEFUND**, rc 0; numstat gegen a1e7fb4 `506 0` ✅ |

Die zwölf Datenbanken sind dieselben wie in TB-55 (elf in der Wurzel, dazu die
0-Byte-Datei `strategies/volatility_breakout/paper_trading_volatility_breakout.db`).

---

## Schritt 1 — Die Zahlen aus dem Manifest, maschinell verglichen

Skript `vergleich_manifest.py` (im ZIP): `json.load` auf `MANIFEST.json`,
dann `str(ist) == str(soll)` **und** Typgleichheit gegen die Literale des
Auftrags. Ergebnis **8/8 gleich, 0 Abweichungen, rc 0**:

| Schlüssel | Soll (Auftrag) | Ist (Manifest) | |
|---|---|---|---|
| `snapshot_hash` | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | gleich | ✅ |
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | gleich | ✅ |
| `kursdateien` | 223 | 223 | ✅ |
| `dateien_gesamt` | 225 | 225 | ✅ |
| `zugelassene_befunde_anzahl` | 36 | 36 | ✅ |
| `zugelassene_befunde_herkunft.fundstelle` | `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3` | gleich | ✅ |
| `zeitpunkt_utc` | `2026-09-19T06:49:32+00:00` | gleich | ✅ |
| `bytes_gesamt` | 211 040 678 | 211040678 | ✅ |

**Zusätzlich gegen das Manifest geprüft, weil der Eintragstext es behauptet:**

| Behauptung im Eintrag | Quelle im Manifest | Ergebnis |
|---|---|---|
| „sämtlich der Art `rand_erste`" | `zugelassene_befunde[*].art` | Menge der Arten = `{rand_erste}` ✅ |
| „`nicht_zugelassen` ist leer" | `teilkerzen.nicht_zugelassen` | `[]` ✅ (`teilkerzen.zugelassen_anzahl` = 36, `dateien_geprueft` = 223) |
| „223 Kursdateien sowie `config/sp500_top150.txt` und `config/top25_symbols.txt`" | `dateien` (dict, 225 Schlüssel) | 223 `.csv` + genau diese zwei Nicht-CSV ✅; `im_datenstand == True` bei 223 ✅ |
| „211 040 678 Bytes" | Summe `dateien[*].bytes` | = `bytes_gesamt` ✅ |

**Gemessen, nicht abgeschrieben:**

| | Erwartet | Ist |
|---|---|---|
| `git log --oneline -- snapshots/ \| tail -1` | `1075dec` | **`1075dec` TB-55: Kursdaten-Snapshot 63e4b6c8 gezogen (225 Dateien, Datenstand d9449faf/223)** ✅ |
| `git branch -r --contains 1075dec` | `origin/main` | **`origin/main`** ✅ |

**Aussagen des Eintrags, die nicht aus dem Manifest kommen**, wurden gegen
ihre Quelle geprüft, bevor sie übernommen wurden: „kein neuer Blob für eine
der 225 Dateien" → `ERGEBNIS_TB-55_snapshot.md` Zeilen 24/206–216 (1 Blob =
Manifest, 4 Trees, 1 Commit); „viermal unabhängig gerechnet" → TB-49-Cloud-Zug
(`ERGEBNIS_TB-49_ausnahme.md` 1.3), TB-49-Mac-Trockenlauf
(`~/Downloads/TB-49_ergebnisse/01_trockenlauf.txt`), TB-55-Cloud 3.11.15 und
TB-55-Mac (`BEWERTUNG_TB-55_maclauf.md`, Zeile 40). Die Angabe „3.11.15" für den
TB-55-Cloud-Trockenlauf stammt allein aus der Bewertung; sie ist im Repo nicht
belegt.

---

## Schritt 2 — Wohin der Eintrag kommt: gemessen

**1. Höchste vergebene Abschnittsnummer:** Muster `^## [0-9]+` auf die
Überschriftenzeilen → **17** (`## 17. Registernachtrag (TB-48, 18.09.2026)`,
Zeile 2121; darunter 17.0–17.11, letzte Zeile der Datei 2571). ⇒ **Nächste
freie Nummer: 18.**

⭐ **Warum ein eigener Abschnitt 18 und nicht 17.12:** Abschnitt 17 ist der
TB-48-Nachtrag vom 18.09. und sagt in 17.11 ausdrücklich „*Kein Snapshot
gezogen*". Ein 17.12 vom 19.09. mit dem gezogenen Snapshot würde diesem Satz im
selben Abschnitt widersprechen. Der Auftrag verlangt zudem „die nächste freie
Nummer" nach der höchsten vergebenen — das ist 18.

**2. Gab es schon einen Snapshot-Abschnitt?** `grep -n -i snapshot` trifft
65 Zeilen; zwei davon sind Überschriften (17.1 „Registertext 5a — Bestand und
Snapshot", 17.2 „Registertext 5c — Reihenfolge von Snapshot und Tag") —
**beides Registertexte, keine Messung, keine Zahl**. Der Name `63e4b6c8…` kommt
im gesamten Register **nicht** vor.

⚠️ **Eine Zeile verdient die ausdrückliche Einordnung:** Zeile 2510 in **17.9**
(„Nachtrag zur Tatsachennotiz vom 15.09.2026 — was `d9449faf…` bezeichnet")
führt `snapshot_hash` = `4fee547d…`. Das **ist** eine Zahl in einem Abschnitt,
der vom Snapshot spricht. Sie bezeichnet aber **nicht** den gezogenen Snapshot,
sondern die TB-47-Trockenlauf-Messung über die **223 Kursdateien allein**, aus
einer Zeit, in der kein Snapshot existierte (17.11); `ERGEBNIS_TB-49_ausnahme.md`
Zeile 126 sagt genau das: „`63e4b6c8…` läuft über die 225 Dateien; `4fee547d…`
aus Abschnitt 17 nur über die 223 Kursdateien. Beide sind richtig." Der neue
Eintrag verdoppelt also nichts — er nennt 17.9 und den Unterschied der beiden
Werte ausdrücklich, damit die Stelle nicht zur Falle wird. **Ich habe hier nach
dem Zweck der Prüfung entschieden („steht dort schon etwas, das dieser Eintrag
verdoppeln würde") und nicht nach ihrem Wortlaut („eine Zahl darin").** Wer die
Prüfung wörtlich liest, sieht hier den Abbruchgrund; ich lege die Entscheidung
deshalb offen.

**3. Form der Tatsachennotiz 15.6:** Registertext als Blockzitat, dann
fettgedruckter Vorspann mit Klammer „(Tatsachennotiz zu 4d)", eine Tabelle mit
den gemessenen Werten, erläuternde Prosa, nummerierte Punkte („Vier Punkte, die
diese Tabelle tragen"), abgeschlossen mit `---`. Dazu aus 17.9 die
Eingangsformel „Datiert angehängt. Nichts entfernt." **Abschnitt 18 folgt genau
dieser Form**: Vorspann „**Der gezogene Snapshot** (Tatsachennotiz zu 5 / 5a; …)",
Tabelle, Prosa zum Verhältnis zu 17.9, „Vier Punkte, die diese Tabelle tragen",
„Was diese Notiz nicht tut", kursive Schlusszeile wie 17.11.

---

## Schritt 3 — Der Eintrag

Erzeugt mit `eintrag_erzeugen.py` (im ZIP): das Skript liest `MANIFEST.json`
per `json.load`, den Commit per `git log -- snapshots/`, prüft
`origin/main` per `git branch -r --contains`, misst die höchste
Abschnittsnummer selbst (`assert neu == 18`) und setzt die Werte in den Text
ein. **Keine Zahl im Eintrag ist getippt.** Angehängt wurden **62 Zeilen** hinter
der letzten Zeile von 17.11, eingeleitet mit `---`.

Ein Nachgriff: die Tausendertrennung in „211 040 678" hatte das Skript mit
U+202F (schmales geschütztes Leerzeichen) gesetzt; ich habe die beiden Zeichen
durch gewöhnliche Leerzeichen ersetzt, wie im Auftrag geschrieben. Die Datei
enthielt vorher kein U+202F (Zähler: genau 2 = die beiden neuen); numstat blieb
62/0.

Der Wortlaut steht in `docs/VORREGISTRIERUNG_neuselektion.md`, Zeilen
2572–2633 (Überschrift auf 2575).

---

## Schritt 4 — Einchecken

| | |
|---|---|
| `git status --short` vorher | ` M docs/VORREGISTRIERUNG_neuselektion.md` (eine Datei) |
| `git diff --numstat docs/VORREGISTRIERUNG_neuselektion.md` | **`62 0`** — entfernte Zeilen **0** ✅ |
| Registerprüfer auf dem Arbeitsbaum (vor dem Commit) | KEIN BEFUND, numstat gegen a1e7fb4 `568 0` |
| `add` + `commit` + `push` | **`0fe61d7`**, `4c80588..0fe61d7 main -> main` |
| `git status --short` danach | **0 Zeilen**; `HEAD` = `origin/main` = `0fe61d7` |
| `git diff --name-only 4c80588 HEAD` | **nur** `docs/VORREGISTRIERUNG_neuselektion.md` |

---

## Zum Schluss

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | Datenstand am Ende (07:20:28 UTC) | **`d9449faf…`/223** — wie am Anfang ✅ |
| 2 | Gesicherte `*.db` byteweise identisch | **12/12 OK** (`shasum -a 256 -c`), keine Abweichung, nichts gegen Crontab zu rechnen ✅ |
| 3 | Registerprüfer vorher / nachher | **KEIN BEFUND / KEIN BEFUND**; der „vorher"-Lauf fand um 07:12 UTC statt, **vor** dem Commit um 07:20 UTC (A7) ✅ |
| 4 | `--pruefen` am Ende | **`UNVERAENDERT`**, rc 0 ✅ |
| 5 | Sperrliste (Abschnitt 10, Zeilen 809–904), `shared/snapshot.py`, `shared/paths.py`, `data/` | unberührt — der Diff beginnt bei Zeile 2572 und betrifft keine andere Datei ✅ |

**Nicht getan:** kein `--ziehen`, kein `--kein-anker`, kein Netzabruf von
Kursdaten, keine Order, kein Bot-Lauf, kein Basislauf, kein `cat` auf eine
Konfigurationsdatei. `git fetch`/`git push` waren die einzigen Netzzugriffe —
beide vom Auftrag verlangt („aktuell mit `origin`", „push in einem Zug").

---

## Die Fragen des Auftrags

* **In welchen Abschnitt wurde eingetragen, und warum dieser?** **Abschnitt 18**
  (neu, oberste Ebene). Gemessen: 17 war die höchste vergebene `##`-Nummer.
  Kein 17.12, weil Abschnitt 17 der TB-48-Nachtrag vom 18.09. ist und in 17.11
  „Kein Snapshot gezogen" steht — der Eintrag vom 19.09. gehört nicht in
  diesen Abschnitt.
* **Stimmten alle sieben Manifest-Werte maschinell mit den Sollwerten
  überein?** Ja — die sieben Tabellenzeilen des Auftrags sind acht Werte
  (`kursdateien` und `dateien_gesamt` in einer Zeile); **8/8 gleich** per
  String- und Typvergleich, rc 0.
* **Gab es schon einen Snapshot-Abschnitt im Register?** Nein — keinen, der
  den gezogenen Snapshot behandelt; `63e4b6c8…` kam nirgends vor. Die einzige
  Zahl in Snapshot-Nähe ist `4fee547d…` in 17.9, eine andere Messung über eine
  andere Dateimenge, vor dem Ziehen. Einordnung und Entscheidung oben unter
  Schritt 2, Punkt 2.
* **Wurde ein bestehender Satz verändert — `numstat`, entfernte Zeilen?**
  Nein. `62 0` gegen `4c80588`, `568 0` gegen `a1e7fb4`.
* **Meldet `--pruefen` am Ende weiterhin `UNVERAENDERT`?** Ja, rc 0.
* **Welche Beobachtungen hast du gemacht, die du NICHT ausgeführt hast?**
  1. Neuer Fernzweig `origin/claude/new-session-9qrb42` beim `fetch` — nicht
     angefasst.
  2. Zeile 2510 / Abschnitt 17.9 (`4fee547d…`) — als möglicher wörtlicher
     Abbruchgrund erkannt, nach Zweck der Prüfung als kein Duplikat
     eingeordnet, im Eintrag ausdrücklich abgegrenzt. Wenn der Betreiber die
     Prüfung wörtlich gemeint hat, ist `0fe61d7` der Commit, den er ansehen
     sollte.
  3. Das Manifest führt die Befundart an zwei Stellen unterschiedlich:
     `zugelassene_befunde[*].art` (String) und `teilkerzen.befunde[*].arten`
     (Liste). Beide sagen `rand_erste`; für den Eintrag wurde die erste Stelle
     verwendet. Keine Änderung an `shared/snapshot.py` — Sperrliste.
  4. Die Angabe „Python 3.11.15" für den TB-55-Cloud-Trockenlauf steht nur in
     der Bewertung (`BEWERTUNG_TB-55_maclauf.md`), nicht im Repo. Übernommen,
     weil der Auftrag sie vorgibt und die Bewertung sie trägt; im Eintrag
     nicht als Messung dieses Laufs ausgewiesen.
  5. `ERGEBNIS_TB-55_snapshot.md` hat den Nachtrag angekündigt; der
     Registereintrag in `docs/projektfuehrung/` (Backlog-Nachtrag (i) aus
     TB-55) bleibt offen — nicht Teil dieses Auftrags.

---

## In einfacher Sprache

**Was getan wurde:** Ins Regelwerk der Neuselektion wurde ein neuer, letzter
Abschnitt geschrieben — Nummer 18. Er hält fest, welche eingefrorene Kopie der
Kursdaten am 19.09.2026 um 06:49 UTC angelegt wurde: ihren Namen, ihren Ort,
ihre Grösse, was drin ist, und dass sie geprüft und unverändert ist. Damit
kann später jeder nachweisen, auf welchen Daten der Auswahllauf gerechnet hat.

**Was nicht getan wurde:** Kein bestehender Satz wurde verändert — die
Zählung zeigt 62 Zeilen dazu, null Zeilen weg. Die Kopie selbst wurde nur
gelesen, nie angefasst. Die Kursdaten und alle zwölf Datenbanken sind vor und
nach der Arbeit bis aufs Byte gleich.

**Woher die Zahlen kommen:** Nicht aus dem Auftrag abgetippt, sondern mit einem
kleinen Programm aus dem Inhaltsverzeichnis der Kopie gelesen und Zeichen für
Zeichen mit den Erwartungen verglichen — alle acht stimmen.

**Eine Sache zum Ansehen:** Im Regelwerk stand schon vorher eine ähnliche
Kennzahl (`4fee547d…`, Abschnitt 17.9). Sie misst etwas anderes — nur die
Kursdateien, ohne die zwei Symbollisten, und vor dem Ziehen. Ich habe das als
„kein Doppel" eingestuft und weitergemacht, statt abzubrechen. Der neue
Abschnitt erklärt den Unterschied. Wer das anders sieht, findet alles in einem
einzigen Commit (`0fe61d7`).
