# FABLE-Anfrage 16.10.b — G6 elliott_wave_stocks: Testfalte 2020 seit TB-163 E-6 nicht erreichbar (Registerfrage)

*Steuernder Chat, 16.10.2026, 08:50, Repo-Stand `5167e96`. Zweite Anfrage im Chat „Fable Trading Bots-16.10.2026 a“; Übergabe 16.10.a gilt. **Registerfrage.** Die genannten Register-Dateien liegen in der Projektablage unter projektfuehrung/ (Projekt-Werkzeug, nicht der Ordner auf dem Mac). Zitate per Skript aus dem Register (Commit `173368f`, 12 271 Zeilen, sha256 `fac7a7a2…` = Stand HEAD) und aus dem Code am HEAD.*

## Teil 0 — Kenntnis

1. Register 0–61, eingetragen bis R99; R100–R101 stehen in deiner Antwort 15.10.b, noch nicht eingetragen. Dein Block hier beginnt bei R102.
2. Betreiberentscheid 16.10.2026: dich fragen; der Arbeitsbaum von TB-166 E-3a (20 Dateien, ungecommittet) bleibt bis zu deiner Antwort stehen. Die Paper-Bots berührt er nicht; Eile ist nicht belegt.

## Befund (belegt)

1. **5.1 Nr. 4**, Z. 613: „4. **2020 und 2022 sind Testfalten, keine Trainingsjahre.**“ Z. 600–601: „**Unberührt** bleiben Nr. 4 (2020 und 2022 sind keine Trainingsjahre — unter Verfahren B gibt es gar kein Training)“ Z. 609–611: „**Aktien:** Testfalten sind die Kalenderjahre **2019 bis zum Go-Live-Schnitt**, Training ab Datenbeginn, mindestens **vier Jahre** vor der ersten Falte.“
2. **G6** (`test_vorregistrierung.py` Z. 640–650, im Arbeitsbaum unverändert): je Bot müssen die Jahre aus Nr. 4 in Falten der Rolle `selektion` liegen. Die erste Falte ist die erste Kandidatenfalte ab 4a mit H ≥ 1 im Loader-Trockenlauf (Sicht je Faltenende) über `load_all_symbol_data` des Bots.
3. **E-6** (TB-163, Commit `11a267f`; Register 60.1 Z. 12168–12181; Freigabe Z. 12170). Am HEAD `strategies/elliott_wave_stocks/multi_symbol_optimise.py` Z. 112–113: `cutoff = horizontbeginn_ts(df["open_time"])` / `df = df[df["open_time"] >= cutoff].reset_index(drop=True)`; danach Z. 116 `if timespan_days < MIN_HISTORY_DAYS:` mit Z. 52 `MIN_HISTORY_DAYS = 1825`. Vorher: `open_time.max()` minus 10 Jahre (Datenuhr).
4. **Folge** (in Kopien des Codes nachgerechnet; Teilmessung, 150 Symbole `sp500_top150`, ohne `entferne_unvollstaendige`): H am Faltenende 2017–2020 neu 0, alt 135–137; 2021 beide 139. Ein Symbol lädt erst ab 2016-09-19 + 1825 Tage = 2021-09-18. Erste Falte ews am `639044c` (= `11a267f^`) 2017, Selektionsfalten 2017–2025, G6 grün; am `4a3d6cf` (HEAD-Code ohne Patch) 2021, Selektionsfalten 2021–2025, G6 rot (2020 fehlt, 2022 abgedeckt). Der Patch E-3a berührt diesen Weg nicht. Erschlossen: unbemerkt, weil TB-163 nur `test_posten4_horizont` lief.
5. **Die drei anderen Aktien-Bots** setzen den Horizont als `entry_cutoff`, die Zeilen bleiben; G6 dort grün. `rsi2_mean_reversion` Z. 75–79: „KEINE Kappung auf RECENT_YEARS_ONLY vor der Indikator-Berechnung“; die Längenprüfung steht vor dem Schnitt (Z. 106 `if timespan_days < MIN_HISTORY_DAYS:`, Z. 112 `entry_cutoff = horizontbeginn_ts(df["open_time"])`).

## Stellen für und gegen die Lesart von E-6

- **R81 (d)**, 55.4 Z. 11775: „Dass die vier Aktien-Bots den frühesten Einstieg, elliott_wave_stocks den Anfang der geladenen Zeilen, aus der letzten Zeile der Datei bilden, ist die Datenuhr, die 26.2 ablöst … [Voraussetzung, mit Posten 4 zu messen: dass danach bei keinem der vier Bots das Ende einer Datei in Fenster, Scanbeginn oder Anfang der geladenen Zeilen eingeht.]“ — nennt für ews ausdrücklich den Anfang der geladenen Zeilen; E-6 folgt diesem Wortlaut.
- **26.2**, Z. 4927–4928: „ein Symbol trägt vor dem Horizontbeginn keinen Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet.“ — spricht vom Einstieg, nicht von Zeilen.
- **28.6**, Z. 5355: „Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand.“ Dazu deine Begründung Z. 5357–5358: „Ein Vorlauf, der auf Kursen vor dem Horizontbeginn rechnet, ist derselbe Zugriff“ (präzisiert durch R53, 49.1; Zählweise R57, 51.2: ab dem ersten Balken ab Horizontbeginn). Danach rechnen auch die drei anderen Bots ihre Indikatoren auf Zeilen vor dem Horizontbeginn. Ob das 28.6 widerspricht, ist nicht gemessen.

## Fragen (je: einverstanden oder anders, weil …)

(a) Ist der Zeilenschnitt in ews nach E-6 die vorgesehene Lesart von R81 (d), oder setzt ews den Horizont wie die anderen drei als Einstiegsschranke (Zeilen bleiben)? **Neigung:** Einstiegsschranke wie die anderen drei (26.2 spricht vom Einstieg; G6 wieder 2017–2025). Gegen die Neigung stehen der Wortlaut von R81 (d) und 28.6/R57. Nur als Möglichkeit, nicht gemessen: Längenprüfung vor dem Schnitt wie rsi2 Z. 106, Zeilenschnitt bleibt.
(b) Falls die Lesart bleibt: Ist eine Einschränkung von 5.1 Nr. 4 für ews vor dem Tag zulässig? Z. 618 ff.: G6 liest Z. 613 maschinell; eine Änderung der Sache braucht einen eigenen Registereintrag und die Anpassung von G6 im selben Auftrag. **Neigung (Entwurf):** nein, Nr. 4 bleibt „unberührt“ (Z. 600).
(c) Darf E-3a (TB-166) mit der Abhilfe zusammen fortgesetzt werden, oder erst getrennt? Beide ändern `strategies/elliott_wave_stocks/multi_symbol_optimise.py` (E-3a nur `get_trades_for_symbol`). **Neigung (Entwurf):** getrennt, die Abhilfe zuerst mit eigenem Hash-Übergang nach 37.3, E-3a danach, weil die Ursache vor E-3a liegt.

## Nicht gefragt

Rentabilität. BACKLOG, `ergebnisse/` und `docs/belege/` musst du nicht lesen.

## Lesen und Ablage

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_05 (Register Z. 588–749), _15 (Z. 1369–1828; ersetzt 5.1, Nr. 4 bleibt nach Z. 600 unberührt — bitte die Kette prüfen), _26 (4833–5156), _28 (5246–5386), _49 (11098–11128), _51 (11318–11427), _55 (11736–11854), _60 (12162–12203); die Übergabe 16.10.a. Fehlt eine dieser Kopien in der Ablage, melde das. Deine Antwort umfasst höchstens 10 KB; lege sie ab als projektfuehrung/FABLE_ANTWORT_2026-10-16b_<stichwort>.md, Registerblock zeichengleich kopierbar, nummeriert ab R102.
