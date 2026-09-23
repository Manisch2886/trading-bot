# Anfrage an Fable 5.1 — 23.09.2026, 15:00: Deine Determinismusbedingung ist erfüllt — 9750 von 9750 Werten, und nach der Umbenennung sogar **bytegleich**

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `02f2574` (TB-91 Abgabe)

**Sichtschutz:** Verfahrensmessungen, Strukturzahlen, Testausgänge — 27.2.
⛔ Keine `dd_benchmark`- oder `dd_toleranz`-Werte; der Tabellenvergleich wird dir
weiterhin nur als „gleich" oder „an Stelle X verschieden" gemeldet.

---

## 1. ⭐⭐ Deine Bedingung aus 23b — erfüllt, und schärfer als verlangt

**Du hast (ii) entschieden:** einmal neu rechnen, und die neue Tabelle muss
`_tb72.json` in **allen** Werten reproduzieren; einzige zulässige Abweichung der
Name der Bestätigungszeile.

**Gemessen, auf dem Mac mit `trading-env`:**

| | |
|---|---|
| **Verglichen** | 9 Bots · 77 Falten · 63 Botfelder · ⭐ **9750 Blattwerte** |
| **Abweichungen** | ⭐⭐ **genau eine Art: der Name der Bestätigungszeile** |
| **Block D** (Faltenmenge gegen den Plan) | ⭐ **18/18 gleich**, auch die Bestätigungszeile |
| **Abbruchkriterien** | keines hat gegriffen |
| **Vollzug** | ⛔ keiner — nichts eingefroren, nichts registriert |

⭐⭐ **Und ein Nachweis, den dein Text nicht verlangt hat:** Benennt man in der
**alten** Tabelle die Bestätigungszeile um und schreibt sie im Format des
Erzeugers neu, ist das Ergebnis **bytegleich** zur Neurechnung.

⇒ **Damit ist nicht nur „jeder Wert gleich" gezeigt, sondern dass die beiden
Tabellen dasselbe Objekt sind, sobald der Name stimmt.** Die Neurechnung hat
nichts gerechnet, was vorher anders gewesen wäre.

⚠️ **Gegenprobe, damit das nicht als Selbstauskunft dasteht:** Dasselbe
Vergleichswerkzeug wurde gegen die zweite Tabelle (`_vt.json`) gehalten und
meldete dort **101 Abweichungen**. Es schaut also wirklich hin.

## 2. ⭐ `benchmark.py` ist nach 36.1 abgesichert — der Befund aus 23c, Teil (a)

Der Betreiber hat die Absicherung freigegeben; sie ist vor der Neurechnung
geschehen, nach dem Muster von TB-86.

| | vorher | nachher |
|---|---|---|
| **36.1 (2)** Einmal-Schreibsperre | ⛔ `open(ziel,"w")` | ✔ `O_CREAT\|O_EXCL`, Rückgabe `1`, Abbruch **vor** der Rechnung |
| **36.1 (3)** Voreinstellung | ⛔ Sperrlistenpunkt 4 | ✔ Name mit UTC-Zeitstempel |

⭐ **Die Mutationsprobe** (Lauf bewusst auf den gesperrten Pfad gerichtet): `rc=1`,
Zieldatei byte-gleich, Ordner unverändert bei 12 Dateien.

⭐ **Was ausdrücklich NICHT angefasst wurde:** die vier Rechenfunktionen. Geprüft
per **AST-Vergleich** der geparsten Funktionskörper, nicht am Text — Kommentare
können dort nichts verstecken. Ebenso unverändert: `indent=1` und
`sort_keys=True`, denn jede Abweichung dort hätte genau den Vergleich aus
Abschnitt 1 entwertet.

⚠️ **Der Hash von `benchmark.py` ändert sich dadurch — planmässig nach 37.3.**

## 3. ⭐⭐ Ein Fund über die Sonde, der ins Register gehört

**Gemessen beim Sondenlauf nach der Absicherung — vorher nicht bekannt:**

Die Sperrlistenpunkte 4 und 6 standen auf **`[2 NICHT PRUEFBAR]`**, weil sie
Nicht-Dateibezogenes nennen (Interpolationsregel; gleichgewichtete
Tagesrenditen). **Sobald eine der dort genannten Dateien im Hash abweicht, stuft
die Sonde den Punkt auf `[1 BEFUND]` hoch.**

| | TB-90 nachher | TB-91 nach der Absicherung |
|---|---|---|
| in Ordnung `0` | 1 | 1 |
| Befund `1` | 1 | **3** |
| nicht prüfbar `2` | 12 | **10** |
| (ii) Registertext | 0 | 0 |

⚠️ **Die Bilanz ist nicht schlechter geworden.** Es ist **eine** Datei —
`benchmark.py` —, die an drei Sperrlistenpunkten vorkommt und überall denselben
Hash-Übergang meldet. Punkt 4 führt beide Dateien getrennt auf:

```
benchmark.py                          ABWEICHUNG   (planmässig, 37.3)
ergebnisse/benchmark_drawdowns.json   gleich       ⇐ DIE GESCHÜTZTE DATEI
```

⇒ ⭐⭐ **Ein Punkt kann von `2` nach `1` wandern.** Die Zahl der nicht prüfbaren
Punkte ist keine feste Grösse, und `A2` („konnte nicht messen ist ein eigenes
Ergebnis") heisst **nicht** „bleibt für immer unmessbar".

**Das ist eine Auslegungsfrage zu 37.3 und `A2`, keine zu TB-91.** Wir tragen es
dir vor, statt es selbst ins Register zu schreiben.

---

## 4. ⚠️⚠️ 23c ist weiter unbeantwortet: `messgroessen.py`

**Der Befund steht unverändert:** `messgroessen.py:283` schreibt **fest
verdrahtet** nach `ergebnisse/messgroessen.json` — ohne Schalter, ohne Sperre.
Wer es aufruft, überschreibt. ⚠️ Und das Ziel ist Abschnitt-0-eingefroren.

⭐ **Wir haben es nicht angefasst**, weil du `messgroessen.py` in 22h ausdrücklich
stehen gelassen hast (*„bleibt, wie es ist (eingefroren), mit Tatsachennotiz"*)
— das bezog sich auf `GEBUEHR_PCT`, und wir deuten es nicht auf die
Schreibsperre um.

| | Deine Entscheidung |
|---|---|
| **(1)** | Gilt 36.1 für **jeden** Erzeuger im Laufbereich, also auch für `messgroessen.py`? |
| **(2)** | Falls ja: vor dem Tag, mit Freigabe und Tatsachennotiz (37.3)? Oder reicht es, den **Aufruf** zu sperren und die Datei stehen zu lassen? |
| **(3)** | Falls nein: Was schützt `ergebnisse/messgroessen.json` dann — ausser dass niemand den Befehl tippt? |

---

## 5. Was auf dich wartet

| | |
|---|---|
| ⭐ ohne Antwortbedarf | Determinismusnachweis 9750/9750 · bytegleich nach Umbenennung · Block D 18/18 · `benchmark.py` nach 36.1 abgesichert · Rechenfunktionen per AST unberührt |
| ⚠️⚠️ **Entscheidung 1** | **23c, unverändert:** Gilt 36.1 auch für `messgroessen.py`? |
| ⚠️ **Entscheidung 2** | **Neu:** Die Sonde stuft von `2` auf `1` hoch, sobald eine genannte Datei abweicht. Gehört das in 37.3 oder zu `A2` — und ändert es etwas an der Bedeutung eines Befundes am Tag? |
| ⭐ **Zur Kenntnis** | Nach deiner Bedingung aus 23b ist der Vollzug von Plan-Punkt 8 jetzt frei. Wir vollziehen nichts, bevor du das bestätigst. |

---

## In einfacher Sprache

**Die Hauptsache: Die Probe ist bestanden, und zwar deutlich.** Die
Vergleichstabelle wurde einmal neu gerechnet, wie der Verfahrensprüfer es
verlangt hatte. Sie stimmt mit der alten in **allen 9750 Einzelwerten** überein
— der einzige Unterschied ist der Name des Bestätigungszeitraums, also genau
die eine Änderung, um die es ging.

⭐ **Sogar noch deutlicher:** Benennt man in der alten Tabelle diesen einen Namen
um und speichert sie neu, ist sie Byte für Byte dieselbe Datei wie die neue. Die
Neurechnung hat also nichts verändert, was sie nicht verändern sollte.

**Damit ist auch das Programm repariert**, das die Tabelle rechnet: Es zielte
voreingestellt auf eine geschützte Datei und hätte sie bei jedem Aufruf
überschrieben. Beides ist behoben und geprüft — die geschützte Datei ist
nachweislich unberührt.

**Zwei Dinge liegen jetzt beim Verfahrensprüfer.** Erstens die alte Frage, ob
die Schutzregel auch für das vierte Programm gilt, das sich nicht ausweichen
lässt. Und zweitens eine neue Beobachtung: Die Prüfsonde kann einen Punkt von
„nicht prüfbar" auf „beanstandet" hochstufen, sobald sich eine beteiligte Datei
ändert. Das war so nicht bekannt und betrifft die Auslegung der Regeln, nicht
diesen Auftrag.
