# Journal-Nachtrag (d) — 20.09.2026, TB-65: welche Schranke für den Benchmark gilt — und was das Register dazu wirklich sagt

**Quelle:** Mac-Sitzung **TB-65 Benchmarkschranke pruefen**, 20.09.2026, 12:38
bis etwa 13:00 UTC, `trading-env/bin/python3` 3.9.6, Ausgang `ff98f0a`, Commits
`9ad37e4` (Frage C mit Belegen) und der Abgabe-Commit. Ergebnisdokument
`docs/ERGEBNIS_TB-65_benchmarkschranke.md`, Belege `docs/belege/TB-65/`.
**Rein lesend**: kein Code, kein Registertext, keine Tabelle angefasst.

---

## Was der Auftrag wollte und was er bekam

Eine Prüfung, die auch zum Gegenteil kommen darf: Ist `MINDESTTRAINING_JAHRE =
4` im Krypto-Benchmark eine offene Frage (TB-61) oder ein Verstoss
(Chat-Sitzung)? Drei Fragen, offen gestellt, mit der Gegenthese gleichberechtigt
daneben.

**Bekommen hat er ein Ergebnis, das keine der beiden Sitzungen so gesagt hat:**
Die Chat-Sitzung hat mit der **Folgerung** recht (die Krypto-Zahlen aus TB-61
ruhen auf einer Menge, die kein Registertext vorsieht) und mit der
**Fundstelle** nur zur Hälfte (5.3 allein trägt es nicht — Sperrliste 8,
Registertext 3b (c) und 15.1 tragen es). TB-61 hat mit der **Zurückhaltung**
recht (nichts zu ändern war richtig) und mit der **Rahmung** nicht („4 behalten
/ 0 / andere Regel" — keine der drei Optionen ist das, was 3b (c) sagt). Und das
Register selbst nennt den Zustand seit dem 16.09. weder „offen" noch „Verstoss",
sondern **„Registertext und Umsetzung fallen auseinander"** (16.11, Zeile 7,
Schliesser TB-30b).

---

## Vier Befunde, und was aus jedem folgt

### 1. Acht Zeilen „vier Jahre" im Register — alle acht ersetzt

Gesucht mit acht Mustern, jede Trefferzahl genannt, auch die Nullen
(`MINDESTTRAINING`: null). Jede Zeile mit „vier Jahre" oder „4 Jahre" liegt in
einem ERSETZT-Block oder trägt einen Ersetzungsvermerk — darunter **Sperrliste
Punkt 8**, wo die vier Jahre als **Universums**regel standen, nicht als
Faltenplanregel. Der einzige Text, der die Menge des Benchmarks positiv nennt,
ist 3b (c): die **geladenen** Symbole.

⇒ ⭐ **Ein Vermerk, der nur an einer Stelle gesucht wird, wird nur dort
gefunden.** Die Chat-Sitzung las 5.3 und 3b (c); die tragende Stelle war
Sperrliste 8, drei Bildschirmseiten weiter. *Der Registertext gilt dort, wo er
steht — und die Frage „für was" beantwortet die Überschrift des Kapitels, nicht
der Satz.*

### 2. Bei den Aktien-Bots sind beide Regeln dieselbe Menge — deshalb fiel es nie auf

Gemessen: „Kursdaten ≥ 4 Jahre vor dem 1. Januar der Falte" und „≥ 1 825 Tage
vor dem 31. Dezember" (Loader, Lesart H) grenzen in **40 von 40**
Aktien-Falten dieselben Symbole ab; alle 100 DD-Stufen sind zeichengleich.
Jede Benchmark-Zahl, die bisher im Register stand oder in 21.6 vorhergesagt
wurde, war eine Aktienzahl.

⇒ ⭐⭐ **Eine Regel, die an allen bisherigen Fällen dasselbe liefert wie die
richtige, ist nicht geprüft, sondern unbemerkt.** Dieselbe Lehre wie TB-61
Befund 2 (21.3 (b) fiel erst am ersten Bot auf, bei dem sie etwas ändert) —
hier an einer Zahl, die vier Tage lang als bestätigt galt.

### 3. Der Faktor ist nicht die Nachricht; `erlaubt(f)` ist es

Bei den fünf Krypto-Bots liegt die `DD_Toleranz` bei 100 % je nach Fassung beim
**2,4- bis 5,0-fachen** — „rund dreimal" war die Grössenordnung. Entscheidend ist
etwas anderes: In den Falten 2019–2021 ist der TB-61-Benchmark **leer**, also
`DD_Benchmark(f) = 0`, also `erlaubt(f) = DD_Toleranz = −12,01 %` — in Jahren, in
denen der Loader 6 bis 10 Symbole lädt und der gleichgewichtete Markt −57 bis
−63 % verlor. Unter der geladenen Menge liegt `erlaubt(f)` dort bei −72 bis
−78 %.

⇒ ⭐ **Eine Nebenbedingung wird dort gemessen, wo sie bindet, nicht dort, wo
ihre Zahl steht.** Der Median sah nach „zu streng um Faktor drei" aus; die Falte
sah nach „Abbruchkriterium (b) für alle Krypto-Bots" aus.

### 4. Was das Register wirklich nicht regelt — und was die Chat-Sitzung nicht gesehen hat

3b (c) sagt „in dieser Falte geladen", Lesart H sagt „an mindestens einem
Handelstag". Ob das Symbol dann für die **ganze Falte** (VH) oder **ab dem
Ladetag** (VT) in den Benchmark geht, sagt kein Text. Gemessen ist der
Unterschied gross: `turtle_soup_crypto` 2018 **−87,92 %** (BTC/ETH das ganze
Jahr) gegen **−3,60 %** (ein Handelstag, Loader ab 30.12.2018); `t3_supertrend`
bei 25 % −16,13 gegen −12,89.

⇒ ⭐⭐ **Die offene Frage lag eine Ebene tiefer als der Streit.** Beide
Sitzungen stritten über die Schranke; keine hatte den Zeitbezug der Menge
angesehen. *Wer eine Regel „umsetzt", trifft die Entscheidungen, die der Text
offen lässt — und genau die gehören vor die Rechnung ins Register (K3f).*

---

## Zwei Dinge zur Form

**Die Auflage „die Gegenthese bekommt denselben Platz" hat gewirkt.** Ohne sie
wäre A2 als „Ort und Überschrift" abgetan worden; mit ihr fand sich, dass A2
in der Fundstellenfrage **recht hat** und die tragenden Stellen woanders liegen.
Das Ergebnis ist genauer als beide Ausgangsthesen — und keine von beiden ist
„bestätigt" worden.

**Die Wegwerf-Kopie hat vor der ersten neuen Zahl die alte reproduziert:** V0
gegen `benchmark_drawdowns_neu.json` **0 Abweichungen**, die geladenen Mengen
gegen den Trockenlauf **78 / 78**. Erst danach wurde etwas Neues gerechnet. Ohne
diese Reihenfolge hätte jede Abweichung zwei Erklärungen gehabt.

---

## Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐⭐ | **Ein Registervermerk gilt für das Kapitel, in dem er steht.** Wer ihn auf ein anderes Kapitel anwenden will, braucht dort eine eigene Fundstelle — und findet sie oft (hier Sperrliste 8), aber erst, wenn er sucht |
| ⭐⭐ | **Eine Regel, die an allen bisherigen Fällen dasselbe liefert wie die richtige, gilt als ungeprüft.** Vor dem Eintrag einer Zahl: einen Fall nennen, an dem die Regel etwas anderes liefert als ihre Alternative |
| ⭐ | **Ein Prüfauftrag, der die Gegenthese gleichberechtigt stellt, bekommt ein drittes Ergebnis** — meistens das richtige. Die Form aus `MAC_TB-65` (Tabelle dafür/dagegen mit Fundstellen, ausdrücklicher Satz zur Quellenlage) taugt als Vorlage |
| ⭐ | **Eine Umsetzung, die eine Lücke im Text schliesst, benennt die Lücke** (hier: ganze Falte oder ab Ladetag) **und rechnet beide Seiten vor**, statt eine zu wählen |
| | Ein Skript in einer Wegwerf-Kopie gehört als Beleg ins Repo (`docs/belege/TB-65/tb65_rechnung.py`), sonst ist die Zahl nicht nachrechenbar, sobald die Kopie weg ist |

*Nachgetragen 20.09.2026 aus der Mac-Sitzung TB-65. Quellenvermerk: siehe Kopf.*
