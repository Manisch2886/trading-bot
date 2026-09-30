# Vormessung E-2 — Voraussetzungen aus Fable 27c/29b, gemessen am 29.09.2026

*Empfänger: Repo `docs/projektfuehrung/`, Grundlage für den Registerauftrag E-2 und für die Vorprüfung nach dem Fable-Filter (UEBERGABE 20:48, Block 4 Nr. 1 und 3). Geschrieben vom steuernden Chat (seit 29.09., ca. 20:55).*

**Stand:** HEAD `0034960` (`003496011e354950b50c9d0873decee3b3cd4818`). Nur gelesen, über die Geräteanbindung. Zwei unabhängige Helfer (A misst, B liest gegen), dazu eigene Nachmessung von R48 (g) und R26.
**md5 HEAD = Arbeitsbaum** für `kennzahlen.py` (`568ce2c7…`); `auswertung.py` Arbeitsbaum `4f4b455e…`, seit `852f253` ohne Commit (`git log 852f253..HEAD` leer).

Quellen: **27c** = `FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`, **29b** = `FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md`, **AW** = `research/vorregistrierung/auswertung.py`, **REG** = `docs/VORREGISTRIERUNG_neuselektion.md`.

## 1. Ergebnis je Punkt

| Punkt | Fable setzt voraus (Fundstelle) | Befund (Fundstelle) | Urteil | A/B |
|---|---|---|---|---|
| R25 | Docstring trägt „unter dem Modus“ seit TB-117 Block D (27c:99, 182) | Zusatz seit `852f253` in AW:53–62 als „unter dem **Selektions**modus fuer JEDEN der neun Bots geprueft, sonst Abbruch mit 2“; Z. 51–52 unverändert | **passt** (Zeilen 53–62, nicht 51–52; Wortlaut „Selektionsmodus“) | gleich |
| R26 | `--bot` läuft unter dem Modus bis zum Bericht; J-7 hat den Modus nachgestellt (27c:185) | Echter Modus-Lauf mit `--bot` in TB-117 **E**: `docs/belege/TB-117/e_auswertung_modus.txt` Z. 1, 5: HEAD `852f253`, „modus_gut: rc 0“. AW seit `852f253` unverändert. J-7 ruft nur `herkunft_pruefen`, nicht `main()`. Laufwrapper (35.4) nicht gefunden | **passt in der Sache, Fundstelle falsch** (E statt J-7). An HEAD ohne Ausführung nicht neu messbar | B fand E, A nicht |
| R28 | Hat `snapshot.py` eine Probe gegen Register 18? Wenn nein: Handwerk (27c:191) | Keine: `probe_3u_datenstand_weicht_vom_anker_ab` (`shared/test_snapshot.py:1324ff`) prüft nur die Erzwingung des Ankers. Nebenbefund: drittes Literal `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97` | **Nein-Fall ⇒ Handwerk** | gleich |
| R33 | Vertrag führt Trade-Zahl je (Zelle, Falte) (29b:165) | `n_trades` in AW:39, Pflichtspalte AW:133 | **passt** | gleich |
| R36 | MtM-Drawdown in der Falte, Basis Faltenbeginn, Tage des Benchmarks (29b:166, 199) | `research/mtm_drawdown/mtm_kern.py:296–304` (Basis letzter Rastertag vor `von`), Raster Z. 135–139. Vertrag hat nur `kapital_drawdown_pct`; die zwei Spalten nach R36 fehlen (sollen neu kommen) | **passt** (`mtm_kern.py`) | gleich |
| R48 (d) | `mittlere_exposure` „bewertet wie die MtM-Reihe“ (29b:239) | In `mtm_kern.py` keine Exposure (nur `gebunden` zum Einstand, Z. 186–188). AW liest `mittlere_exposure` als Eingabe (AW:405). `exposure_kern.py` / `exposure_messung/auswertung.py:234` teilen `gebunden / kapital_start`, bewertet zum Einstand | **nicht vorhanden**, vorhandene Grössen bewerten zum Einstand | gleich |
| R41 | 15.4 (t3_supertrend 11,21 Tage): Kerzenzahl oder Zeitstempeldifferenz? (29b:214) | Zeitstempeldifferenz: `research/faltenplan_neun/embargo_neun.py:36–37, 236–238` | **weicht ab ⇒ Fables Abweichungsfall** (Neurechnung nach Zählregel, Tatsachennotiz 15.4). A rechnet nach der Kerzenregel P95 = 11,375 Tage ⇒ aufgerundet 12, Embargo 13 wie bisher (*erschlossen*, aus Register Z. 1415) | gleich |
| R48 (c) | ausgegebene Zelle im Fall Spitze (29b:238) | AW:554–556, Ausgabe immer der Plateau-Gewinner mit Markierung (AW:710–719) | **passt**. Randfall: kein Nicht-Spitzen-Punkt ⇒ (d) = False, von R48 (c) nicht geregelt | gleich |
| R48 (f) | Kante inkl. Zusatzstufen „kein“, „structural“ (29b:241) | Kante nach Position (AW:466). „kein“ immer letzte Stufe; „structural“ nach Weite einsortiert (`registerdaten.py:574–583`), bei `turtle_soup_crypto` Stufe 2 von 6 (REG:262) ⇒ keine Kante | **hängt an der Lesart**: passt bei „zählt als Stufe mit“, weicht ab bei „ist immer Kante“ | gleich |
| R48 (g) | **Summe** der Tagesrenditen (2a); empirisches 95. Perzentil über T − 1 Verschiebungen (29b:242) | `kennzahlen.py:199`: `np.prod(1.0 + e[index] * r) - 1.0`; Vergleichsseite `gesamtrendite_pct` Z. 92 ebenfalls `np.prod`. REG:1364/4091: „Die Falten-Rendite ist die **Summe** …“. T − 1 (Z. 197) und `np.percentile` (Z. 201) passen | **weicht ab: Register-Code-Widerspruch** (Produkt statt Summe) — selbst nachgemessen | gleich |
| R48 (i) | `pruefe_grenzsaetze.py` prüft die Satzfelder (29b:244) | Z. 100–148, `zahlen_im_satz(g.get("satz"))` | **passt** | gleich |
| R49 (b) | Funktion in `registerdaten.py`, die die Quantil-Stufen bildet; Eingabe Zeitraum/Zeitrahmen/Universum (29b:252) | `registerdaten.py:558–565` (`achse_werte`) **liest nur**; gebildet in `messgroessen.py::je_zeitrahmen` (Z. 169–219): Median über Symbole von `np.nanpercentile` nach 200 Balken Anlauf. Stufen fest `[1,2,5,10]`, `[50,60,70,80]`. Universum `config/sp500_top150.txt`, `config/top25_symbols.txt`. Zeitraum nur über `datenbereiche` (Aktien 1962-01-02–2026-09-01, Krypto 2021-09-01–2026-08-31), kein eigenes Feld | **gemessen; Ort weicht ab** | B genauer |
| R50 | Grenzsatz für jede der 34 Rastergrenzen; fasst `registerbericht.py` gleiche Sätze zusammen? (29b:260) | Jede Grenze hat `satz` über `_grenze` (`registerdaten.py:270`); Dubletten zusammengefasst (`registerbericht.py:111–120`), 20 Satzüberschriften im Register. Zellenname in `AW::zelle_id` (272–274), Cluster in `kennzahlen.py::cluster_anzahl`, Falten-Sharpe ist Eingabe | **Ob: ja/ja. Zahl 34 nicht gemessen** (Zählweise offen). Orte teils anders als Fable annimmt | B genauer |

## 2. Was daraus folgt (Vorschlag, nicht entschieden)

- **Vor E-2 an Fable (Verfahrensfragen nach dem Fable-Filter):** R48 (g) Produkt oder Summe — Register oder Code folgt? (25c (1): Register-Code-Widerspruch vor dem Tag klären). R48 (f) Lesart „eingeschlossen“. R48 (c) Randfall ohne Nicht-Spitzen-Punkt. Zusammen mit den TB-122-Befunden F1, F2, F4 (Block 4 Nr. 3) in **einer** Anfrage.
- **In E-2 ohne Fable, mit Tatsachennotiz:** R25 (Zeilen, Wortlaut), R26 (Fundstelle TB-117 E statt J-7), R41 (Zeitstempeldifferenz; Neurechnung nach 41.3 C2 als Mac-Messung), R49 (b), R50 (Orte).
- **Handwerk:** R28 Probe `snapshot.py` gegen Register 18 (pauschal frei, keine Sperrlistennähe).
- **Offen, braucht einen Lauf:** R26 an HEAD, R50 Zählung „34“ und Ausstiegskonvention der neun `backtest_*.py`. R48 (d) bleibt offen, bis es den Zellen-Erzeuger gibt.
- **Nebenbefund B, nicht beauftragt:** DSR-Einheiten (`sharpe_varianz_ueber_die_zellen` annualisiert, `deflated_sharpe` je Beobachtung, `kennzahlen.py:222–224`) — vor R50 prüfen.

## 3. In einfacher Sprache

Fable hatte für den nächsten Registerschritt aufgeschrieben, was im Code vorher nachgeschaut werden muss. Das ist jetzt gemacht. Das meiste stimmt. Zwei Sachen stimmen nicht: Der Code rechnet die Rendite im Zufallsvergleich anders zusammen, als das Register sagt, und eine Haltedauer wurde anders gezählt als vermutet. Das muss Fable entscheiden, bevor etwas ins Register kommt. Ein kleiner Test fehlt und kann einfach ergänzt werden.

## 4. Nachtrag 30.09.2026 — Berichtigung nach der Vorprüfung (Fable-Filter)

*Steuernder Chat. Grundlage: zwei unabhängige Helfer (Vorprüfung gegen das ganze Register), ein Gegenleser. Ergebnis ist `FABLE_ANFRAGE_2026-09-30a_vorgepruefte_fragen_e2.md`.*

- **R48 (g), eigener Fehler:** Abschnitt 1 nennt das einen „Register-Code-Widerspruch“. Das war zu stark.
  - 2a (REG:1364) definiert wörtlich nur die Rendite **je Falte**, und die rechnet heute kein Code (`netto_rendite_pct` ist Eingabe, AW:134).
  - Für die Rendite über die Selektionsfalten (7 (c)) und für 8.1 nennt das Register keine Rechenart; `kennzahlen.py` verkettet dort.
  - Einen Widerspruch schafft erst Fables R48 (g). Die Frage geht umformuliert an Fable (30a, Frage 2).
- **R48 (f):** ist im Register beantwortet (Kante nach Position, Grenzsätze REG:342, REG:350). Das geht ohne Fable in E-2.
- **R48 (c):** Die Helfer waren uneinig. Die Frage geht an Fable (30a, Frage 3).
- **Neu:** Der Vorlauf im Faltenplan ist bei sechs Bots achsenabhängig, nicht nur bei den drei aus TB-122 F2; `turtle_soup_*` sind nachgetragen. Das geht an Fable (30a, Frage 1).
- **F1, F3, Bauart des Laders:** Handwerk, Entscheidung beim Betreiber. **F4:** im Register beantwortet (Punkt 11 „und der Repo-Commit“, 5e, 37.1).
