# BERICHT — TB-33, Nulltest S-E1 Turn-of-Month

**Stand: 15.09.2026.** Diese Untersuchung fasst **keinen** Bot-Code an.

---

## 1. Frage

Nicht „funktioniert Turn-of-Month?", sondern:

> **Läuft der Weg — Register → Backtest → Forward-Test ohne Live-Status →
> Bestätigungsperiode → Bericht — durch, ohne dass unterwegs jemand eine
> Wahl hat?**

Die Strategie ist das Werkzeug, nicht der Gegenstand. Gewählt wurde sie,
weil sie der **einfachste mögliche Fall** ist: ein Instrument, zwölf Termine
im Jahr, **null Parameter**. Läuft der Weg hier nicht sauber, läuft er bei
`S-B1` auch nicht.

---

## 2. Antwort

**Der Weg läuft — und hat dabei eine Lücke im Verfahren gezeigt.**

Der Selbsttest bildet das Urteil maschinell aus den neun Pfadkriterien:
`110/110`, `WEG SAUBER`. An vier Stellen musste etwas festgelegt werden, das
im TB-30a-Register nicht stand; alle vier **vor** dem Lauf, drei davon aus
der Aufgabenstellung selbst.

Die vierte — **A4, die Faltenzuordnung um den Jahreswechsel** — ist der
Befund:

> Ein Turn-of-Month-Ereignis im Dezember endet im Januar. Zu welcher Falte
> gehört es? TB-30a regelt Faltenlängen, Purge und Embargo — aber nicht das.
> Die Lücke fiel auf, als das Auswertungsskript die Zeile `"jahr": ...`
> brauchte.
>
> Sie ist klein und harmlos. Sie ist auch genau die Art Lücke, die bei
> `S-B1` — neun Bots, 2 416 Zellen — **nicht aufgefallen wäre**, sondern im
> Vorbeigehen im Code entschieden worden wäre. Der Nulltest hat sie an der
> billigsten möglichen Stelle gefunden. Das war sein Zweck.

Festgelegt wurde die konservative Richtung: Zuordnung über den
**Einstiegstag**, Dezember→Januar fällt ins alte Jahr. Sie schiebt keine
Beobachtung in die Bestätigungsperiode hinein, die dort nicht anfängt.

---

## 3. Was **nicht** herauskam

**Kein Ergebnis über den Turn-of-Month-Effekt.** Kein einziger Kurs von SPY
ist in diese Arbeit eingegangen: yfinance ist aus der Arbeitsumgebung nicht
erreichbar (Proxy 403). Die Auswertung lief gegen **erzeugte Beispieldaten**
— dieselbe Zusicherung wie in TB-30a: *das Auswertungsskript hat seinen Test
bestanden, als es noch nichts zu deuten gab.*

Der Datenlauf ist Schritt 6 des Testdokuments, auf dem Rechner des
Betreibers.

---

## 4. Wie geprüft wurde

Sechs gebaute Lagen, in jeder werden **Kurse** gesetzt und nie Ergebnisse.
Welche Bedingung fällt, rechnet die Auswertung selbst aus:

| Lage | B1 | B2 | B3 | Urteil |
|---|:--:|:--:|:--:|---|
| Effekt deutlich | ✓ | ✓ | ✓ | `BESTANDEN` |
| Kein Effekt | ✗ | ✗ | ✓ | `DURCHGEFALLEN` |
| nur Falten-Median fällt | ✗ | ✓ | ✓ | `DURCHGEFALLEN` |
| nur Bootstrap fällt | ✓ | ✗ | ✓ | `DURCHGEFALLEN` |
| nur Perzentil fällt (**reines Beta**) | ✓ | ✓ | ✗ | `DURCHGEFALLEN` |
| Kern fällt, Sweep bestünde | ✗ | ✗ | ✗ | `DURCHGEFALLEN` |

Die fünfte Zeile zeigt Test 2 bei der Arbeit: ein Markt mit kräftiger Drift,
in dem das Fenster **netto positiv** ist — und trotzdem schlechter als
praktisch jedes andere Vier-Tage-Fenster desselben Instruments. Ohne die
Beta-Bereinigung wäre das ein „Effekt" gewesen.

Dass **jede** Bedingung ihren eigenen Fall hat, ist nicht behauptet, sondern
durch Mutation gezeigt: jede wird einzeln entfernt, auf dem Datensatz, in dem
nur sie fällt — und das Urteil kippt. Zusätzlich die Gegenprobe: dieselbe
Entfernung darf in einer **anderen** Lage **nichts** ändern.

---

## 5. Zwei Fallen, die in dieser Sitzung wirklich zugeschlagen haben

**„Eine zweite Wache verdeckt das Fehlen der ersten."** Probe H7 mutierte
zunächst die falsche von **drei** Streich-Wachen in
`handelstage.ereignisse` — und blieb grün, obwohl die Wache weg war. Jetzt
wird die mutiert, die in der Lage wirklich trägt; **H7c** weist nach, dass
die dritte hier nichts beiträgt.

**„Eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich
selbst."** Deshalb setzt der Generator nur Kurse. Und deshalb sucht die
Feiertagsprobe ausdrücklich Jahre, in denen der 31.12. auf einen
**Wochentag** fällt: an einem Samstag läge „−1" ohnehin früher, und die Probe
hätte sich selbst bestätigt, ohne die Regel zu berühren.

---

## 6. Übernahme

**Keine.** Diese Untersuchung übernimmt nichts und schlägt nichts vor.

`S-E1` geht nach dem Backtest in die **Staging-Ebene**, nicht ins Buch: kein
Portfoliogewicht, bevor Rang 3 über die neun Bots entschieden hat. Frist und
Entscheidungskriterium standen beim Anlegen fest und stehen als Code in
`register.py`.

Ein Vorschlag, ausdrücklich als solcher: **A4 gehört ins Hauptregister.**
Die Faltenzuordnung um den Jahreswechsel betrifft jede Strategie, deren
Haltedauer über einen Monatswechsel reicht — also auch die vier Aktien-Bots
in `S-B1`. Geändert wurde dort **nichts**.
