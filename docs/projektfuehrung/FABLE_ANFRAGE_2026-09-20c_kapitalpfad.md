# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026, dritte

**Seine offene Unsicherheit ist gemessen, und die Antwort ist keine der beiden,
die er für möglich hielt. Dadurch trägt sein Ankersatz nicht — und der Ersatz
muss vor den Eintrag, weil er selbst verlangt hat, dass im Register steht, was
der Code tut.**

**Herkunft:** Fables zweite Antwort (`FABLE_ANTWORT_2026-09-20b_kalender.md`)
schlägt für 3b (c) einen Satz zur Zeitachse vor, der den Benchmark an den
Kapitalpfad des Bots bindet, und stellt selbst die Frage, ob dieser Pfad seinen
ersten Tag als 0 führt.

**Die Antwort gehört in den Chat, der TB-61/TB-65/TB-66 bearbeitet.**

---

## Was gemessen wurde, in einer Zeile

⚠️⚠️ **Der Kapitalpfad des Bots hat keinen Tageskalender.** Er ist
**ereignisindiziert** — eine Zeile je ausgeführtem Ein- oder Ausstieg. Die Frage
„führt er den ersten Tag als 0 oder lässt er ihn aus" hat deshalb keine der
beiden Antworten: **er führt Tage überhaupt nicht.**

| Fundstelle | was dort steht |
|---|---|
| `shared/zuteilung.py:720–735` | `equity_curve = []`, danach je Aus- und Einstieg ein `append({"time": zeit, "symbol": …, "capital_after": …})`. Kein Kalender, keine Zeile für einen Tag ohne Trade |
| `shared/messkette.py:139–153` | `calculate_max_drawdown(equity_df, …)` rechnet über `equity_df["capital_after"]` — also über die Ereignisse |
| `research/vorregistrierung/beispieldaten.py:24–26` | ⭐ ausdrücklich: *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und **nicht aus der Tagesreihe nachgerechnet** wird. Das ist auch im echten Lauf so."* |
| `research/vorregistrierung/auswertung.py:246–247` | die Drawdown-Nebenbedingung vergleicht genau dieses `kapital_drawdown_pct` gegen die Grenze aus der Benchmark-Tabelle |

⇒ **Die Nebenbedingung stellt einen ereignisindizierten Bot-Drawdown neben einen
tagesindizierten Benchmark-Drawdown.** Das ist für die Zahl folgenlos — ein
Drawdown hängt an der Reihenfolge, nicht am Kalender —, aber es macht den Satz
*„auf denselben Handelstagen definiert wie der Kapitalpfad des Bots"* zu einer
Beschreibung von etwas, das es nicht gibt.

---

## Der gesendete Text, wörtlich

```
Deine Unsicherheit ist gemessen, und die Antwort ist keine der beiden.


WAS DU GEFRAGT HAST. "Ob der Kapitalpfad des Bots seinen ersten Tag wirklich
als 0 fuehrt oder ihn ebenfalls auslaesst."

WAS GEMESSEN IST. Er fuehrt Tage ueberhaupt nicht. Der Kapitalpfad ist
ereignisindiziert - eine Zeile je ausgefuehrtem Ein- oder Ausstieg, nicht je
Handelstag.

  shared/zuteilung.py:720-735
    equity_curve = []; danach je Aus- und Einstieg
    append({"time": zeit, "symbol": ..., "capital_after": ...}).
    Kein Kalender. Keine Zeile fuer einen Tag ohne Trade.

  shared/messkette.py:139-153
    calculate_max_drawdown rechnet ueber equity_df["capital_after"] -
    also ueber diese Ereignisse.

  research/vorregistrierung/beispieldaten.py:24-26, woertlich:
    "der Kapital-Drawdown einer Falte steht in zellen.csv, weil er im echten
    Lauf aus equity_simulation.py kommt, und nicht aus der Tagesreihe
    nachgerechnet wird. Das ist auch im echten Lauf so."

  research/vorregistrierung/auswertung.py:246-247
    Die Drawdown-Nebenbedingung vergleicht genau dieses kapital_drawdown_pct
    gegen die Grenze aus der Benchmark-Tabelle.

Es gibt daneben eine Tagesreihe je Zelle - sie traegt Sharpe, Rendite und
Exposure. Den Drawdown traegt sie ausdruecklich nicht. Und die Tagesreihen des
echten Laufs existieren noch nicht; der Lauf ist der, der nach dem Tag beginnt.

WAS DARAUS FOLGT FUER DEINEN SATZ. Dein Ankersatz bindet den Benchmark an den
Kalender des Bot-Kapitalpfades. Dieser Kalender existiert nicht. Woertlich
gelesen waere der Benchmark nur an Handelsereignissen definiert - das meinst du
sicher nicht, und es waere eine groessere Aenderung als die Frage, aus der wir
kommen. Deine eigene Auflage - "nur eines darf im Register stehen, und es muss
das sein, was der Code tut" - trifft den Satz also selbst.

UNSER VORSCHLAG: dasselbe Prinzip, an der Groesse verankert, die es wirklich
gibt und die bereits registriert ist - die Loader-Schranke aus 3b (b):

  3b (c), Satz zur Zeitachse. Der Benchmark einer Falte ist an genau den Tagen
  definiert, an denen mindestens ein Symbol des Bots nach 3b (b) handelbar ist.
  Ein Tag, an dem kein Symbol handelbar ist, gehoert nicht zum Benchmark - er
  wird nicht mit Rendite 0 gefuehrt, sondern gar nicht.

Das leistet alles, was dein Satz leisten sollte: es ist in der Sache W, es ist
als Regel formuliert und nicht als Beschreibung eines .dropna(), und es
schliesst C_voll dauerhaft aus (ein Kalender der Falte ist nicht die Menge der
handelbaren Tage). Es behauptet nur nichts ueber einen Bot-Kalender, den es
nicht gibt.

DIE TATSACHENNOTIZ ohne den Halbsatz, der nicht traegt:

  Die Umsetzung laesst den ersten Kurstag je Falte aus, weil pct_change dort
  keine Rendite liefert. Abweichung gegenueber dem Satz: hoechstens ein Tag je
  Falte. Wirkung auf jede registrierte Zahl: null - 0 abweichende Stufen in
  Drawdown und DD_Toleranz ueber 78 x 100. Wird bh_tagesrenditen je aus anderem
  Grund angefasst, ist fillna(0) auf diesem Tag eine Berichtigung des Codes an
  den Satz.

handelstage bleibt Berichtszahl und berichtet die Laenge des gemeinsamen
Kalenders - die W-Spalte. Unveraendert uebernommen.


ZU DEINEM BEFUND t3_supertrend 2018 - nachgesehen, nicht geraten.

Die Falte steht im Plan. Gemessen in benchmark_drawdowns_vt.json:
2018 hat 0 Symbole und 0 Handelstage, 2019 hat 3 Symbole und 136 Handelstage.

Warum sie dort steht, sagt das Modul selbst - faltenplan.py, Z. 39-42:

  "Diese Regel ist Registertext 4a allein. Register 21.3 (b) laesst bei
  Abweichung 3b (a) binden (Trockenlauf des Laufcodes); das rechnet dieses
  Modul nicht, und fuer t3_supertrend weichen beide ab (4a: 2018, 3b (a): 2019,
  weil MIN_HISTORY_DAYS = 730 in der Falte 2018 kein Symbol handelbar macht)."

Also: 21.3 (b) entscheidet den Fall bereits, und kein Code setzt es um. Wir
lesen das als berichtigungsreif, nicht als offene Wahl - der Plan ist an die
registrierte Regel anzugleichen, t3_supertrend beginnt 2019, sieben
Selektionsfalten statt acht. Die Wirkung ist gemessen und bekannt:

  DD_Toleranz t3_supertrend bei 25 / 50 / 100 Prozent Exposure
    mit Falte 2018 (heute):  -12,89 / -24,73 / -45,16
    ohne Falte 2018:         -13,90 / -26,57 / -48,10   (nachgiebiger)

Wir legen es dir vor und vollziehen es nicht, weil die Wirkung bekannt ist und
F17 gilt. Zwei Fragen dazu:

  (1) Ist das eine Berichtigung nach registrierter Regel - dann sag es, und wir
      tragen sie ein wie die Benchmark-Berichtigung.
  (2) Trifft dasselbe Auseinanderlaufen von 4a und 3b (a) noch andere Bots?
      Wir haben bisher nur t3_supertrend gemessen, weil nur dort eine Falte
      leer ist. Ein Bot koennte 4a-fruehe Falten haben, die nicht leer, aber
      duenn sind - dort faellt es nicht auf.
```

---

## In einfacher Sprache

**Was gemessen wurde:** Fable wollte wissen, ob der Verlaufspfad des Bots seinen
ersten Tag mit null führt. Die Antwort: Der Pfad kennt gar keine Tage. Er
verzeichnet nur die Momente, in denen gekauft oder verkauft wird.

**Warum das zählt:** Sein vorgeschlagener Regelsatz bindet den Vergleichskorb an
die Tage des Bot-Pfades — an etwas, das es nicht gibt. Er hat selbst verlangt,
dass im Regelwerk nur steht, was das Programm tut. Also trifft seine eigene
Auflage seinen eigenen Satz.

**Was wir vorschlagen:** Denselben Gedanken, aber festgemacht an der Regel, die
schon im Register steht — ab wann ein Kurs für den Bot handelbar ist. Das sagt
dasselbe und ist wahr.

**Und ein zweiter Punkt:** Er hat nebenbei entdeckt, dass ein Bot ein Jahr in
seinem Plan führt, in dem er gar nichts handeln kann. Das stimmt, es steht seit
dem Vormittag in unseren Unterlagen, und das Regelwerk entscheidet den Fall
bereits — nur setzt es kein Programm um. Wir fragen ihn, ob wir es berichtigen
dürfen, weil die Wirkung auf die Zahlen bekannt ist und wir nach bekannter
Wirkung nichts wählen.
