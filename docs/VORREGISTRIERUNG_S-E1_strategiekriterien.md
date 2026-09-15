# Vorregistrierung S-E1 — Strategiekriterien des Laufs (TB-33)

**Stand: 15.09.2026. Eingefroren vor dem Lauf.**

> **Auch hier wurde nichts gerechnet.** Dieses Dokument legt fest, was
> gerechnet werden wird — nicht, was herausgekommen ist.

Dieses Dokument **baut auf** [`VORREGISTRIERUNG_S-E1_nulltest.md`](VORREGISTRIERUNG_S-E1_nulltest.md)
(TB-30a, PR #103) auf und **ersetzt es nicht**. Wo dort schon etwas steht,
gilt es weiter; dieses Dokument ergänzt das, was für den konkreten Lauf
fehlte, und hält **drei Abweichungen** fest, die der Auftraggeber mit der
Aufgabenstellung TB-33 gesetzt hat.

Der zweite Registereintrag — [`VORREGISTRIERUNG_S-E1_pfadkriterien.md`](VORREGISTRIERUNG_S-E1_pfadkriterien.md)
— legt fest, was als **bestandener Weg** gilt. Beide vor dem Lauf.

---

## 0. Die drei Abweichungen von TB-30a — offen, nicht still

Ein Nulltest, der unterwegs sein eigenes Register umschreibt, ist kein
Nulltest. Deshalb stehen die Abweichungen **hier, vor dem Lauf**, mit Grund
und mit der Angabe, wer sie gesetzt hat.

| # | TB-30a sagte | TB-33 setzt | wer | Grund |
|---|---|---|---|---|
| **A1** | Instrument: das gleichgewichtete `sp500_top150`-Universum, point-in-time (§4.1) | Instrument: **SPY** | Auftraggeber, in der Aufgabenstellung | Ein Instrument statt 150 macht den Fall so einfach wie möglich — und darum geht es beim Nulltest. Das Universum bleibt als Festlegung für spätere Läufe stehen, es ist nicht gestrichen |
| **A2** | Sweep: Fenster von **zwei bis sechs** Handelstagen um den Monatswechsel (§5.1) | Sweep: **−2/+3, −1/+2, −1/+4** sowie die Instrumente **QQQ, IWM, EFA** | Auftraggeber | Derselbe Zweck (hat der Effekt eine Flanke?), engere und benannte Zellen. Die Bedingung aus §5.1 — *keine Sweep-Zelle wird je zum Ergebnis* — gilt unverändert und wird in Abschnitt 4 wörtlich wiederholt |
| **A3** | Schwelle: Falten-Median > 0 **und** Perzentil > 95 (§4.6) | dieselben zwei Bedingungen **plus** eine dritte: untere Bootstrap-Grenze > 0 | dieses Dokument | TB-30a nannte kein Bootstrap-Verfahren und keine Mindest-Ereigniszahl. Beides fehlte und wird hier ergänzt — **verschärfend**, nie lockernd |
| **A4** | — (nicht geregelt) | Ein Ereignis gehört zu dem Kalenderjahr, in dem sein **Einstiegstag** (Tag −1) liegt | dieses Dokument | Nachgetragen beim Schreiben des Auswertungsskripts, **vor jeder Rechnung**. Ein Wechsel Dezember→Januar liegt in zwei Jahren; ohne diese Festlegung hätte das Skript an genau einer Stelle eine Wahl gehabt. Die gewählte Richtung ist die konservative: sie schiebt keine Beobachtung in die Bestätigungsperiode hinein, die dort nicht anfängt |

> **Das sind die Stellen, an denen dieser Lauf etwas festlegen musste, das
> nicht schon im Register stand.** Alle vier liegen **vor** dem Lauf, nicht in
> ihm: A1 bis A3 stammen aus der Aufgabenstellung und wurden vor dem ersten
> Commit eingefroren, **A4 fiel beim Schreiben des Auswertungsskripts auf und
> wurde eingetragen, bevor eine einzige Zahl gerechnet war.** Der
> Übergabebericht führt alle vier unter der Pfadfrage auf.
>
> **A4 ist der eigentliche Befund dieses Nulltests.** Er ist klein und er ist
> harmlos — aber er ist genau die Art Lücke, um derentwillen S-E1 gerechnet
> wird: eine Festlegung, die niemand vermisst, bis ein Skript sie braucht. Bei
> `S-B1` mit neun Bots und 2 416 Zellen wäre sie nicht aufgefallen, sondern
> stillschweigend im Code getroffen worden.

---

## 1. Instrument, Zeitraum, Datenquelle

| | |
|---|---|
| **Kerninstrument** | `SPY` |
| **Sweep-Instrumente** | `QQQ`, `IWM`, `EFA` — ausschliesslich Robustheit, siehe Abschnitt 4 |
| **Datenquelle** | yfinance, dieselbe Quelle wie die vier Aktien-Bots |
| **Ablage** | `research/turn_of_month/daten/<SYMBOL>_1d.csv` — **nicht** `data/`, weil TB-31 dort parallel arbeitet |
| **Kursaufbereitung** | `shared/kursdaten.entferne_unvollstaendige` vor jeder Rechnung. Streichen **und** zählen; die Zahl steht in der Ergebnisdatei |
| **Kursart** | Schlusskurse, `auto_adjust=True` (Dividenden und Splits bereinigt) |
| **Zeitraum** | Der verfügbare Zeitraum bis zum Go-Live-Schnitt. Selektionsfalten: Kalenderjahre **bis einschliesslich 2025**; Bestätigungsperiode: **2026-01-01 bis 2026-09-01**, einmal |
| **Faltenzuordnung** | Ein Ereignis gehört zu dem Kalenderjahr, in dem sein **Einstiegstag** (Tag −1) liegt — siehe A4 |

**Warum der Zeitraum günstig liegt:** McConnell/Xu (2008) enden mit ihrer
Stichprobe **2005**. Alles ab **2006** ist echte Out-of-Sample-Zeit für einen
publizierten Effekt — nichts daran wurde je an diesen Daten angepasst.

---

## 2. Die Handelstags-Regel — **vor** dem Lauf, nicht wenn sie gebraucht wird

Handelstage, nicht Kalendertage. „−1" ist der **letzte Handelstag des
Monats**, nicht der 30. oder 31.

1. **Was ein Handelstag ist.** Ein Tag, an dem die Kursdatei des Instruments
   eine **vollständige** Kerze trägt — nach `shared/kursdaten`. Kein zweiter
   Kalender: ein zweiter Kalender wäre eine zweite Quelle für dieselbe Zahl,
   und die laufen in diesem Projekt schon einmal auseinander (CLAUDE.md).
2. **Feiertage** stehen damit gar nicht erst in der Reihe. Das Fenster
   verschiebt sich von selbst; es gibt keinen Sonderfall und keine Tabelle,
   die gepflegt werden müsste.
3. **Verkürzte Handelstage** (Halbtage, etwa der Tag nach Thanksgiving) sind
   **volle Handelstage** und zählen als einer. Begründung: die Strategie
   handelt zum Schluss, und ein verkürzter Tag hat einen Schluss.
4. **„−1"** ist der letzte Handelstag des Kalendermonats, **„+k"** der k-te
   Handelstag des Folgemonats.
5. **Die Einstiegsrendite** des Tages −1 misst gegen den Schluss des
   **davorliegenden** Handelstags. Ein Ereignis braucht diesen Tag also
   ebenfalls.
6. **Unvollständige Ereignisse werden gestrichen UND gezählt.** Fehlt ein
   Tag des Fensters (Reihenanfang, Reihenende, oder ein Folgemonat mit
   weniger als k Handelstagen), entfällt das Ereignis und die Zahl der
   entfallenen Ereignisse steht in der Ergebnisdatei. Ein stillschweigend
   gestrichener Datenpunkt ist dasselbe Problem in Grün.

---

## 3. Die drei Tests und die Schwellen

### 3.1 Kosten — zuerst, weil sie die Schranke setzen

**0,30 Prozentpunkte je Round-Trip**, dieselbe Konvention wie überall
(`TRADING_FEE_PCT = 0,1` + `SLIPPAGE_PCT = 0,05` je Order, Ein- und
Ausstieg). **Genau ein** Round-Trip je Ereignis.

    netto = (1 + brutto) * (1 - 0,0030) - 1

Zwölf Runden im Jahr sind **3,6 Prozentpunkte jährlich** — die Schranke, die
der Effekt überspringen muss. **Netto gerechnet, nicht brutto**, überall und
auch im Sweep.

### 3.2 Test 1 — der Effekt selbst

Mittlere **Netto**-Rendite des Fensters **−1 bis +3** auf SPY je Ereignis,
über den verfügbaren Zeitraum.

| | |
|---|---|
| **Bootstrap-Verfahren** | Ziehen der **Ereignisse** mit Zurücklegen (i.i.d. auf Ereignisebene, nicht auf Tagesebene — ein Ereignis ist die Beobachtungseinheit) |
| **Ziehungen** | **10 000** |
| **Startwert (Seed)** | **20260915**, fest im Register. Ohne festen Seed gibt es keine Wiederholbarkeit, und Wiederholbarkeit ist ein Pfadkriterium |
| **Intervall** | **95 %**, Perzentilmethode (2,5 % / 97,5 %) |
| **Mindest-Ereigniszahl** | **120** Ereignisse (zehn Jahre Monatswechsel) |

**Unter 120 Ereignissen ist der Lauf `NICHT AUSWERTBAR` — nicht
`DURCHGEFALLEN`.** Das sind zwei verschiedene Aussagen, und sie werden
getrennt gehalten: „zu wenig Daten" ist kein Befund über den Effekt.

### 3.3 Test 2 — die eingebaute Kontrolle (Beta-Bereinigung)

Das Kernfenster gegen **alle anderen Vier-Handelstage-Fenster desselben
Instruments**.

Ausgeführt als **Platzhalter-Verteilung**: je Ziehung werden **genauso
viele** Vier-Handelstage-Fenster gezogen wie es Kernereignisse gibt,
gleichverteilt über alle möglichen Startpositionen, **innerhalb einer
Ziehung überschneidungsfrei**, mit **denselben Kosten**. Aus jeder Ziehung
wird der Mittelwert gebildet.

| | |
|---|---|
| **Ziehungen** | **10 000** |
| **Startwert (Seed)** | **20260915** |
| **Berichtet** | das Perzentil, auf dem der Kern-Mittelwert in dieser Verteilung liegt |

> Das **ist** die Beta-Bereinigung: verglichen wird nicht gegen „nicht
> investiert", sondern gegen **„genauso oft und genauso lange investiert,
> nur an anderen Tagen"**. Wenn das Turn-of-Month-Fenster nur deshalb positiv
> ist, weil SPY über zwanzig Jahre gestiegen ist, zeigt jedes andere
> Vier-Tage-Fenster dasselbe — und der Effekt ist nichts.

### 3.4 Die Schwelle — drei Bedingungen, jede einzeln bindend

S-E1 **besteht**, wenn **alle drei** gelten:

| | Bedingung | Herkunft |
|---|---|---|
| **B1** | Falten-Median der Netto-Rendite des Kernfensters **> 0** | TB-30a §4.6 |
| **B2** | **Untere** Grenze des 95-%-Bootstrap-Intervalls des Ereignis-Mittelwerts **> 0** | TB-33, Abweichung A3 |
| **B3** | Perzentil in Test 2 **> 95** | TB-30a §4.6 |

Fällt **eine** durch, ist S-E1 **durchgefallen**. Das ist ein zulässiges
Ergebnis, genau wie Festlegung 12 im Hauptregister.

**Die drei Bedingungen decken sich nicht gegenseitig.** Der Selbsttest prüft
jede **einzeln**, mit je einem Fall, in dem nur diese eine greift, und weist
durch Mutation nach, dass ihr Wegfall das Urteil ändert. Eine Bedingung,
deren Wegfall nichts ändert, wäre keine — und eine zweite Wache, die das
Fehlen der ersten verdeckt, ist in diesem Projekt schon mehrfach
vorgekommen.

---

## 4. Test 3 — Robustheit, **ausdrücklich als Robustheit**

Sweep über die Fenster **−2/+3, −1/+2, −1/+4** und über die Instrumente
**QQQ, IWM, EFA**. Gerechnet wird in jeder Zelle dasselbe wie im Kern,
**mit denselben Kosten**.

> ⚠️ **Die Sweep-Zellen sind Robustheit, nicht Auswahl. Ins Register, vor
> dem Lauf:**
>
> **Fällt das Kernfenster (−1/+3 auf SPY) durch und besteht eine
> Sweep-Variante, wird die Variante NICHT übernommen. Das Ergebnis lautet
> dann `DURCHGEFALLEN`.**
>
> *Sonst sind es acht Versuche und nicht einer, und die Ausnahme von
> „Kandidaten nach Rang 3" wäre keine mehr.*

Der Sweep hat **keine Schwelle** und **keinen Weg ins Urteil**. Er ist ein
Bild. Im Auswertungsskript ist das keine Absichtserklärung, sondern eine
Eigenschaft der Struktur: die Urteilsfunktion bekommt die Sweep-Ergebnisse
**gar nicht erst übergeben**. Der Selbsttest weist das durch Mutation nach —
an einem Fall, in dem der Kern durchfällt und eine Sweep-Variante besteht.

Wird diese Bedingung je aufgehoben, ist das ein **neuer vorregistrierter
Lauf**, und dann zählen alle Zellen — zum Versuchsregister **und** zur DSR.

---

## 5. Was der Lauf NICHT tut

* Er ändert **keine** `live_params.py`, keinen Bot, keine Datenbank, keine
  `results/*.csv`.
* Er legt **kein** Portfoliogewicht an (siehe Pfadkriterien, Abschnitt zur
  Staging-Ebene und TB-30a §5.2).
* Er trägt **keinen** Cronjob ein. Die Zeile steht als **Vorschlag** im
  Testdokument; der Betreiber trägt sie selbst ein.
* Er trägt **nichts** zur DSR bei: Multiplizität entsteht, wo unter
  Alternativen gewählt wird, und hier ist **N = 1**.

---

## 6. Die Reihenfolge

1. Diese beiden Register einfrieren — **eigener Commit, vor dem Lauf**.
2. Auswertungsskript schreiben und gegen **erzeugte Beispieldaten** prüfen,
   **bevor** echte Ergebnisse existieren.
3. Datenlauf (yfinance), Test 1, Test 2, Sweep als Bild.
4. **Danach** die Bestätigungsperiode, einmal.
5. Bericht — alle Zahlen, auch die unangenehmen.
6. Staging-Ebene. Kein Portfoliogewicht.

Zwischen 2 und 6 gibt es keine Stelle, an der jemand etwas entscheidet. Das
ist der ganze Zweck.

---

*Erstellt in TB-33, vor dem Lauf. Ergänzt TB-30a, ersetzt es nicht.*
