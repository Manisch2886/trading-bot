# Übergabe: Konzept Sentiment-Sammelschicht (TB-21)

**Branch** `claude/new-session-b29hhn`, Basis `origin/main` (`a476a98`, nach
Merge von #91).

**Kein Produktivcode.** Der Diff enthält ausschliesslich drei neue Dateien
unter `docs/`. Kein API-Aufruf gegen xAI oder einen anderen Anbieter, keine
Datenbank angelegt, kein Schlüssel verwendet, kein bestehender Code angefasst.

---

## Frage 3 zuerst: Ist eine look-ahead-freie Auswertung überhaupt möglich?

**Ja — und sie ist hier leichter zu bekommen als im Elliott-Wave-Backtest, weil
sie nicht bewiesen, sondern gebaut wird.**

Der Grund ist derselbe, der die Strategie unbacktestbar macht: Wer heute nach
vorne sammelt, kann nicht schummeln. Das Modell kennt den 20.09.2026 am
13.09.2026 nicht. **Die Unmöglichkeit des Backtests ist die Garantie der
Kausalität.** Im Backtest musste sie nachträglich belegt werden — 1301 Trades
einzeln geprüft. Bei einer Vorwärtssammlung entsteht sie strukturell.

**Aber nur für eine von zwei Fragen**, und das ist die wichtigste
Unterscheidung des ganzen Entwurfs:

| | Frage | beantwortbar? |
|---|---|---|
| **A** | Sagt ein zum Zeitpunkt t **gemessener** Wert die Rendite nach t voraus? | **ja**, sauber |
| **B** | Sagt eine **Nachricht** vom Zeitpunkt p die Rendite nach p voraus? | **nein, dauerhaft nicht** |

Bei (B) hat die Websuche die Kursreaktion zwischen Meldung und Abfrage längst
mitgelesen. Der Wert ist zum **Abfragezeitpunkt** sauber, als Aussage über den
**Meldungszeitpunkt** verdorben. Deshalb wird der Meldungszeitstempel im Entwurf
zwar mitgeschrieben, aber **nie** als Bezugspunkt der Auswertung benutzt — er
taugt nur als Diagnose („wie alt sind die Meldungen, aus denen der Wert
entsteht?").

Drei Bedingungen müssen halten. Zwei sind Handwerk:

* **K1** — Der Prompt enthält keine Information von nach t. Strukturell
  gesichert, weil der Prompt wörtlich mitgeschrieben wird.
* **K2** — Das Renditefenster beginnt streng nach dem Zeitpunkt, zu dem die
  **Antwort da war**, nicht nach dem Absenden. Deshalb führt das Schema zwei
  Zeitstempel. Mechanisch prüfbar, mit Gegenprobe (Prinzip 12).

Die dritte ist die eigentliche Gefahr:

* **K3** — Der Auswerteplan steht fest, **bevor** die ersten Daten da sind.

> **Die grössere Gefahr ist nicht, dass das Modell die Zukunft kennt. Sie ist,
> dass der Auswertende sie kennt.** Wer den Parser baut, nachdem er die
> Rohantworten gesehen hat, und die Kennzahl wählt, nachdem er weiss, welche
> korreliert, hat kein Look-Ahead-Problem — er hat ein Data-Snooping-Problem,
> und das sieht in den Zahlen genauso gut aus wie ein Fund.

Der Entwurf enthält deshalb einen vorab festzulegenden Auswerteplan (Abschnitt
6 des Konzepts). Er kostet heute eine Stunde und ist nach dem ersten Datensatz
nicht mehr nachholbar.

**Und eine vierte Sache, die keine Bedingung ist, sondern eine Grenze:** drei
Monate reichen statistisch wahrscheinlich nicht. Dazu unten mehr — es ist der
Befund, der die Bauweise am stärksten verändert hat.

---

## Die acht Festlegungen — jede mit Empfehlung, keine getroffen

| # | Frage | Empfehlung |
|---|---|---|
| **S1** | Fünfter Agent, oder etwas anderes? | **etwas anderes**: eigener Ordner `sentiment/`, Vorbild `broker/` |
| **S2** | Eigene DB oder die geplante Ereignis-DB? | **eigene** SQLite-Datei; eine Zeile *in* die Ereignis-DB, falls sie kommt |
| **S3** | Zuschnitt: je Symbol, je Markt, je Sektor? | **je Symbol**, gebündelt zu ~10 je Aufruf |
| **S4** | Takt der Sammlung? | **einmal täglich**, feste UTC-Zeit |
| **S5** | Rohantwort und Wert: eine Tabelle oder zwei? | **zwei** — Rohantwort ist Beleg, Wert ist versionierte Ableitung |
| **S6** | Fehler und fehlender Schlüssel? | **Zeile schreiben, nie überspringen** — und laut melden |
| **S7** | Absicherung in Stufe 3? | „kein Wert" = **Verhalten wie ohne Sentiment**; jeder Rückfall wird gezählt |
| **S8** | Auswerteplan jetzt oder später? | **jetzt**, vor dem ersten Datensatz |

---

## Die vier Befunde, bei denen ich Widerspruch erwarte

### 1. Es ist kein fünfter Agent

Der nächste Verwandte sieht wie ein Zwilling aus: `market_context_agent.py`
nutzt Sonnet 5 mit server-seitiger Websuche, fasst Nachrichten zu Symbolen
zusammen und ist ausdrücklich rein informativ. Trotzdem ist die Bauweise die
falsche, und der Unterschied steht in einer einzigen Zeile:

**Die vier Agenten dürfen still scheitern. Diese Schicht darf es nicht.**

`call_claude` wirft absichtlich nie, und ein fehlender Schlüssel gibt `""`
zurück. Für eine E-Mail-Zeile ist das genau richtig. Für eine Messreihe ist es
das Fehlerbild, das dieses Projekt schon einmal Monate gekostet hat: **eine
Lücke sieht in den Zahlen genauso aus wie „nichts passiert"**
(`docs/DATENLUECKEN.md`, offener Punkt 12). Ein Sammler, der bei fehlendem
Schlüssel dreissig Tage lang schweigend nichts tut, liefert am Ende eine Reihe
mit dreissig fehlenden Tagen, und niemand weiss, ob dort nichts war oder nichts
lief.

Der nächste Verwandte ist deshalb nicht Agent 3, sondern der vorgeschlagene
`shared/ereignis_sammler.py` — und, was die Bauweise angeht, `broker/spiegel.py`.

**Zum Ordner:** `broker/` ist der Präzedenzfall. Das Projekt hat schon einmal
einen Ordner auf oberster Ebene angelegt, als ein Teilsystem eigene Gegenstelle,
eigene Zugangsdaten, eigene `requirements.txt` und eigenes Risikoprofil hatte.
Auf `sentiment/` trifft alles vier zu. Gegen `shared/` spricht dessen eigene
Definition im Übergabeprotokoll — „von ALLEN neun Strategien genutzt" —, und
dass dann `claude_client.py` und `xai_client.py` mit verschiedenen Schlüsseln
nebeneinanderlägen. `research/` wäre knapp die zweitbeste Wahl; dort liefe aber
erstmals ein Cronjob monatelang in einem Ordner, der bisher ausschliesslich
**abgeschlossene** Untersuchungen enthält. **Falls Sie sich anders entscheiden,
ändert das an Schema, Takt, Kosten und Auswertung nichts — nur die Pfade.**

### 2. Nicht in die geplante Ereignis-DB

Naheliegend wäre, die Sammlung in die zentrale Ereignis-DB aus
`docs/KONZEPT_ereignisse_und_anbieter.md` zu legen. Drei Gründe dagegen, der
erste trägt allein:

1. **Es gibt sie nicht.** E1–E6 sind unentschieden. Stufe 1 daran zu hängen
   hiesse, eine Sammlung, deren einziger Wert im frühen Beginn liegt, auf eine
   offene Konzeptfrage zu vertagen.
2. **Die Aufbewahrung beweist den Zweckunterschied.** Dort ist Verdichtung nach
   400 Tagen vorgesehen (E6). Eine Rohantwort ist der **Beleg** einer Messung
   und darf nie verdichtet werden — sie ist die einzige Möglichkeit, die Reihe
   neu abzuleiten, wenn sich der Parser ändert.
3. **Kopplung** — genau die Begründung, mit der E5 empfohlen wurde, nur in die
   andere Richtung: eine Forschungsreihe soll nicht an einer Tabelle hängen, in
   die sieben Produktivpfade schreiben.

Der saubere Berührungspunkt bleibt: **eine** Zeile je Sammellauf
(`art='sentiment_lauf'`), falls die Ereignis-DB kommt. Nicht je Abfrage, nie
die Rohantwort. Dieselbe Trennung wie `spiegelungen` gegen Ereignis.

### 3. Drei Monate reichen vermutlich nicht — und das hat die Bauweise geändert

Standardrechnung, 80 % Teststärke, α = 0,05:

| zu erkennende Korrelation | nötige unabhängige Beobachtungen |
|---|---|
| r = 0,30 (sehr gross) | ~85 |
| r = 0,20 | ~194 |
| r = 0,10 (realistisch) | **~783** |

**Bei Marktzuschnitt** liefern 90 Tage genau **90** Beobachtungen je Markt.
Damit ist nur r ≥ 0,30 erkennbar — ein Effekt dieser Grösse wäre für ein
Nachrichtensignal aussergewöhnlich. **Der Marktzuschnitt ist damit praktisch
wertlos, und genau das ist der Grund für S3 (je Symbol).**

**Bei Symbolzuschnitt** kommen 55 Symbole × 90 Tage = 4950 Zeilen zusammen —
aber sie sind nicht unabhängig, Kryptos und Aktien bewegen sich jeweils stark
gemeinsam. Die wirksame Zahl liegt eher bei *Tage × unabhängige Faktoren*, grob
geschätzt in der **Grössenordnung 600–900**. Also gerade eben im Bereich, in
dem r = 0,10 erkennbar wäre. Das ist eine Grössenordnungsabschätzung, keine
exakte Rechnung; die Zahl der wirksamen Faktoren lässt sich aus den vorhandenen
Kursdaten vorab bestimmen und sollte es auch — **vor** dem Start, weil sie die
Universumsgrösse mitbestimmt.

**Was daraus folgt, offen gesagt:** Die ehrliche Erwartung nach drei Monaten
ist nicht „ja" oder „nein", sondern **„noch kein Urteil, weitersammeln"**, und
die Grössenordnung für ein belastbares Urteil ist eher **ein Jahr**. Das ist
kein Argument gegen den Start — es ist eines dafür, jetzt zu starten und die
Erwartung an den 3-Monats-Punkt tief zu hängen. Es ist auch dieselbe Lage wie
bei den Bots: keiner erreicht bisher `MIN_LIVE_CLOSED_TRADES = 10`, und die
Prüftermine liegen deshalb im Oktober 2026 und Januar 2027.

### 4. Der Handelstakt wird jetzt nicht festgelegt — und das ist die Antwort, nicht ihre Verweigerung

Die Aufgabe bittet um einen Takt-Vorschlag mit Begründung. Die Begründung führt
zu einem Widerspruch, der wichtiger ist als jede Zahl:

> Der Takt, in dem Sentiment plausibel Information trägt — Stunden bis wenige
> Tage —, ist genau der Takt, in dem die Handelskosten sie auffressen. Der
> Takt, in dem die Kosten tragbar sind — Wochen bis Monate —, ist genau der
> Takt, in dem von einer Nachrichtenstimmung plausibel nichts mehr übrig ist.

Bei 0,30 % je Rundlauf: täglich ~250 Rundläufe = **75 pp/Jahr**, wöchentlich
~52 = 15,6 pp, monatlich ~12 = 3,6 pp. Das ist der Befund, an dem E2 verworfen
wurde, nur allgemein formuliert — und es ist **kein** Argument gegen Stufe 1,
sondern das schärfste dafür, die Sache zu messen statt zu vermuten.

**Der Handelstakt ist deshalb das Ergebnis von Stufe 2, nicht ihre
Voraussetzung.** Stufe 2 misst die Abklingkurve über 1/2/5/10/20 Tage, und die
Antwort fällt in genau eine von drei Klassen (Wirkung nur Tag 0–1 → kein Stufe
3, 75 pp sind nicht zu verdienen · Wirkung hält 5–20 Tage → Stufe 3 denkbar ·
keine Wirkung → kein Stufe 3, und das ist ein gutes Ergebnis). Wer heute einen
Takt festlegt, legt ihn ohne die einzige Zahl fest, die ihn bestimmen könnte.

**Der einzige Takt, der jetzt begründbar ist, ist der der Sammlung: täglich.**
Aus täglichen Werten lässt sich jeder längere ableiten, umgekehrt nicht. Was
nicht gesammelt wurde, ist weg.

---

## Der stärkste Einzelmechanismus des Entwurfs

Zur Frage „was passiert bei einem ungültigen Modellergebnis in Stufe 3" (S7)
gibt es eine naheliegende Antwort, die **falsch** ist: „kein Wert → keine
Position" oder „kein Wert → alles glattstellen". Beides ist selbst eine
Handlung — ein Ausfall beim Anbieter würde damit das Portfolio umbauen.

Richtig ist: **Der Zustand ohne Signal ist der Zustand vor dem Signal.** Ein
fehlender, veralteter oder ungültiger Wert führt dazu, dass der Bot sich genau
so verhält wie ohne die Sentiment-Erweiterung — also wie die validierte
Grundstrategie.

Daraus folgen vier Prüfungen, bevor der Wert überhaupt angesehen wird:
vorhanden und im erwarteten Bereich · frisch · **vom validierten Modell** · vom
validierten Prompt und Parser. Die dritte ist der stärkste Mechanismus des
ganzen Entwurfs:

> **Wechselt der Anbieter das Modell, schaltet sich das Signal von selbst ab**,
> statt mit einer unvergleichbaren Zahl weiterzuhandeln — bis Stufe 2 neu
> gerechnet ist.

Genau das ist der Schaden, den die Aufgabe unter „Warum der Modell-Zeitstempel
zählt" beschreibt. Er ist hier nicht nur erkennbar, sondern folgenlos gemacht.
Deshalb führt das Schema **zwei** Modellspalten: was angefordert wurde, und was
die API zurückmeldet.

Dazu zwei Grenzen, die auch in Stufe 3 gälten: **Sentiment darf nur wegnehmen,
nie hinzufügen** (es kann einen Trade verhindern, keinen erzeugen — dann ist
die Schadensobergrenze die entgangene Rendite der Grundstrategie, und die ist
messbar; dieselbe Vorsicht, mit der Agent 3 nie als News-Veto gebaut wurde).
Und: **der Anteil der Rückfalltage wird gezählt und angezeigt** — ein Bot, der
an 40 % der Tage zurückfällt, ist nicht der Bot, der validiert wurde.

---

## Kosten: die Zeile, die ich empfehle

**Zum xAI-Preis steht hier bewusst keine Zahl** (siehe unten, P5). Gerechnet
wird mit dem einzigen im Projekt **gemessenen** Anker für einen vergleichbaren
Aufruf: Agent 3 kostet 0,02–0,03 $ je Auslösung inklusive Websuch-Gebühr. Das
ist eine **Grössenordnung, keine Preisangabe**.

| Zuschnitt | Aufrufe/Tag | $/Monat | 90 Tage |
|---|---|---|---|
| 175 Symbole einzeln | 175 | 105–158 | 315–473 |
| 175 Symbole, Bündel zu 10 | 18 | 11–16 | 32–49 |
| **55 Symbole, Bündel zu 10** | **6** | **4–5** | **11–16** |
| 2 Märkte | 2 | 1–2 | 4–5 |

**Empfohlen: 25 Krypto-Paare + 30 Aktien, 6 Bündelaufrufe am Tag, rund 4–5 $
im Monat.** 150 Aktien kosten das Fünffache und bringen weniger als das
Fünffache an Kraft, weil sie sich stark gemeinsam bewegen.

Zum Vergleich: die vier bestehenden Agenten kosten zusammen deutlich unter
1 €/Monat. Selbst die empfohlene Zeile ist ein Vielfaches des heutigen
KI-Verbrauchs — allerdings ein Vielfaches von fast nichts.

**Zwei Dinge, die dabei nicht schiefgehen dürfen:** Das Universum wird am
ersten Tag **eingefroren** (die Krypto-Liste des Projekts wird nach
24-Stunden-Volumen gerankt — ein Coin rutscht in die Top 25, *weil* er sich
gerade bewegt hat). Und die Auswahlregel für die 30 Aktien darf sich auf
**nichts** stützen, was die Bots erlebt haben — das wäre derselbe Fehler wie
beim Aktien-Universum 2026.

---

## Was Sie entscheiden müssen, bevor etwas gebaut wird

**F1 — Wird Stufe 1 begonnen, und für welchen Zeitraum wird sie zugesagt?**
Drei Monate liefern wahrscheinlich kein Urteil, ein Jahr eher. Eine Sammlung,
die nach drei Monaten mit „unklar" abgebrochen wird, war drei Monate umsonst —
dieselbe Falle, die der Auftrag selbst benennt, eine Ebene höher. **Die Zusage
der Dauer ist Teil der Entscheidung, nicht ihre Folge.**

**F2 — Welcher Monatsbetrag ist vertretbar?** 4–5 $, 11–16 $ oder 105–158 $ —
eine Abwägung zwischen Geld und statistischer Kraft.

**F3 — Nach welcher Regel wird das Aktienuniversum auf 30 eingefroren?**
Denkbar: die 30 grössten nach Marktkapitalisierung am Starttag · je Sektor die
grössten drei · Zufallsauswahl mit festgehaltenem Startwert. Empfehlung nur der
Form nach: eine Regel, am Starttag angewandt, festgehalten, danach nie wieder
angefasst.

**F4 — Wer belegt die xAI-Angaben?** Solange sie unbelegt sind, ist der Entwurf
nicht baureif.

---

## Was noch belegt werden muss — acht Punkte, keiner geprüft

Es wurde **kein** Aufruf gemacht und **nichts** aus dem Gedächtnis festgelegt.

**P1 — die API-Adresse.** In einer vorliegenden Vorlage steht
`https://api.xai.com/v1`, geläufiger ist `https://api.x.ai/v1` — **beides ist
hier unbelegt und im Entwurf als zu prüfen markiert.** Warum das genau hier
gefährlich ist: eine falsche Adresse erzeugt Code, der stillschweigend gegen
nichts läuft. Zusammen mit der Agenten-Gewohnheit „Fehler geben leeren Text
zurück" ergibt das eine Sammlung, die monatelang leer bleibt, ohne dass es
auffällt. Genau deshalb steht im Entwurf, dass ein fehlender Schlüssel ein
**lauter** Fehler sein muss.

Dazu: **P2** genaue Modellkennungen und ob es Aliase gibt · **P3** ob die
Antwort eine aufgelöste Modellkennung zurückmeldet (davon hängt ab, ob die
Selbstabschaltung aus dem vorigen Abschnitt überhaupt baubar ist) · **P4** ob
es eine server-seitige Websuche gibt und ob sie Quellen **mit Datum** liefert
(ohne Websuche misst man den Trainingsstand, nicht die Lage — dann ist das
Vorhaben hinfällig) · **P5** die Preise · **P6** strukturierte Ausgabe
(JSON-Schema) · **P7** Determinismus (`seed`, `temperature`) · **P8** die
Nutzungsbedingungen zur Speicherung von Antworten und Suchergebnissen über
Monate.

---

## Was der Entwurf ausdrücklich nicht kann

1. **Ob Sentiment-Handel trägt, beantwortet er nicht.** Das ist eine Frage der
   Literatur und der Empirie, keine der Architektur. Er baut das Messgerät und
   sagt, was es messen kann — nicht, was herauskommt.
2. **Ob Grok dafür taugt, beantwortet er nicht.** Weder Qualität noch
   Verfügbarkeit noch Stabilität wurden geprüft.
3. **Er belegt keine einzige xAI-Angabe** (P1–P8).
4. **Frage (B) bleibt dauerhaft unbeantwortbar** — unabhängig von der
   Sammeldauer.
5. **Er kann keine statistische Kraft herbeischaffen.**
6. **Er kann den schlafenden Mac nicht wecken.** Cron holt nichts nach; die
   Sammlung kann Lücken nur sichtbar machen (`laeufe`), nicht verhindern.
7. **Data Snooping (K3) kann er nicht technisch verhindern** —
   `parser_version` macht es sichtbar, unterlassen muss man es selbst.
8. **Er enthält keinen Code, keine Tests, keine Datenbank.**

---

## Prüfung der Randbedingungen des Auftrags

| Randbedingung | Stand |
|---|---|
| Nur neue Dateien unter `docs/` im Diff | **eingehalten** — `git diff origin/main HEAD --name-only` listet drei Dateien unter `docs/` |
| Kein Produktivcode, keine Tests, keine Datenbank | **eingehalten** |
| Kein API-Aufruf gegen xAI oder einen anderen Anbieter | **eingehalten** |
| `live_params.py`, `forward_test.py`, `equity_simulation.py` nicht angefasst | **eingehalten** |
| Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage | **eingehalten** |
| Zugangsdaten nie zitiert | **eingehalten** — es wurde keine Datei mit Zugangsdaten gelesen; `config/email_config.py`, `shared/fetch_binance_data.py` und `.env` sind gitignored und liegen in dieser Sitzung ohnehin nicht vor |
| API-Adresse als „zu prüfen" markiert, nicht geraten | **eingehalten** — P1, dazu P2–P8 nach derselben Regel |
| Kein Testdokument | **entfällt**, es gibt nichts auszuführen |

---

## Eine Korrektur an einer Zahl aus der Aufgabe

Der Auftrag nennt zum Elliott-Wave-Look-Ahead „von +1 500 % auf +353 %
gedrückt". Die Zahlen stimmen, die Zuordnung ist etwas zu eng: Die abgelegte
Ergebniskurve von `elliott_wave_stocks` trug **+1500,53 %** und steht nach
Neuberechnung bei **+352,72 %** — dieser Rückgang hat allerdings **zwei**
Ursachen, den Look-Ahead **und** einen Parameterwechsel vom 03.09.2026, nach
dem die Kurve nie neu erzeugt wurde (Übergabeprotokoll, offener Punkt 18).

Den Look-Ahead allein beziffert `research/elliott_wave_lookahead/` anders und
deutlich drastischer: `elliott_wave` **+2184,96 % → −24,44 %**,
`elliott_wave_stocks` **+3084,09 % → +338,26 %**.

Am Gewicht des Beispiels ändert das nichts — es macht es eher grösser. Der
Entwurf führt die Korrektur in Abschnitt 5.1 mit.

---

## Die drei Dateien

| Datei | Inhalt |
|---|---|
| `docs/KONZEPT_sentiment_sammelschicht.md` | der Entwurf, 11 Abschnitte |
| `docs/ERGEBNIS_TB21_sentiment_sammelschicht.md` | Kurzfassung zum Kopieren |
| `docs/UEBERGABE_TB21_sentiment_sammelschicht.md` | dieses Dokument |
