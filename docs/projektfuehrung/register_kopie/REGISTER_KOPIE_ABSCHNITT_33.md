# REGISTER-KOPIE Abschnitt 33 (von 0–50) — Register-Z. 5869–6080 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 33. Der Faltenplan als Registertext, und was die Abbild-Datei tragen muss (Fable 21k, 21.09.2026)

⭐ **Zwei Dinge in einem Abschnitt:** der Faltenplan nach 4a als Registertext
(Fables 30.2 (2)) und die **Berichtigung** seines Kriteriums aus 30.2 (3), das
er selbst zurückgenommen hat.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md`,
zeichengleich. Anlass: `FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md`.

### 33.1 Berichtigung zu 30.2 (3) — ein Symptom war zum Kriterium geworden

⚠️ **Der Satz in 30.2 (3)** — *„Trägt eine Datei Felder, die 4a nicht kennt
(Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild"* — **ist ERSETZT.**
Er bleibt dort zeichengleich stehen.

**Der Anlass, gemessen 21.09.2026:** Alle drei vorhandenen Pläne tragen
`training_bis_ausschliesslich` (60 verschiedene Werte) und `embargo_nach_falten`
(29 verschiedene) — der gesperrte `faltenplan.json`, `faltenplan_tb72.json`
**und** der am selben Abend erzeugte `faltenplan_tb80.json`. ⭐ **Und: kein
Laufcode liest sie** — `training_bis_ausschliesslich` hat genau einen Treffer im
Repo, `faltenplan.py:306`, und das ist die Stelle, die es **schreibt**.

⭐⭐ **Fables Grund, warum „die Felder wirken ja nicht" trotzdem kein Kriterium
ist — wörtlich:**

> *„Das ist eine Aussage über Code, der **noch nicht eingefroren ist** (TB-30b
> steht aus). Ein Registertext, der davon abhängt, was der Code heute nicht
> liest, wandert mit dem Code — dieselbe Klasse wie die Datenuhr. Und: Ein
> Abbild ist nicht nur für den Lauf da, sondern für jeden, der später nachliest,
> was der Plan war. Sechzig verschiedene Trainingsgrenzen in einer Datei
> beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht
> man der Datei nicht an."*

### 33.2 Der Registertext — der Faltenplan nach 4a

> **Registertext (30.2 (2)), Faltenplan.** Der Faltenplan ist Registertext. Je
> Bot gelten: der Horizontbeginn (absolutes Datum oder ausdrücklich „kein
> Horizont"), die Faltenlänge in Jahren, die erste Selektionsfalte und die
> vollständige Liste der Selektionsfalten. Die Falten sind zusammenhängende
> Kalenderjahre in Schritten der Faltenlänge, aufsteigend und lückenlos vom
> Beginn der ersten Falte bis zum Go-Live-Schnitt. Eine Datei, die diesen Text
> maschinenlesbar wiedergibt, ist sein **Abbild** (33.3); der Registertext ist
> die Quelle.

> ⭐ **Ergänzt (34.1 und 34.2, TB-82, 22.09.2026):** Zwei Sätze von Fable (21m,
> Frage 1) schliessen diesen Registertext, Wortlaut in 34: **34.1** — bei
> Faltenlänge L > 1 werden (i) und (ii) am **ersten Jahr** der Falte geprüft, die
> Falte umfasst J bis J + L − 1, die folgenden schliessen lückenlos an; **34.2** —
> ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Falte und
> dem Go-Live-Schnitt ist **keine** Selektionsfalte. Der Text oben bleibt
> zeichengleich; die Tabelle unten ändert sich um nichts (Beleg M5).

> ⭐ **Ergänzt (35.1, TB-83, 22.09.2026):** Fable 22a fügt diesem Registertext die
> **Bestätigungsperiode** hinzu, Wortlaut in 35.1: die Datumsspanne von „Bestätigung
> ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich; keine Falte im Sinn
> von 4a, (1b)/34.2 betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild,
> `zellen.csv` und Berichten ist die Spanne selbst, `JJJJ-MM-TT/JJJJ-MM-TT` — für
> alle neun Bots `2026-01-01/2026-09-01` (gemessen, Beleg M1/M2). Der heutige
> Faltenname in `faltenplan.py:336` ist danach unzulässig; die Umstellung ist nicht
> Teil von TB-83. Text und Tabelle oben bleiben zeichengleich (Beleg M5).

**Tatsachennotiz — der Plan, gemessen am 21.09.2026 (TB-81, HEAD `a0c6eb0`) aus
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` (Commit `cadb968`,
SHA-256 `2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`;
Messung `docs/belege/TB-81/schritt1_faltenlisten.txt`, zwei unabhängige
Zählungen — aus `selektionsfalten` und aus `falten` mit `rolle == "selektion"` —
mit 0 Abweichungen, gegen 21.4 0 Abweichungen):**

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| `elliott_wave` | krypto | kein Horizont | 2 J | 2018–2019 | 2018–2019 · 2020–2021 · 2022–2023 · 2024–2025 | 4 |
| `t3_supertrend` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `rsi2_crypto` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `turtle_soup_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `volatility_breakout_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `elliott_wave_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `rsi2_mean_reversion` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `turtle_soup_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `volatility_breakout` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |

*Lesehilfe zur Tabelle:* „kein Horizont" steht in der gemessenen Datei als
JSON-`null` unter dem Schlüssel `horizontbeginn` (Schlüssel gesetzt, Wert
null); der Go-Live-Schnitt ist bei allen neun Bots `2026-09-01`
(ausschliesslich, 5.2). Bei `t3_supertrend` trägt die Datei daneben
`erste_falte_4a = 2018`: Bedingung (i) allein ergäbe 2018, die Konjunktion mit
dem Trockenlauf (25.3) hebt die erste Selektionsfalte auf 2019 — der in 21.4
beschriebene Fall.

⚠️ **Zur Herkunft:** Die Werte ruhen auf `asof` = 2026-09-19 (28.3), dem
Horizontbeginn je Bot (28.4), dem Vorlauf gegen den Horizontbeginn (28.6), der
Konjunktion aus 25.3 und dem Trockenlauf nach 3b (b). ⭐ **Abschnitt 32 hat
gemessen, dass die Umstellung von der Datenuhr auf `asof` keine einzige Falte
bewegt** — die Liste ist also dieselbe wie vor der Umstellung, und das ist
belegt, nicht angenommen.

*Zitierhinweis (TB-81, gemessen):* „Trockenlauf nach 3b (b)" übernimmt den
Wortlaut aus 30.2 (2). In 16.7 ist **3b (a)** der Satz zum Trockenlauf („ein
Symbol an mindestens einem Handelstag handelbar"), **3b (b)** die
`MIN_HISTORY_*`-Tabelle, die der Trockenlauf anwendet; 21.3 (a), 21.4 und
`erste_falte_quelle` in der Datei zitieren den Trockenlauf als 3b (a). Gemeint
ist an beiden Stellen derselbe Trockenlauf; der Wortlaut von 30.2 (2) wird hier
nicht geändert (append-only), der Hinweis steht, damit niemand nach einem
zweiten Trockenlauf sucht.
⭐ *Nachtrag (TB-82, 22.09.2026):* Die ausdrückliche Berichtigung — „3b (b)" lies
„3b (a)" — steht jetzt als eigener Registersatz in **34.3** (Fable 21m, Frage 3);
die Marke am Satz selbst steht unter 30.2 (2).

> ⭐⭐ **Die Benchmark-Tabelle folgt diesem Plan (39.2/39.4, Fable 23a, TB-94,
> 23.09.2026):** Registertext zu Sperrlistenpunkt 4 / 23 / 33 (23a, Wortlaut in
> **39.2**): Die Tabelle, die der Lauf liest, hat je Bot genau die
> Selektionsfalten dieses Registertexts (plus Bestätigungsperiode) — nicht
> mehr, nicht weniger. Gemessen an der vollzogenen Tabelle gegen den Plan aus
> `faltenplan.py` (`7aa0b8cc…`) im Speicher (TB-91 Block D): **18/18 gleich**,
> Bestätigungszeile 9/9 `2026-01-01/2026-09-01`. Text und Tabelle oben bleiben
> zeichengleich.

> ⭐⭐ **Die Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen
> (40.6, Fable 24a, TB-96, 24.09.2026):** Die Faltenlänge je Bot oben ruht auf
> den neun TB-24-Listen (`78e2bc6`), die nicht auf dem registrierten Snapshot
> erzeugt sind. Sie werden neu erzeugt (TB-98), die Faltenlänge wird nach 5.4
> abgeleitet und **gegen diesen Text verglichen**: gleich ⇒ Tatsachennotiz;
> verschieden ⇒ **Berichtigung dieses Texts** und allem, was daran hängt
> (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt"
> — keine Wahl. Text und Tabelle oben bleiben bis dahin zeichengleich.

### 33.3 Die Feldliste des Abbilds — abschliessend

**Fables Ersatztext für 30.2 (3), zeichengleich:**

> Das Abbild trägt **genau** die Grössen, die der Registertext des Faltenplans nach 30.2 (2) nennt — nicht mehr, nicht weniger. Der Registertext 30.2 (2) zählt diese Grössen **abschliessend** auf (die Feldliste). Eine Datei ist das Abbild, wenn (i) ihre Feldmenge gleich der Feldliste ist und (ii) ihre Werte je Bot und je Jahr dem Registertext entsprechen. Beides prüft die Sonde nach 30.2 (3); ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Wie die Datei erzeugt wird, ist Handwerk; der erzeugende Code wird mit der Datei registriert (5e).

**Die Feldliste:**

| | Feld | Inhalt |
|---|---|---|
| | `asof` | das Datum aus 28.2/28.3 |
| je Bot | `bot` | der Name |
| je Bot | `horizontbeginn` | Datum **oder** ausdrücklich „kein Horizont" — ⭐ **gesetzt, nicht weggelassen** |
| | ↳ ⭐ **Ergänzt (34.4, TB-82, 22.09.2026)** | Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen; JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde, die den Wert **positiv** gegen die zwei Formen prüft (Fable 21m, Frage 4, Wortlaut in 34.4). `faltenplan_tb80.json` (`null`) ist auch daran kein Abbild |
| je Bot | ⭐ **`faltenlaenge_jahre`** | ⚠️ **Ergänzung gegenüber Fables Vorschlag — Begründung in 33.4** |
| je Bot | `erste_selektionsfalte` | die erste Falte |
| je Bot | `selektionsfalten` | die Liste, aufsteigend und lückenlos |
| | `quelle` | der Registerabschnitt, dessen Wortlaut die Datei abbildet |
| je Bot | ⭐ **`bestaetigungsperiode`** | ⚠️ **Angefügt (35.2, TB-83, 22.09.2026)** — der Bezeichner nach 33.2/35.1, genau in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich; registrierter Bestand: `2026-01-01/2026-09-01` bei allen neun); die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne. Fable 22a; Grund in 35.3 — ersetzt 33.4 Punkt 3 |

⛔ **Nicht in der Liste und damit nicht in der Datei:** Trainingsgrenzen,
Embargo, Purge. ⭐ *Fable, zwei Sätze aus 21k, je wörtlich:* *„Verfahren B hat
kein Trainingsfenster (Übergabe Abschnitt 1); eine Grösse, die das Verfahren
nicht kennt, kann nicht im Registertext stehen und darf deshalb nicht in der
Datei stehen."* — und zur Feldliste: *„das ist die Folge der Regel, nicht die
Regel."*

⇒ ⚠️ **Keine der drei vorhandenen Dateien ist danach das Abbild** — auch
`faltenplan_tb80.json` nicht, und zwar **nicht wegen ihrer Herkunft**, sondern
weil ihre Feldmenge nicht die Feldliste ist. *Nachgemessen (TB-81, Beleg
Schritt 1): `faltenplan_tb80.json` trägt je Bot 18 Felder und auf oberster
Ebene weder `asof` noch `quelle`.*

> ⭐⭐ **Gerechneter Plan und Abbild — die registrierte Abbildung (42.1 D5,
> 42.2 E3, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Diese Feldliste ist
> die des **Abbilds**. Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt
> mehr — seine Herleitungsfelder (25.3/32.1) — und **schrumpft nicht**; er trägt
> aber keine Grösse, die das Verfahren nicht kennt (Trainingsgrenzen, Embargo,
> Purge, Mindesttraining; entfernt in TB-104 und TB-106). Die Sonde vergleicht
> Plan und Abbild über eine **registrierte Abbildung**; die **Feldliste des
> gerechneten Plans** ist Registertext (**42.2, E3** — die Zuordnung je
> Schlüssel steht aus, 42.6). Mit dem Abbild wird die **Erzeugerkette des
> Trockenlaufs** registriert (**42.3, F4**). Tabelle und Text oben bleiben
> zeichengleich.

> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Tabelle, Text und die Marke oben bleiben
> zeichengleich.

### 33.4 ⚠️ Zwei Anpassungen an Fables Feldliste, und warum

**Er hat sie ausdrücklich zur Prüfung gestellt** (*„ich prüfe dann Text und
Feldliste zusammen"*) und eine Unsicherheit benannt.

| | Befund | Folge |
|---|---|---|
| **1** | ⚠️⚠️ **`selektionsfalten` als „Liste von Kalenderjahren" deckt `elliott_wave` nicht ab.** Gemessen: Seine vier Falten sind **Doppeljahre** (`2018-2019`, `2020-2021`, `2022-2023`, `2024-2025`), die der acht übrigen Bots Einzeljahre | Der Registertext in 33.2 sagt **„zusammenhängende Kalenderjahre in Schritten der Faltenlänge"** statt „Kalenderjahre" |
| **2** | ⭐ **Ohne `faltenlaenge_jahre` ist die Liste nicht prüfbar.** Aus `['2018-2019', …]` allein folgt nicht, ob die Faltenlänge 2 ist oder ob zwei Einzeljahre zusammengeschrieben wurden | Das Feld kommt in die Liste |
| **3** | **Seine Unsicherheit — die Bestätigungsperiode je Bot:** Sie steht **bereits** in Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave` `2026-2027`, die acht übrigen `2026`) | ⭐ **Nicht in die Feldliste.** *Ein Abbild bildet ab, was sein Abschnitt sagt; eine Grösse, die anderswo registriert ist, wäre ein zweiter Ort für denselben Wert* — die Bauart, die er in 21j selbst abgelehnt hat |
| | ⚠️ **Berichtigt (34.6, TB-82, 22.09.2026):** Die Fundstelle „21.4" trägt den Satz nicht — 21.4 führt „Bestätigung ab" `2026-01-01` bei allen neun Bots (gemessen, Beleg M3); `2026-2027` und `2026` sind Faltennamen aus `faltenplan.py:336`, nicht aus dem Register (Beleg M2). Registriert ist die Bestätigungsperiode als **Datumsspanne**: Beginn 21.4 (`2026-01-01`), Ende 5.2 (`2026-09-01`, ausschliesslich) | Die Folge bleibt: **kein Feld** — Fables Halbsatz *„33.2 nennt sie nicht"* trägt allein. ⚠️ Welche der zwei Formen (Datumsspanne / Faltenname) gilt, ist **offen** — bei Fable, Anfrage 21g Punkt 3 (34.6) |
| | ⚠️ **ERSETZT (35.3, TB-83, 22.09.2026):** „Nicht in die Feldliste" gilt nicht mehr — Fable 22a, zeichengleich: *„Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist."* Der Name ist ein Schlüssel, den `auswertung.py` (Z. 432) und der Erzeuger teilen (sechste Rücknahme). Feld `bestaetigungsperiode` in 33.3 angefügt (35.2); Punkt 3 oben bleibt zeichengleich | — |

⚠️ **Alle drei sind dem Verfahrensprüfer vorzulegen.** Punkt 1 und 2 ändern
seinen Wortlaut; Punkt 3 beantwortet seine Unsicherheit. ⛔ **Der Abschnitt gilt
bis dahin mit diesem Vermerk** — er ist nicht vorläufig, aber die Prüfung steht
aus.

### 33.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, nach Fables Prüfung von 33.2/33.3 und mit Betreiberfreigabe |
| ⛔ | **Die Sonde schreiben** (Feldmenge und Werte gegen den Registertext) | dieselbe Aufgabe |
| ⛔ | **Eine Datei mit Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` ändern** — die Freigabe vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⚠️ | **Entscheidungsvorlage, nicht vollzogen:** ob die Abbild-Datei aus einem geänderten `faltenplan.py` entsteht oder aus einem **neuen, kleinen Schreiber**, der genau die Feldliste ausgibt. ⭐ *Fable: „gleichwertig, solange der Code registriert ist."* Beides berührt Sperrlisten-nahen Code und braucht eine eigene Freigabe | Betreiber |

> ⭐⭐ **Plan-Punkt 7 rückt vor (40.6/40.8 (g), Fable 24a, TB-96,
> 24.09.2026):** Das Abbild des Faltenplans (33.3) und die Faltenplan-Sonde
> sind die Wache gegen einen Schwellenübertritt, der den Faltenplan eines Bots
> verschiebt — und sie fehlen. ⚠️ **Erzeugt wird das Abbild NACH der
> Neu-Ableitung der Faltenlänge (TB-98), nicht vorher** — sonst bildet es einen
> Stand ab, der gerade geprüft wird (TB-100). Die Tabelle oben bleibt
> zeichengleich; die Freigaben, die sie verlangt, gelten weiter.

---

