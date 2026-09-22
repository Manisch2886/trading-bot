# ERGEBNIS TB-83 — Registerabschnitt 35: die Bestätigungsperiode bekommt ihren Bezeichner und wird Feld, 30.2 (3) wird präzisiert — und die gesperrte Datei hat vor und nach der Arbeit denselben Hash (Mac-Sitzung, 22.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-83_register_35.md` (Zeiger
`AKTUELLER_AUFTRAG.md` Z. 39 nannte TB-83, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `9dac8d4` (= `origin/main`
beim Start; der Auftrag erwartete `f1a0dc7` oder jünger). Commits `c410fc1`
(Schritt 0/1), `f0fc58b` (2), `d30af22` (3), `15b87b0` (4–8) und der
Abgabe-Commit — jeder einzeln gepusht. Belege `docs/belege/TB-83/`. Geändert:
**nur `docs/`** — das Register (append- und insert-only, **172 / 0**), zehn
Belegdateien, dieses Dokument, ein Journalblock. ⛔ **Kein Code, kein
`python3 faltenplan.py`, keine Abbild-Datei, keine Sonde, kein Wrapper, kein
Hash auf die Sperrliste.**

⚠️⚠️ **M6, vorweg:** `research/vorregistrierung/ergebnisse/faltenplan.json`
(Sperrlistenpunkt 2) — SHA-256 **vor** der Arbeit
`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`, **nach** der
Arbeit **dieselbe**; mtime unverändert 14.09.2026 17:55, 0 Commits auf
`ergebnisse/`. `faltenplan.py` wurde in dieser Sitzung **nicht ausgeführt**,
nur mit `grep`/`sed` gelesen.

*In einfacher Sprache, zu Beginn:* Die „Bestätigungsphase" hat jetzt einen
eindeutigen Namen — ihre Zeitspanne, `2026-01-01/2026-09-01` — und gehört in
die maschinenlesbare Datei; der Prüfer hat dafür eine frühere Aussage
zurückgenommen. Ausserdem steht jetzt, wann die Prüfsonde läuft: vor dem
Start, mit Abbruch bei Abweichung. Alles nur Text; keine Zahl bewegt, die
gesperrte Datei unangetastet — beides gemessen.

---

## Schritt 0 — Ausgangsstand (`c410fc1`)

| | Ergebnis |
|---|---|
| `git status --short` beim Start | **leer.** `FABLE_ANTWORT_2026-09-22a_…` und `FABLE_ANFRAGE_2026-09-22a_…` lagen schon in `9dac8d4` — nur geprüft |
| `grep -cE "^## 35\."` | **0** (Abbruchkriterium 6 nicht eingetreten); höchste `##`-Nummer 34; Register 5667 Zeilen |
| Drei Sperrlisten-Hashes | `0e54ac5c…` · `a163c498…` · `4549395f…`, voller Pfad im Beleg |
| Schlüsselbund / „Claude Max" | Handgriff des Betreibers vor dem Start; von der Sitzung nicht messbar |

## Schritt 1 — M1 bis M6 „vorher" (`c410fc1`)

| # | Messung | erwartet | **gemessen** |
|---:|---|---|---|
| **M1** | 21.4 „Bestätigung ab" | `2026-01-01` bei allen neun | **9/9** (Tabellenkopf per `grep` in Z. 2917 verankert, Datenzeilen 2919–2927). Die Zelle bei `elliott_wave` lautet wörtlich `⚠️ **2026-01-01**`; 21.4 trägt keinen Satz, der die Markierung begründet — nur gemessen, nicht gedeutet (Fable bat in 22a um den ganzen Eintrag) |
| **M2** | 5.2 Go-Live-Schnitt | `2026-09-01`, ausschliesslich | **`2026-09-01`, ausschliesslich** (Z. 582); 21.4 wiederholt es im Vorsatz (Z. 2914) |
| **M3** | `fp.faltenplan` in `auswertung.py` | 1 Treffer, Z. 589 | **1 Treffer, Z. 589** (`plan = fp.faltenplan(mess)`; `import faltenplan as fp` Z. 96). Einzige geöffnete Plandatei: `benchmark_drawdowns.json` Z. 590 — keine `faltenplan*.json`. Der Schlüssel: Z. 432 `name = plan[bot]["bestaetigungsperiode"]`, weitergereicht Z. 550, 638 |
| **M4** | `bestaetigungsperiode` in `faltenplan.py` | 2 Treffer, 336 und 369 | **2 Treffer, Z. 336 und Z. 368** — ⚠️ die Ausgabezeile ist **368** (`best = p["bestaetigungsperiode"]`), nicht 369 (das ist die `print`-Zeile darunter); Auftrag und Anfrage 22a nannten 369. Zahl der Fundstellen bestätigt. Die Falle Z. 372–377 (`main()` schreibt nach `ergebnisse/faltenplan.json`) wörtlich im Beleg — nur gelesen |
| **M5 vorher** | Faltenliste 33.2 | — | neun Zeilen, SHA-256 `e5ab322e…` (= TB-82) |
| **M6 vorher** | Hash `ergebnisse/faltenplan.json` | `0e54ac5c…` | **`0e54ac5c…`**, mtime 14.09. 17:55 |

Belege: `m1_bestaetigung_ab.txt` … `m6_sperrlisten_hash.txt`, Befehl in Zeile 1.

## Schritt 2 — Registerabschnitt 35 (`f0fc58b`)

Ans Ende des Registers, **152 / 0**. Die vier Fable-Texte und ihre Begründungen
per `sed` aus 22a gezogen, nicht abgetippt.

| Eintrag | Z. (Stand nach Schritt 3) | Inhalt |
|---|---|---|
| **35.1** | 5713 | Ergänzung zu 33.2 — Bestätigungsperiode als Datumsspanne, Bezeichner `JJJJ-MM-TT/JJJJ-MM-TT`, für alle neun `2026-01-01/2026-09-01` (aus M1/M2 gebildet); der heutige Faltenname in `faltenplan.py:336` ausdrücklich als unzulässig eingetragen, Umstellung nicht Teil von TB-83 |
| **35.2** | 5754 | Ergänzung zu 33.3 — Feld `bestaetigungsperiode`, positive Prüfung |
| **35.3** | 5768 | Fables sechste Rücknahme — ersetzt 33.4 Punkt 3 und den Schluss von 34.6; Tatsachennotiz M3 (der Schlüssel in `auswertung.py:432`) |
| **35.4** | 5797 | Präzisierung zu 30.2 (3) — Sonde prüft den gerechneten Plan vor dem Start, Wrapper bricht ab; Tatsachennotiz M3 |
| 35.5 | 5823 | Was nicht getan wird, mit M6 und Fables offener Unsicherheit (Fundstellen des Bezeichners) |

| Nachweis | Ergebnis |
|---|---|
| `numstat` | `152 0` |
| `^## 35\.` | genau einmal (grep und awk), fünf `### 35.` |
| Vier Registertexte (22a Z. 27, 29, 17, 39) | **je 1× exakt** als Registerzeile (die `0x` der ersten Lesung im Beleg waren ein Artefakt des `> `-Abzugs, in 3b ohne Abzug nachgemessen) |
| Sechs Begründungszeilen (22a Z. 15, 19, 31, 33, 41, 43) | **je 1× exakt**; Z. 55 als Substring |

Beleg: `schritt2_nachweise.txt`.

## Schritt 3 — Die fünf Marken am alten Ort (`d30af22`)

**Nur eingefügt**, `20 0`; alte Zeilen als Teilfolge 5820/5820 erhalten, `git
diff` gegen den Ausgang **0 entfernte Zeilen**.

| Marke für | Z. (Stand `d30af22`) | Ort | Form |
|---|---|---|---|
| 35.4 | **4872** | direkt unter 30.2 (3), im Registertext-Block | `> >`, eine Zeile, Fables Satz zeichengleich |
| 35.1 | **5365** | unter 33.2, nach der Marke aus 34 | `>`-Block, acht Zeilen |
| 35.2 | **5438** | Feldliste 33.3, **angefügt** nach `quelle` | eigene Tabellenzeile `bestaetigungsperiode` |
| 35.3 | **5464** | 33.4 Punkt 3, unter der Marke aus 34.6 | eigene Tabellenzeile „ERSETZT", Fables Satz zeichengleich |
| 35.1/35.3 | **5662** | unter dem Offen-Block in 34.6 | `>`-Block, acht Zeilen: „beantwortet" (Datumsspanne gilt) und „ersetzt" (kein Feld → Feld) |

| Nachweis | Ergebnis |
|---|---|
| Marken mit `TB-83, 22.09.2026` vor Abschnitt 35 | **5** |
| Zitate in den Marken 35.3 und 35.4 gegen 22a Z. 17 / Z. 39 | **je Substring, je 2× im Register** (Marke + Abschnitt) |
| **M5 nachher** | SHA-256 **`e5ab322e…` = vorher**, `diff` leer, 21.4-Zeilen 0 entfernt (Abbruchkriterium 2 nicht eingetreten) |
| **M6 nachher** | **`0e54ac5c…` = vorher**, mtime unverändert (Abbruchkriterium 5 nicht eingetreten) |

Belege: `schritt3_nachweise.txt`, `m5_faltenlisten.txt`, `m6_sperrlisten_hash.txt`.

## Schritte 4–8 — Abschlussprüfung (`15b87b0`, `schritt4_abschluss.txt`)

| | zu prüfen | Soll | Ist |
|---|---|---|---|
| 5 | `numstat` je Datei, `9dac8d4..HEAD` | zweite Spalte 0 | **0 überall** (Register `172 0`, neun Belege je `n 0`); **0 Dateien ausserhalb `docs/`** |
| 6 | `^## 35\.` | 1 | **1**; 30–35 je genau einmal, höchste Nummer 35 |
| 7 | Drei Sperrlisten-Hashes | unverändert | **unverändert**, 0 Commits auf `ergebnisse/` (Abbruchkriterien 5 und 7 nicht eingetreten) |
| 8 | `AKTUELLER_AUFTRAG.md` nur lesen | `TB-83` ≥ 1, numstat leer | **1**, **87 = 87**, numstat **leer** |

## Abweichungen vom Auftrag — mit Begründung

| | Abweichung | Begründung |
|---|---|---|
| 1 | Schritt-0-Commit ohne Betreiberdateien | lagen schon in `9dac8d4` |
| 2 | **M4: Ausgabezeile ist 368, nicht 369** | gemessen; eingetragen, was gemessen wurde (35.1, 35.5), Zahl der Fundstellen wie erwartet |
| 3 | Begründungen als **volle Quellzeilen**, nicht in der Kurzform des Auftrags | 35.1-Grund im Auftrag ohne „Kein Ergebnis: …", 35.3-Begründung ohne das einleitende `**Aber`, 35.4-Grund aus Z. 41 und Z. 43 mit „…" zusammengezogen — in dieser Form nicht zeichengleich (`C1`, wie TB-81/82). Inhalt unverändert |
| 4 | Marken zu 35.2 und 35.3 sind **Tabellenzeilen**; Marke zu 35.4 ein **`> >`-Block im Registertext-Block** | wie in TB-82: Form folgt dem Ort; der Auftrag lässt beides zu |
| 5 | Ergebnisdokument unter **`docs/ERGEBNIS_TB-83_register_35.md`**, nicht `docs/auftraege/ERGEBNIS_TB-83.md` | `ARBEITSWEISE.md` Abschnitt 1/14; Journal-Quellenzeile setzt `docs/ERGEBNIS_TB-<nr>_…` voraus; wie TB-82 |
| 6 | 35.1 trägt zusätzlich die **Messung der ⚠️-Zelle** bei `elliott_wave` in 21.4 und Fables Bitte dazu | Fable 22a Abschnitt 3: „bitte den ganzen Eintrag vorlegen, bevor jemand sie als Beleg nimmt" — gemessen, nicht gedeutet |
| 7 | 35.5 nennt Fables offene Unsicherheit (Fundstellen des Bezeichners) samt der Messung aus Anfrage 22a Punkt 2 | gehört zum Stand der Sache; Antwort steht bei Fable aus |

## Was NICHT getan wurde — ausdrücklich

⛔ Kein Code (`git diff --name-only` gegen den Ausgang: nur `docs/`). ⛔ **Kein
`python3 faltenplan.py`** — M6 belegt es. ⛔ Keine Abbild-Datei, keine Sonde,
kein Wrapper, kein Hash auf die Sperrliste. ⛔ `faltenplan.py:336` nicht
umgestellt.

## Fehler → Regel

Ein Prüfartefakt, kein Fehler im Register: Die erste Zeichengleichheits-Lesung
zog das `> ` von den Registerzeilen ab, die Quellzeilen tragen es aber selbst —
vier `0x`, in 3b ohne Abzug nachgemessen (`1x`). Regel bestätigt: **eine
Prüfung, die 0 liefert, wo 1 erwartet ist, wird zuerst gegen sich selbst
geprüft** (Positivkontrolle), bevor sie als Befund gilt. Und wieder `C1`: drei
Begründungszitate im Auftrag waren Kurz- oder Mischformen.

## ⚠️ Offen — nicht Teil dieses Auftrags

| | | bei wem |
|---|---|---|
| 1 | ⚠️⚠️ **Umstellung von `faltenplan.py:336`** (und der Ausgabe Z. 368) auf den Bezeichner `JJJJ-MM-TT/JJJJ-MM-TT` — hängt an Fables Antwort auf **`FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md`** (Punkt 3: `main()` überschreibt die gesperrte `faltenplan.json`; Wege a/b/c). Bis dahin: **`python3 faltenplan.py` nicht aufrufen** | Fable → Betreiber (Freigabe) |
| 2 | Fables Unsicherheit, ob der Bezeichner anderswo verwendet wird — Anfrage 22a Punkt 2 hat gemessen (Z. 336, 368; Laufkreis zieht mit); seine Antwort steht aus | Fable |
| 3 | **Abbild-Datei** (jetzt mit `bestaetigungsperiode`), **Sonde** (Feldmenge, Werte, positive Prüfungen 34.4/35.2, Zeitpunkt 35.4), **Laufwrapper**, **Sperrlistenpunkt** — je mit Freigabe; Entscheidung 33.5 | Betreiber |
| 4 | TB-30b (Wache in allen neun, Erzeuger der `zellen.csv` mit demselben Bezeichner) | eigener Auftrag |
| 5 | Unverändert offen: 32.5, (20g)–(20m), `K4t` | — |

## In einfacher Sprache

**Was gemacht wurde:** Vier Sätze des Prüfers stehen jetzt im Regelwerk
(Abschnitt 35) und als Marke bei den alten Sätzen. Die „Bestätigungsphase"
heisst künftig nach ihrer Zeitspanne, `2026-01-01/2026-09-01`, bei allen neun
Bots — der bisherige Name „2026-2027" bei einem Bot ist damit unzulässig. Der
Name ist zugleich der Schlüssel, mit dem zwei Programme dieselbe Tabellenzeile
finden; deshalb gehört er in die maschinenlesbare Datei, und die frühere
Aussage „gehört nicht hinein" ist ersetzt. Und: Die Prüfsonde läuft vor dem
Start und bricht bei Abweichung ab.

**Was gemessen wurde:** Die Grundlage des neuen Namens (Beginn in 21.4, Ende in
5.2) wurde aus dem Regelwerk selbst gemessen. Die Auswertung rechnet den Plan
an genau einer Stelle, liest keine Plandatei. Die Auswertungsjahre je Bot sind
vorher und nachher gleich. Und die gesperrte Datei hat vor und nach der Arbeit
dieselbe Prüfsumme — das Programm, das sie überschreiben würde, wurde nicht
gestartet.

**Was aufgefallen ist:** Eine Zeilennummer im Auftrag war um eins daneben (368
statt 369). Drei Begründungszitate waren gekürzt — ins Regelwerk kamen die
vollen Sätze.

**Was nicht gemacht wurde:** Kein Programm geändert, nichts erzeugt, nichts
gesperrt. Die Umstellung des Programms auf den neuen Namen wartet auf die
Antwort des Prüfers zur Falle an der Sperrliste.

---

## Deine Aufgaben

1. **Fable vorlegen:** Abschnitt 35 (Z. 5691 ff.) und die fünf Marken, zusammen mit der wartenden Anfrage 22a (Sperrlistenfalle) — *Wo:* `docs/VORREGISTRIERUNG_neuselektion.md`, `docs/belege/TB-83/` — *Woran:* seine Antwort entscheidet Weg a/b/c und gibt die Umstellung von `faltenplan.py:336` frei oder nicht; abgelegt als `FABLE_ANTWORT_2026-09-22b_…`.
2. **Bis dahin:** `python3 faltenplan.py` nicht aufrufen (M6 wäre sonst beim nächsten Auftrag rot).

Nicht von dir abhängig: nichts weiter aus diesem Auftrag; alle Commits sind gepusht.
