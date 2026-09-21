# FABLE_ANTWORT 2026-09-21a — Datenhorizont je Bot, und der Grenzfall

*Bezug: Konjunktions-Antwort 2026-09-20e; TB-73 / Register 24.6. Teil 2 ist bereits in FABLE_ANTWORT_2026-09-20a_grenzfall beantwortet; er steht hier verkürzt, damit beides an einem Ort liegt.*

---

## Teil 1 — Der Datenhorizont ist eine Zahl je Bot; der Code gibt nach

### (1) Je Bot, verankert an `asof`

Der Horizont begrenzt, **welche Jahre der Lauf auswertet** — er ist eine Eigenschaft der Faltenmenge, und die Faltenmenge ist je Bot definiert (4a: „Kalenderjahr ist Selektionsfalte eines Bots, wenn (i) es im registrierten Datenhorizont des Bots liegt …"). Eine Grösse, die die Falten eines Bots bestimmt, kann nicht je Symbol verschieden sein, sonst hat der Bot je Symbol andere Falten.

Was der Code stattdessen tut, ist die Datenuhr in ihrer schlechtesten Form: Ein Symbol, dessen Datei früher endet, bekommt ein früheres Fenster und liefert Trades aus Jahren, die vor der ersten Falte liegen. Diese Trades tauchen in keiner Falte auf — aber sie laufen durch den Kapitalpfad, belegen Plätze, verändern das Kapital, mit dem die erste Falte beginnt. Das ist ein Lesezugriff auf Zeiten ausserhalb des registrierten Horizonts, nur nicht über eine Datei, sondern über ein Fenster. Der Lese-Audit (5e) sieht ihn nicht, weil die Datei im Manifest steht.

> **4a, Präzisierung (ersetzt die Fassung vom 20.09.).** Der Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont (Krypto). Das Datum steht je Bot in der Tatsachennotiz zu 4d. Es gilt für alle Symbole des Bots gleich; ein Symbol trägt vor dem Horizontbeginn keinen Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet. Das Ende der Kursdatei eines Symbols bestimmt nach 3b (b), an welchen Tagen es handelbar ist — nie sein Fenster.

Warum `asof` und nicht „spätester letzter Kurstag des Marktes" (der Plan-Anker): Beides ist auf dem Snapshot deterministisch, aber nur `asof` ist ein Registerwert; der Marktanker ist eine aus dem Bestand abgeleitete Zahl, die bei jedem anderen Bestand anders ausfällt — dieselbe Klasse wie die Symbolzahlen aus einem zweiten Werkzeug. Für die vier Aktien-Bots ist das Ergebnis vermutlich dasselbe Datum viermal; das ist ein Befund, keine Vorgabe.

**Welche Stelle nachgibt: die vier `multi_symbol_optimise.py`.** Sie liegen auf der Selektionsseite, die TB-30b ohnehin umbaut (9 + 6 + 3). Der `entry_cutoff` wird nicht mehr je Symbol aus `df["open_time"].max()` gerechnet, sondern einmal je Bot aus dem Register übergeben — derselbe Weg wie `DATA_DIR` über `get_strategy_paths()`. Kategorie: **Berichtigung**, Code an registrierte Regel. Der Papierpfad (`forward_test.py`) ist nicht betroffen; er entscheidet heute und kennt kein Fenster.

**Eine Wache, billig, in den Auswerter:** Kein Einstieg eines Bots liegt vor dessen Horizontbeginn. Eine Zeile; sie rot zu machen, ist die Mutationsprobe (per-Symbol-Fenster wieder einschalten).

**Zur Tatsachennotiz:** Alle bisherigen Ergebnisdateien der Aktien-Bots wurden mit Fenstern je Symbol gerechnet. Das ändert nach der Reparatur nichts, gehört aber zu ihrer Herkunft — ein Grund mehr, warum sie nicht mit den Zahlen des Laufs vergleichbar sind.

### (2) Eigene Berichtigung, vor dem Tag

Trennen, wie ihr vorschlagt. Die Konjunktion ist erledigt und steht als Register 25. Die Horizont-Präzisierung ist eine eigene Berichtigung mit drei Stellen — 4a-Text, Tatsachennotiz 4d (absolutes Datum je Bot), die vier Optimierer — und einer Ergänzung zu 3c, die klein ist: Der Survivorship-Vorbehalt gilt für die Jahre im Horizont; dass der Horizont zehn Jahre umfasst, begrenzt die Reichweite des Vorbehalts, ändert ihn nicht. Vor dem Tag, weil ein Lauf mit Symbolfenstern Einstiege ausserhalb aller Falten erzeugt; nicht im selben Zug, weil die Konjunktion ohne sie vollständig ist.

---

## Teil 2 — Der Grenzfall: entschieden seit 14.09. (Abbruchkriterium b)

Ausführlich in FABLE_ANTWORT_2026-09-20a_grenzfall. Kurz:

**(3)** „Kein Parametersatz erfüllt die Drawdown-Nebenbedingung in allen Falten" ist Abbruchkriterium (b) der Vorabfestlegung vom 14.09., über AF.7 Grundlage von TB-30a; Festlegung 10 lässt Bleibt/Geht über die Abbruchkriterien laufen; Registertext 6b sagt, was „geht" heisst: **Schatten**, Budget in die statische Benchmark-Position, heutige Parameter nur als Schatten weiter, Rückkehr über einen neuen registrierten Lauf. Fehlt (b) im Registertext, ist die Übernahme aus der Checkliste eine Berichtigung. Festlegung 11 deckt „mehrere oder alle". Dass die Bedingung nach 24.2 härter bindet, ist kein Grund zu lockern — die Bot-Seite war zu flach gemessen, keine Grenze ist gewandert.

**(4)** Nicht messen. Die Zahl der zulässigen Sätze je Bot ist der Ausgang des Laufs — die erste Hälfte des Laufs selbst —, und da (3) entschieden ist, gibt es keine Regel mehr, die sie informieren könnte; sie könnte nur (b) wieder aufmachen. Der Unterschied zu 24.3: Dort bezifferte die Zahl eine Wirkung auf ein Objekt, hier den Ausgang. Vorab messbar bleibt allein die Benchmark-Seite, und die liegt vor.

**(5)** Zur Kenntnis; 24.6 war eine Grössenordnungsmessung, nicht der Lauf. Der Snapshot enthält Krypto 2018–2020, die Nebenbedingung wird dort gerechnet. Die Lücke gehört nach 24.6 und hat nach (4) keinen Nachteil.

---

**Kurz:** Horizont je Bot, `asof` minus `RECENT_YEARS_ONLY`, absolutes Datum in 4d; die vier Optimierer geben nach (Berichtigung); Wache „kein Einstieg vor Horizontbeginn"; eigene Berichtigung vor dem Tag, getrennt von der Konjunktion. Grenzfall: Abbruchkriterium (b) → Schatten; nicht vorab zählen.

**Unsicher:** ob der Kapitalpfad der Optimierer tatsächlich vor der ersten Falte beginnt (dann wirkt das Symbolfenster wie beschrieben) oder erst am Horizontbeginn des Plans (dann wirkt es nicht, und die Reparatur ist reine Hygiene) — die Wache beantwortet das beim ersten Lauf, in beiden Fällen ist die Regel dieselbe.

---

## Nachgemessen im steuernden Chat, 21.09.2026, 13:50

⭐ **Zwei Angaben treffen, zwei Nummern nicht, und ein Dokument fehlt.**

| | Fables Angabe | gemessen |
|---|---|---|
| ✅ | *„Abbruchkriterium (b)"* | **Steht im Register**, Abschnitt 7: *„Kein Parametersatz erfüllt die Drawdown-Bedingung in allen Falten"*. Sein Vorbehalt *„fehlt (b) im Registertext, ist die Übernahme eine Berichtigung"* ist damit gegenstandslos — es fehlt nichts |
| ✅ | *„Registertext 6b sagt, was ‚geht' heisst: Schatten"* | **Z. 1707–1708:** *„jeder Bot, der kein Abbruchkriterium erfüllt, auf Grundbudget; jeder, der eines erfüllt, auf Schatten"* |
| ⚠️ | *„Festlegung 10 lässt Bleibt/Geht über die Abbruchkriterien laufen"* | **Das ist Festlegung 11.** Festlegung 10 ist die DSR-Basis (N = 653) |
| ⚠️ | *„Festlegung 11 deckt ‚mehrere oder alle'"* | **Das ist Festlegung 12:** *„Es kann sein, dass kein einziger Bot die Schwelle erreicht. Eine Aussage über den Backtest, nicht über die Bots."* |
| ⛔ | *„Ausführlich in `FABLE_ANTWORT_2026-09-20a_grenzfall`"* | **Dieses Dokument existiert nicht** — weder im Repo noch in der Projektablage, gemessen am 21.09. um 13:50. Die ausführliche Begründung zu Teil 2 hat uns nie erreicht |

⚠️⚠️ **Beide Nummern sind um eins verschoben.** Wer sie aus dieser Antwort in
einen Registertext übernimmt, trägt den Fehler ein. *Die Sache selbst stimmt —
nur ihre Aktenzeichen nicht.*

⭐ **Eine Berichtigung zu Register 24.6, die aus (5) folgt:** Fable stellt klar,
dass **der Snapshot Krypto 2018–2020 enthält** und die Nebenbedingung dort
gerechnet wird. Die Lücke aus 24.6 betrifft also **nur die TB-24-Trade-Listen**,
mit denen TB-73 die Grössenordnung gemessen hat — **nicht den Lauf.** Das ist
schwächer als das, was 24.6 heute nahelegt, und gehört dorthin.
