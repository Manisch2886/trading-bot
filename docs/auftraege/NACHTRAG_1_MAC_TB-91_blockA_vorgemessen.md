# Nachtrag 1 zu TB-91 — Block A ist vorgemessen; du misst nach statt zu bauen

**Angelegt:** 23.09.2026, vom steuernden Chat
**Gilt zusätzlich zu:** `MAC_TB-91_benchmark_absichern_und_neurechnung.md`
⚠️ **Der Auftrag selbst ist unverändert.** Dieser Nachtrag ändert nur, *wie*
Block A abläuft — Block B, C und D bleiben Wort für Wort bestehen.

---

## Was sich geändert hat

⭐ **Block A ist bereits ausgeführt.** Der steuernde Chat hat `benchmark.py` nach
36.1 abgesichert, weil die Verbindung dreimal abbrach und die Absicherung keine
`trading-env` braucht — sie ändert Quelltext, sie rechnet nicht.

**Der Arbeitsbaum trägt die Änderung uncommittet:** `research/vorregistrierung/benchmark.py`,
`numstat 101 12`.

⚠️⚠️ **Das ist eine VORMESSUNG, kein Nachweis** (Prüfprinzip `A8`). Du misst jede
Zahl nach. Weicht etwas ab, **gilt deine Nachmessung**, und die Abweichung kommt
ausdrücklich ins Ergebnisdokument.

**Die Belege liegen:**

| | |
|---|---|
| `docs/belege/TB-91/vormessung_blockA_absicherung_2026-09-23.txt` | die Auswertung, 213 Zeilen |
| `docs/belege/TB-91/sonde_nach_blockA_vormessung.txt` | der Sondenlauf im Rohtext |

---

## Block A wird für dich zu einer Nachmessung

**Statt Abschnitt 3 des Auftrags auszuführen, prüfst du sechs Dinge nach:**

| | zu prüfen | Vormessung sagt |
|---|---|---|
| **A-N1** | Hash von `benchmark.py` | `d6bdd5580534…` (Abbildstand war `3960375a539d…`) |
| **A-N2** | ⭐⭐ AST-Vergleich der **vier** Rechenfunktionen gegen `/tmp/benchmark_vorher.py` | `bh_tagesrenditen`, `drawdown_bei_exposure`, `nachschlagen`, `erlaubt` — **alle vier gleich** |
| **A-N3** | Mutationsprobe: Lauf gegen den Sperrlistenpfad | Abbruch, `rc=1`, Zieldatei byte-gleich, `ergebnisse/` bleibt bei 12 Dateien |
| **A-N4** | 36.1 (3): Voreinstellung | Name mit UTC-Zeitstempel, **nicht** `benchmark_drawdowns.json` |
| **A-N5** | Sondenlauf | Bilanz **1 / 3 / 10**, Befundpunkte **[2, 4, 6]**, `rc=1` |
| **A-N6** | ⭐ Wurde beim Ändern **gefragt**? | in der VM gilt `ask` nicht — **nur du kannst das messen** |

⚠️ **`/tmp/benchmark_vorher.py` liegt in der Brücken-VM, nicht auf dem Mac.** Für
A-N2 stellst du den Vorher-Stand selbst her:
`git show HEAD:research/vorregistrierung/benchmark.py > /tmp/benchmark_vorher.py`

---

## ⚠️ Zwei Berichtigungen an uns selbst

**(1) `median` ist keine Rechenfunktion von `benchmark.py`.** Wir zählten sie
früher zu den gesperrten und meldeten „0 Treffer". Gemessen: Die Funktion
existiert dort überhaupt nicht. Die Null bedeutete **Abwesenheit, nicht
Unberührtheit**. Es sind **vier**, nicht fünf.

**(2) `grep -c "def erlaubt"` auf dem Diff meldet `1`, nicht `0`.** Gemessen ist
das die **Hunk-Kopfzeile** (`@@ …`), in der git die umgebende Funktion nennt.
Geänderte Zeilen (`+`/`-`), die `erlaubt` nennen: **0**. Der AST-Körper ist
identisch. ⭐ *Wir melden das, weil ein Rohtreffer sonst wie ein Widerspruch zu
A-N2 aussähe.*

---

## ⭐⭐ Ein Fund, der ins Register gehört: die Sonde stuft hoch

**Gemessen, vorher nicht bekannt:** Punkt 4 und Punkt 6 standen auf
`[2 NICHT PRUEFBAR]`, weil sie Nicht-Dateibezogenes nennen. **Sobald eine der dort
genannten Dateien im Hash abweicht, stuft die Sonde den Punkt auf `[1 BEFUND]`
hoch.**

⇒ **Ein Punkt kann von `2` nach `1` wandern.** Die Zahl der nicht prüfbaren Punkte
ist keine feste Größe, und `A2` („konnte nicht messen ist ein eigenes Ergebnis")
heißt **nicht** „bleibt für immer unmessbar".

⚠️ **Die Bilanz 1/3/10 ist deshalb nicht schlechter als 1/1/12.** Es ist **eine**
Datei — `benchmark.py` — die an zwei weiteren Sperrlistenpunkten vorkommt und
überall denselben Hash-Übergang meldet. Punkt 4 führt beide Dateien getrennt auf:

```
benchmark.py                          ABWEICHUNG   (planmäßig, 37.3)
ergebnisse/benchmark_drawdowns.json   gleich       ⇐ DIE GESCHÜTZTE DATEI
```

⭐ *Der Wächter ändert sich, das Bewachte nicht. Genau das war der Zweck.*

**Nimm diesen Fund ins Ergebnisdokument auf** — er betrifft die Auslegung von 37.3
und `A2` und ist nicht auf TB-91 beschränkt.

---

## ⛔ Was du trotzdem nicht tust

- **Das Abbild nicht neu erzeugen.** Der Befund an 2/4/6 soll sichtbar bleiben,
  bis 37.3 ihn am signierten Tag auflöst.
- **`messgroessen.py` nicht anfassen.** Der schlimmere Fall liegt bei Fable
  (Anfrage 23c) und ist unbeantwortet.
- **`indent=1` und `sort_keys=True` nicht anfassen.** Sie sind absichtlich
  unverändert; jede Abweichung machte die Neurechnung mit `_tb72.json`
  unvergleichbar und entwertete Fables Determinismusnachweis aus 23b.

---

## ⭐⭐ Und dann: Block B, C, D — unverändert

**Die Neurechnung ist bewusst NICHT vorgemessen.** Sie muss `_tb72.json` in
**allen** Werten reproduzieren; eine fremde Python-Umgebung wäre eine zweite
Fehlerquelle, die den Determinismusnachweis entwertet. **Sie gehört auf den Mac
mit `trading-env`, und nur dorthin.**

⭐ *Damit ist TB-91 für dich kürzer geworden: Block A ist Nachrechnen statt Bauen,
und die eigentliche Arbeit fängt bei Block B an.*

---

## In einfacher Sprache

Die Absicherung des Rechenprogramms ist schon gemacht — sie war möglich, ohne die
besondere Programmumgebung des MacBooks, weil dabei nur Quelltext geändert und
nichts gerechnet wird. Die Änderung liegt fertig im Arbeitsverzeichnis.

**Deine Aufgabe bei diesem ersten Teil ist deshalb nicht mehr bauen, sondern
nachprüfen** — sechs Punkte, alle mit vorgerechnetem Vergleichswert. Findest du
eine Abweichung, gilt dein Ergebnis, nicht das vorgerechnete.

Der eigentliche Teil der Aufgabe, das einmalige Neurechnen der Vergleichstabelle,
ist absichtlich liegen geblieben. Er verlangt, dass ein altes Ergebnis auf die
Nachkommastelle genau wiederholt wird, und dafür braucht es dieselbe
Programmumgebung wie damals. Die gibt es nur auf dem MacBook.
