# Fables Antwort — Kapitalpfad, Zeitachsen-Satz, `t3_supertrend` 2018 (20.09.2026, dritte)

**Eingegangen am 20.09.2026, 18:00 Ortszeit.** Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`.

⭐ **Wörtlich abgelegt, nach der Regel aus Nachtrag (m).**

⚠️⚠️ **Diese Antwort ist die folgenreichste der drei.** Sie nimmt unseren
Zeitachsen-Satz an — und legt daneben einen Befund, der eine der **zwölf
Betreiberfestlegungen vom 14.09.2026** betrifft (Festlegung 1, *„Führendes Mass:
Kapital-Drawdown aus `equity_simulation.py`"*).

---

## 1. Der Zeitachsen-Satz wird übernommen — und die Messung trägt weiter

> Der Zeitachsen-Satz in eurer Fassung ist richtig und geht ins Register:
> verankert an 3b (b), der Grösse, die es gibt und die registriert ist. Meine
> Fassung hat einen Kalender vorausgesetzt, den der Kapitalpfad nicht hat; eure
> setzt nichts voraus. Die Tatsachennotiz ohne den Halbsatz ebenso, `handelstage`
> unverändert.
>
> Was ihr gemessen habt, trägt aber weiter als bis zu diesem Satz, und ich will
> es nicht zwischen den Zeilen lassen:
>
> **Der Drawdown der Nebenbedingung wird auf einem Objekt gerechnet, das das
> Register ausschliesst.** `calculate_max_drawdown` läuft über `capital_after`
> je Ereignis — eine Kurve, die sich nur an Ein- und Ausstiegen bewegt. Das ist
> die Kurvenform aus L1, von der das Projekt am 12.09. gelernt hat, dass sie
> Korrelationen nahe null erzeugt; für den Drawdown tut sie dasselbe mit
> umgekehrtem Vorzeichen: **Sie sieht keinen unrealisierten Verlust.** Eine
> Position, die zwischen Einstieg und Ausstieg 20 % unter Wasser war und mit
> −3 % geschlossen wurde, trägt −3 % zum Drawdown bei. Der Benchmark daneben ist
> tagesgenau bewertet. Die Nebenbedingung vergleicht damit einen systematisch zu
> flachen Bot-Drawdown mit einem vollen Benchmark-Drawdown — am stärksten bei
> den Bots mit langen Haltedauern und hoher Exposure (`turtle_soup_stocks`,
> 100 % im Markt, 14 Tage Median). „Bot und Benchmark leben in derselben Menge"
> gilt dann auf der Symbol- und Zeitachse, aber nicht auf der Bewertungsachse.
>
> Das Register verlangt das andere Objekt schon: 1a (tägliche
> Netto-Mark-to-Market-Renditen des Kapitalpfads), 2a (Falten-Rendite als Summe
> täglicher MtM-Renditen), und die Objektregel aus AF.1. Ihr sagt, die Tagesreihe
> je Zelle existiert und trägt Sharpe, Rendite und Exposure — den Drawdown
> „ausdrücklich nicht", weil `beispieldaten.py` ihn aus `equity_simulation.py`
> nimmt. **Der Drawdown gehört aus derselben Tagesreihe wie der Sharpe.** Sonst
> wird auf einem Objekt selektiert (Sharpe, täglich) und auf einem anderen
> beschränkt (Drawdown, ereignisweise) — genau die Inkonsistenz aus M.3, eine
> Ebene tiefer.
>
> Einordnung nach F17: AF.2 Nr. 1 nennt „Kapital-Drawdown aus
> `equity_simulation.py`" — als Verweis auf das Skript, das den Kapitalpfad
> erzeugt; 1a und 2a sagen, wie der Pfad bewertet wird. Das ist ein Widerspruch
> innerhalb des Registers, aufzulösen zugunsten der Seite mit dem Grund (L1),
> also Berichtigung — mit der Ehrlichkeit, dass die Wirkung bekannt und gegen
> alle neun Bots gerichtet ist: Der tägliche Drawdown ist nie flacher als der
> ereignisweise. Ich würde es trotzdem vor dem Tag tun, weil eine
> Nebenbedingung, die unrealisierte Verluste nicht sieht, in genau den Falten
> nachgiebig ist, in denen sie binden soll (2020, 2022). Der ereignisweise
> Drawdown bleibt als Berichtswert. Sperrliste: ja, das berührt sie — es ist die
> Änderung, für die die Sperrliste die Wiederholung des Laufs vorsieht, und der
> Lauf hat noch nicht begonnen.
>
> > **Registertext 4, Präzisierung.** Der Kapital-Drawdown einer Falte für die
> > Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads
> > gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c)). Der
> > ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht
> > bewertet.

---

## 2. `t3_supertrend` 2018 — (1) Berichtigung, (2) eine Wache statt einer Messung

> **(1) Ja, Berichtigung.** 21.3 (b) ist registrierte Regel (bei Abweichung
> bindet der Trockenlauf), `faltenplan.py` setzt sie nicht um und sagt es
> selbst. Plan an registrierte Regel: `t3_supertrend` beginnt 2019, sieben
> Falten. Die bekannte Wirkung (nachgiebiger: −45,16 → −48,10 bei 100 %) in die
> Notiz, wie bei der Benchmark-Berichtigung. Dass die Richtung diesmal zugunsten
> des Bots geht, ändert an der Kategorie nichts — die Quelle des Grundes ist die
> Regel.
>
> **(2) Andere Bots: nicht messen, sondern die zweite Implementierung
> abschaffen.** Das Auseinanderlaufen von 4a und 3b (a) hat einen Mechanismus —
> `MIN_HISTORY_*` macht Symbole später handelbar, als 4a aus der Datenlage
> rechnet — und er wirkt auf die Faltenexistenz nur, wenn eine ganze Falte leer
> bleibt. Dünne, nicht leere Falten zählen nach Lesart H, und ihre Symbolzahl
> kommt ohnehin aus dem Trockenlauf. Für die Existenz der ersten Falte genügt
> deshalb ein Vergleich je Bot: erste Falte mit mindestens einem geladenen Symbol
> laut Trockenlauf gegen erste Falte laut Plan. Neun Zahlen, mechanisch.
>
> Aber das ist derselbe Fall wie 2.3 am 15.09. — zwei Implementierungen derselben
> Frage laufen irgendwann auseinander, und die Wache fängt es erst, wenn der Lauf
> vorbereitet ist. **`faltenplan.py` sollte die erste Falte aus dem Trockenlauf
> beziehen, nicht aus 4a nachrechnen.** 4a bleibt die Regel; 3b (a) über den
> Trockenlauf ist ihre operative Form; der Plan ist eine Ableitung daraus, keine
> Parallelrechnung. Dann ist die Frage (2) nicht einmal zu stellen — der Plan
> kann nicht abweichen. Bis das umgebaut ist: der Neun-Zahlen-Vergleich als Wache
> am Laufbeginn, Abbruch bei Abweichung.

---

## Seine offene Unsicherheit

> **Unsicher:** ob die Tagesreihe je Zelle, die den Sharpe trägt, tatsächlich
> Mark-to-Market bewertet ist oder nur die Ereignisrenditen auf Tage verteilt —
> wenn Letzteres, ist Punkt 1 kein Umbau der Drawdown-Rechnung, sondern der
> Tagesreihe, und dann grösser. Das entscheidet ein Blick auf ihre Erzeugung,
> nicht diese Antwort.

⭐⭐ **Nachgesehen am 20.09.2026, 18:05 — die Antwort ist wieder keine der
beiden, und sie macht seinen Punkt 1 kleiner, nicht grösser:** Die Tagesreihe je
Zelle **existiert nicht und hat keinen Erzeuger**. Siehe
`FABLE_ANFRAGE_2026-09-20d_tagesreihe.md`.
