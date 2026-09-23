# TB-95 — Ergebnis: „Testannahmen folgen dem Register“ — G6 und H3 folgen dem Faltenplan, der Test ist grün (165/165); Antwort auf Fables Messbitte zu den neun Handelslisten

**Sitzungstitel:** `TB-95` · **Stand:** 23.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-95_testannahmen_und_lesehaken.md` · **Belege:** `docs/belege/TB-95/`
**Eingang:** `4faef05` (TB-94-Abgabe) · Commits: `b83105b` (Schritt 0), `9e2a071`
(Block A/B: Messung und Testanpassung), `069370d` (Block D: Messbitte), Abgabe-Commit
(Block C-Belege, dieses Dokument, Journalblock CW).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** `test_vorregistrierung.py` läuft **165/165, rc 0, 534 s**, und das am echten Stand.
Damit ist die Tag-Vorbedingung „null rote Prüfungen“ aus 21.9/A4 erfüllt. Geändert ist **nur**
diese eine Datei (79/25). Kein Sperrlistenhash hat sich bewegt, die Sonde meldet 0 Befunde bei
15/15 gleichen Pfaden. **Zwei Erwartungen des Auftrags haben sich als falsch erwiesen:**

- H3 greift nicht ins Leere. Alle vier Namen treffen, nur verschieben vier Nullen bei neun
  Falten den Median nicht.
- Die Quelle, die A1 nennt (`faltenplan.json`), liest der Lauf nach Register 30.2 (1) gar nicht.

**Messbitte:** `benchmark.py` öffnet die neun TB-24-Listen selbst, über `fp.faltenplan`. Ihre
Inhalte **gehen ein**, allerdings nur über die Faltenlänge, eine Schwellenentscheidung. Der
Modus-Lauf ist zum fünften Mal bytegleich (`64fb2912…`).

---

## 0. Schritt 0

| | |
|---|---|
| Arbeitsbaum | eine geänderte Datei des steuernden Chats (`ARBEITSWEISE.md` 22.4, +21 Zeilen) → `b83105b` |
| Git-Sperrdateien | `find .git -name '*.lock'` → keine |
| HEAD vor Schritt 0 | `4faef05` = TB-94-Abgabe ✔ |
| Abschnitt 39 im Register | vorhanden, Z. 7073 ✔ (Abbruchkriterium 1 greift nicht) |
| Die TB-94-Hilfsdatei `_anhang_arbeitsweise_22.md` | liegt nicht mehr im Arbeitsbaum |

## 1. Block A — gemessen vor der Änderung

### A1 — der Ist-Stand (`a1_faltenplan_ist.txt`)

⚠️ **Die Quelle aus dem Auftrag war nicht die richtige.** Der Auftrag nennt
`ergebnisse/faltenplan.json` (`0e54ac5c…`). Nach **Register 30.2 (1)** ist diese Datei aber der
„registrierte historische Stand eines früheren Verfahrensstands … wird vom Lauf nicht gelesen“.
Darin sind die fünf Krypto-Bots Platzhalter ohne Falten, die Aktien-Bots beginnen 2019. Nach
**35.4** verwendet der Lauf den Plan, den `faltenplan.py` zur Laufzeit bildet. Genau diesen liest
auch der Test (`_plan()` → `fp.faltenplan(rd._mess())`). Ein Abbild nach 33.3 gibt es noch nicht
(33.5). Gemessen habe ich beide Stände. Massgeblich ist der Laufzeitplan, und der stimmt mit der
Tabelle in **33.2** überein (0 Abweichungen):

| Bot | Faltenlänge | Selektionsfalten | # | Bestätigung |
|---|---:|---|---:|---|
| `elliott_wave` | 2 | 2018-2019 · 2020-2021 · 2022-2023 · 2024-2025 | 4 | `2026-01-01/2026-09-01` |
| `t3_supertrend`, `rsi2_crypto` | 1 | 2019 … 2025 | 7 | dito |
| `turtle_soup_crypto`, `volatility_breakout_crypto` | 1 | 2018 … 2025 | 8 | dito |
| `elliott_wave_stocks`, `turtle_soup_stocks` | 1 | 2017 … 2025 | 9 | dito |
| `rsi2_mean_reversion`, `volatility_breakout` | 1 | 2018 … 2025 | 8 | dito |

### A2 — G6 (`a2_g6.txt`)

| | Ergebnis |
|---|---|
| **A2-1** | Rot ist **nur** `elliott_wave` (Doppeljahre). Das war erwartet und ist bestätigt |
| ⭐ **A2-2** | **Ja.** 2020 und 2022 liegen bei **allen neun** Bots in genau einer Selektionsfalte. Bei `elliott_wave` sind das `2020-2021` und `2022-2023`, gerechnet aus `von`/`bis_ausschliesslich`. Keine Bestätigungsfalte deckt eines der Jahre ab. ⇒ Nur die Formulierung war veraltet, und Block B durfte laufen |
| **A2-3** | Register **5.1 Nr. 4**, Z. 565 (HEAD `b83105b`): „**2020 und 2022 sind Testfalten, keine Trainingsjahre.** … `test_vorregistrierung.py` Teil G prüft es maschinell.“ In 5.1 steht dazu der Vermerk (Z. 552), dass Nr. 4 von Abschnitt 15 **unberührt** bleibt. Die Prüfung stammt aus `a2fcf01` (TB-30a) |
| **A2-4** | Die **Jahre** kommen aus 5.1 Nr. 4, einem Satz über Test- und Trainingsjahre. Die **Falten** kommen aus dem Plan: Registertext 33.2, gerechnet von `faltenplan.py`. Solange das Abbild 33.3 nicht existiert, ist `faltenplan.py` die einzige maschinenlesbare Quelle, und die lässt Fable 23a ausdrücklich zu („aus dem Abbild … oder aus `faltenplan.py`“) |

### A3 — H3 (`a3_h3.txt`)

| | Ergebnis |
|---|---|
| **A3-1** | `BOT = turtle_soup_stocks`: 10 Falten, davon **9 Selektionsfalten** (2017–2025) |
| ⚠️ **A3-2** | **Alle vier** Namen in `ohne` treffen eine Selektionsfalte. **Die Erwartung „null“ ist widerlegt.** Die Probe greift nicht ins Leere; sie beisst nicht, weil die **Anzahl** nicht reicht. Das entspricht der Diagnose in Register 38 |
| **A3-3** | Bestätigt: `'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'`, nachgestellt mit zwei Unterprozessen wie im Test |
| ⭐ **A3-4** | Gerechnet: k Falten mit 0 Trades (Dateiwert 9,0), n−k Falten mit 0,10. Bei ungeradem n ist der Median der ((n+1)/2)-te Wert. Er wechselt deshalb erst ab **k ≥ (n+1)/2**, bei geradem n ab k ≥ n/2. Allgemein ist das kleinste wirksame k = ⌈n/2⌉. **Bei n = 9 beisst die Probe ab k = 5**; mit k = 4 bleibt sie wirkungslos. Für n = 7 (der Kommentar im Test) war 4 richtig. Die Tabelle für k = 0…n steht im Beleg |
| **A3-5** | Ja, dieselbe Klasse wie G6: vier Faltennamen als Literale und dazu eine Anzahl, die aus einer Faltenzahl abgeleitet war, die nirgends im Code steht |
| B3 | Die Mutationsstelle kommt in `auswertung.py` (`c3b4e69d…`) **genau 1-mal** vor ✔ |

### A4 — weitere Literale (`a4_literale.txt`)

| Stelle | Literal | heute | in TB-95 |
|---|---|---|---|
| `test_vorregistrierung.py:495` G6 | `"2020"`, `"2022"` | rot | **geändert** |
| `test_vorregistrierung.py:590` H3 | `{"2019".."2022"}` + Anzahl 4 | rot | **geändert** |
| `test_vorregistrierung.py:246` Teil D | `ruhig, krise = "2021", "2020"` | grün, nur weil `BOT` Einjahresfalten hat. Die Jahreswahl ist Registerinhalt 4.4 | gelistet |
| `test_vorregistrierung.py:442` Teil F | `ohne = "2022"` | grün, aus demselben Grund | gelistet |
| `beispieldaten.py:69` | `falte in ("2020", "2022")` (Krisen-Drawdown) | trifft bei `elliott_wave` nie | gelistet |
| `beispieldaten.py:77` | dasselbe (Exposure) | bei `elliott_wave` konstant 0,40. Nach dem eigenen Docstring ist der Zufalls-Timing-Test dann **entartet** | gelistet |

⚠️ **Zusatzbefund F4:** Die Prüfung sagt „Median mit der Null liegt **unter** …“, prüft aber mit `<=`.
Bei einer Null unter 9 (oder 7) Falten sind beide Mediane gleich (0,10). **F4 hat nie gebissen**,
und das hängt nicht am Plan. Es ist nicht die Bauart von G6/H3, deshalb habe ich es nicht geändert.

**Warum D, F und `beispieldaten.py` nicht geändert sind:** Sie sind heute grün. Für D und F wäre
die Technik dieselbe („Falte, die Jahr J abdeckt“). Welche Registerstelle ihre Jahre trägt, ist
aber eine Entscheidung (4.4 hat den TB-30a-Stand; F ist ein freies Beispiel). `beispieldaten.py`
ist keine Prüfung. ⚠️ **Bruchstelle:** Bekommt `BOT` einmal Zweijahresfalten, bricht Teil D mit
`KeyError` ab, und F1/F2 werden rot.

## 2. Block B — der Test folgt dem Register (`9e2a071`, Beleg `b_probe.txt`)

| | Änderung |
|---|---|
| **B1 G6** | Die Jahre liest der Test aus dem Registertext 5.1 Nr. 4 (`_testjahre_aus_register`, Muster auf den Listenpunkt, genau ein Treffer, sonst `None` ⇒ rot). Die Abdeckung **rechnet** er aus `von`/`bis_ausschliesslich` der Falten mit Rolle `selektion` (`_abgedeckte_jahre`). Name `G6` und Stelle bleiben gleich; die Fehlerausgabe zeigt Faltennamen **und** abgedeckte Jahre. Kein `in namen` mehr |
| **B2 H3** | `ohne` = die ersten `len(sel) // 2 + 1` Selektionsfalten des Plans, also eine strikte Mehrheit, die bei jeder Parität beisst. Heute sind das 5 von 9: `2017`–`2021`. Die Probe steht jetzt in `_h3_lauf(mess, plan, ohne)`, damit die Gegenprobe denselben Weg geht. Der Kommentar nennt die neue Regel und die Zahl mit Stand („beim Plan von TB-95 … fünf“). Die Fehlerausgabe nennt `ohne` und die Selektionsfalten |

**Nachweise, mit den Funktionen des Tests selbst:**

| Probe | erwartet | gemessen |
|---|---|---|
| B1-a echter Plan | 0 × G6 rot | Teil G 107/0 ✔ |
| B1-b `elliott_wave` `2020-2021` als `bestaetigung` | genau 1 × G6 rot | 1 × G6 (`elliott_wave`), dazu G7 wie zu erwarten ✔ |
| B1-c `turtle_soup_stocks` ohne Falte `2022` | genau 1 × G6 rot | 1 ✔ |
| B1-d Registersatz fehlt (Kopie) | 9 × G6 rot | 9, Jahre `None` ✔ |
| ⭐ **B2-a** neue Menge (5 von 9) | beisst | mit Regel `0.0000`, ohne Regel `9.0000` → **bestanden** ✔ |
| ⭐ **B2-b** `ohne` leer | darf nicht beissen | `0.1000` / `0.1000` → **gescheitert** ✔ — die Probe beisst aus dem richtigen Grund |
| B2-c alte Menge (4 von 9) | Vergleich | `0.1000` / `0.1000` → gescheitert (der Zustand vor TB-95) |

Keine Prüfung entfernt, keine Ausnahme für einen Bot, keine Toleranz. `auswertung.py` ist
unberührt.

## 3. Block C — der ganze Test am echten Stand

| | |
|---|---|
| Aufruf | `trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py`, am HEAD `9e2a071`, in einem Zug |
| ⭐ Ergebnis | **165/165 Prüfungen bestanden, rc 0**, Schlusszeile erreicht (`c_test.txt`) |
| Laufzeit | **534 s** (TB-92: 501 s) |
| Zahl der Prüfungen | 165 wie zuvor (163 + 2). Keine hinzugekommen, keine weggefallen |
| Hashes | vorher/nachher (`hashes_vorher.txt`, `c_hashes.txt`): **nur** `test_vorregistrierung.py` `6e7defef…` → `73c9b837…`. Alle Sperrlistendateien, beide Abbilder, `faltenplan.json`, alle Benchmark-Tabellen und die neun Listen sind gleich |
| Sonde gegen `sperrliste_abbild_2026-09-23.json` | vorher und nachher: **0 Befunde**, 15/15 Pfade gleich, (ii) 0, Gesamtausgang **2** (zwölf Punkte mit Nicht-Dateibezogenem, R6, wie in TB-94) (`sonde_vorher.txt`, `c_sonde.txt`) |

## 4. Block D — Fables Messbitte

⭐ **Die Antwort steht fertig formuliert in `docs/belege/TB-95/d3_antwort.md`** und kann
unverändert in eine Anfrage übernommen werden. Kurzfassung:

| | |
|---|---|
| **Wer öffnet** | `benchmark.py::je_bot` (Z. 222) → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (Z. 133, `read_csv`). Jede Liste genau einmal, nur im Hauptprozess, kein Nebenweg. Statisch nennt nur `faltenplan.py` den Pfad (Z. 121/132) |
| ⭐ **Modus-Lauf** | rc 0, 56 s, 11 Prozesse, **`64fb2912…` bytegleich**: die fünfte Wiederholung des Determinismusnachweises ✔ (Abbruchkriterium 6 greift nicht) |
| **Gehen sie ein?** | **Ja, über genau eine Grösse: die Faltenlänge.** (a) Datenfluss: nur `entry_time` → Zählung je vollem Jahr → Mittel gegen die Schwelle 30 → Länge 1 oder 2 → Faltengrenzen → Tabellenzeilen. (b) Störprobe auf Kopien: **eine Zeile entfernt → bytegleich**, **zwei Drittel entfernt → verschieden** (`97cf224f…`, nur `volatility_breakout_crypto`, von Einjahres- auf Zweijahresfalten). (a) und (b) stimmen überein |
| ⚠️ | Die Probe, wie der Auftrag sie vorschlägt („eine Zeile entfernen genügt“), hätte **allein das falsche „nein“** ergeben. Die Inhalte wirken über eine Schwelle |
| **Eingabestand** | Die Listen sind **nicht** im Snapshot und nicht auf der Sperrliste. Im Register sind sie als Quelle genannt (5.4), aber ohne Hash. Es gibt einen einzigen Commit, **`78e2bc6`, 13.09.2026 (TB-24)**, und seitdem sind sie unverändert. Es **sind die TB-24-Listen**, gemessen an Pfad, Commit und Datum: vor TB-31/TB-34/TB-38 und vor dem Snapshot. Die Krypto-Listen beginnen erst 2021-09 |
| Originale | alle neun sha256 vorher = nachher ✔ |

## 5. Vorschlag für den Registertext — gemessen, **nicht eingetragen**

> **40. Testannahmen folgen dem Register — `G6` und `H3` (Fable 23a/23f, TB-95, 23.09.2026)**
>
> **40.1 Tatsachennotiz.** `test_vorregistrierung.py` (`73c9b837…`, Commit `9e2a071`) läuft
> am 23.09.2026 **165/165, rc 0** (534 s). Damit ist die Tag-Vorbedingung „null rote Prüfungen,
> null ‚bekannt rot‘“ (21.9, A4) für diesen Test erfüllt. Geändert sind nur `G6` und `H3`, keine
> Prüfung ist entfallen. Kein Sperrlistenhash hat sich bewegt, und die Sonde gegen
> `sperrliste_abbild_2026-09-23.json` meldet 0 Befunde.
>
> **40.2 `G6`.** Die Jahre kommen aus 5.1 Nr. 4, maschinell aus dem Registertext gelesen. Die
> Abdeckung wird aus den Grenzen der Selektionsfalten des Plans gerechnet, den `faltenplan.py`
> bildet. Gemessen vor der Änderung: Die Sache hinter 5.1 Nr. 4 war bei allen neun Bots erfüllt;
> rot war nur die Formulierung (`elliott_wave`, Doppeljahre).
>
> **40.3 `H3`.** Die Probe setzt eine strikte Mehrheit der Selektionsfalten des Plans auf null
> Trades. Heute sind das 5 von 9, bei `turtle_soup_stocks`. Gemessen vor der Änderung: Alle vier
> alten Namen trafen, aber vier Nullen verschieben den Median über neun Falten nicht. Die Probe
> beisst wieder (`0.0000` / `9.0000`), und die Gegenprobe mit leerer Menge scheitert.
>
> **40.4 Liste der weiteren Literale** (nicht geändert): Teil D (`"2021"`, `"2020"`, Jahre aus
> 4.4), Teil F (`"2022"`), `beispieldaten.py` Z. 69/77. Dazu **F4**, das mit `<=` prüft und nie
> gebissen hat.
>
> **40.5 Tatsachennotiz zu 39.8 (Messbitte 23f Abschnitt 6).** Die neun
> `research/tb24_haltedauern/daten/*_alle_trades.csv` öffnet `benchmark.py` über
> `fp.faltenplan` → `faltenlaenge_jahre`. Ihre Inhalte gehen **über die Faltenlänge** in den Plan
> und damit in die Tabelle ein; eine Störprobe hat das in beide Richtungen gezeigt. Sie stammen aus
> `78e2bc6` (TB-24, 13.09.2026) und liegen nicht im Snapshot. Die Einordnung nach 23d steht bei
> Fable aus.

⚠️ Der Eintrag braucht Fables Kenntnisnahme (Auftrag, „Was NICHT geschieht“). Die Nummer 40 ist
die nächste freie.

## 6. Was offen bleibt

| | |
|---|---|
| Fable | die Einordnung der neun Listen nach 23d (Hash-Eintrag oder volle Regel mit Snapshot und Nachweislauf); ob D/F/`beispieldaten.py` bauartgleich umgestellt werden sollen; F4 (`<=` → `<` würde F4 rot machen, weil der Median bei einer Null gleich bleibt — die Probe bräuchte dann ebenfalls eine Mehrheit) |
| nächster Auftrag | Registerabschnitt 40 (Vorschlag oben) |
| TB-96 | `messgroessen.json`, unverändert offen |

## In einfacher Sprache

Das Prüfprogramm hatte zwei rote Prüfungen. Beide beruhten auf fest eingetippten Jahreszahlen
aus einer Zeit, in der der Plan anders aussah.

**Die erste** suchte wörtlich nach dem Abschnitt „2020“. Ein Bot hat inzwischen Doppeljahre
(„2020-2021“), und dort fand sie nichts, obwohl das Jahr 2020 dort ganz richtig getestet wird.
Jetzt liest die Prüfung die Jahre aus dem Registertext und rechnet nach, welcher Abschnitt sie
abdeckt.

**Die zweite** ist eine Gegenprobe: Sie schaltet eine Regel ab und schaut, ob sich etwas ändert.
Vermutet war, dass ihre eingetippten Namen nichts mehr treffen. Das stimmte nicht; sie trafen
alle. Der eigentliche Grund: Aus früher sieben Abschnitten sind neun geworden, und vier
veränderte Abschnitte reichen bei neun nicht mehr aus, um den Mittelwert (einen Median) zu
verschieben. Jetzt nimmt die Probe immer mehr als die Hälfte der Abschnitte aus dem Plan, heute
fünf, und sie greift wieder. Umgekehrt ist nachgewiesen, dass sie ohne veränderte Abschnitte
tatsächlich fehlschlägt.

Danach liefen alle 165 Prüfungen durch, ohne Fehler, und keine geschützte Datei hat sich verändert.

**Der zweite Teil** beantwortet eine Frage des Verfahrensprüfers. Neun alte Handelslisten vom
13. September werden beim Rechnen der Vergleichstabelle geöffnet. Sie werden nicht nur geöffnet,
sie wirken auch mit: Aus ihnen wird ausgerechnet, ob ein Bot ein- oder zweijährige Abschnitte
bekommt. Eine kleine Änderung an einer Kopie änderte am Ergebnis nichts, eine grosse änderte die
Abschnitte des Bots und damit die Tabelle. Die Listen gehören nicht zum eingefrorenen
Datenbestand. Wie das zu behandeln ist, entscheidet der Verfahrensprüfer.
