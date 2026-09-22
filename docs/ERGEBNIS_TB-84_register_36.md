# ERGEBNIS TB-84 — Registerabschnitt 36: die Schreibregel für Sperrlistenpfade, die Sperrlisten-Sonde mit drei Ausgängen, das Abbild der Sperrliste als neue Datei, die Reihenfolge — und die gesperrte Datei hat vor und nach der Arbeit denselben Hash (Mac-Sitzung, 22.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-84_register_36.md` (Zeiger
`AKTUELLER_AUFTRAG.md` Z. 39 nannte TB-84, gleich der vorangestellten Nummer).
⚠️ **Der Auftrag wurde während der Sitzung vom Betreiber erweitert** (36.5 und
36.6 aus Fable 22c; Schritt 0/1 waren da schon committet, Abschnitt 36 noch
nicht eingetragen) — die Erweiterung ist vollständig abgearbeitet.
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `4bbd720` (= `origin/main`
beim Start; der Auftrag erwartete `fdb181a` oder jünger). Commits `a7c4cea`
(Schritt 0/1), `9122775` (⚠️ **Betreiber-Dateien, unverändert übernommen**:
Fable 22c, Anfrage 22c, Vorarbeit Sonde, erweiterter Auftrag), `5f0c80e` (2),
`61c52a0` (3), `a245902` (4–8) und der Abgabe-Commit — jeder einzeln gepusht.
Belege `docs/belege/TB-84/`. Geändert: **nur `docs/`** — das Register (append-
und insert-only, **345 / 0**), elf Belegdateien, dieses Dokument, ein
Journalblock. ⛔ **Kein Code, kein `python3 faltenplan.py`, keine Sonde, kein
`main()`-Umbau, kein Z. 336, `herkunft.py` unberührt, keine Abbild-Datei, kein
Hash auf die Sperrliste, keine Freigabe.**

⚠️⚠️ **M2, vorweg:** `research/vorregistrierung/ergebnisse/faltenplan.json`
(Sperrlistenpunkt 2) — SHA-256 **vor** der Arbeit
`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`, **nach** der
Arbeit **dieselbe**; mtime unverändert 14.09.2026 17:55, 0 Commits auf
`ergebnisse/`, `git status research/` leer. `faltenplan.py` wurde in dieser
Sitzung **nicht ausgeführt**, nur mit `sed` gelesen (Z. 330–380). Abbruchkriterium
5 nicht eingetreten.

*In einfacher Sprache, zu Beginn:* Das Regelwerk hat jetzt eine Regel, die
bisher fehlte: Kein Programm darf an einen geschützten Pfad schreiben, und
jedes Programm, das solche Dateien erzeugt, schreibt nur einmal — existiert die
Datei, bricht es ab, auch bei gleichem Inhalt. Dazu ein Prüfprogramm mit drei
Antworten („in Ordnung", „Befund", „nicht prüfbar"), eine neue Datei als
maschinenlesbares Abbild der Schutzliste, und die Reihenfolge, in der das alles
gebaut wird. Gebaut ist nichts; alles nur Text, die gesperrte Datei
unangetastet — gemessen.

---

## Schritt 0 — Ausgangsstand (`a7c4cea`)

| | Ergebnis |
|---|---|
| `git status --short` beim Start | **leer.** `FABLE_ANTWORT_2026-09-22b_…` und `FABLE_ANFRAGE_2026-09-22b_…` lagen schon in `4bbd720` — nur geprüft |
| `grep -cE "^## 36\."` | **0** (Abbruchkriterium 6 nicht eingetreten); höchste `##`-Nummer 35; Register 5839 Zeilen |
| Drei Sperrlisten-Hashes | `0e54ac5c…` · `a163c498…` · `4549395f…`, voller Pfad im Beleg |
| Schlüsselbund / „Claude Max" | Handgriff des Betreibers vor dem Start; von der Sitzung nicht messbar |

## Schritt 1 — M1 bis M6 „vorher" (`a7c4cea`)

| # | Messung | erwartet | **gemessen** |
|---:|---|---|---|
| **M1** | Punkte in Abschnitt 10 | 14 | **14** (Z. 815–852 im Ausgang; Punkte 11 und 12 nennen `herkunft.py`) |
| **M2 vorher** | Hash `ergebnisse/faltenplan.json` | `0e54ac5c…` | **`0e54ac5c…`**, mtime 14.09. 17:55, letzter Commit `a2fcf01`. Die Schreibstelle in `main()`: Z. 372 `ziel = …"faltenplan.json"`, Z. 373 `open(ziel, "w", …)` — nur gelesen |
| **M3** | Ausgänge im Kopf von `shared/snapshot.py` | drei, `2` = NICHT PRÜFBAR | **drei, Z. 217–219**, `2   NICHT PRUEFBAR / abgebrochen`; Begründung Z. 221–224 (TB-45). ⚠️ Der Auftrag nannte Z. 214–232 und das Muster `^0\|^1\|^2` — die Ziffern stehen mit vier Leerzeichen eingerückt, das unverankerte Muster träfe sie nicht; mit Einrückung gemessen |
| **M4** | `EINGEFROREN` / `SPERRLISTE_DATEIEN` in `herkunft.py` | Z. 57 und 66 | **Z. 57 und Z. 66** (dritte Fundstelle Z. 114 = Verwendung in `register()`); zehn Einträge / fünf Muster, wörtlich im Beleg |
| **M5** | `benchmark_drawdowns_vt.json` in einer der Listen? | nein | **nein** — 0 Treffer, rc 1; ebenso fehlen `top25_symbols.txt` und `sp500_top150.txt`; Positivkontrolle `faltenplan.json` 1 Treffer (Z. 60) |
| **M6 vorher** | Faltenliste 33.2 | — | neun Zeilen, SHA-256 `e5ab322e…` (= TB-82, TB-83) |

Belege: `m1_sperrlistenpunkte.txt` … `m6_faltenlisten.txt`, Befehl in Zeile 1.

## Zwischenschritt — Betreiber-Dateien während der Sitzung (`9122775`)

Nach `a7c4cea` lagen im Arbeitsbaum: der **erweiterte Auftrag** (36.5, 36.6;
`61 / 5` — die fünf entfernten Zeilen sind die Erweiterung des Betreibers, nicht
von TB-84), `FABLE_ANTWORT_2026-09-22c_drei_ausgaenge_und_abbild.md` (erschien
wenige Minuten nach dem erweiterten Auftrag; ohne sie wären 36.5/36.6 nicht
zeichengleich prüfbar gewesen), `FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md`
und `VORARBEIT_sperrlisten_sonde.md`. Alle vier **unverändert** als eigener
Commit übernommen, bevor Abschnitt 36 geschrieben wurde.

## Schritt 2 — Registerabschnitt 36 (`5f0c80e`)

Ans Ende des Registers, **309 / 0**. Alle Fable-Zeilen per Skript aus 22b und
22c gezogen, nicht abgetippt.

| Eintrag | Z. (Stand nach Schritt 3) | Inhalt |
|---|---|---|
| **36.1** | 5907 | Schreibregel für Sperrlistenpfade (1)–(4), Fables Abwägung der drei Wege, Grund, Härte-Satz, seine Tatsachennotiz — und die Nachmessung (M2): Hash, mtime, Commit, Schreibstelle Z. 372–374 |
| **36.2** | 5957 | Sperrlisten-Sonde; Fables Unsicherheit; die drei Tatsachennotizen (a)(b)(c) des steuernden Chats mit den Messwerten M3–M5, je mit dem Vermerk, dass Frage 1 in 36.5 und Frage 2 in 36.6 beantwortet ist |
| **36.3** | 6029 | Vorsatz und vier Schritte, Fables Satz; ausdrücklich: alle vier brauchen Betreiberfreigabe, keine erteilt |
| **36.4** | 6058 | Tatsachennotiz zu 21.4 (⚠️ trägt keine Erklärung); Rücknahme der Deutung aus Anfrage 21g Punkt 3, zeichengleich zitiert |
| **36.5** | 6083 | Drei Ausgänge für jede Sonde und Wache (22c); Berichtigung des „≠ 0" aus 36.2; Zusatz Schreibsperre endet mit 1; Tatsachennotiz M3 |
| **36.6** | 6119 | Abbild der Sperrliste ist eine eigene, neue Datei; `EINGEFROREN`/`SPERRLISTE_DATEIEN` sind es nicht; drei Gründe voll; Fables erbetene Messung; **Tatsachennotiz zu den Listen ausdrücklich als ausstehend** mit Fundstelle Anfrage 22c; seine Unsicherheit (Abschnitt 10 maschinenlesbar?) |
| 36.7 | 6163 | Was nicht getan wird, mit M2 und dem Offenen |

| Nachweis | Ergebnis |
|---|---|
| `numstat` | `309 0` |
| `^## 36\.` / `^### 36\.` | **1** / **7** |
| 15 Zeilen aus 22b (Z. 19, 20, 15, 25, 27, 29, 22, 23, 48, 33, 35–38, 40) | **je 1× exakt** als Registerzeile |
| 13 Zeilen aus 22c (Z. 13, 17, 18, 20, 22, 24, 30, 31, 33, 35, 37, 39, 49) | **je 1× exakt** |
| 5 Teilzeichenketten (22b Z. 9 und 13, 22c Z. 9 und 41, 21g Z. 87–88) | je in der Quelle, je ≥ 1× im Abschnitt |
| Positivkontrolle | 22b Z. 19 ohne `> ` gesucht → 0 (die Registerzeile trägt das Präfix wie die Quelle) |

Beleg: `schritt2_nachweise.txt`.

## Schritt 3 — Die sechs Marken am alten Ort (`61c52a0`)

**Nur eingefügt**, `36 0`; alte Zeilen als Teilfolge 6149/6149 erhalten, `git
diff` **0 entfernte Zeilen**.

| Marke für | Z. (Stand `61c52a0`) | Ort | Form |
|---|---|---|---|
| 36.2 / 36.6 | **813** | unter der Überschrift von Abschnitt 10 | `>`-Block, acht Zeilen (Sonde prüft; Abbild ist neue Datei; die zwei Listen sind es nicht) |
| 36.1 | **836** | Sperrliste Punkt 2, **unter** der Tatsachennotiz aus 30 | `   >`-Fortsetzung des vorhandenen Blocks, acht Zeilen |
| 36.4 | **2947** | 21.4, direkt unter der Tabelle | `>`-Block, vier Zeilen; Tabellenzeile samt `⚠️` zeichengleich (Nachweis) |
| 36.3 | **5769** | 35.1, nach Fables „Folge, Handwerk"-Zitat | `>`-Block, acht Zeilen, Fables Satz aus 22b Z. 40 zeichengleich |
| 36.5 | **5914** | 36.1, direkt unter dem Registertext, am „(Rückgabewert ≠ 0)" in (2) | `> >`, eine Zeile |
| 36.5 | **5964** | 36.2, direkt unter dem Registertext, am „≠ 0 endet und den Punkt nennt" | `> >`, eine Zeile, Berichtigungstext aus 22c Z. 20 zeichengleich (2× im Register: 36.5 und Marke) |

| Nachweis | Ergebnis |
|---|---|
| Marken mit `TB-84, 22.09.2026` vor Abschnitt 36 / in 36 | **4** / **2** |
| **M6 nachher** | SHA-256 **`e5ab322e…` = vorher**, `diff` leer, 21.4-Zeilen 0 entfernt (Abbruchkriterium 2 nicht eingetreten) |
| **M2 nachher** | **`0e54ac5c…` = vorher**, mtime unverändert (Abbruchkriterium 5 nicht eingetreten) |

Belege: `schritt3_nachweise.txt`, `m6_faltenlisten.txt`, `m2_sperrlisten_hash.txt`.

## Schritte 4–8 — Abschlussprüfung (`a245902`, `schritt4_abschluss.txt`)

| | zu prüfen | Soll | Ist |
|---|---|---|---|
| 5 | `numstat` je Datei, `4bbd720..HEAD` | zweite Spalte 0 | **Register `345 0`**, elf Belege je `n 0`, drei Betreiber-Dateien je `n 0`; einzige Zeile mit zweiter Spalte ≠ 0: `MAC_TB-84_register_36.md` `61 5` = **Erweiterung durch den Betreiber** (9122775), nicht von TB-84. **0 Dateien ausserhalb `docs/`** |
| 6 | `^## 36\.` / `^### 36\.` | 1 / 7 | **1 / 7**; 30–36 je genau einmal, höchste Nummer 36, Register 6184 Zeilen |
| 7 | Drei Sperrlisten-Hashes | unverändert | **unverändert**, 0 Commits auf `ergebnisse/`, 0 auf `research/`, `shared/`, `strategies/`, `*.py` (Abbruchkriterien 4, 5, 7 nicht eingetreten) |
| 8 | `AKTUELLER_AUFTRAG.md` nur lesen | `TB-84` ≥ 1, numstat leer | **1**, **87 = 87**, numstat **leer** |

## Abweichungen vom Auftrag — mit Begründung

| | Abweichung | Begründung |
|---|---|---|
| 1 | Schritt-0-Commit ohne Betreiberdateien | lagen schon in `4bbd720` |
| 2 | **Zusätzlicher Commit `9122775`** mit vier Betreiber-Dateien und dem erweiterten Auftrag | der Betreiber schrieb während der Sitzung ins Repo; eigener Commit, unverändert, damit die TB-84-Commits sauber bleiben (Regel aus TB-68) |
| 3 | **Sieben** Unterabschnitte statt vier (36.5, 36.6, Schlussteil 36.7) | Erweiterung des Auftrags, Schritt 6 verlangt `### 36.` = 7 |
| 4 | Begründungen als **volle Quellzeilen**, nicht in der Kurzform des Auftrags | 36.1-Grund im Auftrag ohne „21b (3): …" und „Kein Ergebnis: …"; 36.5-Zusatz ohne den Vorsatz „*Zur Einmal-Schreibsperre:*"; 36.6 drei Gründe im Auftrag mit zwei „…"-Auslassungen — in dieser Form nicht zeichengleich (`C1`, wie TB-81–83). Inhalt unverändert |
| 5 | 36.2 (a) und (c) tragen den Vermerk „beantwortet in 36.5 / 36.6" statt „Offen bei Fable" | Fable 22c lag beim Eintrag vor; ein Eintrag, der am selben Tag beantwortete Fragen als offen führte, wäre der Fall, den der Betreiber mit der Erweiterung vermeiden wollte. Die Anfrage 22b bleibt als Herkunft der drei Notizen genannt |
| 6 | Marke unter der Überschrift von Abschnitt 10 ist **ein** Block für 36.2 und 36.6 | Auftrag 36.6: „zusammen mit der Marke aus 36.2" |
| 7 | Marke 36.3 sitzt **nach** Fables „Folge, Handwerk"-Zitat in 35.1, nicht zwischen Absatz und Zitat | das Zitat gehört zum Absatz; einfügen zwischen beide hätte den Zusammenhang zerrissen |
| 8 | M3 mit eingerücktem Muster gemessen (`^    [012]   `) | das Muster des Auftrags ist unverankert an der Einrückung und träfe die Zeilen nicht; Zeilen 217–219 statt „214–232" |
| 9 | Ergebnisdokument unter **`docs/ERGEBNIS_TB-84_register_36.md`**, nicht `docs/auftraege/ERGEBNIS_TB-84.md` | `ARBEITSWEISE.md` Abschnitt 1/14; Journal-Quellenzeile setzt `docs/ERGEBNIS_TB-<nr>_…` voraus; wie TB-82, TB-83 |
| 10 | 36.6 nennt zusätzlich Fables Unsicherheit aus 22c (Abschnitt 10 maschinenlesbar?) mit dem Hinweis, dass die Messung (Vorarbeit) vorliegt, aber nicht eingetragen ist | gehört zum Stand der Sache; die Antwort steht aus |

## Was NICHT getan wurde — ausdrücklich

⛔ Kein Code (`git diff --name-only` gegen den Ausgang: nur `docs/`). ⛔ **Kein
`python3 faltenplan.py`** — M2 belegt es. ⛔ Keine Sperrlisten-Sonde, kein
`main()`-Umbau, kein Z. 336, keine Abbild-Datei, kein Hash auf die Sperrliste,
kein Wrapper. ⛔ `herkunft.py` unberührt (nur `grep`/`sed`). ⛔ Die
Tatsachennotiz zu `EINGEFROREN`/`SPERRLISTE_DATEIEN` nicht geschrieben — nur
eingetragen, dass sie aussteht. ⛔ Keine Freigabe erteilt oder unterstellt.

## Randbefund — gemessen, nicht eingetragen, für den steuernden Chat

Beim lesenden Gegencheck der Anfrage 22c (nicht Teil von M1–M6): `grep -rn
"EINGEFROREN\|SPERRLISTE_DATEIEN" --include=*.py` bestätigt, dass
`SPERRLISTE_DATEIEN` ausser der Definition nirgends vorkommt und `EINGEFROREN`
der Vorregistrierung nur in `herkunft.py:114` gelesen wird; `import herkunft`
kommt in `research/vorregistrierung/` nicht vor. ⚠️ **Aber:**
`research/etf_trendfolge/datenstand.py` Z. 43–49 lädt genau dieses
`research/vorregistrierung/herkunft.py` über `reg.lade_fremdes_modul(…)` und
ruft `herkunft.datenstand(…)` auf — ein **dritter** Nutzer der Datei ausserhalb
`turn_of_month/`, der `datenstand()` (Sperrlistenpunkt 12) verwendet, nicht
`register()`/`block()`. Die Anfrage 22c nennt ihn nicht (sie hat nach
`hk.block` gesucht). Nicht bewertet; gehört zu Fables ausstehender
Tatsachennotiz, falls sie „wer liest es" vollständig beantworten soll.

## Fehler → Regel

Ein Prüfartefakt, vor dem Commit behoben: Das Zitat aus 22c Z. 41 stand in
36.6 zunächst über drei Zeilen umbrochen — die Zeichengleichheitsprüfung fand
es nicht (0×). Auf **eine** Zeile gesetzt, 1×. Regel: **Ein Fable-Zitat steht
im Register auf einer Zeile, wie in der Quelle** — Umbruch ist für Prosa des
steuernden Chats, nicht für zitierten Registertext. Und wieder `C1`: drei
Begründungszitate im Auftrag waren Kurz- oder Mischformen, eines mit
sichtbaren Auslassungen. Neu in dieser Sitzung: **Ein Auftrag kann sich
während der Sitzung ändern** — die Datei wurde nach Schritt 1 erweitert und die
Quelle für die Erweiterung kam Minuten später; beides erst prüfen (existiert
die Quelle? was hat sich geändert?), dann fortfahren, und die Betreiber-Dateien
in einen eigenen Commit.

## ⚠️ Offen — nicht Teil dieses Auftrags

| | | bei wem |
|---|---|---|
| 1 | ⚠️⚠️ **Betreiberfreigabe** für die vier Schritte aus 36.3 (Sonde → `main()` absichern mit Mutationsprobe → Z. 336/368 → Abbild + Faltenplan-Sonde + Hash) — **keine erteilt.** Bis dahin: `python3 faltenplan.py` nicht aufrufen | Betreiber |
| 2 | **Fables Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN`** (36.6) — Messung mit Anfrage 22c vorgelegt; dazu der Randbefund oben (`etf_trendfolge/datenstand.py`) | Fable |
| 3 | **Frage der Anfrage 22c:** prüft die Sonde auch Pfade, die für die Sperrliste **bestimmt** sind (`benchmark_drawdowns_vt.json`) — 36.1 (1) deckt es, der Wortlaut 36.2 nicht | Fable |
| 4 | **Fables Unsicherheit 22c:** Abschnitt 10 ist nach der Vorarbeit **nicht** maschinenlesbar (4 von 14 Punkten reine Datei-Hashes); Vorschlag des steuernden Chats: `2` je nicht messbarem Punkt | Fable |
| 5 | Fables Unsicherheit aus 35.5 (weitere Fundstellen des Bezeichners) — gemessen in Anfrage 22a Punkt 2, Antwort aus | Fable |
| 6 | Abbild-Datei des Faltenplans (mit `bestaetigungsperiode`), Faltenplan-Sonde, Laufwrapper, Sperrlistenpunkt — 33.5; TB-30b (Wache, Erzeuger `zellen.csv` + `herkunft.json`) | Betreiber / eigener Auftrag |
| 7 | Unverändert offen: 32.5, (20g)–(20m), `K4t` | — |

## In einfacher Sprache

**Was gemacht wurde:** Sechs Texte des Prüfers stehen jetzt im Regelwerk
(Abschnitt 36) und als Marke an sechs alten Stellen. Die neue Regel: Kein
Programm schreibt an einen geschützten Pfad; Erzeuger schreiben nur einmal und
brechen sonst ab — auch bei gleichem Inhalt („die Sperre ist stärker, wenn sie
dümmer ist"). Jede Prüfung im Verfahren kennt künftig drei Antworten; die
maschinenlesbare Schutzliste wird eine neue Datei, nicht eine der zwei
vorhandenen; und die Reihenfolge des Handwerks ist festgeschrieben.

**Was gemessen wurde:** Alle sechs Messungen wie erwartet. Die gesperrte Datei
hat vor und nach der Arbeit dieselbe Prüfsumme; das Programm, das sie
überschreiben würde, wurde nicht gestartet. Die Auswertungsjahre je Bot sind
unverändert.

**Was aufgefallen ist:** Der Auftrag wuchs während der Arbeit um zwei Einträge,
und die Quelle dafür kam ein paar Minuten später — beides wurde abgewartet und
geprüft, bevor etwas eingetragen wurde. Drei Zitate im Auftrag waren gekürzt;
ins Regelwerk kamen die vollen Sätze. Ein Zeilenmuster im Auftrag hätte nichts
getroffen. Und ein drittes Programm liest die gesperrte Herkunftsdatei, das die
Anfrage an den Prüfer nicht nennt — nur notiert.

**Was nicht gemacht wurde:** Kein Programm geändert, nichts gebaut, nichts
gesperrt, keine Freigabe. Die vier Handwerksschritte warten auf den Betreiber.

---

## Deine Aufgaben

1. **Fable vorlegen:** Abschnitt 36 (Z. 5875 ff.) und die sechs Marken, zusammen mit der wartenden Anfrage 22c — *Wo:* `docs/VORREGISTRIERUNG_neuselektion.md`, `docs/belege/TB-84/` — *Woran:* seine Tatsachennotiz zu den zwei Listen und die Antwort auf „bestimmte Pfade"; dazu der Randbefund (`etf_trendfolge/datenstand.py` ruft `herkunft.datenstand()` auf), falls du ihn nachreichen willst.
2. **Freigabe entscheiden** für die vier Schritte aus 36.3 — erst Schritt 1 (Sonde), dann 2, dann 3. Bis dahin `python3 faltenplan.py` nicht aufrufen.

Nicht von dir abhängig: nichts weiter aus diesem Auftrag; alle Commits sind gepusht.
