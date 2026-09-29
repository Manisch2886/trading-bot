# FABLE_ANFRAGE 2026-09-29b — Tagesanfrage: Sammlung 27.–29.09., Erzeuger F-1…F-17, kalter Leser TB-121 — an: Fable 5.1, bestehender Chat

*Fassung 1, 29.09.2026, steuernder Chat. Dieser Chat steuert seit dem Umzug vom 29.09.; er wurde um 07:26 eröffnet. Stand Repo: HEAD `04f07ef`. Die Anfrage heisst 29b, weil der Buchstabe 29a an deine Antwort zum Betreiberentscheid vergeben ist. Sie verweist auf 27c und wiederholt T116/T117 nicht.*

⛔ **Sichtschutz 27.1:** Die Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Vor dem Übergeben hat ein Helfer sie gegengelesen. Grundlage ist die Regel des Betreibers vom 29.09., 09:20, die deine 29a, Abschnitt 3, auf den steuernden Chat ausdehnt. Die Protokollzeile steht am Ende.

---

## Teil 0. Kenntnis und Stand

1. **27c ist eingegangen.** R18–R32 gehen zeichengleich in den nächsten Registerauftrag (E-2). Die drei Voraussetzungen, die du „zu messen“ nennst (R25 Docstring von `auswertung.py`, R26 `--bot` unter dem Modus, R28 Probe in `shared/snapshot.py`), misst die Sitzung dieses Auftrags, bevor sie einträgt. Weicht eine ab, meldet sie es, statt einzutragen.
2. **T116-5 / R24, Betreiberentscheid 29.09.2026 per Auswahlkarte, wörtlich:** Frage „T116-5 / R24: Soll ein einzelner Bot bis zum Netting bis zu zwei Fünftel des Buchs tragen dürfen?“ ⇒ **„(a) So lassen (Empfohlen)“**. Es gibt keinen Deckel je Bot vor dem Netting. R24 bleibt eine Tatsachennotiz.
3. **Dein Leseprotokoll 27c** nennt eine ausstehende Freigabe für `BACKLOG.md` und `BACKLOG_ENTSCHEIDUNGEN.md`. Sie wird mit dieser Anfrage **nicht** erteilt, weil diese Anfrage sie nicht braucht: Die nötigen Wortlaute aus `BACKLOG_ENTSCHEIDUNGEN.md` (K2h, K2f) stehen unten in Teil 1, Abschnitt D. Ob die Freigabe überhaupt erteilt wird, entscheidet der Betreiber, wenn eine Anfrage sie braucht. Beide Dateien liegen seit TB-118 in der Ablage. Die Zeilen, die die Tatsachennotiz zu 27 betreffen, stehen seitdem in `BACKLOG_SICHTSCHUTZ.md`, und diese Datei kommt nie in die Ablage.
4. **29a ist eingegangen.** Die Ergänzung des Betreibers vom 29.09., 09:20, per Auswahlkarte: Deine Agentenregel aus 29a, Abschnitt 3, gilt als **ein** Regelwerk für alle drei Rollen.
   - Der steuernde Chat setzt Helfer für Recherche, für Fundstellen und als Gegenleser vor jeder Übergabe ein. Das Gegenlesen läuft als Probe über drei Durchgänge; dies ist der erste.
   - Mac-Sitzungen setzen Helfer nur zum Suchen und Lesen ein. Die erste Sitzung, die es tut, misst, ob `deny` auch für die Helfer greift.
   - Der steuernde Chat führt ebenfalls eine Umzugsampel (Schwellen 200 000 / 300 000).
   - Wortlaut: `UEBERGABE.md`, Nachtrag 29.09.2026, 09:20. Das ist eine Kenntnis, keine Frage.
5. **Was mitgeht und was nicht.**
   - Neu in der Ablage, zusammen mit dieser Anfrage: `ERGEBNIS_TB-118_…`, `ERGEBNIS_TB-119_…` und `ERGEBNIS_TB-120_…` (der Schnitt E-1 … E-9 steht in TB-120, Abschnitt 5). Die Sichtschutz-Zeile im Kopf ist nach ARBEITSWEISE 23.1 G5 geprüft; der Helfer hat alle drei gegen 27.1 gelesen.
   - **Nicht** mit geht `ERGEBNIS_TB-121_…`, weil sein Kopf keine Sichtschutz-Zeile trägt (G5). Seine Fragen stehen in Teil 2 wörtlich.
   - Ebenfalls nicht mit gehen die Belege und die Sammlung als Datei. Ihr Inhalt steht in Teil 1.

---

## Teil 1. Die Sammlung vom 27.–29.09., zeichengleich

*Quelle: `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` am HEAD `04f07ef`, Abschnitte B, C und D; die Buchstaben der Überschriften sind die der Sammlung. Abschnitt A der Sammlung („Offen aus Anfrage 27c“) ist durch deine 27c erledigt und entfällt. Abschnitt C beschreibt den Stand vom 27.09.; den heutigen Füllstand misst der steuernde Chat nach dem Ablegen, er steht in `UEBERGABE.md`. Wo die Sammlung von der „Dienstagsanfrage“ spricht, ist diese Anfrage 29b gemeint.*

## B. Aus TB-118 (Projektwissen, Repo-Seite), Abschnitt 9 „Für Fable“, zeichengleich

1. **G1 trifft auf Dateien, die nur in der Ablage liegen** (Abschnitt 8, Punkt 4): Die Annahme in 27b B3 („die
   datierten Kopien … sind im Repo committet“) stimmt für zwei der sechs Registerkopien, nicht für die übrigen vier.
2. **`BACKLOG_ENTSCHEIDUNGEN.md` statt `ENTSCHEIDUNGEN.md`** (Auswahlkarte; DOKUMENTATIONSSTANDARD 10, Wächter).
   Für Teil E: überall, wo 27b `ENTSCHEIDUNGEN.md` nennt, gilt dieser Name.
3. **„K-Einträge“** sind im Backlog ein Namensraum von Abschnitt 4, keine Klasse — offene Aufgaben, Regeln und Lehren
   gemischt. Eingeordnet nach Inhalt.
4. **27b B6 gegen C3 Nr. 3:** Wochenrückmeldung und Fable-Übergabe verlassen die Ablage nach B6 erst mit der nächsten,
   nach C3 sofort. Das Skript folgt B6. Bitte eine Lesart.
5. **„Die zwei jüngsten Paare“:** Die Regel in Teil D E2 sagt Datums-Buchstaben-Paare (heute 27a, 27b), B6 nannte 26a
   und 27a als Tagesanfragen. Das Skript folgt E2; 26a verlässt die Ablage.
6. **„offen“ im Index** ist eng gemessen: Frage oder Messbitte ohne spätere Anfrage, die sie aufnimmt. 27a ist offen,
   weil die Rückmeldung zu TB-116/117 (27c) fehlt — damit hält B5 die Ergebnisse 114/115 in der Ablage, obwohl
   Register 46 steht. B4 hält `MAC_TB-117` (Grundlage 27a); `MAC_TB-116` (Grundlage 26a) geht, obwohl sein Ergebnis
   noch nicht angenommen ist — die Regel koppelt an die Grundlage des Auftrags, nicht an die Annahme.
7. **Drei mehrdeutige Stellen im `REGISTER_INDEX.md`** (4a, 30.2 (3), 33.2/33.3) — dort ist der Wortlaut zu lesen.
8. **G7:** gesichert wird `docs/` als Archiv, nicht das ganze Repo (Auswahlkarte). Für Teil E (ARBEITSWEISE 7b):
   „db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz`“.
9. **D2:** 14 Regeln aus den Übergaben stehen nicht im Regelwerk; eine davon (19/6) widerspricht ARBEITSWEISE 6d.
   Vorlage für den Nachtrag in `d2_fehlende_regeln.txt`.

## C. Kenntnis: die Ablage ist geräumt (27b C4 vollzogen, 27.09.2026)

- Vorher **148 Dateien, 1 570 315 Tokens (79 %)**, nachher **40 Dateien, 638 044 Tokens (32 %)**. Reihenfolge nach C4: erst 13 Dateien abgelegt (Registerkopie Teil 1–4, `REGISTER_INDEX`, `FABLE_DIALOG_INDEX`, `UEBERGABE.md`, `BACKLOG.md` ersetzt, `BACKLOG_ENTSCHEIDUNGEN`, `LOESCHLISTE_TB-118`, `MAC_TB-117`, `MAC_TB-118`, Anfrage 27b), dann 120 entfernt, dann gemessen. Zwei Dateien nach dem Ablegen zurückgelesen: md5 gleich.
- **Zu B1 (G1):** Die 14 Dateien, die nur in der Ablage lagen, sind **vor** dem Entfernen ins Repo gesichert (md5 gleich, noch uncommittet): Registerkopien 21.09. und 24.09. Teil 1–3, `belege/TB-91/…`, `belege/TB-93/…`, 25f, 22f, Wochenrückmeldung 19.09., PRÜFUNG, ERINNERUNG, SITZUNGSWÄCHTER, PROJEKTSTAND, Anfrage 27c.
- Betreiberentscheid: `PROJEKTSTAND_2026-09-26_einfache_sprache.md` (ohne Regel im Skript) bleibt in der Ablage, bis es einen fortgeschriebenen Projektstand ohne Datum gibt.
- **27.5-Meldung:** `projektfuehrung/UEBERGABE.md`, Block 7 der alten Übergabe, Zeile 99 — in der Ablagefassung ist der Wert gestrichen; die Repo-Fassung zieht die nächste Mac-Sitzung nach. Inhalt nicht wiedergegeben.
- Nicht in der Ablage (27b): `BACKLOG_SICHTSCHUTZ.md`, `BACKLOG_ERLEDIGT_2026-09.md`, `belege/`.

## D. Bis Dienstag hinzugekommen

*(wird fortgeschrieben — je Eintrag: Datum, Herkunft, Frage, Neigung)*

### 27.09., TB-119: D2 19/6 gegen ARBEITSWEISE 6d

*Herkunft: `docs/ERGEBNIS_TB-119_repo_nachziehen_regelwerk_nachtrag.md`, Schritt C2; Vorlage
`docs/belege/TB-118/d2_fehlende_regeln.txt`, Zeile 19/6. Nach Auftrag TB-119 nicht ins Regelwerk eingetragen.*

**Wortlaut 1** — `projektfuehrung/UEBERGABE_2026-09-19.md`, Block 7 (Fassung 19.09.), Nr. 6, Spalte „Regel“:
> ⭐ **Ein Abbruchkriterium benennt die Sache, nie ihr Merkmal.** Und: fallen Wortlaut und Zweck auseinander und ist
> jemand erreichbar — **fragen**, nicht entscheiden

**Wortlaut 2** — `projektfuehrung/ARBEITSWEISE.md` 6d, Unterabschnitt „Nur richtungsweisende Rückfragen — und die als
Multiple Choice (22.09.2026)“, Tabelle „NICHT richtungsweisend“, Z. 898 (Stand `df825b6`):
> ⚠️⚠️ **Ein Abbruchkriterium.** Es führt zu **ABBRUCH und Meldung** — nie zu einer Rückfrage. *Wer bei einem
> Abbruchkriterium fragt, verwandelt eine Wache in eine Verhandlung*

**Hinweis:** `projektfuehrung/BACKLOG_ENTSCHEIDUNGEN.md`, Eintrag **K2h** (Z. 111), führt den zweiten Satz von
Wortlaut 1 als Regel (T55b.5) mit dem Zusatz „— in ARBEITSWEISE §7c“. In ARBEITSWEISE 7c steht dazu nichts: 7c nennt
das Abbruchkriterium nur als Zeile „gilt nur für Fehlschläge, **die den Gegenstand der Aufgabe betreffen** (T44.11)“.
Gemessen: `grep -n -i abbruchkriterium` in ARBEITSWEISE, vier Treffer (Z. 155, 898, 1118, 1129 am Stand `7eadc7a`),
keiner mit „fragen“. — Die erste Hälfte von Wortlaut 1 steht als **K2f** (Z. 109, „gehört auch in
`docs/PRUEFPRINZIPIEN.md`“) und widerspricht 6d nicht; sie ist mit 19/6 nach Auftrag ebenfalls nicht eingetragen.

**Frage:** Welche Regel gilt, wenn Wortlaut und Zweck eines Abbruchkriteriums auseinanderfallen und jemand erreichbar
ist: **fragen** (Übergabe 19.09., K2h, T55b.5) oder **Abbruch und Meldung** (ARBEITSWEISE 6d, 22.09.)? Und soll die
erste Hälfte (K2f) getrennt davon eingetragen werden — wenn ja, wohin?

**Neigung:** keine — Mac-Sitzung; die Neigung gibt der steuernde Chat. Zwei Tatsachen dazu: 6d ist die jüngere
Regel und nennt ihre Fälle „abschliessend“; `BACKLOG_ARCHIV.md` T54.2 führt einen Fall, in dem Fragen nach K2h eine
Nummernkollision verhindert hat.

**Neigung des steuernden Chats (27.09., 19:00):** 6d gilt. Beide Sätze lassen sich vereinbaren: Die Sitzung bricht ab und meldet. Die Meldung nennt ausdrücklich, dass Wortlaut und Zweck auseinanderfallen. Der Betreiber entscheidet danach, nicht die Sitzung davor. K2h würde entsprechend umformuliert, und die Stelle „ARBEITSWEISE §7c“ entfällt. K2f (die Sache, nie ihr Merkmal) gehört als Regel in PRUEFPRINZIPIEN, getrennt von 19/6.

### 27.09., TB-119: drei weitere Punkte aus `ERGEBNIS_TB-119`, Abschnitt 6

*Herkunft: `docs/ERGEBNIS_TB-119_repo_nachziehen_regelwerk_nachtrag.md`, Abschnitt 6, Nr. 1, 2 und 4; Belege `docs/belege/TB-119/b_offen.txt`.*

1. **Lesart „Erinnerung als Träger“.**
   - Befund: G1 und Teil E nennen als Träger nur das Repo (Mac + GitHub) und die iCloud-Kopie. Die Erinnerung nennen sie nicht.
   - Umsetzung in TB-119 ohne eigene Entscheidung: In UMZUG 2 bleibt die Zeile „Erinnerung“ stehen. In DOKUMENTATIONSSTANDARD 6 steht jetzt der Satz, die Erinnerung „trägt kein Dokument, sondern wie gearbeitet wird“.
   - Frage: Ist das so gemeint?
   - Neigung: ja. Die Erinnerung trägt Arbeitsweise, keine Belege.
2. **Drei Stellen ausserhalb von Teil E nennen die Ablage weiter einen Träger:**
   - ARBEITSWEISE 10, „Die drei Sätze“, Satz 2;
   - ARBEITSWEISE 15, Tabelle „Die Träger …“, Zeile „Projektablage“;
   - UMZUG, Einleitung, Zeile „Die Anhänge“.
   - Frage: Nach G1 nachziehen?
   - Neigung: ja, als Handwerk mit dem nächsten Regelwerksauftrag. Der Grund steht in G1, kein Ergebnis.
3. **Kenntnis:** Die 13 D2-Regeln sind eingetragen:
   - PRÜFPRINZIPIEN A9, A10, B7, C8;
   - ARBEITSWEISE 14 (drei Regeln) und 15 (sechs Regeln; 21/6 nur als Verweis auf Register 27.5).
   - Die acht TEILWEISE-Regeln bleiben, wie sie sind.
   - Frage: Soll je TEILWEISE-Zeile entschieden werden, oder bleiben alle acht so?
   - Neigung: so lassen, bis ein Fall sie braucht.

### 27.09., steuernder Chat: 27.4 beim Ablegen von `MAC_TB-119`

`auftraege/MAC_TB-119_repo_nachziehen_regelwerk_nachtrag.md`, Z. 69 und 73, nennt den nach 27.5 gestrichenen Wert. Der Grund: Der Auftrag musste die Ersetzung wörtlich angeben.

- Folge: Der Auftrag geht **nicht** in die Ablage, obwohl B4 ihn als offenen Auftrag zu 27b hineinnähme. Das Ergebnis TB-119 enthält den Wert nicht und geht mit der Dienstagsanfrage hinein.
- Frage: Soll ein Auftrag, der eine Streichung nach 27.5 vollzieht, künftig den Wert nur mit Fundstelle nennen und die Zeile per Muster finden lassen?
- Neigung: ja.

### 27.09., TB-120: siebzehn Fragen zum Erzeuger

*Herkunft: `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`, Abschnitt 6, zeichengleich übernommen. Die Wortlaute stehen vollständig in `docs/belege/TB-120/b_offen.md`. Der Schnitt in neun Aufträge E-1 … E-9 steht im Ergebnis, Abschnitt 5, und muss am Dienstag mit.*

Ohne Neigung. F-1 … F-11 sind O-1 … O-11 aus `b_offen.md`; dort stehen die Wortlaute vollständig und geprüft, hier
gekürzt. Herkunft jeweils: diese Sitzung, `docs/belege/TB-120/`.

- **F-1 (O-1) Zeilen in `zellen.csv`.** R5 (b): „`zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die
  Zeilenzahl ist gleich der Zahl der Zellen“ — Vertrag `auswertung.py`: „genau eine Zeile je (Zelle x Falte), fuer ALLE
  Falten des Faltenplans, Bestaetigungsperiode eingeschlossen.“ Welcher Mengenbegriff gilt für die Abnahme?
- **F-2 (O-2) Leere Trade-Liste.** R5 (b) „(Sharpe 0 nach Registertext 1c, leere Trade-Liste)“, 43-7 „(leere Liste,
  Sharpe 0 nach 1c)“; der Vertrag kennt keine Trade-Liste je Zelle. Gibt es sie als Rohergebnis, in welcher Datei, mit
  welchen Feldern?
- **F-3 (O-3) Kill-Test-Werte.** 22.2: „Der Lauf berichtet je Bot für den Plateau-Gewinner drei Werte“. `auswertung.py`
  rechnet sie nicht; bestes Symbol und fünf beste Trades brauchen Daten, die der Vertrag nicht führt. Zellen-Erzeuger
  oder `auswertung.py` (Öffnung der Punkte 3/5/14)?
- **F-4 (O-4) Bootstrap.** 15.3 (a): „Jedes Bootstrap-Intervall im Auswertungsskript wird auf der Reihe der täglichen
  Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet“; 15.3 (b) L = max(„mediane Haltedauer des Parametersatzes in Handelstagen“, …). Im Code 0 Treffer für `bootstrap`; der Vertrag führt keine Haltedauer. Wo entsteht
  das Intervall, und liefert der Erzeuger die Haltedauer je Zelle?
- **F-5 (O-5) Zwei Drawdowns.** 24.2: MtM-Drawdown bewertet, „Der ereignisindizierte Drawdown aus
  `equity_simulation.py` wird berichtet, nicht bewertet.“ — `beispieldaten.py`: „der Kapital-Drawdown einer Falte
  steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt“. Der Vertrag hat eine Spalte. Wo steht
  der ereignisindizierte Wert?
- **F-6 (O-6) Embargo und Beginn der Bestätigung.** 16.6: „Die Bestätigungsperiode eines Bots beginnt am ersten
  Handelstag nach Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen ist.“; 41.3 C3: „für den
  Gewinner auf dessen eigenen simulierten Positionen“ — 15.6/38.1: Bestätigungsfalte `2026-01-01/2026-09-01`,
  Go-Live-Schnitt „2026-09-01, ausschliesslich“. (1) Wo wird die Bedingung ausgewertet, wenn der Gewinner erst in
  `auswertung.py` feststeht? (2) Wie verhält sich „nach Go-Live“ zu dieser Spanne?
- **F-7 (O-7) 3b (d).** Symbolzahl, Anteil, Auslassungen mit Grund und Faltenkohärenz „Berichtet je Bot und Falte“;
  16.11 Z. 7: „Der spätere Auswerter tut es noch nicht“. Die Kohärenz braucht die Rangfolge aller Zellen. Wo?
- **F-8 (O-8) Benchmark-Tagesreihe.** Vertrag: `benchmark_tagesreihen/<markt>.csv`, „das gleichgewichtete
  point-in-time-Universum, taeglich.“ — 23.3: „aus den Symbolen gebildet, die der Loader des Bots an diesem Tag
  handelbar macht“. 46.3 nennt diese Datei nicht als Ausgabe. Wer schreibt sie, je Markt oder je Bot?
- **F-9 (O-9) 36.1 für Rohergebnisse.** 36.1 gilt für Pfade, die „auf der Sperrliste steht oder für sie bestimmt ist“;
  der Plan: „unterliegt der Schreibregel 36.1 von Anfang an“. Genügt der Plan, oder braucht es einen Registersatz?
- **F-10 (O-10) `haltedauer_balken`.** Name registriert (B6/B7), Zählregel und Einheit nicht; `positionen_holen.py`
  zählt `kerzen` „beide Enden eingeschlossen“. Welche Zählregel, welche Einheit, welche Umrechnung für den Deckel in
  Handelstagen?
- **F-11 (O-11) Bindung der neuen Listen.** 40.6: „und als Punkt auf die Sperrliste aufgenommen“ — R3: „gehören mit
  ihrem Hash in die Gruppe `eingefroren` des Abbilds“. Beides, oder erfüllt R3 den Satz aus 40.6?
- **F-12 Ort des Zellen-Kerns.** 11.2: `evaluate_combination_multi` liefere den Kapital-Drawdown „noch nicht“ mit,
  „Das nachzurüsten ist TB-30b.“; 29.4/34.5: die Wache „wird in allen neun `multi_symbol_optimise.py` eingebaut“ —
  `PLAN_VOR_DEM_TAG.md`, Posten 2: „im Erzeuger (10)“. Gemessen: `evaluate_combination_multi` simuliert nicht und
  verwirft Zellen. Wird es zum Zellen-Kern umgebaut, oder rechnet der Erzeuger über `collect_all_trades` und
  `simulate_portfolio` — und schützt die Wache in den Optimierern dann den Lauf?
- **F-13 Reihenfolge Listen gegen Posten 4.** 40.6 verlangt die Listen „mit dem registrierten Code“. Posten 4 (26.2,
  Horizont je Bot) ändert den Signalpfad der vier Aktien-Bots. Werden die Listen vor oder nach Posten 4 erzeugt?
  (Posten 3 mit unveränderten Voreinstellungen ändert keine Ausgabe; das ist messbar.)
- **F-14 Ausgeführte Positionen.** `simuliere_portfolio` gibt sie nicht heraus; A9 verbietet die Kennzeichnung; die
  MtM-Tagesreihe (1a, 24.2) braucht sie. Ist eine zusätzliche Rückgabe aus `shared/zuteilung.py` (Sperrlistenpunkt 10,
  Rechnung unverändert) als beauftragte Änderung nach 37.3 der Weg, oder ein anderer?
- **F-15 Abnahme vor dem Tag ohne Ergebnis.** R5 (b) (Zeilenzahl, Nullzeile) ist erst an einem Lauf prüfbar; ein Lauf
  des Zellen-Erzeugers auf dem Snapshot erzeugt vor dem Tag Ergebnisgrössen des Selektionsraums. Womit wird er vor dem
  Tag abgenommen (synthetische Eingaben, Teilraster, nur Struktur)?
- **F-16 Übernahme von `mtm_kern.py`.** Der MtM-Kern liegt in `research/mtm_drawdown/` (TB-73). Import aus dort
  (Laufbereich wächst um ein Research-Modul) oder Verlagerung nach `shared/`? *Kann auch Handwerk sein; hier genannt,
  weil es den Laufbereich (R4) ändert.*
- **F-17 Parameterdateien.** 40.6 (Folgerung TB-96): „je Bot die Hashes der Parameterdateien“. Gemessen stehen
  Handelsparameter auch als Konstanten in `backtest_*.py` (z. B. `SMA_TREND_PERIOD = 200` in
  `rsi2_mean_reversion/backtest_rsi2.py`; 15.4 zitiert `MAX_HOLD_HOURS` aus `backtest_elliott.py`). Welche Dateien sind
  „Parameterdateien“?

**Neigungen des steuernden Chats zu F-1 … F-17 (27.09., 20:15).** Wo „keine“ steht, sehe ich zwei tragfähige Wege und lege mich vor Fable nicht fest.

| F | Neigung |
|---|---|
| F-1 | Zeilen je (Zelle × Falte), einschliesslich Bestätigungsperiode; R5 (b) als Kurzform lesen. Abnahme: Zeilenzahl = Zellen × Falten des Faltenplans je Bot |
| F-2 | keine; hängt an F-3 |
| F-3 | keine. Jeder Weg öffnet etwas: den Erzeuger-Vertrag oder `auswertung.py` (Punkte 3/5/14) |
| F-4 | keine; hängt an F-3 (dieselbe Frage: welche Daten je Zelle) |
| F-5 | keine |
| F-6 | keine |
| F-7 | keine |
| F-8 | keine |
| F-9 | ein Registersatz. Der Plan ist kein Registertext (K2g: jede Behauptung braucht ihren Beleg im Repo, und die Regel gehört ins Register, nicht in den Plan) |
| F-10 | keine |
| F-11 | keine |
| F-12 | Der Erzeuger rechnet über `collect_all_trades` und `simulate_portfolio`; `evaluate_combination_multi` bleibt ausserhalb des Laufs. Die Wache 29.4 gehört dann in den Pfad, den der Lauf wirklich nimmt; Posten 5 wäre danach neu zu fassen |
| F-13 | Listen **nach** Posten 4. 40.6 verlangt „den registrierten Code“, und das ist der Code am Tag. Listen vor Posten 4 wären an einen Signalpfad gebunden, der danach wechselt |
| F-14 | ja: eine zusätzliche Rückgabe aus `shared/zuteilung.py` als beauftragte Änderung nach 37.3, mit dem Nachweis, dass die Rechnung bytegleich bleibt |
| F-15 | Abnahme vor dem Tag nur auf synthetischen Eingaben (`beispieldaten.py`) und auf Struktur (Zeilenzahl, Nullzeile, Felder); kein Lauf auf dem Snapshot vor dem Tag |
| F-16 | keine |
| F-17 | Parameterdateien sind alle Dateien, aus denen der Signalpfad eines Bots einen Handelsparameter liest (`live_params.py` und `backtest_*.py`), per AST gemessen, nicht per Namensliste |


---

## Teil 2. TB-121: kalter Leser des Registers, Abschnitte 0–12 (Fable 25f V8/F3)

*Quelle: `docs/ERGEBNIS_TB-121_kalter_leser_register_1_12.md`, Commit `04f07ef`. Gelesen wurden die Zeilen 1–1225 des Registers, sha256 `18e39ee2…`.*

**Befund in Zahlen (Verfahren, kein Ergebnis):**
- 85 Befunde der Arten B 19 · V 19 · W 8 · M 16 · A 15 · Z 8. Jedes Zitat ist maschinell als Teil einer Registerzeile geprüft.
- Vollständigkeitstest, kalt angewandt: Von 12 Bausteinen des Auswertungsskripts sind 3 aus 0–12 schreibbar, 2 teilweise, 7 nicht.
- Die grössten Lücken: Sharpe, Calmar und Exposure sind nicht definiert, und der gültige Faltenplan steht ausserhalb von 0–12.
- Stichprobe Text gegen Code: 12 von 12 Stellen gefunden und passend.

Es folgt der Abschnitt „Für Fable“ des Ergebnisses, zeichengleich, mit den Fragen 39–77. Die Sitzung hat sie ohne Neigung gestellt. Der steuernde Chat gibt zu diesen 39 Fragen ebenfalls keine: Es sind Lesarten des Registers, und die sind deine.

## Für Fable

Jeder Befund der Arten W, M und A als Frage, mit Zeile und Zitat, ohne Neigung. Nummern wie in `a_befunde.md`.

### Widersprüche (W)

39. **Wächst die Bestätigungsperiode mit dem Forward-Test (5.1 Nr. 7), oder endet sie am Go-Live-Schnitt 2026-09-01 (5.2)?** — Zeile 596 / 617–619, Zitat: „Und sie wächst jeden Monat.“
40. **Sind `ableitung` bei `bb_squeeze_percentile` oben und `methode` bei der Stop-Zusatzstufe und bei `bb_lookback` unten weitere Ausnahmen neben den zwei in 2.2 benannten, oder fallen sie unter diese beiden?** — Zeile 119–126 / 264, 279, 340, 356, 360, Zitat: „Zwei Grenzen stützen sich auf keine davon.“
41. **Gilt die Stufungsregel aus 2.7 (geometrisch, Faktor 1,5–2,0) für die Quantil-Achsen `rsi_threshold` und `adx_threshold`, oder ist für sie eine andere Stufungsart vorgesehen, und wo steht sie?** — Zeile 209–213 / 254, 257, 272, Zitat: „für Skalenparameter (Faktor 1,5 bis 2,0, drei bis fünf“
42. **Hat Festlegung 4 in ihrem Wortlaut ein Exposure-Argument, oder ergibt es sich erst aus 4.2?** — Zeile 59 / 467–470, Zitat: „Da der Benchmark-Drawdown nach“
43. **Sind die Zahlen in Abschnitt 3 (Benchmark-Tabelle) und 4.4 die der Tabelle, die der Lauf liest, oder die des historischen Stands `benchmark_drawdowns.json`?** — Zeile 408, 461–465, 511 / 931–933, 945–951, Zitat: „Die vollständige Tabelle (1 % bis 100 % in Schritten von 1 %)“
44. **Welche Prüfungs- und Mutationsprobenzahl gilt für den Stand, an dem das Register gelesen wird: 165 und acht (Marke 40.7) oder 196 und sieben (Marke 41.1)?** — Zeile 1206–1208 / 1211–1214, Zitat: „der Test zählt heute 165 Prüfungen (40.1)“
45. **Gilt die Fundstellenregel aus Abschnitt 0 auch für Marken, die Wortlaut aus Abschnitten ab 38 wiedergeben, etwa `registerdaten.py:605` in der Marke aus 42.3?** — Zeile 16–21 / 730, Zitat: „die zweite Deutungsstelle (`registerdaten.py:605`)“
46. **Welcher Stand gilt für das Register: der im Kopf genannte 14.09.2026 oder der Stand der jüngsten Marke?** — Zeile 3 / 16–23 … 1220–1222, Zitat: „Stand: 14.09.2026. Dies ist das Register.“

### Mehrdeutigkeiten (M)

47. **Wird die DSR je Bot mit N = 653 plus den eigenen Zellen gerechnet, oder mit dem Bot-Anteil `N_historisch` plus den eigenen Zellen?** — Zeile 65 / 369–380, 845–848, Zitat: „N = 653 plus die Zellen dieses Laufs, je Bot getrennt.“
48. **Was gilt, wenn der Gewinner eine Spitze ist und der beste Nicht-Spitzen-Punkt (a) nicht erfüllt: bleibt der Bot mit der Spitze, oder wird der Nicht-Spitzen-Punkt gespielt?** — Zeile 753, Zitat: „der beste Nicht-Spitzen-Punkt erfüllt (a)“
49. **Wird der Kapital-Drawdown einer Falte auf einem je Falte neu gestarteten Kapitalpfad gemessen, oder als Ausschnitt eines durchgehenden Pfads?** — Zeile 443–445, Zitat: „Kapital-Drawdown in dieser Falte nicht tiefer liegt als“
50. **Wird `DD_Toleranz(e)` bei der Exposure der jeweiligen Falte ausgewertet oder bei einer über die Falten gemittelten Exposure?** — Zeile 455–456, 473, Zitat: „DD_Toleranz(e) = Median über die Selektionsfalten von DD_Benchmark(f, e)“
51. **Ist der Benchmark eine statische Position mit driftenden Gewichten oder eine täglich gleichgewichtete Tagesrendite?** — Zeile 453 / 958, Zitat: „gleichgewichtete Tagesrenditen,“
52. **Welche Rasterpunkte gelten als Kante: jede Achse an ihrer ersten oder letzten Stufe, auch die Zusatzstufen „kein“ und „structural“ und die Obergrenze des Positionslimits?** — Zeile 167–170, Zitat: „Liegt der Gewinner auf einer Rasterkante, wird“
53. **Meint (b) „alle Falten“ die Selektionsfalten oder schliesst es die Bestätigungsperiode ein?** — Zeile 750 / 445, Zitat: „erfüllt die Drawdown-Bedingung in allen Falten“
54. **Über welchen Zeitraum wird das mittlere Exposure der Kapitalregel gemessen?** — Zeile 781–782, Zitat: „mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.“
55. **Verbindet die Clusterschwelle Zellen bei Korrelation ≥ 0,9 oder > 0,9, und welches Korrelationsmass gilt?** — Zeile 862–866, Zitat: „transitiv fortgesetzt (Einfachverkettung)“
56. **Wird beim Zufalls-Timing über die aneinandergehängten Selektionsfalten oder je Falte verschoben, welche Rendite wird verglichen, und wie wird das 95. Perzentil gerechnet?** — Zeile 823–828, Zitat: „so erzeugten Renditen gegen die Rendite des Satzes.“
57. **Ist die Grundlage `haltedauer` eine Hypothese oder eine Messung, und wenn eine Messung: aus gefundenen oder aus ausgeführten Trades?** — Zeile 286 / 346, Zitat: „Ein Rueckblick kuerzer als die gemessene Median-Haltedauer dieses Bots“
58. **Heisst „gefunden“ bei `elliott_wave` „unter der Kapitalschranke ausgeführt“, oder ist es eine Ausnahme vom Grundsatz aus 5.4?** — Zeile 683–684, Zitat: „greift „gefundene" über die“
59. **Welcher Lauf ist mit „nach dem Lauf“ (15.09.2026) gemeint?** — Zeile 6 / 1035, Zitat: „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“
60. **Welche zwei Bug-Fixes aus Abschnitt 11 sind Voraussetzung des Laufs, und gilt 11.3 ebenfalls als Voraussetzung?** — Zeile 1020–1021, 1087, 1182–1184 / 201, 1095–1157, Zitat: „Der Lauf darf nicht beginnen, bevor die beiden Bug-Fixes“
61. **Gilt die Regel „keine Ziffer, die mit einem Live-Wert zusammenfallen kann“ nur für Grenzsätze oder auch für erzeugte Tabellentexte wie „Median 20-Balken-Spanne“?** — Zeile 104–105 / 236, Zitat: „Median 20-Balken-Spanne“
62. **Kommen „Kapital-Drawdown je Falte“ und „drei tiefste Falten-Drawdowns“ im Bericht aus der täglichen MtM-Reihe oder aus der ereignisindizierten Kurve?** — Zeile 69 / 805–807, Zitat: „die Berichtswert bleibt“

### Nicht ausführbar (A)

63. **Wie ist der Netto-Sharpe einer Falte definiert (Renditereihe, Frequenz, Annualisierung, Kostenabzug)?** — Zeile 57, 750, 775, Zitat: „Median des Netto-Sharpe über die Selektionsfalten“
64. **Wie ist Calmar definiert, und mit welchem Faktor wird Alpha annualisiert?** — Zeile 58, 752, 762, 767, 773, Zitat: „Verglichen wird Calmar gegen Calmar.“
65. **Mit welchen Eingaben wird die DSR gerechnet (welcher Sharpe, Beobachtungszahl, Schiefe, Wölbung, Streuung der Versuchs-Sharpes)?** — Zeile 874–876, Zitat: „Gerechnet wird nach Bailey/López de Prado, ohne“
66. **Wo steht der gültige Krypto-Faltenplan, und soll 0–12 auf ihn verweisen?** — Zeile 396–400, 635–636, Zitat: „Der Krypto-Faltenplan wird geschrieben, sobald TB-31 gemeldet hat“
67. **Wie wird der Benchmark-Drawdown für die Krypto-Bots gebildet, insbesondere für die 1h- und 4h-Bots?** — Zeile 410–428, Zitat: „gilt für alle Bots dieses Marktes mit gleichem Faltenplan“
68. **Wo ist das Format der Rohergebnisse beschrieben, gegen das `auswertung.py` prüft?** — Zeile 804, 1189, Zitat: „Wo die Rohergebnisse den Vertrag verletzen, bricht es“
69. **Wie ist die mittlere Exposure definiert (Grösse, Zeitpunkt, Kalender- oder Handelstage)?** — Zeile 453–455, 765–767, 823, Zitat: „in Höhe der mittleren Exposure“
70. **Wie wird unter 1 % Exposure und bei Exposure 0 in der Benchmark-Tabelle nachgeschlagen?** — Zeile 461–464, Zitat: „beiden benachbarten Stützstellen“
71. **Wie entstehen die Zwischenstufen der Quantil-Achsen, und auf welcher Verteilung (Zeitraum, Zeitrahmen, Universum) sind die ADX- und RSI-Quantile gemessen?** — Zeile 254, 257, 272, 318, 330, Zitat: „Die Schwelle ist als Quantil der gemessenen ADX-Verteilung des Universums gesetzt“
72. **Welche Sätze begründen die Grenzen von `t3_slow_length`, `donchian_period` oben und `stop_mode` unten und oben?** — Zeile 253, 261, 262, 276, 277 / 286, Zitat: „Ein Satz je Grenze, der“
73. **Wie wird der Zellenname gebildet, der bei Gleichstand alphabetisch entscheidet?** — Zeile 739, Zitat: „dann der alphabetisch erste Zellenname“
74. **Wie gross ist die Stichprobe beim Hash-Vergleich nach 10.1, und wie wird sie gezogen?** — Zeile 1067–1069, Zitat: „Stichproben-Hash-Vergleich.“
75. **Wie wird der Mittelwert der drei tiefsten Falten-Drawdowns bei weniger als drei Selektionsfalten gebildet?** — Zeile 806, Zitat: „Mittelwert der **drei tiefsten** Falten-Drawdowns“
76. **Welche Fill-Konvention gilt für den Ausstieg?** — Zeile 983–985, Zitat: „je Order, Ein- und Ausstieg; Einstieg zum“
77. **Wie lautet der vollständige Datenstand-Hash, gegen den geprüft wird, und soll er in 0–12 stehen?** — Zeile 1044, Zitat: „d9449faf51bffaaa…“


---

## Teil 3. Frage 78: Die Sitzung TB-121 war nicht vollständig kalt

*Quelle: `ERGEBNIS_TB-121`, Abschnitt „Was die Sitzung ausser 0–12 gesehen hat“.*

Die Tatsache: Claude Code lädt von selbst ein Gedächtnisverzeichnis (`MEMORY.md`) mit einzeiligen Zusammenfassungen früherer Sitzungen, darunter zu den Registerabschnitten 15–46.
- Die Sitzung sagt, kein Befund stütze sich darauf.
- Verweise auf spätere Abschnitte seien als V aufgenommen und nicht aus dem Gedächtnis beantwortet worden.
- Ob das Vorwissen die *Auswahl* der Befunde gefärbt hat, „lässt sich von innen nicht ausschliessen“.

**Fragen:**
1. Trägt TB-121 unter diesen Umständen als kalter Leser im Sinn von V8/F3, oder nur als gewöhnlicher Leser?
2. Soll bei künftigen kalten Lesern das Gedächtnis der Sitzung vorher ausgeschaltet oder umgangen werden, und gehört das dann als Bedingung in den Auftrag?

**Neigung des steuernden Chats:**
1. Die Befunde mit Zitat tragen. Jedes Zitat ist am Wortlaut geprüft, und ein Gedächtnis erzeugt keine Zeile im Register. Nicht belegt ist, dass die Befundliste vollständig ist.
2. Ja, als Schritt 0 des Auftrags, mit einem Beleg, dass das Gedächtnis nicht geladen wurde.

---

## Antwortform

- Wie bisher: „Kurz“, „Unsicher“, die Umzugsampel und am Ende der Registerblock, zeichengleich kopierbar und nummeriert, **ab R33**.
- Handwerk nennst du als Handwerk. Ein Registertext, der aus einer Frage folgt, bekommt seine Quelle des Grundes.
- Die 39 Fragen aus Teil 2 darfst du bündeln, wo sie denselben Registertext berühren. Nenne dann je R-Block die Nummern, die er beantwortet. Frage 78 steht für sich.

---

*Protokoll des Gegenlesens (Probe, Durchgang 1, 29.09.2026):*
- *Ein Helfer hat den Entwurf gelesen: Mechanik (beide übernommenen Blöcke `diff` rc 0), jede Zahl und Fundstelle der neuen Teile gegen die Quelle, den ganzen Text und `ERGEBNIS_TB-118/119/120` gegen 27.1.*
- *Befunde: 6 Stellen in den neuen Teilen berichtigt (Herkunft der Gegenleser-Regel, fehlende Protokollzeile, Verweis auf den falschen Teil, Buchstaben der Teile, „`BACKLOG*.md` geht nicht mit“, Neigung unter der Überschrift „ohne Neigung“).*
- *Einen 27.1-Verdacht in `ERGEBNIS_TB-118` hat der steuernde Chat an der Stelle selbst geprüft: Es ist eine Kettenrang-Nummer, kein Ergebnis.*
- *Im Entwurf und in TB-119/120: keine Verdachtsfälle.*
- *Nachtrag des steuernden Chats nach dem Gegenlesen: Die übernommene Neigungstabelle endete in einer ersten Fassung bei F-16, weil der Übernahmebereich um eine Zeile zu kurz vorgegeben war (die Zeile zu F-17 fehlte). Der Gegenleser prüfte gegen denselben zu kurzen Bereich und konnte es nicht sehen. Berichtigt vor dem Übergeben; übernommen sind jetzt die Sammlung ab Zeile 16 bis zum Dateiende und TB-121 bis zur Zeile vor dem nächsten Abschnitt.*
