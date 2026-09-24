# TB-97 — Testannahmen, zweite Runde: `F4`, die vier Literale, Gegenproben für alle acht Mutationsproben — und die Sonde liest ihre Gruppen aus dem Abbild

**Sitzungstitel:** `TB-97` · **Angelegt:** 24.09.2026 vom steuernden Chat
**Grundlage:** `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`, Abschnitte 5–7
**Register:** 40.7 und 40.8 (a)–(e) · **Vorgänger:** TB-96 (`4777d18`) · **Aufwand:** hoch

⚠️⚠️ **Dieser Auftrag muss VOR TB-98 laufen.** Fable: *„Teil D bricht mit
`KeyError`, sobald der Bot Zweijahresfalten bekommt — und ob er das bekommt,
weiss heute niemand. Also vor der Ableitung umstellen, nicht danach."*

---

## ⭐⭐ Worum es geht

Fünf Sachen, alle derselben Klasse: **Eine Wache, die ein Literal enthält, ist
so alt wie ihr Literal.**

| | |
|---|---|
| (a) | `F4` prüft mit `<=`, wo sein Text „unter" sagt — **und hat nie gebissen** |
| (b) | Vier weitere Jahresliterale, heute grün, **nur weil ihr Bot Einjahresfalten hat** |
| (c) | Von den acht Mutationsproben aus Abschnitt 12 hat **niemand je gezeigt**, dass sie rot werden können |
| (d) | Die Sonde trägt die Gruppe „bestimmt" **fest verdrahtet im Code** — ein Literal in einer Wache |
| (e) | Ihre Schlusszeilen mischen Pfad- und Regel-Bestandteile |

⭐ Fables Regel dazu, zeichengleich: *„Eine Mutationsprobe ohne Gegenprobe zählt
nicht als Prüfung."*

---

## ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔ | **Keine Prüfung löschen, keine abschwächen, keine Ausnahme für einen Bot, keine Toleranz** |
| ⛔ | **Der Faltenplan wird nicht geändert** — nicht `faltenplan.py`, nicht `faltenplan.json`. Der Test folgt dem Register, nie umgekehrt |
| ⛔ | **`auswertung.py`, `registerdaten.py`, `benchmark.py`, `registerbericht.py` nicht anfassen** (Sperrlistenpunkte 3/4/5/6/14) |
| ⛔ | **Keine Trade-Liste neu erzeugen, keine Faltenlänge ableiten** (⇒ TB-98) |
| ⛔ | ⚠️⚠️ **Kein neues echtes Abbild.** Die Gegenprobe zur Sonde braucht ein **Kopie**-Abbild im Scratchpad mit erfundenem Pfad — **nie** ein neues `sperrliste_abbild_*.json` in `ergebnisse/` |
| ⛔ | **Kein Registerabschnitt geschrieben.** Der Eintrag ist der nächste Schritt und braucht Fables Kenntnisnahme |

⚠️⚠️ **Eine Wache, die dieser Auftrag einhalten muss:** Seit TB-95 liest `G6`
den Registertext **5.1 Nr. 4** mit einem am Zeilenanfang verankerten Muster.
TB-96 hat gemessen: **Auch eine zweite Zeile mit demselben Anfang macht `G6`
rot.** ⇒ Schreibe in keinem Kommentar, keiner Meldung und keinem Beleg eine
Zeile, die mit `4. **<Jahr> und <Jahr> sind Testfalten, keine Trainingsjahre.**`
**beginnt**. Die Marke bei 5.1 Nr. 4 sagt es; halte sie ein.

---

## 0. Schritt 0

Arbeitsbaum committen (der steuernde Chat legt diesen Auftrag, die Anfrage 24b,
den Zeiger und eine Berichtigung in `starte_sitzung.sh` ab). `find .git -name
'*.lock'` → keine. Danach leer. HEAD am Eingang: **`4777d18`**.
⚠️ **Fehlt Abschnitt 40 im Register, brich ab.**

---

## Block A — Erst benennen, dann prüfen

⭐⭐ **Fables Regel aus 40.7 verlangt Gegenproben für „alle acht
Mutationsproben". TB-96 hat gemessen: Abschnitt 12 nennt die Zahl, aber
KEINE NAMEN.** Wer nicht weiss, welche acht gemeint sind, kann die Regel nicht
erfüllen.

**A1 — Die acht benennen.** Durchsuche `test_vorregistrierung.py` nach allen
Proben, die den Code **verändern** und prüfen, dass sich das Ergebnis ändert
(Muster: Kopie anlegen, `_ersetze(...)`, erneut auswerten, Ergebnisse
vergleichen). Für jede: Prüfungsname, Teil, Zeile, **was mutiert wird**, und
**woran** der Unterschied gemessen wird.

| | |
|---|---|
| ⭐ | Sind es **genau acht**? Mehr oder weniger ist ein **Befund** und gehört gemeldet, nicht zurechtgezählt |
| ⭐ | Stimmen sie mit dem überein, was Abschnitt 12 beschreibt? Lies die Stelle |

Beleg: `a1_mutationsproben.txt`.

**A2 — Für jede der acht messen, ob sie heute beissen kann.** ⚠️ **Nicht raten
— laufen lassen:** Mutation weglassen (oder die Menge leeren, wie bei `H3`) und
prüfen, ob die Probe **scheitert**. Ergebnis je Probe: **beisst / beisst nicht /
nicht messbar**.

⭐ *Das ist der Kern des Auftrags. `F4` ist der bekannte Fall; ob es der einzige
ist, weiss heute niemand.*

Beleg: `a2_beissen_vorher.txt`.

**A3 — `F4` genau ausmessen.** Was prüft es, mit welchem Vergleichszeichen, und
was sagt sein Text? Wie viele Falten setzt es auf null? Rechne wie TB-95: Ab
welchem k verschiebt sich der Median bei der heutigen Faltenzahl?

**A4 — Die vier Literale.** Teil D (`ruhig, krise`), Teil F (`ohne`),
`beispieldaten.py` Z. 69/77. Für jedes: Was prüft die Stelle, und braucht sie
ein **bestimmtes Jahr aus dem Register** oder nur **irgendeine Selektionsfalte**?

**A5 — Die Sonde.** Wo steht `BESTIMMT_NICHT_EINGETRAGEN`, was trägt es, und
welche Felder führt das Abbild `sperrliste_abbild_2026-09-23.json` wirklich?
⚠️ TB-96 hat gemessen: Das Abbild führt „bestimmt" **nicht als eigenes Feld**.
⇒ Die Umstellung braucht womöglich auch eine Änderung am **Erzeuger**
(`sperrliste_abbild.py`). Miss es, bevor du baust, und **melde es**, wenn der
Erzeuger mit muss.

**A6 — Hashes und Sonde am Eingang.** Wie in TB-96 (28 Pfade). Sonde gegen
`sperrliste_abbild_2026-09-23.json`: erwartet 0 Befunde, 15/15, (ii) `0`,
Gesamtausgang `2`.

---

## Block B — `F4` beisst wieder

Bauart wie `H3` in TB-95:

| | |
|---|---|
| **B1** | `<=` → `<`, sodass die Prüfung prüft, was ihr Text sagt |
| **B2** | Die Menge der Null-Falten aus dem **Plan**, als strikte Mehrheit (`len(sel)//2 + 1`), nicht als feste Zahl |
| **B3** | ⭐⭐ **Gegenprobe:** leere Menge ⇒ die Probe muss **scheitern**. Beide Ausgaben in den Beleg |
| **B4** | Der Kommentar nennt die neue Regel und die Zahl **mit Stand** („beim Plan von TB-97 … n von m") |

⛔ **Name und Stelle von `F4` bleiben.**

---

## Block C — Die vier Literale

⭐ **Fables Regel, zeichengleich:**

> Wo eine Prüfung eine konkrete Registeraussage prüft (wie G6 mit 5.1 Nr. 4), liest sie die Jahre maschinell aus dieser Stelle; wo sie nur „irgendeine Selektionsfalte" braucht (Teil F, freies Beispiel; `beispieldaten.py` Z. 69/77), nimmt sie sie aus dem Plan (`faltenplan.py`), z. B. die zweite Selektionsfalte des Bots, ohne Literal.

**Für Teil D**, zeichengleich:

> Wenn 4.4 den TB-30a-Stand trägt und die Prüfung diesen Stand prüfen soll, dann bekommt 4.4 eine Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan — sie prüft die Regel, nicht das Beispiel. Eine Prüfung, die an einem Beispieljahr hängt, prüft das Beispiel.

⚠️ **Die Tatsachennotiz zu 4.4 schreibt dieser Auftrag NICHT** — sie ist
Registertext und kommt mit dem nächsten Registerauftrag. Halte den Wortlaut im
Ergebnisdokument fest, damit er dort übernommen werden kann.

**Für jede der vier Stellen eine Gegenprobe**, die zeigt, dass sie nach der
Umstellung noch etwas prüft: Falte umwidmen, entfernen oder Plan verbiegen ⇒ die
Prüfung muss **rot** werden. ⭐ *Sonst haben wir ein Literal durch einen
Platzhalter ersetzt und nichts gewonnen.*

---

## Block D — Gegenproben für alle acht

Für jede der acht Proben aus A1 eine **dauerhafte** Gegenprobe, die der Test
selbst mitführt — nicht ein einmaliges Skript.

| | |
|---|---|
| ⭐⭐ | **Die Bauart entscheidest du** (Handwerk): eine zusätzliche Prüfung je Probe, ein gemeinsamer Durchgang, ein Schalter im Testrahmen. ⛔ **Aber sie muss bei jedem Lauf mitlaufen** — eine Gegenprobe, die man von Hand anstossen muss, ist die nächste Wache, die niemand sieht |
| ⚠️ | Die Gegenproben verlängern den Lauf. TB-95 brauchte 534 s. **Miss und melde die neue Laufzeit.** Wird sie unzumutbar (> ~25 min), brich Block D nach der Hälfte ab, melde es, und lass den Rest für einen eigenen Auftrag |
| ⚠️ | Beisst eine der acht **nicht** (wie `F4`), ist das ein **Befund**: melden, und — wenn es dieselbe Bauart ist wie `F4`/`H3` — im selben Zug beheben. Ist es eine andere Bauart, **nur melden** |

---

## Block E — Die Sonde

**E1 — Getrennte Schlusszeilen.** Fable, zeichengleich:

> Also zwei Zeilen im Schluss: „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert.

⛔ **Der Gesamtwert ändert sich nicht.** Nur die Ausgabe wird lesbar.

**E2 — Die Gruppen kommen aus dem Abbild.** Fable: *„Eine Gruppe, die im Code
der Sonde steht, ist ein Literal in einer Wache — dieselbe Klasse wie G6, nur
an der Sonde selbst."* Alle drei Gruppen (Abschnitt 10, „bestimmt",
`EINGEFROREN`) liest die Sonde aus dem Abbild.

⚠️⚠️ **Wenn A5 ergibt, dass das Abbild die Gruppe nicht führt:** Dann muss der
**Erzeuger** sie aufnehmen, und das heisst, das heutige Abbild kennt sie nicht.
⛔ **Erzeuge trotzdem kein neues echtes Abbild** — das gehört zum
Sperrlisten-Vollzug und braucht Freigabe. Baue den Erzeuger, weise ihn an einem
**Kopie**-Abbild im Scratchpad nach, und melde, dass ein echtes Abbild aussteht.

**E3 — Gegenprobe.** Kopie des Abbilds im Scratchpad, ein **erfundener**
„bestimmt"-Pfad hinein ⇒ die Sonde muss ihn melden. ⭐ Und ein Nullpunkt-Lauf
gegen das echte Abbild: unverändert 0 Befunde.

⛔ **`sperrliste_abbild_2026-09-23.json` wird nicht angefasst.** Hash vorher und
nachher gleich.

---

## Block F — Der ganze Test

```
trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py
```

| erwartet | |
|---|---|
| Schlusszeile | erreicht |
| Ergebnis | ⭐ **alle bestanden, rc 0** |
| Zahl | war 165. ⚠️ Jetzt **mehr**, weil Gegenproben dazukommen. **Nenne die neue Zahl und sag, wie viele dazugekommen sind** |
| Laufzeit | messen, mit 534 s vergleichen |

⚠️ **Wird eine Prüfung rot, die vorher grün war:** melden, die verursachende
Änderung zurücknehmen, so abgeben. ⛔ **Nicht weiterreparieren.**

Danach: Hashes der Sperrlistendateien (⛔ keine darf sich geändert haben) und
Sonde gegen das echte Abbild.

---

## Block G — Abgabe

| | |
|---|---|
| **G1** | Ergebnisdokument `docs/ERGEBNIS_TB-97_testannahmen_zweite_runde.md`, Bauart wie TB-95/TB-96 |
| **G2** | ⭐⭐ **Die Tabelle der acht Mutationsproben** — Name, Teil, was mutiert wird, beisst sie **vorher**, beisst sie **nachher**. Diese Tabelle ist der eigentliche Nachweis zu 40.7 und geht so in den Registertext |
| **G3** | Der Wortlaut für die **Tatsachennotiz zu 4.4** (Block C), gemessen, nicht eingetragen |
| **G4** | Ein Vorschlag für den **Registerabschnitt 41**, gemessen, nicht eingetragen |
| **G5** | Hashes vorher/nachher; ⛔ nur `test_vorregistrierung.py`, `shared/sperrlistensonde.py`, ggf. `sperrliste_abbild.py` und `beispieldaten.py` dürfen sich bewegt haben |
| **G6** | „In einfacher Sprache" und „Für die Folgesitzung vorbereitet" |
| **G7** | Journalblock |

**Commits:** (1) Schritt 0 · (2) Block B+C+D (Test) · (3) Block E (Sonde) ·
(4) Abgabe.

---

## ⚠️ Abbruchkriterien

1. Abschnitt 40 fehlt im Register.
2. **A1 findet nicht acht Mutationsproben** — melden, Zahl nennen, und mit der
   gemessenen Menge weiterarbeiten statt sie zurechtzubiegen.
3. Eine Sperrlistendatei ändert ihren Hash.
4. Ein echtes Abbild müsste erzeugt werden, damit E2 aufgeht → **melden**, nicht
   erzeugen.
5. Eine dritte Prüfung wird rot → Änderung zurücknehmen, so abgeben.
6. ⚠️ **`G6` wird rot** — dann hat etwas eine zweite Zeile mit dem Muster aus
   5.1 Nr. 4 erzeugt. Sofort suchen und entfernen; das ist die Wache aus 40.2.

---

## In einfacher Sprache

Das Prüfprogramm enthält acht Gegenproben: Sie verfälschen absichtlich eine
Stelle im Programm und schauen, ob sich das Ergebnis ändert. Tut es das nicht,
wäre die Regel wirkungslos — so soll der Nachweis funktionieren.

Bei einer dieser acht ist letzte Woche aufgefallen, dass sie das nie geleistet
hat: Ein falsches Vergleichszeichen liess sie immer „bestehen". Der
Verfahrensprüfer hat daraus eine Regel gemacht: **Jede solche Probe braucht
selbst eine Gegenprobe** — einen Nachweis, dass sie überhaupt anschlagen kann.
Eine Probe ohne diesen Nachweis zählt nicht.

Dieser Auftrag führt das für alle acht durch. Der erste Schritt ist dabei der
unscheinbarste und der wichtigste: **herausfinden, welche acht es überhaupt
sind.** Das Regelwerk nennt die Zahl, aber keine Namen. Wer die Namen nicht
kennt, kann die Regel nicht erfüllen — und merkt es nicht.

Dazu kommen vier eingetippte Jahreszahlen, die heute nur zufällig noch passen,
und die Wache über die geschützten Dateien, die selbst eine eingetippte Liste
enthält. Beides wird durch Werte ersetzt, die aus dem Regelwerk oder aus der
Prüfdatei kommen. Für jede Umstellung gibt es eine Gegenprobe — sonst hätten wir
eine eingetippte Zahl durch einen Platzhalter ersetzt und nichts gewonnen.
