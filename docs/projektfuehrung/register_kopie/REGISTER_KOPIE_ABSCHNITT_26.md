# REGISTER-KOPIE Abschnitt 26 (von 0–50) — Register-Z. 4770–5093 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 26. Präzisierung zu Registertext 4a, Bedingung (i) — der Datenhorizont ist ein absolutes Datum je Bot, nicht je Symbol (TB-77, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— die Neufassung 4a / 21.3 (b) in 25.3 bleibt stehen (dort seit heute mit der
Marke *„(i) PRÄZISIERT durch Abschnitt 26"*), Registertext 3 (c) in 15.5 bleibt
stehen (Marke *„ERGÄNZT durch Abschnitt 26, 26.4"*), die Tatsachennotiz 21.4
bleibt unverändert gültig. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21, 23, 24 und 25.

**Anlass:** Fables fünfte Antwort vom 20.09.2026
(`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, Abschnitt (3)) hatte *„im
Datenhorizont"* als `asof` minus `RECENT_YEARS_ONLY` präzisiert und einen
dritten, ungefragten Befund danebengelegt: die Bots rechnen das Fenster **je
Symbol**, der Faltenplan **je Markt**. Abschnitt 25 hat beides ausdrücklich
offen gelassen (25.3, Tatsachennotiz Zeile „Bedingung (i)"; 25.5: *„Bedingung
(i) nicht präzisiert — TB-74"*). Die Anfrage
`FABLE_ANFRAGE_2026-09-21a_horizont_und_grenzfall.md` (Teil 1, Fragen (1) und
(2)) hat die Entscheidung erbeten; Fable hat sie am 21.09.2026 getroffen.

⚠️ **Herkunft des Wortlauts, nicht geglättet:** Fables Antwort vom 21.09. liegt
**nicht im Repo** — gemessen 21.09.2026 (`find` über das Repo: 0 Treffer für
`FABLE_ANTWORT_2026-09-21a*`; die Anfrage hatte um Ablage in der Projektablage
gebeten, `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` Z. 9: *„sie kam als Datei
zurück"*). Der Wortlaut in 26.1 und 26.2 ist **zeichengleich aus
`docs/auftraege/MAC_TB-77_horizont_je_bot.md`, Abschnitt 0**, übernommen, das
ihn aus der Antwort zitiert. Das ist der einzige Träger im Repo; die Ablage der
Antwort selbst ist eine offene Bringschuld des steuernden Chats (26.6).

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Präzisierung,
Quelle des Grundes ist die Regel** — Registertext 4a (*„im registrierten
Datenhorizont"*) und Registertext 5e (der Lese-Audit, 17.4: kein Lesezugriff
ausserhalb des registrierten Horizonts). Eine Wirkung auf eine Zahl ist **nicht
bekannt und nicht gemessen** (26.6): es hat kein Selektionslauf stattgefunden,
kein Parametersatz ist bewertet, kein Ergebnis erzeugt. ⛔ **Dieser Abschnitt
rechnet nicht und fasst keinen Code an** — die vier `multi_symbol_optimise.py`
und `auswertung.py` sind unberührt (Nachweis: `git diff --numstat` in
`docs/ERGEBNIS_TB-77_horizont_je_bot.md`).

---

### 26.1 Der Befund — das Fenster je Symbol erzeugt Einstiege ausserhalb aller Falten, und sie laufen durch den Kapitalpfad

**Was der Code tut, gemessen 21.09.2026 (Stand `2e9cdf9`):**

| | Fundstelle | Wortlaut |
|---|---|---|
| Die Konstante | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:54`, `rsi2_mean_reversion/…:52`, `turtle_soup_stocks/…:46`, `volatility_breakout/…:49` | `RECENT_YEARS_ONLY = 10`, bei allen vier Aktien-Bots, in Jahren (`pd.DateOffset(years=…)`). Die fünf Krypto-Bots haben keine |
| Der Bezug | dieselben Dateien, Z. 93 / 93 / 81 / 88 | `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` — relativ zum **letzten Kurs der Datei**, nicht zum Laufdatum (Datenuhr) |
| ⚠️ **Je Symbol** | dieselben Zeilen, **innerhalb der Ladeschleife** `for symbol in SYMBOLS`; abgelegt je Symbol (`data[symbol] = (df_ind, entry_cutoff)`, Z. 96 / 83 / 91; `elliott_wave_stocks` kappt in Z. 94 die Kursreihe des Symbols selbst) | Jedes Symbol bekommt sein eigenes Fenster, das an **seinem** letzten Kurstag hängt |
| Der Plan | `research/faltenplan_neun/faltenplan_neun.py::fensteranker`, Z. 271, Docstring Z. 272–278 | *„Genommen wird der SPAETESTE letzte Kurstag des Marktes, damit alle Symbole desselben Bots auf demselben Fenster liegen."* — **je Markt** |

**Das ist nicht dasselbe.** Ein Symbol, dessen Datei früher endet — delistet,
Datenlücke, stehengebliebene Datei —, bekommt beim Bot ein früheres Fenster und
liefert Trades aus einem Zeitraum, den der Plan für ausgeschlossen hält (so
gestellt in `FABLE_ANFRAGE_2026-09-21a…`, Teil 1 (c)).

⭐⭐ **Fables Begründung, und sie ist der eigentliche Befund — wörtlich** (aus
seiner Antwort vom 21.09.2026, zitiert nach `MAC_TB-77_horizont_je_bot.md`,
Abschnitt 0): Ein Symbol mit früherem Fenster erzeugt Trades aus Jahren **vor
der ersten Falte**. Die tauchen in keiner Falte auf —

> *„aber sie laufen durch den Kapitalpfad, belegen Plätze, verändern das
> Kapital, mit dem die erste Falte beginnt. Das ist ein Lesezugriff auf Zeiten
> ausserhalb des registrierten Horizonts, nur nicht über eine Datei, sondern
> über ein Fenster. Der Lese-Audit (5e) sieht ihn nicht, weil die Datei im
> Manifest steht."*

Deshalb ist die Frage *„je Bot oder je Symbol"* keine Handwerksfrage: Ein
Fenster je Symbol ist eine Lücke in Registertext 5e, die keine Datei und kein
Hash sichtbar macht — der Kapitalpfad (Registertext 1a) beginnt die erste
Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt.

---

### 26.2 Der Registertext — Fables Präzisierung vom 21.09.2026, zeichengleich

**Ersetzt seine Fassung vom 20.09.2026** (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`,
Abschnitt (3): *„4a, Präzisierung. ‚Im Datenhorizont' heisst: ab dem
Horizontbeginn des Bots, berechnet als registriertes `asof` (5a) minus
`RECENT_YEARS_ONLY` des Bots; das Ergebnis steht je Bot als absolutes Datum in
der Tatsachennotiz zu 4d. Der Vorlauf wird gegen dieses Datum gerechnet, nicht
gegen den ersten Kurs im Bestand."*). ⭐ **Gemessen 21.09.2026: diese Fassung
vom 20.09. ist nie in einen Registertext übernommen worden** — `grep -c` im
Register: `Horizontbeginn` **0**, `4a, Präzisierung` **0**; 25.3 und 25.5
verweisen sie ausdrücklich an TB-74. Es gibt darum im Register keine Stelle,
die als ERSETZT zu markieren wäre; ersetzt wird ein Wortlaut, der nur in
Fables Antwortdatei steht. Präzisiert wird die Neufassung in **25.3**,
Bedingung (i) *„im registrierten Datenhorizont des Bots"*, die stehen bleibt.

> **4a, Präzisierung (ersetzt die Fassung vom 20.09.).** Der Datenhorizont eines
> Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus
> `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont
> (Krypto). Das Datum steht je Bot in der Tatsachennotiz zu 4d. Es gilt für alle
> Symbole des Bots gleich; ein Symbol trägt vor dem Horizontbeginn keinen
> Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet. Das
> Ende der Kursdatei eines Symbols bestimmt nach 3b (b), an welchen Tagen es
> handelbar ist — nie sein Fenster.

**Was der Text festlegt, in drei Sätzen:** Das Fenster ist eine Zahl **je
Bot**, und der Code muss nachgeben, nicht der Plan (Antwort auf Frage (1) der
Anfrage). Es hängt an `asof` aus Registertext 5a — dem Bezugsdatum, das *„aus
dem Register, nie aus der Uhr"* kommt (17.1) —, nicht am letzten Kurs einer
Datei. Und das Ende einer Kursdatei behält genau eine Rolle: es entscheidet
nach 3b (b), an welchen Tagen das Symbol handelbar ist.

⚠️ **Was der Text braucht und was es heute nicht gibt:** `asof`. Registertext
5a sagt seit TB-48, woher es kommt; **es steht nirgends als Wert** — gemessen
21.09.2026 in allen `.py` (8 Zeilen, alle pandas `merge_asof`), allen `.json`
(1 Eintrag, derselbe Bezeichner), im Register (3 Zeilen, Formel und Herkunft),
in `ergebnisse/`, im Snapshot-Manifest (15 Schlüssel, keiner `asof`), in
`registerdaten.py` und in `docs/` (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 2). *Ein Registertext, der auf einen Wert zeigt, den es nicht gibt,
ist kein Fehler — solange er sagt, dass es ihn nicht gibt.* Das tut 26.3.

---

### 26.3 Tatsachennotiz zu 4d — der Horizontbeginn je Bot: ⚠️ Platzhalter, weil `asof` nicht gesetzt ist

Nach 26.2 steht das Datum je Bot in der Tatsachennotiz zu 4d (21.4). **Es kann
heute nicht eingetragen werden**, weil der Minuend fehlt. Nach dem Muster von
23.3 (Fassung TB-66) steht hier ein sichtbarer Platzhalter und **keine
erfundene Zahl**:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `turtle_soup_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `volatility_breakout` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |

Die Konstante je Bot ist aus dem Code **gelesen** (Fundstellen 26.1), nicht
registriert; ob sie als registrierte Grösse in `registerdaten.py` gehört, ist
Teil von 26.6.

⚠️ **Abgegrenzt, damit es niemand für den Wert hält:** 15.6, Punkt 3, nennt
seit dem 15.09.2026 *„gemessen vom letzten Kurstag (2026-09-01) zurück auf
2016-09-01 — so rechnen die vier Aktien-Bots selbst."* Das ist die **Datenuhr**
(letzter Kurs im damaligen Bestand), also genau der Bezug, den 26.2 ablöst —
**kein `asof`** und kein Horizontbeginn im Sinne dieses Abschnitts. Der Wert
wandert nicht in die Tabelle. Wann und wodurch `asof` gesetzt wird, ist als
Frage (1) in `FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4, an Fable
gestellt (Lesart des steuernden Chats dort: *„mit dem Snapshot und dem
signierten Tag zugleich"* — **nicht entschieden, hier nicht vorweggenommen**).

**Was der Platzhalter für den Faltenplan bedeutet:** Bedingung (i) wird bis
zum Eintrag *„wie bisher"* gerechnet (25.3, Tatsachennotiz), also mit dem
Fenster aus `faltenplan_neun.fensteranker` (je Markt, Datenuhr). Die
Faltenliste 21.4 ist damit **vorläufig in (i)** und **endgültig in (ii)**; nach
15.6 Punkt 3 *„bindet das Fenster die Faltenliste nicht"* — ob das mit einem
registrierten `asof` so bleibt, ist erst mit dem Wert prüfbar.

---

### 26.4 Ergänzung zu Registertext 3 (c) — die Reichweite des Survivorship-Vorbehalts

Registertext 3 (c) (15.5) trägt den Vorbehalt *„Beide sind
survivorship-behaftet … Grösse unbekannt"*. Er bleibt zeichengleich stehen und
wird ergänzt:

> **3 (c), Ergänzung (TB-77, 21.09.2026):** Der Survivorship-Vorbehalt gilt für
> die Jahre im Horizont; dass der Horizont zehn Jahre umfasst, begrenzt die
> Reichweite des Vorbehalts, ändert ihn nicht.

*Warum die Ergänzung nötig ist:* `RECENT_YEARS_ONLY` steht im Code als
Gegenmassnahme gegen den Survivorship-Bias (`multi_symbol_optimise.py:52`
und `:49`: *„reduziert Survivorship Bias"*; `UEBERGABEPROTOKOLL.md` Z. 170).
Ein Leser könnte den Horizont darum für eine **Milderung** des Vorbehalts
halten. Er ist keine: Innerhalb der zehn Jahre ist das Universum dieselbe
heutige Liste, mit derselben erwarteten Richtung (*„Bevorzugung von Sätzen mit
weiten oder fehlenden Stops und langen Zeitbremsen"*). Der Horizont sagt nur,
**für welche Jahre** der Vorbehalt ausgesprochen wird.

---

### 26.5 Tatsachennotiz zur Herkunft — alle bisherigen Ergebnisdateien der vier Aktien-Bots sind mit Fenstern je Symbol gerechnet

Gemessen 21.09.2026 (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
letzter Abschnitt): `results/<bot>/multi_symbol_optimisation_results.csv` hat
bei jedem der vier Aktien-Bots genau **einen** Commit und ist seitdem
unverändert; im selben Commit steht der Optimierer bereits mit
`df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` innerhalb der
Ladeschleife, und `git log -S` kennt keinen älteren Stand des Ausdrucks:

| Bot | Ergebnisdatei (Commit) | Optimierer je Symbol seit |
|---|---|---|
| `elliott_wave_stocks` | `0f6491b`, 02.09.2026 | `0f6491b` |
| `rsi2_mean_reversion` | `f56c6d2`, 03.09.2026 | `f56c6d2` |
| `turtle_soup_stocks` | `88b9050`, 04.09.2026 | `88b9050` |
| `volatility_breakout` | `b603861`, 03.09.2026 | `b603861` |

**Folge:** Jede dieser Tabellen ist mit einem Fenster **je Symbol** an dessen
letztem Kurstag gerechnet — nicht mit dem Horizont aus 26.2. Das ist **ein
Grund mehr**, warum sie mit den Zahlen des Laufs nicht vergleichbar sind; die
anderen Gründe stehen in Registertext 7 (Backtester-Prüfung, 16.5) und in der
Warnung zu den Papierpfaden vor dem Umstellungstag (`CLAUDE.md`, TB-38). Sie
bleiben liegen, wo sie liegen, und werden nicht neu gerechnet (26.6). *Nicht
gemessen:* ob weitere, abgeleitete Ergebnisse unter `research/` dieselben
Loader importiert haben; wo sie es taten, gilt dasselbe.

---

### 26.6 Was folgen muss — und hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`asof` setzen.** Wann und wodurch, ist Fables Frage (1) im neuen Chat; die Lesart *„mit Snapshot und Tag zugleich"* ist nicht entschieden. Bis dahin bleibt 26.3 ein Platzhalter | Betreiber / Fable, vor dem Tag |
| ⛔ | **Tatsachennotiz 4d füllen:** vier Daten in 26.3, je `asof` minus zehn Jahre, mit Fundstelle des `asof`-Wertes. Danach prüfen, ob das Fenster die Faltenliste 21.4 in (i) weiterhin nicht bindet | Registernachtrag, sobald `asof` steht |
| ⛔ | **Die vier Optimierer:** `entry_cutoff` **einmal je Bot aus dem Register** statt je Symbol aus `df["open_time"].max()` (Fundstellen 26.1). Sie brauchen denselben Wert; ohne `asof` gibt es nichts einzutragen | **TB-30b** (Umstellung des Laufcodes) |
| ⛔ | **Die Wache** *„kein Einstieg eines Bots liegt vor dessen Horizontbeginn"* — Fable schlägt sie *„billig, in den Auswerter"* vor. `auswertung.py` ist **eingefroren** (Abschnitt 0, Z. 31; 15.8 Nr. 3; Sperrliste 10 Nr. 5); ein eingefrorenes Skript, das einmal geöffnet wird, ist nicht mehr eingefroren. **Samt Mutationsprobe:** Fenster je Symbol wieder einschalten → die Wache muss rot werden | **TB-30b**, mit den Optimierern |
| ⛔ | **Fables Antwort vom 21.09. ablegen** (`FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`) — sie liegt in keinem Träger; bis dahin trägt Abschnitt 0 des Auftrags den Wortlaut | steuernder Chat |
| ⚠️ | **`RECENT_YEARS_ONLY` als registrierte Grösse** (`registerdaten.py`) statt als Codekonstante, die aus vier Dateien gelesen wird — Fable nennt sie *„registrierte Konstante"* (20.09., Abschnitt (3)); eingetragen ist sie nur als Tatsachennotiz (15.6 Punkt 3, 26.3). Ob das eine Registeränderung oder eine Codekopie ist, entscheidet der Betreiber (vgl. `T56b.6`: keine Konstantenkopien) | Entscheidungsvorlage, nicht vollzogen |
| ⚠️ | **Nicht gemessen:** ob und wie viele Einstiege in den bisherigen Ergebnisdateien vor einem Horizontbeginn liegen. Ohne `asof` gibt es die Grenze nicht, gegen die man zählen könnte; und die Zahl wäre eine Aussage über Ergebnisse, die mit dem Lauf ohnehin nicht vergleichbar sind (26.5) | — |

⛔ **Nicht getan:** kein Bot-Code, kein `auswertung.py` (auch nicht der
Docstring), kein `registerdaten.py`, keine Sperrlisten-Datei
(`benchmark_drawdowns.json` `a163c498…`, `faltenplan.json` `0e54ac5c…`
byteweise unverändert), kein Tag, kein Lauf.

---

### 26.7 Der Grenzfall — was gilt, wenn für einen Bot kein Parametersatz besteht: die Kette (b) → Festlegung 11 → Registertext 6 (b) → Schatten

**Das ist ein Verweis, keine Berichtigung.** Fables Teil 2 vom 21.09.2026
(Antwort auf `FABLE_ANFRAGE_2026-09-21a…`, Teil 2, Fragen (3) und (4))
entscheidet den Fall, den die Anfrage für ungeregelt hielt — und die
Entscheidung steht bereits im Register, an vier Stellen, die bisher niemand als
Kette gelesen hat. **Jede Stelle nachgemessen 21.09.2026 (Stand `2e9cdf9`):**

| Glied | Fundstelle | Wortlaut |
|---|---|---|
| **1. Der Fall ist ein Abbruchkriterium** | Abschnitt 7, **(b)**, Z. 686; Präzisierung Z. 692–694 | *„**(b)** Kein Parametersatz erfüllt die Drawdown-Bedingung in allen Falten"* — *„Gewinnen kann nur ein zulässiger Punkt. Ist keiner zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über alle Zellen, ausdrücklich mit der Markierung ‚nicht zulässig'."* |
| **2. Bleibt/Geht läuft über die Abbruchkriterien** | Abschnitt 1, **Festlegung 11** (`registerdaten.FESTLEGUNGEN[11]`) | *„DSR ist Bericht, nicht Tor — Bleibt-Geht läuft über die Abbruchkriterien."* Ein Bot, der (b) erfüllt, **bleibt nicht** |
| **3. Die Stufe** | 16.4, **Registertext 6, Buchstabe (b)** | *„jeder, der eines erfüllt, auf **Schatten** — sein Budgetanteil hält die statische Benchmark-Position in Höhe seines mittleren Exposures. Die Zuweisung ist Ergebnis des eingefrorenen Skripts, keine Lesung."* |
| **4. Was Schatten heisst, und der Weg zurück** | Registertext 6 (a) und (d), 16.4; Abschnitt 7.1 | Schatten: *„läuft, kein Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf"* — mit seinen heutigen Parametern. Kapital: *„statische Benchmark-Position in Höhe des mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden."* Rückkehr: *„nur über einen neuen registrierten Lauf"* (6 (d)); *„Kein ‚vorerst behalten'"* (7.1) |
| **5. Das Ergebnis ist zulässig, auch bei mehreren oder allen** | **Festlegung 12** (wörtlich, Abschnitt 1) und 7.1 | *„Es kann sein, dass kein einziger Bot die Schwelle erreicht."* — *„Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu ändern."* |

**Die Kette ist im eingefrorenen Skript bereits Code:** `auswertung.py::kapitalregel`
(Z. 554–576) gibt `kapitalregel`, `schattenregel`, `schwellenregel` und
`zulaessiges_ergebnis` (`rd.FESTLEGUNGEN[12][1]`) am Ende jeder Bleibt-Geht-Liste
aus; `test_vorregistrierung.py` Teil D prüft
`b_kein_satz_besteht_die_drawdown_bedingung` (Z. 288, 348–350). **Fällt ein
Bot nach (b), gibt es nach dem Lauf keine Entscheidung, nur eine Lektüre**
(Abschnitt 0).

⚠️ **Zwei Aktenzeichen aus Fables Antwort, nachgemessen und nicht übernommen**
(`registerdaten.FESTLEGUNGEN`, `docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 4): Fable nannte *„Festlegung 10"* für Bleibt/Geht über die
Abbruchkriterien — das ist **11** (10 ist die DSR-Basis, N = 653); und
*„Festlegung 11"* für „mehrere oder alle" — das ist **12**. Sein Vorbehalt
*„fehlt (b) im Registertext"* ist gegenstandslos: (b) steht in Abschnitt 7,
wörtlich.

⚠️ **Quelle, nicht geglättet:** Fable verweist für Teil 2 auf ein Dokument
`FABLE_ANTWORT_2026-09-20a_grenzfall`. **Es existiert nicht** — weder im Repo
(gemessen 21.09.2026, 13:50 durch den steuernden Chat; hier nachgemessen:
`find` 0 Treffer für `*grenzfall*` ausser der Anfrage vom 21.09.) noch in der
Projektablage (`FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4 (3)).
Vom 20.09. liegen vier Antworten vor: Kalender, Kapitalpfad, MtM-Messung,
Konjunktion. **Quelle dieses Abschnitts ist allein seine Kurzfassung vom
21.09.2026**, wie sie der Auftrag (`MAC_TB-77_horizont_je_bot.md`, Schritt 3)
und die Übergabe an den neuen Chat (`FABLE_UEBERGABE…`, Abschnitt 3 (e))
wiedergeben — das fehlende Dokument wird nicht zitiert.

⭐ **Und die Antwort auf Frage (4) der Anfrage — ob vorab gemessen werden darf,
wie viele Sätze die härtere Bedingung kostet:** *nein.* Fable, nach
`FABLE_UEBERGABE…` Abschnitt 3 (e): *„Die Zahl der zulässigen Sätze je Bot ist
der Ausgang des Laufs — die erste Hälfte des Laufs selbst."* Das ist dieselbe
Linie wie 24.3 (*„vor jeder Messung"*), nur eine Stufe strenger: dort war die
Zahl folgenlos, hier wäre sie eine Aussage über den Ausgang. **Es wird nicht
gemessen.** Diese Sitzung hat es nicht getan (26.6, letzte Zeile).

---

### In einfacher Sprache

**Was entschieden ist:** Die „letzten zehn Jahre", auf die ein Aktien-Bot bei
der Auswahl schaut, gelten künftig für den ganzen Bot — nicht für jedes
Wertpapier einzeln. Heute rechnet jeder Bot das Fenster für jedes Wertpapier
von dessen letztem Kurs aus zurück. Endet die Kursdatei eines Wertpapiers
früher, liegt sein Fenster früher — und der Bot handelt darin in Jahren, die
offiziell gar nicht ausgewertet werden. Diese Geschäfte tauchen in keiner
Jahresfalte auf, aber sie verändern still das Kapital, mit dem das erste
ausgewertete Jahr beginnt. Der Lesewächter merkt das nicht, weil die Datei
selbst erlaubt ist.

**Was dabei auffiel:** Die neue Regel braucht ein Stichtagsdatum (`asof`), von
dem aus die zehn Jahre zurückgerechnet werden. Das Regelwerk sagt seit dem
18.09., dass es dieses Datum aus dem Register bekommt — **aber es steht
nirgends.** Gesucht wurde im ganzen Code, in allen Ergebnisdateien, im
Datenschnappschuss und im Register selbst. Und die Wache, die Fable
vorschlägt, gehört in eine Datei, die eingefroren ist und bis zum Umbau
(TB-30b) nicht angefasst wird.

**Was dieser Abschnitt deshalb tut:** Er schreibt die Regel wörtlich auf und
setzt dort, wo das Datum stehen müsste, einen sichtbaren Platzhalter — statt
eine Zahl zu erfinden. Das Datum, das dem Wert am nächsten kommt (2016-09-01
aus dem Jahr 2026 zurück), steht ausdrücklich daneben als das, was es ist: der
alte Bezug, nicht der neue. Ausserdem hält er fest, dass alle bisherigen
Auswahltabellen der vier Aktien-Bots noch mit dem alten Fenster je Wertpapier
gerechnet sind — ein Grund mehr, sie nicht mit dem Lauf zu vergleichen.

**Und der Grenzfall:** Was passiert, wenn für einen Bot am Ende gar keine
Einstellung die Verlustgrenze in allen Jahren einhält? Die Antwort stand
schon da, verteilt auf vier Stellen: Das ist Abbruchkriterium (b); der Bot
bleibt nicht; er läuft mit seinen heutigen Einstellungen als Schatten ohne
Geld weiter; sein Geld geht in eine feste Marktposition; zurück kommt er nur
über einen neuen, vorher registrierten Lauf. Und vorher nachzuzählen, wie
viele Einstellungen die härtere Grenze kostet, ist verboten — die Zahl verriete
den Ausgang.

*Nachgetragen in TB-77, 21.09.2026. Präzisierung mit Registertext, Platzhalter
und Verweis: sie nennt den Befund mit seinen Fundstellen, den Registertext mit
seiner Herkunft, den fehlenden Wert als fehlend, die Ergänzung zu 3 (c), die
Herkunft der bisherigen Ergebnisse, die Kette des Grenzfalls und das, was
nicht getan wird — und entfernt nichts.*

---

