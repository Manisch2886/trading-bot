# ERGEBNIS TB-71 — Das Register schliessen: der Platzhalter fällt, Festlegung 1 bekommt ihre Regel (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-71_register_schliessen.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `97cbcef` (= `origin/main` beim Start), **reine
Registerarbeit** — kein Interpreter, kein Python, keine Kursdaten, nichts unter
`research/`, nichts ausserhalb `docs/`. Alle Inhalte waren entschieden (vier
Fable-Antworten vom 20.09.2026, zwei Betreiberentscheidungen); die Sätze wurden
zeichengleich aus dem Auftrag bzw. aus den Fable-Dateien übernommen. Die
Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Im Regelwerk stand an einer Stelle ein
absichtlicher Platzhalter und an einer zweiten ein Widerspruch. Diese Sitzung
trägt den entschiedenen Satz ein, löst den Widerspruch auf — zugunsten der
täglichen Messung zum Marktpreis — und schreibt die Regel, dass die Grösse des
Unterschieds nichts entscheidet, **bevor** jemand ihn misst.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-71_register_schliessen.md
```

Zwei Dateien, beide vom Betreiber (Auftragszeiger mit TB-71 gesetzt und
TB-72/TB-73 neu geordnet; der Auftrag selbst). **Schritt 0:** beide in
`d908b73` committet und gepusht, damit kein Diff dieser Sitzung fremde Zeilen
trägt. Danach `git status --short` = 0 Zeilen (gemessen). Während der Sitzung
hat der Betreiber nicht weiter ins Repo geschrieben (gemessen: kein weiterer
ungesicherter Stand vor der Abgabe).

**Vor dem ersten Schreiben gelesen:** die vier Fable-Antworten
(`FABLE_ANTWORT_2026-09-20{,b,c,d}*.md`), die vierte Anfrage
(`FABLE_ANFRAGE_2026-09-20d_tagesreihe.md`) und die dritte
(`…20c_kapitalpfad.md`, Herkunft des Zeitachsen-Satzes), Register Abschnitt 23
vollständig, Z. 47 und 15.3 (1a), 15.4 (2a), 15.6 (Registertext 4),
`DOKUMENTATIONSSTANDARD.md` Regel 4, `ARBEITSWEISE.md` 6d, BACKLOG Abschnitt 4.

---

## Schritt (a) — der Platzhalter in 23.3 fällt (`cc096e1`)

### Die ersetzte Stelle, alter und neuer Wortlaut

Der Platzhalter lief im Register über **drei physische Zeilen** eines
umbrochenen Blockzitats (Z. 3395–3397 im Stand `d908b73`). ⚠️ *Der Auftrag
spricht von „der einen ersetzten Zeile"; gemessen sind es drei Zeilen für einen
Satz.* Entfernt wurde nur, was Platzhaltertext trug; die Satzfragmente vor und
nach dem Platzhalter (*„Menge ohne weitere Regel auskommt)."* und *„Derselbe
Benchmark gilt für die"*) stehen unverändert wieder da.

**Alt (drei Zeilen, `git diff` `-`):**

```
> Menge ohne weitere Regel auskommt). ⚠️ **[PLATZHALTER — der Satz zu Tagen,
> an denen kein Symbol handelbar ist; Fassung W oder C, siehe unten;
> Betreiberentscheidung offen]** Derselbe Benchmark gilt für die
```

**Neu (fünf Zeilen, `git diff` `+`):**

```
> Menge ohne weitere Regel auskommt). Der Benchmark einer Falte ist an genau
> den Tagen definiert, an denen mindestens ein Symbol des Bots nach 3b (b)
> handelbar ist. Ein Tag, an dem kein Symbol handelbar ist, gehört nicht zum
> Benchmark — er wird nicht mit Rendite 0 geführt, sondern gar nicht.
> Derselbe Benchmark gilt für die
```

Der Satz ist zeichengleich mit Abschnitt 2 des Auftrags und — bis auf
Umlaute/ß, die der gesendete Klartext nicht trug — mit
`FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`, Z. 84–87 (gemessen mit `grep`).

### Was darunter neu steht (angehängt, nichts entfernt)

| Block | Inhalt |
|---|---|
| ⭐ *„Geschlossen in TB-71"* | Herkunft der drei Fassungen: Fables erste („tragen Rendite 0", zurückgezogen: Mechanismus statt Prinzip, `…20b_kalender.md` Teil 2), seine zweite (Kalender des Bot-Kapitalpfades — den es nicht gibt, `shared/zuteilung.py:720–735`), die dritte aus `FABLE_ANFRAGE_2026-09-20c`, von ihm übernommen mit dem Satz *„Meine Fassung hat einen Kalender vorausgesetzt, den der Kapitalpfad nicht hat; eure setzt nichts voraus."* |
| **Tatsachennotiz** | zeichengleich aus Abschnitt 2 des Auftrags: erster Kurstag je Falte ausgelassen (`pct_change`), Abweichung höchstens ein Tag je Falte, Wirkung null über 78 × 100 (TB-66, Nachweis 4 — dort gemessen: *„0 abweichende Stufen"*, Z. 112), `fillna(0)` wäre eine Berichtigung des Codes an den Satz |
| **`handelstage`** | bleibt unverändert die W-Spalte — die Länge des gemeinsamen Kalenders |
| Marke vor der W/C-Tabelle | `> ⚠️ **ERSETZT (TB-71, 20.09.2026) durch den Satz zur Zeitachse oben — keine der beiden Fassungen ist gewählt worden.**` — die Tabelle bleibt stehen, weil sie festhält, wogegen entschieden wurde, und die Messung enthält, die C_voll ausgeschlossen hat (`t3_supertrend` 2018: 365 statt 0 Handelstage) |
| Nachtragszeile unter der 23.7-Tabelle | *(nicht im Auftrag, angehängt)*: Zeilen 1 und 2 der Tabelle („Sperrlisten-Änderung nicht vollzogen — Entscheidung W/C davor", „Formulierungsfrage nicht entschieden") sind überholt; Zeile 4 (`t3_supertrend` 2018) ist TB-72; die Bewertungsachse steht in Abschnitt 24. **Ohne die Zeile hätte 23.7 weiter behauptet, der Platzhalter bleibe** |

`numstat` Schritt (a): **45 / 3**. Kein Code, kein Lauf.

---

## Schritt (b) — Abschnitt 24: Festlegung 1 bekommt ihre Regel, vor jeder Messung (`9eab386`)

Neuer Registerabschnitt **24** am Dateiende (Z. 3660 ff.), **218 / 0**:

| Teil | was dort steht | Quelle, zeichengleich |
|---|---|---|
| Kopf | datiert angehängt, nichts entfernt; Anlass (Kapitalpfad ohne Tageskalender, Fables dritte und vierte Antwort); **Art nach F17:** Fable sagt Berichtigung des Registerwiderspruchs; weil Festlegung 1 eine Betreiberfestlegung vom 14.09. ist, **vorgelegt statt vollzogen** — Betreiberentscheidung 20.09.2026, 18:15, per anklickbarer Frage: erst die Regel, dann die Messung; Richtung der Wirkung bekannt (gegen alle neun Bots), Grösse nicht gemessen | Auftrag Abschnitt 3; `…20c` Teil 1; `…20d` Vorab |
| **24.1 Der Befund** | Fables Zitat *„Der Drawdown der Nebenbedingung wird auf einem Objekt gerechnet, das das Register ausschliesst … Sie sieht keinen unrealisierten Verlust …"*; **sieben Fundstellen** (die vier aus dem Auftrag plus Z. 47, 15.3/1a, 15.4/2a), jede vor dem Eintrag mit `sed -n` gelesen und bestätigt (Tabelle unten) | Auftrag 24.1; `…20c` Teil 1 |
| **24.2 Registertext 4, Präzisierung** | Fables Wortlaut unverändert: tägliche MtM-Reihe (1a), dieselben Tage wie der Benchmark (3b (c)); ereignisindizierter Drawdown wird berichtet, nicht bewertet. Dazu, was der Satz **nicht** ändert (Festlegung 4, 5, Abschnitt 23) | Auftrag 24.2; `…20c` Teil 1 |
| **24.3 Die Entscheidungsregel** | wörtlich: *„… die Grösse der Abweichung zur ereignisindizierten Kurve wird gemessen und berichtet und ist für die Entscheidung ohne Belang."* Dazu Fables Begründung (*„Eine Zahl, die nichts entscheiden darf, sollte nicht auf dem Tisch liegen, während entschieden wird."*) und die Warnung zu 2020/2022; was für TB-73 folgt | Auftrag 24.3; `…20d` (1) |
| **24.4 Festlegung 1** | präzisiert, nicht gestrichen — Tabelle wie im Auftrag, ergänzt um die Zeile *„Wirkung, gemessen: noch nicht — der Eintrag steht absichtlich vor der Zahl"*; Vorgeschichte `research/drawdown_reihenfolge/` (drei Begriffe, MtM nicht dabei; Commits `26bdd97`, `971c001`, `027fe2b`, alle **12.09.2026**); Fables Satz *„Erlebbar ist, was das Konto an jedem Tag zeigt …"*; Bezug zu `L1` | Auftrag 24.4; `…20d` Vorab; `BERICHT.md` Abschnitt 0 |
| **24.5 NICHT getan / was folgen muss** | kein Code, nichts gerechnet, Hashes; die drei Code-Stellen als `K4j`; Laufcode existiert nicht (Spezifikation, kein Umbau); TB-72, TB-73, Sperrlisten-Vollzug, Tag | Auftrag Abschnitt 1 und 4 |
| In einfacher Sprache + Schlusszeile | wie in den Abschnitten 21–23 | — |

**Dazu eine Marke in Abschnitt 1** *(nicht im Auftrag, angehängt, nach dem
Muster der ERSETZT-Marken in 16.7 u. a.)*: unter der Festlegungstabelle steht
`> ⭐ **Festlegung 1 PRÄZISIERT durch Abschnitt 24 (TB-71, 20.09.2026, Betreiberentscheidung 18:15) — der Wortlaut bleibt stehen.**`
Z. 47 selbst ist unverändert (gemessen: `sed -n 47p` liefert weiter *„| 1 |
Führendes Mass | **Kapital-Drawdown** aus `equity_simulation.py` |"*). ⚠️ Durch
die Marke rücken 15.3/1a von Z. 1102–1104 auf Z. 1104–1106; Abschnitt 24 nennt
die Zeilen deshalb *„im Stand `cc096e1`"*.

### Die Fundstellen aus 24.1, vor dem Eintrag gelesen (Stand `d908b73`, Code seither unverändert)

| Fundstelle | gelesen mit `sed -n` | trifft zu? |
|---|---|---|
| `shared/zuteilung.py:720–735` | Z. 731–735: `equity_curve.append({"time": zeit, "symbol": …, "pnl_pct": …, "allocation": …, "capital_after": round(capital, 2)})` im Ausstiegszweig der Zeitpunktschleife | **JA** — je Ereignis, kein Tageskalender |
| `shared/messkette.py:139–153` | `def calculate_max_drawdown(equity_df, starting_capital)`, Z. 153: `max_drawdown_ungerundet(equity_df["capital_after"], …)` | **JA** |
| `research/vorregistrierung/beispieldaten.py:24–26` | *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und nicht aus der Tagesreihe nachgerechnet wird. Das ist auch im echten Lauf so."* | **JA**, wortgleich |
| `beispieldaten.py:125` | `"kapital_drawdown_pct": float(drawdown_fn(werte, idx, f["name"], achsen))` | **JA** |
| `research/vorregistrierung/auswertung.py:246–247` | `"dd_satz": float(z["kapital_drawdown_pct"])`, `"bestanden": float(z["kapital_drawdown_pct"]) >= grenze` | **JA** |
| `auswertung.py:40–58` | Datenvertrag `zellen.csv` (… `kapital_drawdown_pct` …) und `tagesreihen/<zelle_id>.csv` (`datum, netto_rendite, exposure`) | **JA** |
| `registerdaten.py:70` | `1: ("Fuehrendes Mass", "Kapital-Drawdown aus equity_simulation.py"),` | **JA** |
| Register Z. 47 / 15.3 Z. 1102–1104 / 15.4 | Festlegung 1 / Registertext 1a / Registertext 2a | **JA** |

---

## Schritt (c) — eine Backlog-Zeile `K4j` (`295b17f`)

**K-Nummer gemessen** mit dem Muster aus dem Auftrag,
`grep -nE '^\| \*\*(K\d[a-z])\*\*'` ohne schliessenden Balken, ohne `sort -u`,
über `BACKLOG.md` **und** `BACKLOG_ARCHIV.md`: höchste vergebene Nummer der
Reihe K4 ist **`K4i`** (Z. 1412, TB-68); `K4j` vor dem Eintrag: **0** Treffer in
beiden Dateien, 0 im gesamten `docs/`-Baum. Die Zeile steht direkt nach `K4i`
in Abschnitt 4 (Z. 1413). `numstat` **1 / 0**. Inhalt: die drei Stellen (1)
`auswertung.py` Datenvertrag Z. 40–58 — eingefroren, TB-30b; (2)
`beispieldaten.py` Z. 24–26 und 125; (3) `registerdaten.py:70`
`FESTLEGUNGEN[1]`; dazu, dass der Laufcode nicht existiert (Spezifikation, kein
Umbau), dass die TB-73-Zahl nach 24.3 kein Argument ist, und der Hinweis, dass
der Halbsatz zu W/C in Abschnitt 2 (Z. 308) überholt ist.

---

## Die Nachweise 2 bis 7

| # | verlangt | gemessen |
|---:|---|---|
| **2** | Register `numstat` Spalte zwei = 0, Platzhalter einzige Ausnahme | `git diff --numstat d908b73 HEAD -- docs/VORREGISTRIERUNG_neuselektion.md` → **263 / 3**; die drei entfernten Zeilen sind vollständig oben abgedruckt, alle drei tragen `[PLATZHALTER`-Text; `git diff … \| grep '^-'` zeigt keine weitere |
| **3** | SHA-256 beider Benchmark-Tabellen unverändert | vorher **und** nachher: `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` (`benchmark_drawdowns.json`), `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` (`benchmark_drawdowns_vt.json`). ⚠️ Der Auftrag nennt den Pfad `ergebnisse/…`; die Dateien liegen unter `research/vorregistrierung/ergebnisse/` (mit `find` gesucht; `shasum` auf `ergebnisse/…` meldet *No such file*) |
| **4** | kein Python; nichts unter `research/` | **kein Python ausgeführt — auch nicht für Nachweis 5, der ein `grep` ist**; `git diff --numstat 97cbcef HEAD -- research/` → **0 Zeilen**. Die Fundstellen wurden mit `sed -n` gelesen |
| **5** | `grep -c '\[PLATZHALTER'` im Register = 0 | vorher **1**, nachher **0** |
| **6** | Backlog `numstat 1 0`, K-Nummer nirgends doppelt | **1 / 0**; `grep -c '\*\*K4j\*\*'`: `BACKLOG.md` **1**, `BACKLOG_ARCHIV.md` **0** |
| **7** | nichts ausserhalb `docs/` | `git diff --name-only 97cbcef HEAD \| grep -v '^docs/'` → **0** Dateien. Geändert: `docs/VORREGISTRIERUNG_neuselektion.md`, `docs/projektfuehrung/BACKLOG.md`, dieses Dokument, der Journal-Nachtrag (i); vom Betreiber: `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/auftraege/MAC_TB-71_register_schliessen.md` |

**Die harten Auflagen aus Abschnitt 6:** kein Wortlaut erfunden (die Sätze in
23.3 und 24.2/24.3 sind zeichengleich mit dem Auftrag; die längeren
Fable-Zitate zeichengleich mit den Fable-Dateien, Auslassungen als „…" wie im
Auftrag); nichts entfernt ausser dem Platzhalter; `auswertung.py` unberührt
(auch Docstring — `git diff` unter `research/` leer); drei Commits plus
Schritt 0 und Abgabe, je gepusht; `git push` stets allein aufgerufen;
Entscheidungen an den Betreiber: **keine nötig** — alle Inhalte waren
entschieden, die Sitzung hat keine Frage gestellt.

---

## Wo der Auftrag daneben lag — und was die Sitzung dazu getan hat

| Stelle im Auftrag | Befund | getan |
|---|---|---|
| Nachweis 2: *„die eine ersetzte Zeile"* | der Platzhalter lief über **drei** physische Zeilen | alle drei einzeln nachgewiesen (oben); nichts sonst entfernt |
| Nachweis 3: Pfad `ergebnisse/benchmark_drawdowns.json` | liegt unter `research/vorregistrierung/ergebnisse/` | dort gehasht; beide Hashes wie verlangt |
| Nachweis 4: *„Kein Python ausgeführt ausser Nachweis 5"* | Nachweis 5 ist ein `grep` | gar kein Python ausgeführt |
| 24.4: Vorgeschichte *„am 12./13.09."* | alle drei Commits von `research/drawdown_reihenfolge/` sind vom **12.09.2026** | im Register „12.09.2026" mit den drei Hashes |
| Schritt (a) nennt nur 23.3 | 23.7 hätte weiter behauptet, der Platzhalter bleibe; Abschnitt 1 hätte Festlegung 1 ohne Hinweis auf 24 gezeigt | je eine angehängte Nachtragszeile/Marke, nach dem Muster der bestehenden ERSETZT-Marken; nichts entfernt |
| Nachweis 6: *„nur eine Zeile"* im Backlog | der Halbsatz *„vor dem Vollzug steht die Entscheidung W/C aus Register 23.3"* (Abschnitt 2, Z. 308) ist seit Schritt (a) überholt | **nicht geändert** (Auflage 1/0); in `K4j` benannt, unten als offen geführt |
| 24.1-Tabelle: `zuteilung.py:720–735` | der `append` steht in Z. 731–735; 720–735 umfasst ihn | Bereich beibehalten, im Register präzisiert („je Ereignis (Ausstieg)") |
| Betreiberentscheidung 18:15 | im Repo nur im Auftrag überliefert (die vierte Fable-Antwort kennt nur die 18:06-Entscheidung, die *„erneut vorgelegt"* wird) | Abschnitt 24 zitiert die Quelle ausdrücklich: *„überliefert in `docs/auftraege/MAC_TB-71_register_schliessen.md`, Abschnitt 3"* |

---

## Offen — nichts davon gehört zu diesem Auftrag

| | wer |
|---|---|
| **TB-72** — `t3_supertrend` beginnt 2019 (21.3 (b) bindet) plus `faltenplan.py` leitet die erste Falte aus dem Trockenlauf ab; Wirkung bekannt (`DD_Toleranz` −45,16 → −48,10 bei 100 %). ⚠️ **rechnet** | nächster Auftrag |
| **TB-73** — MtM-Wirkung messen, je Bot, Forschungsskript ausserhalb des Laufcodes; Ergebnis in Register 24.4 nachtragen, **nie in eine Entscheidung** (24.3) | nach TB-72 |
| Vollzug der Sperrlisten-Änderung (Register 21.9): W/C ist gegenstandslos, es braucht nur noch die Betreiberfreigabe; dabei `registerbericht.py:178` auf `symbole_handelbar_in_falte` (23.5) | Betreiber |
| `BACKLOG.md` Abschnitt 2, Z. 308: Halbsatz zu W/C nach Regel 9 ändern | nächste Backlog-Pflege |
| `K4j` — die drei Code-Stellen, sobald der Laufcode geschrieben wird | TB-30b |
| Journal-Nachtrag (i) einarbeiten (Block nach `BV`) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): Register, Backlog | steuernder Chat / Betreiber |
| `AKTUELLER_AUFTRAG.md`: TB-71-Zeile schliessen, wenn nachgemessen | Betreiber |

---

## Commit-Liste

| Commit | Schritt |
|---|---|
| `d908b73` | Schritt 0 — zwei Betreiber-Dateien gesichert (Auftragszeiger, Auftrag) |
| `cc096e1` | Schritt (a) — Platzhalter in 23.3 gefallen, Herkunft, Tatsachennotiz, `handelstage`, Marke ERSETZT, Nachtragszeile 23.7 (45/3) |
| `9eab386` | Schritt (b) — Abschnitt 24 und Marke in Abschnitt 1 (218/0) |
| `295b17f` | Schritt (c) — `K4j` (1/0) |
| `b3b37f0` | Abgabe — dieses Dokument und `JOURNAL_NACHTRAG_2026-09-20i.md` |

Alle Commits direkt auf `main`, je einzeln gepusht.

---

## In einfacher Sprache

**Was schiefstand:** Im Regelwerk stand an einer Stelle ausdrücklich ein
Platzhalter — eine Lücke, die absichtlich offen gelassen wurde, bis entschieden
ist. Und an einer zweiten Stelle widersprachen sich zwei Regeln: Die eine sagte,
der Verlust eines Bots wird täglich zum Marktpreis gemessen; die andere nannte
ein Programm, das nur bei Käufen und Verkäufen misst.

**Was diese Sitzung gemacht hat:** Sie hat den entschiedenen Satz eingetragen
(ein Tag, an dem der Bot nichts handeln kann, gehört nicht zum Vergleichskorb —
er zählt nicht als Null, er zählt gar nicht) und den Widerspruch aufgelöst —
zugunsten der täglichen Messung, weil nur die zeigt, was das Konto an einem
Tag wirklich wert ist. Das alte Mass wird weiter berichtet, es entscheidet nur
nichts mehr.

**Und sie hat eine Regel geschrieben, bevor gemessen wird:** dass die Grösse des
Unterschieds für diese Entscheidung keine Rolle spielt. Das ist der Kern —
eine Zahl, die nichts entscheiden darf, soll nicht auf dem Tisch liegen,
während entschieden wird. Gemessen wird danach, in einer eigenen Aufgabe.

**Was nicht passiert ist:** Kein Programm wurde geändert, nichts wurde
gerechnet, die beiden Tabellen mit den Vergleichswerten sind Byte für Byte
dieselben. Im Regelwerk wurde nichts gelöscht — ausser dem Platzhalter, der
genau dafür da war.
