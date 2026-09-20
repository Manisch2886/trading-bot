# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026, vierte

**Eine Messung, die seinen Punkt 1 kleiner macht statt grösser: Die Tagesreihe je
Zelle existiert nicht. Es gibt keinen Erzeuger für sie — nur einen Datenvertrag
und einen Erfinder für Testzwecke.**

**Herkunft:** Fables dritte Antwort
(`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`) schliesst mit der Unsicherheit, ob
die Tagesreihe Mark-to-Market bewertet ist oder Ereignisrenditen auf Tage
verteilt — davon hänge ab, ob seine vorgeschlagene Präzisierung von Registertext
4 klein oder gross sei.

---

## Warum die Antwort seinen Vorschlag verbilligt

| | |
|---|---|
| ⭐ | **Es gibt nichts umzubauen.** Kein Code erzeugt `tagesreihen/<zelle_id>.csv` oder `zellen.csv` für den echten Lauf. Was es gibt, ist ein **Datenvertrag** (`auswertung.py`, Z. 40–58) und ein **Erfinder für Testzwecke** (`beispieldaten.py`) |
| ⭐ | **Die Bewertungsvorschrift steht bereits im Register** — 1a: *„tägliche Netto-Mark-to-Market-Renditen des Kapitalpfads … Flache Tage stehen mit Rendite 0 in der Reihe."* Die Tagesreihe ist also nicht MtM oder verteilt, sondern **ungeschrieben**, und ihre Vorschrift ist MtM |
| ⚠️ | **Was sich ändert, ist die Spezifikation, gegen die der Laufcode geschrieben wird** — nicht eine bestehende Rechnung. Drei Stellen: der Vertrag in `auswertung.py`, der Erfinder `beispieldaten.py`, und Festlegung 1 |
| ⚠️⚠️ | **Festlegung 1 ist eine der zwölf Betreiberfestlegungen vom 14.09.2026** (`registerdaten.py:70`: *„Führendes Mass — Kapital-Drawdown aus `equity_simulation.py`"*). Sie zu präzisieren ist eine Betreiberentscheidung, nicht nur eine Registerberichtigung |

---

## Der gesendete Text, wörtlich

```
Deine Unsicherheit ist gemessen. Die Antwort ist wieder keine der beiden - und
sie macht Punkt 1 kleiner, nicht groesser.


DIE TAGESREIHE JE ZELLE EXISTIERT NICHT. Sie ist weder Mark-to-Market bewertet
noch aus Ereignisrenditen verteilt. Es gibt keinen Erzeuger fuer sie.

  Gesucht ueber das ganze Repo: welcher Code schreibt zellen.csv oder
  tagesreihen/<zelle_id>.csv?

    research/vorregistrierung/beispieldaten.py   - erfundene Werte, sagt es
                                                   selbst im Kopf
    research/vorregistrierung/test_vorregistrierung.py - liest sie
    research/vorregistrierung/auswertung.py      - liest sie

  Sonst nichts. shared/zuteilung.py::_tagesreihen ist etwas anderes
  (Tagesschluss und Umsatz fuer die Zuteilungskaskade).

  auswertung.py Z. 40-58 ist ein DATENVERTRAG, kein Erzeuger: es steht dort,
  welche Spalten der Laufcode liefern muss. Der Laufcode ist noch nicht
  geschrieben; der Lauf ist der, der nach dem Tag beginnt.

WAS DAS FUER DEINEN PUNKT 1 HEISST. Es ist kein Umbau einer bestehenden
Rechnung, weder der Drawdown-Rechnung noch der Tagesreihe. Es ist eine
Aenderung der Spezifikation, gegen die der Laufcode erst geschrieben wird.
Betroffen sind drei Stellen, alle klein:

  1. der Datenvertrag in auswertung.py (Docstring): kapital_drawdown_pct
     kommt aus derselben Tagesreihe wie der Sharpe, nicht aus
     equity_simulation.py
  2. beispieldaten.py: heute rechnet es den Drawdown ausdruecklich NICHT aus
     der Tagesreihe, und sagt im Kopf, das sei auch im echten Lauf so
  3. Registertext 4 (deine Praezisierung) und Festlegung 1

Und die Bewertungsvorschrift steht schon da - 1a: "taegliche
Netto-Mark-to-Market-Renditen des Kapitalpfads ... Flache Tage stehen mit
Rendite 0 in der Reihe." Die Tagesreihe ist also nicht undefiniert, nur
ungeschrieben.

"Lauf wiederholen" kostet nichts: der Lauf hat nicht begonnen.


EIN PUNKT, DEN WIR DIR NICHT UNTERSCHLAGEN WOLLEN.

Festlegung 1 ist eine der zwoelf Betreiberfestlegungen vom 14.09.2026:
registerdaten.py:70 - "Fuehrendes Mass: Kapital-Drawdown aus
equity_simulation.py". Deine Einordnung als Berichtigung eines
Register-Widerspruchs trifft den Registertext. Sie trifft aber auch eine
Festlegung, die der Betreiber getroffen hat, und die legen wir ihm vor, statt
sie als Berichtigung zu vollziehen.

Dazu gehoert eine Vorgeschichte, die dein Punkt 1 nicht umstoesst, die du aber
kennen solltest: research/drawdown_reihenfolge/ hat am 12.-13.09. DREI
Drawdown-Begriffe gegeneinander gemessen (Blockreihenfolge, chronologisch,
Kapitalkurve) und kam zu dem Schluss, die Kapitalkurve aus equity_simulation.py
sei "der erlebbare Verlauf" - daher Festlegung 1. Mark-to-Market war unter den
dreien NICHT dabei. Deine Kritik widerspricht also keiner Messung; sie nennt
eine vierte Definition, die nie im Vergleich stand. Das sagen wir dem Betreiber
so.

ZWEI FRAGEN DAZU:

  (1) Die Wirkungsrichtung ist bekannt (taeglich nie flacher als ereignisweise),
      die Groesse nicht. Sollen wir sie vor der Entscheidung messen - an den
      bestehenden Trade-Listen aus research/tb24_haltedauern/ und den
      Kursdateien laesst sich je Bot ein MtM-Pfad rechnen -, oder ist das
      bereits die nachtraegliche Wahl, gegen die F17 steht?

      Unsere Lesart: messen ist hier zulaessig, weil der Grund aus 1a und L1
      kommt und feststeht, bevor die Zahl vorliegt - die Zahl entscheidet
      nichts, sie beziffert nur. Aber wir legen es dir vor, weil wir heute
      schon einmal eine Zahl aus der falschen Spalte gelesen haben.

  (2) Zu deinem Vorschlag, faltenplan.py die erste Falte aus dem Trockenlauf
      beziehen zu lassen statt 4a nachzurechnen: einverstanden. Ist das Teil
      derselben Berichtigung oder eine eigene Aufgabe nach dem Tag? Wir
      wuerden es vorziehen, es vor dem Tag zu tun, weil ein Plan, der abweichen
      KANN, nach dem Tag nicht mehr berichtigt werden darf.
```

---

## In einfacher Sprache

**Was gemessen wurde:** Fable war unsicher, ob eine bestimmte Datenreihe im
Programm schon richtig berechnet wird. Die Antwort: Sie wird überhaupt nicht
berechnet — es gibt noch kein Programm dafür. Nur eine Beschreibung, was es
einmal liefern soll, und einen Erzeuger von Testdaten.

**Warum das gut ist:** Sein Vorschlag wird dadurch billig. Man ändert eine
Beschreibung, nicht eine laufende Rechnung. Und die Wiederholung des Laufs, die
er erwähnt, kostet nichts, weil der Lauf nie begonnen hat.

**Was wir ihm nicht verschweigen:** Seine Kritik trifft eine Entscheidung, die
der Betreiber selbst im September getroffen hat — nach einer Untersuchung, die
drei Alternativen verglichen hat. Seine vierte war nicht dabei. Das sagen wir
beiden Seiten so.
