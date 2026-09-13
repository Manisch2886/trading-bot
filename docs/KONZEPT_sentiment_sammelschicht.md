# Konzept: Sentiment-Sammelschicht (Stufe 1)

**Entwurfsdokument, kein Produktivcode.** Stand 13.09.2026, Basis `origin/main`
(`a476a98`, nach Merge von #91). Alle Code-Ausschnitte sind **Skizzen im
Dokument**, keine Dateien im Repo. Es wurde kein API-Aufruf gegen xAI oder
einen anderen Anbieter gemacht, keine Datenbank angelegt, kein Schlüssel
verwendet.

Geschrieben für eine Entscheidung. Abschnitt 0 nennt die Antwort auf die
wichtigste Frage, Abschnitt 1 listet, was zu entscheiden ist; alles Weitere ist
Begründung.

---

## 0. Die Antwort auf Frage 3, vorweg

**Ja — eine look-ahead-freie Auswertung ist möglich. Sie ist sogar leichter zu
bekommen als im Elliott-Wave-Backtest, weil sie hier nicht bewiesen, sondern
gebaut wird.**

Der Grund ist derselbe, der die Strategie unbacktestbar macht. Wer heute nach
vorne sammelt, kann nicht schummeln: das Modell kennt den 20.09.2026 am
13.09.2026 nicht. **Die Unmöglichkeit des Backtests *ist* die Garantie der
Kausalität.** Im Backtest musste die Kausalität nachträglich belegt werden —
1301 Trades einzeln geprüft (`research/elliott_wave_lookahead/`, Nachtrag K).
Bei einer Vorwärtssammlung entsteht sie strukturell.

Das gilt aber nur **für eine bestimmte Frage**, und es gibt drei Bedingungen.

**Die Frage, die beantwortbar ist (A):** *Sagt ein Wert, der zum Zeitpunkt t
gemessen wurde, die Rendite nach t voraus?*

**Die Frage, die NICHT beantwortbar ist (B):** *Sagt eine Nachricht vom
Zeitpunkt p die Rendite nach p voraus?* — Wird das Modell heute nach einer
Meldung von vorgestern gefragt, hat die Websuche die Kursreaktion dieser zwei
Tage längst mitgelesen. Der Wert ist zum **Abfragezeitpunkt** sauber, als
Aussage über den **Meldungszeitpunkt** ist er verdorben. Diese Unterscheidung
ist der Kern des Entwurfs, und sie ist der Grund, warum der Meldungszeitstempel
zwar mitgeschrieben, aber **nie** als Bezugspunkt der Auswertung benutzt werden
darf.

**Die drei Bedingungen:**

| # | Bedingung | Wer sichert sie |
|---|---|---|
| K1 | Der Prompt enthält keine Information von nach t | Stufe 1, strukturell (Prompt wird wörtlich mitgeschrieben) |
| K2 | Das Renditefenster beginnt **streng nach** dem Zeitpunkt, zu dem die **Antwort da war** — nicht nach dem Absenden | Stufe 2, mechanisch prüfbar |
| K3 | Der Auswerteplan steht fest, **bevor** die ersten Daten da sind | nur der Nutzer, und nur jetzt |

K1 und K2 sind Handwerk. **K3 ist die eigentliche Gefahr**, und sie ist kein
Look-Ahead, sondern sein hässlicherer Verwandter:

> **Die grössere Gefahr ist nicht, dass das Modell die Zukunft kennt. Sie ist,
> dass der Auswertende sie kennt.** Wer den Parser baut, nachdem er die
> Rohantworten gesehen hat, und die Kennzahl wählt, nachdem er weiss, welche
> korreliert, hat kein Look-Ahead-Problem — er hat ein Data-Snooping-Problem,
> und das sieht in den Zahlen genauso gut aus.

Deshalb enthält dieser Entwurf einen **vorab festzulegenden Auswerteplan**
(Abschnitt 6). Er kostet heute eine Stunde und ist nach dem ersten
Datensatz nicht mehr nachholbar.

**Und eine vierte Einschränkung, die keine Bedingung ist, sondern eine
Grenze:** drei Monate reichen statistisch wahrscheinlich nicht. Siehe
Abschnitt 6.3 — die Grössenordnung ist eher **ein Jahr**. Das ändert die
Bauweise (Abschnitt 3: je Symbol statt je Markt) und es ändert, was von Stufe 2
zu erwarten ist: eher „noch kein Urteil" als „ja" oder „nein".

---

## 1. Was zu entscheiden ist

Acht Festlegungen. Bei jeder steht eine Empfehlung mit Alternative und
Begründung — **keine ist getroffen.** Dazu vier Fragen, die ohne den Nutzer
nicht zu beantworten sind.

| # | Frage | Empfehlung | steht in |
|---|---|---|---|
| **S1** | Fünfter Agent, oder etwas anderes? | **etwas anderes**: eigener Ordner `sentiment/`, Vorbild `broker/` | 2 |
| **S2** | Eigene DB oder die geplante Ereignis-DB? | **eigene** SQLite-Datei; eine Zeile *in* die Ereignis-DB, falls sie kommt | 2.3 |
| **S3** | Zuschnitt: je Symbol, je Markt, je Sektor? | **je Symbol**, gebündelt zu ~10 je Aufruf | 3.1 |
| **S4** | Takt der Sammlung? | **einmal täglich**, feste UTC-Zeit | 3.2 |
| **S5** | Rohantwort und ausgewerteter Wert: eine Tabelle oder zwei? | **zwei** — Rohantwort ist Beleg, Wert ist versionierte Ableitung | 4.2 |
| **S6** | Was passiert bei Fehlern und fehlendem Schlüssel? | **Zeile schreiben, nie überspringen** — und laut melden | 4.4 |
| **S7** | Wie sähe die Absicherung in Stufe 3 aus? | „kein Wert" = **Verhalten wie ohne Sentiment**, jeder Rückfall wird gezählt | 7.2 |
| **S8** | Auswerteplan jetzt oder später? | **jetzt**, vor dem ersten Datensatz | 6 |

**Die vier Fragen an den Nutzer** (Abschnitt 8): Wird Stufe 1 überhaupt
begonnen und wofür wie lange · welcher Monatsbetrag ist vertretbar · nach
welcher Regel wird das Forschungsuniversum eingefroren · wer belegt die
xAI-Angaben aus der offiziellen Dokumentation.

---

## 2. Wo das im Projekt hingehört (S1)

### 2.1 Ist es ein fünfter Agent?

Angesehen: `shared/market_context_agent.py`, `shared/claude_client.py`,
`shared/daily_interpreter.py`, `shared/param_search_agent.py`,
`shared/portfolio_interpreter_agent.py`, `shared/quarterly_interpreter.py`.

Der nächste Verwandte ist **Agent 3** (`market_context_agent.py`): Sonnet 5 mit
server-seitiger Websuche, 3–5 Sätze zu aktuellen Nachrichten, ausdrücklich rein
informativ. Das sieht auf den ersten Blick aus wie genau das, was hier gebaut
werden soll. Es ist es nicht.

| | die vier Agenten | die Sammelschicht |
|---|---|---|
| Zweck | Text für einen Menschen, **jetzt** | Datenreihe für eine Auswertung, **in Monaten** |
| Ausgabe | wandert in eine E-Mail und ist danach weg | muss dauerhaft, abfragbar und **über Monate vergleichbar** bleiben |
| Fehlerverhalten | leerer String, Bot läuft weiter — richtig so | leerer String wäre eine **unsichtbare Datenlücke** |
| Anbieter | Anthropic, über `claude_client.py` | **xAI**, eigener Schlüssel, eigener Endpunkt |
| Prompt-Änderung | folgenlos | bricht die Vergleichbarkeit der ganzen Reihe |
| Modellwechsel | folgenlos | bricht die Vergleichbarkeit der ganzen Reihe |

**Die entscheidende Zeile ist die dritte.** Die vier Agenten dürfen still
scheitern — `call_claude` wirft absichtlich nie, und ein fehlender Schlüssel
gibt `""` zurück. Für eine Anzeige-Funktion ist das genau richtig. Für eine
Messreihe ist es das Fehlerbild, das dieses Projekt schon einmal Monate
gekostet hat: **eine Lücke sieht in den Zahlen genauso aus wie „nichts
passiert"** (`docs/DATENLUECKEN.md`, offener Punkt 12 des Übergabeprotokolls).

Ein Sammler, der bei fehlendem Schlüssel dreissig Tage lang schweigend nichts
tut, liefert am Ende eine Reihe mit dreissig fehlenden Tagen — und niemand
weiss, ob dort nichts war oder nichts lief.

**Die Sammelschicht ist also kein fünfter Agent, sondern ein Sammler.** Ihr
nächster Verwandter im Projekt ist nicht `market_context_agent.py`, sondern
der vorgeschlagene `shared/ereignis_sammler.py` aus
`docs/KONZEPT_ereignisse_und_anbieter.md`, Abschnitt 2.5 — und, was die
Bauweise angeht, `broker/spiegel.py`.

### 2.2 Welcher Ordner

**Empfehlung: ein neuer Ordner `sentiment/` auf oberster Ebene**, Geschwister
von `broker/`, `notifications/`, `dashboard/`, `research/`.

*Begründung — `broker/` ist der Präzedenzfall.* Das Projekt hat schon einmal
einen eigenen Ordner auf oberster Ebene angelegt, als ein Teilsystem diese vier
Eigenschaften hatte: eigene Gegenstelle, eigene Zugangsdaten, eigene
`requirements.txt`, eigenes Risikoprofil. Auf die Sammelschicht trifft alles
vier zu. Und der Ordnername macht die Grenze sichtbar: was in `sentiment/`
liegt, wird von nichts in `strategies/` importiert — genauso wie `broker/`
keinen Bot-Code anfasst.

*Alternative A: `shared/sentiment_sammler.py` + `shared/xai_client.py`.*
**Verworfen aus zwei Gründen.** Erstens sagt das Übergabeprotokoll über
`shared/`: „von ALLEN neun Strategien genutzt" — die Sammelschicht wird von
*keiner* genutzt. Zweitens hiesse der eine Anbieter-Wrapper dort
`claude_client.py` und der andere `xai_client.py`, im selben Ordner, mit
verschiedenen Schlüsseln; das ist die Sorte Nachbarschaft, in der jemand
irgendwann den falschen importiert.

*Alternative B: `research/sentiment_sammlung/`.* **Verworfen, aber knapp.**
Dafür spräche viel: es *ist* eine Untersuchung, und die Projektregel
„Untersuchungen fassen keinen Bot-Code an" wäre damit automatisch bindend.
Dagegen spricht, dass alles unter `research/` **abgeschlossene** Untersuchungen
mit einem `BERICHT.md` sind — hier liefe erstmals ein Cronjob monatelang in
einem `research/`-Ordner. Das wäre ein Präzedenzfall mit Folgen für alle
künftigen Ordner dort.

> **Falls Alternative B trotzdem gewählt wird**, ändert das an Schema, Takt,
> Kosten und Auswertung dieses Entwurfs **nichts** — nur die Pfade. Die
> Entscheidung ist Ordnung, nicht Architektur.

Skizze des Ordners:

```
sentiment/                          (Entwurf, existiert nicht)
├── xai_zugang.py                   Schlüssel aus .env, NIE aus dem Repo
├── xai_client.py                   der eine Aufrufpunkt zum Anbieter
├── prompts.py                      Systemprompt + Version, EINZIGE Stelle
├── schema.sql                      die vier Tabellen aus Abschnitt 4
├── sammler.py                      der Cronjob
├── universum.py                    eingefrorene Symbolliste + Snapshot-Id
├── auswertung_plan.md              der vorab festgelegte Plan (Abschnitt 6)
├── requirements.txt                separat, wie broker/requirements.txt
├── README.md
└── test_sammler.py                 Selbsttests gegen Attrappen, kein Netz
```

Die Datenbank liegt **nicht** im Repo: `*.db` steht bereits in `.gitignore`.

### 2.3 Wo die Daten liegen (S2)

Drei Möglichkeiten, alle drei ernsthaft geprüft.

| | eigene SQLite-Datei | zentrale Ereignis-DB | JSONL-Dateien |
|---|---|---|---|
| Existiert heute | nein, aber sofort baubar | **nein, und E1–E6 sind unentschieden** | ja, trivial |
| Abfragbar für Stufe 2 | ja | ja | nur mit eigenem Leser |
| Doppelschreib-Schutz | `UNIQUE`, wie die drei Vorbilder | dito | keiner |
| Kopplung an Produktivbetrieb | keine | **Forschung hängt an einer Beobachtungstabelle** | keine |
| Aufbewahrung | unbegrenzt, ~30 MB/Jahr | dort ist **Verdichtung nach 400 Tagen** vorgesehen | unbegrenzt |

**Empfehlung: eigene SQLite-Datei** `sentiment/sentiment.db`, gebaut nach dem
Muster der drei vorhandenen Nachverfolgungs-DBs (fachlicher Schlüssel mit
`UNIQUE`, Erfolg und Versuch getrennt, Zeitstempel als UTC-Text).

*Drei Gründe, der erste trägt allein:*

1. **Die Ereignis-DB gibt es nicht.** E1 bis E6 sind offene Entscheidungen.
   Stufe 1 daran zu hängen hiesse, eine Sammlung, deren einziger Wert im
   frühen Beginn liegt, auf eine unentschiedene Konzeptfrage zu vertagen.
2. **Die Zwecke sind verschieden, und die Aufbewahrung beweist es.** Die
   Ereignis-DB soll nach 400 Tagen verdichten (E6). Für Lauf-Ereignisse ist
   das richtig. Eine Rohantwort eines Sprachmodells ist der **Beleg** einer
   Messung und darf nie verdichtet werden — in dem Moment, in dem der Parser
   sich ändert, ist sie die einzige Möglichkeit, die Reihe neu abzuleiten.
3. **Kopplung.** Genau die Begründung, mit der E5 (Stichtag statt Migration)
   empfohlen wurde: `spiegelungen` ist ein Arbeitsvermerk und darf nicht an
   einer Tabelle hängen, die auch das Dashboard beschreibt. Hier ist es
   umgekehrt und genauso unerwünscht — eine Forschungsreihe soll nicht an
   einer Tabelle hängen, in die sieben Produktivpfade schreiben.

**Der saubere Berührungspunkt, falls die Ereignis-DB kommt:** *eine* Zeile je
Sammellauf mit `art='sentiment_lauf'` — Anzahl Abfragen, Anzahl Fehler, Dauer.
Genau die Trennung wie bei der Brücke: `spiegelungen` hält den Arbeitsvermerk,
das Ereignis hält „es ist passiert". **Nicht** je Abfrage, und **nie** die
Rohantwort.

*Alternative JSONL* (eine Zeile je Abfrage, append-only): billiger und
schemafrei. **Verworfen**, weil damit der `UNIQUE`-Schutz entfällt — und zwei
gleichzeitig gestartete Cronjobs sind in diesem Projekt kein Gedankenspiel
(rund 730 Prozessstarts am Tag, gebündelt auf volle Minuten).

---

## 3. Zuschnitt, Takt und Kosten (Frage 4)

### 3.1 Je Symbol, je Markt oder je Sektor (S3)

Das ist keine Geschmacksfrage, sondern eine Frage der statistischen Kraft — und
die entscheidet sich in Abschnitt 6.3. Das Ergebnis vorweg:

| Zuschnitt | Aufrufe/Tag | Beobachtungen in 90 Tagen | brauchbar? |
|---|---|---|---|
| je Markt (2) | 2 | 2 Reihen à 90 Punkte | **nein** — erkennt nur sehr grosse Effekte |
| je Sektor (~14) | 14 | 14 Reihen à 90 | grenzwertig, und Sektoren korrelieren stark |
| **je Symbol, gebündelt zu 10** | **~6** | **55 Reihen à 90, quervergleichbar** | **ja** |
| je Symbol, einzeln | 175 | dito, aber tiefer | ja, ~30× teurer |

**Empfehlung: je Symbol, aber gebündelt.** Ein Aufruf fragt nach ~10 Symbolen
und liefert je Symbol einen eigenen Wert.

*Warum je Symbol und nicht je Markt:* Ein Marktwert misst im Wesentlichen die
Stimmung, die alle Symbole gemeinsam haben — und die ist mit dem Marktindex
fast identisch. Je Symbol bekommt man zusätzlich die **Querschnitts-Variation**:
Steigt das Symbol mit dem höchsten Wert am selben Tag stärker als das mit dem
niedrigsten? Diese Frage lässt sich mit weit weniger Tagen beantworten, weil
der gemeinsame Marktfaktor herausfällt. Das ist der eigentliche Grund für die
Empfehlung, und er ist ein rein statistischer.

*Warum gebündelt und nicht einzeln:* Kosten (Abschnitt 3.3). Der Preis der
Bündelung ist geringere Tiefe je Symbol und eine mögliche Reihenfolge-Wirkung
innerhalb des Bündels. **Gegenmassnahme:** die Bündelzusammensetzung wird
einmal festgelegt und eingefroren, nicht bei jedem Lauf neu gewürfelt — sonst
ändert sich der Kontext eines Symbols von Tag zu Tag, und das steckt dann
unbemerkt im Wert. Die Bündel-Id wird mitgeschrieben.

*Alternative „nur Symbole mit offenen Positionen"* — so macht es Agent 3 heute,
aus guten Kostengründen. **Hier verworfen:** die offenen Positionen sind das
Ergebnis der Bot-Regeln, das Universum wäre also von der Strategie ausgewählt.
Damit misst man Sentiment auf einer Stichprobe, die niemand ohne die Strategie
hätte — und vergleicht sie hinterher mit ebendieser Strategie. Für die
tägliche E-Mail ist das egal, für eine Messreihe nicht.

### 3.2 Der Takt der Sammlung (S4)

**Empfehlung: einmal täglich, zu einer festen UTC-Zeit, für beide Märkte.**

*Warum nicht häufiger:* Ein Fünf-Minuten-Takt wäre 288 Läufe am Tag und damit
das ~300-Fache der Kosten. Er wäre aber vor allem **für Stufe 3 nutzlos** —
siehe 3.4.

*Warum nicht seltener:* Wöchentlich gäbe in drei Monaten **13** Beobachtungen
je Symbol. Das ist keine Datenbasis, das ist eine Anekdote.

*Warum eine feste Uhrzeit:* Vergleichbarkeit. Ein Wert von 09:00 und einer von
17:00 stehen an verschiedenen Punkten des Nachrichtentages; wechselnde
Abfragezeiten verrauschen die Reihe, ohne dass es auffällt. **UTC, nicht
Lokalzeit** — sonst springt die Reihe bei der Zeitumstellung um eine Stunde,
und zwar genau einmal mitten im Sammelzeitraum.

*Warum keine Ausrichtung an der Börsensitzung:* Das Projekt hat mit
`notifications/boersenkalender.py` einen echten NYSE-Kalender, und es wäre
verlockend, die Aktien-Abfrage „kurz vor Eröffnung" zu legen. **Empfohlen wird
das nicht**, und der Grund ist ein Prinzip: **der Sammler zeichnet auf, er
richtet nicht aus.** Jede Ausrichtung ist eine Auswertungsentscheidung, und
Auswertungsentscheidungen gehören in Stufe 2, wo man sie ändern kann, ohne die
Reihe zu brechen. Der Sammler schreibt den Zeitstempel; Stufe 2 sucht den
ersten handelbaren Kurs danach. Nebeneffekt: der Sammler hängt an keinem
Kalender und kann deshalb auch nicht an einem scheitern.

**Der Takt der Sammlung ist nicht der Takt des Handelns.** Das ist die
wichtigste Trennung dieses Abschnitts. Täglich sammeln heisst nicht täglich
handeln — aus täglichen Werten lässt sich in Stufe 2 jeder längere Takt
ableiten, umgekehrt nicht. Was nicht gesammelt wurde, ist weg.

### 3.3 Was es kostet

**Zum Preis bei xAI wird hier bewusst keine Zahl genannt** — siehe Abschnitt 9,
sie ist aus der offiziellen Dokumentation zu belegen. Was genannt werden kann,
ist die einzige im Projekt **gemessene** Zahl für einen vergleichbaren Aufruf:
Agent 3 kostet **0,02–0,03 $ je Auslösung inklusive Websuch-Gebühr**
(Übergabeprotokoll 6.3). Die folgende Rechnung benutzt diesen Anker und ist
damit eine **Grössenordnung, keine Preisangabe**.

| Zuschnitt | Aufrufe/Tag | $/Tag | $/Monat | 90 Tage gesamt |
|---|---|---|---|---|
| 175 Symbole einzeln | 175 | 3,50–5,25 | **105–158** | 315–473 |
| 175 Symbole, Bündel zu 10 | 18 | 0,36–0,54 | **11–16** | 32–49 |
| **55 Symbole, Bündel zu 10** | **6** | **0,12–0,18** | **4–5** | **11–16** |
| 2 Märkte | 2 | 0,04–0,06 | 1–2 | 4–5 |

**Zum Vergleich:** die vier bestehenden Agenten kosten zusammen deutlich unter
1 €/Monat (Agent 1: „unter 0,20 €/Monat gesamt"). Selbst die empfohlene Zeile
ist also ein Vielfaches des heutigen KI-Verbrauchs des Projekts — allerdings
ein Vielfaches von fast nichts.

**Empfohlene Zeile: 55 Symbole in 6 Bündelaufrufen, rund 4–5 $ im Monat.**
Zusammensetzung: die 25 Krypto-Paare (dieselben wie die Bots, sie sind ohnehin
das Universum) plus **30 Aktien** statt 150.

*Warum die Aktien gekürzt werden:* 150 Aktien kosten das Fünffache und bringen
weniger als das Fünffache an statistischer Kraft, weil sie sich stark gemeinsam
bewegen — 30 breit gestreute Werte enthalten fast dieselbe Querschnitts-
Information. **Aber die Auswahlregel ist heikel** und deshalb Frage F3 in
Abschnitt 8: Sie muss **vorher** feststehen und darf sich auf **nichts**
stützen, was die Bots erlebt haben. „Die 30, bei denen der Bot gut lief" wäre
genau der Fehler, den dieses Projekt beim Aktien-Universum schon einmal
gemacht hat (Survivorship Bias, Abschnitt 3.3 des Übergabeprotokolls).

**Eingefroren, und zwar wirklich.** Die Krypto-Liste des Projekts wird nach
24-Stunden-Volumen gerankt und ändert sich damit. Für die Sammlung ist das
schädlich: ein Coin, der neu in die Top 25 rutscht, ist dort, **weil** er sich
gerade bewegt hat. Die Sammlung nimmt deshalb einen **Schnappschuss am ersten
Tag**, schreibt dessen Id in jede Zeile und ändert ihn nicht. Fällt ein Symbol
aus dem Handel, wird es als beendet markiert, nicht ersetzt.

### 3.4 Die Handelskosten — und der Widerspruch, der daraus folgt

Das Projekt rechnet einheitlich mit **0,30 % je Rundlauf** (0,1 % Gebühr +
0,05 % Slippage, je einmal für Ein- und Ausstieg — `research/pnl_2025_fixed_size/`).
Was das bei verschiedenen Takten bedeutet, wenn ein Signal jedes Mal vollständig
umschichtet:

| Handelstakt | Rundläufe/Jahr | Kosten/Jahr | muss brutto mehr bringen als |
|---|---|---|---|
| alle 5 Minuten | ~26 000 | 7 800 pp | *sinnlos* |
| täglich | ~250 | **75 pp** | 75 Prozentpunkte |
| wöchentlich | ~52 | 15,6 pp | 15,6 Prozentpunkte |
| zweiwöchentlich | ~26 | 7,8 pp | 7,8 Prozentpunkte |
| monatlich | ~12 | 3,6 pp | 3,6 Prozentpunkte |

(Bei teilweisem Umschichten skaliert es proportional herunter — schichtet ein
tägliches Signal im Schnitt nur 40 % des Bestands um, sind es 30 pp statt 75.)

**Daraus folgt der Widerspruch, der über Stufe 3 entscheidet:**

> Der Takt, in dem Sentiment plausibel Information trägt — Stunden bis wenige
> Tage —, ist genau der Takt, in dem die Handelskosten sie auffressen. Der
> Takt, in dem die Kosten tragbar sind — Wochen bis Monate —, ist genau der
> Takt, in dem von einer Nachrichtenstimmung plausibel nichts mehr übrig ist.

Das ist derselbe Befund, an dem der Kandidat E2 verworfen wurde, nur allgemein
formuliert. Es ist **kein** Argument gegen Stufe 1 — im Gegenteil, es ist das
schärfste Argument dafür, die Sache zu messen statt zu vermuten.

**Vorschlag für den Handelstakt, mit Begründung: er wird jetzt nicht
festgelegt.** Er ist das **Ergebnis** von Stufe 2, nicht ihre Voraussetzung.
Stufe 2 misst die **Abklingkurve** — wie lange ein Wert Vorhersagekraft behält
(Abschnitt 6.2) — und die Antwort fällt in genau eine von drei Klassen:

| Abklingkurve | Handelstakt | Urteil über Stufe 3 |
|---|---|---|
| Wirkung nur am Tag 0–1 | täglich | **kein Stufe 3** — 75 pp sind nicht zu verdienen |
| Wirkung hält 5–20 Tage | wöchentlich bis monatlich | Stufe 3 **denkbar**, wenn der Vorsprung 15,6 pp übersteigt |
| keine messbare Wirkung | — | **kein Stufe 3**, und das ist ein gutes Ergebnis |

Wer heute einen Takt festlegt, legt ihn ohne die einzige Zahl fest, die ihn
bestimmen könnte. **Damit ist der einzige Takt, der jetzt begründbar ist, der
der Sammlung: täglich.**

---

## 4. Was genau gespeichert wird (Frage 2)

Die wichtigste Frage des Entwurfs. Maßstab: **Kann man in drei Monaten mit
diesen Daten allein — ohne Erinnerung, ohne Chatverlauf — den Auswerteplan aus
Abschnitt 6 ausführen?**

### 4.1 Die vier Tabellen

```sql
-- 1) Ein Eintrag je Sammellauf. Damit ist eine Lücke SICHTBAR.
CREATE TABLE IF NOT EXISTS laeufe (
    lauf_id        TEXT PRIMARY KEY,      -- UUID, einmal je Cron-Start
    begonnen_utc   TEXT NOT NULL,
    beendet_utc    TEXT,                  -- NULL = abgebrochen, und das sieht man
    geplant_utc    TEXT NOT NULL,         -- die Soll-Zeit des Takts
    anzahl_geplant INTEGER NOT NULL,
    anzahl_ok      INTEGER NOT NULL DEFAULT 0,
    anzahl_fehler  INTEGER NOT NULL DEFAULT 0,
    sammler_version TEXT NOT NULL
);

-- 2) Eine Zeile je API-Aufruf. Die Rohantwort im Original.
CREATE TABLE IF NOT EXISTS abfragen (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    lauf_id          TEXT NOT NULL REFERENCES laeufe(lauf_id),
    schluessel       TEXT NOT NULL,        -- fachlicher Schluessel, siehe 4.3

    -- Zeit: ZWEI Stempel, und der zweite ist der wichtige
    angefragt_utc    TEXT NOT NULL,        -- unmittelbar vor dem Absenden
    geantwortet_utc  TEXT,                 -- als die Antwort vollstaendig da war
    dauer_ms         INTEGER,

    -- Gegenstand
    markt            TEXT NOT NULL,        -- 'krypto' | 'aktien'
    zuschnitt        TEXT NOT NULL,        -- 'symbol' | 'markt' | 'sektor'
    symbole          TEXT NOT NULL,        -- JSON-Liste, auch bei einem Symbol
    buendel_id       TEXT NOT NULL,        -- eingefrorene Buendelzusammensetzung
    universum_id     TEXT NOT NULL,        -- Schnappschuss-Id, siehe 3.3

    -- Modell: was wir wollten UND was wir bekamen
    anbieter         TEXT NOT NULL,        -- 'xai'
    endpunkt         TEXT NOT NULL,        -- vollstaendige URL, wie benutzt
    modell_angefordert TEXT NOT NULL,
    modell_geliefert   TEXT,               -- was die API zurueckmeldet, siehe 4.5
    websuche         INTEGER NOT NULL,     -- 0/1
    parameter        TEXT,                 -- JSON: temperature, max_tokens, seed ...

    -- Prompt: woertlich, plus Version
    prompt_version   TEXT NOT NULL,        -- 'v1'
    system_prompt    TEXT NOT NULL,        -- woertlich
    user_prompt      TEXT NOT NULL,        -- woertlich

    -- Antwort
    status           TEXT NOT NULL,        -- 'ok'|'fehler'|'ungueltig'|'abgeschnitten'|'kein_schluessel'
    rohantwort       TEXT,                 -- UNVERAENDERT, ungeparst
    stop_grund       TEXT,
    fehler           TEXT,
    tokens_ein       INTEGER,
    tokens_aus       INTEGER,

    UNIQUE(schluessel)
);
CREATE INDEX abfragen_zeit  ON abfragen (geantwortet_utc);
CREATE INDEX abfragen_markt ON abfragen (markt, geantwortet_utc);

-- 3) Abgeleitete Werte. Jederzeit aus (2) neu berechenbar.
CREATE TABLE IF NOT EXISTS werte (
    abfrage_id     INTEGER NOT NULL REFERENCES abfragen(id),
    symbol         TEXT NOT NULL,
    kennzahl       TEXT NOT NULL,          -- 'stimmung' | 'zuversicht' | 'nachrichtendichte'
    wert           REAL,
    parser_version TEXT NOT NULL,
    UNIQUE(abfrage_id, symbol, kennzahl, parser_version)
);

-- 4) Quellenangaben der Websuche.
CREATE TABLE IF NOT EXISTS quellen (
    abfrage_id        INTEGER NOT NULL REFERENCES abfragen(id),
    url               TEXT NOT NULL,
    titel             TEXT,
    veroeffentlicht_utc TEXT,              -- wie gemeldet; oft NULL. Siehe 5.2
    UNIQUE(abfrage_id, url)
);
```

Betriebseinstellungen wie in `docs/KONZEPT_ereignisse_und_anbieter.md` 2.7
empfohlen (`WAL`, `busy_timeout = 10000`, `synchronous = NORMAL`) — hier sogar
unkritischer, weil nur ein Prozess schreibt.

### 4.2 Warum Rohantwort und Wert getrennt sind (S5)

**Das ist „Ein Wert, eine Quelle" auf eine Messreihe angewandt.** Die
Rohantwort ist die Quelle, `werte` ist eine versionierte Ableitung — dieselbe
Beziehung wie zwischen `live_params.py` und allem, was daraus importiert.

*Der Fall, für den das gebaut ist:* Nach sechs Wochen fällt auf, dass der
Parser bei „vorsichtig optimistisch" etwas anderes tut als gedacht. Mit
getrennten Tabellen wird der Parser auf `v2` gehoben, die ganze Reihe neu
abgeleitet, **und beide Fassungen stehen nebeneinander** — man kann zeigen, ob
das Ergebnis am Parser hängt. Ohne Trennung wären sechs Wochen verloren, weil
der ursprüngliche Text nicht mehr da ist.

*Und es ist zugleich die Gegenmassnahme zu K3.* Ein Parserwechsel, der nach
Sichtung der Korrelationen erfolgt, ist Data Snooping. Sichtbar wird das nur,
wenn beide Fassungen nebeneinander stehen und die Version in der Zeile
mitgeführt wird. Deshalb ist `parser_version` Teil des `UNIQUE`.

*Alternative: nur den geparsten Wert speichern.* **Verworfen** — spart ein paar
Megabyte und wirft den einzigen Beleg weg. *Alternative: nur die Rohantwort.*
**Verworfen** — Stufe 2 müsste dann bei jeder Abfrage neu parsen, und der
Parser bekäme keine Version, an der Änderungen auffallen.

### 4.3 Der fachliche Schlüssel

```
<markt>:<zuschnitt>:<geplant_utc>:<buendel_id>
Beispiel:  krypto:symbol:2026-09-20T08:00Z:b03
```

`UNIQUE(schluessel)` überträgt, was alle drei Vorbilder richtig machen
(`spiegelungen`, `gemeldet`, und der Entwurf der Ereignis-DB): **derselbe
Abfragepunkt kann nicht zweimal drinstehen**, auch wenn der Cronjob doppelt
startet. Bezugspunkt ist die **geplante** Zeit, nicht die tatsächliche — sonst
wären zwei Läufe um 08:00:03 und 08:00:07 zwei verschiedene Schlüssel.

**Fehlversuche belegen den Schlüssel nicht.** Das ist die „wichtigste
Einzelerkenntnis" aus der Bestandsaufnahme der drei vorhandenen DBs, und sie
gilt hier genauso: eine gescheiterte Abfrage bekommt ihre Zeile mit
`status='fehler'`, aber `schluessel` = `NULL` — und `UNIQUE` greift in SQLite
bei `NULL` nicht. Ein Wiederholungsversuch ist damit möglich; erst der Erfolg
belegt den Platz. **Das muss im Code kommentiert stehen, sonst wirkt es wie
ein Loch.**

### 4.4 Fehler sind Zeilen, keine Lücken (S6)

**Die härteste Regel des Entwurfs**, und die einzige, die direkt aus einem
bestehenden Schaden dieses Projekts folgt.

1. **Jeder Fehlversuch bekommt eine Zeile.** Zeitüberschreitung, HTTP 500,
   abgeschnittene Antwort, unparsbare Antwort, Kontingent erschöpft — alles
   mit eigenem `status`. Nie ein stilles `return`.
2. **Ein fehlender Schlüssel ist ein lauter Fehler.** Die vier Agenten geben
   bei fehlendem `ANTHROPIC_API_KEY` `""` zurück, und das ist dort richtig.
   Hier wäre es der Weg, auf dem die Sammlung monatelang schweigend nichts
   tut. Der Sammler schreibt stattdessen eine Zeile mit
   `status='kein_schluessel'`, beendet sich mit Rückgabewert **ungleich 0**
   und meldet über `notifications/notify.py`. *(Zur Abwägung des
   Rückgabewerts: die Notbremse der Brücke gibt bewusst **0** zurück, weil
   eine gezogene Bremse eine befolgte Anweisung ist. Hier ist es umgekehrt —
   ein fehlender Schlüssel ist keine Anweisung, sondern ein Ausfall, und
   genau der soll auffallen.)*
3. **Ein ausgefallener Lauf ist sichtbar**, weil `laeufe` eine Zeile je
   geplantem Lauf führt. Fehlt sie ganz, lief der Cronjob nicht — und das ist
   die Lage, die offener Punkt 12 des Übergabeprotokolls für die Bots
   beschreibt. Für die Sammelschicht wird sie hier gelöst, weil es hier
   billig ist: es gibt keine Regel „fasse `forward_test.py` nicht an", die
   dem im Weg stünde.
4. **Der Mac schläft.** Cron holt nichts nach — am 11.09.2026 schlief er
   drei Stunden. Ein verschlafener Tag ist für diese Reihe ein fehlender
   Datenpunkt, und `laeufe` macht ihn sichtbar statt unsichtbar. **Mehr kann
   kein Code hier tun**; die Sammlung erbt diese Randbedingung vollständig.
5. **Und das Ausfallverhalten in die andere Richtung:** Der Sammler darf
   nichts anfassen, was ein Bot braucht. Er öffnet keine Bot-Datenbank, er
   importiert nichts aus `strategies/`, er schreibt ausschliesslich in seine
   eigene Datei. Fällt er komplett aus, merken die neun Bots davon nichts.

### 4.5 Der Modell-Zeitstempel — warum zwei Spalten

Die Aufgabe nennt den Punkt zu Recht: Ändert der Anbieter das Modell, sind die
Werte davor und danach nicht mehr vergleichbar. Der Entwurf geht einen Schritt
weiter und führt **zwei** Spalten.

`modell_angefordert` ist, was im Code steht. Das kann ein Alias sein. Ein Alias
zeigt per Definition irgendwann woandershin, und zwar ohne Ankündigung — genau
der Vorgang, den der Nutzer erkennen will. `modell_geliefert` ist, was die API
zurückmeldet.

> **Zu prüfen (Abschnitt 9):** ob die xAI-API im Antwortobjekt eine
> **aufgelöste** Modellkennung zurückgibt und ob diese fein genug ist, um eine
> Modellrevision zu unterscheiden. Falls nicht, ist der Alias-Weg nicht
> absicherbar — dann muss im Code eine **feste, versionierte Modellkennung**
> stehen, und ein Wechsel ist ein bewusster Schritt mit einer Markierung in der
> Reihe. Das ist die sicherere Bauweise und wird unabhängig vom Prüfergebnis
> empfohlen.

Dasselbe gilt für den Prompt: `prompt_version` **und** der wörtliche Text. Die
Version, damit man filtern kann; der Text, damit man weiss, was die Version
bedeutete. Ein Prompt-Wechsel ist für die Vergleichbarkeit genauso
folgenschwer wie ein Modellwechsel — und weit leichter versehentlich zu
machen.

### 4.6 Reicht das für Stufe 2?

Gegenprobe, Feld für Feld gegen den Plan aus Abschnitt 6:

| Stufe 2 braucht | steht in | vorhanden |
|---|---|---|
| Wert je Symbol und Tag | `werte` | ja |
| Kausaler Schnitt (K2) | `abfragen.geantwortet_utc` | ja |
| Vergleichbarkeit über Zeit | `modell_geliefert`, `prompt_version`, `parser_version` | ja |
| Lücken von Nullwerten trennen | `laeufe`, `abfragen.status` | ja |
| Auswahleffekte ausschliessen | `universum_id`, `buendel_id` | ja |
| Neuableitung bei Parserwechsel | `rohantwort` | ja |
| Kontrolle gegen Momentum | Kursdaten aus `data/` | ja, extern |
| Meldungszeitpunkt | `quellen.veroeffentlicht_utc` | **nur teilweise**, siehe 5.2 |

Die letzte Zeile ist die einzige Lücke, und sie ist **nicht schliessbar** —
Abschnitt 5.2 erklärt, warum das folgenlos ist.

---

## 5. Look-Ahead im Einzelnen (Frage 3)

### 5.1 Die fünf Kanäle

| # | Kanal | Gefahr | Abwehr |
|---|---|---|---|
| L1 | Trainingsstand des Modells | Bei rückwirkender Befragung kennt das Modell den Ausgang | **entfällt** bei Vorwärtssammlung — und ist zugleich der Grund, warum nicht nachgeholt werden kann |
| L2 | Websuche liest die Kursreaktion mit | Der Wert enthält, was seit der Meldung passiert ist | **unvermeidbar** — deshalb gilt der Wert für `geantwortet_utc`, nie für den Meldungszeitpunkt (5.2) |
| L3 | Renditefenster falsch angesetzt | Einstiegskurs von vor oder während der Abfrage | K2: erster handelbarer Kurs **streng nach** `geantwortet_utc`; mechanisch prüfbar (5.3) |
| L4 | Kursinformation im Prompt | „Sentiment" ist in Wahrheit Momentum | Prompt enthält **keine** Kursdaten; wörtlich mitgeschrieben und prüfbar; Kontrolle in 6.2 |
| L5 | Parser/Kennzahl nach Sichtung gewählt | Data Snooping, sieht aus wie ein Fund | S8: Plan und Parser vor dem ersten Datensatz; `parser_version` in jeder Zeile |

**L1 ist der Kanal, der den Elliott-Wave-Fall ausmachte** — ein Pivot ist erst
ein Pivot, wenn der Kurs sich danach bewegt hat, und der Backtest stieg
trotzdem zum Pivot ein. Der Schaden lag zwei Jahre unbemerkt im Code. Hier
existiert dieser Kanal nicht, weil es keinen Rückblick gibt.

*(Zur Zahl aus der Aufgabe, der Genauigkeit halber: die abgelegte
Ergebniskurve von `elliott_wave_stocks` trug **+1500,53 %** und steht nach
Neuberechnung bei **+352,72 %**. Der Rückgang hat allerdings **zwei**
Ursachen, nicht eine: den Look-Ahead **und** einen Parameterwechsel vom
03.09.2026, nach dem die Kurve nie neu erzeugt wurde. Den Look-Ahead allein
beziffert `research/elliott_wave_lookahead/` anders — für den Krypto-Bot
+2184,96 % → −24,44 %, für den Aktien-Bot +3084,09 % → +338,26 %. Am Gewicht
des Beispiels ändert das nichts; es macht es eher grösser.)*

**L5 ist der Kanal, der hier wirklich droht**, und er ist der einzige, gegen
den kein Code hilft.

### 5.2 Warum der Meldungszeitstempel mitläuft, aber nichts entscheidet

Die Aufgabe verlangt, den Zeitstempel der ausgewerteten Meldung zu speichern.
Der Entwurf tut das (`quellen.veroeffentlicht_utc`) — und muss zugleich sagen,
dass er für die Auswertung **nicht brauchbar** ist. Drei Gründe:

1. **Er ist oft nicht da.** Websuch-Ergebnisse liefern Veröffentlichungsdaten
   unvollständig und uneinheitlich; viele Seiten nennen nur ein Datum ohne
   Uhrzeit, manche das Datum der letzten Änderung.
2. **Er ist nicht der Zeitpunkt, zu dem der Wert entstand.** Fasst eine
   Antwort fünf Meldungen aus drei Tagen zusammen, gibt es keinen einen
   Meldungszeitpunkt.
3. **Und selbst wenn beides stimmte, hilft er nicht** — das ist L2. Eine
   Antwort, die eine Meldung von vorgestern bewertet, hat die Kursreaktion von
   gestern gesehen. Ein Renditefenster ab dem Meldungszeitpunkt würde also
   messen, wie gut ein Modell Vergangenheit beschreibt.

**Wofür er trotzdem gut ist:** als Diagnose. Ist ein Wert überwiegend aus
Meldungen entstanden, die drei Tage alt sind, misst die Reihe eher träge
Nachrichtenlage als frische Stimmung — und das ist etwas, das man wissen will,
bevor man einen Handelstakt wählt. Er gehört also in die Daten, aber nie in
die Formel.

### 5.3 Die mechanische Prüfung

Projekt-Prinzip 10 verlangt es so: „für jeden Trade belegen, dass der
Einstiegszeitpunkt **nach** dem Zeitpunkt liegt, zu dem das Signal überhaupt
bekannt sein konnte". Hier ist das eine Zeile:

```
für jede Beobachtung:  zeitstempel(einstiegskurs) > abfragen.geantwortet_utc
Anzahl Verletzungen muss 0 sein — und die Zahl wird berichtet, nicht nur geprüft.
```

Und, weil Prinzip 12 es verlangt (eine grüne Prüfung ist erst etwas wert, wenn
belegt ist, dass sie rot werden kann): **die Gegenprobe gehört dazu.** Die
Prüfung wird einmal gegen `angefragt_utc` statt `geantwortet_utc` laufen
gelassen und muss dann bei jedem Aufruf mit nennenswerter Dauer anschlagen.
Tut sie es nicht, misst sie nichts.

### 5.4 Der Rest-Look-Ahead, den niemand wegbauen kann

Wird Stufe 2 **mehrfach** gerechnet, während die Daten wachsen, und hängt die
Entscheidung „weitersammeln oder abbrechen" an den Zwischenständen, dann fliesst
Wissen über die Daten in die Auswahl des Zeitpunkts ein. Es ist kein
Look-Ahead, aber dieselbe Familie, und es macht jeden p-Wert bedeutungslos.

**Gegenmittel, und es ist unbequem:** Der Auswertezeitpunkt wird vorher
festgelegt und eingehalten. Zwischenstände sind erlaubt, aber ausschliesslich
zur **Betriebsprüfung** — laufen die Abfragen, gibt es Fehlerhäufungen, ist die
Reihe vollständig. **Nicht** zur Frage, ob etwas korreliert.

---

## 6. Der Auswerteplan, festzulegen vor dem ersten Datensatz (S8)

Dieser Abschnitt ist die Antwort auf „reicht es für Stufe 2?". Er gehört als
`sentiment/auswertung_plan.md` in den Ordner und wird **vor** dem ersten Lauf
festgeschrieben.

### 6.1 Die eine Haupthypothese

> **H1:** Symbole mit dem höchsten Stimmungswert eines Tages erzielen über die
> folgenden **fünf Handelstage** eine höhere Rendite als Symbole mit dem
> niedrigsten — gemessen im Querschnitt innerhalb desselben Marktes, jeweils ab
> dem ersten handelbaren Kurs nach `geantwortet_utc`.

Eine Hypothese, ein Horizont, vorab benannt. Alles andere ist **erkundend** und
wird als solches beschriftet. Das ist die Gegenmassnahme gegen L5: bei 55
Symbolen, drei Kennzahlen und vier Horizonten findet man immer irgendwo etwas.

*Warum fünf Tage und nicht einer:* bei einem Tag stünde H1 von vornherein im
75-pp-Bereich aus 3.4 und wäre auch bei klarem Befund wirtschaftlich tot.
Fünf Tage liegen im Bereich, in dem ein Befund handelbar **sein könnte**.

### 6.2 Was daneben gemessen wird

| Messung | Warum |
|---|---|
| **Abklingkurve** über 1, 2, 5, 10, 20 Tage | Bestimmt den Handelstakt — die Zahl, die Stufe 3 entscheidet (3.4) |
| **Kontrolle gegen Momentum** | Sentiment entsteht aus Nachrichten, die Kursbewegungen berichten. Trägt der Wert über die Vorlaufrendite **hinaus** etwas bei? Wenn nein, ist es Momentum mit API-Rechnung. Umsetzung: Doppelsortierung oder partielle Korrelation gegen die Rendite der letzten 5 Tage |
| **Umschlagshäufigkeit** des Signals | Ohne sie ist die Kostenrechnung aus 3.4 nicht anwendbar |
| **Anteil der Rückfalltage** (`status != 'ok'`) | Über ~10 % ist die Reihe für eine Handelsentscheidung untauglich, egal was sie zeigt |
| **Negativkontrolle:** dieselbe Auswertung mit zeitlich verwürfelten Werten | Prinzip 12. Zeigt sie etwas, misst der Aufbau etwas anderes als gemeint |
| **Kausalitätsprüfung** aus 5.3 | Muss 0 Verletzungen melden, mit Gegenprobe |

### 6.3 Wie viele Beobachtungen nötig sind — und warum drei Monate knapp sind

Standardrechnung für eine Korrelation, 80 % Teststärke, α = 0,05 zweiseitig:

| zu erkennende Korrelation | nötige unabhängige Beobachtungen |
|---|---|
| r = 0,30 (sehr gross) | ~85 |
| r = 0,20 (gross) | ~194 |
| r = 0,15 | ~347 |
| r = 0,10 (realistisch für so ein Signal) | **~783** |

Was die Sammlung liefert:

* **Bei Marktzuschnitt:** 90 Tage = **90** Beobachtungen je Markt. Damit ist
  nur r ≥ 0,30 erkennbar — ein Effekt dieser Grösse wäre für ein
  Nachrichtensignal aussergewöhnlich. **Dieser Zuschnitt ist damit praktisch
  wertlos**, und das ist der eigentliche Grund für S3.
* **Bei Symbolzuschnitt:** 55 Symbole × 90 Tage = 4950 Zeilen — aber sie sind
  **nicht** unabhängig, Kryptos und Aktien bewegen sich jeweils stark
  gemeinsam. Die wirksame Zahl liegt näher an *Tage × Anzahl unabhängiger
  Faktoren*. Bei grob geschätzt 2–3 Faktoren im Krypto- und 5–8 im
  Aktienuniversum landet man bei einer **Grössenordnung von 600–900** — also
  gerade eben im Bereich, in dem r = 0,10 erkennbar wäre.

**Das ist eine Grössenordnungsabschätzung, keine exakte Rechnung.** Die Zahl
der wirksamen Faktoren lässt sich aus den vorhandenen Kursdaten vorab
bestimmen und sollte es auch — **vor** dem Start, weil sie die Universumsgrösse
mitbestimmt. Das ist der einzige Teil des Auswerteplans, der Rechenarbeit
verlangt, und er kostet nichts ausser Zeit.

**Was daraus folgt, offen gesagt:** Drei Monate liefern ein Ergebnis mit
breitem Unsicherheitsband. Die ehrliche Erwartung ist nicht „ja" oder „nein",
sondern **„noch kein Urteil, weitersammeln"** — und die Grössenordnung für ein
belastbares Urteil ist eher **ein Jahr**. Das ist kein Argument gegen den Start;
es ist eines dafür, **jetzt** zu starten und die Erwartung an den 3-Monats-Punkt
tief zu hängen. Es ist auch dieselbe Lage wie bei den Bots: kein Bot erreicht
bisher `MIN_LIVE_CLOSED_TRADES = 10`, und die Prüftermine liegen deshalb im
Oktober 2026 und Januar 2027.

### 6.4 Die Abbruchkriterien — vorher festzulegen

Stufe 2 darf **nicht** mit „interessant, mal weitersehen" enden. Vorab:

| Befund | Entscheidung |
|---|---|
| Rückfallanteil > 10 % **oder** Kausalitätsverletzungen > 0 | Reihe ungültig, Ursache beheben, neu beginnen |
| H1 nicht signifikant **und** Abklingkurve flach | **Kein Stufe 3.** Sammlung beenden oder bewusst verlängern |
| H1 signifikant, aber verschwindet gegen Momentum | **Kein Stufe 3** — das Signal ist Momentum |
| H1 signifikant, Vorsprung unter den Kosten aus 3.4 | **Kein Stufe 3** — richtig, aber nicht handelbar |
| H1 signifikant, Vorsprung über den Kosten | Stufe 3 **prüfen** — mit Walk-Forward, Equity-Simulation und Buy-and-Hold-Vergleich, wie jede andere Strategie |

Die letzte Zeile ist wichtig: ein positiver Befund in Stufe 2 wäre **kein**
freigegebener Bot, sondern der Beginn der normalen Validierungskette aus
Abschnitt 7 des Übergabeprotokolls.

---

## 7. Die Sicherheitsgrenzen (Frage 5)

### 7.1 In Stufe 1

| Regel | Wie sie strukturell gesichert ist |
|---|---|
| Kein Trade, keine Parameteränderung | Der Sammler kennt `strategies/` nicht — kein Import, keine Bot-DB, auch nicht lesend. Prüfbar per AST-Selbsttest |
| Keine Anzeige im Notfallweg | Nichts im Dashboard, schon gar nicht auf der Übersichtsseite. Falls je eine Anzeige gewünscht wird: eigene Seite, wie die Portfolio-Sicht aus PR #80 |
| Keine Rückwirkung auf Bots | Eigene Datei, eigener Prozess, eigener Cronjob. Fällt er aus, merken die neun Bots nichts |
| Kein Schlüssel im Repo | `XAI_API_KEY` aus der `.env`; die steht in `.gitignore`. Nie protokolliert, nie in die DB, nie in eine Fehlermeldung |
| **Keine Portfoliodaten nach draussen** | Siehe unten |

**Die Regel, die leicht übersehen wird: der Prompt enthält nie Portfoliozustand.**
Keine offenen Positionen, keine Stückzahlen, kein PnL, keine Kontogrösse. Zwei
Gründe, und beide tragen allein:

1. **Datenschutz.** Der Prompt geht an einen Dritten. Was dort steht, hat
   dieser Dritte. Symbolnamen plus eine allgemeine Frage sind unbedenklich;
   „meine offenen Positionen sind …" ist die Offenlegung des Portfolios.
2. **Messhygiene.** Hinge der Wert vom Portfolio ab, wäre er zwischen zwei
   Tagen nicht mehr vergleichbar, und in Stufe 3 entstünde eine Rückkopplung:
   die Position beeinflusst das Signal, das die Position beeinflusst.

**Zur `.env` und dem, was daran hängt (O2 / offener Punkt 17):** Die `.env` ist
nicht versioniert. Für das Dashboard ist das bereits ein offener Punkt — geht
sie verloren, lauscht der Dienst auf `127.0.0.1` und meldet nichts. Für die
Sammelschicht wäre der Schaden derselbe, nur leiser: kein Schlüssel, keine
Abfragen, keine Meldung, monatelang. **Dieser Entwurf löst das nicht** — er
fügt nur einen zweiten Nutzer desselben Arguments hinzu und zieht die
Konsequenz, die im eigenen Zuständigkeitsbereich liegt: Punkt 2 in 4.4, ein
fehlender Schlüssel ist ein lauter Fehler. Der Entwurf hält aber fest: wenn die
Namen der benötigten `.env`-Schlüssel je versioniert festgehalten werden (einer
der beiden Wege in Punkt 17), gehört `XAI_API_KEY` dazu.

### 7.2 Wie die Absicherung in Stufe 3 aussähe (S7)

Verlangt ist der Entwurf, nicht der Bau. Grundsatz: **„Ein ungültiges oder
unerwartetes Modellergebnis darf nie zu einer Handlung führen."** Die Umsetzung
ist weniger offensichtlich, als sie klingt.

**Der Fehler, der naheliegt:** „Kein Wert → keine Position" oder „kein Wert →
alles glattstellen". Beides ist **falsch**, denn beides ist selbst eine
Handlung. Ein Ausfall beim Anbieter würde dann das Portfolio umbauen — ein
Modellfehler hätte eine Wirkung, und zwar eine grosse.

**Die richtige Fassung:**

> Ein fehlender, veralteter oder ungültiger Sentiment-Wert führt dazu, dass
> der Bot sich **genau so verhält wie ohne die Sentiment-Erweiterung** — also
> wie die validierte Grundstrategie. Nicht „Position zu", nicht „Position auf".
> Der Zustand ohne Signal ist der Zustand vor dem Signal.

Daraus vier Prüfungen, jede muss bestanden sein, bevor der Wert überhaupt
angesehen wird:

| Prüfung | Wenn sie scheitert |
|---|---|
| **Vorhanden und geparst** — `status='ok'`, Wert im erwarteten Bereich | Rückfall auf Grundstrategie |
| **Frisch** — nicht älter als eine fest verdrahtete Höchstdauer | Rückfall. Ein Wert von vorgestern ist kein Wert (die Bots kennen das als `SIGNAL_FRESHNESS_DAYS`) |
| **Vom validierten Modell** — `modell_geliefert` = die in Stufe 2 geprüfte Kennung | Rückfall, **dauerhaft**, bis Stufe 2 neu gerechnet ist |
| **Vom validierten Prompt und Parser** — Versionen stimmen überein | dito |

**Die dritte Zeile ist der stärkste Einzelmechanismus des ganzen Entwurfs.**
Wechselt der Anbieter das Modell, schaltet sich das Signal **von selbst ab**,
statt mit einer unvergleichbaren Zahl weiterzuhandeln. Genau das ist der
Schaden, den die Aufgabe unter „Warum der Modell-Zeitstempel zählt" beschreibt
— und er ist hier nicht nur erkennbar, sondern folgenlos gemacht.

Und zwei Grenzen, die auch in Stufe 3 gelten müssten:

* **Sentiment darf nur wegnehmen, nie hinzufügen.** Es kann einen Trade
  verhindern, den die Grundstrategie vorschlägt — es kann keinen erzeugen.
  Dann ist die Obergrenze des Schadens die entgangene Rendite der
  Grundstrategie, und die ist messbar. Das ist dieselbe Vorsicht, mit der
  Agent 3 seit jeher **nicht** als News-Veto gebaut wurde: „so ein
  News-Veto wäre ein eigenständiges Feature, das erst separat backgetestet und
  validiert werden müsste".
* **Der Anteil der Rückfalltage wird laufend gezählt und angezeigt.** Ein Bot,
  der an 40 % der Tage auf die Grundstrategie zurückfällt, ist nicht der Bot,
  der validiert wurde. Ohne diese Zahl merkt das niemand — derselbe Fehler wie
  bei `state.json` und bei den Datenlücken.

---

## 8. Die vier Fragen, die dieser Entwurf nicht beantworten kann

Nicht ausgefüllt, sondern als Fragen stehen gelassen.

**F1 — Wird Stufe 1 begonnen, und für welchen Zeitraum wird sie zugesagt?**
Abschnitt 6.3 sagt: drei Monate liefern wahrscheinlich kein Urteil, ein Jahr
eher. Eine Sammlung, die nach drei Monaten mit „unklar" abgebrochen wird, war
drei Monate umsonst — dieselbe Falle, die der Auftrag für die Datenqualität
benennt, eine Ebene höher. **Die Zusage der Dauer ist Teil der Entscheidung,
nicht ihre Folge.**

**F2 — Welcher Monatsbetrag ist vertretbar?** Der Entwurf empfiehlt die Zeile
mit rund 4–5 $/Monat (Grössenordnung, siehe 3.3). Das ist ein Vielfaches des
heutigen KI-Verbrauchs des Projekts und trotzdem wenig Geld. Die Wahl zwischen
4–5 $, 11–16 $ (volles Aktienuniversum) und 105–158 $ (je Symbol einzeln) ist
eine Abwägung zwischen Geld und statistischer Kraft, und sie gehört dem Nutzer.

**F3 — Nach welcher Regel wird das Aktienuniversum auf 30 eingefroren?** Die
Regel muss vorher feststehen und darf sich auf nichts stützen, was die Bots
erlebt haben. Denkbar: die 30 grössten nach Marktkapitalisierung am Starttag ·
je Sektor die grössten drei (streut breiter, ist aber eine zweite Entscheidung)
· eine Zufallsauswahl aus den 150 mit festgehaltenem Startwert (am saubersten,
am schwersten zu erklären). **Empfehlung nur der Form nach: eine Regel, am
Starttag angewandt, mit Schnappschuss festgehalten, danach nie wieder
angefasst.**

**F4 — Wer belegt die xAI-Angaben?** Siehe Abschnitt 9. Solange sie
unbelegt sind, ist der Entwurf nicht baureif.

---

## 9. Was aus der offiziellen Dokumentation zu belegen ist

**Nichts davon wurde geprüft** — es wurde kein Aufruf gemacht und nichts aus
dem Gedächtnis festgelegt. Jede Zeile ist vor dem Bau aus der offiziellen
Anbieterdokumentation zu belegen.

| # | Zu belegen | Warum es sonst schiefgeht |
|---|---|---|
| **P1** | **Die API-Adresse.** In einer vorliegenden Vorlage steht `https://api.xai.com/v1`. Geläufiger ist `https://api.x.ai/v1` — **beides ist hier unbelegt** | Eine falsche Adresse erzeugt Code, der stillschweigend gegen nichts läuft. Zusammen mit „Fehler geben leeren Text zurück" ergibt das eine Sammlung, die monatelang leer bleibt, ohne dass es auffällt. Genau deshalb Punkt 2 in 4.4 |
| **P2** | **Die genauen Modellkennungen** und ob es Aliase gibt | 4.5 — ein Alias, der unbemerkt umzieht, bricht die Reihe genau in der Mitte |
| **P3** | **Ob die Antwort eine aufgelöste Modellkennung zurückmeldet** | 4.5 — davon hängt ab, ob `modell_geliefert` überhaupt füllbar ist |
| **P4** | **Ob es eine server-seitige Websuche gibt**, wie sie aktiviert wird, und ob sie **Quellenangaben mit Datum** liefert | Ohne Websuche misst man den Trainingsstand des Modells, nicht die aktuelle Lage — dann ist das ganze Vorhaben hinfällig. Ohne Quellen fällt Tabelle 4 weg |
| **P5** | **Die Preise** je Token und je Websuche | Abschnitt 3.3 rechnet mit dem **Anthropic**-Anker aus dem eigenen Projekt, weil es der einzige gemessene ist. Das ist eine Grössenordnung, keine Preisangabe |
| **P6** | **Ob strukturierte Ausgabe** (JSON-Schema) unterstützt wird | Entscheidet, wie robust der Parser sein muss — und wie oft `status='ungueltig'` auftritt |
| **P7** | **Ob Determinismus** (`seed`, `temperature=0`) unterstützt wird und was er bei aktiver Websuche noch bedeutet | Ohne ihn schwankt die Reihe zusätzlich; mit ihm ist die Schwankung wenigstens benennbar |
| **P8** | **Nutzungsbedingungen** zur Speicherung von Antworten und Suchergebnissen | Der Entwurf speichert Rohantworten über Monate. Ob das zulässig ist, ist eine Rechtsfrage, keine Architekturfrage |

---

## 10. Was dieser Entwurf ausdrücklich nicht kann (Frage 6)

1. **Er sagt nicht, ob Sentiment-Handel trägt.** Das ist eine Frage der
   Literatur und der Empirie, keine der Architektur. Dieser Entwurf baut das
   Messgerät und sagt, was es messen kann — nicht, was herauskommt.
2. **Er sagt nicht, ob Grok für diese Aufgabe taugt.** Weder Qualität noch
   Verfügbarkeit noch Stabilität der Modelle wurden geprüft; es wurde kein
   Aufruf gemacht.
3. **Er belegt keine einzige xAI-Angabe.** Abschnitt 9, P1–P8. Der Entwurf ist
   bis dahin nicht baureif.
4. **Er kann Frage (B) aus Abschnitt 0 nicht beantworten** — „sagt eine
   Nachricht vom Zeitpunkt p die Rendite nach p voraus?". Diese Frage bleibt
   mit diesen Daten unbeantwortbar, dauerhaft und unabhängig von der
   Sammeldauer.
5. **Er kann die statistische Kraft nicht herbeischaffen.** 6.3 ist eine
   Grössenordnungsabschätzung; die Zahl der wirksamen Faktoren ist vorab aus
   den Kursdaten zu bestimmen. Die ehrliche Erwartung nach drei Monaten ist
   „noch kein Urteil".
6. **Er kann den schlafenden Mac nicht wecken.** Cron holt nichts nach. Die
   Sammlung erbt diese Randbedingung vollständig; sie kann Lücken nur sichtbar
   machen (`laeufe`), nicht verhindern.
7. **Er kann L5 nicht technisch verhindern.** Data Snooping im Parser und in
   der Auswertung ist eine Frage der Disziplin. `parser_version` macht es
   sichtbar; unterlassen muss man es selbst.
8. **Er enthält keinen Code, keine Tests und keine Datenbank.** Der Diff dieses
   Auftrags enthält ausschliesslich neue Dateien unter `docs/`.

---

## 11. Wenn entschieden wird: die Reihenfolge

Kein Auftrag, sondern die Ableitung aus den Abhängigkeiten. Die Schritte 1–3
sind vor jedem Zeileschreiben fällig.

| # | Schritt | hängt ab von |
|---|---|---|
| 1 | P1–P8 aus der Anbieterdokumentation belegen | — |
| 2 | F1–F3 entscheiden (Dauer, Budget, Universumsregel) | 1 (für F2) |
| 3 | Auswerteplan (Abschnitt 6) festschreiben, inkl. Vorab-Bestimmung der wirksamen Faktoren aus vorhandenen Kursdaten | 2 |
| 4 | Universum einfrieren, Schnappschuss und Bündel festhalten | 2, 3 |
| 5 | Prompt `v1` und Parser `v1` festlegen — **bevor** eine echte Antwort gesehen wurde | 3 |
| 6 | Schema anlegen, Sammler bauen, Selbsttests gegen Attrappen (ohne Netz) | 4, 5 |
| 7 | Einen Tag im Trockenlauf: schreibt er Zeilen? Werden Fehler zu Zeilen? Greift `UNIQUE` bei Doppelstart? | 6 |
| 8 | Cronjob eintragen, Sammlung beginnen | 7 |
| 9 | Nur Betriebsprüfung, keine Korrelationen ansehen (5.4) | 8 |
| 10 | Zum vorher festgelegten Termin: Stufe 2 nach Plan | 3, 9 |

Schritt 5 ist der, der am ehesten übersprungen wird, und der, dessen
Überspringen am teuersten ist.
