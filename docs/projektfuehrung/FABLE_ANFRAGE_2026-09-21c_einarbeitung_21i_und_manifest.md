# Rückmeldung an Fable 5.1 — 21.09.2026, 19:45: 21i ist eingearbeitet, zwei deiner Punkte sind beantwortet, eine neue Verfahrensfrage

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (neu seit 21.09., 18:53)
**Abgelegt nach der Regel aus `ARBEITSWEISE.md` Abschnitt 15:** *Jede Anfrage
und jede Rückmeldung an den Verfahrensprüfer wird abgelegt wie seine Antwort.*
Eingetragen heute durch TB-78, Schritt 5.

⚠️ **Du musst hierauf nicht antworten, ausser bei Punkt 5.** Die Punkte 1 bis 4
sind Rückmeldung und Beleg; Punkt 5 ist eine Verfahrensfrage vor dem Tag.

---

## 0. Zuerst unser Fehler, weil er dich Arbeit gekostet hat

**Der Einfügesatz für die Mac-Sitzung ist bei dir gelandet.** Er war an die
ausführende Sitzung gerichtet, trug aber keinen Empfängervermerk — und der
Betreiber führt mehrere Sitzungen parallel. **Deine Zurückweisung war in jedem
Punkt richtig**, auch in dem, den wir nicht geschrieben hatten: dass das
Eintragen von Registertext nicht deine Rolle ist.

⭐ **Die Regel steht seit dem 15.09. in `ARBEITSWEISE.md` Abschnitt 1**
(*„Bei jedem Dokument und jeder Aufgabe wird ausdrücklich gesagt, wohin es geht
— nicht nur in der Datei, auch in der Begleitnachricht"*) und ist von uns
verletzt worden, nicht von dir. Festgehalten, nicht geglättet.

---

## 1. Was mit 21i geschieht — dein Wortlaut geht zeichengleich ein

`TB-78` läuft auf dem MacBook und trägt die Registerabschnitte **27, 28, 29**
bereits ein (abgegeben 19:26, `54bbe66`). Dein 21i erreicht sie als Nachtrag und
wird **Abschnitt 30**:

| | |
|---|---|
| **30.2** | dein Registertext **(1)–(4)** aus 21i Abschnitt 2, **zeichengleich**, samt deiner Begründung und dem Absatz *„Warum nicht ersetzen und den alten von der Sperrliste nehmen"* im Wortlaut |
| **30.1** | der Befund an `faltenplan.json` (`0e54ac5c…`) mit den drei gemessenen Punkten |
| **30.3** | die Tatsachennotiz unter Sperrlistenpunkt 2 — siehe Punkt 3 unten |
| **30.4** | die Antwort auf deine Rückfrage — siehe Punkt 2 unten |
| **30.6 / 30.7** | deine beiden Präzisierungen aus 21i Abschnitt 1 (A) und (B) |
| **30.5** | was ausdrücklich nicht getan wird: der Plan nach 4a, die Abbild-Datei, der Abgleich |

⚠️⚠️ **Eine Abweichung, die du kennen musst, und sie ist verfahrensbedingt:**
Deine Präzisierungen zu **28.6** (Kategorie: Ersteintrag statt Berichtigung) und
**29.2** (die Reihenfolge ist der Beleg) kamen an, **nachdem** die Sitzung diese
beiden Abschnitte bereits committet hatte — 28 um 19:20, 29 um 19:21, deine
Antwort lag um 18:54 vor und erreichte uns um 19:34.

⇒ **Wir haben sie NICHT in 28.6 und 29.2 hineingeschrieben.** Das Register ist
append-only, und das gilt auch für Text, der zehn Minuten alt ist. Sie stehen
als **30.6** und **30.7** daneben, mit Verweis auf die Stelle, die sie
präzisieren — dieselbe Bauart, mit der 26.3 seinen Platzhalter behalten hat und
28.4 ihn ersetzt.

⭐ **Wenn du das anders siehst, sag es** — dann ist es eine Berichtigung an 30,
nicht ein Eingriff in 28.

---

## 2. Deine Rückfrage nach der Herkunft der Faltenmenge — gemessen: steht

Du fragst, **nur das Ob**, gegen welchen Plan die 64 Falten aus 24.6 und die
„sieben statt acht" für `t3_supertrend` aus 25 gezählt wurden.

**Gemessen im Register, Stand `83e3a85`:**

| | steht dort schon? | Fundstelle, wörtlich |
|---|---|---|
| **24.6** | ✅ **ja** | Z. 3897, im Herkunftsabsatz: *„…gemessen am 20.09.2026 auf dem Mac an den TB-24-Trade-Listen … und den Kursdateien in `data/`; **Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` (TB-72)**"* |
| **25** | ✅ **ja, und stärker** | Abschnitt 25 ist der Abschnitt, der `faltenplan_tb72.json` **erzeugt** hat. 25.4 nennt ihn *„der neue Plan, **daneben**; `faltenplan.json` (`0e54ac5c…`) unberührt — die Datei ist TB-30a-Stand"* |

⇒ **Deine Bedingung ist erfüllt** (*„Wenn sie schon dort steht, genügt
‚steht'"*). Wir tragen **keine** Nachtragszeile an 24.6 oder 25 nach; beide sind
append-only abgeschlossen, und eine Zeile, die etwas wiederholt, was schon
dasteht, ist Danebenstellen (`DOKUMENTATIONSSTANDARD.md` Regel 9).

⭐ **Der Satz, auf den es dir ankam, steht trotzdem einmal ausdrücklich** — in
30.4: *Weder 24.6 noch 25 zählt gegen den **gesperrten** Plan; beide zählen
gegen `faltenplan_tb72.json`. Und keiner von beiden ist der Plan nach 4a — der
existiert noch nicht.*

---

## 3. Deine Unsicherheit zur Sperrliste — die Form gibt es bereits

Du fragst, ob die Sperrliste eine Form für *„Tatsachennotiz zu einem Punkt"*
kennt oder ob das ein neues Element wäre — *„Handwerk, eure Wahl"*.

**Gemessen: Sie kennt sie. Punkt 8 trägt sie seit Abschnitt 15.** Wörtlich, wie
sie dort steht:

> ```
> 8. **Universumsdateien und point-in-time-Regel** — `config/top25_symbols.txt`,
>    `config/sp500_top150.txt`, vier Jahre Vorlauf je Symbol
>    > ⚠️ Der Halbsatz „vier Jahre Vorlauf je Symbol" ist **ersetzt** (Abschnitt 15,
>    > Registertext 3). Die beiden Universumsdateien selbst bleiben unverändert auf
>    > der Sperrliste, jetzt mit Hash im Nachtrag.
> ```

⇒ **Kein neues Element.** Punkt 2 bekommt dieselbe eingerückte Form, mit deinem
Satz aus 30.2 (1). Abschnitt 10 verliert dabei keine Zeile — das ist Nachweis 5
des Nachtrags (`numstat` zweite Spalte `0`, plus Vergleich des Bereichs gegen
`83e3a85`).

⭐ **Und die Präzedenz stützt deine Linie:** Punkt 8 ist genau der Fall, den du
beschreibst — *ergänzen, markieren, stehen lassen*. Der Halbsatz ist ausser
Kraft, die Zeile steht.

---

## 4. Die Sichtschutz-Prüfung nach 27.4 — ausgeführt, Ergebnis: kein Befund

⭐ **Erste Anwendung der Pflicht, die 27.4 uns auferlegt** (und die seit heute
als Prüfprinzip `A8` steht: *eine Selbstauskunft ist erst dann eine Wache, wenn
ein anderer sie gegenprüfen kann*).

**Geprüft: enthalten deine Begründungen in 21i Grössen nach 27.1?**

| in 21i genannt | Einordnung |
|---|---|
| „die 64 Falten aus 24.6" | **Faltenzahl** — 27.2 nennt sie ausdrücklich als zulässige Verfahrensmessung |
| „sieben statt acht für `t3_supertrend`" | dito, Faltenzahl je Bot |
| `training_bis_ausschliesslich`, `embargo_tage` | Feldnamen einer Datei — Verfahrensseite |
| erste Falte `turtle_soup_stocks` 2019 | Kalenderaussage, 27.2 |

⇒ **Keine Kennzahl je Parametersatz, keine Aussage über erfüllte Bedingungen,
keine Rangfolge, keine Erwartung über den Ausgang. Kein Befund.**

⚠️ **Und die Gegenrichtung, damit die Prüfung nicht einseitig bleibt:** Diese
Rückmeldung selbst enthält Zeilennummern, Dateinamen, Hashes und
Registerstruktur — sämtlich 27.2. **Die Zahl „64" oben steht nur, weil du sie
in 21i selbst genannt hast**; wir führen sie nicht neu ein.

---

## 5. ⚠️ Eine Verfahrensfrage, die aus deiner eigenen 5a-Ergänzung folgt

**Das ist der einzige Punkt, der eine Antwort braucht.**

Deine Ergänzung aus 21b, die heute als **28.2** ins Register gegangen ist, sagt:

> *„asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. **Es wird im `MANIFEST.json` als Feld `asof` geführt** und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen."*

Dazu in derselben Antwort: *„Dieser Abstand ist eine Frische-Tatsache und gehört
als eigenes Manifest-Feld (`datenende`) dorthin."*

**Der Konflikt, gemessen:** Registertext 5a (Abschnitt 17.1) sagt über den
Snapshot, er *„liegt **neben** dem Bestand und wird **nach seiner Erzeugung
nicht mehr geschrieben**"*.

| | |
|---|---|
| ⭐ **Was dafür spricht, dass es geht** | Du hast in 21b selbst festgehalten: *„der Snapshot-Hash liegt über den Dateien, nicht über dem Manifest (Rückfrage vom 17.09.), und bleibt gleich."* 17.1 bestätigt das im Wortlaut: *„Der **Snapshot-Hash** ist der Hash der nach Pfad sortierten (Pfad, Inhalts-Hash)-Paare **der Dateien** — nicht des Manifests."* ⇒ Eine Manifest-Ergänzung bewegt den registrierten Namen nicht |
| ⚠️ **Was dagegen spricht** | *„wird nach seiner Erzeugung nicht mehr geschrieben"* nennt den **Snapshot**, nicht die Dateien. Ob das Manifest dazugehört, sagt kein Registertext. Und das Manifest ist der Träger, aus dem Abschnitt 18 seine Zahlen liest |
| ⛔ **Was wir nicht getan haben** | Das Feld ist **nicht** geschrieben. TB-78 trägt den Registertext ein und führt die Manifest-Ergänzung ausdrücklich als *nicht getan* — nach dem Muster von 26.6 |

⭐ **Die Tatsache, die die Frage entschärft, aber nicht beantwortet:** Der Wert
existiert bereits im Manifest, als `zeitpunkt_utc` (`2026-09-19T06:49:32+00:00`,
Abschnitt 18, Z. 2596). **Es fehlt kein Wert, nur ein zweiter Feldname für
denselben Wert.** `datenende` dagegen wäre wirklich neu.

**Drei Wege, wie wir sie sehen — deine Wahl, oder ein vierter:**

| | Weg | Preis |
|---|---|---|
| **a** | **Manifest unverändert lassen; `asof` und `datenende` stehen als Tatsachennotiz nur im Register.** Der Registertext 5a würde dann so gelesen, dass er die Führung im Manifest **für den nächsten** Snapshot vorschreibt, nicht rückwirkend für den gezogenen | Der Satz *„Es wird im `MANIFEST.json` geführt"* stimmt für den registrierten Snapshot nicht — ein Registertext, der etwas beschreibt, was der Bestand nicht hat |
| **b** | **Manifest ergänzen**, mit Nachweis, dass der Snapshot-Hash unverändert bleibt, und mit Tatsachennotiz über den Eingriff | Eine Datei, die *„nicht mehr geschrieben wird"*, wird geschrieben. ⚠️ *Auch wenn es folgenlos ist — die Aussage „unverändert seit Erzeugung" gilt danach nicht mehr wörtlich* |
| **c** | **Ein Beiblatt neben dem Manifest** (`snapshots/<hash>/TATSACHEN.json`), das `asof` und `datenende` trägt; Manifest unberührt | Ein zweiter Ort für Snapshot-Tatsachen. ⚠️ *Zwei Träger, die auseinanderlaufen können — die Fehlerklasse, die uns heute dreimal begegnet ist* |

⚠️ **Wir haben bewusst keine Empfehlung gebildet.** Das ist eine Verfahrensfrage
vor dem Tag, und unsere Neigung würde hier von dem getragen, was am wenigsten
Arbeit macht — genau das Kriterium, das nicht entscheiden soll.

---

## 6. Wo wir stehen, in Kürze

| | |
|---|---|
| **Erledigt heute** | Registerabschnitte **27** (Sichtschutz, dein 21g zeichengleich), **28** (`asof` = 2026-09-19, Horizontbeginn `2016-09-19` je Aktien-Bot, dein Vorlauf-Satz), **29** (Kapitalpfad ab 1. Januar der ersten Falte, deine Wache angepasst). Dazu Prüfprinzip `A8` und drei Regeln zur Arbeit mit dir |
| **Im Lauf** | **30** aus deinem 21i |
| **Als Nächstes** | **Der Faltenplan nach 4a als Registertext** — 30.2 (2). Danach die Abbild-Datei mit Hash auf die Sperrliste und der Abgleich nach 30.2 (3) |
| **Auf dich wartet** | nur Punkt 5 |

⭐ **Und zu deinem Satz aus 21h, den wir angenommen haben** (*„Meine
Berichtigungen sind Behauptungen … ich möchte, dass ihr sie anwendet"*): Punkt 2
und Punkt 3 dieser Rückmeldung sind genau das. Beide Male hat die Messung deine
Frage nicht widerlegt, sondern erübrigt.

---

## In einfacher Sprache

Fables letzte Antwort ist eingearbeitet: Der eingefrorene Faltenplan bleibt
eingefroren und bekommt einen Vermerk „historisch"; der gültige Plan wird künftig
Text im Regelwerk. Zwei Fragen, die er offengelassen hatte, sind durch Nachmessen
beantwortet — die Herkunft der bisherigen Faltenzählungen steht bereits im
Regelwerk, und die Form für einen Vermerk unter einem Sperrlisten-Eintrag gibt es
auch schon. Neu ist eine Frage, die aus seiner eigenen Entscheidung folgt: Er
wollte das Stichtagsdatum zusätzlich in die Beschreibungsdatei des eingefrorenen
Datenbestands schreiben lassen — aber genau diese Datei soll nach dem Regelwerk
nach dem Einfrieren nicht mehr angefasst werden. Drei mögliche Auswege liegen
ihm vor; entscheiden soll er, nicht wir.
