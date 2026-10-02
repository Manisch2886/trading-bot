# REGISTER-KOPIE Abschnitt 36 (von 0–51) — Register-Z. 6516–6866 — Commit f63ad4cbd1230427305a24ac3d7467b83f088fd2 — 2026-10-02 — Original sha256 7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4 — KOPIE, nicht das Register

## 36. Die Schreibregel für Sperrlistenpfade, die Sperrlisten-Sonde mit drei Ausgängen, das Abbild der Sperrliste als neue Datei und die Reihenfolge der Handwerksschritte — und eine Tatsachennotiz zur ⚠️-Markierung in 21.4 (Fable 22b und 22c, TB-84, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 und 35. Sechs Einträge — vier
Ersteinträge (36.1, 36.2, 36.5, 36.6), eine Reihenfolge (36.3) und eine
Tatsachennotiz (36.4) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`
(Antwort auf die Anfrage 22a des steuernden Chats, die Sperrlistenfalle:
`faltenplan.py main()` schreibt nach `ergebnisse/faltenplan.json`,
Sperrlistenpunkt 2) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22c_drei_ausgaenge_und_abbild.md`
(Antwort auf die Anfrage 22b, Frage 1 und 2; **berichtigt einen Satz aus 22b
am selben Tag**, 36.5). Auftrag `docs/auftraege/MAC_TB-84_register_36.md`
(erweitert um 36.5 und 36.6, bevor Abschnitt 36 eingetragen war); Messungen
`docs/belege/TB-84/` (M1–M6), alle **vor** dem Eintrag gemessen, HEAD `4bbd720`.
⛔ **Kein Code, keine Sonde, kein Umbau von `main()`, kein Aufruf von
`faltenplan.py`, keine Abbild-Datei, kein Hash, keine Freigabe** — 36.7.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Sperrliste
Punkt 2, Überschrift von Abschnitt 10, 35.1, 21.4 — und für die Berichtigung
aus 36.5 an den zwei Sätzen in 36.1 und 36.2, die sie berichtigt). Die alten
Sätze bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für
TB-84 in der zweiten Spalte `0`.

⚠️ **Was dieser Abschnitt ist:** Er schliesst die Lücke, die die Anfrage 22a
gemessen hat — *Fable, 22b Abschnitt 2, zeichengleich:* *„Was ihr gemessen habt, ist nicht ein Fehler in `faltenplan.py`, sondern **das Fehlen einer Regel**: Nirgends steht, dass ein Programm eine gesperrte Datei nicht schreiben darf. Die Sperrliste sagt, *was* unverändert bleiben muss; sie sagt nicht, *wer* es sicherstellt. Acht Tage lang war das der Zufall."* Die Regel steht ab hier
(36.1); wer sie ausführt, steht ebenfalls (36.2), mit welchen Ausgängen (36.5)
und gegen welches Abbild (36.6); und in welcher Reihenfolge das Handwerk folgt,
steht in 36.3. ⚠️ **Gebaut ist davon nichts** — die Freigabe des Betreibers
für die vier Handwerksschritte steht aus (36.3, 36.7), und bei Fable stehen
eine Tatsachennotiz und eine Frage aus (36.6).

### 36.1 Schreibregel für Sperrlistenpfade — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Schreibregel für Sperrlistenpfade:**
> **(1)** Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist. **(2)** Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt. **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.
>
> > ⚠️ **Präzisiert durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „bricht er ab (Rückgabewert ≠ 0)" in (2) — der Wert ist **1**: der Erzeuger hat geprüft und einen Befund („Ziel existiert, Hash …"), nicht 2. Der Satz oben bleibt zeichengleich stehen.

**Fables Abwägung der drei Wege aus der Anfrage 22a, zeichengleich:**

> **Zu den drei Wegen:** (c) fällt nach A8 — eine Regel, die niemand ausführt, ist keine Wache; ihr sagt es selbst. (a) allein beseitigt den Fall, nicht die Klasse: Der neue Zielname landet, sobald er Abbild ist, selbst auf der Sperrliste — und `main()` überschreibt ihn beim nächsten Aufruf genauso. (b) allein lässt ein Programm stehen, dessen **Voreinstellung** eine gesperrte Datei ist, mit einer Sicherung davor; die Sicherung muss dann die Sperrliste kennen, und das ist ein zweiter Ort, an dem die Sperrliste steht.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste („nichts Gesperrtes ist bewegt worden", Übergabe Abschnitt 5) und A8 (eine Wache ist, was jemand ausführt). Die Einmal-Schreibsperre braucht keine Sperrlistenkenntnis — sie schützt auch die Abbild-Datei, die noch nicht auf der Liste steht, und sie schützt gegen den Fall, den niemand vorausgesehen hat. 21b (3): Prüfungen wandern dorthin, wo geändert werden darf. Kein Ergebnis: Kein Inhalt einer Datei ist berührt; es geht darum, dass keiner berührt werden kann.

**Und sein Satz zur Härte der Sperre, zeichengleich:**

> *Warum „nie überschreiben, auch nicht mit identischem Inhalt":* Eine Sperre, die bei gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich programmiert, entscheidet, was „gleich" heisst (Schlüsselreihenfolge, Zeilenende, `sort_keys`). Die Sperre ist stärker, wenn sie dümmer ist.

⭐ **Fables Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz dazu:** `ergebnisse/faltenplan.json` (Hash `0e54ac5c…`) ist seit dem 14.09. unverändert, obwohl `faltenplan.py main()` seit demselben Tag bei jedem Aufruf dorthin schreibt; TB-72 und TB-80 haben eigene Belegskripte verwendet. Der Bestand hielt durch Übung, nicht durch Regel. Der Hash ist am 22.09. gemessen und stimmt.

**Tatsachennotiz (TB-84, gemessen vor dem Eintrag, `m2_sperrlisten_hash.txt`
— Fables Notiz wird nicht übernommen, sondern nachgemessen):**
`research/vorregistrierung/ergebnisse/faltenplan.json` hat SHA-256
`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`, mtime
14.09.2026 17:55, letzter berührender Commit `a2fcf01` (TB-30a, 14.09.2026) —
**keine** Änderung seit dem Ersteintrag, obwohl `faltenplan.py` selbst seither
geändert wurde (letzter Commit `76c20ec`, 21.09.2026, TB-80). Die Schreibstelle
in `main()` ist, nur gelesen: Z. 372 `ziel = os.path.join(_HIER, "ergebnisse",
"faltenplan.json")`, Z. 373 `with open(ziel, "w", …)`, Z. 374 `json.dump(…)` —
Voreinstellung ohne Argument, ohne Abfrage, ob die Datei besteht: genau der
Fall, den (2), (3) und (4) ausschliessen. Der Hash ist **nach** dem Eintrag
erneut gemessen und gleich (36.7). ⇒ Fables Notiz stimmt in jedem Wort: *Der
Bestand hielt durch Übung, nicht durch Regel.*

⚠️ **Was (4) heute bedeutet, ausdrücklich:** Die in 35.1 eingetragene
Umstellung von `faltenplan.py:336` auf den Bezeichner `JJJJ-MM-TT/JJJJ-MM-TT`
darf nach (4) **erst nach** der Voreinstellungs-Änderung und der
Einmal-Schreibsperre in `main()` kommen — das ist Schritt 3 nach Schritt 2 in
36.3. Bis dahin gilt weiter: `python3 faltenplan.py` wird nicht aufgerufen.

**Marke am alten Ort:** unter **Sperrliste Punkt 2** (Abschnitt 10), als
eingerückter Block **unter** der Tatsachennotiz aus Abschnitt 30 — diese bleibt
zeichengleich stehen. Dazu die Marke aus 36.5 direkt unter dem Registertext
oben, am „(Rückgabewert ≠ 0)" in (2).

### 36.2 Die Sperrlisten-Sonde — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Sperrlisten-Sonde:**
> Vor dem signierten Tag existiert ein Prüfskript, das für **jeden** Sperrlistenpunkt Pfad und Hash gegen den Registertext prüft und bei einer Abweichung mit Rückgabewert ≠ 0 endet und den Punkt nennt. Der Registertext der Sperrliste ist die Quelle; eine maschinenlesbare Fassung ist Abbild und wird von der Sonde selbst gegen den Registertext geprüft (Bauart 33.3). Die Sonde läuft (a) als Nachweis vor dem Tag, (b) im Laufwrapper vor `auswertung.py`, (c) am Ende jedes Auftrags, der Sperrlisten-nahen Code berührt. Ein Sperrlistenbruch, den die Sonde findet, ist eine Tatsachennotiz — nie eine stille Reparatur.
>
> > ⚠️ **Berichtigt durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn". Der Satz oben bleibt zeichengleich stehen; die drei Ausgänge gelten nach 36.5 für jede Sonde und jede Wache.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „bei einer Abweichung … endet" — **was ein Befund bedeutet, hängt vom Tag ab.** Vor dem signierten Tag ist ein Befund `1` zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein neues Abbild unter neuem Namen geschlossen; **nach** dem Tag ist er ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Der Satz oben bleibt zeichengleich stehen.

**Fables Unsicherheit dazu, 22b, zeichengleich:**

> **Unsicher:** ob es bereits ein Prüfskript für die Sperrliste gibt (etwa nach dem Muster `snapshot.py --pruefen`) — dann ist Schritt 1 eine Erweiterung, kein Neubau; ihr seht es im Repo.

⭐⭐ **Drei Tatsachennotizen des steuernden Chats (Anfrage 22b, 22.09.2026,
07:35), von TB-84 vor dem Eintrag nachgemessen (M3–M5, `m3_snapshot_ausgaenge.txt`,
`m4_herkunft_listen.txt`, `m5_vt_in_listen.txt`, HEAD `4bbd720`).** Sie waren
Fable mit `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md`
vorgelegt; seine Antwort (22c) liegt vor und ist in 36.5 und 36.6 eingetragen:

> **(a) Das Muster existiert, die Sache nicht.** `shared/snapshot.py --pruefen`
> (1306 Zeilen) prüft **Datenstände**, nicht die Sperrliste, und hat **drei**
> Ausgänge — gemessen im Kopf der Datei, Z. 217–219: `0` *„in Ordnung: gezogen,
> oder `--pruefen` findet den Stand unveraendert"*, `1` *„Befund: `--pruefen`
> findet den Snapshot VERAENDERT"*, **`2` *„NICHT PRUEFBAR / abgebrochen"***.
> Begründung ebendort (Z. 221–224), wörtlich: *„Die 2 ist der Grund, warum es
> sie gibt. In TB-45 haben zwei Wachen "bestanden" gemeldet, ohne etwas gemessen
> zu haben - ein gescheiterter Aufruf und ein leeres Ergebnis sahen gleich aus.
> Hier nicht: wer nicht messen konnte, sagt es mit einem eigenen Wert."*
> ⚠️ Der Registertext oben sagt nur „Rückgabewert ≠ 0" und unterscheidet die
> beiden roten Fälle nicht — nach `A2` („konnte nicht messen" ist ein eigenes
> Ergebnis, nicht grün und nicht rot) und `A8` sind sie verschieden.
> **Frage 1 an Fable** (drei Ausgänge?) — ⭐ **beantwortet: ja, in 36.5.**
>
> **(b) `herkunft.py` scheidet als Ort aus.** `research/vorregistrierung/herkunft.py`
> (260 Zeilen): sein `--pruefen` meldet die vier Verankerungen (append-only-Kette,
> GPG, OpenTimestamps), nicht Sperrlisten-Hashes — **und die Datei steht selbst
> auf der Sperrliste** (Punkte **11** `herkunft.py::register()` und **12**
> `herkunft.py::datenstand()`, gemessen M1: 14 Punkte in Abschnitt 10). Die
> Sonde kann dort nicht eingebaut werden, ohne gesperrten Code zu öffnen; sie
> braucht eine **eigene Datei**. ⇒ Schritt 1 in 36.3 ist ein **Neubau nach
> vorhandenem Muster**, keine Erweiterung. ⭐ Fable 22c, Abschnitt 0: *„angenommen, und es bestätigt die Bauart aus 22b (Sonde als eigene, nicht gesperrte Datei)"*.
>
> **(c) ⚠️ Zwei maschinenlesbare Listen liegen bereits in `herkunft.py`** und
> decken sich **nicht** mit dem Registertext: `EINGEFROREN` (Z. 57, **zehn**
> Einträge: `registerdaten.py`, `faltenplan.py`, `benchmark.py`, `kennzahlen.py`,
> `auswertung.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`, `ergebnisse/faltenplan.json`,
> `ergebnisse/benchmark_drawdowns.json`) und `SPERRLISTE_DATEIEN` (Z. 66,
> **fünf** Muster: `shared/messkette.py`, `shared/zuteilung.py`,
> `strategies/*/equity_simulation.py`, `strategies/*/multi_symbol_optimise.py`,
> `strategies/*/multi_symbol_walk_forward.py`) gegen **14** Registerpunkte (M1).
> Gemessen (M5, 0 Treffer, Positivkontrolle `faltenplan.json` 1 Treffer):
> `ergebnisse/benchmark_drawdowns_vt.json` (Sperrlisten-Hash `4549395f…`) steht
> in **keiner** der beiden Listen, ebenso wenig die beiden Universumsdateien aus
> Punkt 8 (`config/top25_symbols.txt`, `config/sp500_top150.txt`); umgekehrt
> führt `EINGEFROREN` Dateien, die der Registertext nicht als eigene Punkte nennt
> (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`). ⛔ **Nicht bewertet** — ob `EINGEFROREN`
> überhaupt als Sperrlisten-Abbild gemeint war oder für Abschnitt 0 („vor dem
> Lauf geschrieben und eingefroren"), steht nirgends. Genau der Zustand, gegen
> den die Sonde nach 36.2 schützen soll — eine maschinenlesbare Fassung, die vom
> Registertext abweicht und nie dagegen geprüft wurde —, besteht damit heute
> schon. **Frage 2 an Fable** (welche Liste wird Abbild?) — ⭐ **beantwortet:
> keine, in 36.6**; die Tatsachennotiz zu den beiden Listen steht bei Fable aus.

⭐ Die Antwort auf Fables Unsicherheit lautet damit, gemessen: **Das Muster
gibt es, die Sache nicht.** Die Sonde selbst ist Schritt 1 in 36.3 und
**nicht** freigegeben.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, als
Hinweisblock, zusammen mit der Marke aus 36.6.

### 36.3 Die Reihenfolge der Handwerksschritte

**Fable, 22b Abschnitt 3, zeichengleich — Vorsatz und die vier Schritte:**

> Alle mit Betreiberfreigabe; die Reihenfolge ist Verfahren, weil jeder Schritt den nächsten absichert:
>
> 1. **Sperrlisten-Sonde** schreiben und einmal laufen lassen — Nachweis, dass heute alles stimmt (der Nullpunkt).
> 2. **`faltenplan.py main()`:** Voreinstellung ändern, Einmal-Schreibsperre einbauen. **Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün.
> 3. **Erst jetzt** Z. 336 (Bezeichner der Bestätigungsperiode, 22a). Prüfen über `main()` ist ab jetzt ungefährlich; Sonde danach → grün.
> 4. Abbild-Datei, Faltenplan-Sonde (33.3), Hash auf die Sperrliste — wie geplant; der Erzeuger des Abbilds unterliegt der Schreibregel von Anfang an.

**Fables Satz dazu, zeichengleich:**

> Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt. Deshalb steht die Reihenfolge hier und nicht nur im Auftrag.

⛔ **Eingetragen, ausdrücklich:** Alle vier Schritte brauchen
**Betreiberfreigabe**. Am 22.09.2026, 07:40 (Erstellung des Auftrags TB-84)
ist **keine** erteilt; TB-84 hat keine erhalten und keinen der vier Schritte
begonnen (36.7). Die Reihenfolge ist **Verfahren**, nicht Empfehlung: Schritt 3
(Z. 336, 35.1) ist ohne Schritt 2 genau die in Anfrage 22a gemessene Falle, und
Schritt 2 ohne Schritt 1 hat keinen Nullpunkt, gegen den seine Mutationsprobe
gemessen würde. Der Erzeuger der Abbild-Datei (Schritt 4, 33.3/35.2)
unterliegt der Schreibregel 36.1 von seinem ersten Aufruf an; seine Ausgänge
regelt 36.5, das Abbild der Sperrliste 36.6.

**Marke am alten Ort:** in **35.1**, direkt beim Absatz über den heutigen
unzulässigen Bezeichner (*„Die Umstellung ist Handwerk mit eigener Freigabe"*)
— Verweis, dass die Umstellung nach 36.3 erst nach Schritt 2 kommt.

### 36.4 Tatsachennotiz zu 21.4 — die ⚠️-Markierung ohne Erklärung

**Fable, 22b Abschnitt 1 (Kenntnisnahme zu Punkt 1 der Anfrage 22a),
zeichengleich:**

> Die ⚠️-Markierung in 21.4 hat keinen Text. Dann ist sie eine Markierung ohne Bedeutung, und das gehört als Tatsachennotiz zu 21.4: „⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht als Beleg verwendbar." Sonst nimmt sie in einem Jahr jemand für einen Vorbehalt, den es nie gab.

**Tatsachennotiz zu 21.4 (TB-84, 22.09.2026; Messung `m1_bestaetigung_ab.txt`
aus TB-83, unverändert):** Die Zelle bei `elliott_wave` in der Spalte
„Bestätigung ab" lautet wörtlich `⚠️ **2026-01-01**`; 21.4 trägt keinen Satz,
der die Markierung begründet, und kein anderer Abschnitt des Registers
erklärt sie. **⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine
Erklärung; nicht als Beleg verwendbar.**

⭐ **Rücknahme des steuernden Chats, eingetragen:** Die Deutung aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 3 — zeichengleich: **(Möglicherweise ist das der Grund für die ⚠️-Markierung, die 21.4 ausgerechnet bei `elliott_wave` in der Spalte „Bestätigung ab" trägt.)** — ist **zurückgezogen.** Sie war eine
Vermutung und taugt nicht als Beleg; Fable hatte in 22a ausdrücklich gebeten,
den ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (35.1). Die
Tabellenzeile in 21.4 bleibt zeichengleich stehen, **samt `⚠️`** — die
Markierung wird nicht entfernt, sondern erklärt: sie erklärt nichts.

**Marke am alten Ort:** ⚠️ **direkt in 21.4**, als Zeile unter der Tabelle —
die Tabellenzeile selbst bleibt zeichengleich, samt `⚠️`.

### 36.5 ⭐⭐ Drei Ausgänge für jede Sonde und jede Wache — Ersteintrag, und die Berichtigung zu 36.2

⚠️ **Fable berichtigt hier seinen eigenen Text aus 22b (36.2), nachdem ihm
`shared/snapshot.py` vorgelegt war (Anfrage 22b, Frage 1; Messung M3).**
*Seine Begründung, 22c Frage 1, zeichengleich:*

> Mein „Rückgabewert ≠ 0" war zu grob, und der Kopf von `snapshot.py` sagt genau, warum: Ein gescheiterter Aufruf und ein Befund sahen in TB-45 gleich aus. A2 verlangt, dass „konnte nicht messen" ein eigenes Ergebnis ist; ein Rückgabewert, der Befund und Nichtprüfbarkeit zusammenlegt, ist keine Wache im Sinn von A8, weil niemand am Wert erkennen kann, ob gemessen wurde.

**Fable, 22c Frage 1, zeichengleich — Registertext und Berichtigung:**

> **Registertext, Ersteintrag — Ausgänge von Sonden und Wachen:**
> Jede Sonde und jede Wache des Verfahrens (Sperrlisten-Sonde, Faltenplan-Sonde nach 33.3, Einmal-Schreibsperre der Erzeuger, Wache nach 29.4, Laufwrapper) endet mit genau einem von drei Rückgabewerten, Bauart `snapshot.py --pruefen`: **0** = geprüft und in Ordnung; **1** = geprüft und **Befund** (Abweichung, Verweigerung, Abbruch nach Regel); **2** = **nicht prüfbar** (Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert). Ein Wrapper behandelt 1 und 2 verschieden: 1 ist eine Tatsachennotiz mit dem genannten Punkt; 2 ist kein Ergebnis und darf nirgends als „bestanden" oder „nicht bestanden" geführt werden. Kein Aufruf endet mit 0, ohne dass gemessen wurde.
>
> **Berichtigung zu 22b, Sperrlisten-Sonde:** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn".
>
> > ⚠️ **Präzisiert durch 37.1 (Fable 22d, TB-87, 22.09.2026):** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil** — für jeden genannten Pfad 0 oder 1, für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts; der Punkt ist 1, wenn ein Bestandteil 1 ist, sonst 2, wenn einer 2 ist, sonst 0. Am Tag: kein Pfad-Bestandteil mit 1, jede 2 mit Tatsachennotiz. Der Text oben bleibt zeichengleich stehen.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 und A8, im Register vorhanden; der Vorfall TB-45, im Kopf von `snapshot.py` dokumentiert. Kein Ergebnis.

**Und sein Zusatz zur Einmal-Schreibsperre (36.1 (2)), zeichengleich:**

> *Zur Einmal-Schreibsperre:* Der Erzeuger, der wegen vorhandener Zieldatei nicht schreibt, endet mit **1** — er hat geprüft und einen Befund („Ziel existiert, Hash …"). Nicht mit 2: Er konnte prüfen. Das ist die Wache, die ihre Arbeit tut; der Wert 1 sagt es dem Aufrufer.

**Tatsachennotiz (TB-84, M3, `m3_snapshot_ausgaenge.txt`):** Die Bauart, auf
die der Registertext verweist, ist im Kopf von `shared/snapshot.py` Z. 217–219
(`0` in Ordnung · `1` Befund · `2` NICHT PRUEFBAR / abgebrochen) mit der
Begründung Z. 221–224 (TB-45: *„wer nicht messen konnte, sagt es mit einem
eigenen Wert"*) — gemessen, nur gelesen. Der Registertext dehnt sie auf **jede**
Sonde und Wache des Verfahrens aus; keine davon ist gebaut (36.7).

**Marken am alten Ort — zwei, beide in diesem Abschnitt:** in **36.2**, direkt
unter dem Registertext, am Satz *„mit Rückgabewert ≠ 0 endet und den Punkt
nennt"* — **berichtigt durch 36.5**, der Satz bleibt zeichengleich stehen; und
in **36.1**, direkt unter dem Registertext, am *„bricht er ab (Rückgabewert
≠ 0)"* in (2) — dasselbe, der Wert ist **1**.

> ⭐ **Wofür die drei Ausgänge gelten, und was seitdem mit 2 endet (42.1 D8/D12,
> 42.2 E5, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Die drei Ausgänge
> gelten mit „kein Fallback" und der Resolver-Pflicht für den **Laufbereich** —
> die Vereinigung aller registrierten Lauf-Typen, gemessen am Tag-Commit
> (**42.2, E5**). In TB-105 bis TB-107 sind Stellen, die still weiterrechneten
> oder mit 0 endeten, auf 2 umgestellt: unter dem Modus „Keine Daten gefunden"
> (14 Stellen) und eine leere Symbolliste; die stillen Ersatzwerte in
> `faltenplan.py`, `benchmark.py`, `auswertung.py` und `faltenplan_neun.py`;
> `_min_history` bei Fehltreffer (**42.1 D12, 42.3 F4**). Ob
> `auswertung.Abbruch` mit 1 statt 2 endet, ist offen (25d (4), 42.4 G5). Der
> Text oben bleibt zeichengleich.

> ⭐⭐ **Ergänzungen zu 36.5 — Ausgänge von `auswertung.py` und null Trades
> (43.1, 43-1; 43.2, 43-7; Fable 25d/25e, TB-110, 26.09.2026):** Die offene
> Frage in der Marke darüber ist beantwortet: `auswertung.py` endet mit 0 oder
> **2**, nie mit 1 (**43-1**; vollzogen erst mit der nächsten Öffnung von
> `auswertung.py`). Und: ein Lauf des Laufbereichs, der keine Trades findet,
> schreibt dieses Ergebnis und endet mit 0; unter dem Modus endet ein `exit()`
> ohne geschriebenes Ergebnis mit 2 (**43-7**; zehn weitere Stellen in TB-109,
> Gegenprobe über 24). Beide Texte oben bleiben zeichengleich.

> ⭐ **`Abbruch` endet mit 2 seit TB-111, siehe 44.1 (44-1; TB-113,
> 26.09.2026):** Vollzogen in `6c98c38` (Zweig `tb-111`, zusammengeführt in
> `257e7db`): `auswertung.py` endet mit 0 oder 2; die zwölf Stellen und die
> Meldung sind zeichengleich. Die Texte oben bleiben zeichengleich.

> ⭐ **Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9** (Fable
> 27a R14, TB-117, 26.09.2026). Die Texte und die Marken oben bleiben
> zeichengleich.

### 36.6 Das Abbild der Sperrliste ist eine neue Datei — Ersteintrag

**Fable, 22c Frage 2, zeichengleich:**

> **Registertext, Ersteintrag — Abbild der Sperrliste:**
> Das Abbild der Sperrliste ist eine **eigene, neue Datei** (Handwerk: Name, Form), die genau die Punkte des Registerabschnitts 10 mit Pfad und Hash trägt — nicht mehr, nicht weniger (Bauart 33.3). Sie wird einmalig geschrieben (Schreibregel 22b); jede Fortschreibung der Sperrliste vor dem Tag erzeugt ein neues Abbild unter neuem Namen, das alte bleibt. Das aktuelle Abbild steht selbst mit Hash im Register. Die Sperrlisten-Sonde prüft (i) jeden Punkt des Abbilds gegen die Datei im Repo und (ii) das Abbild gegen den Registertext von Abschnitt 10; weicht das Abbild vom Registertext ab, ist das ein Befund (1), kein Anlass zur Anpassung des Abbilds ohne Registereintrag.
>
> `herkunft.py` `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das Abbild der Sperrliste und werden nicht dazu. Beide erhalten eine Tatsachennotiz zu Abschnitt 10: Was sie sind, wer sie liest, was daraus entsteht, und dass sie mit dem Registertext an fünf Stellen nicht übereinstimmen (zwei Dateien fehlen, drei stehen zusätzlich).
>
> > ⚠️ **Ergänzt durch 37.2 (Fable 22d, TB-87, 22.09.2026):** Das Abbild führt **zwei Gruppen** — die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade (heute `ergebnisse/benchmark_drawdowns_vt.json`); die Sonde prüft beide gleich und weist die Gruppe aus; am Tag ist die zweite Gruppe leer. Der Satz oben bleibt zeichengleich stehen.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „jede Fortschreibung … erzeugt ein neues Abbild unter neuem Namen, das alte bleibt" — ein Befund `1` **vor** dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein **neues** Abbild geschlossen, nie durch Anpassung des alten; **nach** dem Tag ist derselbe Befund ein Sperrlistenbruch nach 10.1. Das letzte Abbild vor dem Tag trägt die Hashes des Tag-Commits. Erster Anwendungsfall: `faltenplan.py` in TB-86 (37.3).
>
> > ⭐ **Ergänzt durch 40.8 (e) (Fable 24a, TB-96, 24.09.2026):** Die Sonde liest **alle drei Gruppen** — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) und `herkunft.py::EINGEFROREN` (39.7) — **aus dem Abbild**, nicht aus ihrem eigenen Code; „Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache". Vollzug TB-97, mit Gegenprobe. Der Satz oben bleibt zeichengleich.

**Seine drei Gründe, zeichengleich:**

> *Quelle des Grundes — drei, alle aus dem Bestand:* **(1)** Beide Listen liegen in `herkunft.py`, das mit Punkt 11/12 auf der Sperrliste steht. Ein Abbild, das mit der Sperrliste wachsen muss (Abbild-Datei, Erzeuger, Sonde kommen noch hinzu), kann nicht in einer Datei liegen, die nicht geöffnet werden darf. **(2)** Sie weichen heute vom Registertext ab, und ihr Zweck ist nirgends registriert — eine Liste, von der man nicht weiss, was sie darstellen soll, kann nicht zum Abbild von etwas erklärt werden. **(3)** Der Registertext ist die Quelle (30.2 (2) sinngemäss): Ein Abbild wird aus ihm gebildet und gegen ihn geprüft, nicht aus einer vorhandenen Datei übernommen, weil sie schon da ist. Kein Ergebnis.

**Was der Fund aus 36.2 (c) bedeutet und was nicht — Fable, zeichengleich:**

> **Was der Fund bedeutet, und was er nicht bedeutet:** Der Zustand „maschinenlesbare Fassung weicht vom Registertext ab, und niemand hat sie geprüft" besteht — ihr sagt es richtig — heute schon. Er ist **kein Sperrlistenbruch**: Die Dateien selbst sind unverändert (Hashes stimmen). Er ist eine **Lücke im Nachweis**, wenn `herkunft.py` aus diesen Listen die Hashes bildet, die in `herkunft.json` als Herkunft des Laufs stehen — dann fehlen dort `benchmark_drawdowns_vt.json` und die beiden Universumsdateien, und drei Dateien stehen drin, die kein Sperrlistenpunkt sind. Ob das so ist, weiss ich nicht — **das ist die Messung, die ich brauche:**

⚠️⚠️ **Die Tatsachennotiz zu den zwei Listen (`EINGEFROREN`,
`SPERRLISTE_DATEIEN`), die der Registertext oben verlangt, wird in diesem
Abschnitt NOCH NICHT geschrieben.** Fable hat dafür eine Messung erbeten,
zeichengleich:

> **Nur das Ob:** Welche Funktionen von `herkunft.py` lesen `EINGEFROREN` und `SPERRLISTE_DATEIEN`, und in welche Ausgabe (Datei, Feld) gehen die daraus gebildeten Hashes ein? Läuft `register()` oder `datenstand()` (Punkt 11/12) über diese Listen?

⭐ Die Messung ist am 22.09.2026 vom steuernden Chat gemacht und Fable mit
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md` vorgelegt;
**seine Tatsachennotiz folgt** und wird als eigener Eintrag eingetragen.
Eingetragen ist hier nur, **dass** sie aussteht — mit dieser Fundstelle. Die
beiden Listen selbst bleiben unberührt: `herkunft.py` steht auf der Sperrliste
(Punkte 11, 12), und ob es vor dem Tag geöffnet werden muss, entscheidet Fable
nach der Messung — 22c, zeichengleich:
„**Meine Linie dazu, vorab und nicht als Entscheidung:** Nach 21b (3) nicht öffnen, wenn die Sperrlisten-Sonde die Lücke schliesst".

**Fables Unsicherheit, 22c, zeichengleich:**

> **Unsicher:** ob Abschnitt 10 in einer Form vorliegt, aus der ein Programm Pfad und Hash je Punkt zuverlässig lesen kann (Prüfung (ii) der Sonde). Wenn nicht, ist der Abgleich Abbild↔Registertext eine Prüfung mit Beleg im Auftrag statt einer Codezeile — Handwerk, aber ihr müsst es wissen, bevor ihr die Sonde beauftragt.

⚠️ Auch dazu liegt Fable eine Messung vor (Anfrage 22c Abschnitt 3,
`docs/projektfuehrung/VORARBEIT_sperrlisten_sonde.md`, lesend, HEAD `fdb181a`);
sie ist hier **nicht** eingetragen — sie gehört zur ausstehenden Antwort.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, zusammen
mit der Marke aus 36.2.

### 36.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sperrlisten-Sonde schreiben** (Schritt 1 in 36.3) — keine Freigabe; ihre Ausgänge sind seit 36.5 festgelegt, ihr Gegenstand (das Abbild) seit 36.6 | Betreiber |
| ⛔ | **`faltenplan.py main()` absichern** — Voreinstellung, Einmal-Schreibsperre (Ausgang 1 nach 36.5), Mutationsprobe (Schritt 2) — keine Freigabe | Betreiber |
| ⛔ | **`faltenplan.py:336` umstellen** (Schritt 3) — nach 36.1 (4) und 36.3 **erst nach Schritt 2** | Betreiber, nach Schritt 2 |
| ⛔ | **Abbild-Datei der Sperrliste (36.6), Abbild des Faltenplans, Faltenplan-Sonde (33.3), Hash auf die Sperrliste** (Schritt 4) | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m2_sperrlisten_hash.txt`). Ein Hashbruch wäre nach 36.2 eine Tatsachennotiz, nie eine stille Reparatur | — |
| ⛔ | **`herkunft.py` anfassen** — auch nicht die beiden Listen aus 36.2 (c); die Datei steht selbst auf der Sperrliste (Punkte 11, 12) | Fable (Tatsachennotiz), dann Betreiber |
| ⛔ | **Die Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN` schreiben** (36.6) — nur eingetragen, dass sie aussteht | Fable (Anfrage 22c) |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M6); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |
| ⚠️ | **Offen bei Fable:** die Tatsachennotiz zu den zwei Listen (36.6); die Frage der Anfrage 22c, ob die Sonde auch Pfade prüft, die für die Sperrliste **bestimmt** sind (`benchmark_drawdowns_vt.json`, 21.9/23.7 — von 36.1 (1) gedeckt, vom Wortlaut in 36.2 „für jeden Sperrlistenpunkt" nicht); seine Unsicherheit aus 22c, ob Abschnitt 10 maschinenlesbar ist (Messung vorgelegt); seine Unsicherheit aus 35.5 (weitere Fundstellen des Bezeichners, in Anfrage 22a Punkt 2 gemessen) | Fable |
| ⚠️ | **Offen beim Betreiber:** die Freigabe für die vier Schritte aus 36.3 — keine erteilt | Betreiber |

*Dieser Abschnitt ist rein additiv: Er trägt vier Ersteinträge, eine
Reihenfolge und eine Tatsachennotiz des Verfahrensprüfers zeichengleich ein,
darunter eine Berichtigung, die er am selben Tag an seinem eigenen Text
vorgenommen hat; setzt sechs Marken am alten Ort; hält drei nachgemessene
Tatsachen zum Bestand und das Ausstehende fest — und entfernt nichts. Gebaut
wird nichts.*

