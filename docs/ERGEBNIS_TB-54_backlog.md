# ERGEBNIS TB-54 — Die acht Backlog-Nachträge (d)–(k) eingearbeitet (Mac-Lauf, 19.09.2026)

**Auftrag:** `MAC_TB-54_nachtraege_backlog_v2.md` (formuliert 19.09.2026, Fassung
v2). **Ausgeführt am MacBook**, Zweig `main`, Ausgang **`1124880`** (= `0fe61d7`
plus das TB-55b-Ergebnisdokument; `BACKLOG.md` in beiden identisch), Ergebnis
**`d9f3c4b`** für (d)–(g) und **`3121ec2`** für (h)–(k), beide gepusht.
Interpreter durchgehend `trading-env/bin/python3` = **Python 3.9.6**. Kein
eigener Zweig, kein PR.

**Kurzfassung:** Alle acht Nachträge sitzen in `docs/projektfuehrung/BACKLOG.md`
— sieben neue Blöcke **2j, 2k, 2m, 2n, 2o, 2p, 2q**, 21 neue Zeilen in Abschnitt
4, sechs ersetzte Kettenzeilen (**jede mit altem Wortlaut darunter, als ersetzt
gekennzeichnet und datiert**), eine Kopfzeile vor T34.10. **Gegen `0fe61d7`:
167 Zeilen hinzu, 2 entfernt** — die zwei sind die Kettenzeilen 0,84 und 0,85,
beide stehen darunter weiter. Der Auftrag wurde in **zwei Commits** ausgeführt,
weil (h) eine Kettenzeile `0,87` einfügen wollte, die es bereits gab — der
Betreiber wurde gefragt und entschied **0,88 mit Vermerk**. Datenstand, zwölf
Datenbanken und der Snapshot sind vor und nach der Arbeit identisch; der
Registerprüfer meldet vorher (07:37 UTC, vor jeder Änderung) und nachher
**KEIN BEFUND**.

---

## Schritt −1 — Ortsprüfung

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | vorhanden | **vorhanden**, `Python 3.9.6` ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell mit `origin` | `/Users/jaquelineloffler/trading-bot`, `main`, nach `git fetch`: `HEAD` = `origin/main` = `1124880` ✅ (neuer als `0fe61d7`, wie der Auftrag erlaubt) |
| `git status --short` | 0 Zeilen | **0** ✅ |

---

## Schritt 0 — Sichern und messen

**Sicherungsordner:** `~/Sicherungen/tb54_backlog_20260919T073739Z/` (Liste,
Quersummen, Kopien, Prüfprotokoll nachher).

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | 12, davon 9 `paper_trading_*` | **12**, davon **9** `paper_trading_*` in der Wurzel (plus die 0-Byte-Doppelgängerin `strategies/volatility_breakout/paper_trading_volatility_breakout.db`, V1) ✅ — Kopien gegen `shasum -a 256 -c`: **12/12 OK** |
| Datenstand vorher (`--nur-hash`, 07:37:47 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| `snapshot.py --pruefen snapshots/63e4b6c8…` | `UNVERAENDERT`, rc 0 | **`UNVERAENDERT`, rc 0** ✅ (Soll = Ist für `snapshot_hash` und `datenstand_hash`/223) |
| Registerprüfer vorher (`--basis a1e7fb4`), **07:37:55 UTC** | KEIN BEFUND | **KEIN BEFUND**, rc 0, `Quelle beleg: trockenlauf` ✅ — **vor** der ersten Änderung an `BACKLOG.md`, nicht nachgeholt (A7) |
| `BACKLOG.md` Ausgangswert | festhalten | **764 Zeilen, 207 502 Bytes**, SHA-256 `86549420…` |

Die zwölf Datenbanken sind dieselben wie in TB-55 und TB-55b.

---

## Schritt 1 — Bestandsaufnahme

**Quelle, und nur sie:** `~/Downloads/nachtraege_backlog/` (acht Dateien plus
`00_INHALT.txt`). Alle acht Bytegrössen stimmen mit `00_INHALT.txt` überein.
**Keiner der acht war bereits eingearbeitet** — für jeden Buchstaben wurden
mehrere kennzeichnende Zeichenfolgen gesucht (Blocküberschrift, erste
Punktnummer, erste K-Nummer), Treffer überall **0**.

| Buchstabe | Bytes gemessen | Bytes laut `00_INHALT.txt` | Kennzeichen gesucht (Treffer vorher) | schon eingearbeitet? | Kopien gefunden wo |
|---|---:|---:|---|---|---|
| (d) | 5 862 | 5 862 ✅ | `T51.1`, `2j —` (0/0) | nein | `docs/projektfuehrung/BACKLOG_NACHTRAG_2026-09-18d.md` (versioniert, **byteidentisch**) · `~/Downloads/TB-51_bewertung/` (byteidentisch) |
| (e) | 8 828 | 8 828 ✅ | `T52.1 `, `2k —`, `K1r` (0/0/0) | nein | **keine** |
| (f) | 5 201 | 5 201 ✅ | `T52.14`, `K1u` (0/0) | nein | **keine** |
| (g) | 7 533 | 7 533 ✅ | `F13`, `2m —`, `K1w` (0/0/0) | nein | **keine** |
| (h) | 9 921 | 9 921 ✅ | `T55.1 `, `2n —`, `K1x` (0/0/0) | nein | `~/Downloads/tb55_bewertung/` (byteidentisch) |
| (i) | 4 939 | 4 939 ✅ | `2o —`, `K2a`, `DOPPELGÄNGERIN` (0/0/0) | nein | `~/Downloads/tb55_v3/` (byteidentisch) |
| (j) | 6 790 | 6 790 ✅ | `T55.13`, `2p —`, `K2c` (0/0/0) | nein | `~/Downloads/tb55final/` (byteidentisch) |
| (k) | 6 731 | 6 731 ✅ | `T55b.1`, `2q —`, `K2f` (0/0/0) | nein | `~/Downloads/tb54/` (byteidentisch) |

Kopien wurden **genannt, nicht benutzt**. Weitere Nachtragsdateien in
`~/Downloads` betreffen (a)–(c) und sind nicht Gegenstand dieses Auftrags.

**Zwei Messungen vor dem Einfügen, die der Auftrag verlangt („nichts raten"):**

- **Letzter Block der 2er-Reihe:** `2i` (Zeile 480). Die Blöcke stehen als
  `## 2e…2i` (Ebene 2, T50.10) — die Nachträge schreiben `### 2j…`; die
  Überschriften wurden auf `##` gesetzt, damit sie keine Unterabschnitte von
  2i werden. **Es gibt keinen Block `2l`**: (f) legt keinen an, (g) sieht
  diesen Fall vor („*nach dem letzten Block der 2er-Reihe*") → 2m folgt auf 2k.
- **Die Kette (Abschnitt 3):** `0,84` (Zeile 512) und `0,85` (Zeile 513,
  spricht von den 90 Modulen) mit dem im Nachtrag zitierten Wortlaut
  (Gleichheit für 0,84 per `assert` geprüft). ⚠️ **`0,87` existiert bereits**
  (Zeile 514, *„In einem Zug, braucht die Freigabe für
  `shared/entscheidungskerze.py`"*) — Nachtrag (h) will eine **neue** `0,87`
  anlegen. Siehe Schritt 2, (h).

---

## Schritt 2 — Einarbeiten, einer nach dem anderen

Jede Einfügung lief über ein kleines Werkzeug (`werkzeug.py`, `schritt_?.py`
im ZIP), das für jeden Anker prüft, dass er **genau einmal** vorkommt, und
sonst **vor dem Schreiben** abbricht. Zwei solche Abbrüche gab es (ein
Anführungszeichen im Anker bei (d), ein Zeilenumbruch im Anker bei (h)) —
beide vor dem Schreiben, Datei unverändert, Anker gekürzt, wiederholt. Nach
jedem Nachtrag wurde **zweifach** gemessen: `git diff --numstat` gegen `HEAD`
(kumulativ) **und** `git diff --no-index --numstat` gegen die Kopie des Standes
vor diesem Nachtrag (der Schritt allein). Der zweite Wert ist nötig, weil
(f), (h), (j) und (k) Kettenzeilen ersetzen, die **derselbe Arbeitsbaum** erst
angelegt hatte — gegen `HEAD` sind die unsichtbar.

**Form der Ersetzung:** die neue(n) Zeile(n), unmittelbar darunter die alte
Zeile **wörtlich**, nur die Rang-Zelle um *(alter Wortlaut — ersetzt
19.09.2026 durch Nachtrag (x) vom …)* ergänzt.

| Nachtrag | Schritt allein (+/−) | kumulativ gegen HEAD | Einfügestellen | entfernte Zeile → steht darunter? |
|---|---:|---:|---|---|
| (d) | **24 / 1** | 24 / 1 | Block 2j nach 2i (vor `## 3`) · Kette 0,84 · Abschnitt 4: `~~K1n~~`, K1o, K1q ans Tabellenende | 0,84 → **ja** |
| (e) | **32 / 1** | 56 / 2 | Block 2k nach 2j · Kette 0,85 → 0,85a / 0,85b / 0,85c · Abschnitt 4: K1r–K1t | 0,85 → **ja** |
| (f) | **11 / 1** | 66 / 2 | 2k-Tabelle: T52.14–T52.20 angehängt · Kette 0,85a → ERLEDIGT, **Merge-Commit `7e48e1f`** aus `git log --merges` eingesetzt · Abschnitt 4: K1u, K1v | 0,85a (aus (e)) → **ja** |
| (g) | **18 / 0** | 84 / 2 | Kopfzeile **vor** T34.10 (Zeile 265, Punkt bleibt) · Block 2m nach 2k · Kette 0,86 **vor 0,95** · Abschnitt 4: K1w | — |
| *Commit `d9f3c4b`* | *85 / 3* | *84 / 2* | *Differenz 1/1 = die 0,85a-Zeile, von (e) angelegt, von (f) ersetzt* | |
| (h) | **25 / 1** | 25 / 1 | Block 2n nach 2m · Kette 0,86 → 0,86 neu + TB-56-Zeile als **0,88** (s. u.) · Abschnitt 4: K1x–K1z | 0,86 (aus (g)) → **ja** |
| (i) | **16 / 0** | 41 / 1 | Block 2o nach 2n · Abschnitt 4: K2a, K2b | — |
| (j) | **22 / 1** | 62 / 1 | Block 2p nach 2o · Kette 0,86 → 0,86 ERLEDIGT + 0,86a · Abschnitt 4: K2c–K2e | 0,86 (aus (h)) → **ja** |
| (k) | **23 / 1** | 84 / 1 | Block 2q nach 2p · Kette 0,86a → 0,86a ERLEDIGT + 0,86b · Abschnitt 4: K2f–K2h | 0,86a (aus (j)) → **ja** |
| *Commit `3121ec2`* | *86 / 3* | *84 / 1* | *Differenz 2/2 = 0,86 aus (h) und 0,86a aus (j), im selben Arbeitsbaum ersetzt* | |

**Die Rückfrage bei (h).** Nachtrag (h) löst eine Nummernkollision (0,86 doppelt
vergeben) auf, indem er `0,86` neu fasst und die Faltenschranke als **neue
Zeile `0,87`** einträgt — *„damit die Nummern eindeutig bleiben"*. `0,87` war
aber bereits belegt. Wortlaut und Zweck fielen auseinander; nach der Regel
aus TB-55b wurde **gefragt, nicht entschieden**. Der Betreiber wählte: **die
TB-56-Zeile als `0,88`, mit Vermerk in der Rang-Zelle** (*„im Nachtrag (h) als
0,87 vergeben; 0,87 war bereits belegt — Betreiberentscheidung 19.09.2026:
0,88"*). Die bestehende `0,87` blieb unberührt; (i)–(k) verweisen nicht auf
0,87, kein Folgekonflikt. (d)–(g) waren zu diesem Zeitpunkt bereits als
Teilerfolg committet und gepusht (`d9f3c4b`), wie der Auftrag es vorsieht.

**Die Kette nach dem Einarbeiten** (Zeilen 645–660), zur Ansicht:

```
0,84 (neu) · 0,84 alt (d) · 0,85a ERLEDIGT · 0,85a alt (f) · 0,85b · 0,85c ·
0,85 alt (e) · 0,87 (bestehend) · 0,86 ERLEDIGT · 0,86a ERLEDIGT · 0,86b ·
0,86a alt (k) · 0,86 alt (j) · 0,88 [TB-56, Vermerk] · 0,86 alt (h) · 0,95 …
```

Die Reihenfolge ist die, die die Nachträge vorgeben („vor 0,95", „ersetzen,
alter Wortlaut darunter") — numerisch ist sie nicht sortiert (0,87 steht vor
0,86). **Nicht umsortiert**, weil Umsortieren entfernte Zeilen erzeugt hätte.

---

## Schritt 3 — Einchecken

| | Ist |
|---|---|
| `git status --short` vor jedem Commit | nur ` M docs/projektfuehrung/BACKLOG.md` ✅ |
| Gesamtmessung gegen `0fe61d7` | **167 / 2** |
| Summe der Schritt-Messungen | 171 / 6 — abzüglich der **vier** Zeilen, die in dieser Sitzung angelegt und wieder ersetzt wurden (0,85a; 0,86 zweimal; 0,86a): **167 / 2** ✅ stimmt |
| Zeilen | 764 + 167 − 2 = **929** ✅ (`wc -l`), 254 860 Bytes |
| Commits | `d9f3c4b` (d)–(g) · `3121ec2` (h)–(k), je `add`+`commit`+`push` in einem Zug; `git status` danach leer, `main` = `origin/main` ✅ |
| Kennzeichen nachher | jede Blocküberschrift 2j–2q, jede erste Punktnummer, jede erste K-Nummer, `0,88`, `0,86b`: **genau 1** Treffer · „alter Wortlaut — ersetzt 19.09.2026": **6** = die sechs Ersetzungen ✅ |

---

## Zum Schluss

| # | Prüfung | Ist |
|---|---|---|
| 1 | Datenstand am Ende (07:47 UTC) | **`d9449faf…a995f84` / 223** ✅ |
| 2 | Gesicherte `*.db` byteweise identisch | **12/12 OK** (`shasum -a 256 -c`), keine Abweichung, nichts gegen den Crontab zu rechnen ✅ |
| 3 | Snapshot `--pruefen` am Ende | **`UNVERAENDERT`**, rc 0 ✅ |
| 4 | Registerprüfer nachher (`--basis a1e7fb4`) | **KEIN BEFUND**, rc 0, `Quelle beleg: trockenlauf` ✅ |
| 5 | Dieses Dokument | `docs/ERGEBNIS_TB-54_backlog.md` |
| 6 | ZIP | `~/Downloads/TB-54_backlog.zip` (Ergebnisdokument, Werkzeug und acht Schrittskripte, Stufenkopien 00–08, Sicherungsliste/Quersummen/Prüfprotokoll, die acht Nachträge samt `00_INHALT.txt`) |
| 7 | Nachtragsdateien ins Repo | **sieben** Dateien — (e), (f), (g), (h), (i), (j), (k) — byteidentisch (`cmp`) nach `docs/projektfuehrung/nachtraege/`, mit ihrem Dateinamen; (d) lag schon versioniert unter `docs/projektfuehrung/`. `git check-ignore`: rc 1, von keinem Muster erfasst. **Begründung:** *Ein Beleg in `~/Downloads` ist kein Beleg; er existiert auf einem Rechner und in keiner Version.* |

Unberührt: `data/`, `snapshots/`, die Sperrliste, `shared/*`, jeder
Registertext, `JOURNAL.md`, `PRUEFPRINZIPIEN.md`, `ARBEITSWEISE.md`. Kein
Netzabruf ausser `fetch`/`push`, keine Order, kein Bot-Lauf, kein Basislauf,
kein `cat` auf eine Konfigurationsdatei.

---

## Die Fragen des Auftrags

**Wo lag jeder der acht Nachträge, und wie gross war er?** Alle acht in
`~/Downloads/nachtraege_backlog/`, Grössen 5 862 / 8 828 / 5 201 / 7 533 /
9 921 / 4 939 / 6 790 / 6 731 Bytes — jede gleich der Angabe in
`00_INHALT.txt`. Kopien: siehe Tabelle in Schritt 1.

**War einer schon eingearbeitet?** **Nein**, keiner (0 Treffer für jedes
Kennzeichen).

**Je Nachtrag: eingefügte Zeilen, entfernte Zeilen, Einfügestelle?** Tabelle in
Schritt 2: (d) 24/1 · (e) 32/1 · (f) 11/1 · (g) 18/0 · (h) 25/1 · (i) 16/0 ·
(j) 22/1 · (k) 23/1.

**Musste bei einer Kettenzeile etwas ersetzt werden — und steht der alte
Wortlaut noch darunter?** Sechs Ersetzungen: 0,84 (d) · 0,85 (e) · 0,85a (f) ·
0,86 (h) · 0,86 (j) · 0,86a (k). **Jede alte Zeile steht wörtlich darunter**,
in der Rang-Zelle als ersetzt gekennzeichnet und datiert — sechs Marker
gezählt. Dazu die Kopfzeile vor T34.10 aus (g), die nichts ersetzt.

**Stimmt die Gesamtmessung mit der Summe der Zwischenmessungen?** **Ja**:
171/6 in Schritten, 167/2 gegen `0fe61d7`; die Differenz 4/4 ist vollständig
den vier Zeilen zugeordnet, die innerhalb der Sitzung angelegt und ersetzt
wurden.

**Beobachtungen, NICHT ausgeführt:**

1. **`0,87` doppelt** — siehe Rückfrage; gelöst als 0,88 mit Vermerk. Die
   Kette ist damit numerisch unsortiert (0,87 vor 0,86/0,88).
2. **`V1`–`V7` aus (i) kollidieren mit den `V`-Nummern in Abschnitt 2** (dort
   `V1` = *„absolute Drawdown-Grenze gestrichen"*, Zeile 54). Nach dem
   Einfügen zwei `| **V1** |`. Nicht umnummeriert — es steht so im Nachtrag.
3. **`0,85c` nennt „TB-54 — Lese-Audit"**, dieser Auftrag heisst ebenfalls
   TB-54 (und (k) trägt in 0,86b „TB-54 — die acht Backlog-Nachträge").
   Dieselbe Aufgabennummer für zwei Dinge — Wortlaut der Nachträge, nicht
   angefasst.
4. **`K1n`, `K1o`, `K1q` stehen jetzt zweimal in Abschnitt 4** (Original aus
   (c) und Fortschreibung aus (d)) — so verlangt es „nur hinzufügen"; (d)
   erwartete ausdrücklich nur eine entfernte Zeile.
5. **Die Nachtragsdatei (d) im Repo hat keinen Beleg-Kopf** („EINGEARBEITET …
   Commit …"), wie ihn (c) in TB-51 bekam. Nicht angefasst — nur `BACKLOG.md`
   war freigegeben; die sieben neuen Kopien sind ebenfalls byteidentisch und
   ohne Kopf, damit ihre Grössen gegen `00_INHALT.txt` prüfbar bleiben.
6. **Das Muster aus TB-51 (0,82) hat den alten Wortlaut nicht stehen
   lassen**; dieser Auftrag verlangt es. Die Form (Rang-Zelle mit Marker)
   ist neu und offen für Einspruch — sie ist in einem Commit je Hälfte
   einsehbar.
7. **Der Registerprüfer meldet `Quelle numstat: 568 0`** gegen `a1e7fb4`
   (TB-55b: 506 0) — der Zuwachs ist Abschnitt 18 aus TB-55b, kein Befund.
8. **`git rev-parse --short HEAD origin/main`** als Kontrollbefehl schlug fehl
   (`Needed a single revision`, `--short` nimmt nur eine Revision) — der
   Push war erfolgt, nachgeprüft mit zwei getrennten Aufrufen und
   `git status -sb`. Werkzeugfehler der Sitzung, kein Befund am Repo.

---

## In einfacher Sprache

**Was gemacht wurde:** Acht vorbereitete Ergänzungen wurden in die
Vorhabenliste eingetragen, in der vorgeschriebenen Reihenfolge, eine nach der
anderen. Nach jeder einzelnen wurde gezählt, wie viele Zeilen dazukamen und
wie viele verschwanden.

**Was verschwunden ist:** Nur zwei Zeilen der Ausgangsdatei — und beide stehen
direkt unter ihrer neuen Fassung weiter, mit dem Hinweis „alter Wortlaut,
ersetzt am 19.09.2026". Nichts ist weg.

**Wo es geklemmt hat:** Die fünfte Ergänzung wollte eine Zeile mit der Nummer
0,87 anlegen — die Nummer war aber schon vergeben. Statt selbst zu
entscheiden, wurde gefragt. Antwort: die neue Zeile bekommt 0,88 und einen
Vermerk, warum. Die ersten vier Ergänzungen waren da schon gesichert
abgelegt; die letzten vier folgten danach.

**Woran man sieht, dass nichts anderes passiert ist:** Die Kursdaten, die
eingefrorene Kopie und alle zwölf Datenbanken sind vor und nach der Arbeit
bis aufs Byte gleich. Der Prüfer für das Regelwerk meldet vor und nach der
Arbeit keinen Befund — und der „vorher"-Lauf war wirklich vorher.

**Was noch ansteht:** Die Ergänzungen für Tagebuch und Prüfregeln (TB-54b)
sind nicht Teil dieses Auftrags und noch offen.
