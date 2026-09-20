# Fables Antwort — Registertext 3b (c): VH oder VT (20.09.2026)

**Eingegangen am 20.09.2026, 15:19 Ortszeit.** Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20_benchmarkfenster.md`.

⭐ **Wörtlich abgelegt, nach der Regel aus Nachtrag (m):** *„Jede Rückfrage an
den Betreiber und seine Antwort kommen wörtlich in den Bericht — sonst leben sie
nur im Sitzungsverlauf, der mit der Sitzung verschwindet."*

---

## Die Festlegung

> **VT — und der Grund steht im Registertext selbst, nicht in der Wirkung.**

**Seine Begründung, in seinen Worten:**

> Der Wortlaut „in dieser Falte geladen" war meiner, und er war unpräzise. Der
> Begründungssatz war es nicht: *„Bot und Benchmark leben in derselben Menge."*
> Die Menge, in der ein Bot lebt, ist tagesgenau — er kann ein Symbol an keinem
> Tag halten, an dem sein Loader es nicht geladen hat. Ein Benchmark, der es für
> die ganze Falte hält, ist eine Alternative, die dem Bot nicht offenstand, und
> genau dagegen war 3b (c) geschrieben.

**Zwei Gründe, beide aus dem Register, keiner aus der Messung:**

| | |
|---|---|
| **1** | ⚠️ **Unter VH ist die Nebenbedingung dort leer, wo sie binden soll.** Der Bot hat in Falte 2018 vor dem 30.12. keine Position, sein Drawdown ist nahe null. Der zulässige wäre 1,25 × −87,9 % — **jeder Parametersatz besteht, egal was er tut.** *Eine Nebenbedingung, die in dünnen Falten automatisch erfüllt ist, prüft nichts* — und die dünnen Falten sind genau die, in denen 3b (d) Rauschen erwartet |
| **2** | ⚠️⚠️ **Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme.** Benchmark −88 %, Bot ≈ 0 ⇒ **+88 Prozentpunkte Alpha daraus, dass der Bot nichts halten *konnte*.** ⭐ *Die Nullen-als-Diversifikation-Fehlerklasse aus `L1`, in neuer Kleidung.* Rang 3 misst dann, **wie lange der Loader gebraucht hat** |

⭐ **Zu Lesart H — kein Widerspruch:** H beantwortet, **ob** eine Falte zählt (ab
einem handelbaren Tag). VT beantwortet, **was der Benchmark an jedem Tag hält**.
**H mit VH zusammen wäre der Widerspruch** — eine Falte, die wegen eines Tages
zählt, bekäme einen Benchmark aus 250 Tagen, an denen der Bot nicht dabei war.

⭐ **Einordnung nach F17: Berichtigung.** Der Wortlaut wird an den Zweck
angeglichen, der im selben Registertext steht. **Die Wirkung ist bekannt und
geht gegen die Bots** (VT ist die strengere Lesart in den frühen Krypto-Falten);
sie wird in der Notiz vermerkt. **Sie ist nicht der Grund.**

---

## Der neue Wortlaut 3b (c), wörtlich

> Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen gebildet, die
> der Loader des Bots an diesem Tag handelbar macht: gleichgewichtet, täglich
> rebalanciert (Konvention; sie ist die einzige Gewichtung, die bei wechselnder
> Menge ohne weitere Regel auskommt). Tage, an denen kein Symbol handelbar ist,
> tragen Rendite 0. Derselbe Benchmark gilt für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3. Bot und Benchmark leben an jedem Tag in
> derselben Menge.

**Der alte Wortlaut bleibt stehen, als ERSETZT gekennzeichnet**, mit der Notiz:
Lesart VT, Wirkung gemessen und bekannt (`turtle_soup_crypto` 2018: **−3,60 %**
statt −87,92 % bei 100 % Exposure; DD-Toleranz je nach Bot **2,4- bis
5,0-fach**), Grund der Zweck-Satz von 3b (c).

⭐ **Die Toleranzuntergrenze bleibt** und tut unter VT genau das, wofür sie da
ist: *„Eine Falte mit einem Handelstag bekommt nicht −4,5 % als Grenze, sondern
den Median."*

⭐ **Der Vierjahresfilter in `benchmark.py` geht mit** — *„das Verfahren-A-Artefakt,
das mit `MINDESTTRAINING` schon einmal gegangen ist; Code an registrierte Regel,
Berichtigung."*

---

## Die beiden Nebenfragen

| | Antwort |
|---|---|
| **1 — Rang 3** | ⭐ **Dieselbe Lesart, zwingend.** *„Es ist ein Benchmark-Objekt mit zwei Verwendungen, nicht zwei Benchmarks."* Rang 3 mit VH erzeugte das Phantom-Alpha aus Grund 2; der Rang-3-Vergleich (V.4) ist ohnehin tagesgenau gebaut. **Ein Satz in 3b (c) genügt, keine eigene Festlegung** |
| **2 — Form** | ⭐ **Registertext, nicht Tatsachennotiz.** *„Eine Tatsachennotiz kann sie festhalten, nicht schaffen"* (seine Antwort vom 19.09., Frage c). **3b (c) selbst wird neu gefasst**; die gemessenen Zahlen kommen in die Berichtigungsnotiz |

---

## ⚠️ Eine Begriffskorrektur, die er nebenbei anbringt

> *„Vor dem Tag ist es eine **Berichtigung des Registers** und ein **Bug-Fix am
> Auswerter**; **‚Amendment' gehört zur Sperrliste des Codes, nicht zum
> Register** — die Unterscheidung bleibt wichtig, sobald der Tag steht."*

⚠️ **Das betrifft unseren Sprachgebrauch seit dem 19.09.** Registerabschnitt
21.9 und die Backlog-Zeile `T56b.3` nennen den Vorgang durchgehend „Amendment".
**Nach Fable ist das für den Registerteil falsch** — für
`benchmark_drawdowns.json` (Sperrliste Punkt 4) bleibt es richtig.
⇒ **Zu berichtigen, wo es den Registertext meint.**

---

## ⭐ Seine offene Unsicherheit — hier beantwortet

**Er schreibt:**

> **Unsicher:** ob „gleichgewichtet, täglich rebalanciert" mit der heutigen
> `benchmark.py` übereinstimmt oder ob dort Buy-and-Hold ab Eintritt gerechnet
> wird — beides ist vertretbar, aber nur eines darf im Register stehen, und es
> muss das sein, was der Code tut. **Vor dem Eintrag nachsehen.**

**Nachgesehen am 20.09.2026, 15:22, `research/vorregistrierung/benchmark.py`,
`bh_tagesrenditen()`:**

```python
rahmen = pd.DataFrame(reihen).sort_index()
return rahmen.pct_change().mean(axis=1, skipna=True).dropna()
```

⭐⭐ **Seine Formulierung trifft den Code.** Der Mittelwert der Tagesrenditen
über die Symbole, Tag für Tag, ist **gleichgewichtet und täglich
rebalanciert** — ein echtes Buy-and-Hold hätte driftende Gewichte. **`skipna=True`
lässt an jedem Tag genau die Symbole zählen, die eine Rendite haben** — das ist
VT auf der Datenseite bereits.

⚠️ **Zwei Befunde dazu, beide klein:**

| | |
|---|---|
| **1** | **Der Docstring nennt es *„Gleichgewichteter Buy-and-Hold"***. ⚠️ **Der Name widerspricht der Rechnung** — dieselbe Fehlerklasse wie `K1h` (`KURSDATEN_DIR_VERBOTEN`) und `T44.10` (`_ist_geraet`). **Zu berichtigen, wenn die Datei ohnehin angefasst wird** |
| **2** | ⚠️ **`.dropna()` entfernt Tage ohne handelbares Symbol; der neue Registertext sagt, sie tragen Rendite 0.** ⭐ **Für den Drawdown gleichwertig** — ein Tag mit 0 % bewegt den Kapitalpfad nicht. ⚠️ **Für die berichtete `handelstage`-Zahl nicht**, weil der Code solche Tage gar nicht zählt. **Vor dem Eintrag zu entscheiden: Wortlaut an den Code oder Code an den Wortlaut** |

---

## Was daraus folgt

| | |
|---|---|
| ⭐ | **Für die vier Aktien-Bots ändert sich nichts** — TB-65 hat gemessen: V0 und die Loader-Fassung sind auf allen 100 Stufen und in allen 40 Falten zeichengleich. **Die Sperrlisten-Änderung kann dort sofort vollzogen werden** |
| ⚠️ | **Für die fünf Krypto-Bots erst nach der Neufassung** — Registertext 3b (c) neu, `benchmark.py` auf VT, Lauf wiederholen |
| ⚠️ | **`benchmark_drawdowns_neu.json` aus TB-61 ist damit überholt**, bevor es je registriert wurde |
