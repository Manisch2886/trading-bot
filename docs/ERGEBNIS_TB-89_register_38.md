# TB-89 — Ergebnis: Registerabschnitt 38

**Sitzung:** Mac, `TB-89`, 23.09.2026
**Auftrag:** `docs/auftraege/MAC_TB-89_register_38.md`
**Eingang:** `c140ca9` · Schritt-0-Commit `da251da` · danach Abgabe-Commit
**Quelle der Zitate:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`
**Belege:** `docs/belege/TB-89/`

⛔ **Nur Registertext.** Keine `.py` im Bot- oder Forschungscode geändert, kein
neues Modul, kein Import, kein Abbild, kein Vollzug, `python3 faltenplan.py`
nicht aufgerufen, `registerbericht.py` und `test_vorregistrierung.py` nicht
angefasst. Kein Abbruchkriterium hat gegriffen.

---

## Schritt 0 — der Arbeitsbaum

Committet in `da251da`: `docs/projektfuehrung/ARBEITSWEISE.md` (`numstat 10 0`,
Abschnitt 7 — vom Betreiber, nicht entfernt), die Antwort
`FABLE_ANTWORT_2026-09-22h_…`, der Auftrag `MAC_TB-89_register_38.md` und der
umgestellte Zeiger `AKTUELLER_AUFTRAG.md` (`4 ++--`, ebenfalls vom Betreiber;
im Auftrag nicht genannt, aber im Arbeitsbaum). Danach `git status --porcelain`
leer (`0` Zeilen).

## 1. `numstat` auf das Register — beide Spalten

```
454	0	docs/VORREGISTRIERUNG_neuselektion.md
```

(`numstat.txt`) — **zweite Spalte `0`**. Zwölf Hunks, alle reine Einfügungen
(`@@ -n,0 +m,k @@`): elf Marken-Orte plus der angehängte Abschnitt 38
(340 Zeilen).

## 2. Die drei Hashes — vorher und nachher

| Datei | vorher (nach `da251da`) | nachher (vor dem Abgabe-Commit) |
|---|---|---|
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | gleich |
| `research/vorregistrierung/ergebnisse/faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | gleich |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | gleich |

`hashes_vorher.txt` / `hashes_nachher.txt`, `diff` leer. Zusätzlich
mitgemessen (gleicher Dateiname, anderer Ort, nicht gesperrt):
`research/faltenplan_neun/daten/faltenplan.json` `93fbf09c…`, gleich.

**Sperrlisten-Sonde, lesend, vor und nach dem Eintrag** (`sonde_vorher.txt`,
`sonde_nachher.txt`, gegen `sperrliste_abbild_2026-09-22.json`): beide Male
rc `1`, `1` nur an Punkt 2 (37.3, bekannt), Prüfung (ii) `0`, *„Listentext wie
bei Erzeugung: ja"*. Die Ausgaben sind bis auf das Zeilenintervall der Liste
gleich (Z. 836–901 → Z. 845–942: die neue Marke im Kopf von Abschnitt 0
verschiebt um 9, die Marken bei Punkt 4, 7 und 9 verlängern die Liste — die
Sonde liest sie als Notiz, R2).

**Ausserhalb von `docs/` geändert: nichts** (`git status --porcelain` zeigt nur
`docs/VORREGISTRIERUNG_neuselektion.md` und `docs/belege/TB-89/`).

## 3. Die Marken einzeln — vierzehn

Zeilen am Stand des Abgabe-Commits.

| # | Zeile | Ort | Eintrag |
|---|---|---|---|
| 1 | 16 | **Kopf von Abschnitt 0**, direkt unter der Überschrift | 38.2 — die Fundstellen-Regel |
| 2 | 871 | **Abschnitt 10, Punkt 4**, eingerückt, ohne Leerzeile | 38.4 — *„Form steht fest, Vollzug steht aus"* |
| 3 | 896 | **Punkt 7**, unter der Marke aus 37.5 (die zeichengleich bleibt) | 38.5 — der Ort steht schon (`registerdaten.py`) |
| 4 | 920 | **Punkt 9**, unter der Marke aus 37.5 | 38.5 — neun Importe statt überwachter Kopien |
| 5 | 928 | **Punkt 9**, darunter | 38.7 (b) — Slippage 9/9, 0,30 % |
| 6 | 1001 | **10.1**, unter dem Absatz zum append-only-Protokoll | 38.3 — kein Amendment, kein Protokolleintrag |
| 7 | 3196 | **21.9**, unter der Betreiberentscheidung | 38.3 |
| 8 | 3218 | **21.9**, unter der Tabelle der Folgen (wo der rote Test geführt wird) | 38.7 (d) — Absturz, 163/2, **offene Frage** |
| 9 | 3753 | **23.7**, unter dem Nachtrag TB-71 | 38.7 (d) — **offene Frage** |
| 10 | 5884 | **35.1**, unter der bestehenden Marke aus 36.1 (4)/36.3 | 38.1 — Weg (A) |
| 11 | 5893 | **35.1**, darunter | 38.7 (a) — Z. 338/460 seit `4daa254`; zugleich Beleg für 38.2 |
| 12 | 5900 | **35.1**, darunter | 38.7 (c) — Weg (B) hätte Sperrlistenpunkt 5 berührt |
| 13 | 6458 | **37.4**, direkt unter Fables Tatsachennotiz | 38.6 — ERSETZT (Z. 51; acht statt fünf) |
| 14 | 6526 | **37.5**, direkt unter dem Registertext (1)–(4) | 38.5 — Entscheidung zu (2) und (3) |

Abschnitt 38 selbst beginnt auf Z. 6616.

## 4. Zeichenvergleich je Blockzitat

`zeichenvergleich.py` → `zeichenvergleich.txt`: je Zitat die Quellzeile und die
Registerzeile (ohne vorangestelltes `> `, wo die Quelle keines hat) in zwei
Dateien, dann `diff`.

| Quelle Z. | Eintrag | Zeichen | `diff` |
|---|---|---|---|
| 33 | 38.1 Befund | 251 | rc 0, gleich |
| 37 | 38.1 Entscheidung (Berichtigung zu 35.1) | 626 | rc 0, gleich |
| 39 | 38.1 Quelle des Grundes | 288 | rc 0, gleich |
| 41 | 38.1 *„Zu eurem Einwand gegen (A)"* | 897 | rc 0, gleich |
| 43 | 38.1 Handwerk daraus | 294 | rc 0, gleich |
| 73 | 38.1 Unsicher | 263 | rc 0, gleich |
| 47 | 38.2 Anlass | 195 | rc 0, gleich |
| 49 | 38.2 Registertext | 337 | rc 0, gleich |
| 51 | 38.2 Quelle des Grundes | 153 | rc 0, gleich |
| 55 | 38.3 welcher Satz gilt | 654 | rc 0, gleich |
| 57 | 38.3 Tatsachennotiz | 321 | rc 0, gleich |
| 59 | 38.4 Form (ii), Ablehnung (i)/(iii) | 588 | rc 0, gleich |
| 61 | 38.4 Fertigkriterium | 259 | rc 0, gleich |
| 21 | 38.5 Entscheidung | 460 | rc 0, gleich |
| 23 | 38.5 *„Warum beseitigen und nicht überwachen"* | 633 | rc 0, gleich |
| 25 | 38.5 Zu Punkt 7 | 395 | rc 0, gleich |
| 27 | 38.5 Zu `messgroessen.py` | 196 | rc 0, gleich |
| 9 | 38.6 (a) | 236 | rc 0, gleich |
| 11 | 38.6 (b) | 198 | rc 0, gleich |
| 13 | 38.6 Ersatzsatz für 37.4 | 384 | rc 0, gleich |
| 15 | 38.6 Schlusssatz | 74 | rc 0, gleich |
| 29 | 38.7 (b) Messbitte | 556 | rc 0, gleich |

**22 Zitate, 0 Abweichungen.** Die Zitate wurden nicht abgetippt, sondern von
`eintrag_register_38.py` zeilengenau aus der Quelldatei eingesetzt
(Platzhalter `«Q:<zeile>»` in `abschnitt38_vorlage.md`); der Vergleich prüft
das Ergebnis unabhängig davon. Das Einfügeskript ist reproduzierbar: in einem
Wegwerf-Worktree auf `da251da` angewandt ergibt es ein byte-gleiches Register
(`cmp`).

Kurzzitate in Marken und Fliesstext (*„Ein Import ist keine Prüfung, sondern
eine **Struktur**"*, *„die Änderung ist eine Zeile"*) sind zeichengleiche
Teilstücke der Quelle; wo eine Marke den Inhalt eines Zitats nur benennt (37.4:
„acht Stellen, vier fehlend und vier zusätzlich"), steht es **nicht** in
Anführungszeichen und verweist auf den vollen Wortlaut in 38.6.

## 5. Wo 38.2 steht — und warum

**Im Kopf von Abschnitt 0 des Registers** (Marke 1), nicht bei den
Prüfprinzipien; dazu die belegende Tatsachennotiz bei 35.1 (Marke 11).

1. **Sie ist Registertext.** Fable schreibt sie als „Registertext,
   Ersteintrag"; sie bindet jeden künftigen Registertext. Registertext gehört
   in das Register — das ist append-only und geht mit seinem Hash in
   `herkunft.py::register()` ein. Die Prüfprinzipien sind ein Arbeitsdokument
   des steuernden Chats, nicht registriert, nicht append-only.
2. **Der Kopf von Abschnitt 0 ist der Durchgang.** Wer einen Registertext
   schreibt, schreibt ihn in dieser Datei; an Abschnitt 0 kommt jeder Leser und
   jeder Schreiber vorbei, bevor er einen Abschnitt öffnet. Eine Regel in
   Abschnitt 38 allein fände nur, wer bis 38 liest.
3. **Die Prüfprinzipien regeln das Prüfen, diese Regel das Schreiben.** Geprüft
   wird sie nach den Prüfprinzipien wie jeder Registertext; eine Kopie dort wäre
   eine zweite Fassung derselben Regel an einem zweiten Ort — genau das, was 21j
   und 37.5 für Werte ausschliessen.

Dieselbe Begründung steht in 38.2 im Register. Abschnitt 38 wendet die Regel
schon auf sich selbst an (Fundstellen als Datei und Funktion, Zeilennummern nur
mit Commit — ausser in Zitaten, die zeichengleich bleiben).

## 6. ⚠️ Abweichungen vom Auftrag

| | Auftrag | getan | Grund |
|---|---|---|---|
| 1 | 38.7 (b) Slippage als Tatsachennotiz „aus TB-88" (`ERGEBNIS_TB-88.md`) | ⚠️ Die Slippage-Messung steht **nicht** in `ERGEBNIS_TB-88.md` und nicht in `docs/belege/TB-88/` (`grep -i slippage`: 0 Treffer), sondern in `FABLE_ANFRAGE_2026-09-22i_…` Abschnitt 1 (steuernder Chat, HEAD `ec54618`). **Lesend nachgemessen** am Stand `da251da` (`m_slippage_backtest.txt`): 9/9 `SLIPPAGE_PCT = 0.05`, 9/9 `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)`, `t3_supertrend` mit `pnl_pct -= …` — gleich. Im Register ist die Herkunft so benannt | Eingetragen ist, was gemessen ist, mit seiner wirklichen Quelle |
| 2 | 38.2-Marke „bei 35.1 (die Tatsachennotiz zu den Zeilennummern, siehe 38.7 a)" | eine Marke für beides (Marke 11: 38.7 (a), „belegt 38.2") | Es ist dieselbe Notiz; zwei Marken mit demselben Inhalt an derselben Stelle wären eine Doppelung |
| 3 | Zitatumfang | **mehr** Zitate als verlangt: zusätzlich Fables Befund (Z. 33), Handwerk (Z. 43), Unsicherheit (Z. 73), Anlass zu 38.2 (Z. 47), Fertigkriterium (Z. 61), Messbitte (Z. 29) | Z. 43 und Z. 61 sind die beiden Stellen, an denen „grün" als Fertigkriterium steht — ohne sie hätte die offene Frage 38.7 (d) keinen Wortlaut, auf den sie sich bezieht; Z. 73 beantwortet TB-88 M1 (e) |
| 4 | „keine Sonde" (Zeiger) / „die Sonde nicht anpassen" (Auftrag §4) | Sonde **lesend** vor und nach dem Eintrag laufen lassen, nicht angepasst | Wie TB-87: die Marken in Abschnitt 10 dürfen den Listentext der Sonde nicht ändern; das ist nur durch einen Lauf zu zeigen. Die Sonde schreibt nichts |
| 5 | „Keine `.py` ändern, kein neues Modul" | zwei **Belegskripte** unter `docs/belege/TB-89/` angelegt (`eintrag_register_38.py`, `zeichenvergleich.py`) | Werkzeuge der Sitzung, kein Modul, von nichts importiert, ausserhalb des Codes — wie `m2_bezeichner_probe.py` in TB-88. Sie machen Eintrag und Vergleich wiederholbar |
| 6 | 38.6 (a) „als Tatsachennotiz zu 37.4" | Z. 51 in die ERSETZT-Marke bei 37.4 aufgenommen | Beide Berichtigungen betreffen denselben Satz; eine Marke daran |
| 7 | — | Datum des Abschnitts **23.09.2026** | Tag der Sitzung; der Auftrag wurde am 22.09. geschrieben |
| 8 | 38.4: Vollzug „hängt an zwei offenen Fragen (Anfrage 22i)" | beide benannt: „grün" (22i Abschnitt 3) **und** die Tabelle für `t3_supertrend` (22i Abschnitt 4) | Der Auftrag nennt die Zahl, nicht die Fragen; so steht es in 22i |

**Nicht beantwortet, ausdrücklich offen eingetragen:** ob „`test_vorregistrierung.py`
grün" Fertigkriterium von Plan-Punkt 8 bleibt (38.7 (d), Marken 8 und 9); welche
Tabelle für `t3_supertrend` gilt (38.4); ob `G6`/`H3` ein eigener Punkt werden.
Alle drei liegen bei Fable (Anfrage 22i).

## Offen

- **Fable:** Anfrage 22i Abschnitt 3 (grün), 4 (`t3_supertrend`), G6/H3.
- **TB-90:** Namensbildung in `faltenplan.py` (38.1), neues Kostenmodul und neun
  Importe (38.5), Ort bei Punkt 7 nachtragen, danach **ein** Abbild.
- **Plan-Punkt 8:** Vollzug von Punkt 4 in Form (ii), nach Fables Antwort.
