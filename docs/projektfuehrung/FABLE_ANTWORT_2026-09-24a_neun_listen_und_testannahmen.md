# FABLE_ANTWORT 2026-09-24a — Die neun Listen sind Eingabe einer Herleitung und fallen unter 23d in voller Form; Abschnitt 40 eintragen; F4 und die vier Literale vor dem Tag; die Sonde liest ihre Gruppen aus dem Abbild

*Bezug: `FABLE_ANFRAGE_2026-09-24a_punkt8_vollzogen_test_gruen_neun_listen.md` (24.09., Anhang). Kenntnisnahme zu 1–3, drei Berichtigungen angenommen (4), Antworten auf die fünf Fragen (6), Abschnitt 40 (5) mit einer Ergänzung.*

---

## 1. Kenntnisnahme

**Punkt 8 im Register:** 575/0, 29 Zitate mit `diff` rc 0, zehn Marken, Abbild `2f23f76c…`, Sonde 0 Befunde — alle acht Kriterien erfüllt. **Plan-Punkt 8 ist fertig.** Der benannte Zwischenzustand hat eine Nacht gedauert und ist geschlossen; so war es gemeint.

**Test grün:** 165/165, rc 0, nur eine Datei geändert, keine Prüfung entfernt, keine Toleranz, `auswertung.py` unberührt. Die zwei Berichtigungen der Sitzung an den Erwartungen des Auftrags sind das Wertvollste daran: H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer; und die Quelle des Plans ist `faltenplan.py` zur Laufzeit, nicht die historische Datei (30.2 (1)). Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat, und die vier Gegenproben — vor allem „`ohne` leer ⇒ scheitert" — zeigen, dass sie aus dem richtigen Grund bestehen.

## 2. Drei Berichtigungen an mir — alle angenommen

**(a)** `benchmark.py` an **zwei** Punkten (4 und 6), nicht drei. Mein „drei" war nicht gemessen; richtig, dass 39.5 die gemessene Zahl trägt und meinen Satz nicht zitiert. Die Sache (ein Übergang, mehrere Punkte, eine Notiz) trägt mit zwei genauso.

**(b)** `beispieldaten.py` liest keine Benchmark-Tabelle. Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen. Repo-weit drei Leser, wie TB-88 sagte. Die Bedingung „Test und Lauf lesen dieselbe Konstante" ist mit zwei Dateien erfüllt.

**(c)** TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8.

Alle drei sind dieselbe Klasse wie die sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung genannt. Ich zähle sie mit.

## 3. Frage (1) — die neun Listen: 23d in voller Form, und die Form ist nicht „Snapshot", sondern „reproduzierbar aus Snapshot und Code"

**Was gemessen ist:** `benchmark.py` → `faltenplan.py::faltenlaenge_jahre` → `read_csv` der neun TB-24-Listen (`78e2bc6`, 13.09.); nur `entry_time`; Einträge je vollem Kalenderjahr gemittelt gegen die Schwelle aus 5.4 ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen ⇒ Tabellenzeilen. Störprobe in beide Richtungen: eine Zeile weg ⇒ bytegleich, zwei von drei weg ⇒ ein Bot kippt auf Zweijahresfalten. **Die Listen gehen ein — als Schwellenentscheidung.** Und sie sind nicht im Snapshot, nicht auf der Sperrliste, aus Code und Daten vor TB-31/34 erzeugt.

**Eure Frage:** Genügt für eine Eingabe, die nur über eine registrierte Schwellenentscheidung wirkt, ein Hash-Eintrag — oder die volle Regel aus 23d?

**Die volle Regel.** Und zwar aus dem Grund, den die Störprobe selbst liefert: Eine Schwellenentscheidung ist nicht „kleiner" als ein stetiger Einfluss, sie ist **unsichtbarer**. Kleine Änderungen zeigen nichts, ein Übertritt verschiebt den ganzen Faltenplan eines Bots — und damit 33.2, die Benchmark-Tabelle, die Zellen. Ein Hash-Eintrag würde festhalten, **dass** die Listen so sind, wie sie sind; er sagt nichts darüber, ob sie den Datenstand beschreiben, mit dem der Lauf rechnet. Genau das war der Befund bei `messgroessen.json` (23f/23d), und hier ist er derselbe: **erzeugt vor TB-34, die Krypto-Listen beginnen 2021-09, der Snapshot beginnt 2017-08.** Ob die Faltenlänge eines Krypto-Bots auf dem Snapshot anders ausfiele, weiss ich nicht — und das ist der Grund, die Regel zu halten, nicht sie zu lockern: Wer jetzt „Hash genügt" sagt, weil ein Nachrechnen Falten bewegen könnte, wählt nach Wirkung.

**Zu eurem Einwand „nicht möglich, ohne sie in einen Snapshot zu nehmen":** 23d verlangt nicht, dass jede Eingabe **im** Snapshot liegt — es verlangt, dass sie **aus** dem registrierten Snapshot und dem registrierten Code **reproduzierbar** ist. Kursdaten liegen im Snapshot; Ergebnisdateien werden daraus erzeugt. Die Listen sind Ergebnisdateien der neun Backtests mit heutigen Parametern; TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren. Also:

> **Registertext, Ergänzung zu 23d („Eingabestand") und zu 5.4:** Die neun Trade-Listen, aus denen `faltenlaenge_jahre` die Faltenlänge nach 5.4 ableitet, sind Eingabe einer Herleitung von Registertext (33.2) und damit Eingabedateien im Sinn von 23d. Sie werden **vor dem Tag einmal auf dem registrierten Snapshot mit dem registrierten Code neu erzeugt** — im Selektionsmodus, mit den registrierten heutigen Parametern, durch einen Erzeuger unter 36.1 (`--ziel`, Einmal-Schreibsperre), mit Beleg, je Liste Hash, Snapshot-Hash und Commit als Tatsachennotiz — und als Punkt auf die Sperrliste aufgenommen; `faltenplan.py` liest sie über einen registrierten Pfad (Konstante, kein Schalter). Die alten Listen (`78e2bc6`) bleiben liegen als historischer Stand mit Tatsachennotiz. **Danach wird die Faltenlänge je Bot nach 5.4 aus den neuen Listen abgeleitet und gegen 33.2 verglichen.** Gleich ⇒ Tatsachennotiz. Verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt" — keine Wahl. Der Reproduzierbarkeitsnachweis (23e) ist der Modus-Lauf selbst: zweimal, bytegleich.

*Quelle des Grundes:* 23d (Eingaben reproduzierbar aus Snapshot und Code), 5a/5e, 3 („erzeugt, nicht abgetippt"), 24.3 als Bauart — die Regel steht, bevor gerechnet ist. **Kein Ergebnis:** Ich verlange die Ableitung, ohne zu wissen, ob sie 33.2 bestätigt; und ich brauche danach nur das Ob je Bot (1 oder 2), keine Trade-Zahlen (27.1 nennt „Anzahl Trades" — die Sitzung meldet die Faltenlänge, nicht die Zählung).

*Zu eurem Umstand 1* (die Faltenlänge ist als Ergebnis registriert, eine Kippung würde am Abbild sichtbar — „vorausgesetzt, das Abbild ist erzeugt, und es ist es nach 33.5 nicht"): richtig, und das ist die zweite Folge dieser Antwort — **Plan-Punkt 7 (Abbild des Faltenplans, Faltenplan-Sonde) rückt vor**; es ist die Wache, die diese Klasse fängt, und sie fehlt noch. Das Abbild wird nach der Ableitung erzeugt, nicht vorher — sonst bildet es einen Stand ab, der gerade geprüft wird.

*Zu eurem Umstand 2* („über `git` reproduzierbar"): Aus der Git-Historie reproduzierbar heisst, aus einem Datenstand, den der Lauf nicht verwendet. Das ist genau die Unterscheidung aus 23d, Frage (1): historischer Stand, kein Eingabestand.

**Eine Folge für 5.4 selbst:** 5.4 nennt die Listen „als Quelle, ohne Hash". Nach dieser Antwort nennt eine Tatsachennotiz zu 5.4 die neuen Listen mit Hash, Snapshot und Commit; der Regeltext von 5.4 (die Schwelle) bleibt unverändert.

## 4. Frage (2) — Abschnitt 40 eintragen: ja, mit zwei Anpassungen

Eintragen, wie vorgeschlagen, mit: **40.5 als Nachtrag zu 39.8** (es setzt dessen Tatsache fort, und wer 39.8 liest, soll dort fündig werden — dieselbe Regel wie bei den Marken am alten Ort); und **40.6 neu:** die Entscheidung aus Abschnitt 3 dieser Antwort (Listen als Eingabedateien, Neu-Erzeugung, Vergleich gegen 33.2, Sperrlistenpunkt), damit 40.5 nicht mit „Einordnung steht aus" endet, sondern mit der Einordnung. 40.4 (Liste der weiteren Literale) bleibt, wird aber durch Frage (4) unten zum Auftrag.

## 5. Frage (3) — F4: vor dem Tag, und eine Regel für alle Mutationsproben

**Vor dem Tag.** Eine Prüfung, die nie beissen konnte (`<=` statt `<`, bei gleichen Medianen), ist kein Nachweis; sie steht aber in der Zahl, mit der Abschnitt 12 die Vollständigkeit belegt („150 Prüfungen, davon acht Mutationsproben"). Am Tag muss diese Zahl wahr sein — nicht als Anzahl, sondern als Aussage. Dass F4 nicht am Faltenplan hängt, ändert die Kategorie („Testannahmen folgen dem Register" → hier: „die Prüfung prüft, was sie sagt"), nicht den Zeitpunkt. `<=` → `<`, Probe mit Mehrheit wie H3, Gegenprobe „leere Menge ⇒ scheitert".

> **Registertext, Ergänzung zu 12:** Jede Mutationsprobe hat eine **Gegenprobe**, die zeigt, dass sie rot werden kann (die Mutation weggelassen ⇒ die Probe scheitert). Eine Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal geführt und als Tatsachennotiz festgehalten.

*Quelle des Grundes:* A8 (eine Wache ist, was ein anderer gegenprüfen kann) und 12. F4 ist der Beleg, dass eine Probe drei Wochen „bestehen" kann, ohne je gemessen zu haben — TB-45 in anderer Form. Kein Ergebnis.

## 6. Frage (4) — die vier Literale: bauartgleich umstellen, vor dem Tag

Euer Satz ist der Grund: **Eine Prüfung, die grün ist, weil ihr Literal zufällig noch stimmt, ist genauso gealtert wie eine rote — sie sagt es nur noch nicht.** Teil D bricht mit `KeyError`, sobald der Bot Zweijahresfalten bekommt — und ob er das nach Abschnitt 3 dieser Antwort bekommt, weiss heute niemand. Also vor der Ableitung umstellen, nicht danach.

**Welche Registerstelle die Jahre trägt:** Wo eine Prüfung eine konkrete Registeraussage prüft (wie G6 mit 5.1 Nr. 4), liest sie die Jahre maschinell aus dieser Stelle; wo sie nur „irgendeine Selektionsfalte" braucht (Teil F, freies Beispiel; `beispieldaten.py` Z. 69/77), nimmt sie sie aus dem Plan (`faltenplan.py`), z. B. die zweite Selektionsfalte des Bots, ohne Literal. Für Teil D („2021", „2020"): Wenn 4.4 den TB-30a-Stand trägt und die Prüfung diesen Stand prüfen soll, dann bekommt 4.4 eine Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan — sie prüft die Regel, nicht das Beispiel. Eine Prüfung, die an einem Beispieljahr hängt, prüft das Beispiel.

## 7. Frage (5) — die Sonde

**(i) Ausgabe trennen: ja — die Regel bleibt.** Gesamtausgang 2 bei zwölf Punkten mit Regelanteil ist korrekt (36.5/37) und am Tag mit Tatsachennotiz zulässig (22g/37.3). Aber die Tag-Vorbedingung aus 22d lautet „kein Pfad-Bestandteil 1, jede 2 mit Notiz" — und die soll man an der Ausgabe **ablesen** können, ohne zu rechnen. Also zwei Zeilen im Schluss: „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert.

**(ii) Die Gruppe „bestimmt" fest verdrahtet in `sperrlistensonde.py`: ein Befund, vor dem Tag zu beheben.** 36.6 sagt: Das Abbild ist die maschinenlesbare Fassung, die Sonde prüft **gegen das Abbild** — auch die Gruppe „bestimmt" (37.2). Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache — dieselbe Klasse wie G6, nur an der Sonde selbst. Sie liest alle drei Gruppen (10, „bestimmt", `EINGEFROREN`) aus dem Abbild; das Abbild führt die Gruppe „bestimmt" heute leer (39.3). Handwerk mit Freigabe; die Sonde ist nicht gesperrt; danach Nullpunkt-Lauf und Gegenprobe (Abbild mit einem erfundenen „bestimmt"-Pfad ⇒ Sonde meldet ihn).

## 8. Was daraus auf den Plan kommt

- **Neu, Stufe III:** Neun Trade-Listen auf dem Snapshot neu erzeugen (Erzeuger unter 36.1), Sperrlistenpunkt, Notizen; Faltenlänge nach 5.4 ableiten und gegen 33.2 vergleichen; Folgen als Berichtigung.
- **Punkt 7 rückt vor** (Abbild des Faltenplans + Sonde) — nach der Ableitung, als Wache gegen diese Klasse.
- **Testannahmen, zweite Runde:** F4 (`<`, Mehrheit, Gegenprobe), vier Literale (aus Registerstelle oder Plan), Gegenproben für alle acht Mutationsproben mit Notiz.
- **Sonde:** Gruppen aus dem Abbild; getrennte Schlusszeilen; Gegenprobe.
- Abschnitt 40 mit 40.5 als Nachtrag zu 39.8 und 40.6 neu.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23f; dazu ANFRAGE 24a (als Anhang). Nicht gelesen: `belege/` (nach eurem Hinweis: gesperrt vor dem Tag, ich lese dort nichts), ANFRAGE 21d, `MAC_TB-82…95`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** Punkt 8 fertig, Test 165/165 — beides angenommen, drei Berichtigungen an mir ebenso. (1) Die neun Listen fallen unter 23d in voller Form: Eine Schwellenentscheidung ist nicht kleiner, sondern unsichtbarer; Hash allein friert einen fremden Datenstand ein. Neu erzeugen auf dem Snapshot mit registriertem Code (Backtests reproduzieren byte-identisch), Sperrlistenpunkt, Faltenlänge nach 5.4 ableiten, gegen 33.2 vergleichen; Abweichung ist Berichtigung, keine Wahl; Punkt 7 rückt vor. (2) 40 eintragen, 40.5 als Nachtrag zu 39.8, 40.6 mit dieser Entscheidung. (3) F4 vor dem Tag; Regel: jede Mutationsprobe hat eine Gegenprobe. (4) Vier Literale umstellen, vor der Ableitung — Jahre aus der Registerstelle oder aus dem Plan. (5) Sonde: getrennte Schlusszeilen, Regel bleibt; „bestimmt" aus dem Abbild statt aus dem Code — ein Literal in einer Wache.

**Unsicher:** ob 5.4 die Schwelle „mit heutigen Parametern" ausdrücklich nennt — wenn nicht, gehört der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4, sonst ist die Ableitung nicht reproduzierbar.

---

## In einfacher Sprache

Der Austausch der Vergleichstabelle steht jetzt auch im Regelwerk, und das Prüfprogramm ist fehlerfrei — beides fertig. Die grosse Frage: Neun alte Handelslisten vom 13. September bestimmen, ob ein Bot ein- oder zweijährige Zeitabschnitte bekommt. Sie stammen aus einer Zeit vor der Erweiterung der Krypto-Daten und gehören nicht zum eingefrorenen Bestand. Genügt es, ihre Prüfsumme festzuhalten? Fable sagt nein: Eine Ja-Nein-Schwelle ist nicht harmloser als ein stetiger Einfluss, sondern nur schwerer zu sehen — und die Prüfsumme würde bezeugen, dass die Listen so sind, nicht, dass sie zum Datenstand passen. Die Listen werden deshalb aus dem eingefrorenen Bestand neu erzeugt (die Programme dafür sind nachweislich reproduzierbar), geschützt, und die Zeitabschnittslänge wird nach der festen Regel neu abgeleitet und mit dem Regelwerk verglichen. Ob sich dabei etwas ändert, weiss niemand — genau deshalb steht die Regel jetzt fest. Dazu drei kleinere Dinge, alle vor dem Stichtag: eine Prüfung, die durch ein falsches Vergleichszeichen nie anschlagen konnte, wird repariert und künftig hat jede solche Probe eine Gegenprobe; vier eingetippte Jahreszahlen werden durch Werte aus dem Regelwerk oder dem Plan ersetzt; und die Wache selbst enthält eine eingetippte Liste, die aus der Prüfdatei kommen muss statt aus dem Programm.
