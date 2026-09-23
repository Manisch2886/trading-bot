"""TB-89: fuegt Abschnitt 38 und die vierzehn Marken in das Register ein.
Rein additiv: jede Marke wird NACH einer eindeutigen Ankerzeile eingefuegt,
keine bestehende Zeile wird veraendert. Zitate werden zeilengenau aus der
Fable-Antwort 22h uebernommen (Platzhalter «Q:<zeile>»)."""
import re, sys
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
QUELLE = "docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md"
VORLAGE = sys.argv[1]

q = open(QUELLE, encoding="utf-8").read().split("\n")
def zitat(m):
    z = q[int(m.group(1)) - 1]
    assert z.strip(), m.group(0)
    return z if z.startswith("> ") else "> " + z
abschnitt = re.sub(r"«Q:(\d+)»", zitat, open(VORLAGE, encoding="utf-8").read())
assert "«Q:" not in abschnitt

zeilen = open(REG, encoding="utf-8").read().split("\n")

def nach(anker, text, start=None):
    """Fuegt text nach der einzigen Zeile == anker ein (ab Zeile start)."""
    idx = [i for i, z in enumerate(zeilen) if z == anker
           and (start is None or i >= start)]
    assert len(idx) == 1, (anker[:60], len(idx))
    i = idx[0]
    zeilen[i + 1:i + 1] = text.split("\n")

def zeile_von(prefix):
    idx = [i for i, z in enumerate(zeilen) if z.startswith(prefix)]
    assert len(idx) == 1, prefix; return idx[0]

# --- Marke 1: Kopf von Abschnitt 0 (38.2) ---
nach("## 0. Warum es dieses Dokument gibt", """
> ⭐ **Registertext, Ersteintrag — Fundstellen (38.2, Fable 22h, TB-89,
> 23.09.2026):** Ein Registertext nennt Fundstellen im Code als **Datei und
> Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als
> Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem
> Commit, an dem sie gemessen wurden. *Eine Zeilennummer ohne Commit ist keine
> Fundstelle.* Gilt für jeden Registertext ab Abschnitt 38; ältere Abschnitte
> bleiben zeichengleich, ihre Zeilenangaben gelten für ihren Commit-Stand
> (30.3). Wortlaut, Herkunft und Grund in **38.2**.""")

# --- Marken 2-4: 35.1, unter der bestehenden Marke aus 36.1 (4)/36.3 ---
nach("> dahin: `python3 faltenplan.py` nicht aufrufen.", """
> ⭐⭐ **Berichtigung (38.1, Fable 22h, TB-89, 23.09.2026) — Weg (A):** Der
> Satz „die Änderung ist eine Zeile" im Handwerkszitat oben ist berichtigt.
> Der Bezeichner entsteht **dort, wo die letzte Falte ihren Namen bekommt**
> (`faltenplan.py`, Funktion `_plan`, Zuweisung der Rolle `bestaetigung`): die
> letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`; Faltenname,
> `bestaetigungsperiode`, Spalte `falte` und Bericht tragen denselben String
> aus derselben Quelle. Weg (B) — zwei Namen für dieselbe Periode — ist
> unzulässig. Umsetzung: TB-90, Freigabe liegt vor.

> ⚠️ **Tatsachennotiz zu den Zeilennummern oben (38.7 (a), TB-88, belegt
> 38.2):** Am Stand `8851f67` steht die Erzeugung auf **Z. 338**, die
> Konsolenausgabe auf **Z. 460** von `faltenplan.py` (Funktionen `_plan` und
> `main`); verschoben durch **`4daa254`** (TB-86 Schritt 2/3). Die Zahlen 336
> und 368 oben bleiben zeichengleich; sie gelten für den Stand, an dem TB-83
> sie gemessen hat.

> ⚠️⚠️ **Tatsachennotiz (38.7 (c), TB-88, Messstand `8851f67`):** Weg (B)
> hätte einen Sperrlistenpunkt berührt — `auswertung.py`, Funktion
> `lies_zellen`, vergleicht die Menge der `falte`-Werte gegen die Faltennamen
> des Plans und bricht unter (B) ab (Sperrlistenpunkt 5). Weg (A) läuft in der
> Probe durch. Einzelheiten in **38.1**.""")

# --- Marke 5: 21.9, unter der Betreiberentscheidung (38.3) ---
nach("> unverändert; die neu gerechnete Tabelle liegt als eigene Datei daneben.", """
> ⭐⭐ **Tatsachennotiz (38.3, Fable 22h, TB-89, 23.09.2026):** Der Vollzug von
> Sperrlistenpunkt 4 vor dem Tag ist eine **beauftragte Änderung nach 37.3** —
> Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. **Kein
> Amendment nach 10.1, kein Protokolleintrag**; das Protokoll entsteht mit dem
> Erzeuger. Das Wort „Amendment" oben bleibt zeichengleich; es stammt aus einer
> Zeit, in der der Begriff für beides stand (23.6). Die Reihenfolge-Entscheidung
> gilt weiter. Die Form des Vollzugs steht in **38.4**.""")

# --- Marke 6: 21.9, unter der Tabelle der Folgen (38.7 (d)) ---
nach("| Abschnitt 3, *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle\"* | wird im selben Zug berichtigt; die Prämisse trägt seit 21.5 nicht mehr |", """
> ⚠️⚠️ **Tatsachennotiz zur ersten Zeile (38.7 (d), TB-88, Messstand
> `8851f67`):** „rot" heisst heute: `test_vorregistrierung.py` **stürzt ab**
> (`KeyError: '2017'` in `auswertung.py`, Funktion `zulaessigkeit`), **0
> bestanden, 0 gescheitert**. Nach dem simulierten Vollzug: **163 bestanden,
> 2 gescheitert** (`G6`, `H3`) — beide hängen am Faltenplan, nicht an der
> Tabelle. ⚠️ **OFFENE FRAGE bei Fable (Anfrage 22i, Abschnitt 3), nicht
> entschieden:** ob „grün" Fertigkriterium des Vollzugs bleibt. Bis dahin gilt
> die Zeile oben unverändert: offen durch eigene Änderung, blockierend für den
> Tag. Einzelheiten in **38.7 (d)**.""")

# --- Marke 7: 10.1 (38.3) ---
nach("Vorregistrierung liefen.", """
> ⭐⭐ **Tatsachennotiz (38.3, Fable 22h, TB-89, 23.09.2026):** Diese Regel
> betrifft Bug-Fixes **nach** Beginn des Laufs; das Protokoll ist der Ort der
> **Läufe** und ihrer Amendments, und vor dem ersten Lauf gibt es nichts, was
> dort stünde. Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist daher **kein
> Amendment nach 10.1** und erzeugt **keinen Protokolleintrag**, sondern ist
> eine beauftragte Änderung nach 37.3. Das Protokoll entsteht mit dem Erzeuger
> und beginnt mit dem Stand des Tags. Wortlaut und Grund in **38.3**.""")

# --- Marke 8: Sperrlistenpunkt 4 (38.4), ohne Leerzeile ---
nach("   Interpolationsregel**", """   > ⭐ **Form (ii) (38.4, Fable 22h, TB-89, 23.09.2026) — Form steht fest,
   > Vollzug steht aus:** Punkt 4 nennt künftig **beide** Dateien;
   > `ergebnisse/benchmark_drawdowns.json` (`a163c498…`) bleibt gesperrt und
   > unverändert als **registrierter historischer Stand** mit Tatsachennotiz,
   > wie Punkt 2 (30.3); `ergebnisse/benchmark_drawdowns_vt.json` ist die
   > Tabelle, die der Lauf liest. Nicht (i) (Streichen) und nicht (iii)
   > (ERSETZT-Marke). ⛔ **Der Punkttext oben ist NICHT geändert** — der Vollzug
   > ist Plan-Punkt 8 (37.3, kein Amendment, 38.3) und wartet auf zwei offene
   > Fragen an Fable (Anfrage 22i: „grün" als Fertigkriterium; welche Tabelle
   > für `t3_supertrend`).""")

# --- Marke 9: Punkt 7 (38.5), unter der Marke aus 37.5 ---
nach("   > nicht.", """   >
   > ⭐ **Der Ort steht schon (38.5, Fable 22h, TB-89, 23.09.2026):**
   > `registerdaten.py` ist ein Modul, ein Ort, und steht als Punkt 1 auf der
   > Sperrliste — **hier ist nichts zu verschieben.** Punkt 7 bekommt den Ort
   > nachgetragen (`registerdaten.py`, `CLUSTER_SCHWELLE` und
   > `N_HISTORISCH_JE_BOT`); die Sonde prüft Datei plus Wert. Fables Kandidat
   > aus 22d war für Punkt 7 keiner. Der Nachtrag selbst ist Handwerk (TB-90).""",
     start=zeile_von("7. **N-Buchführung und Clusterschwelle**"))

# --- Marken 10-11: Punkt 9 (38.5 und 38.7 (b)), unter der Marke aus 37.5 ---
nach("   > Umsetzung **ungeschützt**. Die Werte `0,1` / `0,05` ändern sich nicht.", """   >
   > ⭐⭐ **Neun Importe, nicht neun überwachte Kopien (38.5, Fable 22h, TB-89,
   > 23.09.2026):** Kein Laufmodul trägt eine eigene Kopie — die neun
   > `backtest_*.py` ersetzen ihre Zuweisung durch den **Import** aus einem
   > neuen Modul, das mit Hash auf diese Liste kommt. Fable: *„Ein Import ist
   > keine Prüfung, sondern eine **Struktur**"* (38.5). Der Papierpfad (`forward_test.py`) und
   > `messgroessen.py` (`GEBUEHR_PCT`) bleiben **überwachte** Kopien. Modul und
   > Importe: TB-90; bis dahin gilt die Marke oben.
   >
   > ⭐ **Tatsachennotiz (38.7 (b), Slippage):** **9 von 9** `backtest_*.py`
   > tragen `SLIPPAGE_PCT = 0.05` und rechnen `2 * (TRADING_FEE_PCT +
   > SLIPPAGE_PCT)` = **0,30 %** — genau die Summe dieses Punktes, Ein- und
   > Ausstieg. Formabweichung ohne Wertunterschied bei `t3_supertrend`
   > (`pnl_pct -= …`). Gemessen in Anfrage 22i (HEAD `ec54618`), in TB-89 lesend
   > nachgemessen am Stand `da251da`, gleich.""")

# --- Marke 12: 23.7, unter dem Nachtrag TB-71 (38.7 (d)) ---
nach("Abschnitt 24.*", """
> ⚠️⚠️ **Tatsachennotiz (38.7 (d), TB-88, Messstand `8851f67`, eingetragen
> TB-89, 23.09.2026):** Der Vollzug der Sperrlisten-Änderung braucht nach 38.3
> kein Amendment (37.3) und hat seit 38.4 seine Form (ii). Fables
> Fertigkriterium „`test_vorregistrierung.py` grün" ist heute **nicht
> erreichbar**: der Test stürzt ab (`KeyError: '2017'`), nach dem simulierten
> Vollzug bleibt er **163/2** (`G6`, `H3`, beide am Faltenplan). Die fünfte
> Zeile oben („G6/H3 aus TB-61 nicht repariert") gilt fort. ⚠️ **OFFENE FRAGE
> bei Fable (Anfrage 22i), nicht entschieden.** Einzelheiten in **38.7 (d)**.""",
     start=zeile_von("### 23.7 "))

# --- Marke 13: 37.4, unter Fables Tatsachennotiz (38.6) ---
nach([z for z in zeilen if z.startswith("> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):**")][0], """
> ⚠️ **ERSETZT (38.6, Fable 22h, TB-89, 23.09.2026) — zwei Stellen dieses
> Satzes, der Satz selbst bleibt zeichengleich:** (a) „`auswertung.py` Z. 41"
> lies **Z. 51** (Fables Berichtigung (a)). (b) Der Halbsatz „weicht von dieser
> an fünf Stellen ab (fehlend: …; zusätzlich: …)" ist ersetzt durch Fables
> Ersatzsatz — acht Stellen, vier fehlend und vier zusätzlich; der Wortlaut
> steht zeichengleich in **38.6**. Beleg ist die Tatsachennotiz TB-87 (M3)
> unten.""")

# --- Marke 14: 37.5, direkt unter dem Registertext (38.5) ---
nach([z for z in zeilen if z.startswith("> **(4)** Tatsachennotiz zu 7 und 9, jetzt:")][0], """
> ⭐⭐ **Entscheidung zu (2) und (3) (38.5, Fable 22h, TB-89, 23.09.2026):** Es
> bleibt bei (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun
> `backtest_*.py` beziehen `TRADING_FEE_PCT` / `SLIPPAGE_PCT` künftig per
> Import aus einem **neuen** Modul (die Kandidaten aus (3) sind blockiert); der
> Papierpfad und `messgroessen.py` / `GEBUEHR_PCT` bleiben überwachte Kopien.
> **Für Punkt 7 ist (3) schon erfüllt:** `registerdaten.py` ist der Ort, nichts
> wird verschoben. Wortlaut und Begründung in **38.5**.""")

text = "\n".join(zeilen)
assert text.endswith("\n")
text = text + "\n" + abschnitt.lstrip("\n")
open(REG, "w", encoding="utf-8").write(text)
print("ok")
