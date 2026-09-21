# ERGEBNIS TB-81 — Der Faltenplan als Registertext, und die abschliessende Feldliste des Abbilds (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-81_faltenplan_als_registertext.md` (Zeiger
`AKTUELLER_AUFTRAG.md` Z. 39 nannte TB-81, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `0509c5e` (= `origin/main`
beim Start), macOS 15.7.9; Messungen mit `/usr/bin/python3` **und**
`trading-env/bin/python3`, beide **3.9.6**, Ausgaben gleich. Commits `955dced`
(Schritt 0), `a0c6eb0` (1), `5ff34a4` (2) und der Abgabe-Commit — jeder einzeln
gepusht. Belege `docs/belege/TB-81/`. Geändert: **nur `docs/`** — das Register
(append-only), vier Belegdateien, dieses Dokument, ein Journalblock. ⛔ **Kein
Code, keine Abbild-Datei, keine Sonde, keine Sperrlisten-Datei, kein
`faltenplan.py`, nichts unter `research/`, `strategies/`, `shared/`,
`snapshots/`.**

*In einfacher Sprache, zu Beginn:* Welche Jahre bei welchem Bot ausgewertet
werden, stand bisher nur in einer Datei. Jetzt steht es als Text im Regelwerk
(Abschnitt 33), gemessen aus der Datei und zweimal unabhängig gezählt. Dazu
steht jetzt abschliessend fest, welche Felder die maschinenlesbare Fassung
tragen muss — genau diese, keins mehr, keins weniger. Die Datei selbst wurde
**nicht** erzeugt; das kommt nach der Prüfung durch den Verfahrensprüfer und mit
eigener Freigabe.

---

## Schritt 0 — Sichern und Ausgangsstand (`955dced`)

| | Ergebnis |
|---|---|
| `git status --short` beim Start | **leer.** `FABLE_ANTWORT_2026-09-21k_abbild_schema.md` lag bereits versioniert in `0509c5e` (der steuernde Chat hatte sie mit dem Auftrag abgelegt); nichts vom Betreiber unversioniert, also nichts mitzucommitten — der Schritt-0-Commit trägt nur den Beleg |
| `grep -cE "^## 33\."` vor dem Eintrag | **0** (Abbruchkriterium 1 nicht eingetreten) |
| Drei Sperrlisten-Hashes, voller Pfad | `research/vorregistrierung/ergebnisse/faltenplan.json` `0e54ac5c…` · `…/benchmark_drawdowns.json` `a163c498…` · `…/benchmark_drawdowns_vt.json` `4549395f…` |
| Dazu die zwei Nachbardateien | `faltenplan_tb72.json` `19e8cbca…` · `faltenplan_tb80.json` `2dd28291…` |
| `faltenplan*.json` im Repo | **acht** (ohne `trading-env/`), nicht sechs wie im Auftrag — Liste im Beleg; gemessen wurden die drei Sperrlisten-Dateien und die zwei unter `ergebnisse/` |

Beleg: `docs/belege/TB-81/schritt0_ausgangsstand.txt`.

## Schritt 1 — Die Zahlen selbst gemessen (`a0c6eb0`)

**Quelle:** `research/vorregistrierung/ergebnisse/faltenplan_tb80.json`
(SHA-256 `2dd28291…`), **nicht** der Auftrag (`C1`). Das Messskript (nur
`json`/`hashlib`) ist im Beleg eingebettet, **nicht** als eigene Datei abgelegt.

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| `elliott_wave` | krypto | kein Horizont (`null`) | 2 | 2018-2019 | 2018-2019, 2020-2021, 2022-2023, 2024-2025 | 4 |
| `t3_supertrend` | krypto | kein Horizont (`null`) | 1 | 2019 | 2019 … 2025 | 7 |
| `rsi2_crypto` | krypto | kein Horizont (`null`) | 1 | 2019 | 2019 … 2025 | 7 |
| `turtle_soup_crypto` | krypto | kein Horizont (`null`) | 1 | 2018 | 2018 … 2025 | 8 |
| `volatility_breakout_crypto` | krypto | kein Horizont (`null`) | 1 | 2018 | 2018 … 2025 | 8 |
| `elliott_wave_stocks` | aktien | 2016-09-19 | 1 | 2017 | 2017 … 2025 | 9 |
| `rsi2_mean_reversion` | aktien | 2016-09-19 | 1 | 2018 | 2018 … 2025 | 8 |
| `turtle_soup_stocks` | aktien | 2016-09-19 | 1 | 2017 | 2017 … 2025 | 9 |
| `volatility_breakout` | aktien | 2016-09-19 | 1 | 2018 | 2018 … 2025 | 8 |

| Prüfung | Ergebnis |
|---|---|
| Zweite, unabhängige Zählung aus `falten` (`rolle == "selektion"`): Namen, Anzahl, erste Falte aus `von`, Faltenlänge aus `von`/`bis_ausschliesslich` | **0 Abweichungen** in neun Bots (Abbruchkriterium 3 nicht eingetreten) |
| Gegen **Register 21.4** (erste Falte, # Selektionsfalten, Faltenlänge; die neun Tabellenzeilen wörtlich per `grep` im Beleg) | **0 Abweichungen** (Abbruchkriterium 4 nicht eingetreten) |
| Gegen die im Auftrag genannten Listen (nur `elliott_wave` und die Bestätigungsperioden sind dort genannt) | gleich (Abbruchkriterium 2 nicht eingetreten) |
| Zusatz: aufsteigend und lückenlos (`bis` der Falte *n* = `von` der Falte *n+1*), Faltenlänge je Bot einheitlich, einzige Bestätigungsfalte beginnt am Ende der letzten Selektionsfalte und endet am `go_live_schnitt` `2026-09-01`; keine andere Rolle als `selektion`/`bestaetigung` | **alle neun: ja** |
| Feldmenge der Datei | je Bot **18 Felder**, alle neun gleich; oberste Ebene nur die neun Bot-Namen — **kein `asof`, kein `quelle`** |

**Befunde am Rand (kein Abbruchgrund):**

1. `horizontbeginn` ist bei den fünf Krypto-Bots als JSON-`null` **gesetzt**
   (Schlüssel vorhanden), bei den vier Aktien-Bots `2016-09-19`. Ob `null` als
   das ausdrückliche „kein Horizont" aus 33.3 gilt oder ein String gewählt
   wird, ist Handwerk der Abbild-Datei — hier nur festgehalten.
2. `t3_supertrend`: `erste_falte = 2019`, `erste_falte_4a = 2018` — die
   Konjunktion aus 25.3 hebt die erste Selektionsfalte auf 2019 (Trockenlauf in
   2018: 0 Symbole), genau der in 21.4 beschriebene Fall. Die Tabelle nennt die
   erste **Selektions**falte.

Beleg: `docs/belege/TB-81/schritt1_faltenlisten.txt`.

## Schritt 2 — Registerabschnitt 33 (`5ff34a4`)

Ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md`, ab **Z. 5304**,
**146 / 0** (append-only). Inhalt nach Auftrag: 33.1 Berichtigung zu 30.2 (3)
(der Satz bleibt dort zeichengleich stehen, gilt als ERSETZT), 33.2 der
Registertext des Faltenplans mit der **gemessenen** Neun-Zeilen-Tabelle, 33.3
Fables Ersatztext und die Feldliste, 33.4 die zwei Anpassungen und die Antwort
auf seine Unsicherheit, 33.5 was nicht getan wird.

| Nachweis | Ergebnis |
|---|---|
| 1 `numstat` | `146 0` |
| 2 `^## 33\.` | genau einmal, Z. 5304 — `grep -c` **1**, `awk` **1** |
| 3 Tabelle 33.2 gegen Schritt 1 | neun Zeilen, dritte Lesung direkt aus der JSON gegen die Registerzeilen: **9/9 identisch** |
| 4 Zeichengleichheit gegen Fable 21k | Ersatztext (ganzer Absatz) **ja**; 30.2 (3)-Satz im Register vor 33 genau einmal und in 21k **ja**; Grund-Zitat (Blockzitat) **ja**; die vier kurzen Zitate **ja** |

Beleg: `docs/belege/TB-81/schritt2_nachweise.txt`.

## Schritt 3 — Abschlussprüfung (`schritt3_abschluss.txt`)

| | zu prüfen | Soll | Ist |
|---|---|---|---|
| 1 | `numstat` je Datei, `0509c5e..HEAD` | zweite Spalte 0 überall | **0 überall** (Register 146/0, drei Belege 30/0, 168/0, 30/0; dieser Abgabe-Commit fügt nur hinzu) |
| 2 | Nichts ausserhalb `docs/` | leer | **leer** |
| 3 | Drei Sperrlisten-Hashes | unverändert | `0e54ac5c…` · `a163c498…` · `4549395f…` **unverändert** (Abbruchkriterium 5 nicht eingetreten) |
| 4 | `faltenplan_tb80.json`, `faltenplan_tb72.json` | unverändert | `2dd28291…` · `19e8cbca…` **unverändert**, 0 Commits auf beide seit Ausgang |
| 5 | Registerabschnitte | 26…33 je genau einmal | **je 1** (grep und awk), höchste Nummer 33 |
| 6 | `git status --porcelain` nach dem letzten Commit | nur `.claude/settings.local.json` | **leer** — die Datei existiert in diesem Arbeitsbaum nicht (Start war sauber); gemessen nach dem Abgabe-Commit, Ausgabe unten im Beleg nachgetragen |

## Abweichungen vom Auftrag — mit Begründung

| | Abweichung | Begründung |
|---|---|---|
| 1 | Schritt-0-Commit enthält **nichts vom Betreiber**, nur den Beleg | Arbeitsbaum war leer; Fable 21k lag schon in `0509c5e`. Abbruchkriterium 6 damit nicht eingetreten |
| 2 | 33.2: Platzhalter `<Stand/Commit>` und `<deiner>` gefüllt mit Datei-Commit `cadb968`, Sitzungs-HEAD `a0c6eb0` und `2dd28291…`; dazu Zeiger auf den Beleg und die zwei Zählungen | so verlangt („mit deinen gemessenen Werten") |
| 3 | 33.2: eine **Lesehilfe** unter der Tabelle (`null` = „kein Horizont", Go-Live-Schnitt, `t3_supertrend` 2018→2019) | Tatsachen aus der Messung, die die Tabelle sonst offen lässt — insbesondere, dass „kein Horizont" in der Datei ein `null` ist (33.3 verlangt „gesetzt, nicht weggelassen") |
| 4 | 33.2: ein **Zitierhinweis** zu „Trockenlauf nach 3b (b)" | Gemessen: In 16.7 ist **3b (a)** der Trockenlauf-Satz, **3b (b)** die `MIN_HISTORY_*`-Tabelle; 21.3 (a), 21.4 und `erste_falte_quelle` zitieren 3b (a). Der Wortlaut stammt aus 30.2 (2) und bleibt (append-only); ohne Hinweis sucht ein Leser nach einem zweiten Trockenlauf. Nicht angeglichen — ob Fable 30.2 (2) berichtigt, ist seine Sache (siehe Offen) |
| 5 | 33.3: das *Fable:*-Zitat zu „Folge der Regel" steht als **zwei wörtliche Sätze**, nicht als ein Satz | Der Satz im Auftrag war aus zwei Stellen von 21k (Z. 33 ohne Klammer, Z. 31 Ende) zusammengezogen und in der Form **nicht** zeichengleich; die Register-Fassung ist es (Nachweis 2.4). Inhalt unverändert |
| 6 | 33.3: ein Satz *„Nachgemessen (TB-81) … 18 Felder, weder `asof` noch `quelle`"* | Die Folgerung „keine der drei ist das Abbild" bekommt damit für `faltenplan_tb80.json` eine Messung statt einer Übernahme (`C1`) |
| 7 | Messskript **nicht** als `.py` unter `docs/belege/`, sondern eingebettet im `.txt` | Auftrag: „kein Code, keine Sonde". Nachlaufbar aus dem Beleg; beide Pythons 3.9.6 liefern die gleiche Ausgabe |
| 8 | `JOURNAL.md` liegt unter `docs/projektfuehrung/`, nicht unter `docs/` | Pfad gemessen; Block **CI** (letzter war CH) vor `## Wiederkehrende Lehren` |
| 9 | Abschlussprüfung 6: Status **leer** statt „nur `.claude/settings.local.json`" | Die Datei gibt es hier nicht; leer ist die strengere Erfüllung |
| 10 | Auftrag: „sechs Dateien `faltenplan*.json`" — gemessen **acht** | Zwei zusätzliche unter `docs/belege/TB-72/` und `docs/belege/TB-80/` (Speicherstände). Für die Hashes ohne Belang, voller Pfad überall |

## Fehler → Regel

Kein Fehler in dieser Sitzung, der eine neue Regel trüge. Bestätigt: `C1`
(Zitat aus einem Auftrag ist so zu prüfen wie eine Zahl — das zusammengezogene
Zitat in Abweichung 5 wäre sonst als „zeichengleich" ins Register gegangen).

## ⚠️ Offen — nicht Teil dieses Auftrags

| | | bei wem |
|---|---|---|
| 1 | **Prüfung von 33.2/33.3/33.4 durch den Verfahrensprüfer** (Fable: „ich prüfe dann Text und Feldliste zusammen") — Punkte 1 und 2 ändern seinen Wortlaut, Punkt 3 beantwortet seine Unsicherheit; 33 gilt bis dahin mit Vermerk | steuernder Chat → Fable |
| 2 | Dabei vorlegen: der **Zitierhinweis** in 33.2 (3b (b) vs. 3b (a)) und die Frage, ob `null` das ausdrückliche „kein Horizont" ist | steuernder Chat → Fable |
| 3 | **Abbild-Datei, Sonde, Sperrlistenpunkt** — eigene Aufgabe nach 1 und mit Betreiberfreigabe (33.5) | Betreiber |
| 4 | **Entscheidungsvorlage 33.5:** geänderter `faltenplan.py` oder neuer kleiner Schreiber | Betreiber |
| 5 | Unverändert offen aus TB-80: 32.5, `fensteranker` in den Messwerkzeugen, TB-30b, Journal-Nachträge (20g)–(20m), Backlog-Zeile `K4t` | — |

## In einfacher Sprache

**Was gemacht wurde:** Der Auswertungsplan — welche Jahre bei welchem Bot
geprüft werden — steht jetzt als Text im Regelwerk. Die Zahlen wurden nicht
aus dem Auftrag abgeschrieben, sondern aus der Datei gemessen, auf zwei
verschiedenen Wegen gezählt und gegen die ältere Tabelle im Regelwerk
gehalten: überall gleich. Dazu steht jetzt abschliessend fest, welche Felder
die maschinenlesbare Fassung tragen muss; ein Feld zu viel ist derselbe Fehler
wie eines zu wenig, und das kann später ein kleines Programm prüfen statt
eines Urteils.

**Was aufgefallen ist:** Ein Zitat im Auftrag war aus zwei Stellen
zusammengesetzt und stimmte so nicht Wort für Wort; im Regelwerk stehen jetzt
die zwei Sätze einzeln und wörtlich. Und ein Verweis aus einem älteren
Abschnitt zeigt auf den Nachbarabsatz statt auf den gemeinten — er bleibt
stehen, mit einem Hinweis daneben.

**Was nicht gemacht wurde:** Die Datei selbst, das Prüfprogramm und der
Eintrag auf die Sperrliste. Das kommt erst, wenn der Prüfer den Text gesehen
hat, und mit eigener Freigabe.

---

## Deine Aufgaben

1. **Fable vorlegen:** Registerabschnitt 33 (Z. 5304 ff.) mit den drei Punkten aus 33.4, dem Zitierhinweis in 33.2 und der `null`-Frage — *Wo:* `docs/VORREGISTRIERUNG_neuselektion.md`, `docs/belege/TB-81/` — *Woran:* seine Antwort wird als `FABLE_ANTWORT_2026-09-21l_…` abgelegt.
2. **Entscheiden (33.5):** geänderter `faltenplan.py` oder neuer Schreiber für die Abbild-Datei — erst nach 1.

Nicht von dir abhängig: nichts weiter aus diesem Auftrag; alle Commits sind gepusht.
