# REGISTER-KOPIE Abschnitt 10 (von 0–56) — Register-Z. 971–1177 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 10. Die Sperrliste

> ⚠️ **Hinweis (36.2 und 36.6, Fable 22b/22c, TB-84, 22.09.2026):** Ab 36.2 prüft
> eine Sonde diese Liste — für jeden Punkt Pfad und Hash gegen diesen
> Registertext, mit drei Ausgängen (36.5). **Die maschinenlesbare Fassung ist
> Abbild, nicht Quelle**; das Abbild ist nach 36.6 eine **eigene, neue Datei**,
> einmalig geschrieben und selbst mit Hash im Register. `herkunft.py`
> `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das
> Abbild und werden es nicht; ihre Tatsachennotiz steht bei Fable aus
> (Anfrage 22c). Sonde und Abbild sind nicht gebaut (36.7).

> ⚠️ **Hinweis (37.1–37.5, Fable 22d/22g, TB-87, 22.09.2026):** Die
> Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN` steht jetzt in
> **37.4**: `EINGEFROREN` bildet die Abschnitt-0-Menge ab, nicht diese Liste;
> `SPERRLISTE_DATEIEN` liest niemand; `herkunft.py` wird nicht geöffnet. Sonde
> und Abbild sind seit TB-85 gebaut (`shared/sperrlistensonde.py`, Abbild
> `sperrliste_abbild_2026-09-22.json`, `6a1b732e…`); nach 37.1 meldet sie
> künftig je Bestandteil, nach 37.2 führt das Abbild Punkte und bestimmte Pfade.
> ⭐⭐ **Was ein Befund `1` bedeutet, hängt vom Tag ab (37.3):** Diese Liste gilt
> „ab dem signierten Tag"; vorher ist ein beauftragter Befund planmässig und
> wird mit Tatsachennotiz und neuem Abbild geschlossen, danach ist er ein
> Bruch nach 10.1. Punkte 7 und 9 nennen Werte ohne Ort (37.5).

Ab dem signierten Tag sind unveränderlich:

1. **Rastergrenzen und Grenzsätze** — `registerdaten.py`, Abschnitt 3 dieses
   Registers
2. **Faltengrenzen, Go-Live-Schnitt, Purge-Längen, Faltenlängen** —
   `faltenplan.py`, `ergebnisse/faltenplan.json`
   > ⚠️ **Tatsachennotiz (Abschnitt 30, 21.09.2026):** `ergebnisse/faltenplan.json`
   > (`0e54ac5c…`) bleibt gesperrt und unverändert. Er ist der **registrierte
   > historische Stand** eines früheren Verfahrensstands (Trainingsfenster,
   > Embargo) und **nicht** der Faltenplan nach 4a; der Lauf liest ihn nicht.
   > Kein Ersatz, keine Streichung — **die Sperrliste beweist, dass nichts
   > bewegt wurde.** Der Plan nach 4a ist Registertext; genau eine Abbild-Datei
   > kommt vor dem Tag mit Hash als **neuer Punkt** auf diese Liste.
   >
   > ⚠️ **Schreibregel (Abschnitt 36.1, Fable 22b, TB-84, 22.09.2026):** Kein
   > Programm im Repo schreibt an einen Pfad, der auf dieser Liste steht oder
   > für sie bestimmt ist; Erzeuger schreiben **einmalig** und brechen bei
   > vorhandener Zieldatei ab (Rückgabewert 1 nach 36.5), auch bei gleichem
   > Inhalt. `faltenplan.py main()` schreibt heute ohne Abfrage genau hierher
   > (Z. 372–374, nur gelesen) — Voreinstellung und Schreibsperre sind nach
   > 36.1 (4) zu ändern, **vor** Z. 336, Reihenfolge 36.3; Freigabe steht aus.
   > Hash `0e54ac5c…` am 22.09.2026 vor und nach TB-84 gemessen und gleich.
3. **Selektionsstatistik, Plateau-Regel, Spitzen-Schwelle** —
   `auswertung.py`, `registerdaten.SPITZEN_SCHWELLE`
4. **Drawdown-Bedingung, `DD_Toleranz` und die vorab berechneten
   Benchmark-Drawdowns** — `benchmark.py`,
   `ergebnisse/benchmark_drawdowns.json`, **einschliesslich der
   Interpolationsregel**
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
   > ⭐ **Form (ii) (38.4, Fable 22h, TB-89, 23.09.2026) — Form steht fest,
   > Vollzug steht aus:** Punkt 4 nennt künftig **beide** Dateien;
   > `ergebnisse/benchmark_drawdowns.json` (`a163c498…`) bleibt gesperrt und
   > unverändert als **registrierter historischer Stand** mit Tatsachennotiz,
   > wie Punkt 2 (30.3); `ergebnisse/benchmark_drawdowns_vt.json` ist die
   > Tabelle, die der Lauf liest. Nicht (i) (Streichen) und nicht (iii)
   > (ERSETZT-Marke). ⛔ **Der Punkttext oben ist NICHT geändert** — der Vollzug
   > ist Plan-Punkt 8 (37.3, kein Amendment, 38.3) und wartet auf zwei offene
   > Fragen an Fable (Anfrage 22i: „grün" als Fertigkriterium; welche Tabelle
   > für `t3_supertrend`).
   >
   > ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026).** Der Punkt nennt jetzt beide
   > Dateien. ⚠️ **Zwei Berichtigungen am Kasten darüber:** (1) Die Tabelle,
   > die der Lauf liest, ist **nicht** `benchmark_drawdowns_vt.json`, sondern
   > die Neurechnung `benchmark_drawdowns_2026-09-23_nach_wegA.json`
   > (`64fb2912…`) — so entschieden in **23b**, nachdem 23a die Bedingung
   > „die Tabelle folgt dem registrierten Faltenplan" gesetzt hatte; `_vt.json`
   > trägt bei `t3_supertrend` eine Falte `2018`, die der Plan seit TB-72 nicht
   > mehr hat. (2) Die zwei offenen Fragen aus 22i sind **beide beantwortet**:
   > das Fertigkriterium in **23a** (berichtigt in 39.1), die Tabelle in
   > **23a/23b** (vollzogen hier). Der Kasten oben ist als Zitat richtig und
   > bleibt unverändert; überholt ist an ihm nur der Dateiname und der Satz
   > „Vollzug steht aus".
5. **Abbruchkriterien und Kapitalregel** — `auswertung.py`
6. **Benchmark-Definitionen** — gleichgewichtete Tagesrenditen,
   point-in-time, `benchmark.py::bh_tagesrenditen`
7. **N-Buchführung und Clusterschwelle** —
   `registerdaten.N_HISTORISCH_JE_BOT`, `CLUSTER_SCHWELLE = 0,9`
   > ⚠️ **Ort registrierter Werte (37.5, Fable 22d, TB-87, 22.09.2026):**
   > `CLUSTER_SCHWELLE` steht hier ohne Ort, `N_HISTORISCH_JE_BOT` mit Modulnamen,
   > aber ohne Pfad und Hash (Sonde: „kein Dateipfad“). Nach 37.5 (1)–(3) bekommen
   > `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` **genau ein** Modul, das mit
   > Hash auf die Sperrliste kommt (Handwerk mit Freigabe, offen). Heute
   > gemessen (37.5 (4)): `registerdaten.py:99` `CLUSTER_SCHWELLE = 0.90`,
   > `registerdaten.py:115` `N_HISTORISCH_JE_BOT` — keiner davon steht mit Hash
   > auf dieser Liste; bis zur Umsetzung **ungeschützt**. Die Werte ändern sich
   > nicht.
   >
   > ⭐ **Der Ort steht schon (38.5, Fable 22h, TB-89, 23.09.2026):**
   > `registerdaten.py` ist ein Modul, ein Ort, und steht als Punkt 1 auf der
   > Sperrliste — **hier ist nichts zu verschieben.** Punkt 7 bekommt den Ort
   > nachgetragen (`registerdaten.py`, `CLUSTER_SCHWELLE` und
   > `N_HISTORISCH_JE_BOT`); die Sonde prüft Datei plus Wert. Fables Kandidat
   > aus 22d war für Punkt 7 keiner. Der Nachtrag selbst ist Handwerk (TB-90).
8. **Universumsdateien und point-in-time-Regel** — `config/top25_symbols.txt`,
   `config/sp500_top150.txt`, vier Jahre Vorlauf je Symbol
   > ⚠️ Der Halbsatz „vier Jahre Vorlauf je Symbol" ist **ersetzt** (Abschnitt 15,
   > Registertext 3). Die beiden Universumsdateien selbst bleiben unverändert auf
   > der Sperrliste, jetzt mit Hash im Nachtrag.
9. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und
   `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum
   Schlusskurs des Bestätigungsbalkens
   > ⚠️ **Ort registrierter Werte (37.5, Fable 22d, TB-87, 22.09.2026):** Dieser
   > Punkt nennt Werte, aber keinen Ort — *„Ein Sperrlistenpunkt, der einen Wert
   > nennt und keinen Ort, sperrt nichts — er legt fest."* Nach 37.5 (1)–(3)
   > bekommt er **genau ein** Modul mit `TRADING_FEE_PCT` und `SLIPPAGE_PCT`,
   > das mit Hash auf die Sperrliste kommt (Handwerk mit Freigabe, offen).
   > Heute gemessen (37.5 (4)): je eine Kopie in neun `forward_test.py` und
   > neun `backtest_*.py`; `messgroessen.py:59` `SLIPPAGE_PCT`, die Gebühr dort
   > als `GEBUEHR_PCT` (Z. 58) — keinen davon nennt dieser Text; bis zur
   > Umsetzung **ungeschützt**. Die Werte `0,1` / `0,05` ändern sich nicht.
   >
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
   > nachgemessen am Stand `da251da`, gleich.
10. **Zuteilungskaskade inklusive Seed** — `shared/zuteilung.py`,
    `SEED = 20260913`
11. **Commit-Hashes von Simulation, Erkennung, Optimierern und
    Auswertungsskript** — `herkunft.py::register()` und der Repo-Commit
12. **Hash des Datenstands** — `herkunft.py::datenstand()`
13. **Die Liste der berichteten Kennzahlen und die Regel, dass alle
    berichtet werden, auch die unangenehmen** — Abschnitt 8
14. **Die Reihenfolge Selektion → Bestätigungsperiode → Bericht** — im
    Kopftext von `auswertung.py` als Ablauf festgeschrieben

Zusätzlich gilt: **Der Lauf darf nicht beginnen, bevor die beiden Bug-Fixes
aus Abschnitt 11 eingebaut sind.**

*Tatsache zu Punkt 12 (15.09.2026, TB-34):* Der Datenstand-Hash hat sich
**vor** jedem Selektionslauf geändert — durch den nativen Neuaufbau der 72
Krypto-Kursdateien (`shared/kursdaten_neuaufbau.py`, Stand 2026-09-15
09:51:31 UTC, Sicherung `data_sicherung/2026-09-15_115131`). Vorher
`6258cbc38872f9d6dd2b0315e9ea15a68148b133e97996cf5dbb18c82758c1f0`, nachher
`97498f14527651a28323c1f273be24d2252595840b1b57364d263d7ff87eef1c` (je 242
Dateien). Das ist **kein Amendment**: es gab keinen Lauf, dessen Ergebnisse
davon berührt wären; genau deshalb kam TB-34 vor TB-30b. Die Aktiendateien
sind unverändert. Der daraus folgende Krypto-Faltenplan (5.3) ist gerechnet
(`research/krypto_historie/daten/faltenplan_nach_tb34.json`), aber **nicht**
eingetragen — Lesart von „je Symbol" und Eintrag bleiben Betreiberentscheidung.

*Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf):* Der oben
genannte Stand `97498f14…` bestand nur kurz. Anschliessend wurden die **19
verwaisten `*_15m.csv`** aus `data/` entfernt — Reste eines verworfenen
15-Minuten-Versuchs, von **keinem** Programm gelesen (geprüft über den gesamten
Python-Quelltext; die einzigen beiden Fundstellen sind `shared/zeitabdeckung.py`
und ihr Test, und dort steht `_15m` als **Beispiel für einen nicht geführten
Zeitrahmen**). Beides zusammen liegt in Commit `90e3cbd`.

**Der Datenstand, der für den Selektionslauf gilt, ist damit:**
`d9449faf51bffaaa…` bei **223** Kursdateien (223 = 72 Krypto + 150 Aktien +
`XAUTUSDT_1h`), erfasst mit `research/vorregistrierung/herkunft.py`.

*Nachtrag zu derselben Tatsachennotiz (18.09.2026, TB-48 — angehängt, nichts
entfernt):* ⚠️ **Ab Registertext 5a (neu, Abschnitt 17.1) bezeichnet
`d9449faf…` den Kursdatenteil des Snapshots — den Datenstand-Hash —, nicht den
Snapshot selbst; der Snapshot-Hash ist ein eigener Wert.** **Der hier
festgehaltene Wert bleibt in jedem Wort gültig**: er misst den Bestand, und den
misst er weiterhin. Benannt wird nur sein Referent. Beide Werte nebeneinander
in **17.9**.

*Warum beides in einem Zug geschah:* Die 19 Dateien waren im Hash mitgezählt.
Sie später zu entfernen hätte einen **zweiten** Hash-Wechsel erzeugt — und wäre
er nach dem Selektionslauf erfolgt, wäre er kein Tatsachenvermerk mehr gewesen,
sondern ein Bruch der Sperrliste. Es gibt daher genau **einen** Übergang:
`6258cbc3…` (242 Dateien) → `d9449faf…` (223 Dateien), vollzogen vor jedem Lauf.

### 10.1 Die Amendment-Regel

> Ein **Bug-Fix ist ein Amendment**: dokumentiert, **der Lauf beginnt von
> vorn**, und die Ergebnisse davor werden **nicht** neben die danach gelegt.
> *Wer Vorher und Nachher vergleicht, hat wieder eine Wahl.*
>
> **Erlaubt sind nur** Laufzeit-Optimierungen mit **bitidentischen**
> Ergebnissen — nachzuweisen über `shared/determinismus.py` und einen
> Stichproben-Hash-Vergleich.

Ein Amendment wird im append-only-Protokoll
(`ergebnisse/herkunft_protokoll.jsonl`) mit eigenem Anlass eingetragen. Der
Register-Hash ändert sich dabei zwangsläufig, und genau daran ist im
Protokoll zu sehen, dass zwei Läufe **nicht** unter derselben
Vorregistrierung liefen.

> ⭐⭐ **Tatsachennotiz (38.3, Fable 22h, TB-89, 23.09.2026):** Diese Regel
> betrifft Bug-Fixes **nach** Beginn des Laufs; das Protokoll ist der Ort der
> **Läufe** und ihrer Amendments, und vor dem ersten Lauf gibt es nichts, was
> dort stünde. Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist daher **kein
> Amendment nach 10.1** und erzeugt **keinen Protokolleintrag**, sondern ist
> eine beauftragte Änderung nach 37.3. Das Protokoll entsteht mit dem Erzeuger
> und beginnt mit dem Stand des Tags. Wortlaut und Grund in **38.3**.

---

