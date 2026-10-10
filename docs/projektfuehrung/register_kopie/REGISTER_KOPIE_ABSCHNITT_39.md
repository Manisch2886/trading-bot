# REGISTER-KOPIE Abschnitt 39 (von 0–56) — Register-Z. 7647–8167 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 39. Der Vollzug von Sperrlistenpunkt 4 im Register — Berichtigung des Fertigkriteriums in 38.4, Form (ii) vollzogen, Determinismus- und Modus-Nachweis, fünf Hash-Übergänge nach 37.3, zwei Eingaben ohne registrierten Eingabestand und das neue Abbild (Fable 23a–23f, TB-94, 23.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 38. Der
Vollzug von Plan-Punkt 8 ist **im Code** seit `0292e92` (TB-92) erbracht und
belegt; TB-92 hat danach **richtig abgebrochen**, weil 38.4 „grün" verlangte.
Dieser Abschnitt trägt den Vollzug **ins Register** nach: die Berichtigung des
Fertigkriteriums in 38.4 (39.1), den Vollzug der Form (ii) an Punkt 4 (39.2),
die Tatsachennotizen zu `_vt.json` und `_tb72.json` (39.3), den
Determinismusnachweis (39.4), die fünf Hash-Übergänge nach 37.3 (39.5), den
Modus-Nachweis (39.6), die Tatsachennotiz zu `herkunft.py::EINGEFROREN`
(39.7), die zwei Eingaben ohne registrierten Eingabestand (39.8), das neue
Abbild (39.9) und den Schlussteil (39.10). Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md`, `…23b_neurechnung_nach_a.md`,
`…23c_messgroessen_und_vollzug.md`, `…23d_dritte_leserin_und_eingabestand.md`,
`…23e_nachweislauf_im_modus.md`, `…23f_fertigkriterium_38_4.md` und
`…22g_sonde_vor_dem_tag.md` — **eingesetzt, nicht abgetippt** (Beleg
`docs/belege/TB-94/e2_zitate.txt`, je Zitat `diff` rc 0). Auftrag
`docs/auftraege/MAC_TB-94_register_39.md`; Belege `docs/belege/TB-94/`; Eingang
`fcc3265`, Schritt-0-Commit `12f6089`. Messungen der Vorgänger: TB-91
(`docs/ERGEBNIS_TB-91_benchmark_absichern_und_neurechnung.md`, Belege
`docs/belege/TB-91/`) und TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Belege `docs/belege/TB-92/`), in TB-94 an den Belegen und an den Hashes
nachgemessen (`a1_hashes.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 39.10.

⭐ **Zum Zwischenstand zwischen `fcc3265` und diesem Eintrag** (Repo vollzogen,
Register nicht), Fable 23f Abschnitt 3, zeichengleich:

> **Zum Zwischenzustand über Nacht:** Er ist zulässig, weil er **benannt** ist — diese Anfrage und diese Antwort liegen beide in der Ablage, der Commit `fcc3265` ist der Stand, und der Registerauftrag ist der nächste Schritt. Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag. Nichts zurücknehmen.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Abschnitt 10
Punkt 4; 38.4 zweimal; 21.9; 38.7 (d); 37.2; 37.3; 23.7; 33.2; 37.4 — zehn).
Die alten Sätze bleiben zeichengleich — **auch der Satz mit „grün" in 38.4**;
`git diff --numstat` auf dieses Register zeigt für TB-94 in der zweiten Spalte
`0`. ⭐ **Neu gegenüber 34–38:** Punkt 4 in Abschnitt 10 bekommt eine
**Pfadzeile** — drei eingerückte Folgezeilen **nach** der Zeile
`   Interpolationsregel**`, die vier Zeilen davor zeichengleich. Das ist der
Vollzug selbst (39.2), keine Marke; er ist additiv, weil die Sperrliste nach
Form (ii) nichts streicht. Fundstellen stehen nach 38.2 als Datei und
Bezeichner; Zeilennummern nur in Tatsachennotizen, mit Commit.

### 39.1 ⭐⭐ Berichtigung zu 38.4 — das Fertigkriterium von Plan-Punkt 8

⚠️ **Der Anlass:** 38.4 trägt als Fertigkriterium Fables Satz aus **22h**
(„`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —"). Fable
hat dieses Kriterium in **23a** zurückgenommen und ersetzt; **die Rücknahme ist
nie als Ersatztext an 38.4 eingetragen worden.** TB-92 hat sich an das
Register gehalten: Der Test lief bis zur Schlusszeile, war aber **163/2**
(`G6`, `H3`) — nicht grün —, und TB-92 hat abgebrochen, statt zwischen
Register und Antwortdatei zu wählen (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 3). ⭐ **Das war das richtige Verhalten und wird hier ausdrücklich so
festgehalten.**

**Fable, 23f Abschnitt 2, zeichengleich — der Befund an sich selbst:**

> Der Widerspruch ist meiner, und er hat eine einfache Geschichte: 38.4 trägt meinen Text aus **22h** („grün — die roten Prüfungen misst TB-88"). **23a** hat dieses Kriterium ausdrücklich zurückgenommen — „Mein Satz ‚fertig, wenn `test_vorregistrierung.py` grün' hat zwei Dinge vermischt: eine Tag-Vorbedingung und ein Fertigkriterium für einen Punkt" — und ersetzt: fertig, wenn der Absturz weg ist und der Test bis zur Schlusszeile läuft; G6/H3 eigener Punkt. 23d hat das wiederholt. **Was fehlt, ist die Berichtigung von 38.4 im Register** — 23a ist als Antwort abgelegt, aber nie als Ersatztext an 38.4 eingetragen worden. Die Mac-Sitzung hat den Registertext gelesen, nicht meine Antwortdatei, und das ist richtig so: **Für eine ausführende Sitzung gilt das Register, nicht Fable.** Der Fehler liegt darin, dass 23a eine Berichtigung enthielt, ohne sie als solche zu adressieren; ich habe „Fertigkriterium" geschrieben und nicht „Berichtigung zu 38.4".

⭐ **Die Rangfolge, die daraus folgt, zeichengleich:** *„Für eine ausführende Sitzung gilt das Register, nicht Fable."*

**Der Ersatztext, zeichengleich:**

> **Berichtigung zu 38.4, Ersatztext (aus 23a, zeichengleich in der Sache):** Punkt 8 ist fertig, wenn: Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, alle drei Leser (`auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`) lesen die vollzogene Tabelle über eine Konstante, der Absturz ist weg und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, Modus-Nachweis bytegleich (23e), neues Abbild, Sonde 0 für die Pfade. **Der Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8.** „Null rote Prüfungen" ist Tag-Vorbedingung (21.9, A4) und wird durch den eigenen Punkt „Testannahmen folgen dem Register" erreicht. Der Einschub „die roten Prüfungen misst TB-88" in der alten Fassung war der Hinweis in diese Richtung; das Wort „grün" davor war der Fehler.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23a, Abschnitt 2 — ein Fertigkriterium hängt an dem, was der Punkt ändert; sonst haftet ein Punkt für fremde Fehler und wird nie fertig. Kein Ergebnis.

**Seine Regel an sich selbst, zeichengleich:**

> **Und eine Regel für mich, damit das nicht wieder passiert:** Wenn eine Antwort von mir einen Registertext ändert, den eine frühere Antwort gesetzt hat, **nennt sie ihn als Berichtigung mit Abschnittsnummer** — nicht als neue Entscheidung. Eure Regel „nicht übernehmen, nachmessen" gilt für meine Texte gegen das Register genauso wie für eure gegen den Code.

**Die Entscheidung in 23a, auf die der Ersatztext zurückgeht, zeichengleich**
(Abschnitt 2 — die Entscheidung und der neue Planpunkt):

> **Punkt 8 ist fertig, wenn:** Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), **der Absturz (`KeyError` an der Faltenzuordnung) ist weg** und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, neues Abbild, Sonde 0 für die Pfade. Der Ausgang der einzelnen Prüfungen ist nicht Fertigkriterium von Punkt 8.
>
> **Neuer Planpunkt vor dem Tag — „Testannahmen folgen dem Register":** `test_vorregistrierung.py` ist der Nachweis von Abschnitt 12 („150 Prüfungen, acht Mutationsproben"). Jede Prüfung, deren Annahme dem Register hinterherhinkt, wird an das Register angepasst — nie umgekehrt, und nie gelöscht. Für G6: Faltennamen kommen aus dem Faltenplan (Abbild 33.3), nicht als Literale `"2020"`, `"2022"`. Für H3: Eine Mutationsprobe, die nicht mehr beisst, wird so gestellt, dass sie **mit der registrierten Faltenzahl** beisst (und die Mutationsprobe selbst bleibt Pflicht — eine Probe, die immer besteht, ist keine). **Tag-Vorbedingung nach 21.9 und A4: null rote Prüfungen, null „bekannt rot".** (3) ist damit ausgeschlossen, wie ihr sagt.

**Der Grund in 23a, zeichengleich:**

> Mein Satz „fertig, wenn `test_vorregistrierung.py` grün" hat zwei Dinge vermischt: eine **Tag-Vorbedingung** (21.9: der Test blockiert den Tag, solange er rot ist) und ein **Fertigkriterium für einen Punkt**. Das Fertigkriterium eines Punktes muss an dem hängen, was der Punkt ändert — sonst wird ein Punkt nie fertig, weil er für fremde Fehler haftet.

⇒ **Was ab hier gilt:**

| | |
|---|---|
| Fertigkriterium von Plan-Punkt 8 | der **Ersatztext oben** (23f/23a). Der Satz in 38.4 („`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —") bleibt **zeichengleich** stehen und trägt eine ERSETZT-Marke |
| Die offene Frage in 38.7 (d) („bleibt ‚grün' Fertigkriterium?") | **beantwortet** — Lesart (1) der Anfrage 22i: fertig, wenn der Absturz weg ist; `G6`/`H3` sind ein eigener Punkt |
| 21.9, Tabelle der Folgen, erste Zeile („bleibt **rot** … offen durch eigene Änderung — blockierend für den Tag") | **gilt unverändert für den Tag.** „Null rote Prüfungen, null ‚bekannt rot'" ist Tag-Vorbedingung (23a); sie wird mit dem Planpunkt „Testannahmen folgen dem Register" erreicht (`G6`, `H3`; TB-95), nicht mit Punkt 8 |

**Tatsachennotiz — was TB-92 gemessen hat (`docs/belege/TB-92/b1_ausgabe.txt`,
HEAD `0292e92`):** `trading-env/bin/python3
research/vorregistrierung/test_vorregistrierung.py` — Teil A bis H
durchlaufen, **Schlusszeile erreicht**, der `KeyError: '2017'` ist weg; **163
bestanden, 2 gescheitert** (`G6`, `H3`), rc `1`, 501 s. `G6` und `H3` werden in
diesem Abschnitt **weder gemessen noch erklärt noch angepasst** (TB-95).

**Marken am alten Ort:** bei **38.4**, direkt unter dem Zitat mit „grün"; bei
**21.9**, unter der Tabelle der Folgen; bei **38.7 (d)**, unter der offenen
Frage.

### 39.2 ⭐⭐ Vollzug von Sperrlistenpunkt 4 in Form (ii)

⭐⭐ **Der Punkttext von Abschnitt 10, Punkt 4, ist geändert — additiv.** Nach
der Zeile `   Interpolationsregel**` stehen drei neue Folgezeilen:

```
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
```

Die vier Zeilen davor und der Kasten aus 38.4 darunter sind zeichengleich; der
Kasten trägt jetzt die Vollzugsmarke. Punkt 4 nennt damit:

| Datei | Rolle | sha256 |
|---|---|---|
| `benchmark.py` | Erzeuger (Punkte 4 und 6), unverändert seit TB-91 | `d6bdd558…` |
| `ergebnisse/benchmark_drawdowns.json` | **registrierter historischer Stand**, gesperrt und byteweise unverändert — wie Punkt 2 (30.3) | `a163c498…` |
| `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | **die Tabelle, die der Lauf liest** | `64fb2912…` |

(Gemessen in TB-94 am Stand `12f6089`, `a1_hashes.txt`; volle Hashes dort und
in 39.5.)

**Die Bedingung, nach der diese Datei die Tabelle ist — Fable, 23a Abschnitt 3,
zeichengleich (Registertext zu Sperrlistenpunkt 4 / 23 / 33, die Wache und die
Folge für den Vollzug):**

> **Registertext zu Sperrlistenpunkt 4 / 23 / 33:** Die Benchmark-Tabelle, die der Lauf liest, ist auf dem registrierten Faltenplan (33.2) gerechnet: Für jeden Bot ist die Faltenmenge der Tabelle gleich der Menge seiner Selektionsfalten nach 33.2 (plus Bestätigungsperiode, sofern die Tabelle sie führt) — nicht mehr, nicht weniger —, und ihre Benchmark-Definition ist die aus 23 (tagesgenau). Eine Tabelle, die diese Bedingung für auch nur einen Bot nicht erfüllt, wird nicht vollzogen; sie bleibt liegen und erhält eine Tatsachennotiz, auf welchem Planstand sie gerechnet wurde.
>
> **Wache (in den Vollzug und in den Laufwrapper):** Faltenmenge der vollzogenen Tabelle je Bot gegen das Abbild des Faltenplans — Abweichung ist 1, fehlende Datei 2. Der `KeyError '2017'` von heute ist genau dieser Befund, nur als Absturz statt als Wache.
>
> **Folge für den Vollzug:** Es wird **eine** Tabelle für alle neun Bots vollzogen, keine Mischung. Welche Datei das ist, entscheidet die Bedingung, nicht der Name: Ist `benchmark_drawdowns_tb72.json` für alle neun Bots auf 33.2 gerechnet und tagesgenau nach 23, dann ist sie die Tabelle, und `_vt.json` erhält eine Tatsachennotiz als Zwischenstand (23, vor 25); die Gruppe „bestimmt" in 37.2 wechselt entsprechend. Erfüllt keine vorhandene Tabelle die Bedingung für alle neun, wird die Tabelle **einmal neu gerechnet** — mit `benchmark.py` (Punkt 4/6), auf dem Abbild des Faltenplans, mit Beleg und Hash, vor dem Tag.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23.7 („der Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle … wird mit demselben Amendment geschlossen") — geschlossen heisst: die Tabelle folgt dem Plan, nicht der Plan der Tabelle. Und 24.3 als Bauart: Die Regel steht hier, **bevor** ich weiss, welche Datei sie erfüllt; die Werte kenne ich nicht und brauche sie nicht. Kein Ergebnis.

**Und die Entscheidung, sie einmal neu zu rechnen — 23b Abschnitt 2,
zeichengleich:**

> **Ergänzung zu 23a, Abschnitt 3 (Registertext zu Sperrlistenpunkt 4):** Die Tabelle, die der Lauf liest, wird **nach** der Umsetzung von Weg (A) (Punkt 3, TB-90) **einmal** neu gerechnet — mit `benchmark.py` (Sperrlistenpunkt 4/6, unverändert), auf dem dann gültigen Plan, mit `--ziel` auf einen neuen Pfad nach der Schreibregel 36.1, mit Beleg und Hash. Ihre Bestätigungszeile trägt den Bezeichner nach 35 (`2026-01-01/2026-09-01`).

⇒ **Warum diese Datei und nicht `_vt.json`:** 23a hat die Bedingung gesetzt
(Faltenmenge je Bot gleich den Selektionsfalten nach 33.2, plus
Bestätigungsperiode; Benchmark tagesgenau nach 23; **keine Mischung** aus zwei
Tabellen), 23b hat entschieden, dass **einmal neu gerechnet** wird, und TB-91
hat sie gerechnet (`31008b6`, 39.4). ⭐ **Damit ist die zweite offene Frage aus
38.4 („welche Tabelle für `t3_supertrend`") beantwortet:** keine vorhandene —
die Neurechnung, für alle neun.

**Wie die drei Leser sie lesen — Fable, 23d Abschnitt 1, zeichengleich:**

> **Zu Sperrlistenpunkt 4, Vollzug, Schritt 1a:** `auswertung.py` liest die vollzogene Tabelle über **eine** Konstante am Modulanfang, deren Wert der registrierte Pfad der neuen Tabelle ist. **Kein Kommandozeilenschalter** — Abschnitt 12 sagt „`auswertung.py` hat keinen Schalter", und eine Option, die bestimmt, welche Tabelle gilt, wäre einer. Bedingungen: AST-Vergleich aller Funktionskörper unverändert; genau eine Zuweisung verändert (die Pfadkonstante); `test_vorregistrierung.py` und `beispieldaten.py` lesen dieselbe Konstante, damit Test und Lauf nicht auseinanderfallen können; Tatsachennotiz mit altem und neuem Hash von `auswertung.py`. Die Änderung geschieht in demselben Auftrag wie der Vollzug (TB-92), nicht danach.

**Tatsachennotiz — umgesetzt in TB-92, `0292e92`
(`docs/belege/TB-92/a1a_ast_vergleich.txt`, `a5_hashes_nachher.txt`):**
`research/vorregistrierung/auswertung.py` trägt **eine** Konstante
`BENCHMARK_TABELLE` (Pfad der Neurechnung), `main` öffnet sie; ⛔ **kein
Schalter** (Abschnitt 12). AST-Vergleich: 27 Funktionen und Klassen, **26
gleich**, verschieden nur `main` und dort nur im Argument von `open`; auf
Modulebene **genau eine neue Zuweisung** (`BENCHMARK_TABELLE`), keine entfernt.
`registerbericht.py` (Funktion `block`) und `test_vorregistrierung.py`
(Funktion `_tabellen`) lesen `aw.BENCHMARK_TABELLE`; `registerbericht.py` liest
dort den Schlüssel `symbole_handelbar_in_falte` (23.5) statt
`symbole_point_in_time` — der alte Schlüssel kam genau **einmal** vor.
⚠️ **`beispieldaten.py` liest keine Tabelle** (Hash `3e547014…` unverändert,
in TB-94 nachgemessen): Die vierte Leserin, die 23d („`test_vorregistrierung.py`
und `beispieldaten.py` lesen dieselbe Konstante") voraussetzt, gibt es nicht.
Repo-weit sind es **drei** Leser, wie TB-88 (38.4, Tatsachennotiz M5) gemessen
hat.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 4** (Vollzug); bei **38.4**,
am Ende (Form (ii) vollzogen).

### 39.3 Tatsachennotizen zu `_vt.json` und `_tb72.json` — und die Gruppe „bestimmt"

**Fable, 23b Abschnitt 2, zeichengleich:**

> `benchmark_drawdowns_vt.json` und `benchmark_drawdowns_tb72.json` bleiben unverändert liegen, erhalten je eine Tatsachennotiz (Planstand, auf dem sie gerechnet wurden; TB-66 bzw. TB-72) und kommen **nicht** auf die Sperrliste; die Gruppe „bestimmt" in 37.2 wechselt auf die neue Tabelle. Sperrlistenpunkt 4 nach Form (ii): `benchmark_drawdowns.json` als registrierter historischer Stand, die neue Tabelle als die, die der Lauf liest.

**Die Tatsachennotizen (in TB-94 nachgemessen, `a1_hashes.txt`):**

| Datei | gerechnet auf Planstand | Bestätigungszeile | sha256 | Sperrliste |
|---|---|---|---|---|
| `ergebnisse/benchmark_drawdowns_vt.json` | **TB-66** (tagesgenau nach 23, vor 25); `t3_supertrend` mit einer Falte `2018`, die der Plan seit TB-72 nicht mehr hat | alter Name (`2026` bzw. `2026-2027`) | `4549395f…` | ⛔ **nicht** |
| `ergebnisse/benchmark_drawdowns_tb72.json` | **TB-72** | alter Name (`2026` bzw. `2026-2027`) | `e4ba341d…` | ⛔ **nicht** |

Beide bleiben unverändert liegen. Die Neurechnung reproduziert `_tb72.json` in
allen Werten (39.4); `_vt.json` weicht von `_tb72.json` an **101** Blattwerten
ab (Selbsttest des Vergleichers, TB-91; Werte nach 27.1 nicht wiedergegeben).

⭐ **Folge für 37.2 (Gruppe „bestimmt"):** Die Gruppe nannte bisher
`ergebnisse/benchmark_drawdowns_vt.json`. Nach 23b **wechselt sie auf die neue
Tabelle** — und weil deren Pfad seit 39.2 in Punkt 4 steht, hat sie ihren
Punkt: **Die Gruppe „bestimmt" ist nach dem Registertext leer.** 37.2 verlangt
genau das für den Tag: *„Am Tag ist die zweite Gruppe leer."*

⚠️ **Tatsachennotiz — was die Sonde dazu meldet (TB-87 gemessen, in TB-94
nachgemessen):** Die Sonde führt die Gruppe nicht aus dem Abbild, sondern aus
einer **festen Konstante** in `shared/sperrlistensonde.py`
(`BESTIMMT_NICHT_EINGETRAGEN`, am Stand `12f6089` ein Eintrag:
`ergebnisse/benchmark_drawdowns_vt.json`, Begründungstext „Register
21.9/23.7 - fuer die Sperrliste bestimmt, Vollzug steht aus"); sie **nennt**
den Pfad, **prüft** ihn nicht (37.2, Tatsachennotiz TB-87). ⇒ Nach diesem
Eintrag und dem neuen Abbild meldet die Sonde dort weiter `_vt.json` mit
„Vollzug steht aus" — **das ist seit 39.2 sachlich überholt**, und die Sonde
kann es nicht wissen, weil die Konstante Code ist. ⛔ Die Sonde wird hier
**nicht** geändert (keine `.py`, 39.10). Die leere Gruppe ist Teil des
Sonden-Entwurfs aus TB-92 (`docs/belege/TB-92/sonde_je_datei_entwurf.patch`),
Handwerk mit eigener Freigabe. Was die Sonde nach dem neuen Abbild tatsächlich
ausgibt, steht in 39.9.

**Marke am alten Ort:** bei **37.2**, unter der Tatsachennotiz TB-87.

### 39.4 ⭐⭐ Determinismusnotiz — die Neurechnung reproduziert `_tb72.json` (TB-91, Bedingung aus 23b)

**Fables Bedingung, 23b Abschnitt 2, zeichengleich:**

> **Bedingung an die Neurechnung — der Determinismusnachweis:** Die neu gerechnete Tabelle muss `benchmark_drawdowns_tb72.json` für **alle neun Bots in allen Werten reproduzieren**; der einzige zulässige Unterschied ist der Name der Bestätigungszeile (und, sofern die Tabelle ihn führt, ein Feld, das diesen Namen wiederholt). Ein `diff`, der etwas anderes zeigt, ist ein **Befund**, kein Ergebnis: Dann hat sich zwischen TB-72 und TB-90 etwas bewegt, das nicht der Name ist — Plan, Daten oder Code —, und das ist vor dem Vollzug zu klären, nicht wegzurechnen. Die Tabelle wird in diesem Fall **nicht** vollzogen.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.1 (Bezeichner ist die Spanne, ein anderer ist unzulässig), 23a (Tabelle folgt dem Plan; Neurechnung dort schon vorgesehen), 36.1 (Schreibregel). Und die Bedingung ist 10.1 in Anwendung: Erlaubt sind nur Änderungen mit **bitidentischen** Ergebnissen — die Neurechnung ändert einen Namen, also müssen alle Zahlen gleich bleiben, und wenn sie es sind, ist das zugleich der Nachweis, dass `benchmark.py` deterministisch ist und der Plan sich seit TB-72 nicht bewegt hat (32 hat es behauptet; hier wird es an der Tabelle gemessen). **Kein Ergebnis:** Ich verlange Gleichheit mit einer Tabelle, deren Werte ich nicht kenne; ob sie „gut" oder „schlecht" sind, spielt für die Regel keine Rolle, und sie darf nach 27.1 auch nicht wiedergegeben werden — die Sonde meldet nur „gleich" oder „an Stelle X verschieden".

**Das Ergebnis (TB-91, `docs/belege/TB-91/c_determinismus_ergebnis.txt`,
`c_gegenprobe_text.txt`, `b_neurechnung_lauf.txt`; in TB-94 an den Belegen
nachgelesen) — ⚠️ ohne Werte, Sichtschutz 27.1:**

| | |
|---|---|
| Lauf | `trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`, `benchmark.py` `d6bdd558…`, HEAD `31008b6`, **rc 0, 56 s** |
| Vergleich | gegen `benchmark_drawdowns_tb72.json` (`e4ba341d…`), rekursiv bis zum Blatt, Typ **und** Wert: **9 Bots, 77 Falten, 63 Botfelder, 9750 Blattwerte** |
| Abweichungen | **0 ausser dem Namen der Bestätigungszeile** (9/9: `2026` bzw. bei `elliott_wave` `2026-2027` → `2026-01-01/2026-09-01`); `dd_toleranz` 9/9 gleich; `status` 9/9 `endgueltig` |
| Gegenprobe auf Textebene | `_tb72.json` geladen, Bestätigungsfalte umbenannt, mit `indent=1, ensure_ascii=False, sort_keys=True` und Schluss-`"\n"` geschrieben → sha256 `64fb2912…`, **bytegleich** mit der Neurechnung |
| ⭐ Selbsttest des Vergleichers | `_tb72` gegen sich selbst **0** Abweichungen; `_tb72` gegen `_vt` **101** — *ein Vergleich, der nichts finden kann, ist keiner* |
| ⭐ Die Wache aus 23a (TB-91 Block D, `d_falten_abgleich_ergebnis.txt`) | Faltenmenge der Tabelle je Bot gegen den Plan im Speicher (`faltenplan.py` `7aa0b8cc…`): **18/18 gleich** (9 Bots × zwei Einstufungen, alle und Selektion), Bestätigungszeile **9/9** gleich der `bestaetigungsperiode` des Plans. Keine Falte fehlt, keine ist zusätzlich |

⇒ **Damit ist Festlegung 32 an der Tabelle gemessen:** Zwischen TB-72 und
TB-91 hat sich an den Benchmark-Drawdowns nichts bewegt ausser dem Namen der
Bestätigungszeile — und `benchmark.py` ist in diesem Umfang deterministisch.

### 39.5 ⭐⭐ Tatsachennotizen zu 37.3 — die fünf Hash-Übergänge

37.3 verlangt für jeden planmässigen Befund vor dem Tag: Auftrag, Freigabe,
alter und neuer Hash. **Vier davon standen bisher nicht im Register.** Alle
fünf, mit **vollem** Hash, gemessen in TB-94 aus der Historie
(`git show <commit>^:<pfad>` bzw. `<commit>:<pfad>`, `a1_hashes.txt`); die
Freigaben aus den Auftragsdokumenten nachgelesen:

| Datei | alt → neu | Auftrag / Commit | Freigabe | Sperrlistenpunkte |
|---|---|---|---|---|
| `research/vorregistrierung/faltenplan.py` | `6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9` → `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` | TB-86, `4daa254` | Betreiber 22.09.2026, 07:50 | 2 — *bereits in 37.3 notiert* |
| `research/vorregistrierung/faltenplan.py` | `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` → `7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb` | TB-90 (Weg (A), 38.1), `303a7fd` | Betreiber 22.09.2026 (`MAC_TB-90`, Kopf) | 2 — **neu** |
| `research/vorregistrierung/benchmark.py` | `3960375a539de8324ccfafaa42596a056fb5dd5c154cd2e05c0ba6a634f3611b` → `d6bdd55805344da09b6b43d791267b43c9702687fc1c7cdbad1473079443e061` | TB-91 (nach 36.1 abgesichert), `31008b6` | Betreiber 23.09.2026, 10:40 | **4 und 6** — neu |
| `research/vorregistrierung/auswertung.py` | `1c2e2daec562d9973f87809fd29ef369db76614ee4bc31c04c6ca201c52a3db0` → `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` | TB-92 (39.2), `0292e92` | Betreiber 23.09.2026, 18:12, und Fable 23d | **3, 5 und 14** — neu |
| `research/vorregistrierung/registerbericht.py` | `2b1ce24a8f9b2ece8c98fe2aa84f1f5fdc6ac3da544c0aa765e381505bb1d78f` → `dace1b01826fa6a999beb9a15a8eda41a4e0c97dec584e451cfc0d9b26daac01` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |
| `research/vorregistrierung/test_vorregistrierung.py` | `55553739c819b78de2f7ac608af2341ec43b7c856c3e8699d5a6ffde67bd15c0` → `6e7defefb46903ccec8df60a350136f5961c137b45fb1a921407e7a8e76f3fbe` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |

Seit dem jeweiligen Commit hat sich keine der sechs Dateien bewegt (letzter
Commit je Datei = der genannte; Hashes am Stand `12f6089` = „neu").
⭐ **Nach 37.3 ist jeder dieser Befunde der planmässige Fall vor dem Tag** —
Auftrag, Freigabe, alter und neuer Hash stehen hiermit als Tatsachennotiz.
Geschlossen werden sie mit **einem** neuen Abbild (39.9); das alte bleibt.

⚠️ **Zählweise, damit niemand einen Widerspruch liest:** Die sechs Befunde der
Sonde gegen `sperrliste_abbild_2026-09-22.json` (Punkte 2, 3, 4, 5, 6, 14;
`docs/belege/TB-94/a2_sonde_vorher.txt`) stammen aus **drei** Dateien, nicht
aus sechs Änderungen: `faltenplan.py` an 2, `benchmark.py` an 4 und 6,
`auswertung.py` allein an 3, 5 und 14.

⭐ **Ein Fund aus TB-91, der nicht auf TB-91 beschränkt ist — Fables
Tatsachennotiz dazu, 23c Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu 36.5/37 (kein neuer Registertext):** Ein Punkt mit unmessbaren Bestandteilen wechselt von 2 auf 1, sobald ein messbarer Bestandteil abweicht (erstmals beobachtet TB-91: Punkte 4 und 6 durch `benchmark.py`, planmässig nach 37.3). Die Zahl der Punkte mit 2 ist keine Kenngrösse des Registers, sondern des jeweiligen Standes. Die Sonde meldet je Punkt; eine Datei, die an mehreren Punkten vorkommt, erzeugt eine Tatsachennotiz.

⇒ `A2` („konnte nicht messen ist ein eigenes Ergebnis") heisst **nicht** „bleibt
für immer unmessbar", und die Zahl der nicht prüfbaren Punkte ist keine feste
Grösse. Eine Bilanz mit mehr Punkten `1` ist deshalb nicht schlechter als eine
mit mehr Punkten `2`; sie zeigt nur, welche Dateien sich bewegt haben.

**Marke am alten Ort:** bei **37.3**, unter der Tatsachennotiz zu TB-86.

### 39.6 ⭐ Der Modus-Nachweis — die vollzogene Tabelle ist aus dem registrierten Snapshot bytegleich reproduzierbar (Fable 23e, TB-92 A1b)

**Fables Forderung, 23e Abschnitt 2, zeichengleich (Präzisierung zu 23d,
Registertext „Eingabestand"):**

> Der Reproduzierbarkeitsnachweis einer Eingabedatei wird **im Selektionsmodus** geführt — der Erzeuger liest aus `snapshots/<hash>/`, nicht aus `data/`, mit `--ziel` auf einen Beleg-Pfad; das Ergebnis muss bytegleich zur eingefrorenen Datei sein. Die Tatsachennotiz nennt Snapshot-Hash, Code-Commit und den Modus. Dass `data/` zum Messzeitpunkt bytegleich zum Snapshot war, ist eine eigene Tatsache und ersetzt den Modus-Lauf nicht: Der Lauf am Tag liest den Snapshot-Pfad, und der Nachweis muss denselben Weg gehen wie der Lauf.

**Und die Folge, die er für die Benchmark-Tabelle nennt, zeichengleich:**

> - **TB-92:** dasselbe für die Benchmark-Tabelle aus TB-91 — `benchmark.py` im Selektionsmodus, `--ziel` Beleg-Pfad, `diff` gegen `benchmark_drawdowns_2026-09-23_nach_wegA.json` → bytegleich. Das ist nicht die „Vorab-Nachrechnung" aus 23d, die mit Messbitte (b) entfallen ist (die fragte nach anderen Eingaben); es ist der Nachweis, dass der Erzeuger im Modus dasselbe tut wie ausserhalb. Wenn `benchmark.py` länger braucht als elf Sekunden, ist das Handwerk — der Nachweis gehört trotzdem vor den Tag, einmal.

**Das Ergebnis (TB-92, `docs/belege/TB-92/a1b_ergebnis.txt`,
`a1b_ergebnis_kinder.txt`, `a1b_lesequellen_kinder.txt`; in TB-94 an den
Belegen nachgelesen):**

| | |
|---|---|
| Wurzel | Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` (Register 18), MANIFEST-`datenstand_hash` `d9449faf…`; `data/` war zum Messzeitpunkt **225/225** Dateien byteweise gleich dem Snapshot (Anfrage 23g, von Fable in 23e zur Kenntnis genommen) — ⚠️ nach 23e eine eigene Tatsache, die den Modus-Lauf **nicht** ersetzt |
| Umlenkung | `TB30A_BASE_DIR` auf einen Hilfsordner, dessen `data/` (223 Verknüpfungen) und `config/` auf den Snapshot zeigen. ⚠️ `TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` **nicht** (0 Treffer) — der „Modus" ist hier die Umlenkung auf den Snapshot, wie in TB-93 |
| Code-Commit | `d136251` (`benchmark.py` `d6bdd558…`, `faltenplan.py` `7aa0b8cc…`) |
| ⭐ Ergebnis | **Vier Läufe, alle rc 0, je 51–52 s, alle bytegleich** `64fb2912…` mit `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`. Lauf 1 nach `docs/belege/TB-92/benchmark_modusnachweis.json`, die übrigen ins Scratchpad; **nichts in `ergebnisse/` geschrieben** |
| ⭐ Lesequellen | Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (**11 Prozesse**): **0 Lesezugriffe auf `data/` oder `config/` des Repos**; **222** CSV und **2** Universumsdateien aus dem Snapshot. Dazu Eingaben **ausserhalb** des Snapshots — 39.8 |

⇒ **Die vollzogene Tabelle ist aus dem eingefrorenen Datenstand byteweise
wiederherstellbar**, auf dem Weg, den der Lauf am Tag nimmt. Snapshot-Hash,
Code-Commit und Modus stehen damit neben ihrem Hash, wie 23e es verlangt.

⚠️ **Tatsachennotiz:** Der Registertext „Eingabestand eingefrorener
Ergebnisdateien" (23d Abschnitt 2), den 23e präzisiert, ist mit diesem
Abschnitt **nicht** eingetragen — nach 23d Abschnitt 4 gehört er zum Planpunkt
`messgroessen.json` (TB-96). Hier stehen nur die Tatsachen, die er für die
Benchmark-Tabelle verlangt.

> ⭐⭐ **Zweiter Anwendungsfall (40.6, Fable 24a, TB-96, 24.09.2026):** Neben
> `messgroessen.json` fallen die **neun TB-24-Listen** unter 23d
> („Eingabestand") in voller Form — Fables Registertext „Ergänzung zu 23d und
> zu 5.4" steht in **40.6**. Der Registertext „Eingabestand eingefrorener
> Ergebnisdateien" selbst ist weiter **nicht** eingetragen. ⚠️ Die Nummer oben
> ist gerückt: `messgroessen.json` ist **TB-101**, nicht TB-96 (40.9 (c)).

> ⭐⭐ **Dieser Nachweis ist nach der Zwei-Teile-Regel 2 (41.2 B4, 41.3 C6/C7,
> Fable 24c/24d, TB-108, 25.09.2026):** Ein Nachweis besteht aus
> Ergebnisvergleich **und** Leseprotokoll; zeigt das Protokoll einen Zugriff
> ausserhalb, ist er 2 (**41.2, B4**). Das eigene Protokoll dieses Laufs zeigt
> zwei Eingaben ausserhalb des Snapshots (39.8). Zudem war TB-92 A1b ein
> **Hilfsordner-Lauf** (`TB30A_BASE_DIR`, Zeile „Umlenkung" oben) — nach 41.3
> (C6) kein Modus-Lauf; der Ergebnisvergleich bleibt Tatsache, als Nachweis 2
> (**41.3, C7**). Die Tabelle ist seitdem im Resolver-Modus bytegleich
> reproduziert (TB-104 bis TB-107, 42.4 G10) — als Nachweis weiter 2, bis
> beide Eingaben registriert sind. Tabelle und Text oben bleiben zeichengleich.

### 39.7 ⚠️ Tatsachennotiz — `herkunft.py::EINGEFROREN` zeigt weiter auf den historischen Stand

`research/vorregistrierung/herkunft.py` ist **unverändert** (`56a1c2e1…`,
TB-94 gemessen). Seine Liste `EINGEFROREN` hasht damit weiter
`ergebnisse/benchmark_drawdowns.json` — **nicht** die Tabelle, die der Lauf
liest. **Fable, 23d Abschnitt 1, zeichengleich:**

> **(2) `EINGEFROREN` bleibt, wie es ist — es trägt weiter den alten Pfad, nicht beide.** Der Grund ist nicht der Wortlaut, sondern der Ort: `EINGEFROREN` steht in `herkunft.py` (Punkte 11/12), und in 22d habe ich entschieden, `herkunft.py` nicht zu öffnen, weil die Sperrlisten-Sonde die Lücke schliesst. Das gilt hier genauso: Die **neue** Tabelle ist durch Punkt 4 und das Abbild geschützt (Sonde); die **alte** bleibt in `EINGEFROREN` als das, was sie ist — der registrierte historische Stand, dessen Hash `register()` bezeugt. Die Tatsachennotiz zu 37.4 wird um den Satz ergänzt: „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde." Zwei Nachweise, zwei Gegenstände, kein Widerspruch (22d).

⇒ Die neue Tabelle schützen **Punkt 4** (39.2) und **das Abbild** (39.9);
beides ist mit diesem Abschnitt erfüllt. ⭐ **Deshalb ist das eine
Tatsachennotiz und kein Befund** — aber sie gehört ins Register, damit niemand
`EINGEFROREN` für vollständig hält. Der Satz, um den Fable die Tatsachennotiz
zu 37.4 ergänzt, steht dort als Marke.

**Fables Präzisierung zu 36.1 (1), 23c Abschnitt 2, zeichengleich** — „gesperrt"
umfasst jeden Pfad, dessen Hash am Tag bezeugt wird, **auch
`herkunft.py::EINGEFROREN`**:

> **Präzisierung zu 36.1 (1):** „auf der Sperrliste steht oder für sie bestimmt ist" umfasst jeden Pfad, dessen Hash am Tag bezeugt wird — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) **und die Einträge von `herkunft.py::EINGEFROREN`**, solange `register()` über sie hasht. Die Sperrlisten-Sonde führt diese Pfade als dritte Gruppe („Abschnitt 0") und prüft sie gleich.

⚠️ **Tatsachennotiz:** Die „dritte Gruppe" („Abschnitt 0") führt die Sonde
heute **nicht** — sie kennt `EINGEFROREN` nicht (Kopf von
`shared/sperrlistensonde.py`). Offen, Handwerk mit eigener Freigabe.

> ⭐ **Stand (42.3 F2, 42.5, TB-108, 25.09.2026):** „`herkunft.py` ist
> unverändert (`56a1c2e1…`)" beschreibt den Stand von TB-94. Seit TB-106
> (`5791b4c`) ist es planmässig geöffnet (`351f24c2…`); `EINGEFROREN` ist dabei
> zeichengleich geblieben und zeigt weiter auf
> `ergebnisse/benchmark_drawdowns.json`. Die dritte Gruppe führt die Sonde seit
> TB-97 aus dem Abbild (Gruppe „eingefroren" in `cb4eb1b4…` und `40ffe18d…`).
> Der Text oben bleibt zeichengleich.

**Marke am alten Ort:** bei **37.4**, vor der Marke am alten Ort des
Abschnitts.

### 39.8 ⭐⭐ Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand

Der Modus-Lauf (39.6) hat neben dem Snapshot **zwei weitere Eingabequellen im
Repo** geöffnet (`docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4
gleich):

| Eingabe | Tatsache |
|---|---|
| `research/vorregistrierung/ergebnisse/messgroessen.json` | ⚠️ beschreibt nach TB-93 einen Datenstand, den es nicht mehr gibt (Eingabestand vor `90e3cbd`, TB-34). Wird mit **TB-96** geschlossen (23d, 23e) |
| **neun** `research/tb24_haltedauern/daten/*_alle_trades.csv` | ⚠️ Ergebnisdateien, keine Kursdaten; weder auf der Sperrliste noch im Snapshot. Der Weg führt über den Faltenplan (TB-92) |

**Fable, 23f Abschnitt 6, zeichengleich — der Fund:**

> Die Sitzung hat protokolliert, was der Modus-Lauf öffnet: 222 aus `snapshot/csv`, 2 aus `snapshot/config`, **dazu `ergebnisse/messgroessen.json` und neun Trade-Listen aus dem Repo.** Das ist die Sonde „Lesequellen" als Laufzeitmessung — genau 5e —, und sie zeigt zweierlei: Erstens liest der Benchmark-Lauf die Messdatei, deren Eingabestand 23d beanstandet hat (das ist bekannt und wird mit TB-94 geschlossen). Zweitens **neun Trade-Listen**. Die sind Ergebnisdateien, keine Kursdaten, und sie stehen weder auf der Sperrliste noch im Snapshot.

⚠️ **Berichtigung einer Nummer, damit die Ablage lesbar bleibt:** Fable nennt
oben (und in 23e Abschnitt 2) für den Eingabestand von `messgroessen.json` die
Nummer **TB-94**; so stand es im Plan des steuernden Chats vom Vormittag des
23.09. Die Nummern sind danach gerückt, weil der Registervollzug vorgezogen
wurde (`docs/auftraege/AKTUELLER_AUFTRAG.md`, 23.09.2026, 20:00): **TB-94 ist
dieser Eintrag, TB-95 sind `G6`/`H3` und die Messbitte unten, TB-96 ist
`messgroessen.json`.** *Eine Nummer, die zwei Sachen meint, ist schlimmer als
eine verschobene.*

⚠️⚠️ **OFFEN — Fables Messbitte, eingetragen, nicht beantwortet** (23f
Abschnitt 6, zeichengleich):

> **Messbitte, nur das Ob:** Welcher Schritt des Modus-Laufs öffnet die neun Trade-Listen — `benchmark.py` selbst, oder ein Nebenweg (`registerdaten.py`, `faltenplan.py`, Trockenlauf)? Und **gehen ihre Inhalte in die Tabelle ein** — oder werden sie nur geöffnet (etwa für eine Konsistenzprüfung)? Wenn sie eingehen, hat die Benchmark-Tabelle eine Eingabe, deren Eingabestand nicht registriert ist — derselbe Fall wie `messgroessen.json`, und die Regel aus 23d gilt für sie. Wenn sie nur geöffnet werden, ist es eine Tatsachennotiz und ein Kandidat für die Lesequellen-Sonde.

**Seine Unsicherheit dazu, zeichengleich:**

> **Unsicher:** ob die neun Trade-Listen die TB-24-Listen sind (dann alter Code, alter Datenstand — 26.5) — das ändert nicht die Frage, nur ihr Gewicht.

⛔ **In TB-94 nicht gemessen und nicht beantwortet** — Gegenstand von TB-95.

**Zwei weitere Tatsachen aus TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 2, A1b-6), die hierher gehören:** (1) `benchmark.py` und
`messgroessen.py` lesen an `shared/paths.py` **vorbei** (`TB30A_BASE_DIR` bzw.
`<BASE>/data`); die Kindprozesse des Faltenplans folgen **eigenen** Variablen
(`faltenplan_neun.py` `TB36_BASE_DIR`, `universum_trockenlauf.py` und
`loaderlauf.py` `TB40_BASE_DIR`) und haben gemessen trotzdem aus dem Snapshot
gelesen. (2) Der Lauf öffnet `logs/notifications/manuelle_eingriffe.log` im
Modus `a` (Import aus `notifications/`); die Datei blieb unverändert (mtime
11.09.). Beides ist Stoff für Fables Sonde „Lesequellen" (23d), nicht für
diesen Eintrag.

⭐⭐ **Nachtrag zu 39.8 (40.5, Fable 24a, TB-96, 24.09.2026) — die Messbitte
oben ist beantwortet.** Gemessen in TB-95 (`069370d`; Belege
`docs/belege/TB-95/d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d3_antwort.md`),
im Modus-Lauf gegen den Snapshot `63e4b6c8…`, Sichtschutz 27.1 (keine
Ergebnisgrössen):

| | |
|---|---|
| **Wer öffnet** | **`benchmark.py` selbst**, kein Nebenweg: `benchmark.py::je_bot` → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (`read_csv`). Jede der neun Listen **genau einmal**, **nur im Hauptprozess**; die zehn Kindprozesse (Trockenlauf/Loader) und `registerdaten.py` öffnen keine davon |
| **Gehen sie ein?** | **Ja — über genau eine Grösse, die Faltenlänge.** Gelesen wird nur `entry_time`; gezählt je vollem Kalenderjahr, gemittelt, gegen die Schwelle aus 5.4 verglichen ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen ⇒ Tabellenzeilen. Sonst erreicht nichts aus den Listen die Tabelle |
| **Störprobe, in beide Richtungen** (auf Kopien, Originale vorher = nachher) | **eine Zeile weg ⇒ Tabelle bytegleich** (`64fb2912…`), weil die Schwelle nicht überschritten wird; **zwei von drei Zeilen weg ⇒ verschieden** (`97cf224f…`): **ein** Bot (`volatility_breakout_crypto`) kippt von Einjahres- auf Zweijahresfalten, die anderen **acht bleiben gleich** |
| **Herkunft** | ein einziger Commit, **`78e2bc6`, 13.09.2026, TB-24**, seitdem unverändert — die TB-24-Listen, gemessen an Pfad, Commit und Datum; vor TB-31/TB-34/TB-38 und vor dem Snapshot. **Nicht im Snapshot, nicht auf der Sperrliste**; im Register als Quelle genannt (5.4), **ohne Hash** |
| Nebenbefund | Derselbe Modus-Lauf lieferte die vollzogene Tabelle zum fünften Mal bytegleich (`64fb2912…`, 39.6) |

⚠️ **Der methodische Satz, der über den Fall hinausgeht:** Die Störprobe, wie
der Auftrag TB-95 sie vorschlug („eine Zeile entfernen genügt"), hätte
**allein das falsche „nein"** ergeben. Eine Eingabe, die über eine Schwelle
wirkt, zeigt bei kleinen Änderungen nichts; wer nur in eine Richtung stört,
misst die Schwelle nicht, sondern ihren Abstand. ⇒ Eine Störprobe nach „geht
es ein?" wird in **beide** Richtungen geführt: klein (bleibt gleich?) **und**
über eine bekannte Schwelle hinweg (ändert sich?).

⇒ **Die Einordnung steht in 40.6:** Die neun Listen sind Eingabedateien nach
23d in voller Form — Neu-Erzeugung auf dem Snapshot, Sperrlistenpunkt,
Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (TB-98). Die
Nummer 40.5 verweist hierher.

> ⭐⭐ **Zwei Nachträge (41.3 C9, 42.1 D10/D11, Fable 24d/25a, TB-108,
> 25.09.2026):** (1) Der Lesehaken dieses Abschnitts ist **von TB-92** — der
> Satz „erst mit TB-95" des steuernden Chats war falsch, dieses Register hatte
> recht (Messung in **41.3, C9**). (2) Das Öffnen von
> `logs/notifications/manuelle_eingriffe.log` im Modus `a` ist ein Schreibziel
> ausserhalb `--ziel` (Klasse (iii), 42.1 D6); **behoben in TB-105**
> (`d48a195`), der Benchmark-Lauf im Modus öffnet es seither nicht mehr
> (**42.1, D11**). Der Text oben bleibt zeichengleich.

### 39.9 Das neue Abbild und die Sonde

**Was 36.6 und 37.3 verlangen:** Jede Fortschreibung der Sperrliste vor dem Tag
erzeugt ein **neues** Abbild unter neuem Namen; das alte bleibt und wird nie
angepasst; das aktuelle Abbild steht selbst mit Hash im Register. Ein Befund
`1` aus beauftragter Änderung wird durch Tatsachennotiz (39.5) und neues
Abbild geschlossen. **Fable, 22g, zeichengleich:** *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

**Was die Sonde am Tag liefern muss — Fable, 23c Abschnitt 3, zeichengleich:**
*„Die Tag-Vorbedingung aus 22d/37 lautet: kein Pfad-Bestandteil 1, jede 2 mit Tatsachennotiz."*
⇒ „Sonde 0 für die Pfade" im Fertigkriterium (39.1) heisst: **jede Datei
jedes Punktes gleich** und Prüfung (ii) `0`. Ein Gesamtausgang `2` wegen
Punkten, die Nicht-Dateibezogenes nennen (Werte, Funktionen,
Registerverweise), ist damit vereinbar; er ist keine Aussage über die Pfade.

**Reihenfolge:** Das Abbild liest den Listentext von Abschnitt 10. Es wird
deshalb **nach** dem Commit gezogen, der Punkt 4 (39.2) und diesen Abschnitt
enthält, mit `research/vorregistrierung/sperrliste_abbild.py --ziel` (keine
Voreinstellung, Einmal-Schreibsperre). Name, Hash und die Bilanz der Sonde
davor und danach werden **unmittelbar unten** eingetragen, in einem eigenen
Commit — additiv, der Listentext von Abschnitt 10 wird dabei nicht berührt.

**Ergebnis (Block D, TB-94, 23.09.2026; `docs/belege/TB-94/d1_abbild.txt`,
`d2_sonde_nachher.txt`, `a2_sonde_vorher.txt`,
`b_sonde_nach_blockB_altes_abbild.txt`):**

| | |
|---|---|
| ⭐ Neues Abbild | `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json`, **sha256 `2f23f76c99e22991e4a331ec1107dc0f090a425bc9e050793470ee3cd52dd4fe`**, 7351 Bytes, erzeugt 2026-09-23T18:21:35Z am Stand `27b68b9` (der Commit mit 39.2 und diesem Abschnitt), 14 Punkte aus Abschnitt 10 (Z. 845–958 am Stand `27b68b9`), 15 Pfadnennungen; `sperrliste_abbild.py --ziel` rc 0, Ziel existierte vorher nicht |
| Altes Abbild | `sperrliste_abbild_2026-09-22.json` `6a1b732e…` — **nicht gelöscht, nicht geändert** (36.6); vor und nach dem Ziehen gemessen |
| Sonde vorher (altes Abbild, Stand `12f6089`) | rc **1**; Befund an **2, 3, 4, 5, 6, 14** (drei Dateien, 39.5); (ii) `0`; Bilanz 0 / 6 / 8 |
| Sonde nach Block B und C (altes Abbild, uncommittet) | rc **1**; dazu (ii) **1** an Punkt 4, Felder `pfade` und `nicht_dateibezogen` — der neue Pfad. Das ist der erwartete Nachweis, dass die Sonde die Pfadzeile liest |
| ⭐ Sonde gegen das neue Abbild (Stand `27b68b9`) | rc **2**; **0 Befunde**; **alle 15 Pfadnennungen „gleich"**, darunter `ergebnisse/benchmark_drawdowns.json` `a163c498…` und `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` `64fb2912…`; Punkte **2 und 5** `0`; Punkte 1, 3, 4 und 6–14 `2`, jeder wegen Nicht-Dateibezogenem im Punkttext; (ii) `0`, Listentext wie bei Erzeugung: ja. Bilanz **2 / 0 / 12** |
| Gruppe „bestimmt" | die Sonde nennt weiter `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) mit „Vollzug steht aus" — die feste Konstante aus 39.3; nach dem Registertext ist die Gruppe leer |

⇒ **Die planmässigen Befunde aus 39.5 sind geschlossen: kein Pfad-Bestandteil
ist `1`.** Der Gesamtausgang `2` sagt nichts über die Pfade, sondern über
Werte, Funktionen und Registerverweise in den Punkttexten (A2, je Sache; 23c).
Punkt 4 steht auf `2`, nicht auf `0`, weil schon sein alter Text
„einschliesslich der Interpolationsregel" nennt; die Pfadzeile aus 39.2
bringt weiteren Wortlaut dazu, ändert am Ausgang aber nichts. ⚠️ Ob **jede**
`2` eine Tatsachennotiz trägt, ist Tag-Vorbedingung (23c) und hier **nicht**
geprüft.

⭐ **Das aktuelle Abbild der Sperrliste (36.6) ist damit
`sperrliste_abbild_2026-09-23.json`, `2f23f76c…`.**

### 39.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`, `benchmark.py`, `faltenplan.py`, `messgroessen.py`, `herkunft.py` noch `shared/sperrlistensonde.py` | — |
| ⛔ | **Nichts gerechnet** — `benchmark.py`, `faltenplan.py main()`, `messgroessen.py` nicht aufgerufen; in `research/vorregistrierung/ergebnisse/` nichts geschrieben **ausser dem neuen Abbild** (39.9) | — |
| ⛔ | **`G6`/`H3` nicht angefasst** — weder gemessen noch erklärt noch angepasst | TB-95 |
| ⛔ | **Fables Messbitte zu den neun Trade-Listen nicht beantwortet** (39.8) | TB-95 |
| ⛔ | **`messgroessen.json` nicht angefasst**; der Registertext „Eingabestand" (23d) nicht eingetragen (39.6) | TB-96 |
| ⛔ | **Der Sonden-Entwurf `sonde_je_datei_entwurf.patch` nicht angewandt**; die Konstante `BESTIMMT_NICHT_EINGETRAGEN` und die dritte Gruppe (39.3, 39.7) bleiben, wie sie sind | Handwerk, eigene Freigabe |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der Satz mit „grün" in 38.4, die offene Frage in 38.7 (d), der Kasten an Punkt 4 und die Punktzeilen 1–4 von Punkt 4 bleiben zeichengleich; ERSETZT-, Vollzugs- und Hinweis-Marken, nichts entfernt | — |
| ⭐ | **`benchmark_drawdowns.json` byteweise unverändert** (`a163c498…`) — vor Block B, nach Block B und nach dem Abbild gemessen (`a1_hashes.txt`, `d1_abbild.txt`) | — |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Zellenzahl je Bot 80/384/400/96/320/320/400/96/320, **Summe 2416**, wie Register Abschnitt 3 (ERZEUGT-Block; gemessen TB-92, `docs/belege/TB-92/d_zellenzahl.txt`) | — |
| ⚠️ | **Offen:** `G6`/`H3` und die Messbitte (TB-95) · `messgroessen.json` und der Registertext „Eingabestand" (TB-96) · die Sonde: leere Gruppe „bestimmt", dritte Gruppe „Abschnitt 0", „Schreibziele", „Lesequellen" (23c, 23d) · „null rote Prüfungen" als Tag-Vorbedingung (21.9, 23a) | TB-95 / TB-96 / Handwerk |

*Dieser Abschnitt ist rein additiv: Er vollzieht Sperrlistenpunkt 4 in Form
(ii) durch drei neue Folgezeilen, berichtigt ein Fertigkriterium, ohne den
alten Satz anzutasten, trägt die Messungen aus TB-91 und TB-92 als
Tatsachennotizen samt einer offenen Messbitte ein, setzt zehn Marken am alten
Ort — und entfernt nichts. Gebaut und gerechnet wird nichts.*

