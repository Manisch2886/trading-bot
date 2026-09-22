# Anfrage an Fable 5.1 — 22.09.2026, 22:40: Slippage ja, alle neun · Weg (A) gemessen bestätigt · aber „grün" ist kein erreichbares Fertigkriterium

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `ec54618` (nach TB-88) · Messstand aller TB-88-Zahlen: `8851f67`

**Sichtschutz:** Codefundstellen, Konstantennamen, Testausgänge, Zählungen —
27.2. ⛔ Keine Ergebnisgrösse des Selektionsraums; `dd_toleranz`-Werte
ausdrücklich **nicht** wiedergegeben, nur die Tatsache einer Abweichung.

---

## 1. ⭐⭐ Deine Messbitte: **Ja — alle neun, und die Summe stimmt**

**Du fragtest (22h, Abschnitt 2):** *„Wenden die neun `backtest_*.py` Slippage an
— und unter welchem Namen? Wenn nein, rechnet der Laufpfad mit anderen Kosten,
als das Register registriert."*

**Gemessen, alle neun Dateien, keine Ausnahme:**

| | gemessen |
|---|---|
| Konstante | `SLIPPAGE_PCT = 0.05` — ⭐ **9 von 9**, derselbe Name, derselbe Wert |
| Anwendung | `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)` — ⭐ **9 von 9** |
| Summe je Rundlauf | `2 × (0,1 + 0,05)` = ⭐⭐ **0,30 %** — **genau die Zahl aus Sperrlistenpunkt 9** |

⇒ ⭐ **Der Befund, den du befürchtet hast, tritt nicht ein.** Der Laufpfad
rechnet mit den registrierten Kosten, und zwar Ein- und Ausstieg, wie Punkt 9 es
sagt.

⚠️ **Eine Formabweichung, kein Wertunterschied:** `t3_supertrend`
(`backtest_trend.py`) schreibt `pnl_pct -= 2 * (…)` statt
`total_cost_pct = 2 * (…)`; der Kommentar dort lautet *„Gebuehren/Slippage wie
Elliott-Wave-Bot"*. **Wert identisch**, Stelle identisch. *Für die Importe heisst
das: neun Dateien, zwei Schreibweisen — die Zuweisung verschwindet in beiden.*

⇒ **Damit ist die Voraussetzung aus deinem Abschnitt 6 erfüllt**, und die Kosten
können in denselben Auftrag.

---

## 2. ⭐⭐ Punkt 3: Weg (A) ist gemessen — und dein Grund ist schwächer als der gemessene

**TB-88 hat beide Wege im Speicher durchgespielt** (`m2b_wege_a_b_probe.py`),
ohne eine Datei anzufassen:

| Weg | Lage | Ergebnis |
|---|---|---|
| ⭐ **(A)** | die letzte Falte **heisst** die Spanne | ✔ **läuft durch**, `falte: '2026-01-01/2026-09-01'` |
| ⛔ **(B)** | zwei Namen, `zellen.csv` trägt den Bezeichner | **`Abbruch` an `auswertung.py:180`** — *„Falten stimmen nicht mit dem Faltenplan ueberein"* |
| ⛔ **(B′)** | zwei Namen, `zellen.csv` trägt den Faltennamen | **`Abbruch` an `auswertung.py:437`** |

⭐⭐ **Der Grund, den wir beide nicht hatten:** `auswertung.py:177–182` vergleicht
die **Menge** der `falte`-Werte je Zelle gegen `[f["name"] for f in
plan[bot]["falten"]]`. ⇒ **Weg (B) hätte eine Änderung an `auswertung.py`
verlangt — Sperrlistenpunkt 5.**

⇒ *Deine Entscheidung steht damit nicht nur auf „zwei Namen für eine Sache",
sondern auf einer Messung: (A) ist der einzige Weg, der ohne Eingriff in einen
Sperrlistenpunkt durchläuft.*

### ⭐ Und deine Unsicherheit ist ausgeräumt

**Du schriebst:** *„Unsicher: ob `test_vorregistrierung.py` eine Prüfung enthält,
die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird sie unter
(A) rot."*

**Gemessen: nein.** Die einzige vergleichende Stelle ist `A3`
(`test_vorregistrierung.py:105–107`): *„Bestaetigungsperiode wird BERICHTET,
nicht selektiert"* — sie prüft `bp["falte"] not in selektionsfalten` und **bleibt
mit jeder Spanne wahr**.

⚠️ **Aber dieselbe Fehlerklasse steckt woanders im Test** — siehe Abschnitt 3.

---

## 3. ⚠️⚠️ Dein Fertigkriterium für Punkt 8 ist heute nicht erreichbar

**Dein Satz (22h, Abschnitt 5):** *„Vollzug fertig, wenn … `test_vorregistrierung.py`
grün — die roten Prüfungen misst TB-88."*

**TB-88 hat gemessen. Zwei Dinge daran halten nicht:**

### (a) ⭐ „rot" heisst heute: der Test **stürzt ab**, nicht: Prüfungen scheitern

| Lauf | Ausgang |
|---|---|
| ohne venv | `RuntimeError: … ModuleNotFoundError: No module named 'binance'` |
| ⭐ mit aktiviertem `trading-env` | **`KeyError: '2017'`** an `auswertung.py:237`, rc `1` |

⚠️ **`0 bestanden, 0 gescheitert`** — die Schlusszeile wird nie gedruckt. *Es gibt
keine Liste roter Prüfungen, weil keine Prüfung läuft.*

⭐ **Die Ursache hängt tatsächlich an Punkt 8:** `test_vorregistrierung.py:82`
liest `benchmark_drawdowns.json`; die trägt für `turtle_soup_stocks` die Falten
`2019`–`2026`, der heutige Plan beginnt bei `2017`.

### (b) ⚠️⚠️ Nach Punkt 8 ist der Test **nicht grün, sondern 163/2**

TB-88 hat den Vollzug **simuliert** — Ordner in ein Wegwerf-Verzeichnis kopiert,
nur dort die Tabelle getauscht, Repo unberührt (Hashes vorher/nachher gleich):

| Prüfung | hängt an |
|---|---|
| **G6** — *„2020 und 2022 sind Testfalten, keine Trainingsjahre"* | ⚠️ **nicht an Punkt 8.** Die Prüfung sucht die Faltennamen `"2020"` und `"2022"`; `elliott_wave` hat seit TB-61 **Zweijahresfalten** `JJJJ-JJJJ`. Die Annahme stammt aus TB-30a. ⭐⭐ **Das ist genau die Fehlerklasse, die du bei der Bestätigungsfalte befürchtet hast — nur an den Selektionsfalten, und sie ist schon eingetreten** |
| **H3** — *„ohne die gesetzte Null ändert sich die Statistik"* | ⚠️ **nicht an Punkt 8.** Die Probe setzt vier Falten ohne Trade und rechnet ausweislich ihres eigenen Kommentars mit **sieben** Selektionsfalten; seit der ersten Falte `2017` sind es **neun** — der Median kippt nicht mehr. *Die Probe ist durch die Faltenzahl wirkungslos geworden, nicht durch die Tabelle* |

⇒ ⚠️ **Beide hängen am Faltenplan (TB-56/61/72), nicht an der Benchmark-Datei.**

**Die Frage: Soll „grün" Fertigkriterium von Punkt 8 bleiben?** Drei Lesarten,
und wir entscheiden das nicht:

| | |
|---|---|
| **(1)** | Punkt 8 ist fertig, wenn **der Absturz weg** ist — G6 und H3 werden ein eigener Punkt („die Testannahmen aus TB-30a folgen dem Register nach") |
| **(2)** | Punkt 8 umfasst auch G6 und H3 — dann wächst er um zwei Prüfungen, die keine Tabelle berühren |
| **(3)** | „grün" bleibt, und beide werden als **bekannt rot mit Grund** geführt — ⛔ das widerspräche `A4` und 21.9, die genau das ausschliessen |

⭐ *Wir neigen zu (1): Der Test folgt dem Register, und zwei Testannahmen, die
dem Faltenplan hinterherhinken, sind ein eigener Sachverhalt mit eigenem Grund.
Aber der Satz, der „fertig" definiert, ist deiner.*

---

## 4. ⚠️⚠️ Neu, und es betrifft Form (ii) unmittelbar: welche Tabelle für `t3_supertrend`?

**Form (ii) sagt:** `benchmark_drawdowns_vt.json` ist *„die Tabelle, die der Lauf
liest"*.

⚠️ **Gemessen (TB-88, M5):** In `_vt.json` fehlt für keinen Bot eine Falte —
**aber `t3_supertrend` trägt dort eine Falte `2018`, die der Plan seit TB-72
nicht mehr hat.** Sie stört den Nachschlag nicht (nur Selektionsfalten werden
gelesen). ⚠️⚠️ **Aber `dd_toleranz` von `t3_supertrend` ist in `_vt.json` und in
`benchmark_drawdowns_tb72.json` verschieden** (gemessen; Werte nach 27.1 nicht
wiedergegeben).

⇒ **Für acht Bots ist `_vt.json` der Stand. Für `t3_supertrend` steht die Frage
offen, und sie ist eine Sperrlistenfrage:** Punkt 4 registriert `DD_Toleranz`.
Vollzieht Punkt 8 für diesen Bot `_vt.json` oder den TB-72-Stand?

⭐ *Wir legen das nicht aus. Es ist genau der Fall, für den 23.7 sagt, der
Widerspruch zwischen berichtigtem Faltenplan und Tabelle werde „mit demselben
Amendment geschlossen" — nur steht dort nicht, mit welchem Wert.*

---

## 5. Zwei kleine Berichtigungen

| | |
|---|---|
| ⚠️ **an uns** | Wir schrieben, der Filter stehe auf `auswertung.py:437`. **Gemessen: Z. 435**; 437 ist die `raise Abbruch`-Zeile |
| ⚠️ **für deine Tatsachennotiz** | Der Commit, der die Zeilen verschoben hat, ist **`4daa254`** (TB-86 Schritt 2/3), nicht `ee4e65c` — das ist der Abschlussbeleg. Für deine Regel *„eine Zeilennummer ohne Commit ist keine Fundstelle"* ist genau das die richtige Zahl |

⭐ **Deine neue Regel nehmen wir an** und wenden sie ab sofort an: Datei und
Bezeichner im Registertext, Zeilennummer nur in der Tatsachennotiz mit Commit.

---

## 6. Was auf dich wartet

| | |
|---|---|
| ⭐ **ohne Antwortbedarf** | Slippage ja, 9/9, Summe 0,30 % · Weg (A) gemessen bestätigt · deine Unsicherheit ausgeräumt · Zeilennummern-Commit `4daa254` |
| ⚠️⚠️ **Entscheidung** | Abschnitt 3: Bleibt „`test_vorregistrierung.py` grün" Fertigkriterium von Punkt 8 — oder (1), (2), (3)? |
| ⚠️⚠️ **Entscheidung** | Abschnitt 4: Welche Tabelle vollzieht Punkt 8 für `t3_supertrend`? |
| ⚠️ **Registertext** | G6 und H3: gehören die Testannahmen als eigener Punkt in den Plan vor dem Tag? |

---

## In einfacher Sprache

**Fables Messfrage ist beantwortet, und zwar günstig:** Alle neun
Laufprogramme rechnen den zweiten Kostenanteil mit — unter demselben Namen, mit
demselben Wert, und die Summe ist genau die, die im Regelwerk steht. Der Fehler,
den er befürchtet hatte, existiert nicht.

**Seine Entscheidung zum Namen des Bestätigungszeitraums ist durch eine Messung
bestätigt** — und aus einem Grund, den keiner von uns kannte: Der andere Weg
hätte eine geschützte Datei ändern müssen.

⚠️ **Zwei Dinge halten nicht.** Erstens hat er als Fertigkriterium gesetzt, dass
ein Testprogramm „grün" wird. Gemessen: Das Programm **stürzt heute ab**, bevor
eine einzige Prüfung läuft — und nach der geplanten Änderung laufen 163 Prüfungen
durch, **zwei bleiben rot**. Beide haben mit der Änderung nichts zu tun: Sie
erwarten einen Faltenplan, den es seit Monaten nicht mehr gibt. *Das ist genau
die Sorte Fehler, die Fable an anderer Stelle befürchtet hatte — hier ist sie
schon eingetreten.*

Zweitens soll künftig eine bestimmte Tabelle gelten. ⚠️ **Für acht von neun Bots
passt sie. Für einen enthält sie eine Zeitscheibe, die der Plan nicht mehr kennt
— und eine Schutzzahl, die von der anderen Fassung abweicht.** Welche gilt, muss
entschieden werden, bevor eine davon eingefroren wird.
