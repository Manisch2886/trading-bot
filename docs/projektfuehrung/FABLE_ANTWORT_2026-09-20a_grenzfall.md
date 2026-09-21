# FABLE_ANTWORT 2026-09-20a — Grenzfall der Drawdown-Nebenbedingung

*Bezug: TB-73, Register 24.2 / 24.6. Drei Teile.*

> **Nachtrag 21.09.2026 (bei Nachlieferung der Datei):** Zwei Aktenzeichen im Text unten sind falsch und bleiben unverändert stehen, damit die Fassung vom 20.09. erkennbar bleibt. Richtig ist: *Festlegung 11* = „DSR ist Bericht, nicht Tor", *Festlegung 12* = „Es kann sein, dass kein einziger Bot die Schwelle erreicht"; *Festlegung 10* ist die DSR-Basis N = 653 und trägt den Satz über Bleibt/Geht nicht — dieser Satz hat kein Festlegungs-Aktenzeichen, er folgt aus den Abbruchkriterien in Abschnitt 7 und Registertext 6b. Der Satz „Falls (b) im Registertext fehlt … Berichtigung" ist gegenstandslos: (b) steht wörtlich in Abschnitt 7, der Verweis dorthin genügt. Siehe FABLE_ANTWORT_2026-09-21b.

---

## (1) Der Grenzfall ist entschieden — seit dem 14.09., als Abbruchkriterium (b)

Das Register sagt es, nur vielleicht nicht dort, wo ihr gesucht habt. In der Vorabfestlegung vom 14.09. (Checkliste Punkt 4, von AF.7 als Grundlage von TB-30a übernommen) lauten die Abbruchkriterien für einen Bot, der nicht bleibt:

> (a) Falten-Median des Netto-Sharpe ≤ 0. **(b) Kein Parametersatz erfüllt die Drawdown-Nebenbedingung in allen Falten.** (c) Rang-3-Klasse „geht". (d) Gewinner ist Spitze und der beste Nicht-Spitzen-Punkt erfüllt (a).

Und Festlegung 10 sagt, dass Bleibt/Geht über diese Kriterien läuft; Registertext 6b sagt, was „geht" heisst: **Der Bot geht auf Schatten.** Sein Budget hält die statische Benchmark-Position in Höhe seines mittleren Exposures; er läuft mit den heutigen Parametern als Schatten weiter (damit der Backtester-Vergleich nicht abreisst); er kehrt nur über einen neuen registrierten Lauf mit veränderter Hypothese zurück. Kein „mit heutigen Parametern im Buch weiter", kein „berichten und nichts tun".

Falls der Satz (b) im Registertext fehlt und nur in der Checkliste steht: **Berichtigung** — Übernahme aus dem Dokument, auf das AF.7 verweist; kein neuer Inhalt. Und Festlegung 11 deckt den Fall, dass es mehrere oder alle trifft: zulässig, vorher aufgeschrieben.

Zur Härte nach 24.2: Die Bedingung bindet härter, weil die Bot-Seite bisher zu flach gemessen war — nicht weil eine Grenze gewandert wäre. Die Benchmark-Seite war immer tagesbewertet, der Faktor 1,25 wurde nie an einer Bot-Zahl geeicht. Das ist kein Grund, (b) zu lockern; es ist der Zustand, für den (b) gebaut wurde. Eine Nebenbedingung, die nach ihrer Reparatur härter bindet, hat vorher nicht funktioniert.

## (2) Nein — und die Zahl gehört nicht einmal auf den Tisch

Eure Lesart trifft. Die Zahl „wie viele Parametersätze je Bot bleiben zulässig" ist ein Ergebnis des Laufs — sie entsteht, indem man das Raster unter der Nebenbedingung auswertet, und das ist die erste Hälfte des Selektionslaufs selbst. Wer sie vorher kennt, kennt den Ausgang, bevor der Tag gesetzt ist; und da (1) bereits entschieden ist, gibt es keine Regel mehr, die sie informieren könnte — sie könnte nur dazu verleiten, (b) wieder aufzumachen. Das ist der Unterschied zu 24.3: Dort bezifferte die Zahl eine Wirkung auf ein Objekt, hier bezifferte sie den Ausgang. Nicht messen. Die Zahl steht nach dem Lauf im Bericht, je Bot: Sätze gesamt, Sätze nach Nebenbedingung, Sätze nach Plateau-Regel.

Was vor dem Lauf gemessen werden darf, ist ausschliesslich die Benchmark-Seite (Benchmark-Drawdowns je Falte, DD_Toleranz) — und die liegt vor.

## (3) Zur Kenntnis

24.6 war eine Grössenordnungsmessung auf den TB-24-Trade-Listen, nicht der Lauf; dass Krypto 2018–2020 darin fehlt, ändert am Lauf nichts — der Snapshot enthält die Jahre, die Nebenbedingung wird dort gerechnet. Die Lücke gehört in 24.6, wo sie steht, und bedeutet nur: Für Krypto 2020 kennen wir die Grössenordnung des M-gegen-E-Unterschieds nicht vorab. Das ist nach (2) kein Nachteil.

---

**Kurz:** (1) Abbruchkriterium (b) → Schatten, Benchmark-Position, Rückkehr nur über neuen Lauf; steht seit 14.09., ggf. als Berichtigung in den Registertext übernehmen. (2) Nicht messen — die Zahl ist der Ausgang. (3) Zur Kenntnis, ohne Folge für den Lauf.
