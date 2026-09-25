# STOFFSAMMLUNG Register 41/42 — was aus Fable 24b bis 25c ins Register gehört, mit Quelle, Art und Stand

**Angelegt:** 25.09.2026, 22:50, vom steuernden Chat, während der Betreiber abwesend ist. **Kein Auftrag, keine Entscheidung.** Die Sammlung soll den Registerauftrag (voraussichtlich TB-108) vorbereiten, sobald Fable 25d und 25e beantwortet hat.

**Stand des Registers (gemessen, 25.09.2026):** Abschnitte **0–40**, 7993 Zeilen, unverändert seit `d0dc890`. Keiner der Einträge unten steht schon im Register.

**Regeln, die für den späteren Auftrag gelten** (aus dem Register und aus Fables Antworten):
- Das Register wird nur angehängt, nie umgeschrieben (Abschnitt 0).
- Fables Registertext wird **zeichengleich** aus der Quelldatei übernommen, mit Quelle.
- Wo Fable einen eigenen Text später berichtigt hat, stehen **beide** Fassungen im Register, die spätere mit Verweis. Ausnahme 24d (a): Der zurückgenommene Text wird nur mit Grund eingetragen, „damit die Ablage nicht zwei Fassungen führt“.
- Am alten Ort steht jeweils eine Marke (Bauart 37.x, 40.x: „⭐ PRÄZISIERT durch …“).
- Sichtschutz 27.1 gilt auch für das Register.

⚠️ **Vorschlag zur Gliederung, von Fable nicht entschieden:**
- **41** nimmt 24b, 24c, 24d auf: Nachweis, Resolver, Deckel/Purge, Mutationsproben.
- **42** nimmt 25a bis 25e auf: Zugriffsklassen, Laufbereich, Rückfälle, Tatsachennotizen TB-103 bis TB-107.

Fable spricht immer von „Register 41/42“, ohne die Grenze zu ziehen. **Das ist eine Frage an Fable, bevor der Auftrag geschrieben wird.**

---

## A. Aus 24b (`FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md`, Abschnitt D Punkt 5)

| | Eintrag | Art | Stand, gemessen |
|---|---|---|---|
| A1 | Berichtigung zu 12: sieben Mutationsproben H1–H7 mit Namen, F4 keine, H0 Grundlauf | Berichtigung | Test seit TB-95 so gebaut |
| A2 | 40.7 „sieben“ | Berichtigung | — |
| A3 | 40.6, der TB-90-Satz | Berichtigung | — |
| A4 | Regel „jede Mutationsprobe beisst allein“ (24b B3) und H6 (eigenständig oder als Paar registriert) | Registertext | seit TB-105 in jedem Auftrag angewandt |
| A5 | Störproben-Satz, Herkunft TB-95 | Registertext | — |
| A6 | Marke an 5.1 Nr. 4, um den zweiten Leser ergänzt; ein Parser | Marke | — |
| A7 | Testrahmen-Notiz | Tatsachennotiz | — |
| A8 | `bot_lauf.py`/`symbol` | Tatsachennotiz | — |
| A9 | Regel „keine Kennzeichnung in Laufcode-Feldern“ | Registertext | — |
| A10 | 24b A2: **kein Fallback unter dem Modus, gleich welcher Art**, Rückgabe 2 | Registertext | umgesetzt TB-103 (Resolver), TB-105 (b)(c)(a), TB-106 (d), TB-107 |
| A11 | 24b A2: neue Tag-Vorbedingung „Trockenlauf aller neun im Modus mit Lesehaken“ | Registertext | gelaufen TB-103, TB-105 F1, TB-106 G5, TB-107 G3; am Tag-Commit zu wiederholen (25a (d)) |
| A12 | 24b A3: Listen-Erzeuger auf dem Signalpfad, Feldliste registriert, Erzeuger unter 36.1 | Registertext | Erzeuger nicht gebaut (Plan-Punkt 3) |

⚠️ In der Zeigerdatei steht noch **TB-100** mit „Registerabschnitt 41 (…Berichtigung ‚sieben statt acht‘…)“. Das ist derselbe Stoff wie A1–A9. Beim Registerauftrag diese Zeile ersetzen oder als erledigt markieren; TB-100 wurde nie ausgelöst.

## B. Aus 24c (`FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md`, Abschnitt 6 Punkt 4)

| | Eintrag | Art | Stand |
|---|---|---|---|
| B1 | Reichweite 5.4: Herleitung aus **gefundenen** Trades | Präzisierung | Wortlaut 5.4 „gefundene“ ja/nein: 24b „Unsicher“, prüfen |
| B2 | Berichtigung der 2d-Herleitung | Berichtigung | ⚠️ durch 24d (a)/(b) teilweise zurückgenommen, siehe C1/C2 |
| B3 | Donchian-Herleitung | Registertext | offen (Erzeuger) |
| B4 | **Nachweis mit zwei Teilen:** bytegleich **und** Leseprotokoll; fehlt eines, ist er 2 | Registertext | angewandt ab TB-103; Benchmark-Nachweis bleibt 2 (zwei Eingaben ausserhalb des Snapshots) |
| B5 | **Resolver-Pflicht** | Registertext | Wortlaut berichtigt durch 25a (a): „über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)“ |
| B6 | `haltedauern_je_bot.csv` historisch | Tatsachennotiz | — |
| B7 | `tb24_haltedauern/auswertung.py` historisch | Tatsachennotiz | — |
| B8 | TB-93/TB-102-Nachweis = 2 | Tatsachennotiz | — |

## C. Aus 24d (`FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md`, Abschnitt 4, Tabelle a–i)

| | Eintrag | Art | Stand |
|---|---|---|---|
| C1 (a) | Rücknahme „`purge_tage` als Schranke über das Raster“ | Rücknahme mit Grund | — |
| C2 (b) | 2d/16.6: Deckel aus gefundenen Trades (P95 + 1), kein Rastermaximum | Registertext | Deckel noch nicht gerechnet |
| C3 (c) | 2d/16.6: Bedingung für den Gewinner auf dessen Positionen | Registertext | „Unsicher“ (4) in 24d: Berichtigung oder Präzisierung, je nach 16.6 |
| C4 (d) | 5.4 bei `elliott_wave`: „gefundene“ greift über die Ausführung | Tatsachennotiz | — |
| C5 (e) | `purge_tage`/„Trainingsende“ | entschieden in 25a (e): **historischer Stand**; Felder aus dem Plan mit TB-104 | umgesetzt TB-104 (`f334a7b`) |
| C6 (f) | „Modus-Lauf = Resolver-Modus; Hilfsordner kein Nachweis“ | Registertext | angewandt ab TB-103 |
| C7 (g) | TB-92 A1b und TB-95 D1 waren Hilfsordner-Läufe; als Nachweise 2 | Tatsachennotiz | — |
| C8 (h) | Berichtigung an 24c: „TB-91 A1b“ lies „TB-92 A1b“ | Berichtigung | — |
| C9 (i) | Widerspruch „Lesehaken erst TB-95“ gegen 39.6/39.8 | nach Messung | **gemessen: Lesehaken seit TB-92, das Register hatte recht** (Fehler des steuernden Chats, Übergabe 25.09. Block 7 Nr. 1; 25a) |

## D. Aus 25a (`FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md`)

| | Eintrag | Art | Stand |
|---|---|---|---|
| D1 | Berichtigung (a) an 24c Abschnitt 2: Resolver-Fundstelle, **achter Fall** | Berichtigung | — |
| D2 | Präzisierung (b) an 24b A2: „0 Zugriffe ausserhalb“ lies nach den drei Klassen | Präzisierung | ergänzt durch 25b (a) Klasse (iv) und 25c (h) registrierte Protokolle |
| D3 | Präzisierung (c) an 24b A2: Symbolmenge nach (1)–(4) in 3 (B) | Präzisierung | Stichtag präzisiert durch 25b (f): Go-Live-Schnitt 5.2 |
| D4 | Ergänzung (d): Wiederholung am Tag-Commit | Ergänzung | — |
| D5 | Ergänzung (e): 24d (e) historischer Stand; Präzisierung zu 33.3/35.4 | Ergänzung | ⚠️ 33.3/35.4-Präzisierung **berichtigt durch 25b (c)**: Plan schrumpft nicht, registrierte Abbildung |
| D6 | Die drei Klassen: (i) Eingaben, (ii) Umgebung nach Liste, (iii) Schreibziele leer (3 (A)) | Registertext | ergänzt durch 25b (a), 25b (b), 25c (g), 25c (h) |
| D7 | Die vier Teile der Symbolbedingung (3 (B)) | Registertext | — |
| D8 | Laufbereich (Abschnitt 4) | Registertext | ⚠️ **berichtigt durch 25b (e)**: Vereinigung aller registrierten Lauf-Typen, Messung am Tag-Commit |
| D9 | Tatsachennotiz TB-103: Resolver mit MANIFEST als Ort; Trockenlauf mit Umgebungsliste; Ladeprotokoll-Teil (4) offen | Tatsachennotiz | Ladeprotokoll-Teil (4) weiter offen, prüfen |
| D10 | Tatsachennotiz Lesehaken (TB-92, `a1b_lesehaken.py`) | Tatsachennotiz | — |
| D11 | Schreibziel-Notiz `manuelle_eingriffe.log` | Tatsachennotiz | **behoben TB-105** (Log erst bei der ersten Zeile) |
| D12 | Einordnung der vier Rückfälle mit Verweis auf 11.1 | Registertext | alle vier geschlossen: (b) TB-105, (c) TB-105, (a) TB-105, (d) TB-106 und TB-107 |

## E. Aus 25b (`FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md`, Abschnitt 4, a–h)

| | Eintrag | Art | Stand |
|---|---|---|---|
| E1 (a) | Klasse (iv) Zwischenablage, drei Bedingungen; Messumgebung (iii)/(iv) dort, wo die Ziele fehlen | Registertext | `tb40_lauf_*` erfüllt seit TB-107; `tb40_faltenplan_*`/`tb40_proben_*` offen (25e Frage 1) |
| E2 (b) | Klasse „Code“ mit Bindung an die Startprüfung; Ergänzung zu 19 (Sauberkeit über den Laufbereich) | Registertext | 19-Erweiterung offen, eigener Auftrag, **Tag-Vorbedingung** (25c 2 (d)) |
| E3 (c) | Berichtigung zu 25a (1): Plan schrumpft nicht; registrierte Abbildung; Feldliste des Plans als Registertext | Berichtigung + Registertext | Feldliste heute im Test (`FELDLISTE_PLAN`/`FELDLISTE_FALTE`, Stand TB-106) |
| E4 (d) | `mindesttraining_jahre`, `embargo_nach_falten`, Berichtszeile: Verfahren-A-Reste; Konstante tot bis 40.8 (h) | Berichtigung | Felder und Zeile entfernt TB-106; Konstante tot, kein Leser (gemessen TB-106) |
| E5 (e) | Berichtigung zu 25a Abschnitt 4: Laufbereich = Vereinigung; Lauf-Typen registriert; Messung am Tag-Commit | Berichtigung + Registertext | Zwischenstand: 81 Module (TB-107, 25.09.) |
| E6 (f) | Präzisierung zu 25a (B)(2): Stichtag = Go-Live-Schnitt (5.2), ausschliesslich | Präzisierung | — |
| E7 (g) | Tatsachennotizen TB-104 | Tatsachennotiz | Werte: Abbild `cb4eb1b4…`, 80 Module, `regimewache` 0/3 |
| E8 (h) | offen bis zur Messung (`_bedingung`, `anhaengen()`, `_min_history`, `MINDESTTRAINING_JAHRE`) | — | **alle vier beantwortet** in 25c und umgesetzt in TB-106/TB-107 |

## F. Aus 25c (`FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md`, Abschnitt 5, a–h)

| | Eintrag | Art | Stand |
|---|---|---|---|
| F1 (a) | „keine Rasterbedingung (Abschnitt 6)“; unbekannter Bedingungstext ⇒ 2, eine Deutung | Berichtigung + Registertext | umgesetzt TB-106 D3; zweite Deutungsstelle `registerdaten.py:605` bis 40.8 (h) |
| F2 (b) | Berichtigung zu 37.4: `herkunft.py` einmal geöffnet für den Datenpfad; „planmässig geöffnet ist nicht offen“ | Berichtigung | umgesetzt TB-106 E; Folgefragen 25d (2)/(3) |
| F3 (c) | Tatsachennotiz zu 11: 11.1 geschlossen (TB-105), 11.2/11.3 offen (TB-30b) | Tatsachennotiz | — |
| F4 (d) | `_min_history` genau ein Treffer oder 2; Erzeugerkette des Trockenlaufs mit dem Faltenplan-Abbild registrieren (33.3) | Registertext | `_min_history` umgesetzt TB-107; Erzeugerkette offen (Abbild TB-101) |
| F5 (e) | Ersatzmodule der Regelbetrieb-Wächter: Tatsachennotiz; unter dem Modus 2; Gegenprobe über alle `__main__`-Stellen | Tatsachennotiz + Registertext | Gegenprobe umgesetzt TB-107; Wächter unverändert (Betreiber 18:09: vorerst nur Notiz) |
| F6 (f) | `getattr`-Ersatz in `strategy_paths.py`: Rückfall, entfernt | Tatsachennotiz | umgesetzt TB-107; Folge `pfadvergleich.py` rc 1 (25e Frage 3) |
| F7 (g) | Klasse (ii) umfasst Interpreter-Caches als Muster; `__pycache__` im Repo nur git-ignoriert und ausserhalb `snapshots/` | Registertext | — |
| F8 (h) | Registrierte Protokolle als eigene Zeile in (iii); append-only; Ordner nicht anlegen; Ausnahme von 19 — **vor dem 19-Auftrag** | Registertext | Ordner-Regel umgesetzt TB-106 E3; Ausnahme von 19 muss vor dem 19-Auftrag im Register stehen |

## G. Tatsachennotizen aus TB-105 bis TB-107 (gemessen, zum Eintragen)

| | Notiz | Quelle |
|---|---|---|
| G1 | 11.1: `pruefe_einbau()` 3 von 3; vorher stiller Weiterlauf von `t3_supertrend` ohne BTCUSDT mit anderem Trade-Hash | `ERGEBNIS_TB-105` A1, B |
| G2 | 14 × „Keine Daten gefunden“ unter dem Modus rc 2; `symbols_config` rc 2 bei leerer oder fehlender Liste | `ERGEBNIS_TB-105` C, D |
| G3 | Ersatzmodule in `kurven_lauf.py`, `determinismus_lauf.py`, `messung_primaerschluessel.py` | `ERGEBNIS_TB-105` Abschnitt 5 Befund 1 |
| G4 | TB-106: A8-Tabelle je Stelle; A5 Rechenregel mit Beleg; `register()` `57ec6573…` ⇒ `0ece95e2…`; Abbild `40ffe18d…`; Datenstand der Kette im Modus = `d9449faf…` | `ERGEBNIS_TB-106` Abschnitt 9 |
| G5 | `auswertung.Abbruch` endet mit 1 (12 Stellen) | `ERGEBNIS_TB-106` A10; Frage 25d (4) |
| G6 | `TB30A_BASE_DIR` wirkt unter dem Modus auf Commit und Registerdatei in `herkunft.py` | `ERGEBNIS_TB-106` A11; Frage 25d (3) |
| G7 | `registerbericht.py --pruefen` rot seit vor TB-106 (erzeugter Block Z. 392 ff. veraltet) | `ERGEBNIS_TB-106` Befund 2; 39.1 |
| G8 | Laufbereich 81 Module (neu `shared/regimewache.py`), Liste `docs/belege/TB-107/f1_laufbereich_vereinigung.txt` | `ERGEBNIS_TB-107` F1 |
| G9 | `elliott_wave` `MIN_HISTORY_HOURS`, die acht anderen `MIN_HISTORY_DAYS`, je genau einmal | `ERGEBNIS_TB-107` A2 |
| G10 | Benchmark-Tabelle `64fb2912…` im Modus (Repo und frischer Klon) und ohne Modus, unverändert durch TB-103 bis TB-107 | TB-103 bis TB-107 |

## H. Noch nicht beantwortet — gehört mit in den Auftrag, sobald die Antworten da sind

- **25d:** (1) Kopie in `faltenplan_neun.py` (in TB-107 schon gebaut, Commit `f5fdb53`, revertierbar) · (2) Prüfansicht `herkunft.py` unter dem Modus · (3) `TB30A_BASE_DIR` unter dem Modus · (4) `Abbruch` rc 1 oder 2.
- **25e:** (1) `tb40_faltenplan_*`/`tb40_proben_*` · (2) `trades.empty ⇒ exit()` · (3) `pfadvergleich.py` rc 1.
- **Gliederung 41/42** (siehe oben) und die **Reihenfolge**: F8 muss vor dem 19-Auftrag im Register stehen.

---

## In einfacher Sprache

Seit dem 24.09. hat der Verfahrensprüfer in sechs Antworten gut sechzig Einträge benannt, die ins Regelwerk gehören: neue Regeln, Berichtigungen seiner eigenen Texte und Tatsachennotizen zu dem, was gemessen wurde. Keiner davon steht bisher im Regelwerk. Diese Sammlung listet sie alle mit Fundstelle, Art und dem heutigen Stand. Der spätere Auftrag muss sie dann nur noch zeichengleich übertragen. Mehrere Einträge sind durch spätere Antworten schon wieder berichtigt; das ist jeweils vermerkt, damit beide Fassungen mit Verweis eingetragen werden.
