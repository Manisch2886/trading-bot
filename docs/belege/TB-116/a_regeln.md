# TB-116 Block A — die Regeln, die das Prüfwerkzeug anwendet

**Werkzeug:** `research/leiter_pruefung/leiter_lesarten.py` · **Register:**
`docs/VORREGISTRIERUNG_neuselektion.md` (10 034 Zeilen, Stand `50afdbf`).
**Suchmuster und Treffer:** `a_fundstellen.txt`.

Jedes Zitat unten ist **zeichengleich** aus dem Register kopiert (eingesetzt von
`a_einsetzen.py`, geprüft von `a_zitate.py` mit `diff`, Ergebnis
`a_zitate.txt`). Was das Werkzeug tut und **nicht** im Zitat steht, ist unten
unter „Lesarten“ benannt (L0.x fest, L1–L5 variiert). **Keine Lesart ist hier
entschieden.**

---

## 1. Die Zitate

### Z1 — 16.4 (a), die drei Stufen · Register Z. 1934–1937

~~~~text
> **(a)** Jeder Bot steht auf einer von drei Stufen: **Schatten** (läuft, kein
> Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf),
> **Grundbudget** (im Buch), **Bestätigt** (im Buch, Rang-5-Gewichtung, sobald
> Netting existiert).
~~~~

### Z2 — 16.4 (b), die Stufe nach dem Lauf · Register Z. 1939–1943

~~~~text
> **(b)** Nach dem Selektionslauf steht jeder Bot, der **kein** Abbruchkriterium
> erfüllt, auf **Grundbudget**; jeder, der eines erfüllt, auf **Schatten** —
> sein Budgetanteil hält die statische Benchmark-Position in Höhe seines
> mittleren Exposures. **Die Zuweisung ist Ergebnis des eingefrorenen Skripts,
> keine Lesung.**
~~~~

### Z3 — 16.4 (c), Aufstieg · Register Z. 1945–1952

~~~~text
> **(c)** **Aufstieg** Grundbudget → Bestätigt, geprüft am Ende jedes
> Kalenderquartals durch dasselbe Skript, frühestens nach **30 geschlossenen
> Trades und sechs Monaten** Bestätigungsperiode: Netto-Sharpe der
> Bestätigungsperiode > 0, **und** Netto-Calmar ≥ **0,5 ×** Netto-Calmar des
> Gewinners über die Selektionsfalten, **und** Max-Drawdown der
> Bestätigungsperiode nicht tiefer als die tiefste Selektionsfalte des
> Gewinners. *(30 Trades, sechs Monate und 0,5 sind **willkürlich**; 0,5 ist
> eine fremde Faustregel, keine Messung dieses Projekts.)*
~~~~

### Z4 — 16.4 (d), Abstieg · Register Z. 1954–1957

~~~~text
> **(d)** **Abstieg** auf Schatten, quartalsweise: Max-Drawdown tiefer als
> **1,25 ×** die tiefste Selektionsfalte des Gewinners, **oder** Netto-Sharpe
> < 0 nach **60** geschlossenen Trades. **Rückkehr nur über einen neuen
> registrierten Lauf.**
~~~~

### Z5 — 16.4 (e), keine Stufe zwischen den Prüfungen, Notbremse · Register Z. 1959–1961

~~~~text
> **(e)** Zwischen den Quartalsprüfungen ändert sich keine Stufe. **Kein
> Betreiberentscheid setzt eine Stufe hinauf; der Betreiber kann einen Bot
> jederzeit auf Schatten setzen (Notbremse), aber nie hinauf.**
~~~~

### Z6 — 16.4 (g), die Zellen · Register Z. 1968–1978

~~~~text
> **(g)** **Zellen sind Quelle × Anlage.** Heute:
>
> | Zelle | Bots |
> |---|---|
> | Fortsetzung × Aktien | `volatility_breakout` |
> | Umkehr × Aktien | `rsi2_mean_reversion`, `turtle_soup_stocks`, `elliott_wave_stocks` |
> | Fortsetzung × Krypto | `t3_supertrend`, `volatility_breakout_crypto` |
> | Umkehr × Krypto | `rsi2_crypto`, `turtle_soup_crypto`, `elliott_wave` |
>
> Jeder Bot gehört zu **genau einer** Zelle; **die Zuordnung steht im Register
> und ändert sich nur mit dem Bot.**
~~~~

### Z7 — 16.4 (h), aktive Zellen teilen das Buch · Register Z. 1980–1983

~~~~text
> **(h)** Eine Zelle ist **aktiv**, wenn mindestens ein Bot darin auf
> Grundbudget oder Bestätigt steht. **Aktive Zellen teilen das Buch zu gleichen
> Teilen.** *Gleichteilung ist willkürlich; sie ist die einzige Aufteilung, die
> kein Ergebnis verwendet.*
~~~~

### Z8 — 16.4 (i), Stufenfaktor · Register Z. 1985–1987

~~~~text
> **(i)** Innerhalb einer Zelle teilen die Bots nach **Stufenfaktor: Schatten 0,
> Grundbudget 1, Bestätigt 2** *(Faktor 2 willkürlich)*. Anteil = eigener Faktor
> / Summe der Faktoren der Zelle.
~~~~

### Z9 — 16.4 (j), Aufstieg, Abstieg, inaktive Zelle · Register Z. 1989–1992

~~~~text
> **(j)** **Aufstieg:** mehr vom **Zellenbudget**; das Zellenbudget ändert sich
> nicht. **Abstieg:** Zellenbudget **bleibt**, die übrigen teilen es nach (i).
> **Wird die Zelle inaktiv, geht ihr Budget in die statische
> Benchmark-Position ihrer Anlage — nicht an andere Zellen.**
~~~~

### Z10 — 16.4 (k), neue aktive Zelle · Register Z. 1994–1996

~~~~text
> **(k)** Wird eine **neue Zelle aktiv**, steigt die Zahl aktiver Zellen und
> alle Zellenanteile sinken entsprechend. **Das ist die einzige Umverteilung
> zwischen Zellen, und sie folgt aus Zulassung, nicht aus Ergebnis.**
~~~~

### Z11 — 16.4 (l), Anlageklassen-Schlüssel · Register Z. 1998–2000

~~~~text
> **(l)** ⭐ **Anlageklassen-Schlüssel, Betreiberentscheid vom 16.09.2026:
> Aktien 80 / Krypto 20.** Er skaliert die Zellen einer Anlage gemeinsam und
> gilt, bis Netting (Rang 5) existiert.
~~~~

### Z12 — 16.4 (m), die Formel · Register Z. 2002–2008

~~~~text
> **(m)** **Umsetzung ohne gemeinsames Konto:** Das Leiter-Skript berechnet
> quartalsweise je Bot einen Multiplikator auf dessen heutige statische
> Positionsgrösse:
>
> `m_b = (Zellenanteil × Klassenschlüssel × Bot-Anteil in der Zelle) / (1/9)`
>
> **Die Bots lesen `m_b`; sonst ändert sich nichts.**
~~~~

### Z13 — 16.4, das Prinzip, das (j) und (k) trägt · Register Z. 2012–2016

~~~~text
> **Die Leiter bewegt Bots. Sie bewegt keine Zellen.** Out-of-Sample-Evidenz
> über einen Bot ist Evidenz über eine **Implementierung**, nicht darüber, dass
> die Ertragsquelle seiner Zelle mehr Kapital verdient. Schrumpfte die Zelle
> beim Abstieg, würde ein Bot für das Versagen eines anderen bestraft — **und
> das Kapital ginge dorthin, wo es zufällig besser lief.**
~~~~

### Z14 — 16.4, Prüfung vor dem Tag · Register Z. 2038–2042

~~~~text
Das Leiter-Skript muss aus **jeder** möglichen Stufentabelle — **3⁹ = 19 683**,
trivial aufzählbar — einen **eindeutigen** Multiplikatorvektor erzeugen,
**ohne Eingabe des Betreibers**. *Ein Fall, in dem es fragt, ist ein Fall, in
dem das Register unvollständig ist.* Auch das ist eine Prüfung mit Befund, kein
Abbruchkriterium.
~~~~

### Z15 — 7.1, zweite Regel für mehrere Ausfälle · Register Z. 781–782

~~~~text
- Das **Kapital** geht in eine **statische Benchmark-Position** in Höhe des
  mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.
~~~~

### Z16 — 15.6 (c), unterbestimmter Bot · Register Z. 1549–1555

~~~~text
> **(c)** *[ersetzt „behält seine heutigen Parameter"]* Ein Bot mit weniger als
> 3 Selektionsfalten wird nicht selektiert. Er wird als „unterbestimmt" mit
> Faltenzahl berichtet, läuft mit den heutigen Parametern **als Schatten
> ausserhalb des Buchs** weiter, und sein Budget hält eine **statische
> Benchmark-Position in Höhe seines gemessenen mittleren Exposures**. Die
> Selektion wird für ihn als eigener registrierter Lauf nachgeholt, sobald 3
> Falten vorliegen.
~~~~

### Z17 — 16.5, Backtester nicht bestätigt · Register Z. 2054–2057

~~~~text
> Abweichung. Ein Bot, dessen Signalübereinstimmung unter **95 %** liegt
> *(willkürlich)*, wird im Selektionslauf ausgewertet, aber mit dem Vermerk
> **„Backtester nicht bestätigt"**, und kann bis zur Klärung **nicht über
> Schatten hinaus**.
~~~~

### Z18 — 22.4, Notbremse auf einen In-Sample-Befund · Register Z. 3524–3528

~~~~text
> Die **Notbremse aus 6e bleibt jederzeit zulässig.** Wird sie auf einen Befund
> **aus dem Selektionslauf selbst** gezogen, ist das eine **nachträgliche
> Wahl**: Sie wird als solche im Protokoll vermerkt, und **kein anderer Bot und
> kein anderer Parametersatz steigt dadurch auf.** Ein Aufstieg entsteht allein
> aus **6c** auf Bestätigungsdaten oder aus einem **neuen registrierten Lauf**.
~~~~

### Z19 — 16.11, Zeile 3 · Register Z. 2312–2312

~~~~text
| 3 | **6 (a)–(m)** — Budgetstufen, Zellen, `m_b` | **Kein Leiter-Skript.** Kein Bot liest einen Multiplikator; alle neun rechnen mit fester Positionsgrösse (faktisch 1/9). Die 3⁹-Prüfung kann noch nicht laufen. | eigene Aufgabe (`m_b` in die `forward_test.py`) |
~~~~

### Z20 — 45.8 R8 (e), das Zellenbudget steht in 16.4 · Register Z. 9986–9986

~~~~text
> (e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genannt.
~~~~

**Ergebnis der Suche nach späteren Stellen (`a_fundstellen.txt`):** Keine
Stelle nach 16.4 **ändert** Registertext 6 (g)–(m). Späterer Text zu 6
**ergänzt** (22.4: Notbremse auf In-Sample-Befund, Z18; 17.7: „unbestimmt“ →
eingestuft, Aufstieg auf Bestätigt erst ab n ≥ 20, Z. 2679–2682),
**verweist** (26.7 Kette (b) → Schatten, Z. 4804–4817; 45.8 R8 (e), Z20) oder
**benennt die Lücke im Code** (16.11 Zeilen 3 und 9, Z19). 17.7 und 16.5
wirken nur auf die **Stufe** (welcher Bot wo steht), nicht auf die Rechnung von
der Stufe zum Multiplikator — für das Werkzeug ist die Stufe Eingabe. 16.10
(e) setzt einen Short-Sleeve auf Schatten und sagt ausdrücklich: *„Registertext
6 braucht dafür keine eigene Stufe“* (Z. 2296).

---

## 2. Wie das Werkzeug die Zitate anwendet

| Regel im Werkzeug | Quelle | Stelle im Code |
|---|---|---|
| drei Stufen `schatten`/`grund`/`bestaetigt` | Z1 | `STUFEN` |
| vier Zellen, Bots je Zelle, Reihenfolge wie in der Tabelle | Z6 | `ZELLEN` (Probe P12 vergleicht mit dem Register) |
| aktiv = mindestens ein Bot auf Grundbudget oder Bestätigt | Z7 | `_aktiv` |
| Stufenfaktor 0 / 1 / 2, Anteil = Faktor / Summe der Zelle | Z8 | `FAKTOR`, `_mit_bezug` |
| inaktive Zelle → Benchmark ihrer Anlage, nicht an andere Zellen | Z9 | `_mit_bezug` (`# (j)`) |
| Schlüssel Aktien 80 / Krypto 20 | Z11 | `SCHLUESSEL` |
| `m_b = (Zellenanteil × Klassenschlüssel × Bot-Anteil) / (1/9)` | Z12 | `NENNER`, `_mit_bezug` |
| alle 3⁹ Tabellen, eindeutiger Vektor, ohne Eingabe | Z14 | `alle_tabellen`, `rechne` („keine Antwort“ statt Rückfrage) |
| Schatten: Budgetanteil hält Benchmark | Z2, Z15, Z16 | Lesart L4 (nur für Schatten in aktiver Zelle variiert) |
| Bestätigt erst nach einer Quartalsprüfung | Z3, Z5 | Lesart L4d |

---

## 3. Die Lesarten

### Fest (nicht variiert)

| Name | Was das Werkzeug tut | Warum es nicht im Zitat steht |
|---|---|---|
| **L0.1** | Benchmark-Position wird als **Budgetanteil** des Buchs geführt; „in Höhe seines mittleren Exposures“ (Z2, Z15, Z16) wird **nicht** gerechnet | Die Höhe ist eine Ergebnisgrösse des Selektionsraums (27.1); ihre Messung wäre ein Abbruchkriterium des Auftrags |
| **L0.2** | Exakte Brüche; „eindeutig“ heisst gleich als Bruch | Z14 sagt nicht, was „eindeutig“ bei Rundung heisst |
| **L0.3** | Heutige statische Positionsgrösse = 1/9 des Buchs | Z12 nennt den Nenner 1/9, nicht dass die Grösse ein Neuntel des **Buchs** ist; `shared/groessenfaktor.py` liest es so („m_b = 1,0 heisst ‚wie bisher‘“) |
| **L0.4** | Anlage einer Zelle aus dem Zellennamen in Z6 | Z6 nennt „Quelle × Anlage“ im Namen, keine eigene Spalte |
| **L0.5** | aktiv nach Z7, unabhängig von L5 | — (steht so in Z7; als Name geführt, weil L5 den Faktor ändert, nicht die Aktivität) |
| **L0.6** | Schatten hat `m_b = 0` | Z1 „kein Portfoliogewicht“; Z8 ergibt in einer inaktiven Zelle 0/0 |
| **L0.7** | Eingabe ist **nur** die Stufentabelle | Z14 verlangt es so; Vorgeschichte und Herkunft der Stufe sind deshalb nicht verfügbar (siehe L2c, L4d) |
| **L0.8** | Buchsumme = Σ `m_b` × (1/9) + Benchmark-Anteile; Rest = 1 − Buchsumme, keinem Ort zugeordnet | Formel des Auftrags; der Text sagt nicht, wohin ein Rest geht (Z15: „nicht in Kasse“) |
| **L0.9** | Schatten in einer Zelle **ausserhalb** der Bezugsmenge (L2) bekommt keinen Anteil | Z2/Z16 nennen für ihn einen „Budgetanteil“, Z7 gibt seiner Zelle keinen |

### Variiert (144 Kombinationen)

**L1 — Zellenanteil und Klassenschlüssel** (Z7, Z11, Z12). Z7 sagt „teilen das
**Buch**“, Z11 „skaliert die Zellen einer Anlage gemeinsam“, Z12 multipliziert
beides.

| | |
|---|---|
| **L1a** | Zellenanteil = 1/\|R\| über alle Zellen, Schlüssel danach multipliziert (Z12 wörtlich mit Z7 „das Buch“) |
| **L1b** | Buch zuerst 80/20, Zellenanteil = 1/\|R_Anlage\| innerhalb der Anlage; eine Anlage ohne Zelle in R gibt ihren Schlüssel in ihre Benchmark |
| **L1c** *(Sitzung ergänzt)* | gleiche Teile über alle Zellen, mit dem Schlüssel gewichtet und auf das Buch normiert: w = K / Σ K über R |

**L2 — Bezugsmenge R der Zellen** (Z7, Z9, Z10). Z7/Z10 zählen **aktive**
Zellen; Z9 verbietet, dass das Budget einer inaktiv gewordenen Zelle an andere
Zellen geht — mit Z7 wörtlich stiege aber der Anteil der übrigen, sobald eine
Zelle inaktiv wird.

| | |
|---|---|
| **L2a** | R = die jetzt aktiven Zellen (Z7/Z10 wörtlich) |
| **L2b** *(Sitzung ergänzt)* | R = alle vier Zellen aus Z6; eine inaktive Zelle in R gibt ihr Budget in die Benchmark ihrer Anlage (Z9) |
| **L2c** *(Sitzung ergänzt)* | R = die seit der letzten Zulassung aktiven Zellen (Z9 + Z10: nur Zulassung ändert die Zahl). R steht nicht in der Tabelle: Antwort nur, wenn **jede** mögliche Vorgeschichte (aktiv ⊆ R ⊆ alle) denselben Vektor ergibt |

**L3 — Anlage ohne aktive Zelle** (Z9, Z11).

| | |
|---|---|
| **L3a** | ihr Anteil geht in die Benchmark ihrer Anlage (Z9, zellenweise gelesen) |
| **L3b** | ihr Schlüssel geht an die andere Anlage (Schlüssel 1/0), sofern diese eine aktive Zelle hat |

**L4 — Schatten-Bot in einer aktiven Zelle** (Z2 gegen Z8/Z9).

| | |
|---|---|
| **L4a** | Z8/Z9 gelten immer: Faktor 0, die übrigen teilen das Zellenbudget, keine Benchmark aus diesem Bot |
| **L4b** | Z2 gilt immer: der Schatten zählt beim Teilen wie Grundbudget, sein Anteil hält die Benchmark seiner Anlage |
| **L4c** *(Sitzung ergänzt)* | Z2 gilt immer, „sein Budgetanteil“ = heutige Grösse 1/9 (L0.3), zusätzlich zum Zellenbudget, das die übrigen nach Z8 teilen |
| **L4d** | Z2 gilt nur direkt nach dem Lauf (vor der ersten Quartalsprüfung), danach Z8/Z9. Ein Bestätigt entsteht nur an einer Quartalsprüfung (Z3, Z5) → steht eines in der Tabelle, wie L4a; sonst Antwort nur, wenn L4a und L4b dasselbe ergeben |

**L5 — Faktor „Bestätigt“ vor Netting** *(Sitzung ergänzt)* (Z1 gegen Z8).

| | |
|---|---|
| **L5a** | Faktor 2 (Z8, ohne Bedingung) |
| **L5b** | Faktor 1, bis Netting existiert (Z1: „Rang-5-Gewichtung, sobald Netting existiert“; Z11: „gilt, bis Netting (Rang 5) existiert“) |
