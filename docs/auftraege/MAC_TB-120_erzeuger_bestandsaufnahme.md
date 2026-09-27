# TB-120 Erzeuger — Bestandsaufnahme, nur lesend: Listen-Erzeuger (40.6) und Zellen-Erzeuger (Stufe V, R5/R16), dazu TB-30b Posten 2–6; vorab UMZUG 6 auf `UEBERGABE.md`

**Sitzungstitel:** `TB-120` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 27.09.2026, 19:10, vom steuernden Chat
**Vorgänger:** TB-119 (abgegeben `d9e3600`, geschlossen 27.09., 18:45).
**Kein Fable bis Dienstag, 29.09.** Alles, was an Fable geht, kommt ins Ergebnis unter „Für Fable“. Der steuernde Chat überträgt es in `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md`. Die Sitzung schreibt dort **nicht** hinein.

## ⭐⭐ Freigabe des Betreibers, wörtlich

- **27.09.2026, 18:08, Chat:** *„bis Dienstag arbeiten wir strukturier ohne fable weiter und sammeln alles für fable soweit möglich“*
- **27.09.2026, ca. 18:25, Auswahlkarte „Was soll bis Dienstag ohne Fable laufen?“**, darin die Option *„Erzeuger: Bestandsaufnahme (Empfohlen) — Nur lesend: Was existiert für Stufe V, was fehlt gegen R5? Ergebnis ist ein Plan und Fragen für Dienstag.“* ⇒ Antwort: **„Wir arbeiten alles strukturiert ab“.**

⛔ **Nicht freigegeben:**
- Code ändern, gleich wo;
- einen Optimierer, eine Simulation, einen Backtest, `faltenplan.py main()`, `positionen_holen.py` oder irgendeinen Erzeuger **laufen lassen**;
- in `research/**/ergebnisse/` oder `research/**/daten/` schreiben;
- Register, Sperrliste, Abbilder, `crontab`, Datenbanken.

Erlaubt sind Lesen (`grep`, `ast`, `git log`, `sha256sum`) und die Sonde, nur wenn sie nachweislich nichts schreibt (wie in TB-119 A2).

**Sichtschutz 27.1:** Diese Sitzung erzeugt **keine** Ergebnisgrösse des Selektionsraums und liest keine: keine Trade-Liste, keine Kennzahl eines Parametersatzes, keine Datei unter `research/tb24_haltedauern/daten/`. Hashes und Zeilenzahlen dieser Dateien sind erlaubt, Inhalte nicht. Das Ergebnis geht in die Projektablage.

In einfacher Sprache: Das grösste Stück Arbeit bis zum grossen Lauf ist der Erzeuger, also das Programm, das die Rohergebnisse schreibt. Niemand hat bisher gemessen, was davon schon da ist. Diese Sitzung liest nur. Sie schreibt eine Liste: was das Regelwerk vom Erzeuger verlangt, was im Code schon existiert, was fehlt, wie man den Bau in Aufträge schneiden kann, und welche Fragen am Dienstag an Fable gehen. Vorab zieht sie eine Zeile im Umzugsdokument nach, damit ein neuer Chat die richtige Übergabe liest.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short`. Erwartet sind genau diese drei Dateien:

| Datei | Zustand | md5 |
|---|---|---|
| `docs/auftraege/MAC_TB-120_erzeuger_bestandsaufnahme.md` | neu | (dieser Auftrag) |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | geändert | Zeiger; die Zeile TB-119 ist entfernt |
| `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` | geändert | `d08f5431b0bcfc459cec5a6e1056e408`, numstat gegen HEAD **32/0** |

Weicht etwas ab ⇒ Abbruch. Danach der Commit `TB-120 Schritt 0`, dann pushen.

0b. In `docs/belege/TB-120/0b_ausgang.txt` festhalten:
- HEAD;
- sha256 des Registers;
- `git status --porcelain | wc -l`.

0c. db-Sicherung nach 7c Schritt 0.

## Schritt A — UMZUG 6, Eröffnungstext: auf `UEBERGABE.md` zeigen

**Grundlage:** UMZUG, Tabellenzeile „Übergabe-Name“ (Z. 295 am Stand `d9e3600`), wörtlich:
*„⚠️ Beim Umbenennen der Übergabe (offener Punkt in ihrem Kopf: `UEBERGABE.md` ohne Datum) wird diese eine Zeile mitgezogen“.*
Befund aus `ERGEBNIS_TB-119`, Abschnitt 7: Der Eröffnungstext nennt noch `UEBERGABE_2026-09-25.md`.

A1. In `docs/projektfuehrung/UMZUG.md` im Eröffnungstext (Z. 257–258 am Stand `d9e3600`) genau diese Stellen ändern:
- `UEBERGABE_2026-09-25.md` ⇒ `UEBERGABE.md`;
- `docs/projektfuehrung/UEBERGABE_2026-09-25.md` ⇒ `docs/projektfuehrung/UEBERGABE.md`.

Nichts sonst. Kommt der alte Name im Eröffnungstext öfter vor, wird jede Stelle genannt und ersetzt, und alle stehen im Nachweis. Ausserhalb des Eröffnungstexts wird nichts ersetzt.

Nachweis in `a1_nachweis.txt`:
- Zeile davor und danach;
- numstat;
- `grep -n 'UEBERGABE_2026-09-25' docs/projektfuehrung/UMZUG.md` danach. Jeder verbleibende Treffer wird mit seinem Zweck genannt, zum Beispiel ein Vorgängerverweis.

Commit `TB-120 A UMZUG 6 auf UEBERGABE.md`.

## Schritt B — Anforderungen an die zwei Erzeuger, aus dem Register gelesen

Eine Tabelle in `b_anforderungen.md`, je Anforderung eine Zeile mit diesen Spalten:
- Nr.;
- Anforderung (ein Satz);
- Fundstelle (Registerabschnitt, zeichengleiches Kurzzitat ≤ 15 Wörter);
- welcher Erzeuger: Listen (L) oder Zellen (Z);
- vor dem Tag ja/nein, mit Fundstelle.

Gelesen wird **mindestens** Folgendes; Ketten und Marken werden über `REGISTER_INDEX.md` bis zur geltenden Fassung verfolgt:

| Quelle | Inhalt |
|---|---|
| 40.6, 41.1 A12, 45.3, **46.3 (R12)** | zwei Erzeuger; Bindung der Listen; `EINGEFROREN` |
| **45.5 (R5)** (a)–(c) und **46.7 (R16)** (b) = R5 (d) | Abnahmebedingungen |
| 22d / Feld `teile` in `herkunft.json` | Fundstelle suchen |
| 17.4 (5e) und 19 | Lese-Audit, Codeherkunft |
| 36.1 | Schreibregel, Einmal-Schreibsperre |
| 15.2–15.6, 16.6 (2d), 16.7 (3b (a)–(e)), 41.2 B1, 41.3 C1–C3 | Verfahren B, Faltenzuordnung, Embargo als Bedingung am Bestand, gefundene Trades |
| 11.2, 11.3; `PLAN_VOR_DEM_TAG.md` „TB-30b im Einzelnen“ Posten 2–6 und 8 | Posten 8 ist die Wache gegen Walk-Forward-Aufrufe |
| 22.2 | Kill-Test-Berichtswerte: vom Erzeuger zu liefern oder von `auswertung.py`? |
| 43.2 (43-7) | null Trades ist ein Wert; nie ohne Ausgabe |
| 12 und 46.5 (R14), Lesart 46.9 | was `auswertung.py` vom Erzeuger erwartet |
| Kopf und Docstring von `research/vorregistrierung/auswertung.py` | Datenvertrag: Dateinamen, Spalten, Pflichtfelder |

Wo zwei Stellen verschiedenes verlangen oder eine Anforderung unklar ist ⇒ nicht entscheiden. Die Stelle in `b_offen.md` nennen, mit beiden Wortlauten.

⚠️ **Pfade:** Bei `research/vorregistrierung/` liegt der Ordner nicht unter `docs/`. Die Sitzung misst die Pfade selbst von der Repo-Wurzel aus (`git ls-files | grep`). Sie rät keine Pfade.

## Schritt C — Bestand im Code, gemessen

`c_bestand.md`: Für jede Zeile aus B steht dort, was im Code existiert, mit Datei, Bezeichner und Commit. Die Einordnung ist eine von vier:
- **vorhanden**;
- **teilweise** (was fehlt);
- **fehlt**;
- **nicht prüfbar ohne Lauf**. Dieser Fall wird nicht gelaufen, sondern benannt.

Mindestens zu messen:

C1. **Listen-Erzeuger:** `research/tb24_haltedauern/positionen_holen.py`:
- `--ziel` und `O_EXCL`;
- wo „gefunden“ statt „ausgeführt“ gezählt wird (41.2 B1);
- ob der Modus und der Resolver genutzt werden;
- welche Parameterdateien er liest und ob der Parameterstand protokolliert wird (40.6 verlangt ihn als Tatsachennotiz);
- ob `elliott_wave` über die Ausführung zählt (41.3 C4).

Zusätzlich die Hashes der neun heutigen Listen gegen `docs/belege/TB-114/`, nur Hashes.

C2. **Zellen-Erzeuger:** Gibt es irgendeinen Ansatz?
- Suche nach `zellen.csv`, `tagesreihen`, `herkunft.json`, `teile`, `Lese-Audit`/`lese_audit`/`audit_zeilen` über das ganze Repo, mit Fundstellen;
- was `auswertung.py` und `beispieldaten.py` als Format der Rohergebnisse voraussetzen;
- ob `beispieldaten.py` die Gestalt von `zellen.csv` und `tagesreihen/` schon vollständig vorgibt, sodass ein Erzeuger gegen diese Gestalt gebaut werden kann.

C3. **Rechenkern:** Welche Funktion rechnet heute eine Zelle?
- `evaluate_combination_multi` in den neun `multi_symbol_optimise.py`;
- `equity_simulation.py`;
- `shared/zuteilung.py`.

Dazu je Bot:
- liefert der Kern den Kapital-Drawdown (11.2)?
- liefert er eine Tagesreihe der Netto-Mark-to-Market-Renditen (15.3, 24)?
- liefert er Trades mit Einstiegs- und Ausstiegszeit und `haltedauer_balken` (24b A3)?

C4. **TB-30b Posten 3–5:**
- Posten 3: Durchreichung `sma_trend_filter`, `bb_squeeze_percentile`, `bb_lookback`;
- Posten 4: `entry_cutoff` je Bot (26.1);
- Posten 5: Wache 29.4 in allen neun Optimierern (34.5).

Je Bot die Einordnung vorhanden, teilweise oder fehlt.

C5. **Posten 8:** Wird irgendwo verhindert, dass ein `multi_symbol_walk_forward.py` im Modus läuft? Die Fundstelle angeben, oder „fehlt“.

C6. **Laufbereich:** Die 81 Module aus 44-8 lesen, nicht neu messen. Welche davon ein Erzeuger importieren würde, soweit aus C3 erkennbar.

## Schritt D — Plan und Fragen

`d_plan.md` enthält:

D1. **Lückenliste**, sortiert nach „vor dem Tag“ und nach Abhängigkeit.

D2. **Schnitt in Aufträge:** Vorschlag, in wie viele Aufträge der Bau zerfällt, in welcher Reihenfolge, je Auftrag mit Gegenstand, Abnahme aus R5/R16 und den Dateien, die geöffnet werden müssen.
- Ausdrücklich zu nennen: welche Datei auf der Sperrliste steht oder in `EINGEFROREN` liegt und damit eine Öffnung nach 37.3 braucht.
- Umfang je Auftrag schätzen. Die Schätzung ist als „geschätzt“ markiert (K2o).

D3. **Was ohne Fable gebaut werden kann**, nämlich alles, was keine offene Lesart berührt, und **was auf Fable wartet**. Das gilt insbesondere für:
- 27c (L2–L5, T117-5 `paths.py`);
- die Offenen aus `b_offen.md`.

## Schritt E — Ergebnis

`docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` enthält:
- die Schritte 0 bis D mit Nachweisen;
- die Tabellen aus B, C und D, oder Verweise auf die Belege, wenn sie länger als etwa 60 Zeilen sind;
- **„Für Fable“**: jede Frage mit Herkunft, beiden Wortlauten, falls es zwei gibt, und ohne Neigung (die gibt der steuernde Chat);
- „Nicht getan, und warum“;
- „In einfacher Sprache“.

Dazu ein Journal-Eintrag, der Abgabe-Commit und das Pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- Eine Messung verlangt einen Lauf, der schreibt oder rechnet ⇒ nicht laufen lassen. Die Messung als „nicht prüfbar ohne Lauf“ benennen und weitermachen. Das ist kein Abbruch der Sitzung.
- Eine Datei, deren Inhalt eine Ergebnisgrösse nach 27.1 sein könnte, müsste gelesen werden ⇒ nur Hash und Grösse, Inhalt nicht.
- Schritt 0a weicht ab ⇒ Abbruch.
