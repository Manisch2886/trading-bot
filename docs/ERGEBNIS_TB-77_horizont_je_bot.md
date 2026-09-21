# ERGEBNIS TB-77 — Der Datenhorizont wird eine Zahl je Bot: Registerabschnitt 26 und der Grenzfall (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-77_horizont_je_bot.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `1ded755` (= `origin/main` beim Start, TB-69
erledigt). Geändert nur `docs/`: `docs/VORREGISTRIERUNG_neuselektion.md` (nur
Zusätze, `numstat` **330 / 0**), dieses Dokument, ein Journalblock, eine
Backlog-Zeile, Belege unter `docs/belege/TB-77/`. Commits `9250570` (Schritt 0,
Auftrag und Zeiger des Betreibers), `2e9cdf9` (während Schritt 1: eine
Fable-Übergabe des Betreibers, getrennt), `3bc62f4` (Schritt 1), `729443c`
(Schritt 2), `fbde499` (Schritt 3) und der Abgabe-Commit. ⭐ **Rechnet nicht.
⛔ Kein Bot-Code, kein `auswertung.py`, kein `registerdaten.py`, keine
Sperrlisten-Datei angefasst** (Nachweise 8 und 9).

*In einfacher Sprache, zu Beginn:* Fable hat entschieden, dass die „letzten
zehn Jahre", auf die ein Aktien-Bot bei der Auswahl schaut, für den ganzen Bot
gelten und nicht für jedes Wertpapier einzeln — sonst handelt der Bot still in
Jahren, die niemand auswertet. Diese Regel steht jetzt im Register. Das Datum,
an dem die zehn Jahre hängen, gibt es aber noch nicht; dort steht ein
sichtbarer Platzhalter, keine erfundene Zahl. Und der Grenzfall „kein
Parametersatz besteht" ist als Kette aus vier Stellen benannt, die es alle
schon gab.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, `HEAD` = `1ded755`:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-77_horizont_je_bot.md
```

Beides vom Betreiber (mtime 16:19), ein Urheber, ein Commit `9250570`
(Zeiger TB-69 → TB-77, Planungszeile TB-74 aus der Kettentabelle entfernt,
`numstat` 3/4; Secrets-Probe 0). Während Schritt 1 kam
`docs/projektfuehrung/FABLE_UEBERGABE_2026-09-21_neuer_chat.md` hinzu
(Betreiber, mtime 16:29, 12 170 B) — getrennt committet in `2e9cdf9`, weil
sie nicht zum Auftrag gehört. ⭐ **`2e9cdf9` ist der Stand, gegen den die
Zeilenangaben der Belege messen; `1ded755` der Stand für den `numstat`.**

## Nachweis 2 — ⭐⭐ Wo überall nach `asof` gesucht wurde, und das Ergebnis je Ort

Vollständig in `docs/belege/TB-77/schritt1_blocker_nachgemessen.md`. Kurz:

| Ort | Ergebnis |
|---|---|
| alle `*.py` (ohne `trading-env/`) | 8 Zeilen, **alle pandas `merge_asof`** |
| alle `*.json` | 1 Datei (`research/backtest_defaults/results/default_scan.json`), der Eintrag `"pandas.py:merge_asof"` in einer Aufrufliste |
| das Register | 3 Zeilen — **17.1** (Registertext 5a: Herkunft *„aus dem Register, nie aus der Uhr"*, zweimal) und 25.3 (Verweis auf TB-74); **keine Zahl** |
| `research/vorregistrierung/ergebnisse/` (8 JSON) | 0 |
| Snapshot-Manifest `snapshots/63e4b6c8…/MANIFEST.json` | 15 Schlüssel, keiner `asof`; `zeitpunkt_utc` ist der Ziehzeitpunkt |
| `registerdaten.py` | 0 |
| `docs/` (`*.md`) | 11 Dateien, alle nennen `asof` als Grösse oder Formel; keine trägt einen Wert |
| `*.txt/csv/yaml/yml/toml/cfg/ini/env*`, Umgebung, `.env` | 0 / 0 / keine `.env` |

**Befund: `asof` ist nirgends als Wert gesetzt** — dasselbe wie die Messung des
Chats (16:25). ⭐ **Der Schnitt bleibt**; es wurde nicht weitergeschrieben,
bevor das feststand (Commit `3bc62f4` vor `729443c`).

## Nachweis 3 — `auswertung.py` eingefroren: Fundstellen

Register Abschnitt 0, Z. 29–31 (*„vor dem Lauf geschrieben und eingefroren:
`research/vorregistrierung/auswertung.py`"*); 15.8 Nr. 3 (*„eingefroren … Ihre
Umstellung ist TB-30b"*); 24.5 (*„bleibt es, auch ihr Docstring"*); 25.5;
Sperrliste Abschnitt 10 Nr. 5 (Z. 825); Docstring der Datei Z. 3. **Bestätigt.**

## Nachweis 4 — ⭐ Die Festlegungsnummern, selbst nachgemessen

`registerdaten.FESTLEGUNGEN` (dict, 12) mit `python3` gelesen: **10** DSR-Basis
N = 653 · **11** „DSR ist Bericht, nicht Tor — Bleibt-Geht läuft über die
Abbruchkriterien" · **12** „Es kann sein, dass kein einziger Bot die Schwelle
erreicht". Registertabelle Abschnitt 1, Z. 56–58: gleich. **Beide
Berichtigungen des Auftrags treffen** (Bleibt/Geht = 11, nicht 10; „mehrere oder
alle" = 12, nicht 11). Fables Zahlen stehen nicht im Register.

## Nachweis 5 — Abbruchkriterium (b) und Registertext 6 (b), Fundstelle je Zeile

Stand `2e9cdf9`: (b) Abschnitt 7, **Z. 686**, Präzisierung Z. 692–694; Folge
7.1 Z. 714–720; Registertext 6 (b) in 16.4, **Z. 1707–1711**; 6 (d) Rückkehr
Z. 1724–1725; 6 (a) Schatten Z. 1702–1705. ⚠️ „6b" ist keine Überschrift (`grep
-c "Registertext 6b"` = 0), sondern Buchstabe (b) von Registertext 6 — so ist
es in 26.7 geschrieben. Dazu: die Kette ist in `auswertung.py::kapitalregel`
(Z. 554–576) schon Code.

## Nachweis 6 — ⭐ Kam die 4a-Fassung vom 20.09. je in einen Registertext?

`grep -c` im Register: `Horizontbeginn` **0** · `4a, Präzisierung` **0** ·
`Im Datenhorizont" heisst` **0**. **Nie.** 25.3 und 25.5 verweisen sie an
TB-74. Folge für 26.2: es gibt keine ERSETZT-Stelle; die Marke steht als
„PRÄZISIERT" an 25.3 (i).

## Nachweis 7 — Register: `numstat` Spalte zwei = 0

`git diff --numstat 1ded755 HEAD -- docs/VORREGISTRIERUNG_neuselektion.md` =
**330 / 0** (Schritt 2: 230/0, Schritt 3: 100/0; `schritt2_numstat.txt`,
`schritt3_numstat.txt`). Vier Stellen berührt, alle nur Zusätze: Anhang
Abschnitt 26 (Z. 4226 ff.), Einfügemarke 25.3 (i), Einfügemarke 15.5 (c),
Nachtragszeile unter 24.6.

## Nachweis 8 — Sperrlisten-Hashes unverändert

Vor Schritt 2 und nach Schritt 3 gemessen:
`benchmark_drawdowns.json` **`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`**,
`faltenplan.json` **`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`**.

## Nachweis 9 — `git diff --numstat 1ded755 HEAD` je Datei, nichts ausserhalb `docs/`

```
330	0	docs/VORREGISTRIERUNG_neuselektion.md
3	4	docs/auftraege/AKTUELLER_AUFTRAG.md            (Betreiber, Schritt 0)
183	0	docs/auftraege/MAC_TB-77_horizont_je_bot.md    (Betreiber, Schritt 0)
143	0	docs/belege/TB-77/schritt1_blocker_nachgemessen.md
1	0	docs/belege/TB-77/schritt2_numstat.txt
2	0	docs/belege/TB-77/schritt3_numstat.txt
248	0	docs/projektfuehrung/FABLE_UEBERGABE_2026-09-21_neuer_chat.md  (Betreiber)
```

Dazu der Abgabe-Commit: dieses Dokument, `JOURNAL.md` (Block, nur Zusatz),
`BACKLOG.md` (eine Zeile). **0 Dateien ausserhalb `docs/`**; die vier
`multi_symbol_optimise.py`, `auswertung.py`, `registerdaten.py` unberührt.

---

## Was gebaut wurde: Abschnitt 26 (`docs/VORREGISTRIERUNG_neuselektion.md`)

| | Inhalt |
|---|---|
| Kopf | Präzisierung zu 4a Bedingung (i); F17: Quelle des Grundes ist die Regel (4a, 5e); keine Wirkung gemessen; **Herkunft nicht geglättet** — Fables Antwort vom 21.09. liegt nicht im Repo, Träger des Wortlauts ist Abschnitt 0 des Auftrags |
| 26.1 | Der Befund mit den nachgemessenen Fundstellen (Konstante 54/52/46/49, Bezug 93/93/81/88 **je Symbol** in der Ladeschleife, `fensteranker` 271–278 **je Markt**) und Fables Begründung wörtlich |
| 26.2 | Der Registertext, **zeichengleich** aus Auftrag Z. 19–26 (`diff` leer); die Fassung vom 20.09. war nie Registertext (Nachweis 6) |
| 26.3 | Tatsachennotiz zu 4d als Tabelle: fünf Krypto-Bots „kein Horizont", vier Aktien-Bots `⚠️ [PLATZHALTER — asof ist nicht gesetzt]` nach dem Muster von 23.3 (TB-66-Fassung, `fe76857`). 2016-09-01 aus 15.6 Punkt 3 ausdrücklich als **Datenuhr** abgegrenzt und nicht in die Tabelle übernommen |
| 26.4 | Ergänzung zu 3 (c), wörtlich aus dem Auftrag; Grund: die Konstante steht im Code als Survivorship-Gegenmassnahme und wäre sonst als Milderung des Vorbehalts lesbar |
| 26.5 | Herkunft: die vier `results/<bot>/multi_symbol_optimisation_results.csv` haben je einen Commit, und der Optimierer im selben Commit rechnet schon je Symbol (`0f6491b`, `f56c6d2`, `88b9050`, `b603861`) |
| 26.6 | Was folgt und nicht getan wird: `asof` setzen · 4d füllen · vier Optimierer und Wache samt Mutationsprobe → **TB-30b** · Antwort ablegen · `RECENT_YEARS_ONLY` als registrierte Grösse (Entscheidungsvorlage) · nicht gezählt, wie viele Einstiege vor einem Horizont lägen |
| 26.7 | Der Grenzfall als Kette (b) → Festlegung 11 → Registertext 6 (b) → Schatten, jedes Glied mit Fundstelle; Fables Aktenzeichen berichtigt; das fehlende Dokument nicht zitiert; die Antwort auf Frage (4): **nicht vorab messen** |
| Marken | 25.3 (i) „PRÄZISIERT durch Abschnitt 26"; 15.5 (c) „ERGÄNZT durch Abschnitt 26"; Nachtragszeile unter 24.6 (Lücke betrifft nur die TB-24-Listen; am Snapshot nachgemessen: BTC/ETH 1d ab 2017-08-17, 6 von 24 Krypto-1d-Dateien vor 2019) |

---

## Abweichungen vom Auftrag — und wo er daneben lag

| | Auftrag | gemessen / getan |
|---|---|---|
| ⚠️ | *„Register 16.3: ‚Das Bezugsdatum des Laufs (`asof`) kommt aus dem Register, nie aus der Uhr'"* | Der Satz steht in **17.1** (Registertext 5a, TB-48). 16.3 (a) ist die **ersetzte** Fassung und enthält das Wort `asof` nicht. Das Aktenzeichen **5a** im Auftrag ist richtig; in 26.2 steht 17.1 |
| ⚠️ | Der Auftrag zitiert `FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md` als Quelle | **Die Datei liegt nicht im Repo** (`find` 0). Die Anfrage bat um Ablage in der Projektablage; `FABLE_UEBERGABE…` Z. 9: *„kam als Datei zurück"* — abgelegt ist sie nirgends. Der Registertext ist aus dem Auftrag übernommen und nennt das; die Ablage steht in 26.6 als Bringschuld des steuernden Chats |
| ⚠️ | *„Registertext 6b"* | ist Registertext 6, Buchstabe **(b)**, in 16.4 — keine eigene Überschrift. So benannt |
| ⭐ | 26.7 sollte *„die Kette benennen"* | benannt — und dazu die Antwort auf Frage (4) der Anfrage (nicht vorab messen), Quelle `FABLE_UEBERGABE…` 3 (e). Sie gehört zum Grenzfall, stand sonst nirgends im Register und ist dieselbe Linie wie 24.3. **Über den Wortlaut des Auftrags hinaus, ausdrücklich benannt** |
| ⭐ | 26.3 sollte nur den Platzhalter tragen | zusätzlich die Abgrenzung zu 15.6 Punkt 3 (2016-09-01) — damit niemand die Datenuhr für den Wert hält |
| ⭐ | Auftrag nennt keine Marken in 15.5/25.3 | gesetzt, weil Abschnitte 21, 23, 25 es so halten (Regel 4: der abgelöste Text trägt den Vermerk); nur Zusätze |
| ✅ | Fables falsche Aktenzeichen | nicht übernommen, in 26.7 berichtigt (Nachweis 4) |
| ✅ | 20a nicht zitieren | nicht zitiert; genannt nur als fehlend |
| ✅ | Ein Urheber-Posten kam **während** der Sitzung hinzu (FABLE_UEBERGABE, 16:29) | getrennt committet (`2e9cdf9`), wie TB-68/69 es hielten |

## Fehler → Regel

| Fehler | Regel |
|---|---|
| Der Auftrag nannte 16.3 als Fundstelle eines Satzes, der in 17.1 steht — und ich hätte ihn übernommen, wenn `grep -n asof` nicht die Zeilennummer geliefert hätte | Ein Aktenzeichen aus einem Auftrag wird mit `grep -n` an die Zeile gebunden und die Überschrift darüber gelesen, bevor es ins Register kommt — ersetzte Abschnitte tragen den Vermerk, aber nicht mehr den Satz |
| Fables Antwort vom 21.09. hat im Repo keinen Träger; der Auftrag zitiert sie, als läge sie vor | Wird ein Dokument zitiert, misst die Sitzung zuerst, ob es liegt (`find`); liegt es nicht, nennt der Registertext den Träger, aus dem er wirklich stammt |

## ⚠️ Offen — nicht Teil dieses Auftrags

- **`asof` setzen** — Frage (1) im neuen Fable-Chat; bis dahin bleibt 26.3 ein Platzhalter, und die Faltenliste 21.4 ist in Bedingung (i) vorläufig.
- **Fables Antwort vom 21.09. ablegen** (`FABLE_ANTWORT_2026-09-21a_…`) — steuernder Chat; sie liegt in keinem Träger.
- **TB-30b:** vier Optimierer (`entry_cutoff` je Bot aus dem Register), Wache samt Mutationsprobe in `auswertung.py`.
- **Entscheidungsvorlage:** `RECENT_YEARS_ONLY` als registrierte Grösse in `registerdaten.py` — oder Codekonstante bleiben (vgl. `T56b.6`).
- **Projektablage** nachziehen (`K4e`) — steuernder Chat.
- `AKTUELLER_AUFTRAG.md` zeigt weiter auf TB-77; die Zeile wird beim nächsten Auftrag ersetzt (Betreiber).

## In einfacher Sprache

**Was entschieden ist:** Die „letzten zehn Jahre", auf die ein Aktien-Bot bei
der Auswahl schaut, gelten künftig für den ganzen Bot — nicht für jedes
Wertpapier einzeln. Sonst handelt er in Jahren, die offiziell gar nicht
ausgewertet werden, und verändert damit still das Startkapital des ersten
Jahres. Das steht jetzt wörtlich im Register.

**Was dabei auffiel:** Die Regel braucht ein Stichtagsdatum, das es noch nicht
gibt — nachgesucht im ganzen Code, in allen Ergebnisdateien, im
Datenschnappschuss und im Register selbst. Und die Wache, die sie überwachen
soll, gehört in eine Datei, die eingefroren ist.

**Was diese Aufgabe deshalb getan hat:** Sie hat die Regel aufgeschrieben und
an der Stelle, wo das Datum stehen müsste, einen sichtbaren Platzhalter
gesetzt, statt eine Zahl zu erfinden. Sie hat den Grenzfall „kein
Parametersatz besteht" als Kette aus vier Regeln benannt, die es alle schon
gab. Sie hat zwei falsche Aktenzeichen und eine falsche Fundstelle nicht
übernommen. Und sie hat nichts gerechnet und keinen Bot-Code angefasst — das
ist nachgewiesen.
