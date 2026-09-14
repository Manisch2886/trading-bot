# Vorregistrierung S-E1 — der Nulltest (TB-30a)

**Stand: 14.09.2026. Eigener Registereintrag, eingefroren vor jedem Lauf.**

> **Auch hier wurde nichts gerechnet.** Dieses Dokument legt fest, was
> gerechnet werden wird — nicht, was herausgekommen ist.

---

## 1. Was S-E1 ist

**Turn-of-Month.** Die Hypothese stammt aus der Literatur
(McConnell & Xu): Aktienrenditen konzentrieren sich auf ein Fenster um den
Monatswechsel. Das Fenster ist dort definiert als der **letzte Handelstag
eines Monats plus die ersten drei Handelstage des folgenden** — vier
Handelstage, long, gleichgewichtet.

**S-E1 ist kein Bot-Kandidat, sondern ein Nulltest des Verfahrens.**

---

## 2. Warum S-E1 von „Kandidaten nach Rang 3" ausgenommen ist

Drei Gründe, alle drei vor dem Lauf:

1. **Keine Selektion.** Das Fenster stammt aus der Literatur, nicht aus
   diesen Daten. Es gibt keinen Parameter, der gewählt wird — und damit
   nichts, worauf eine Rasterselektion anzuwenden wäre.
2. **Die Beta-Bereinigung ist eingebaut.** Test 2 (unten) vergleicht das
   Fenster gegen **alle anderen Vier-Tage-Fenster desselben Instruments**.
   Was übrig bleibt, ist bereits der Überschuss über „irgendwann investiert
   sein".
3. **Er berührt nichts.** Weder die neun Bots noch das Mass in Reparatur.
   Kein Bot-Code, keine `live_params.py`, keine Datenbank.

---

## 3. Was S-E1 prüft

**Den Weg, nicht die Strategie:**

> Register → Forward-Test ohne Live-Status → Bestätigungsperiode → Bericht,
> **ohne dass unterwegs jemand eine Wahl hat.**

Wenn dieser Weg an einer Strategie ohne Parameter, ohne Selektion und mit
eingebauter Beta-Bereinigung schon eine Entscheidung offen lässt, dann liegt
es am Weg — und dann wäre es besser, das an S-E1 zu merken als an der
Neuselektion der neun Bots.

---

## 4. Die Festlegungen

### 4.1 Instrument und Universum

Dasselbe Aktien-Universum wie die vier Aktien-Bots:
`config/sp500_top150.txt`, gleichgewichtet, **point-in-time** (ein Titel geht
in einen Monat nur ein, wenn seine Kursdaten mindestens vier Jahre vor
Monatsbeginn einsetzen — dieselbe Regel wie im Hauptregister).

### 4.2 Das Kernfenster

**Letzter Handelstag des Monats + erste drei Handelstage des Folgemonats**,
long, gleichgewichtet, an allen übrigen Tagen flach.

Handelstage sind die Tage, an denen das Universum Kurse trägt — abgeleitet
aus `data/*.csv`, nicht aus einem zweiten Kalender. Ein zweiter Kalender wäre
eine zweite Quelle für dieselbe Zahl.

### 4.3 Kosten

**0,30 % je Round-Trip**, dieselbe Konvention wie überall
(`TRADING_FEE_PCT = 0,1` + `SLIPPAGE_PCT = 0,05` je Order, Ein- und
Ausstieg). Bei zwölf Runden im Jahr sind das **3,6 Prozentpunkte jährlich**
— eine Schranke, die der Effekt erst einmal überspringen muss. Das gehört
vor den Lauf, nicht in die Deutung danach.

### 4.4 Falten

Derselbe Plan wie für die Aktien-Bots: Kalenderjahre **2019 bis 2025** als
Selektionsfalten, **2026 bis zum Go-Live-Schnitt `2026-09-01`** als
Bestätigungsperiode. Purge und Embargo: **vier Handelstage** — die maximale
Haltedauer dieser Strategie, und damit dieselbe Regel wie bei den Bots.

Selektionsfalten heissen sie hier der Einheitlichkeit halber; **selektiert
wird nichts** — es gibt nichts zu wählen.

### 4.5 Die zwei Tests

| | |
|---|---|
| **Test 1** | Netto-Rendite und Netto-Sharpe des Kernfensters je Falte, gegen null |
| **Test 2** | Das Kernfenster gegen **alle anderen Vier-Tage-Fenster desselben Instruments** — jedes mögliche Startdatum, jeweils vier Handelstage gehalten, gleiche Kosten. Berichtet wird das Perzentil, auf dem das Kernfenster in dieser Verteilung liegt |

Test 2 **ist** die Beta-Bereinigung: er vergleicht nicht gegen „nicht
investiert", sondern gegen „genauso oft investiert, nur zu anderen Tagen".

### 4.6 Die Schwelle

S-E1 besteht, wenn **beides** gilt:

* Falten-Median der Netto-Rendite des Kernfensters **> 0**, und
* das Kernfenster liegt in Test 2 **über dem 95. Perzentil** aller
  Vier-Tage-Fenster.

Beides vor dem Lauf. Fällt eines davon durch, ist S-E1 durchgefallen — und
das ist ein zulässiges Ergebnis, genau wie Festlegung 12 im Hauptregister.

---

## 5. Die zwei Bedingungen, die ins Register gehören

### 5.1 Die Sweep-Zellen sind Robustheit, nicht Auswahl

Neben dem Kernfenster wird ein **Sweep** gerechnet: Fenster von zwei bis
sechs Handelstagen, jeweils um den Monatswechsel verschoben. Er zeigt, ob der
Effekt eine Flanke hat oder auf genau vier Tagen steht.

> ⚠️ **Fällt das Kernfenster durch und besteht eine Sweep-Variante, wird sie
> NICHT übernommen.** *Sonst sind es acht Versuche und nicht einer.*

Der Sweep ist ein **Bild**, keine Kandidatenliste. Er hat keine Schwelle, und
es gibt keinen Weg, über den eine Sweep-Zelle zum Ergebnis wird.

### 5.2 S-E1 geht in die Staging-Ebene, nicht ins Buch

Nach dem Backtest geht S-E1 in die **Staging-Ebene**: Forward-Test ohne
Live-Status, keine `live_params.py`, kein Cronjob, **kein Portfoliogewicht**
— bevor Rang 3 über die neun entschieden hat.

Ein Nulltest, der sich währenddessen ein Gewicht nimmt, ist kein Nulltest
mehr.

---

## 6. N-Buchführung

| Register | Eintrag | Begründung |
|---|---|---|
| **Versuchsregister** (`research/versuchsregister/REGISTER.md`) | **ein Eintrag** | *Ein Versuch ohne Wahl ist trotzdem ein Versuch.* Wer später fragt, wie oft in diesem Projekt etwas probiert wurde, muss S-E1 finden. |
| **DSR** | **kein** Beitrag | Multiplizität entsteht, wo unter Alternativen gewählt wird. Hier ist **N = 1**: ein Fenster, aus der Literatur, ohne Alternative. |

Die Sweep-Zellen zählen in **keines** von beiden hinein, solange 5.1 gilt —
sie sind nicht auswählbar und damit keine Versuche im Sinn der
Multiplizität. Wird 5.1 je aufgehoben, ist das ein **neuer vorregistrierter
Lauf**, und dann zählen sie alle.

---

## 7. Die Reihenfolge

1. Dieses Register einfrieren (Teil des TB-30a-Tags).
2. Backtest über die Selektionsfalten, Test 1 und Test 2, Sweep als Bild.
3. **Danach** die Bestätigungsperiode, einmal.
4. Bericht — alle Zahlen, auch die unangenehmen.
5. Staging-Ebene. Kein Portfoliogewicht.

Zwischen 2 und 5 gibt es keine Stelle, an der jemand etwas entscheidet. Das
ist der ganze Zweck.

---

*Erstellt in TB-30a. Kein Lauf, kein Ergebnis, kein Bot-Code.*
