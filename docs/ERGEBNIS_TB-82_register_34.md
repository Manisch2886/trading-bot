# ERGEBNIS TB-82 — Registerabschnitt 34: Fables fünf Einträge aus 21l/21m, eine Berichtigung von uns, und jede Berichtigung mit Marke am alten Ort (Mac-Sitzung, 22.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-82_register_34.md` (Zeiger
`AKTUELLER_AUFTRAG.md` Z. 39 nannte TB-82, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `9614624` (= `origin/main`
beim Start; der Auftrag erwartete `ad020b5` oder jünger), Ortszeit 22.09.2026
kurz nach Mitternacht — die UTC-Zeitstempel in den Belegen lauten deshalb
`2026-09-21T22:…Z`. Commits `1b8da04` (Schritt 0/1), `6cbbf95` (2), `04cf1da`
(3), `d82f82d` (4–8) und der Abgabe-Commit — jeder einzeln gepusht. Belege
`docs/belege/TB-82/`. Geändert: **nur `docs/`** — das Register (append- und
insert-only, **221 / 0**), neun Belegdateien, dieses Dokument, ein
Journalblock. ⛔ **Kein Code, keine Abbild-Datei, keine Sonde, kein Hash, keine
Wache, kein `faltenplan.py`, nichts unter `research/`, `strategies/`, `shared/`.**

*In einfacher Sprache, zu Beginn:* Der Verfahrensprüfer hat den Auswertungsplan
geprüft und fünf kleine Einträge ins Regelwerk verlangt; dazu kommt eine
Berichtigung eines eigenen Satzes. Alle sechs stehen jetzt in einem neuen
Abschnitt **und** — das ist neu — als kurze Marke direkt bei dem Satz, den sie
berichtigen oder ergänzen. Kein alter Satz wurde geändert, keine Zahl hat sich
bewegt; beides ist gemessen.

---

## Schritt 0 — Ausgangsstand (`1b8da04`)

| | Ergebnis |
|---|---|
| `git status --short` beim Start | **leer.** Die sechs im Auftrag genannten Dateien unter `docs/projektfuehrung/` lagen bereits versioniert in `9614624` (der steuernde Chat hatte sie mit dem Auftrag abgelegt) — nichts erneut committet, nur geprüft |
| `grep -cE "^## 34\."` vor dem Eintrag | **0** (Abbruchkriterium 6 nicht eingetreten); höchste `##`-Nummer 33; Register 5446 Zeilen |
| Drei Sperrlisten-Hashes, voller Pfad | `…/faltenplan.json` `0e54ac5c…` · `…/benchmark_drawdowns.json` `a163c498…` · `…/benchmark_drawdowns_vt.json` `4549395f…` |
| Schlüsselbund / Kopfzeile „Claude Max" | Handgriff des Betreibers vor dem Start; von der Sitzung nicht messbar, nur vorausgesetzt |

Beleg: `docs/belege/TB-82/schritt0_ausgangsstand.txt`.

## Schritt 1 — M1 bis M4 und M5 „vorher" (`1b8da04`)

Alle Messungen **vor** dem ersten Eintrag, am Stand `9614624`; die Zahlen des
Auftrags wurden nicht übernommen, sondern nachgemessen.

| # | Messung | erwartet | **gemessen** |
|---:|---|---|---|
| **M1** | `Rest` (ganzes Wort), `Teilfalte`, `angebrochene` im Register | 0 | **0** — in zwei Lesungen (`\b` mit Positivkontrolle, und `-w`); das einzige „Rest…" im Register ist „Reste" (Z. 872, `*_15m.csv`), kein Treffer für das Wort. ⇒ (1b) ist eine **Regel, kein Verweis** |
| **M2** | `grep -c "2026-2027"` | 1 | **1**, Z. 5431 = der berichtigte Satz in 33.4 Punkt 3 selbst; Halbgeviertstrich-Form `2026–2027` 0; `faltenplan.py:336` im Register 0; die Codestelle `falten[-1]["name"]` liegt in `research/vorregistrierung/faltenplan.py:336` (nur gelesen) |
| **M3** | 21.4, Spalte „Bestätigung ab" | `2026-01-01` bei allen neun | **9/9 `2026-01-01`**; kein `2026` in dieser Spalte, das nicht `2026-01-01` ist; `2026-2027` in den neun Zeilen 0. 21.4 führt je Bot: Markt, Faltenlänge, erste Falte, # Selektionsfalten, Bestätigung ab, 4b erfüllt |
| **M4** | Wachen in den neun `multi_symbol_optimise.py` | alle 0 | **alle 0**, in der engen (`assert `, `raise `, „Wache") und der weiten Lesung (`assert`, `raise`, `wache` ohne Gross/Klein, `Selektionsfalte`); neun Dateien vorhanden, SHA-256 je Datei im Beleg, `git status strategies/` leer ⇒ **Ersteinbau** |
| **M5 vorher** | die neun Tabellenzeilen aus 33.2 | — | festgehalten, SHA-256 der Zeilen `e5ab322e…`; gegen 21.4 (Faltenlänge, erste Falte, Anzahl) **0 Abweichungen**; Anzahl aus der Liste nachgezählt gegen Spalte „#": 9/9 gleich |

Belege: `m1_rest.txt`, `m2_2026-2027.txt`, `m3_bestaetigung_ab.txt`,
`m4_wachen_optimierer.txt`, `m5_faltenlisten.txt` (jede mit dem Befehl in
Zeile 1).

## Schritt 2 — Registerabschnitt 34 (`6cbbf95`)

Ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md`, **200 / 0**. Die fünf
Fable-Texte wurden per `sed` aus den Quelldateien gezogen, nicht abgetippt, und
im Beleg zeilenweise gegen die Quelle gehalten.

| Eintrag | Fundstelle im Register (Stand nach Schritt 3) | Inhalt |
|---|---|---|
| **34.1** | Z. 5500 | Ergänzung zu 33.2, Falten mit L > 1 (21m 1a) — Tatsachennotiz: nur `elliott_wave` betroffen, die vier Falten aus 33.2 folgen aus dem Text; Liste unverändert |
| **34.2** | Z. 5521 | Ergänzung zu 33.2, Rest vor Go-Live (21m 1b) — Tatsachennotiz M1/M3: (1b) ist Regel, kein Verweis; für den Bestand tritt der Fall nicht ein (Rest bei allen neun `2026-01-01` bis `2026-09-01`, kürzer als L) |
| **34.3** | Z. 5549 | Berichtigung zu 30.2 (2), `3b (b)` lies `3b (a)` (21m Frage 3) — mit Fables Grund für den eigenen Satz |
| **34.4** | Z. 5569 | Ergänzung zu 33.3, `horizontbeginn` Datum oder `"kein Horizont"`, `null` Fehlschlag (21m Frage 4) — Folge: `faltenplan_tb80.json` auch daran kein Abbild; die `null`-Frage aus TB-81 damit entschieden: nein |
| **34.5** | Z. 5592 | Berichtigung zu 29.4, „vier" → „neun" (21l 4b) — Tatsachennotiz M4: Ersteinbau, TB-30b |
| **34.6** | Z. 5618 | Berichtigung zu 33.4 Punkt 3 (eigener Satz) mit den gemessenen Werten M2/M3, und die **offene Frage** (zwei Formen der Bestätigungsperiode) — als offen eingetragen, nicht entschieden |
| 34.7 | Z. 5653 | Was nicht getan wird |

| Nachweis | Ergebnis |
|---|---|
| `numstat` | `200 0` |
| `^## 34\.` | genau einmal, Z. 5450 (vor den Marken; jetzt 5471) — `grep -c` **1**, `awk` **1**, sieben `### 34.` |
| Zeichengleichheit der fünf Registertexte gegen die Quellzeilen (21m Z. 19, 25, 45, 53; 21l Z. 38) | **je 1× exakt** als Zeile im Register |
| Zeichengleichheit der fünf *Grund*-Absätze (21m Z. 21, 27, 47, 55; 21l Z. 40) | **je 1× exakt** (ohne das vorangestellte `> `) |
| Sechs Teilzitate (Kopf ×2, 34.2, 34.4, 34.5, 34.6) und der 33.4-Satz | **alle Substring der Quellzeile** |

Beleg: `docs/belege/TB-82/schritt2_nachweise.txt`.

## Schritt 3 — Die sechs Marken am alten Ort (`04cf1da`)

**Nur eingefügt**, `21 0`; das Einfügewerkzeug (Einmalskript im Scratchpad der
Sitzung, nicht im Repo) hat vor dem Schreiben geprüft, dass jede alte Zeile in
gleicher Reihenfolge als Teilfolge erhalten ist (5647 / 5647); `git diff` gegen
den Ausgang zeigt **0 entfernte Zeilen**.

| Marke für | Ort (Z. im Stand `04cf1da`) | Form |
|---|---|---|
| 34.5 | **4821**, unter dem Absatz „in den vier `multi_symbol_optimise.py`" (29.4) | `>`-Block, sechs Zeilen, mit Fables Satz zeichengleich |
| 34.3 | **4870**, direkt unter 30.2 (2), **innerhalb** des Registertext-Blocks | verschachtelter `> >`-Block, eine Zeile |
| 34.1 + 34.2 | **5356**, unter dem Registertext-Block 33.2 | `>`-Block, sieben Zeilen |
| 34.3 (Zitierhinweis) | **5406**, als Satz am Ende des Zitierhinweises 33.2 | drei Zeilen Fliesstext, angefügt ohne Leerzeile — „bekommt einen Satz" |
| 34.4 | **5423**, in der Feldliste 33.3 direkt unter `horizontbeginn` | **eigene Tabellenzeile** (`↳`) |
| 34.6 | **5452**, in der Tabelle 33.4 direkt unter Punkt 3 | **eigene Tabellenzeile** |

| Nachweis | Ergebnis |
|---|---|
| Marken mit `TB-82, 22.09.2026` vor Abschnitt 34 | **6** |
| Zitat in der 34.3-Marke gegen 21m Z. 45; Zitat in der 34.5-Marke (über vier Zeilen umbrochen, zusammengefügt) gegen 21l Z. 38; „33.2 nennt sie nicht" gegen 21m Z. 39 | **alle zeichengleich / Substring** |
| **M5 nachher** | neun Zeilen, SHA-256 **`e5ab322e…` = vorher**, `diff` leer; gegen 21.4 0 Abweichungen; die 21.4-Zeilen selbst: 0 entfernt (Abbruchkriterium 2 nicht eingetreten) |

Belege: `schritt3_nachweise.txt`, `m5_faltenlisten.txt` (Abschnitt „NACHHER").

## Schritte 4–8 — Abschlussprüfung (`d82f82d`, `schritt4_abschluss.txt`)

| | zu prüfen | Soll | Ist |
|---|---|---|---|
| 4 | M5 nachher gegen vorher | identisch | **identisch** (s. o.) |
| 5 | `numstat` je Datei, `9614624..HEAD` | zweite Spalte 0 | **0 überall** — Register `221 0`, neun Belege je `n 0`; **0 Dateien ausserhalb `docs/`** |
| 6 | Abschnitt 34 genau einmal | 1 | **1** (grep und awk), 26–34 je genau einmal, höchste Nummer 34 |
| 7 | Drei Sperrlisten-Hashes | unverändert | `0e54ac5c…` · `a163c498…` · `4549395f…` **unverändert**, 0 Commits auf `ergebnisse/` (Abbruchkriterium 5 nicht eingetreten) |
| 8 | `AKTUELLER_AUFTRAG.md` nur lesen | `TB-82` ≥ 1, `wc -l` unverändert, numstat leer | **1**, **87 = 87**, numstat **leer**; die Zeigertabelle hat genau eine Datenzeile (TB-82); die Zeile TB-70 in Z. 57 gehört zur Planungstabelle „Geplant, noch nicht formuliert" |

## Abweichungen vom Auftrag — mit Begründung

| | Abweichung | Begründung |
|---|---|---|
| 1 | Schritt-0-Commit enthält **nichts vom Betreiber**, nur den Beleg | Die sechs Dateien lagen schon in `9614624`; „nicht erneut committen, nur prüfen" |
| 2 | Die *Grund*-Zitate stehen im Register als **volle Absätze** aus 21m/21l, nicht in der Kurzform des Auftrags | Die Kurzformen im Auftrag lassen Sätze weg (etwa „Kein Ergebnis: …" bei 34.2, „…" bei 34.4) und wären als „zeichengleich" falsch etikettiert; die vollen Absätze sind es (Nachweis 2.3). Inhalt unverändert (`C1`) |
| 3 | Die Marken zu **34.4 und 34.6** sind **Tabellenzeilen**, keine `>`-Blöcke | Beide alten Sätze stehen in Tabellen; ein `>`-Block zwischen zwei Tabellenzeilen zerreisst die Tabelle. Vermerk als eigene Tabellenzeile ist das Muster aus TB-54b |
| 4 | Die Marke zu **34.3** steht als verschachtelter `> >`-Block **innerhalb** des Registertext-Blocks 30.2 | „Direkt unter 30.2 (2)" ist eine Zeile mitten im Block; nur so steht die Marke am Satz und nicht drei Zeilen tiefer hinter (4). Kein Zeichen des Blocks geändert; die Absätze (3)/(4) rendern dadurch als eigener Absatz |
| 5 | Der Zitierhinweis in 33.2 bekommt seinen Satz als **neue Zeilen ohne Leerzeile** | So bleibt es ein Satz desselben Absatzes und die numstat-Bedingung (zweite Spalte 0) hält — ein Anfügen an die bestehende Zeile hätte `1 1` ergeben |
| 6 | Ergebnisdokument unter **`docs/ERGEBNIS_TB-82_register_34.md`**, nicht `docs/auftraege/ERGEBNIS_TB-82.md` | `ARBEITSWEISE.md` Abschnitt 1 und 14 (Regel 3): Ergebnisdokument unter `docs/`, Journal-Quellenzeile auf `docs/ERGEBNIS_TB-<nr>_<stichwort>.md`; alle 60+ Vorgänger liegen dort. Die stehende Regel wiegt schwerer als der Pfad im Auftrag |
| 7 | Abschnitt 34 trägt zusätzlich **Fables allgemeine Regel aus dem Vorab von 21m** (Voraussetzung nennen, vorher messen) und einen Unterabschnitt **34.7** | Die Regel erklärt, warum 34.1/34.2/34.5/34.6 je eine Tatsachennotiz tragen; 34.7 ist die Form aus 33.5 |
| 8 | 34.4 zieht die Folge, dass die in TB-81 offen gelassene `null`-Frage **entschieden** ist | Steht wörtlich in Fables Text („JSON-`null` … sind Fehlschläge"); nur benannt, nichts hinzugefügt |
| 9 | Datum in Abschnittstitel, Marken und Journal: **22.09.2026** (Ortszeit) | Die Sitzung lief nach Mitternacht Ortszeit; UTC in den Belegen ist der 21.09. Beides steht im Kopf dieses Dokuments |

## Was NICHT getan wurde — ausdrücklich

⛔ Kein Code geändert (`git diff --name-only` gegen den Ausgang: nur `docs/`).
⛔ Keine Abbild-Datei erzeugt. ⛔ Keine Sonde geschrieben — auch nicht die
positive Prüfung aus 34.4. ⛔ Kein Hash auf die Sperrliste. ⛔ Keine Wache in
einen Optimierer eingebaut (M4: heute in keinem der neun; Ersteinbau ist
TB-30b). ⛔ `faltenplan.py` nicht angefasst. ⛔ Die offene Frage aus 34.6 nicht
beantwortet.

## Fehler → Regel

Zwei Handwerksfehler in dieser Sitzung, beide im Beleg benannt, keiner mit
Wirkung auf das Register: (1) das erste Zeilenfenster für M3 (`2917,2925`) traf
Kopf- und Trennzeile statt der letzten zwei Bots — am Tabellenkopf nachgemessen
und auf `2919-2927` gesetzt; (2) ein Suchmuster mit Backslash in `grep -F` fand
die Nachtrag-Marke nicht — nachgemessen und die Belegzeile ersetzt. Bestätigt:
**ein Tabellenfenster wird am Kopf der Tabelle verankert, nicht geschätzt**,
und **eine Messung, die 0 liefert, bekommt eine Positivkontrolle** (M1 mit
`\b`, hier gemacht; M3 wäre ohne die Kontrolle „7 von 9" gewesen, und das
hätte den Auftrag fälschlich als abweichend gemeldet).

Bestätigt: `C1` — die *Grund*-Zitate im Auftrag waren Kurzformen; ohne die
Prüfung an der Quelle wären sie als „zeichengleich" ins Register gegangen
(Abweichung 2).

## ⚠️ Offen — nicht Teil dieses Auftrags

| | | bei wem |
|---|---|---|
| 1 | ⚠️ **Zwei Formen der Bestätigungsperiode** (34.6): im Register Datumsspanne `2026-01-01` bis `2026-09-01`, in `faltenplan.py:336` Faltenname (`elliott_wave` `2026-2027`). **Welche gilt, ist nicht registriert** — die Frage liegt bei Fable, Anfrage 21g Punkt 3; 34.6 entscheidet sie nicht | Fable (steuernder Chat legt vor) |
| 2 | **Abbild-Datei, Sonde (mit der positiven Prüfung aus 34.4), Sperrlistenpunkt** — je mit Betreiberfreigabe; Fable setzt den Tag erst, wenn auch der Erzeuger aus Nachtrag 2 registriert ist (21l 4a, 21m Schluss) | Betreiber |
| 3 | **Entscheidungsvorlage 33.5:** geänderter `faltenplan.py` oder neuer Schreiber | Betreiber |
| 4 | **TB-30b:** Wache in allen neun Optimierern (34.5), Erzeuger der `zellen.csv` vor dem Tag | eigener Auftrag |
| 5 | Unverändert offen: 32.5, `fensteranker` in den Messwerkzeugen, Journal-Nachträge (20g)–(20m), Backlog-Zeile `K4t` | — |

## In einfacher Sprache

**Was gemacht wurde:** Fünf Sätze des Prüfers und eine eigene Berichtigung
stehen jetzt im Regelwerk — einmal gesammelt im neuen Abschnitt 34, und
zusätzlich als kurze Marke direkt bei dem Satz, den sie betreffen. Wer den
alten Satz liest, sieht die Berichtigung sofort und muss nicht drei Abschnitte
weiterblättern. Kein alter Satz wurde verändert; das zeigt die Zählung: 221
Zeilen dazu, null Zeilen weg.

**Was gemessen wurde:** Alle Zahlen, die der Auftrag nannte, wurden nachgemessen
und bestätigt: Das Regelwerk kennt das Wort „Rest" nicht (also ist der neue
Satz eine Regel), die Fundstelle „21.4" trägt den alten Satz wirklich nicht,
und in keinem der neun Programme steht heute die Kontrollzeile. Die
Auswertungsjahre je Bot sind vor und nach der Arbeit Zeichen für Zeichen
dieselben.

**Was aufgefallen ist:** Die Begründungszitate im Auftrag waren gekürzt — ins
Regelwerk kamen die vollen Absätze aus der Quelle. Zwei Marken stehen in
Tabellen und sind deshalb Tabellenzeilen, keine eingerückten Blöcke.

**Was nicht gemacht wurde:** Kein Programm geändert, keine Datei erzeugt,
nichts auf die Sperrliste, keine Kontrollzeile eingebaut. Und die Frage, welche
der zwei Bedeutungen von „Bestätigungsperiode" gilt, ist als offen eingetragen —
sie liegt beim Prüfer.

---

## Deine Aufgaben

1. **Fable vorlegen:** Registerabschnitt 34 (Z. 5471 ff.) und die sechs Marken — *Wo:* `docs/VORREGISTRIERUNG_neuselektion.md`, `docs/belege/TB-82/` — *Woran:* seine Antwort auf Anfrage 21g Punkt 3 (zwei Formen der Bestätigungsperiode) entscheidet, was in 34.6 offen steht; sie wird als `FABLE_ANTWORT_2026-09-2…` abgelegt.
2. **Freigabe (33.5 / 34.7):** Abbild-Datei, Sonde und Sperrlistenpunkt als eigene Aufgabe — erst nach 1.

Nicht von dir abhängig: nichts weiter aus diesem Auftrag; alle Commits sind gepusht.
