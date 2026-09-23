# TB-95 — „Testannahmen folgen dem Register": `G6` und `H3` ausmessen und anpassen — und Fables Messbitte zu den neun Handelslisten

**Sitzungstitel:** `TB-95` · **Angelegt:** 23.09.2026 vom steuernden Chat
**Grundlage:** `FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md` (Abschnitt 2, der
neue Planpunkt) und `FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md`
(Abschnitte 5 und 6)
**Vorgänger:** TB-94 (Registerabschnitt 39). ⚠️ **TB-94 muss abgegeben sein.**
**Aufwand:** hoch.

---

## ⭐⭐ Worum es geht

`test_vorregistrierung.py` läuft seit TB-92 zum ersten Mal **bis zur
Schlusszeile** durch. Zwei von 165 Prüfungen scheitern: `G6` und `H3`. Beide
haben nach Fables Erwartung dieselbe Ursache — **Faltennamen als Literale im
Test**, während der registrierte Faltenplan seit TB-56/61/72 Doppeljahre führt.

Fable, **23a Abschnitt 2**, zeichengleich — der Planpunkt, der hier abgearbeitet
wird:

> **Neuer Planpunkt vor dem Tag — „Testannahmen folgen dem Register":** `test_vorregistrierung.py` ist der Nachweis von Abschnitt 12 („150 Prüfungen, acht Mutationsproben"). Jede Prüfung, deren Annahme dem Register hinterherhinkt, wird an das Register angepasst — nie umgekehrt, und nie gelöscht. Für G6: Faltennamen kommen aus dem Faltenplan (Abbild 33.3), nicht als Literale `"2020"`, `"2022"`. Für H3: Eine Mutationsprobe, die nicht mehr beisst, wird so gestellt, dass sie **mit der registrierten Faltenzahl** beisst (und die Mutationsprobe selbst bleibt Pflicht — eine Probe, die immer besteht, ist keine). **Tag-Vorbedingung nach 21.9 und A4: null rote Prüfungen, null „bekannt rot".**

Und seine Regel dazu, **23a**, zeichengleich:

> Prüfungen und Werkzeuge, die Falten kennen müssen, beziehen sie aus dem Abbild des Faltenplans (33.3) oder aus `faltenplan.py` — **nie als Literale**. Das ist Handwerk in der Umsetzung, aber Verfahren im Grundsatz: Ein Literal ist eine Kopie des Registers im Code, und Kopien altern.

⚠️ **23f Abschnitt 5, zeichengleich — und der Satz, der diesen Auftrag begrenzt:**

> Erwartung nach den Meldetexten: G6 ist die Doppeljahr-Klasse, H3 die Faltenzahl-Klasse — aber **Erwartung ist keine Messung; der Auftrag misst.**

⇒ **Block A misst, bevor Block B ändert.** Bestätigt die Messung die Erwartung
nicht, wird **nicht** geändert, sondern gemeldet.

---

## ⛔ Was in diesem Auftrag NICHT geschieht

| | |
|---|---|
| ⛔ | **Keine Prüfung wird gelöscht oder abgeschwächt.** Fable: „nie gelöscht". Eine Probe, die immer besteht, ist keine |
| ⛔ | **Der Faltenplan wird nicht geändert**, weder `faltenplan.py` noch `ergebnisse/faltenplan.json`. ⭐ *Der Test folgt dem Register, nie umgekehrt* |
| ⛔ | **`auswertung.py`, `registerdaten.py`, `benchmark.py`, `registerbericht.py` werden nicht geändert** — sie stehen auf der Sperrliste (Punkte 3/4/5/6/14) |
| ⛔ | **Kein neues Abbild** — `test_vorregistrierung.py` und `beispieldaten.py` stehen auf **keinem** Sperrlistenpunkt (gemessen in TB-92/TB-94). Ändert sich trotzdem ein Sperrlistenhash, **abbrechen** |
| ⛔ | **Der Registerabschnitt wird nicht geschrieben.** Dieser Auftrag misst und ändert Testcode; der Registereintrag ist der nächste Schritt und braucht Fables Kenntnisnahme |
| ⛔ | **`messgroessen.json` wird nicht angefasst** (TB-96) |

---

## 0. Schritt 0

Arbeitsbaum committen, `find .git -name '*.lock'` → keine, Arbeitsbaum leer.
HEAD muss die TB-94-Abgabe sein. **Ist Abschnitt 39 nicht im Register, brich ab.**

---

## Block A — Messen: woran scheitern `G6` und `H3` wirklich?

⭐ **Alles in diesem Block ist lesend.** Keine Datei wird geändert.

### A1 — Der Ist-Stand aus dem Register

Lies den **registrierten** Faltenplan — aus `ergebnisse/faltenplan.json`
(`0e54ac5c…`, Sperrlistenpunkt 2, **nur lesen**) — und stelle je Bot fest:

| | |
|---|---|
| die Namen aller Falten, in Reihenfolge | |
| welche `rolle` jede trägt (`selektion` / `bestaetigung`) | |
| die **Zahl** der Falten je Bot | |
| welche Kalenderjahre eine Falte abdeckt | ⭐ die Sachfrage hinter G6 |

Beleg: `a1_faltenplan_ist.txt`. ⚠️ **Sichtschutz 27.1: Faltennamen und
Faltenzahlen sind Verfahrensseite und dürfen an Fable — keine Ergebnisgrössen
des Selektionsraums nennen.**

### A2 — `G6` ausmessen

Die Prüfung lautet heute (Z. 494–496):

```python
namen = [f["name"] for f in p["falten"]]
pruefe(f"G6: {bot} - 2020 und 2022 sind Testfalten, keine Trainingsjahre",
       "2020" in namen and "2022" in namen, str(namen))
```

**Miss und schreibe auf:**

| | |
|---|---|
| **A2-1** | Für **welche** Bots schlägt `G6` fehl? Erwartet: nur `elliott_wave` (Meldetext TB-92: `['2018-2019', '2020-2021', '2022-2023', '2024-2025', '2026-01-01/2026-09-01']`). ⚠️ Sind es mehr, ist die Ursache eine andere |
| **A2-2** | Ist die **Sache**, die G6 prüfen will, erfüllt — sind die Jahre 2020 und 2022 bei jedem Bot von einer Falte der Rolle `selektion` abgedeckt? ⭐ *Das ist die entscheidende Messung: Wenn ja, ist nur die Formulierung veraltet. Wenn nein, ist es ein **Befund am Plan**, und dann wird hier nichts geändert, sondern gemeldet* |
| **A2-3** | Woher stammt das Literal? Steht der Satz „2020 und 2022 sind Testfalten" so im Register, und **wo**? Gib Abschnitt und Zeile an (Zeilennummer nur mit Commit, 38.2) |
| **A2-4** | Welche Stelle im Register ist die **richtige Quelle** für diese Prüfung — 33.2 (der Plan), 33.3 (das Abbild), oder ein Satz über Trainings- und Testjahre? |

Beleg: `a2_g6.txt`.

### A3 — `H3` ausmessen

Die Probe setzt heute vier Falten auf null Trades (Z. 590):

```python
ohne = {"2019", "2020", "2021", "2022"}
```

**Miss und schreibe auf:**

| | |
|---|---|
| **A3-1** | Welcher Bot ist `BOT` in diesem Test, und **wie viele** Falten hat er nach dem registrierten Plan? |
| **A3-2** | ⭐ **Wie viele der vier Namen in `ohne` treffen überhaupt eine Falte dieses Bots?** Erwartet: **null** — dann bekommt keine Falte eine gesetzte Null, die Mutation ändert nichts, und die Probe besteht scheinbar nicht mehr, weil sie nicht mehr **beisst** |
| **A3-3** | Der Meldetext von TB-92 war `'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'` — **beide Seiten gleich**. Bestätige das oder widerlege es |
| **A3-4** | ⭐⭐ **Ab wie vielen Null-Falten verschiebt sich der Median bei der registrierten Faltenzahl?** Der Kommentar im Test (Z. 583–589) begründet die Vier mit „sieben Falten". Hat der Bot heute weniger Falten, ist die Vier womöglich zu gross **oder** zu klein. **Rechne es aus, rate es nicht** — und schreib die Rechnung in den Beleg |
| **A3-5** | Gilt für `H3` dasselbe wie für `G6` — ist auch `ohne` ein Literal, das aus dem Plan kommen müsste? |

Beleg: `a3_h3.txt`.

### A4 — Suche nach weiteren Literalen derselben Klasse

⭐ **Fable nennt G6 „die zweite Instanz derselben Fehlerklasse" (die erste war
die Bestätigungsfalte). Such die dritte, bevor sie dich sucht.**

Durchsuche `test_vorregistrierung.py` **und** `beispieldaten.py` nach
Jahresliteralen in Faltenzusammenhängen (`"2017"`–`"2027"`, `"2018-2019"`,
`"2026-2027"`, `"2026"` …). Für jeden Treffer: Zeile, Prüfungsname, und ob er
heute zufällig noch passt.

⚠️ **Eine Prüfung, die heute grün ist, weil ihr Literal zufällig noch stimmt,
ist genauso kaputt wie eine rote** — sie sagt es nur noch nicht. Liste sie,
**ändere sie in diesem Auftrag aber nur**, wenn die Änderung dieselbe Bauart hat
wie die von G6 und H3. Alles andere kommt als Liste ins Ergebnisdokument.

Beleg: `a4_literale.txt`.

---

## Block B — Anpassen: der Test folgt dem Register

⚠️⚠️ **Nur ausführen, wenn A2-2 „ja" ergibt** (die Sache stimmt, nur die
Formulierung ist veraltet). Ergibt A2-2 „nein", **überspringe Block B**, melde
den Befund am Plan und geh zu Block D.

### B1 — `G6` aus dem Plan statt aus Literalen

**Was die Prüfung sagen soll, unverändert in der Sache:** die Jahre, die das
Register als Testjahre führt, sind bei jedem Bot von Selektionsfalten abgedeckt.

**Wie sie es prüfen soll:** die Jahre kommen aus dem Register (A2-4), die Falten
aus dem Plan (`p["falten"]`, Rolle `selektion`), die Abdeckung wird **gerechnet**
— eine Falte `2020-2021` deckt 2020 und 2021 ab. ⛔ **Kein `in namen` auf
Zeichenketten mehr.**

| | |
|---|---|
| ⭐ | Der Prüfungsname `G6` **bleibt** und bleibt an derselben Stelle. Der Text darf die neue Formulierung nennen |
| ⭐ | Die Ausgabe bei Fehlschlag muss **weiter die Faltennamen zeigen** — sonst ist der nächste Befund nicht lesbar |
| ⚠️ | Deckt eine Falte der Rolle `bestaetigung` eines der Jahre ab, ist das **kein** Treffer. Nur `selektion` |

### B2 — `H3` beisst wieder

**Was die Probe nachweist, unverändert:** ohne die Regel „Netto-Sharpe = 0 für
Falten ohne Trade" ändert sich die Selektionsstatistik.

**Was sich ändert:** die Menge `ohne` wird **aus dem Plan des Bots** gebildet —
so viele Selektionsfalten, wie nach A3-4 nötig sind, damit der Median sich
verschiebt, und zwar über ihre **tatsächlichen Namen**, nicht über geratene.

| | |
|---|---|
| ⭐⭐ | **Die Probe muss nachweislich beissen.** Nach der Änderung: einmal mit der Regel, einmal ohne — die beiden Statistikzeilen müssen **verschieden** sein. Zeig beide im Beleg |
| ⭐ | **Und sie muss aus dem richtigen Grund beissen.** Gegenprobe: Lässt man `ohne` leer, muss die Probe **fehlschlagen** (weil nichts sich ändert). Tut sie das nicht, prüft sie etwas anderes als gedacht |
| ⚠️ | Bleibt der Kommentar Z. 583–589 stehen, muss er die neue Zahl nennen. Ein Kommentar, der „vier bei sieben Falten" sagt, während im Code etwas anderes steht, ist die nächste alternde Kopie |

### B3 — Was du dabei nicht tun darfst

| | |
|---|---|
| ⛔ | Keine Prüfung entfernen, keine `continue`-Ausnahme für einen Bot einbauen. ⭐ *Fable 23b: „Eine Wache mit Ausnahme für den einen Fall, der ihr widerspricht, ist keine Wache"* |
| ⛔ | Keine Toleranz einbauen („fast gleich genügt") |
| ⛔ | `auswertung.py` nicht anfassen — auch nicht die Zeichenkette, die `_ersetze` in Z. 596–599 sucht. ⚠️ **Prüfe, dass sie im heutigen `auswertung.py` noch genau einmal vorkommt**; TB-92 hat die Datei geändert. Kommt sie nicht mehr vor, ist das ein **eigener Befund** und `H3` scheitert aus einem zweiten Grund |

---

## Block C — Der ganze Test, am echten Stand

```
trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py
```

⚠️ **Rechne mit rund 500 Sekunden** (TB-92: 501 s). Lass ihn **vollständig**
laufen, in einem Zug, am echten Stand — nicht in einer Wegwerf-Kopie.

| erwartet | |
|---|---|
| Schlusszeile erreicht | ja |
| Ergebnis | ⭐ **165 bestanden, 0 gescheitert**, `rc 0` |
| ⚠️ Zahl der Prüfungen | war 165 (163 + 2). Ist sie jetzt anders, **sag warum** — eine Prüfung mehr ist gut, eine weniger ist ein Befund |

⚠️⚠️ **Wird eine dritte Prüfung rot, die vorher grün war, hast du etwas
gebrochen.** Melde sie, nimm die Änderung zurück, die sie verursacht hat, und
gib den Stand so ab. **Nicht daran weiterreparieren.**

⛔ **Grün ist Tag-Vorbedingung, nicht Erfolgsbedingung dieses Auftrags.** Bleibt
etwas rot, ist der Auftrag trotzdem abgearbeitet — wenn die Ursache gemessen und
aufgeschrieben ist.

**Danach, zur Kontrolle:** Hashes der Sperrlistendateien vor und nach dem Lauf.
⛔ **Keiner darf sich geändert haben.** Und die Sonde gegen das neueste Abbild
(aus TB-94) — erwartet `0`.

Beleg: `c_test.txt`, `c_hashes.txt`, `c_sonde.txt`.

---

## Block D — ⭐⭐ Fables Messbitte: die neun Handelslisten

**23f Abschnitt 6, zeichengleich:**

> **Messbitte, nur das Ob:** Welcher Schritt des Modus-Laufs öffnet die neun Trade-Listen — `benchmark.py` selbst, oder ein Nebenweg (`registerdaten.py`, `faltenplan.py`, Trockenlauf)? Und **gehen ihre Inhalte in die Tabelle ein** — oder werden sie nur geöffnet (etwa für eine Konsistenzprüfung)? Wenn sie eingehen, hat die Benchmark-Tabelle eine Eingabe, deren Eingabestand nicht registriert ist — derselbe Fall wie `messgroessen.json`, und die Regel aus 23d gilt für sie. Wenn sie nur geöffnet werden, ist es eine Tatsachennotiz und ein Kandidat für die Lesequellen-Sonde.

Die Dateien sind `research/tb24_haltedauern/daten/*_alle_trades.csv`, neun Stück.
TB-92 hat sie mit dem Lesehaken (`sys.addaudithook`, `sitecustomize`, 11
Prozesse) beim Modus-Lauf gesehen und notiert: *„über den Faltenplan"*.

### D1 — Wer öffnet sie

⭐ **Statisch zuerst, das ist billig:** Such im Quelltext, welche Datei den Pfad
`tb24_haltedauern` oder `_alle_trades` nennt — `benchmark.py`, `faltenplan.py`,
`faltenplan_neun.py`, `registerdaten.py`, `messgroessen.py`,
`universum_trockenlauf.py`, `loaderlauf.py`. Nenne Datei, Zeile und Funktion.

⭐ **Dann dynamisch, weil statisch nicht beweist, dass der Weg auch begangen
wird:** Nimm den Lesehaken aus TB-92 (`docs/belege/TB-92/`), ergänze ihn um den
**Aufrufstapel** beim Öffnen (`traceback.extract_stack()`), und lass **einen**
Modus-Lauf laufen.

⚠️⚠️ **Der Lauf schreibt mit `--ziel` in den Scratchpad, niemals nach
`ergebnisse/`.** Der Hash muss `64fb2912…` sein — ⭐ **das ist zugleich die
fünfte Wiederholung des Determinismusnachweises.** Ist er es nicht, ist das ein
**Befund** und geht allem anderen vor.

### D2 — Ob die Inhalte eingehen

⭐ **Die Frage ist beantwortbar, ohne eine Zahl zu nennen** (Sichtschutz 27.1):

| Weg | was er zeigt |
|---|---|
| **(a) Datenfluss lesen** | Wird das Ergebnis des `read`/`read_csv` in einen Wert überführt, der in der Tabelle landet — oder nur gezählt, geprüft, verworfen? |
| **(b) ⭐⭐ Störprobe** | Kopiere den Datenordner in den Scratchpad, **verändere** eine der neun Listen dort (eine Zeile entfernen genügt), lass den Lauf gegen die Kopie laufen und vergleiche den Hash der Ausgabe. **Ändert er sich, gehen die Inhalte ein. Ändert er sich nicht, tun sie es nicht.** ⛔ Die Originale bleiben unberührt — prüfe ihre Hashes vorher und nachher |

⭐ *(b) ist der stärkere Nachweis, weil er nicht vom Lesen des Codes abhängt.
Mach beides und melde beide Ergebnisse; widersprechen sie sich, ist **das** der
Fund.*

### D3 — Die Antwort formulieren

Als kurzer Abschnitt, der **ohne** weiteren Kontext lesbar ist, für Fable:

| | |
|---|---|
| Welcher Schritt öffnet sie (Datei, Funktion, über welchen Weg) | |
| Gehen die Inhalte ein — **ja / nein / nicht entscheidbar**, mit dem Nachweis | |
| Falls ja: Was ist ihr Eingabestand? Liegen sie im Snapshot? (TB-92: **nein**) Wann und von welchem Commit stammen sie? | |
| Falls nein: Wozu werden sie geöffnet? | |
| ⚠️ Ist es **nicht entscheidbar**, sag das. `A2`: „konnte nicht messen" ist ein eigenes Ergebnis | |

⭐ **Und die eine Frage, die Fable selbst offen lässt:** Sind es die
**TB-24-Listen** (dann alter Code, alter Datenstand, 26.5)? Miss es am Pfad, am
Commit und am Datum — nicht am Namen.

Beleg: `d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d3_antwort.md`.

---

## Block E — Abgabe

**E1 — Ergebnisdokument** `docs/ERGEBNIS_TB-95_testannahmen_und_lesehaken.md`,
Bauart wie TB-92, mit:

| | |
|---|---|
| der Messung aus Block A **vor** der Änderung aus Block B | ⭐ damit später nachvollziehbar ist, was geändert wurde und warum |
| der Liste der weiteren Literale aus A4 | auch derer, die heute noch grün sind |
| dem Testergebnis aus Block C, mit Zahl und Laufzeit | |
| ⭐⭐ der Antwort auf Fables Messbitte (D3), **so formuliert, dass sie unverändert in eine Anfrage an ihn übernommen werden kann** | |
| einem Vorschlag für den Registertext, **gemessen, nicht eingetragen** | der Eintrag ist der nächste Auftrag |
| „In einfacher Sprache" | |

**E2 — Hashes vorher/nachher** für `test_vorregistrierung.py` und alle
Sperrlistendateien. ⛔ Nur die erste darf sich geändert haben.

**E3 — Journalblock.**

**E4 — Commits:** (1) Schritt 0 · (2) Block B (Testanpassung) · (3) Block D
(Messung, Belege) · (4) Abgabe.

---

## ⚠️ Abbruchkriterien

1. **Abschnitt 39 fehlt im Register** — TB-94 ist nicht abgegeben.
2. **A2-2 ergibt „nein"** — die Sache hinter G6 stimmt nicht. Dann ist es ein
   Befund am Plan, nicht am Test: Block B überspringen, melden.
3. **Die Zeichenkette in `_ersetze` (H3) kommt in `auswertung.py` nicht mehr
   genau einmal vor** — melden, nicht suchen und ersetzen.
4. **Ein Sperrlistenhash ändert sich.**
5. **Eine dritte Prüfung wird rot** — die verursachende Änderung zurücknehmen,
   so abgeben.
6. **Der Modus-Lauf in D1 liefert nicht `64fb2912…`** — alles stehen lassen und
   melden. Das wäre ein Determinismusbefund und wiegt schwerer als dieser
   Auftrag.

---

## In einfacher Sprache

Das Prüfprogramm hat 165 Prüfungen. Zwei schlagen fehl, und zwar vermutlich aus
demselben Grund: Sie haben Jahreszahlen fest eingetippt, damals, als die
Zeitabschnitte noch einzelne Jahre hiessen. Inzwischen sind es Doppeljahre —
„2020-2021" statt „2020" —, und die eingetippten Zahlen treffen nichts mehr.

**Die erste Prüfung** fragt, ob bestimmte Jahre als Testabschnitte geführt
werden. Sie sucht wörtlich nach „2020" und findet nichts. Sie soll künftig
ausrechnen, welche Jahre ein Abschnitt abdeckt, statt Namen zu vergleichen.

**Die zweite** ist eine Gegenprobe: Sie schaltet absichtlich eine Regel ab und
schaut, ob sich das Ergebnis ändert. Tut es das nicht, wäre die Regel
wirkungslos. Sie setzt dafür vier Zeitabschnitte auf „keine Geschäfte" — und
trifft mit den alten Namen keinen einzigen. Die Probe „beisst" deshalb nicht
mehr; sie besteht nicht, weil alles in Ordnung ist, sondern weil sie ins Leere
greift. Sie soll ihre Abschnitte künftig aus dem eingetragenen Plan nehmen, und
zwar so viele, dass sich das Ergebnis messbar verschiebt.

⭐ **Wichtig ist die Reihenfolge:** erst messen, ob die Vermutung stimmt, dann
ändern. Stellt sich heraus, dass die Jahre tatsächlich nicht abgedeckt sind,
dann liegt der Fehler nicht im Prüfprogramm, sondern im Plan — und dann wird
nichts geändert, sondern gemeldet. Gesucht wird ausserdem nach weiteren
eingetippten Jahreszahlen, auch solchen, die heute noch zufällig passen.

**Der zweite Teil** beantwortet eine Frage des Verfahrensprüfers. Beim
Vergleichslauf wurde beobachtet, dass neun Handelslisten geöffnet werden, die
nicht zum eingefrorenen Datenbestand gehören. Zu klären ist, wer sie öffnet und
ob ihr Inhalt in das Ergebnis einfliesst. Der sauberste Nachweis dafür ist eine
Störprobe: eine Kopie der Liste verändern und schauen, ob sich das Ergebnis
mitverändert. Die Originale bleiben dabei unangetastet.
