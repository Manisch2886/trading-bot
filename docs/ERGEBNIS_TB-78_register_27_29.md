# ERGEBNIS TB-78 — Registerabschnitte 27–29, Prüfprinzip A8, drei Arbeitsweise-Regeln (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-78_register_27_29.md` (691 Zeilen; Zeiger
`AKTUELLER_AUFTRAG.md` nannte TB-78, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `83e3a85` (= `origin/main`
beim Start, TB-77 erledigt). Geändert nur `docs/`. Commits `ee0b799`
(Schritt 0), `2848b7a` (1), `003f894` (2), `94b3b3b` (3), `2fd9498` (4),
`5d32be4` (5), `7d2f739` (6) und der Abgabe-Commit — jeder einzeln gepusht.
Belege unter `docs/belege/TB-78/`. ⭐ **Rechnet nicht. ⛔ Kein Code, keine
Sperrlisten-Datei, nichts unter `research/`, `strategies/`, `shared/`,
`snapshots/` angefasst** (Abschlussprüfung 3 und 4).

*In einfacher Sprache, zu Beginn:* Vier Entscheidungen, die am Nachmittag
feststanden, stehen jetzt im Regelwerk: was der Prüfer vor dem grossen Lauf
nicht wissen darf (27), das Stichtagsdatum und die vier Startdaten, die bisher
Platzhalter waren (28), ein verlorener Satz über die Anlaufzeit (28.6) und die
Regel, dass der Kapitalpfad am 1. Januar des ersten Auswertungsjahres beginnt
(29). Dazu ein neues Prüfprinzip und drei Regeln für den Umgang mit dem
Prüfer. Alles nur angehängt, nichts oben verändert.

---

## Schritt 0 — Sichern, was schon dastand (`ee0b799`)

| geprüft | Ergebnis |
|---|---|
| `git status --short` | genau die elf Dateien unter `docs/projektfuehrung/` plus die zwei Auftragsdateien. ⚠️ **Abweichung:** `.claude/settings.local.json` erschien **nicht** im Status — die Datei liegt vor (5003 B), ist aber über `~/.config/git/ignore` global ignoriert. Unschädlich; sie wurde nicht committet |
| `git diff --numstat -- docs/projektfuehrung/UEBERGABE_2026-09-19.md` | **`542  0`** wie verlangt; 442 → 984 Zeilen. Zusätzlich: die ersten 442 Zeilen der neuen Fassung sind `diff`-gleich mit der alten (Präfixprobe) |
| Secrets-Probe über alle 13 Dateien | 0 Treffer |
| ⚠️ `docs/auftraege/AKTUELLER_AUFTRAG.md` | `numstat` **1 / 86** — der Betreiber hat die Zeigerdatei auf eine einzige Pfadzeile reduziert (die alte Fassung trug 86 Zeilen Erklärung, darunter den Schlüsselbund-Hinweis und die Tabelle „Gültiger Auftrag"). Nicht von dieser Sitzung; im Auftrag ausdrücklich zum Commit bestellt. **Das ist die einzige Zeile mit zweiter Spalte ≠ 0 in der ganzen Aufgabe** — siehe Abschlussprüfung 1 |
| `git status --short` danach | leer |

## Schritt 1 — Registerabschnitt 27, Sichtschutz (`2848b7a`)

Angehängt ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md`, `numstat`
**65 / 0** (`docs/belege/TB-78/schritt1_numstat.txt`).

| Nachweis | Ergebnis |
|---|---|
| Zeichengleichheit 27.1–27.5 samt Tatsachennotiz gegen `FABLE_ANTWORT_2026-09-21g` Abschnitt 3 | 14 Zeilen, `diff` **leer** |
| Fable-Zitate in 27.6 / 27.7 | *„regelt den Grund, nicht den Zugriff"*, *„festgehalten, nicht bewertet"* (21g Abschnitt 4), *„Durch das Zitat kenne ich die Zeile jetzt"* (21g Abschnitt 1) — je vorhanden |
| Herkunftszahlen | `Sharpe` im Register **24** Vorkommen (24 Zeilen); `BACKLOG.md` Z. 190 = `W14`, Z. 170 = `T39.2` — treffen |
| `grep -c "27.5"` | **3** |
| Wortlaut *„keine Erwartung, Schätzung oder Prognose"* | Z. **4567** |

## Schritt 2 — Registerabschnitt 28, `asof` und Vorlauf (`003f894`)

Angehängt, `numstat` **138 / 0** (`schritt2_numstat.txt`).

| Nachweis | Ergebnis |
|---|---|
| ⭐ `RECENT_YEARS_ONLY` **aus dem Code gelesen** | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:54`, `rsi2_mean_reversion/…:52`, `turtle_soup_stocks/…:46`, `volatility_breakout/…:49` — **je `= 10`**. Auftragswert 10. Gleich; kein Abbruch. Horizontbeginn nachgerechnet: 2026-09-19 − 10 Jahre = **2016-09-19** |
| `zeitpunkt_utc` | `snapshots/63e4b6c8…/MANIFEST.json`: `2026-09-19T06:49:32+00:00`; im Register Abschnitt 18, Z. 2596. Das Manifest trägt **kein** Feld `asof` (16 Schlüssel) — 28.7 lässt es bewusst offen |
| Registertext 5a, Ergänzung | zeichengleich zu 21b Abschnitt (2), `diff` leer |
| 4a, Präzisierung, Ergänzung | zeichengleich zu 21c Abschnitt 3.1, `diff` leer |
| fünf Fable-Zitate (Datenende, Frische-Tatsache, „Nicht mit dem signierten Tag", „falsch adressiert", „derselbe Zugriff") | je **1** Treffer in 21b bzw. 21c |
| Vorlauf-Satz *„nicht gegen den ersten Kurs im Bestand"* | **genau einmal**, Z. **4307–4308** (umbrochen), im Zitat der ersetzten Fassung in 26.2 — Behauptung trifft |
| 28.1: Nachtrag nie angekommen | `Nachtrag zu TB-77` und `FABLE_ANTWORT_2026-09-21b` in `docs/ERGEBNIS_TB-77_…` und `docs/belege/TB-77/`: **0 / 0** |
| `grep -c "2016-09-19"` | vorher **0**, nachher **5** |

⚠️ **Vermerk, kein Eingriff:** 28.6 zitiert die Zählungen `Horizontbeginn` **0**
und `4a, Präzisierung` **0**. Das ist die TB-77-Messung **vor** Abschnitt 26
(im Register selbst Z. 4310 so dokumentiert). Heute stehen **9** bzw. **3**
Treffer — alle innerhalb von Abschnitt 26, keiner davor. Die Aussage „die
Fassung vom 20.09. war nie Registertext" bleibt richtig; der Wortlaut wurde
wie bestellt eingetragen, nicht nachformuliert.

## Schritt 3 — Registerabschnitt 29, Beginn des Kapitalpfads (`94b3b3b`)

Angehängt, `numstat` **73 / 0** (`schritt3_numstat.txt`). ⭐ **Die zwei
Messungen aus dem Auftrag selbst wiederholt** (`C1`), am Stand `83e3a85` und
am Stand nach Schritt 2 — beide gleich (`schritt3_messung_29_2.txt`):

| Muster | Zählung 1 (`grep`, dieselbe Zeile) | Zählung 2 (python, ±1 Zeile Kontext, zusätzlich „beginnt") |
|---|---:|---:|
| `Startkapital` | **0** | **0** |
| `Kapitalpfad` gesamt | 19 Zeilen | — |
| `Kapitalpfad` + Beginn/Start/1. Januar/erste Falte | **1** — Z. 4296 (Schadensbeschreibung) | **2** — Z. 4296 und Z. 4288 (Zitat des (d)-Grundes *„verändern das Kapital, mit dem die erste Falte beginnt"*, ebenfalls Schaden, keine Regel) |

Alle 19 `Kapitalpfad`-Zeilen gesichtet (60, 448, 1106, 1116, 1820, 2054, 3418,
3422, 3535, 3675, 3677, 3683, 3730, 3745, 3804, 4267, 4288, 4296, 4489): keine
regelt den Beginn — 1820 ist Registertext 7 (Backtester-Prüfung), 1106/1116/
3745/3804 die MtM-Reihe, der Rest Verweise und Befunde. ⇒ **Neuaufnahme**,
Abbruchkriterium 3 nicht ausgelöst. Die fünf Zitate aus 21c Abschnitt 3.2
(Registertext, Wache, „genau der Schaden", „Steht im Register bereits ein
Satz", „drei Daten nebeneinander") je 1 Treffer. `Startkapital` steht jetzt
zweimal im Register (Messtabelle 29.2, Z. 4785, und Registertext 29.3, Z. 4795).

## Schritt 4 — Prüfprinzip `A8` (`2fd9498`)

`docs/PRUEFPRINZIPIEN.md`, `numstat` **24 / 0** (`schritt4_numstat.txt`).
Vorher gemessen: `grep -nE "^### A[0-9]"` → A1 (Z. 19) … A7 (Z. 110), **A8
frei**, A5 (Z. 65) ist *„Ein Werkzeug, das nicht mehr misst, sagt es"* — der
Auftrag hatte recht. Eingefügt nach der letzten A7-Textzeile (Z. 124), vor dem
Gruppentrenner `---` und `## B` (innerhalb der Gruppe A trennen nur
Leerzeilen). Nachher A1…A8, **keine doppelt**, nichts umnummeriert. Das
21d-Zitat steht wörtlich in `FABLE_ANTWORT_2026-09-21d` (1 Treffer).

## Schritt 5 — drei Regeln in `ARBEITSWEISE.md` (`5d32be4`)

`numstat` **37 / 0** (`schritt5_numstat.txt`), nur angefügt:

| Überschrift | Ort | jetzt Z. |
|---|---|---:|
| `### ⭐ Auch Fables Fragen an den Betreiber werden ungefragt mit einer Empfehlung beantwortet` | Ende von 6d, vor `---`/`## 7` | 836 |
| `### ⭐⭐ Und dasselbe gilt für den Verfahrensprüfer — in beide Richtungen` | Abschnitt 15, hinter „Und jede Rückfrage an den Betreiber …" | 1350 |
| `### ⭐ Bei jeder Übergabe wird ungefragt gesagt, was mitgeht und was nicht` | dahinter, vor `---`/`## 16` | 1367 |

`UMZUG.md` Abschnitt 2 trägt den zitierten Satz *„Der Chatverlauf ist kein
Träger"* (Z. 53). ⚠️ Die Zählung *„neun Antworten, eine einzige Anfrage"*
betrifft die **Projektablage** und ist im Repo nicht nachmessbar; im Repo
liegen nach Schritt 0 neun `FABLE_ANFRAGE_*`-Dateien (19.–21.09.).

## Schritt 6 — Berichtigung zur TB-77-Offen-Liste (`7d2f739`)

`docs/ERGEBNIS_TB-77_horizont_je_bot.md`, `numstat` **34 / 0**
(`schritt6_numstat.txt`), Block ans Ende (Z. 194). Vorher gemessen: die
überholte Zeile *„Wache samt Mutationsprobe in `auswertung.py`"* steht in
Z. 166 (dazu 26.6-Zeile Z. 135); der 16.3/17.1-Befund in Z. 50 und Z. 145;
Fables Rücknahme in 21h (*„eine Stufe zurück"*, *„zurückgenommen"*) vorhanden.

## Schritt 7.1 — Abschlussprüfung

| | Soll | Ist |
|---|---|---|
| 1 | `numstat` zweite Spalte überall 0 | **alle 0** — ausser `docs/auftraege/AKTUELLER_AUFTRAG.md` **1 / 86** (Betreiber-Kürzung aus Schritt 0, s. o.). Register gesamt **276 / 0** (`abschluss_numstat_gegen_83e3a85.txt`) |
| 2 | `##` 26, 27, 28, 29 je genau einmal | `grep` Z. 4226 / 4550 / 4615 / 4753; zweite Zählung (python) `{26: 1, 27: 1, 28: 1, 29: 1}` |
| 3 | Sperrlisten-Hashes | `a163c498…` · `0e54ac5c…` · `4549395f…` — **unverändert**, vorher und nachher gemessen (`abschluss_sperrlisten_hashes.txt`) |
| 4 | nichts ausserhalb `docs/` | `git diff --stat 83e3a85..HEAD -- . ":(exclude)docs"` → **leer** |
| 5 | A1…A8, keine doppelt | `grep`: A1–A8, doppelt 0; zweite Zählung (python) gleich |
| 6 | `git status --porcelain` nach dem letzten Commit | siehe Abgabe-Commit — erwartet leer (`settings.local.json` global ignoriert) |
| 7 | zweite unabhängige Zählung für 2 und 5 | oben je Zeile, deckungsgleich |

Kein Basislauf, keine Datenstand-Messung, keine DB-Quersummen — wie bestellt.

## Abweichungen vom Auftrag — mit Begründung

| | Auftrag | tatsächlich |
|---|---|---|
| 1 | Status zeigt `.claude/settings.local.json` | zeigt es nicht (global ignoriert). Kein Handlungsbedarf |
| 2 | „`numstat` bei einer Datei ≠ 0 → Abbruch" | `AKTUELLER_AUFTRAG.md` 1 / 86 — vom Betreiber vor der Sitzung gekürzt, im Auftrag zum Commit bestellt; kein Löschen dieser Sitzung. **Nicht abgebrochen**, hier gemeldet. ⚠️ Mit der Kürzung sind der Schlüsselbund-Hinweis und die Tabelle „Gültiger Auftrag" aus der Zeigerdatei verschwunden — falls das nicht Absicht war, steht die alte Fassung in `83e3a85` |
| 3 | 28.6 zitiert `Horizontbeginn` 0 / `4a, Präzisierung` 0 | heute 9 / 3, alle in Abschnitt 26 — historische Messung, Wortlaut nicht angefasst |
| 4 | Belege | zusätzlich `docs/belege/TB-78/` mit je einem `numstat`-Beleg und der 29.2-Messung angelegt (Muster TB-77) |

Rückfragen an den Betreiber: **keine**.

## Fehler → Regel

Keiner dieser Sitzung. Zwei Fehler des Vorlaufs, die der Auftrag benennt und
die jetzt als Regel stehen: der Nachtrag, der TB-77 nie erreichte (28.1:
laufende Aufträge gegen jede Fable-Antwort prüfen), und die falsche
Prinzipien-Nummer `A5` (`K2i`: Nummer messen, nicht raten — hier gemessen: A8).

## ⚠️ Offen — nicht Teil dieses Auftrags

- Register-KOPIE mit Commit-Hash, Datum, KOPIE in die Projektablage (27.8) — steuernder Chat, **jetzt möglich**: alle Abschnitte stehen, HEAD = Abgabe-Commit.
- `asof`/`datenende` ins `MANIFEST.json` — Verfahrensfrage vor dem Tag (28.7), Verfahrensprüfer/Betreiber.
- TB-30b: vier Optimierer und die Wache gegen den **Beginn der ersten Falte** (29.4).
- Messung 29.5 (nur das Ob, auf KOPIE der neun DBs) — eigene Aufgabe.
- Faltenplan nach 4a — wartet auf Fables Antwort zu `FABLE_ANFRAGE_2026-09-21b` Abschnitt C.
- `RECENT_YEARS_ONLY` als registrierte Grösse — Entscheidungsvorlage (26.6 Zeile 6).
- Zeigerdatei `AKTUELLER_AUFTRAG.md`: ob die Kürzung auf eine Zeile so bleiben soll (Betreiber).
- Backlog-Zeile zu TB-78 (nächste wäre `K4s`, nach `K4r`): im Auftrag nicht bestellt, deshalb nicht angelegt — steuernder Chat oder nächster Nachtrag.

## In einfacher Sprache

Diese Sitzung hat nichts gerechnet und keinen Programmcode angefasst. Sie hat
vier Entscheidungen, die am Nachmittag zwischen dem steuernden Chat und dem
Prüfer gefallen waren, ins Regelwerk geschrieben — immer nur unten angehängt,
nie oben umgeschrieben, und jeden Schritt sofort gesichert.

Erstens: Der Prüfer darf vor dem grossen Auswertungslauf keine Ergebniszahlen
und keine Vermutungen über den Ausgang kennen; was er beim Start wusste, ist
festgehalten. Zweitens: Das Stichtagsdatum ist der 19. September 2026, der Tag,
an dem die Kursdaten eingefroren wurden. Damit haben die vier Aktien-Bots ein
festes Startdatum: 19. September 2016. Die Zahl „zehn Jahre" habe ich aus dem
Programmcode nachgelesen, nicht aus dem Auftrag abgeschrieben. Drittens: Ein
Satz über die Anlaufzeit der Indikatoren, der verlorengegangen war, gilt
weiter. Viertens: Das Kapital eines Bots beginnt am 1. Januar seines ersten
Auswertungsjahres — vorher darf kein Kauf liegen. Diese Regel steht, bevor
jemand nachmisst, ob es solche Käufe gibt.

Dazu ein neues Prüfprinzip: Wenn jemand nur selbst sagt, was er gelesen hat,
kann man das nicht prüfen — also prüft man seine Begründungen. Und drei Regeln
für den Umgang mit dem Prüfer: alles, was wir ihm schreiben, wird abgelegt;
bei jeder Übergabe wird gesagt, was mitgeht; seine Fragen an den Betreiber
bekommen ungefragt eine Empfehlung.

Eine Auffälligkeit: Die kleine Zeigerdatei, die sagt, welcher Auftrag gerade
gilt, wurde vom Betreiber vor der Sitzung auf eine Zeile gekürzt. Das war die
einzige Löschung im ganzen Vorgang, und sie war nicht meine.
