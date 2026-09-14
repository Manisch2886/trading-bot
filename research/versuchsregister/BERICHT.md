# TB-29 — Versuchsregister: Bericht

**Stand: 13.09.2026.** Erhebung, keine Änderung. Diese Untersuchung fasst
**keinen** Bot-Code an (Methodik-Prinzip 14 des Übergabeprotokolls): sie liest
Quelltext und abgelegte Ergebnisdateien, führt nichts aus, importiert nichts
und überschreibt nichts. Beleg in Abschnitt 6.

Das Register selbst — eine Zeile je Versuchsblock, Summen je Bot, Gesamtsumme —
steht in **[`REGISTER.md`](REGISTER.md)**. Dieser Bericht erklärt, **wie**
gezählt wurde, **was dabei herauskam**, und **was sich nicht zählen liess**.

---

## 1. Die Antwort zuerst

> **2 798 belegbare Rasterauswertungen** über die gesamte Projektgeschichte —
> jede einzelne belegt durch eine abgelegte Ergebnisdatei oder durch das
> Raster im Quelltext, das den Lauf definiert. Konservativer gerechnet, nach
> Abzug aller Wiederholungen derselben Kombination: **653 verschiedene
> Parameter-Kombinationen**.
>
> **Und ein zweiter Befund, der die erste Zahl erst einordnet:** die
> Git-Historie beginnt am **02.09.2026** mit einem Commit, der bereits drei
> vollständige Bots samt Rastern und Ergebnisdateien enthält. Über alle
> 21 Optimierungsstellen hinweg hat sich seither **keine einzige Rastergrösse
> geändert** — mechanisch nachgerechnet für jeden Commit. Die Runden, nach
> denen der Auftrag fragt, liegen damit fast vollständig **vor** dem ersten
> Commit und sind in diesem Repo nicht sichtbar.

| je Bot | Rasterauswertungen | verschiedene Kombinationen |
|---|---:|---:|
| `elliott_wave_stocks` | 1 085 | 264 |
| `elliott_wave` | 977 | 252 |
| `t3_supertrend` | 406 | 81 |
| `rsi2_crypto` | 73 | 18 |
| `turtle_soup_crypto` | 49 | 12 |
| `turtle_soup_stocks` | 49 | 12 |
| `rsi2_mean_reversion` | 25 | 6 |
| `volatility_breakout` | 17 | 4 |
| `volatility_breakout_crypto` | 17 | 4 |
| bot-übergreifend | 100 | — |
| **Summe** | **2 798** | **653** |

---

## 2. Wie gezählt wurde

### 2.1 Das Zählmass

Gezählt werden **Auswertungsstellen**: jeder Aufruf einer Funktion, deren Name
mit `evaluate_combination` beginnt, gewichtet mit dem Produkt der Schleifen, in
denen er steht. Eine Kombination, die ausgewertet und anschliessend vom
Mindestfilter verworfen wird, zählt mit — sie wurde geprüft, und darauf kommt
es für die Multiplizität an.

Nicht gezählt wird das **Anlegen** einer Kombinationsliste.
`combinations = list(itertools.product(...))` erzeugt Tupel, wertet aber nichts
aus; erst die Schleife darüber tut das. Die Liste geht nur als *Schleifenlänge*
ein. Ohne diese Unterscheidung hätte `elliott_wave` 36 + 36 = 72 statt 36.

### 2.2 Warum ein AST-Zähler und kein Ablesen von Hand

Die neun `multi_symbol_optimise.py` bilden ihr Raster in **vier verschiedenen
Formen**:

| Form | Bot | Kombinationen |
|---|---|---:|
| `itertools.product(A, B, C)` | `elliott_wave`, `t3_supertrend` | 36 / 81 |
| verschachtelte `for`-Schleifen | `rsi2_crypto`, beide Turtle-Soup-Bots, beide Volatility-Breakout-Bots | 18 / 12 / 4 |
| List-Comprehension | `rsi2_mean_reversion` | 6 |
| Schleife mit zusätzlichem `append` je Zwischenstufe | `elliott_wave_stocks` | 64 |

Die vierte Form ist die tückische: `elliott_wave_stocks` hängt je Kursziel eine
Zeile an **und** je (Zigzag, Stop) eine weitere für „kein Kursziel". Wer nur
die Zuweisung `combinations = []` ansieht, findet dort die Länge 0 — und meldet
für diesen Bot stillschweigend **null** Kombinationen. Genau dieser Fehler ist
bei der Entwicklung des Werkzeugs aufgetreten und wird durch eine eigene
Zusicherung im Test festgehalten.

`research/versuchsregister/raster.py` löst zusätzlich Importe aus dem
Nachbarmodul auf: die sechs eigenständigen `multi_symbol_walk_forward.py`
holen ihre Rastergrenzen per `from multi_symbol_optimise import …`, die drei
übrigen rufen sogar `run_multi_optimisation` direkt auf. Ohne diese Auflösung
lieferten sechs von neun Walk-Forward-Stellen `unklar` und drei die Zahl **1**.

### 2.3 Was der Zähler nicht kann — und dann auch sagt

Eine Schleife über etwas statisch Unbekanntes (eine Datei, ein
Symbolverzeichnis, ein Funktionsergebnis) macht die Datei `unklar`; der Zähler
gibt dann den Grund aus statt einer Zahl. **Und er gibt nie 0 aus:** eine Null
fällt in einer Summe nicht auf und wäre von „null Versuche" nicht zu
unterscheiden. Findet er keine Auswertungsstelle, meldet er das als Lücke.

Der Fall ist nicht theoretisch. `research/elliott_wave_params/search.py` baut
seine Kombinationen in einem Generator (`combos()`), den der Zähler nach
diesem Mass **nicht** zählen kann — er meldet das, und die 252 Kombinationen
dieses Rasters kommen stattdessen aus der direkten Zeilenzählung der abgelegten
Dateien (je 252 Zeilen). Eine frühere Fassung des Zählers gab hier 756 aus:
rechnerisch richtig, aber aus dem falschen Grund (drei Fundstellen von
`combos()` mal 252). Eine Zahl, die nur zufällig stimmt, ist schlimmer als eine
gemeldete Lücke.

### 2.4 Drei unabhängige Belegarten

Für jede Zahl im Register gibt es mindestens eine, meist zwei Quellen:

1. **Der Quelltext** — das Raster, das den Lauf definiert (AST-gezählt).
2. **Die abgelegte Ergebnisdatei** — eine Zeile je tatsächlich gerechneter
   Kombination. Belastbarer als die Rastergrösse, weil dort steht, was
   gerechnet wurde, nicht was gerechnet werden sollte.
3. **Die ungefilterten Rasterläufe unter `research/`** — `drawdown_reihenfolge`
   und `elliott_wave_params` legen *alle* Kombinationen ab, samt Spalte
   `besteht_mindestfilter`. Damit lässt sich die Differenz zwischen
   Rastergrösse und abgelegter Zeilenzahl **nachrechnen** statt erklären.

---

## 3. Die Befunde

### 3.1 Wo Rastergrösse und Zeilenzahl auseinandergehen

Bei vier von neun Bots ist die abgelegte Datei kürzer als das Raster. Die
Ursache ist in allen vier Fällen nachgerechnet:

| Bot | Raster | abgelegt | bestehen laut `drawdown_reihenfolge` | passt? |
|---|---:|---:|---:|---|
| `rsi2_crypto` | 18 | 6 | 6 | ja |
| `turtle_soup_crypto` | 12 | 8 | 8 | ja |
| `t3_supertrend` | 81 | 23 | 64 **mit** / **23 ohne** BTC-Regimefilter | ja, ohne Filter |
| `elliott_wave (Einzelsymbol)` | 36 | 30 | — | Mindestfilter |

Der t3-Fall ist der interessanteste: die abgelegte Datei, **die die
Parameterwahl dieses Bots getragen hat**, stammt aus der Zeit *vor* dem
BTC-Regimefilter. Das steht so auch in
`research/drawdown_reihenfolge/adapters.py` und ist damit nicht neu — aber es
heisst, dass die 23 Zeilen einen Bot-Zustand beschreiben, den es heute nicht
mehr gibt.

### 3.2 Wo sie **nicht** auseinandergehen — und das der Befund ist

`elliott_wave` (36/36) und `elliott_wave_stocks` (64/64): hier besteht jede
Kombination den Mindestfilter. Auf **korrigierter** Grundlage — nach der
Look-Ahead-Behebung vom 07.09.2026 — besteht bei `elliott_wave` dagegen
**keine einzige** der 36 Kombinationen mehr
(`research/elliott_wave_lookahead/BERICHT.md`: „36 von 36" gegen „0 von 36";
unabhängig nachgezählt in
`drawdown_reihenfolge/results/elliott_wave_raster.csv`: 0 bestanden), bei
`elliott_wave_stocks` noch 17 von 64.

Die beiden abgelegten Dateien beschreiben also einen Rechenstand, der
nachweislich falsch war. Sie sind trotzdem der beste Beleg dafür, **dass**
dieser Lauf stattgefunden hat — und genau dafür stehen sie im Register.

### 3.3 Die Runden: null sichtbare, mindestens vier belegte

`versuchsregister.py --historie` rechnet die Rastergrösse **für jeden Commit
neu** aus dem damaligen Quelltext und vergleicht. Ergebnis über alle
21 Stellen: **0 Rasteränderungen**; auch die Rastergrenzen sind unverändert.

Das heisst nicht, dass es nur eine Runde gab. Es heisst, dass die Runden vor
dem ersten Commit stattfanden. Zwei Spuren belegen sie, ohne sie zählbar zu
machen:

* **Der Kommentar, der auf ein verlorenes Werkzeug zeigt.**
  `strategies/elliott_wave_stocks/multi_symbol_optimise.py:39` begründet die
  Stop-Obergrenze mit „erweitert (bis 8 %) nach Erkenntnis aus
  `compare_exit_rules.py`". Diese Datei liegt nicht im Repo und hat **nie**
  darin gelegen (`git log --all` auf den Dateinamen: leer). Eine Rastergrenze
  wurde verschoben, weil ein Ergebnis dazu Anlass gab — die Selektion ist
  belegt, ihr Umfang nicht.
* **Die Universumsentwicklung.** Übergabeprotokoll 3.3 beschreibt
  Top 25 → 50 → 100 → 150 mit jeweils angehobenen Mindestschwellen. Das sind
  mindestens vier Durchgänge des Aktien-Elliott-Rasters; abgelegt ist die
  Ergebnisdatei **eines** davon.

### 3.4 Jede Ergebnisdatei wurde genau einmal abgelegt

Alle neun `multi_symbol_optimisation_results.csv` erscheinen **je einmal** in
der Git-Historie — beim Anlegen des Bots — und nie wieder. Läufe danach (und es
gab sie: sonst wäre die Look-Ahead-Korrektur ohne Nachrechnung geblieben)
haben entweder dieselbe Datei lokal überschrieben oder ihr Ergebnis nur auf
den Bildschirm geschrieben.

Bei `elliott_wave` ist das besonders sichtbar: seine Datei liegt bis heute
unter dem alten Pfad `results/multi_symbol_optimisation_results.csv`, obwohl
`strategy_paths.py` längst `results/elliott_wave/` vorsieht — und dieser Ordner
existiert nicht. Seit der Umstellung hat dieser Bot **keinen**
Optimierungslauf mehr abgelegt.

### 3.5 Was ausdrücklich nicht mitgezählt wurde

`order_sensitivity` (4 500 Läufe), `determinismus` (180), `exposure_messung`,
`tb24_haltedauern`, `pnl_2025_fixed_size`, `sync_check` und die übrigen
Prüf-Untersuchungen rechnen viel, **wählen aber nichts aus**: sie permutieren
oder vermessen dieselbe Konfiguration. Sie erhöhen die Multiplizität einer
Selektion nicht und stehen deshalb mit Begründung in `REGISTER.md` 3.4 statt
in der Summe. Die Versuchszahl mit ihnen aufzufüllen wäre einfach gewesen und
falsch.

---

## 4. Einordnung für die Deflated Sharpe Ratio

Bei **N** Versuchen mit reinem Rauschen liegt das erwartete Maximum der
standardisierten Kennzahl bei etwa **√(2 ln N)** Standardabweichungen
(führender Term der Extremwertnäherung, der Kern der DSR nach
Bailey/López de Prado). Der Schätzfehler eines Sharpe aus **T** Beobachtungen
ist etwa 1/√T; die Rauschschwelle, auf ein Jahr hochgerechnet, also
√(2 ln N)/√T · √252.

`python3 research/versuchsregister/versuchsregister.py --dsr`

| N | √(2 ln N) | Schwelle T = 252 (1 Jahr) | Schwelle T = 1 260 (5 Jahre) |
|---:|---:|---:|---:|
| 36 (kleinstes Bot-Raster mit Vorgeschichte) | 2,677 | 2,68 | 1,20 |
| 81 (grösstes einzelnes Bot-Raster) | 2,965 | 2,96 | 1,33 |
| 237 (alle neun Bot-Raster zusammen) | 3,307 | 3,31 | 1,48 |
| **653** (verschiedene Kombinationen) | **3,600** | **3,60** | **1,61** |
| **2 798** (belegbare Auswertungen) | **3,984** | **3,98** | **1,78** |

**Nicht bewertet, nur ausgerechnet** — ob daraus etwas folgt, entscheidet der
Nutzer. Zwei Eigenschaften der Rechnung gehören aber dazu, weil sie die
Richtung des Fehlers bestimmen:

* Die Näherung setzt **unabhängige** Versuche voraus. Benachbarte Rasterpunkte
  sind es nicht — Stop 2 % und Stop 3 % handeln weitgehend dieselben Trades.
  Die effektive Zahl unabhängiger Versuche liegt unter N, die Schwelle ist
  damit **eher zu hoch** angesetzt.
* Dem steht entgegen, dass N selbst eine **Untergrenze** ist (Abschnitt 3.3
  und 3.4): die Runden vor dem ersten Commit fehlen vollständig.

Bemerkenswert ist der Abstand zwischen den Zeilen: zwischen dem kleinsten
Einzelraster (N = 36) und der Gesamtsumme (N = 2 798) liegt in der
Fünf-Jahres-Spalte ein Unterschied von 1,20 zu 1,78 Sharpe. Die Multiplizität
wächst mit dem Logarithmus — **hundertmal mehr Versuche heben die Schwelle
nicht um das Hundertfache, sondern um etwa die Hälfte.** Das ist der Grund,
warum es sich lohnt, die Zahl zu belegen statt zu schätzen: eine
Grössenordnung daneben verschiebt die Schwelle nur wenig, und genau deshalb
ist eine belegte Untergrenze brauchbar, obwohl sie unvollständig ist.

---

## 5. Was fehlt — ausdrücklich benannt, nicht geschätzt

1. **Informelle Versuche von Hand, bevor ein Raster stand.** Nicht
   rekonstruierbar, weder Zahl noch Richtung. Bekannte Beispiele: die
   Zeitrahmen-Odyssee des T3-Bots (1 h → 15 min → 4 h) und die verworfene
   Erweiterung auf alle 503 S&P-500-Werte.
2. **Läufe, deren Ergebnisdatei überschrieben wurde.** Jede der neun Dateien
   wurde genau einmal committet (Abschnitt 3.4); alles danach ist lokal
   überschrieben oder nie abgelegt worden.
3. **Varianten, die verworfen wurden, bevor sie in einen Bericht kamen.**
   `compare_exit_rules.py` ist der eine Fall, der eine Spur hinterlassen hat —
   einen Kommentar. Wie viele es sonst gab, steht nirgends.
4. **Die Rundenzahl vor dem 02.09.2026.** Das Repo beginnt mit einem fertigen
   Projekt. Die gesamte Entwicklung davor — nach Übergabeprotokoll mehrere
   Wochen, drei Bots, mehrere Universumserweiterungen — ist versionsgeschichtlich
   nicht vorhanden.

**Das Ergebnis ist eine Untergrenze, und genau so gehört es benannt.** Eine
Untergrenze, die belegt ist, ist mehr wert als eine Schätzung, die es nicht
ist.

---

## 6. Nachweis: nichts verändert

```bash
git status --porcelain
#   ?? research/versuchsregister/          (nur der neue Ordner)

git diff origin/main HEAD --name-only
#   nur Dateien unter research/ und docs/
```

* **Kein Produktivcode angefasst.** Die 21 Optimierungsstellen,
  `live_params.py`, `forward_test.py` und `equity_simulation.py` werden
  ausschliesslich **gelesen** — der Zähler arbeitet auf dem AST, es wird nichts
  importiert und nichts ausgeführt.
* **Keine `results/*.csv` überschrieben.** `shared/ergebniskurven.py` meldet
  nach dem Lauf **denselben** Stand wie auf unverändertem `main`. Zum Stand
  selbst siehe Abschnitt 7.
* **Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage.**

Der Test `test_versuchsregister.py` prüft beides mit (Abschnitt 11 seiner
Ausgabe): `git status` darf nichts ausserhalb von `research/` und `docs/`
melden, und `git diff` gegen `HEAD` muss in allen Produktivordnern leer sein.

---

## 7. Zwei Hinweise zur Umgebung

**`shared/ergebniskurven.py` meldet `9x ABWEICHEND`, nicht `9x AKTUELL`** — und
zwar **schon auf unverändertem `origin/main`**, nachgewiesen in einem separaten
Arbeitsverzeichnis. Das ist ein bekannter, gewollter Zustand: TB-26 hat die
Zuteilungskaskade eingeführt und die abgelegten Kurven **bewusst nicht** mit
erneuert (Übergabeprotokoll, Nachtrag vom 13.09.2026). Was diese Untersuchung
zusichern kann und zusichert, ist die **Unverändertheit**: vorher wie nachher
9× ABWEICHEND, kein einziges `results/*.csv` angefasst.

Zwei Tests (`shared/test_stabile_sortierung.py`,
`shared/test_wellenauswahl.py`) schlagen aus genau diesem Grund je mit **einer**
Zusicherung fehl — ebenfalls schon auf `main`. Einzelheiten und der Basislauf
stehen in `TESTAUFTRAG_TB-29.md`.

**`--historie` braucht eine vollständige Git-Historie.** In einem flachen Klon
(`git clone --depth …`, wie ihn manche Arbeitsumgebungen anlegen) bricht der
Befehl mit einem Hinweis ab, statt eine zu niedrige Rundenzahl zu melden — der
Unterschied ist gross: flach sah die Historie nach 137 Commits ab dem
08.09.2026 aus, vollständig sind es 274 ab dem 02.09.2026.

---

## 8. Offene Punkte

1. **Die Elliott-Ergebnisdateien sind überholt.** `results/multi_symbol_…csv`
   (36 Zeilen) und `results/elliott_wave_stocks/…` (64) beschreiben den Stand
   vor der Look-Ahead-Korrektur. Ob sie neu erzeugt werden sollen, ist eine
   Nutzerentscheidung — diese Untersuchung ändert nichts.
2. **`results/elliott_wave/` existiert nicht.** Der Bot legt seit der
   Umstellung auf `strategy_paths.py` keine Optimierungsergebnisse mehr ab.
   Ob das ein Versäumnis oder Absicht ist, geht aus dem Code nicht hervor.
3. **Das Register braucht eine Pflegestelle.** Der Wächter meldet Abweichungen,
   trägt sie aber nicht nach. Wer ein Raster erweitert, muss `STAND_*` in
   `versuchsregister.py` **und** `REGISTER.md` nachziehen. Sinnvoll wäre, den
   Wächter in denselben Lauf zu hängen wie `shared/ergebniskurven.py`.
4. **Die Unabhängigkeitsannahme der DSR ist nicht geprüft.** Wie viele der
   653 Kombinationen effektiv unabhängig sind, liesse sich aus den
   Trade-Überschneidungen messen (`research/tb24_haltedauern` hat die Daten
   dafür schon). Das wäre die nächste Verschärfung der Zahl — und die einzige,
   die sie **senken** statt anheben würde.
