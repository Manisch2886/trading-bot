# Ergebnis — Konzept Sentiment-Sammelschicht (TB-21)

Branch `claude/new-session-b29hhn`, Basis `origin/main` (`a476a98`).

**Kein Produktivcode.** Drei neue Dateien unter `docs/`, sonst nichts. Kein
API-Aufruf, keine Datenbank, kein Schlüssel.

---

## Die Antwort auf Frage 3

**Ja, eine look-ahead-freie Auswertung ist möglich — und sie ist leichter zu
bekommen als im Backtest, weil sie nicht bewiesen, sondern gebaut wird.**
Wer nach vorne sammelt, kann nicht schummeln: das Modell kennt den 20.09. am
13.09. nicht. **Die Unmöglichkeit des Backtests ist die Garantie der
Kausalität.**

Aber nur für **eine von zwei Fragen**:

* **(A) Sagt ein zum Zeitpunkt t gemessener Wert die Rendite nach t voraus?** →
  beantwortbar, sauber.
* **(B) Sagt eine Nachricht vom Zeitpunkt p die Rendite nach p voraus?** →
  **dauerhaft nicht**, weil die Websuche die Kursreaktion zwischen Meldung und
  Abfrage mitgelesen hat.

Deshalb wird der Meldungszeitstempel mitgeschrieben, aber **nie** als
Bezugspunkt der Auswertung benutzt — nur als Diagnose.

**Die grössere Gefahr ist nicht, dass das Modell die Zukunft kennt, sondern
dass der Auswertende sie kennt.** Wer den Parser baut, nachdem er die
Rohantworten gesehen hat, hat kein Look-Ahead-Problem, sondern ein
Data-Snooping-Problem — und das sieht in den Zahlen genauso gut aus.

---

## Die acht Festlegungen — keine getroffen

| # | Frage | Empfehlung |
|---|---|---|
| S1 | Fünfter Agent? | **nein** — eigener Ordner `sentiment/`, Vorbild `broker/` |
| S2 | Eigene DB oder Ereignis-DB? | **eigene** SQLite-Datei |
| S3 | Zuschnitt? | **je Symbol**, gebündelt zu ~10 |
| S4 | Takt? | **täglich**, feste UTC-Zeit |
| S5 | Rohantwort und Wert? | **zwei Tabellen**, Parser versioniert |
| S6 | Fehler? | **Zeile schreiben, nie überspringen** |
| S7 | Stufe 3 bei ungültigem Wert? | **Verhalten wie ohne Sentiment** |
| S8 | Auswerteplan? | **jetzt**, vor dem ersten Datensatz |

---

## Die vier Befunde, die am ehesten überraschen

**Es ist kein fünfter Agent.** Der Unterschied steht in einer Zeile: die vier
Agenten dürfen still scheitern, diese Schicht darf es nicht. Ein Sammler, der
bei fehlendem Schlüssel dreissig Tage schweigend nichts tut, liefert eine Reihe
mit dreissig Lücken — und **eine Lücke sieht in den Zahlen genauso aus wie
„nichts passiert"**. Der nächste Verwandte ist nicht `market_context_agent.py`,
sondern der geplante `ereignis_sammler.py`.

**Nicht in die Ereignis-DB.** Es gibt sie nicht (E1–E6 offen) · dort ist
Verdichtung nach 400 Tagen vorgesehen, eine Rohantwort ist aber ein Beleg und
darf nie verdichtet werden · Kopplung — dieselbe Begründung wie bei E5, nur
andersherum. Berührungspunkt bleibt *eine* Zeile je Sammellauf.

**Drei Monate reichen vermutlich nicht.** Für r = 0,10 braucht es ~783
unabhängige Beobachtungen. Bei **Marktzuschnitt** sind es nach 90 Tagen genau
**90** — damit ist nur r ≥ 0,30 erkennbar, und dieser Zuschnitt ist praktisch
wertlos. **Das ist der Grund für S3.** Bei Symbolzuschnitt (55 × 90) liegt die
wirksame Zahl in der Grössenordnung 600–900, also gerade eben im nötigen
Bereich. Ehrliche Erwartung nach drei Monaten: **„noch kein Urteil,
weitersammeln"**; für ein belastbares Urteil eher ein Jahr.

**Der Handelstakt wird jetzt nicht festgelegt** — und das ist die Antwort, nicht
ihre Verweigerung:

> Der Takt, in dem Sentiment plausibel Information trägt (Stunden bis Tage), ist
> genau der, in dem die Handelskosten sie auffressen. Der Takt, in dem die
> Kosten tragbar sind (Wochen bis Monate), ist genau der, in dem von einer
> Nachrichtenstimmung nichts mehr übrig ist.

Bei 0,30 % je Rundlauf: täglich ~250 = **75 pp/Jahr**, wöchentlich 15,6 pp,
monatlich 3,6 pp. Der Handelstakt ist damit das **Ergebnis** von Stufe 2 (über
die Abklingkurve), nicht ihre Voraussetzung. Der einzige jetzt begründbare Takt
ist der der **Sammlung**: täglich — aus täglichen Werten lässt sich jeder
längere ableiten, umgekehrt nicht.

---

## Was gespeichert wird

Vier Tabellen: `laeufe` (macht Lücken sichtbar) · `abfragen` (Rohantwort im
Original, **zwei** Zeitstempel, **zwei** Modellspalten, Prompt wörtlich) ·
`werte` (abgeleitet, `parser_version`) · `quellen`.

Drei Punkte tragen den Entwurf:

* **`geantwortet_utc`, nicht `angefragt_utc`** ist der kausale Schnitt.
* **Rohantwort und Wert getrennt** — „Ein Wert, eine Quelle" auf eine Messreihe
  angewandt. Ändert sich der Parser, wird die ganze Reihe neu abgeleitet und
  beide Fassungen stehen nebeneinander.
* **Fehler sind Zeilen, keine Lücken.** Ein fehlender Schlüssel ist ein
  **lauter** Fehler mit Rückgabewert ungleich 0, kein leerer String.

---

## Kosten

Gerechnet mit dem einzigen im Projekt **gemessenen** Anker (Agent 3:
0,02–0,03 $ je Auslösung inkl. Websuche). **Grössenordnung, keine
Preisangabe** — der xAI-Preis ist unbelegt (P5).

| Zuschnitt | Aufrufe/Tag | $/Monat |
|---|---|---|
| 175 Symbole einzeln | 175 | 105–158 |
| 175 Symbole, Bündel zu 10 | 18 | 11–16 |
| **55 Symbole, Bündel zu 10** | **6** | **4–5** |

**Empfohlen: 25 Kryptos + 30 Aktien, ~4–5 $/Monat.** Universum am ersten Tag
**eingefroren** (die Krypto-Top-25 ändert sich nach Volumen — ein Coin ist
dort, *weil* er sich gerade bewegt hat). Die Auswahlregel für die 30 Aktien
darf sich auf nichts stützen, was die Bots erlebt haben.

---

## Die Absicherung in Stufe 3

Naheliegend und **falsch**: „kein Wert → glattstellen". Das ist selbst eine
Handlung — ein Anbieterausfall würde das Portfolio umbauen.

**Richtig: der Zustand ohne Signal ist der Zustand vor dem Signal.** Der Bot
verhält sich dann genau wie ohne die Erweiterung. Vier Prüfungen vorher:
vorhanden · frisch · **vom validierten Modell** · vom validierten Prompt und
Parser.

> **Wechselt der Anbieter das Modell, schaltet sich das Signal von selbst ab**,
> statt mit einer unvergleichbaren Zahl weiterzuhandeln.

Dazu: Sentiment darf nur **wegnehmen**, nie hinzufügen (kein Trade wird
erzeugt, nur verhindert — Schadensobergrenze messbar). Und der Anteil der
Rückfalltage wird gezählt und angezeigt.

---

## Zu entscheiden

**F1** Wird Stufe 1 begonnen — und für welche Dauer zugesagt? (drei Monate
liefern wahrscheinlich kein Urteil) · **F2** welcher Monatsbetrag? · **F3** nach
welcher Regel wird das Aktienuniversum eingefroren? · **F4** wer belegt die
xAI-Angaben?

## Zu belegen, nichts davon geprüft

**P1 die API-Adresse** — Vorlage sagt `https://api.xai.com/v1`, geläufiger ist
`https://api.x.ai/v1`; **beides unbelegt, im Entwurf als zu prüfen markiert.**
Eine falsche Adresse erzeugt Code, der stillschweigend gegen nichts läuft.
Dazu **P2** Modellkennungen und Aliase · **P3** ob die Antwort eine aufgelöste
Modellkennung zurückmeldet · **P4** server-seitige Websuche und Quellen mit
Datum (ohne Websuche misst man den Trainingsstand — dann ist das Vorhaben
hinfällig) · **P5** Preise · **P6** JSON-Schema · **P7** Determinismus ·
**P8** Nutzungsbedingungen zur Speicherung.

---

## Was der Entwurf nicht kann

**Ob Sentiment-Handel trägt, beantwortet er nicht** — das ist eine Frage der
Literatur und der Empirie, keine der Architektur. Ebenso wenig, ob Grok dafür
taugt. Er belegt keine xAI-Angabe, kann Frage (B) dauerhaft nicht beantworten,
schafft keine statistische Kraft herbei, weckt den schlafenden Mac nicht (Cron
holt nichts nach — Lücken werden sichtbar gemacht, nicht verhindert) und kann
Data Snooping nicht technisch verhindern.
