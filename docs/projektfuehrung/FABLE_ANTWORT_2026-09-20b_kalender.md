# Fables Antwort — Berichtigung Aktien-Bots und die Frage W/C (20.09.2026, zweite)

**Eingegangen am 20.09.2026, 17:29 Ortszeit.** Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20b_wortlaut_nulltage.md`.

⭐ **Wörtlich abgelegt, nach der Regel aus Nachtrag (m):** *„Jede Rückfrage an
den Betreiber und seine Antwort kommen wörtlich in den Bericht — sonst leben sie
nur im Sitzungsverlauf, der mit der Sitzung verschwindet."*

---

## Teil 1 — VT bleibt; sein Schlusssatz geht

> Die Festlegung stand auf zwei Gründen aus dem Register (leere Nebenbedingung
> unter VH; Phantom-Alpha in Rang 3), nicht auf der Aktien-Null. Die Null trug
> nur den Satz, dass man in zwei Schritten vollziehen könne — der ist mit der
> Berichtigung hinfällig, und „einmal für alle neun" ist richtig. Dass die
> Aktien-Bots unter VT leicht strenger werden (ANET, PLTR, DASH, ABNB, APP,
> HOOD werden erst ab ihrem Eintrittstag gezählt), ist dieselbe Richtung wie bei
> Krypto, nur kleiner: Der Benchmark hält nichts, was der Bot nicht halten
> konnte. Es ändert an der Festlegung nichts und gehört als gemessene Wirkung in
> dieselbe Berichtigungsnotiz.

⭐ **Damit steht:** VT bleibt, **ein** Vollzug für alle neun, die Aktien-Wirkung
kommt in die Berichtigungsnotiz (Register 23.4).

---

## Teil 2 — weder W noch C als Satz; das Prinzip, das beide meinen

> Mein Satz „tragen Rendite 0" war der Versuch, zu sagen, dass der Benchmark an
> solchen Tagen nicht *undefiniert* ist. Er hat dabei einen Mechanismus
> vorgeschrieben (Nullen einfügen), wo das Register ein Prinzip braucht — und
> C_voll zeigt, wohin ein Mechanismus ohne Prinzip führt: eine leere Falte mit
> 365 Handelstagen. Das Prinzip ist die Zeitachse von „derselben Menge":
>
> > **3b (c), Satz zur Zeitachse.** Der Benchmark ist auf denselben Handelstagen
> > definiert wie der Kapitalpfad des Bots in dieser Falte. Ein Tag, an dem kein
> > Symbol handelbar ist, gehört zu keinem von beiden.
>
> Das ist in der Sache W — der Kapitalpfad des Bots hat keine Tage, an denen kein
> Symbol einen Kurs hat, weil sein Kalender die Vereinigung der Symboltage ist;
> also hat der Benchmark sie auch nicht. Aber es ist als Regel formuliert, nicht
> als Beschreibung eines `.dropna()`, und es schliesst C_voll dauerhaft aus: Ein
> Kalender der Falte ist nicht der Kalender des Bots.
>
> **Was der Code davon abweicht, und wohin das gehört:** `bh_tagesrenditen`
> lässt zusätzlich den ersten Kurstag weg, weil `pct_change` dort keine Rendite
> hat — der Bot-Pfad führt diesen Tag als 0. Das ist die Ein-Tages-Differenz aus
> eurer Messung (C_lit: +1 in vier Falten), sie hat auf jede registrierte Zahl
> die Wirkung null, und sie ist genau das, was ihr gezeigt habt: 1 + e·0 = 1,
> Peak und Trough bleiben. **Keine Codeänderung** — Sperrliste Punkt 6 bleibt
> unberührt, kein neuer Lauf. Stattdessen eine **Tatsachennotiz** zu 3b (c):
> „Die Umsetzung lässt den ersten Kurstag je Falte aus (keine Rendite
> berechenbar); der Kapitalpfad führt ihn mit 0. Abweichung höchstens ein Tag je
> Falte; gemessen: 0 abweichende Stufen in Drawdown und DD_Toleranz über
> 78 × 100." Damit sagt das Register, was der Code tut, ohne dass der Code sich
> ändern muss — und wenn `bh_tagesrenditen` je aus anderem Grund angefasst wird,
> ist `fillna(0)` auf dem ersten Tag eine Berichtigung des Codes an den Satz.
>
> `handelstage` bleibt Berichtszahl und berichtet die Länge des gemeinsamen
> Kalenders — die W-Spalte.

---

## Ein Befund in unserer Tabelle, der nicht die Frage ist

> `t3_supertrend 2018`: 0 Symbole, 0 Handelstage, Drawdown 0,00. Nach 3b (a)
> zählt eine Falte, wenn der Loader mindestens ein Symbol an mindestens einem
> Handelstag handelbar macht. Diese Falte erfüllt das nicht — sie ist keine
> Selektionsfalte, und sie sollte im Faltenplan nicht als solche stehen. Falls
> sie dort steht, ist das die Stelle, an der 4a (erste Falte = erstes Jahr mit
> Daten und Vorlauf am 1. Januar) und der Plan auseinanderlaufen; unter 4a
> beginnt `t3_supertrend` dann 2019. Nachsehen, nicht raten.

---

## Seine offene Unsicherheit

> **Unsicher:** ob der Kapitalpfad des Bots seinen ersten Tag wirklich als 0
> führt oder ihn ebenfalls auslässt — davon hängt ab, ob die Tatsachennotiz
> „höchstens ein Tag" oder „null Tage" Abweichung sagt. Beides ist wirkungslos;
> nur eines ist wahr.

⚠️⚠️ **Nachgesehen am 20.09.2026, 17:33 — und die Antwort ist keine der beiden.**
Siehe `FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`: Der Kapitalpfad des Bots hat
**gar keinen Tageskalender**. Er ist ereignisindiziert.
