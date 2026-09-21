# Berichtigung zu den Nachträgen (q) und (r) — 19.09.2026, 21:05

**Anlass:** Der Betreiber fragte, ob Fable die fünf Nachträge querprüfen soll.
Bei der Vorbereitung dieser Frage habe ich festgestellt, dass **drei tragende
Behauptungen in (q) und (r) nicht gemessen, sondern aus Bezeichnernamen
erschlossen** sind. Eine davon ist jetzt gemessen; zwei sind es nicht.

⚠️ **Diese Berichtigung ersetzt nichts.** Sie wird zusammen mit (q) und (r)
eingearbeitet, und die berichtigten Stellen tragen den Verweis hierher — nach
demselben Muster wie TB-56b die Registerstelle 15.6 berichtigt: **an der Stelle
des Fehlers, mit der Messung daneben.**

---

## 1. ⭐ KG5 — gemessen, und die Aussage wird schärfer

**In (q) stand:** *„feinste vorhandene Auflösung: 1 Stunde (`MIN_HISTORY_HOURS =
17520` bei `elliott_wave`); alle übrigen acht Bots rechnen auf Tagesdaten"*.

⚠️ **Das war aus den Konstantennamen erschlossen, nicht aus den Daten gelesen.**

**Gemessen am 19.09.2026, 21:03, an den Dateinamen und den ersten Datenzeilen
in `data/`:**

| Auflösung | Dateien | erste Spalte `open_time` |
|---|---:|---|
| `1d` | **174** | `1980-12-12` — Datum ohne Uhrzeit |
| `1h` | **25** | `2020-10-15 03:00:00`, Folgezeile `04:00:00` |
| `4h` | **24** | — |
| **Summe** | **223** | = der registrierte Datenstand `d9449faf…` |

⭐ **Die Aussage stimmt — und sie ist strenger als geschrieben:**

> **Eine Stundenauflösung existiert für 25 von 223 Dateien, sämtlich Krypto.
> Für alle 174 Aktiendateien ist die feinste vorhandene Auflösung ein Tag.**

⚠️⚠️ **Folge, die in (q) fehlt und die wichtiger ist als der ursprüngliche
Punkt:** §7 des Konzepts (Cross-Asset-Übertragung `Macro Shock → Rates → USD →
Equities / Crypto / Commodities`) ist die Stelle, an der Aktien und Krypto
zusammenkommen. **Auf der Aktienseite gibt es dafür nur Tagesdaten.** Damit ist
Cross-Asset-Übertragung nicht auf eine Stunde, sondern **auf einen Tag**
beschränkt — und eine Übertragung, die innerhalb eines Handelstages abläuft, ist
mit diesem Bestand grundsätzlich nicht messbar, nicht nur ungenau.

⇒ **KG-F2 wird ergänzt:** Das Pflichtfeld Auflösung trägt **je Anlageklasse**
einen Wert, nicht einen für den ganzen Lauf.

---

## 2. ⚠️⚠️ RT3 — behauptet, nicht gemessen

**In (r) stand:** *„Vier der neun Bots sind Breakout- oder Trendbots … Wörtlich
angewandt fällt jeder davon durch."*

⚠️ **Das ist aus den Bot-Namen erschlossen** (`volatility_breakout`,
`volatility_breakout_crypto`, `turtle_soup_stocks`, `turtle_soup_crypto`),
**nicht aus den Renditeverteilungen gemessen.** Ob die Performance dieser vier
Bots tatsächlich an wenigen Trades hängt, steht in den Trade-Listen der neun
`paper_trading_*.db` — und dort habe ich nicht nachgesehen.

⚠️ **Warum nicht, und das ist kein Versäumnis:** Während der TB-56-Sitzung sind
die zwölf Datenbanken mit Quersummen gesichert und werden am Ende byteweise
verglichen. **Eine SQLite-Datei zu öffnen kann `-wal`- und `-shm`-Dateien
anlegen** und den Vergleich scheitern lassen. ⇒ **Kein Zugriff auf die
Datenbanken, solange eine Mac-Sitzung läuft.**

⇒ **Der Satz in (r) ist zu ersetzen durch:** *„Vier der neun Bots sind nach
ihrer Bauart Trendfolger; ob ihre Performance an wenigen Trades hängt, ist
**nicht gemessen**. Der Einwand gegen KILL TEST 7 gilt unabhängig davon, weil er
aus der Form rechtsschiefer Renditeverteilungen folgt und nicht aus diesen
Bots."*

⭐ **Der Einwand trägt also weiter** — nur seine Illustration war eine
Behauptung. **A1: ein fehlgeschlagener Nachweis und ein leeres Ergebnis sehen
gleich aus, und ich habe hier gar nicht erst gemessen.**

---

## 3. ⚠️ RT1 — dasselbe, und es betrifft den wichtigsten Punkt von (r)

**In (r) stand:** *„Fünf der acht Kill Tests sind heute rechenbar"* — mit einer
Tabelle, die **Kill Test 7** aus den Trade-Listen und **Kill Test 5** aus dem
Parametergitter (N = 653) speist.

⚠️ **Beides ist plausibel und nicht geprüft.** Ob die Datenbanken Trade-Listen
in auswertbarer Form enthalten und ob die Gitterergebnisse je Parameterpunkt
erhalten sind, ist **nicht nachgesehen** — aus demselben Grund wie unter 2.

⇒ **Die Tabelle in RT1 trägt ab sofort eine dritte Spalte: „gemessen / nicht
gemessen".** Heute: **alle fünf „nicht gemessen"**.

⭐⭐ **Und das schwächt den Hauptbefund von RT1 nicht — es verstärkt ihn.**
Der Befund war: *ein Kill Test, der nach dem Blick auf den Gewinner gewählt
wird, ist eine zweite Selektion.* Diese Regel gilt **unabhängig davon, wie viele
Tests rechenbar sind**. Sie gilt sogar, wenn keiner rechenbar ist — dann für den
Tag, an dem einer es wird.

---

## 4. ⚠️ KG1 — die Zahl 196 000 ist meine Rechnung auf meinen Annahmen

**In (q) stand:** *„Rechnung an der Struktur des Entwurfs selbst"*, und dann
`50 × 49 × 20 × 4 = 196 000`.

⚠️ **Das Konzept nennt 22 Knoten**arten** und 10 Kanten**arten**. Die Zahlen 50
konkrete Knoten, 20 Verzögerungen und 4 Regime sind **meine**, nicht seine.**
*„An der Struktur des Entwurfs selbst"* ist damit falsch formuliert — sie ist an
meinen Annahmen gerechnet.

⇒ **Zu ersetzen durch:** *„Eine Beispielrechnung mit 50 konkreten Knoten, 20
Verzögerungen und 4 Regimen — Annahmen des Verfassers, nicht des Konzepts —
ergibt 196 000 prüfbare Beziehungen und bei α = 0,05 rund 9 800 Scheintreffer.
Die Größenordnung, nicht die Zahl, ist die Aussage."*

⭐ **Der Punkt bleibt:** Die Zahl der Tests muss vorher registriert werden, und
zwar umso dringender, je freier die Knotenwahl ist.

---

## 5. Was daraus als Regel folgt

⭐⭐ **Eine Regel für mich, und sie ist die allgemeine Fassung eines Fehlers, den
ich heute vier Mal bei Nummern und drei Mal bei Sacheigenschaften gemacht habe:**

> **Ein Nachtrag unterscheidet in jedem Satz zwischen gemessen und erschlossen —
> und markiert das Erschlossene als solches.** Ein Bezeichnername ist kein
> Messwert. `MIN_HISTORY_HOURS` sagt, dass eine Konstante Stunden zählt; es sagt
> nichts über die Auflösung der Daten. `volatility_breakout` sagt, wie ein Bot
> heißt; es sagt nichts über seine Renditeverteilung.

⚠️ **Das ist dieselbe Klasse wie Fables Schicht-3-Befund:** *„Der Lese-Audit
beweist, welche DATEN gelesen wurden. Er sagt nichts darüber, welcher CODE
gelesen hat."* Ein Name beweist, wie etwas heißt. Er sagt nichts darüber, was es
tut.

⇒ **Diese Regel gehört als eigener Punkt nach Abschnitt 4** — nächste freie
Nummer, von der Sitzung gemessen.

---

## 6. Was nach TB-56 zu messen ist, bevor (r) als belegt gilt

| | zu messen | womit |
|---|---|---|
| **1** | Enthalten die neun `paper_trading_*.db` Trade-Listen mit Einzelergebnissen? | **auf einer Kopie**, nie am Original |
| **2** | Hängt die Performance der vier Trendbots an wenigen Trades — und **stärker als ihre eigene Verteilung erwarten lässt**? | Kopie + Nullmodell |
| **3** | Sind die Gitterergebnisse je Parameterpunkt erhalten (N = 653), oder nur die Sieger? | lesend |

⚠️ **Bis diese drei gemessen sind, trägt RT1 seine Tabelle mit dem Vermerk
„nicht gemessen".**

---

## In einfacher Sprache

**Beim Vorbereiten der Frage, ob Fable querprüfen soll, habe ich drei eigene
Behauptungen gefunden, die ich nicht gemessen hatte, sondern aus Namen
geschlossen.**

**Eine habe ich jetzt gemessen, und sie stimmt** — sogar strenger als
geschrieben: Von unseren 223 Kursdateien haben nur 25 eine Stundenauflösung, und
alle 174 Aktiendateien gibt es **nur als Tagesdaten**. Damit ist der
Zusammenhang zwischen Aktien und Krypto, um den es im Konzept geht, auf
Tagesabstand beschränkt — nicht ungenau, sondern grundsätzlich nicht messbar,
wenn er innerhalb eines Tages abläuft.

**Zwei konnte ich nicht messen**, weil sie in den neun Handelsdatenbanken
stehen — und die sind während der laufenden Mac-Sitzung mit Quersummen gesichert.
**Eine solche Datei zu öffnen kann Begleitdateien anlegen und den Vergleich am
Ende scheitern lassen.** Also habe ich es nicht getan und schreibe stattdessen
hin, dass es nicht gemessen ist.

⭐ **Wichtig: keiner der drei Einwände fällt dadurch weg.** Der Einwand gegen den
Test *„nimm die fünf besten Trades weg"* folgt aus der Form solcher
Renditeverteilungen, nicht aus unseren Bots — er gilt also weiter. Was wegfällt,
ist nur meine Behauptung, es sei bei uns schon so.

**Und daraus eine Regel, die ich heute gebraucht hätte:** Ein Name ist kein
Messwert. Dass eine Konstante `MIN_HISTORY_HOURS` heißt, sagt nichts über die
Auflösung der Daten. Dass ein Bot `volatility_breakout` heißt, sagt nichts über
seine Gewinnverteilung. **Jeder Satz in einem Nachtrag sagt künftig, ob er
gemessen oder geschlossen ist.**
