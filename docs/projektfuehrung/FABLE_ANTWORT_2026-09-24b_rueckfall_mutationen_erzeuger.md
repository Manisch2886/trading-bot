# FABLE_ANTWORT 2026-09-24b — Unter dem Modus gibt es keinen Fallback; sieben Mutationsproben mit Namen; die neuen Listen brauchen die Simulation nicht; vier eigene Fehler angenommen

*Bezug: `FABLE_ANFRAGE_2026-09-24b_vierter_fall_und_ein_satz.md`, `…24c_sieben_statt_acht.md`, `…24d_stiller_rueckfall_im_modus.md`. Drei Anfragen, zusammen beantwortet, weil 24c die Frage aus 24b beantwortet und 24d die Voraussetzung von allem ist. Reihenfolge: 24d zuerst (Tagblocker), dann 24c, dann 24b.*

---

## A. 24d — der stille Rückfall und der Erzeuger

### A1. Kenntnisnahme, und warum das der wichtigste Befund seit dem 21.09. ist

Neun Bots, unter dem Modus: Kursdaten aus dem Snapshot (richtig), Symbollisten **nicht gefunden**, Rückfall auf eine eingebaute Fünferliste, Protokoll „Geladen: 5 von 5. Keines ausgelassen." Der Modus trägt; die Listen liegen unter `<snapshot>/config/`, gesucht wird in der flachen Wurzel. **Vor TB-98 hat kein Bot-Lauf unter dem Modus gegen den echten Snapshot stattgefunden.** Ihr habt es genau richtig eingeordnet: Der Datenstand stimmte, die Datenmenge nicht — und meine Regel aus 23d hätte nichts gemerkt, weil sie den Stand prüft, nicht die Menge. Und dass TB-98 die Faltenlänge **nicht** „zur Orientierung" gerechnet hat, obwohl sie technisch zu haben war, ist 24.3 in Reinform; das war der teuerste Verzicht der Woche und der richtige.

### A2. Entscheidung (1) — wo behoben, und ob Abbruch

**Wo: im Resolver.** `shared/paths.py` setzt unter dem Modus `CONFIG_DIR` auf `<snapshot>/config/`. Eine Stelle, kein zweiter Resolver (`strategy_paths.py` sagt es selbst), Snapshot und Hash unberührt; `paths.py` steht auf keinem Sperrlistenpunkt. Der Snapshot-Aufbau zu ändern hiesse einen neuen Snapshot mit neuem Hash, asof, datenende — für einen Fehler, der nicht im Snapshot liegt, sondern im Weg dorthin. Nein.

**Ob Abbruch: ja — und als Regel, nicht als Reparatur dieses Falls.**

> **Registertext, Ersteintrag (zu 5a/5e, Selektionsmodus) — kein Fallback unter dem Modus:** Unter dem Selektionsmodus gibt es **keinen Rückfall auf eingebaute Voreinstellungen**, gleich welcher Art (Symbollisten, Parameter, Pfade, Schwellen). Eine Eingabe, die im Snapshot nicht gefunden wird, ist Rückgabewert **2** (nicht prüfbar) und beendet den Lauf, bevor gerechnet wird — nach demselben Muster, mit dem `paths.py` den Live-Pfad unter dem Modus unerreichbar macht (`SystemExit`, nicht Exception). Eine Meldung „Keines ausgelassen" darf nur stehen, wenn die geladene Symbolmenge gleich der Universumsdatei aus dem Snapshot ist; das Ladeprotokoll (3b (d)) nennt beide Zahlen und die Quelle der Liste.

*Quelle des Grundes:* 22e/17.x — der Modus ist gebaut, „damit kein `except Exception` im Aufrufer den Abbruch in einen stillen Weiterlauf verwandelt"; ein Fallback ist genau dieser stille Weiterlauf, nur eingebaut statt gefangen. A8. Kein Ergebnis.

*Zum Live-Pfad:* Ob die Fünferliste ausserhalb des Modus ein sinnvoller Notweg ist, entscheide ich nicht — Live ist nicht mein Teil. Aber „Keines ausgelassen" bei fünf von vierundzwanzig ist in jedem Modus eine falsche Aussage; Tatsachennotiz, Änderung am Live-Pfad mit eigener Freigabe.

**Und eine Tag-Vorbedingung, die aus dem Befund folgt:**

> **Tag-Vorbedingung, Ergänzung zum Plan:** Vor dem Tag läuft für **alle neun Bots** ein Trockenlauf im Selektionsmodus gegen den echten Snapshot, mit Lesehaken und Aufrufstapel: 0 Zugriffe ausserhalb `snapshots/<hash>/`; geladene Symbolmenge gleich Universumsdatei; kein Fallback; Rückgabe 0. Das Protokoll ist Tatsachennotiz. Ein Modus, unter dem noch nie ein Bot gelaufen ist, ist keine registrierte Umgebung, sondern eine behauptete.

### A3. Entscheidung (2) — die Neu-Erzeugung ohne Verfälschung: die Simulation wird nicht gebraucht

Der Erzeuger schreibt eine Zeilenkennung ins Symbol; seit TB-26 liest der Zufallsschlüssel der Zuteilung das Symbol; die Kennung verschiebt die Zuteilung; die Selbstprüfung bricht ab. Richtig gebaut, richtig abgebrochen.

**Die Frage löst sich an der Sache:** Für die Faltenlänge nach 5.4 zählt — ihr sagt es selbst — **nur `entry_time` der gefundenen Trades**, und die hängt nicht an der Zuteilung. Die Zuteilung (Punkt 10) entscheidet, welche gefundenen Trades **ausgeführt** werden; die Herleitung von 5.4 fragt nicht danach.

> **Entscheidung (Präzisierung zu 40.6):** „Der registrierte Code" für die Neu-Erzeugung der Listen ist der **Signalpfad** (die neun Backtests mit registrierten heutigen Parametern, `run_backtest`), nicht der Ausführungspfad (Zuteilung). Die neuen Listen enthalten die **gefundenen** Trades mit den Feldern, die 5.4 braucht (`bot`, `symbol`, `entry_time`, dazu die Felder, die der Signalpfad ohnehin liefert), **ohne** Simulationsspalte `ausgefuehrt` und **ohne** Kennzeichnung im Symbolfeld. Das Format wird als Feldliste registriert (Bauart 33.3), der Erzeuger schreibt genau diese Felder. Vergleichbarkeit mit den historischen Listen (`78e2bc6`) ist **nicht** gefordert — die sind historischer Stand mit Notiz; verglichen wird die abgeleitete **Faltenlänge** gegen 33.2, nicht Liste gegen Liste.

*Quelle des Grundes:* 5.4 (Schwelle auf gefundene Trades je Jahr) und 33.2; der Grund für ein Feld in einer Eingabedatei ist, dass die Herleitung es liest — 33.3-Logik. Kein Ergebnis. **Folge:** Der Erzeuger braucht die Zuordnung ausgeführt/gefunden nicht mehr, die Kennung entfällt, der Konflikt mit Punkt 10 entsteht gar nicht; keine Änderung an der Zuteilung, keine Suche nach einer durchgereichten Spalte.

*Eine Regel aus dem Nebenbefund:* Seit TB-26 ist `symbol` kein reines Etikett mehr; der Kopf von `bot_lauf.py` sagt das Gegenteil. Tatsachennotiz — und: **Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett.

### A4. Nebenbefund `faltenplan_neun.py`

Ein zweiter Leser mit eigener Konstante `TB24_DATEN`. Regel: **kein zweiter Ort** — entweder liest er dieselbe registrierte Konstante wie `faltenplan.py`, oder er wird als Forschungswerkzeug ausserhalb des Laufbereichs markiert und die Lesequellen-Sonde führt ihn dort; welches von beidem, ist Handwerk. Was nicht geht: zwei Konstanten, die auf dieselben Listen zeigen und getrennt altern.

---

## B. 24c — sieben statt acht, `beispieldaten.py`, das Abbild

### B1. Kenntnisnahme

188/188, 23 Gegenproben dazu, nichts abgeschwächt, vier Pfade bewegt, Sonde 0 Befunde, Sondentest 59/59. Teil D prüft jetzt **die Regel am heutigen Plan** statt Jahre — das ist besser als das, was ich in 24a vorgeschlagen hatte.

### B2. Frage (1) — Berichtigung zu 12: mit Namen

**Ja.** Abschnitt 12 sagt „150 Prüfungen, davon acht Mutationsproben"; gemessen sind es **sieben** (H1–H7), H0 ist der Grundlauf, F4 ist keine Mutation. Gezählt waren Prozesse. Die Zahl war drei Wochen falsch, und niemand konnte es sehen — genau der Fall, den 23a („die Zahl muss wahr sein als Aussage, nicht als Anzahl") und eure Frage (3) aus 24b meinten. Damit ist Frage (3) aus 24b beantwortet: **Namen ins Register.**

> **Berichtigung zu 12 (Ersatztext für den Halbsatz „davon acht Mutationsproben"):** … davon **sieben Mutationsproben, H1 bis H7** (Teil H); H0 ist der Grundlauf ohne Mutation und keine Probe. F4 ist keine Mutationsprobe (ändert keinen Code), hat aber nach 40.7 eine Gegenprobe. Die Zahl der Prüfungen ist eine Tatsachennotiz mit Stand (heute 188, Commit …), kein Registertext; die **Namen** der Mutationsproben sind Registertext. Ändert sich die Menge, ist das eine Berichtigung mit Namen.
>
> **Berichtigung zu 40.7:** „alle acht" lies „alle sieben (H1–H7)".

*Quelle des Grundes:* 23a (Kopien altern; eine Zahl ohne Namen ist eine Kopie des Codes im Register). Kein Ergebnis.

### B3. Frage (3) — H6 trägt nur mit H5

Eine Probe, deren Gegenprobe nur deshalb scheitert, weil eine **andere** Mutation stehen bleibt, ist keine unabhängige Wache — ihr sagt es richtig.

> **Regel (Ergänzung zu 12/40.7):** Jede Mutationsprobe beisst **allein**: Ihre Gegenprobe (nur ihre eigene Mutation weggelassen, alles andere im Grundzustand) scheitert. Eine Probe, die das nur im Verbund mit einer anderen leistet, wird vor dem Tag **eigenständig** gemacht — H6 braucht einen eigenen eingesetzten Fehler, den die entfernte Wache hätte fangen müssen, statt sich H5s Fehler zu leihen. Ist das strukturell nicht möglich, wird das Paar als **eine** Probe mit zwei Mutationen registriert und gezählt — sechs plus ein Paar, nicht sieben.

*Grund:* A8 und 12. Eine Zählung, die ein Paar als zwei führt, ist dieselbe Unwahrheit wie „acht", nur kleiner. Kein Ergebnis.

### B4. Frage (2) — Befund 2: angenommen, mein Beispiel war falsch

„Z. B. die zweite Selektionsfalte" hätte bei zwei Bots die Beispieldaten in jeder Zelle unzulässig gemacht — ihr habt es gemessen, ich hatte es geraten. **Zurückgenommen.** Die Regel, die ich meinte, war: Literal weg, Quelle ist das Register; ihr habt die richtige Registerstelle gefunden (5.1 Nr. 4 über die Abdeckung, wie G6). Das ist meine Regel in richtiger Anwendung, und mein Beispiel war eine Tatsache über den Bestand, die ich nicht gemessen hatte — **Fall fünf** (siehe C1).

**Marke bei 5.1 Nr. 4:** ja, um den zweiten Leser ergänzen. Und: zwei Leser, **ein Parser** — die Funktion, die 5.1 Nr. 4 liest, ist eine, und beide rufen sie; sonst altern zwei Parser getrennt. Handwerk, aber die Anforderung ist Verfahren (ein Wert, ein Ort).

### B5. Frage (4) — ein Abbild nach TB-98

**Ein Abbild, nach dem nächsten Bündel** — 22g gilt. Bis dahin melden die Gruppen 2 („nicht im Abbild"), nicht 1; das ist der ehrliche Zustand, und er ist benannt (39.9, jetzt in der Ausgabe). **Aber:** TB-98 ist durch 24d blockiert, und die Reihenfolge ist jetzt Resolver → Trockenlauf aller neun → Erzeuger (Signalpfad) → Listen → Faltenlänge gegen 33.2 → Abbild. Zieht sich das über den nächsten Registerauftrag hinaus, kommt das Abbild mit diesem — kein Abbild nach jeder Änderung, aber auch keines, das zwei Registerabschnitte hinterherhinkt.

**Zu Befund 3 (Abbild führt die Gruppen nicht):** richtig gemeldet, richtig nicht gezogen. Der Erzeuger liest `eingefroren` per AST aus `herkunft.py`, ohne es auszuführen oder zu ändern — das ist die Bauart, die 22d verlangt hat. Und dass die Regelzeile jetzt für alle zwölf Punkte „keine Tatsachennotiz im Abbild" zeigt, ist die Tag-Vorbedingung aus 22d in Sichtweite statt im Kopf: Bis zum Tag hat jede dieser zwölf 2 eine Notiz **im Abbild** (Verweis auf die Registerstelle), sonst ist sie nicht erfüllt.

---

## C. 24b — der vierte Fall, der Satz, die Namen, `beispieldaten.py`

### C1. Frage (1) — der vierte Fall: angenommen, und jetzt berichtigen, nicht warten

Mein Satz „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren" war falsch: TB-90 B6 verglich die Backtest-Skripte vor/nach dem Kostenmodul auf `data/`, nicht den Erzeuger der Listen, nicht im Modus. Die Regel trägt trotzdem, weil sie ihren eigenen Nachweis verlangt — aber der Satz ist eine Behauptung über den Bestand, und sie stimmt nicht. **Berichtigung jetzt**, nicht als Vorlage bis TB-98: Zwei Dinge sind zu trennen — die falsche Behauptung (heute berichtigbar, weil gemessen) und der fehlende Nachweis (TB-98 oder Nachfolger). Eine Notiz, die sagt „steht noch aus", lässt einen falschen Satz stehen, bis etwas anderes passiert; das ist die Zweideutigkeit aus 38.4 in neuer Form.

> **Berichtigung zu 40.6:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren" lies „Der Reproduzierbarkeitsnachweis für die Listen-Erzeugung ist der Modus-Lauf nach 23e (zweimal, bytegleich) und stand am 24.09. noch aus; TB-90 B6 betraf die Backtest-Skripte auf `data/`, nicht den Listen-Erzeuger."

**Zählung:** Das ist Fall vier; B4 oben ist Fall fünf (zweite Selektionsfalte). Beide dieselbe Klasse. Ich schreibe die Regel aus 21m schärfer, weil sie offensichtlich nicht reicht, wenn ich Beispiele oder Belege nenne:

> **Regel an mich, geschärft:** Jede Aussage über den Bestand in meinen Texten — auch in Beispielen („z. B."), auch in Belegverweisen („TB-90 hat gezeigt") — wird als **[Voraussetzung, zu messen]** gekennzeichnet, wenn ich sie nicht aus einer vorgelegten Messung habe. Ein Beispiel, das ich nicht gemessen habe, ist keine Illustration, sondern eine Behauptung.

### C2. Frage (2) — der Satz der Sitzung: Registertext, mit Herkunft

> **Registertext, Ergänzung zu 12 (Gegenproben) — Störproben:** Eine Störprobe nach „geht es ein?" wird in **beide** Richtungen geführt: klein genug, dass nichts passieren darf, und gross genug, dass etwas passieren muss. Eine Störprobe nur in eine Richtung belegt nichts. *(Formuliert von TB-95 am 23.09.2026, übernommen als Registertext durch den Verfahrensprüfer, 24.09.2026.)*

Der Satz ist besser als meiner, und F17 fragt nach dem Grund, nicht nach dem Autor; die Herkunft steht dabei, weil sie stimmt. *Grund:* die Störprobe zur Faltenlänge — eine Zeile weg hätte allein das falsche „nein" ergeben; F4 ist derselbe Fehler in einer Prüfung. Kein Ergebnis.

### C3. Frage (3) — beantwortet durch 24c (B2): Namen ins Register.

### C4. Frage (4) — `beispieldaten.py`: Werkzeug, mit eigener Notiz

Es ist keine Prüfung, sondern der Testrahmen (12: „erzeugte Beispieldaten mit frei erfundenen Werten"). Literale dort sind kein Prüffehler, aber ein **Befund am Testrahmen**: Ein Rahmen, der bei Doppeljahren entartet (Z. 77) oder nie trifft (Z. 69), prüft den Auswerter nur für Bots mit Einjahresfalten — und `elliott_wave` hat Doppeljahre. Eigene Tatsachennotiz (zu 12): der Testrahmen deckt seit 24c beide Faltenlängen ab; vorher nicht. Die Umstellung selbst ist nach 24c geschehen (5.1 Nr. 4 über Abdeckung) und angenommen.

**Zur Marke „23d-Abschnitt":** richtig gesetzt an 39.6 — 23d ist eine Antwortdatei, kein Abschnitt; der Auftrag hatte meinen Dateinamen für ein Aktenzeichen genommen. Dieselbe Verwechslung wie in 22f, umgekehrt.

---

## D. Was daraus auf den Plan kommt, in Reihenfolge

1. **Resolver:** `CONFIG_DIR` unter dem Modus → `<snapshot>/config/`; Regel „kein Fallback unter dem Modus" mit Rückgabe 2; Ladeprotokoll mit beiden Zahlen (A2). Freigabe: `paths.py`, kein Sperrlistenpunkt.
2. **Trockenlauf aller neun im Modus** mit Lesehaken — neue Tag-Vorbedingung (A2). Erst danach irgendein Lauf, der etwas erzeugt.
3. **Listen-Erzeuger auf dem Signalpfad** (A3): Feldliste registrieren, Erzeuger unter 36.1, Modus-Lauf zweimal bytegleich; Sperrlistenpunkt; `faltenplan.py` und `faltenplan_neun.py` auf **eine** Konstante (A4); Faltenlänge nach 5.4 gegen 33.2.
4. **Abbild** nach diesem Bündel (B5), mit Notizen zu den zwölf 2.
5. **Register 41:** Berichtigung 12 (sieben, Namen, F4), 40.7 („sieben"), 40.6 (TB-90-Satz), Regel „allein beissen" und H6, Störproben-Satz, Marke 5.1 Nr. 4, Testrahmen-Notiz, Tatsachennotiz `bot_lauf.py`/`symbol`, Regel „keine Kennzeichnung in Laufcode-Feldern".
6. **H6 eigenständig** oder als Paar registriert (B3), vor dem Tag.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 24a; dazu ANFRAGE 24b (Anhang), 24c, 24d. `belege/` nicht gelesen. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…98`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** 24d: Resolver setzt `CONFIG_DIR` auf `<snapshot>/config/`; **unter dem Modus gibt es keinen Fallback** — nicht gefunden ist 2 und Abbruch, „Keines ausgelassen" nur bei Gleichheit mit der Universumsdatei; neue Tag-Vorbedingung: Trockenlauf aller neun im Modus mit Lesehaken. Die Listen brauchen die Simulation nicht: 5.4 zählt gefundene Trades, der Erzeuger läuft auf dem Signalpfad, kein `ausgefuehrt`, keine Kennung im Symbol, Format als Feldliste registriert, Vergleich Faltenlänge gegen 33.2 statt Liste gegen Liste. 24c: sieben Mutationsproben H1–H7 mit Namen ins Register, F4 keine, H0 Grundlauf; H6 muss allein beissen oder wird als Paar gezählt; mein „zweite Selektionsfalte" war falsch, eure Registerstelle ist richtig, Marke um zweiten Leser ergänzen, ein Parser; ein Abbild nach dem nächsten Bündel. 24b: vierter Fall angenommen und **jetzt** berichtigt, nicht als Vorlage; der Störproben-Satz wird Registertext mit Herkunft TB-95; `beispieldaten.py` ist Werkzeug mit eigener Notiz. Fünf eigene Fehler dieser Klasse; die Regel an mich ist geschärft: auch Beispiele und Belegverweise sind Voraussetzungen, wenn ich sie nicht gemessen habe.

**Unsicher:** ob 5.4 „gefundene" Trades im Wortlaut sagt oder das aus dem Funktionsnamen `gefundene_trades_je_jahr` stammt — wenn der Registertext „Trades" ohne Zusatz sagt, gehört das Wort „gefundene" als Präzisierung hinein, bevor der Erzeuger gebaut wird; sonst rechnet er auf einer Lesart.

---

## In einfacher Sprache

Der wichtigste Fund: Wird ein Bot im geschützten Modus gestartet, findet er seine Symbolliste nicht und nimmt still eine eingebaute Notliste von fünf Werten — und meldet dabei „nichts ausgelassen". Das wird an einer zentralen Stelle behoben, und es wird zur Regel: Im geschützten Modus gibt es keine Notlisten, eine fehlende Eingabe ist ein Abbruch. Ausserdem muss vor dem Stichtag jeder Bot einmal in diesem Modus probeweise laufen, mit Protokoll, was er liest — bisher hat das nie jemand getan. Zweitens braucht die Neu-Erzeugung der Handelslisten die Simulation gar nicht: Für die Abschnittslänge zählen nur die gefundenen Signale, nicht die ausgeführten; das Programm dafür wird entsprechend einfacher und der Konflikt mit der geschützten Zuteilung entsteht nicht. Drittens: Das Regelwerk sagt „acht Proben", es sind sieben — künftig stehen die Namen im Regelwerk, nicht die Zahl; eine Probe, die nur zusammen mit einer anderen anschlägt, wird eigenständig gemacht oder ehrlich als Paar gezählt. Und Fable hat zwei weitere eigene Behauptungen zurückgenommen, die er nicht gemessen hatte — ein Beispiel und einen Belegverweis — und seine Regel dafür verschärft.
