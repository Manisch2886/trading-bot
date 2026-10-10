# REGISTER-KOPIE Abschnitt 41 (von 0–56) — Register-Z. 8566–8986 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 41. Nachweis mit zwei Teilen, Resolver ohne Rückfall, Deckel statt Purge, Mutationsproben einzeln — die Einträge aus Fable 24b, 24c, 24d (TB-108, 25.09.2026)

### 41.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 40. Der
Verfahrensprüfer hat vom 24.09.2026 an in sechs Antworten (24b, 24c, 24d, 25a,
25b, 25c) Registertexte, Berichtigungen, Präzisierungen und Tatsachennotizen
benannt. **Der Code ist mit TB-103 bis TB-107 danach gebaut; das Register stand
bis zu diesem Eintrag auf dem Stand von Abschnitt 40 (`d0dc890`, 24.09.2026).**
Dieser Abstand war benannt, nicht still — Fable 23f Abschnitt 3, zeichengleich:
„Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag."
Mit 41 und 42 ist er geschlossen, soweit Fable entschieden hat.

**Gliederung:** 41 nimmt die Einträge aus **24b, 24c und 24d** auf (41.1–41.3),
42 die aus **25a, 25b und 25c** samt den Tatsachennotizen aus TB-103 bis TB-107.
⚠️ **Diese Grenze hat der steuernde Chat vorgeschlagen und der Betreiber am
25.09.2026, 22:34 gewählt (Auswahlkarte, `docs/auftraege/MAC_TB-108_register_41_42.md`).
Fable hat sie nicht entschieden** — er spricht nur von „Register 41/42". Er kann
ihr widersprechen; eine andere Grenze wäre eine Umnummerierung mit Vermerk, keine
Änderung der Einträge.

**Bauart je Eintrag:** Kennung aus der Arbeitsliste
(`docs/projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md`, A1–A12, B1–B8, C1–C9;
in 42 D1–D12, E1–E8, F1–F8, G1–G10) · Fables Text **eingesetzt, nicht
abgetippt** (Blockzitat; Teilzitate in „…"), mit Quelle · Art · Stand, gemessen
in TB-108 (`docs/belege/TB-108/a3_stand.txt`, `c_hashuebergaenge.txt`), ohne
Ergebnisgrössen (27.1) · wo die Fassung später berichtigt wurde. **Beide
Fassungen stehen**, die frühere mit „⭐ BERICHTIGT durch …", die spätere mit
„berichtigt …". Je Zitat ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-108/d2_zitate.txt`).

⚠️ **Tatsachennotiz zur Herkunft der Quellen:** Die sechs Antwortdateien
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-24b_…`, `…24c_…`, `…24d_…`,
`…25a_…`, `…25b_…` und `…25c_…` hat der steuernde Chat aus der Projektablage
**abgeschrieben**, nicht byteweise übertragen — das Werkzeug liefert dort nur
Text (`docs/projektfuehrung/UEBERGABE_2026-09-25.md`, Block 8). **Die Zitate
hier sind zeichengleich mit der Datei im Repo; ob diese zeichengleich mit Fables
Ablage ist, ist nicht gemessen.**

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag, der einen alten Satz
berichtigt, präzisiert oder ergänzt, steht zusätzlich als **Marke** beim alten
Satz; die Liste der Marken steht in 42.7. Die alten Sätze bleiben zeichengleich;
`git diff --numstat` auf dieses Register zeigt für TB-108 in der zweiten Spalte
`0`. ⛔ **In Abschnitt 10 steht keine Marke** — die Sperrlisten-Sonde vergleicht
dessen Listentext mit dem Abbild (36.6, Prüfung (ii)); was dorthin gehörte,
steht in 42 mit Verweis auf den Punkt.

### 41.1 Aus Fable 24b (`FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md`)

Fables Liste für dieses Register, 24b Abschnitt D Punkt 5, zeichengleich:

> 5. **Register 41:** Berichtigung 12 (sieben, Namen, F4), 40.7 („sieben"), 40.6 (TB-90-Satz), Regel „allein beissen" und H6, Störproben-Satz, Marke 5.1 Nr. 4, Testrahmen-Notiz, Tatsachennotiz `bot_lauf.py`/`symbol`, Regel „keine Kennzeichnung in Laufcode-Feldern".

**A1 — Berichtigung zu 12: sieben Mutationsproben, mit Namen** · Art:
Berichtigung · Quelle: 24b Abschnitt B2

> **Berichtigung zu 12 (Ersatztext für den Halbsatz „davon acht Mutationsproben"):** … davon **sieben Mutationsproben, H1 bis H7** (Teil H); H0 ist der Grundlauf ohne Mutation und keine Probe. F4 ist keine Mutationsprobe (ändert keinen Code), hat aber nach 40.7 eine Gegenprobe. Die Zahl der Prüfungen ist eine Tatsachennotiz mit Stand (heute 188, Commit …), kein Registertext; die **Namen** der Mutationsproben sind Registertext. Ändert sich die Menge, ist das eine Berichtigung mit Namen.

*Seine Quelle des Grundes, zeichengleich:* „23a (Kopien altern; eine Zahl ohne Namen ist eine Kopie des Codes im Register). Kein Ergebnis."

**Stand, gemessen:** Der Test zählt heute **196** Prüfungen
(`research/vorregistrierung/test_vorregistrierung.py`, `db50e187…`, letzter
Commit `abeca36`, TB-106; 196/196 in TB-107, `docs/belege/TB-107/g4_tests.txt`).
Die Namen H1 bis H7 stehen im Test (Teil H). ⚠️ Zu H6 siehe A4.

**A2 — Berichtigung zu 40.7: „alle acht" lies „alle sieben"** · Art:
Berichtigung · Quelle: 24b Abschnitt B2

> **Berichtigung zu 40.7:** „alle acht" lies „alle sieben (H1–H7)".

**Stand, gemessen:** Die Gegenproben aller Mutationsproben hat TB-97 geführt
(`docs/ERGEBNIS_TB-97_testannahmen_zweite_runde.md`). ⚠️ „sieben" setzt voraus,
dass H6 eigenständig beisst — siehe A4.

**A3 — Berichtigung zu 40.6: der TB-90-Satz** · Art: Berichtigung · Quelle: 24b
Abschnitt C1

> **Berichtigung zu 40.6:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren" lies „Der Reproduzierbarkeitsnachweis für die Listen-Erzeugung ist der Modus-Lauf nach 23e (zweimal, bytegleich) und stand am 24.09. noch aus; TB-90 B6 betraf die Backtest-Skripte auf `data/`, nicht den Listen-Erzeuger."

Fable nennt es seinen vierten Fall derselben Klasse (24b C1). Die Berichtigung
betrifft den in 40.6 zeichengleich zitierten Satz aus 24a; er bleibt dort
stehen, die Marke steht in 40.6.

**A4 — Regel: jede Mutationsprobe beisst allein; H6** · Art: Registertext
(Ergänzung zu 12/40.7) · Quelle: 24b Abschnitt B3

> **Regel (Ergänzung zu 12/40.7):** Jede Mutationsprobe beisst **allein**: Ihre Gegenprobe (nur ihre eigene Mutation weggelassen, alles andere im Grundzustand) scheitert. Eine Probe, die das nur im Verbund mit einer anderen leistet, wird vor dem Tag **eigenständig** gemacht — H6 braucht einen eigenen eingesetzten Fehler, den die entfernte Wache hätte fangen müssen, statt sich H5s Fehler zu leihen. Ist das strukturell nicht möglich, wird das Paar als **eine** Probe mit zwei Mutationen registriert und gezählt — sechs plus ein Paar, nicht sieben.

*Sein Grund, zeichengleich:* „A8 und 12. Eine Zählung, die ein Paar als zwei führt, ist dieselbe Unwahrheit wie „acht", nur kleiner. Kein Ergebnis."

**Stand, gemessen:** ⚠️⚠️ **H6 ist bis heute nicht eigenständig.** TB-97 hat
gemessen: Sind die Mutationen von H5 **und** H6 weggelassen, besteht H6 — „H6
trägt nur zusammen mit H5" (`docs/ERGEBNIS_TB-97_testannahmen_zweite_runde.md`,
Zusatz zu H6); der Test sagt es selbst (Kommentar „Die Mutation von H5 ist
Voraussetzung von H6", Stand `db50e187…`). Seitdem ist H6 nicht umgebaut (letzte
Änderung an H6: `ae8db0b`, TB-97). Die Regel ist seit TB-103 auf **neue**
Proben angewandt worden (Ergebnisse TB-104 bis TB-107: „beisst allein"; TB-103
nach Fable 25a Abschnitt 2).
⇒ **Vor dem Tag offen:** H6 bekommt einen eigenen eingesetzten Fehler, oder
H5/H6 werden als **eine** Probe mit zwei Mutationen geführt und gezählt — dann
gilt „sechs plus ein Paar", und „sieben" in A1/A2 ist nach Fables eigener Regel
zu berichtigen (42.6).

**A5 — Störproben in beide Richtungen** · Art: Registertext (Ergänzung zu 12) ·
Quelle: 24b Abschnitt C2

> **Registertext, Ergänzung zu 12 (Gegenproben) — Störproben:** Eine Störprobe nach „geht es ein?" wird in **beide** Richtungen geführt: klein genug, dass nichts passieren darf, und gross genug, dass etwas passieren muss. Eine Störprobe nur in eine Richtung belegt nichts. *(Formuliert von TB-95 am 23.09.2026, übernommen als Registertext durch den Verfahrensprüfer, 24.09.2026.)*

*Sein Grund, zeichengleich:* „die Störprobe zur Faltenlänge — eine Zeile weg hätte allein das falsche „nein" ergeben; F4 ist derselbe Fehler in einer Prüfung. Kein Ergebnis."

Die Tatsache, aus der der Satz stammt, steht im Nachtrag zu 39.8 (TB-95,
„Der methodische Satz, der über den Fall hinausgeht").

**A6 — Marke an 5.1 Nr. 4: zwei Leser, ein Parser** · Art: Marke · Quelle: 24b
Abschnitt B4

> **Marke bei 5.1 Nr. 4:** ja, um den zweiten Leser ergänzen. Und: zwei Leser, **ein Parser** — die Funktion, die 5.1 Nr. 4 liest, ist eine, und beide rufen sie; sonst altern zwei Parser getrennt. Handwerk, aber die Anforderung ist Verfahren (ein Wert, ein Ort).

**Stand, gemessen:** Seit TB-97 steht der Parser **einmal**, in
`research/vorregistrierung/beispieldaten.py::jahre_aus_register_5_1_nr_4`
(Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`,
genau ein Treffer, sonst `None`). Ihn rufen `test_vorregistrierung.py`
(`_testjahre_aus_register`, `G6`) und `beispieldaten.krisenfalten` — zwei Leser,
ein Parser. Die Marke steht bei 5.1 Nr. 4, unter der Marke aus 40.2.

**A7 — Testrahmen-Notiz** · Art: Tatsachennotiz (zu 12) · Quelle: 24b Abschnitt
C4

> Es ist keine Prüfung, sondern der Testrahmen (12: „erzeugte Beispieldaten mit frei erfundenen Werten"). Literale dort sind kein Prüffehler, aber ein **Befund am Testrahmen**: Ein Rahmen, der bei Doppeljahren entartet (Z. 77) oder nie trifft (Z. 69), prüft den Auswerter nur für Bots mit Einjahresfalten — und `elliott_wave` hat Doppeljahre. Eigene Tatsachennotiz (zu 12): der Testrahmen deckt seit 24c beide Faltenlängen ab; vorher nicht. Die Umstellung selbst ist nach 24c geschehen (5.1 Nr. 4 über Abdeckung) und angenommen.

Die Stoffsammlung führt diesen Eintrag nur als Stichwort (24b D5
„Testrahmen-Notiz"); der Text steht in derselben Antwort, Abschnitt C4.

**A8 — `bot_lauf.py` und `symbol`** · Art: Tatsachennotiz · Quelle: 24b
Abschnitt A3

> *Eine Regel aus dem Nebenbefund:* Seit TB-26 ist `symbol` kein reines Etikett mehr; der Kopf von `bot_lauf.py` sagt das Gegenteil. Tatsachennotiz — und: **Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett.

**Stand, gemessen:** Der Kopf von `research/exposure_messung/bot_lauf.py` sagt
weiter, `simulate_portfolio()` benutze `symbol` „ausschliesslich als
Beschriftung der Ausgabezeile" (Z. 32–37; letzter Commit `d48a195`, TB-105,
dort nur die Ordneranlage geändert). Nach TB-98 Befund 2 liest der
Zufallsschlüssel der Zuteilung seit TB-26 das Symbol — der Satz im Kopf ist
damit falsch; **Tatsachennotiz, der Kopf ist nicht geändert.**

**A9 — Regel: keine Kennzeichnung in Laufcode-Feldern** · Art: Registertext ·
Quelle: 24b Abschnitt A3, derselbe Absatz wie A8

„**Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett."

**A10 — kein Fallback unter dem Modus** · Art: Registertext, Ersteintrag (zu
5a/5e) · Quelle: 24b Abschnitt A2

> **Registertext, Ersteintrag (zu 5a/5e, Selektionsmodus) — kein Fallback unter dem Modus:** Unter dem Selektionsmodus gibt es **keinen Rückfall auf eingebaute Voreinstellungen**, gleich welcher Art (Symbollisten, Parameter, Pfade, Schwellen). Eine Eingabe, die im Snapshot nicht gefunden wird, ist Rückgabewert **2** (nicht prüfbar) und beendet den Lauf, bevor gerechnet wird — nach demselben Muster, mit dem `paths.py` den Live-Pfad unter dem Modus unerreichbar macht (`SystemExit`, nicht Exception). Eine Meldung „Keines ausgelassen" darf nur stehen, wenn die geladene Symbolmenge gleich der Universumsdatei aus dem Snapshot ist; das Ladeprotokoll (3b (d)) nennt beide Zahlen und die Quelle der Liste.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 22e/17.x — der Modus ist gebaut, „damit kein `except Exception` im Aufrufer den Abbruch in einen stillen Weiterlauf verwandelt"; ein Fallback ist genau dieser stille Weiterlauf, nur eingebaut statt gefangen. A8. Kein Ergebnis.

**Stand, gemessen:** umgesetzt im Resolver (`shared/paths.py`, TB-103,
`d87997e`: `CONFIG_DIR = <snapshot>/config`, Prüfung gegen das MANIFEST,
`SystemExit(2)`), für die vier Rückfälle aus 25a (42.1, D12) in TB-105, TB-106
und TB-107. ⚠️ **Nicht umgesetzt ist der letzte Satz** („Das Ladeprotokoll …
nennt beide Zahlen und die Quelle der Liste"): `shared/ladeprotokoll.py` ist
seit `55b991d` (TB-45, 17.09.2026) unverändert und nennt weder die Zeilenzahl
der Universumsdatei noch die Quelle der Liste — derselbe offene Teil wie 25a
(B) (4) (42.1, D3/D9).

> ⭐ **`fehlend` im Modus: siehe 46.2** (Fable 27a R10, TB-117, 26.09.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**A11 — Tag-Vorbedingung: Trockenlauf aller neun im Modus** · Art: Registertext
(Ergänzung zum Plan) · Quelle: 24b Abschnitt A2

> **Tag-Vorbedingung, Ergänzung zum Plan:** Vor dem Tag läuft für **alle neun Bots** ein Trockenlauf im Selektionsmodus gegen den echten Snapshot, mit Lesehaken und Aufrufstapel: 0 Zugriffe ausserhalb `snapshots/<hash>/`; geladene Symbolmenge gleich Universumsdatei; kein Fallback; Rückgabe 0. Das Protokoll ist Tatsachennotiz. Ein Modus, unter dem noch nie ein Bot gelaufen ist, ist keine registrierte Umgebung, sondern eine behauptete.

⭐ **PRÄZISIERT durch 42.1** (D2: „0 Zugriffe" nach drei Klassen; D3: Liste und
Menge; D4: Wiederholung am Tag-Commit) und **42.2** (E6: Stichtag).

**Stand, gemessen:** gelaufen in TB-103 (`836865f`), TB-105 (F1, auch im
frischen Klon), TB-106 (G5) und TB-107 (G3), je 9 × rc 0. Nach 42.1 (D4) ist
keiner davon die Tag-Vorbedingung selbst — sie wird am Tag-Commit wiederholt.

**A12 — Präzisierung zu 40.6: die neuen Listen kommen vom Signalpfad** · Art:
Registertext (Präzisierung zu 40.6) · Quelle: 24b Abschnitt A3

> **Entscheidung (Präzisierung zu 40.6):** „Der registrierte Code" für die Neu-Erzeugung der Listen ist der **Signalpfad** (die neun Backtests mit registrierten heutigen Parametern, `run_backtest`), nicht der Ausführungspfad (Zuteilung). Die neuen Listen enthalten die **gefundenen** Trades mit den Feldern, die 5.4 braucht (`bot`, `symbol`, `entry_time`, dazu die Felder, die der Signalpfad ohnehin liefert), **ohne** Simulationsspalte `ausgefuehrt` und **ohne** Kennzeichnung im Symbolfeld. Das Format wird als Feldliste registriert (Bauart 33.3), der Erzeuger schreibt genau diese Felder. Vergleichbarkeit mit den historischen Listen (`78e2bc6`) ist **nicht** gefordert — die sind historischer Stand mit Notiz; verglichen wird die abgeleitete **Faltenlänge** gegen 33.2, nicht Liste gegen Liste.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5.4 (Schwelle auf gefundene Trades je Jahr) und 33.2; der Grund für ein Feld in einer Eingabedatei ist, dass die Herleitung es liest — 33.3-Logik. Kein Ergebnis. **Folge:** Der Erzeuger braucht die Zuordnung ausgeführt/gefunden nicht mehr, die Kennung entfällt, der Konflikt mit Punkt 10 entsteht gar nicht; keine Änderung an der Zuteilung, keine Suche nach einer durchgereichten Spalte.

⭐ **ERGÄNZT durch 41.2 (B3, B6/B7):** Die Feldliste bekommt `exit_time` und
`haltedauer_balken` (24c Abschnitt 4).

**Stand, gemessen:** Der Erzeuger auf dem Signalpfad ist **nicht gebaut**
(Plan-Punkt 3); die neun Listen sind nicht neu erzeugt.

> ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114,
> 26.09.2026). Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.

### 41.2 Aus Fable 24c (`FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md`)

Fables Liste für dieses Register, 24c Abschnitt 6 Punkt 4, zeichengleich:

> 4. **Register 41/42:** Reichweite 5.4, Berichtigung 2d-Herleitung, Donchian-Herleitung, Nachweis mit zwei Teilen, Resolver-Pflicht, Tatsachennotizen (`haltedauern_je_bot.csv` historisch, `tb24_haltedauern/auswertung.py` historisch, TB-93/102-Nachweis = 2).

**B4 — Der Nachweis hat zwei Teile** · Art: Registertext (Ersatz für den
Nachweisbegriff aus 23e) · Quelle: 24c Abschnitt 1

> **Registertext, Ersatz für den Nachweisbegriff aus 23e (Eingabestand):** Ein Reproduzierbarkeitsnachweis besteht aus **zwei** Teilen, und beide sind Pflicht: **(a)** dem Ergebnisvergleich — die erzeugte Datei ist bytegleich zur eingefrorenen; **(b)** dem **Leseprotokoll** — alle Lesezugriffe des Laufs auf Kurs-, Universums- und Ergebnisdateien liegen innerhalb `snapshots/<hash>/` oder auf registrierten Eingabedateien, **null** im Repo-Arbeitsstand (`data/`, `config/`, `ergebnisse/` ausserhalb der registrierten Pfade). Fehlt (b) oder zeigt es einen Zugriff ausserhalb, ist der Nachweis **2**, gleich was (a) sagt. „Bytegleich" ohne Leseprotokoll ist kein Nachweis, sondern ein Zufall, der heute stimmt.

*Seine Quelle des Grundes, zeichengleich:* „5e (der Lauf belegt, woraus er nachweislich gelesen hat) und TB-98 Befund 1 / TB-102 Lesart 2: richtiges Ergebnis, falscher Ort, keine Warnzeile. Kein Ergebnis."

⭐ **PRÄZISIERT durch 42.1 (D6):** Was „ausserhalb" heisst, regeln die drei
Klassen von Zugriffen (ergänzt durch 42.2 E1, E2 und 42.3 F7, F8).

**Stand, gemessen:** angewandt seit TB-103 — jeder Modus-Lauf der Aufträge
TB-103 bis TB-107 hat einen Lesehaken mitgeführt. ⚠️ **Der Nachweis der
Benchmark-Tabelle bleibt 2**: Der Modus-Lauf liest zwei Eingaben ausserhalb des
Snapshots (die neun TB-24-Listen und `ergebnisse/messgroessen.json`; zuletzt
gemessen TB-104 C5). Ebenso der Nachweis für `messgroessen.json`
(`haltedauern_je_bot.csv` aus dem Repo, TB-103).

**B8 — der TB-93/TB-102-Nachweis ist 2** · Art: Tatsachennotiz · Quelle: 24c
Abschnitt 1, Absatz „Für alle bisherigen Nachweise"

> *Für alle bisherigen Nachweise heisst das:* TB-91 A1b (`benchmark.py` im Modus, zweimal bytegleich) — hatte es ein Leseprotokoll? TB-95 hat später mit Lesehaken gemessen, dass `benchmark.py` 222 + 2 Dateien aus dem Snapshot liest; wenn diese Messung derselbe Lauf-Typ war, gilt A1b als vollständig; wenn nicht, ist das Leseprotokoll für die Benchmark-Tabelle einmal nachzuholen. **Nur das Ob.** Der TB-93/TB-102-Nachweis für `messgroessen.json` ist nach dieser Regel **2** — nicht geführt.

⭐ **BERICHTIGT durch 41.3 (C8):** „TB-91 A1b" lies „TB-92 A1b". Die Frage
„hatte es ein Leseprotokoll?" ist beantwortet in 41.3 (C9) und 42.1 (D10): ja,
seit TB-92.

**B5 — Resolver-Pflicht** · Art: Registertext (Ergänzung zu 5a/5e) · Quelle:
24c Abschnitt 2

> **Registertext, Ergänzung zu 5a/5e:** Jedes Modul des Laufbereichs, das Kursdaten oder Universumsdateien liest, bezieht seine Pfade über den Resolver (`shared/paths.py`, `get_strategy_paths()`). Eine eigene Pfadlogik für diese Dateien ist ein Befund der Lesequellen-Sonde (1). Es gibt **eine** Anordnung, die der Snapshot vorgibt (Kurse flach, Universum unter `config/`), und der Resolver ist der einzige Ort, der sie kennt.

*Seine Quelle des Grundes, zeichengleich:* „`strategy_paths.py` selbst („Hier steht KEIN zweiter Resolver") und 24b A2. Drei Anordnungen sind zwei zu viel; und ein Programm, das den Modus nicht kennt, kann ihn nicht einhalten. Kein Ergebnis."

⭐ **BERICHTIGT durch 42.1 (D1):** Die Fundstelle „(`shared/paths.py`,
`get_strategy_paths()`)" lies „über den Resolver (`shared/paths.py`, direkt oder
über `strategy_paths.get_strategy_paths()`)" — Fables achter Fall. ⭐
**ERGÄNZT durch 41.3 (C6):** Ein Modus-Lauf ist ein Lauf unter dem Resolver;
Hilfsordner tragen keinen Nachweisteil (b).

**Stand, gemessen:** Die Leser des Laufbereichs holen ihre Kurs- und
Universumspfade über `shared/paths.py`: `messgroessen.py` (TB-103, `ae136fd`),
`benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py`,
`universum_trockenlauf.py` (TB-104, `572d725`); Ersatzwurzeln brechen unter dem
Modus mit 2 ab, bevor gelesen wird.

**B1 — Reichweite des Grundsatzes aus 5.4** · Art: Registertext, Ersteintrag ·
Quelle: 24c Abschnitt 4

> **Registertext, Ersteintrag — Reichweite des Grundsatzes aus 5.4:** Keine Festlegung des Verfahrens, die vor dem Lauf steht (Faltenlänge, Purge, Embargo, Trainingsende, Rastergrenzen), wird aus Grössen hergeleitet, die vom **Positionslimit** oder von der **Ausführung** abhängen. Herleitungen aus Trades verwenden **gefundene** Trades (Signalpfad), nie ausgeführte. Der Grundsatz gilt für alle Stellen, an denen 5.4 ihn heute allein anwendet.

*Seine Quelle des Grundes, zeichengleich (für B1, B2, B3 und B6/B7 gemeinsam):*

> *Quelle des Grundes:* 5.4 im Wortlaut („keine Festlegung vor dem Lauf, die vom Positionslimit abhinge"), 2d im Zweck (kein Leck zwischen Falten), 3 („erzeugt, nicht abgetippt"). **Kein Ergebnis — und hier gilt es besonders:** Ich weiss nicht, ob `purge_tage` länger, die Donchian-Untergrenze anders, `messgroessen.json` wie stark verändert herauskommt. Ihr habt es nicht gerechnet, ich habe es nicht gefragt. Die Regel ist dieselbe, wie auch immer es ausgeht, und deshalb steht sie jetzt — bevor der Erzeuger läuft (24.3). Wer nach der Messung sagt „das verändert den Raster zu sehr", wählt nach Wirkung; wer vorher sagt „lassen wir es, es ist ja nicht zirkulär im Lauf", wählt auch — für die Zellen mit kurzen Haltedauern.

**Stand, gemessen:** 5.4 sagt „gefundene" im Wortlaut („Gerechnet aus den
**gefundenen** Trades je vollem Kalenderjahr" und „Gefunden, nicht ausgeführt");
Fables Unsicherheit aus 24b ist damit ausgeräumt (24c Abschnitt 0). Die
Marke steht bei 5.4. ⭐ **Tatsachennotiz zu `elliott_wave`:** 41.3 (C4).

**B2 — Berichtigung der 2d-Herleitung (Purge als Schranke über das Raster)** ·
Art: Berichtigung — ⭐⭐ **ZURÜCKGENOMMEN durch 41.3 (C1), der Deckel neu
gefasst durch 41.3 (C2)** · Quelle: 24c Abschnitt 4

> **Berichtigung zu 2d (Purge/Embargo), Herleitung:** `purge_tage` wird nicht aus der maximalen Haltedauer eines Parameterstands hergeleitet, sondern als **Schranke über das registrierte Raster**: die grösste Haltedauer, die ein Trade in irgendeiner Zelle des Rasters erreichen kann — aus den registrierten Rastergrenzen der Ausstiegsachsen (Zeitausstieg, maximale Haltedauer), wo eine Strategie keinen begrenzten Ausstiegshorizont hat, aus dem Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag als Tatsachennotiz. Ein Purge, das für eine Zelle des Rasters zu kurz ist, ist ein Befund.

⛔ **Dieser Text gilt nicht.** Er steht hier, weil Fable ihn in 24c als
Registertext benannt und in 24d ausdrücklich zurückgenommen hat — mit dem Grund
„damit die Ablage nicht zwei Fassungen führt" (41.3, C1).
Eingetragen wurde er nie; 2d/16.6 bleiben, wie sie sind, mit den Präzisierungen
aus 41.3 (C2, C3).

**B3 — Donchian-Untergrenze aus gefundenen Trades** · Art: Registertext
(Berichtigung zur Herleitung) · Quelle: 24c Abschnitt 4

> **Berichtigung zur Herleitung der Donchian-Untergrenze (zwei Bots):** aus `median_balken` der **gefundenen** Trades, nicht der ausgeführten. Die Rastergrenze selbst bleibt eine gemessene Grösse (Abschnitt 2/3, „erzeugt, nicht abgetippt") — nur ihre Eingabe wechselt auf den Signalpfad.

Fable bestätigt in 24d: „**Donchian-Untergrenze (zwei Bots):** bleibt wie in 24c — `median_balken` der gefundenen Trades."

**Stand, gemessen:** offen — die Eingabe (neue Listen gefundener Trades) gibt es
noch nicht (Plan-Punkt 3). `mess["haltedauer"]` liest heute
`registerdaten.py:231` (`median_balken`, TB-104 A3).

**B6/B7 — `haltedauern_je_bot.csv` und ihr Erzeuger werden historischer Stand**
· Art: Tatsachennotiz · Quelle: 24c Abschnitt 4, „Folge für die Eingabedateien"

> **Folge für die Eingabedateien:** Die Haltedauern werden aus **denselben neuen Listen gefundener Trades** abgeleitet, die 24b A3 für die Faltenlänge anordnet — jede gefundene Trade-Zeile trägt `entry_time` und `exit_time`, die Haltedauer folgt daraus. **Ein Erzeuger, eine Eingabedatei je Bot, zwei Herleitungen** (Faltenlänge nach 5.4, Haltedauern für 2d und die Rastergrenze). `haltedauern_je_bot.csv` in heutiger Form und ihr Erzeuger `tb24_haltedauern/auswertung.py` werden historischer Stand mit Tatsachennotiz; `messgroessen.py` liest die Haltedauern aus der neuen Quelle (Konstante, unter dem Resolver). Die Feldliste der neuen Listen (24b A3) bekommt `exit_time` und `haltedauer_balken` ausdrücklich.

**Stand, gemessen:** `research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv`
und `research/tb24_haltedauern/auswertung.py` sind unverändert; `messgroessen.py`
liest die Datei weiter (der eine Zugriff ausserhalb des Snapshots, TB-103). Die
Umstellung auf die neue Quelle hängt am Erzeuger (Plan-Punkt 3).

> ⭐ **41.2 B6/B7 ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 41.3 Aus Fable 24d (`FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md`)

Fables Liste für dieses Register, 24d Abschnitt 4, zeichengleich (Kopf):

> **Register 41/42, zusätzlich zu 24c Abschnitt 6 Punkt 4:**

**C1 (a) — Rücknahme „`purge_tage` als Schranke über das Raster"** · Art:
Rücknahme, **mit Grund** · Quelle: 24d Abschnitt 1 · berichtigt 41.2 (B2)

> **Rücknahme (zu 24c, „Berichtigung zu 2d (Purge/Embargo), Herleitung"):** Der Satz *„`purge_tage` wird … als Schranke über das registrierte Raster bemessen"* ist zurückgenommen. Unter Verfahren B gibt es zwischen Selektionsfalten weder Purge noch Embargo (2c) und vor der Bestätigungsperiode keine Lücke, sondern Bedingung plus Deckel mit Attribution je Position (16.6). Eine Grösse, die eine Trainingsgrenze oder eine Lücke bemisst, gehört zu Verfahren A und wird **nicht neu hergeleitet**.

*Seine Quelle des Grundes, zeichengleich:* „2c und 16.6 im Wortlaut. Kein Ergebnis."

**Der Grund, warum die Rücknahme hier steht** — Fables Art-Spalte zu (a),
zeichengleich: „Rücknahme eines noch nicht eingetragenen Textes — mit Grund eintragen, damit die Ablage nicht zwei Fassungen führt".
Dazu nimmt er eine Zeile aus 24c Abschnitt 5 zurück: „Meine Zeile in 24c Abschnitt 5 („G8 prüft künftig das aus dem Raster geschrankte `purge_tage`") ist damit zurückgenommen."

**C2 (b) — Deckel für Bots ohne Zeitbremse aus gefundenen Trades** · Art:
Registertext (Präzisierung zu 2d, Fassung 16.6) · Quelle: 24d Abschnitt 1 ·
berichtigt 41.2 (B2)

> **Präzisierung zu 2d (Fassung 16.6), Deckel für Bots ohne Zeitbremse:** Das 95. Perzentil der Haltedauer wird aus den **gefundenen** Trades gerechnet (Signalpfad, die neuen Listen nach 24b A3 / 24c), plus 1, aufgerundet wie in 15.4 Anmerkung 4; Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen. Der Zusatz aus 24c *„Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag"* ist zurückgenommen.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 24c, Registertext „Reichweite des Grundsatzes aus 5.4" (Herleitungen aus Trades verwenden gefundene Trades) — und TB-98 Befund 2: ausgeführte Positionen sind seit TB-26 nicht reproduzierbar erzeugbar, gefundene sind es. Die Wirkung kenne ich nicht (der Wert 13 kann sich bewegen); sie beschränkt sich auf den spätesten Beginn der Bestätigungsperiode des Gewinners. Kein Ergebnis.

**Stand, gemessen:** nicht gerechnet — der Deckel von `t3_supertrend` steht in
15.4 und 16.6 weiter mit dem Wert aus **ausgeführten** Positionen
(`research/tb24_haltedauern/daten/t3_supertrend_positionen.csv`, TB-24). Neu zu rechnen, wenn
die neuen Listen gefundener Trades vorliegen (Plan-Punkt 5, 24d Abschnitt 4).
Marken bei 15.4 und 16.6.

> ⭐ **41.3 C2 ERGÄNZT durch R86 (56.3)** (Fable 09a R86, Unterpunkt (a), TB-149, 10.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**C3 (c) — die Bedingung wird für den Gewinner auf dessen Positionen
ausgewertet** · Art: Registertext (Präzisierung zu 2d, Fassung 16.6) · Quelle:
24d Abschnitt 1

> **Präzisierung zu 2d (Fassung 16.6), Auswertungsebene:** Die Bedingung wird im Selektionslauf **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet; der Deckel ist je Bot eine Konstante über alle Zellen. Das Journal des Papierpfads ist dafür keine Quelle. *(Ob der heutige Code eine der beiden Lesarten schon umsetzt, ist nicht gemessen; nach 24.5 existiert der Laufcode, der die Tagesreihe je Zelle erzeugt, nicht.)*

*Seine Quelle des Grundes, zeichengleich:* „5.1 Nr. 7 und 15.1 (Verfahren B: Out-of-Sample ist allein die Bestätigungsperiode — des gewählten Satzes). Kein Ergebnis."

**Kategorie:** Fable hatte gefragt, ob es eine Berichtigung sei (24d,
Unsicher (4)). Nach der Messung, dass der Wortlaut von 16.6 beide Lesarten
trägt, 25a Abschnitt 1 (4), zeichengleich: „Nach eurer Messung ist Eintrag c eine **Präzisierung**, und F17 ist so oder so erfüllt; die Kategorie ist Handwerk (30.6). Sie bleibt Präzisierung."

**C4 (d) — 5.4 bei `elliott_wave`: „gefundene" greift über die Ausführung** ·
Art: Tatsachennotiz (zu 5.4) · Quelle: 24d Abschnitt 2

> **Zum Nebenbefund `elliott_wave`:** richtig — bei ihm ist das Positionslimit keine Achse (2.4: keine Limitachse, Kapitalschranke `floor(1/ALLOCATION_PCT) = 10`). Der Grundsatz greift dort über das zweite Wort im Registertext aus 24c, *„oder von der Ausführung"*: Die Zuteilung entscheidet auch bei ihm, welche gefundenen Trades ausgeführt werden, und die Kapitalschranke ist eine Ausführungsgrösse. Der Registertext braucht keine Ergänzung; die Tatsachennotiz zu 5.4 sollte den anderen Grund nennen, damit niemand bei diesem Bot „gefundene" für überflüssig hält.

⇒ **Tatsachennotiz zu 5.4** *(eigene Fassung der Sitzung nach diesem Absatz,
kein Fable-Wortlaut):* Bei `elliott_wave` ist das Positionslimit keine
Rasterachse (2.4); „gefundene" statt „ausgeführte" Trades ist dort trotzdem
nötig, weil die Zuteilung mit der Kapitalschranke `floor(1/ALLOCATION_PCT)`
entscheidet, welche gefundenen Trades ausgeführt werden — der Grundsatz greift
über „oder von der Ausführung" (41.2, B1). Marke bei 5.4.

**C5 (e) — `purge_tage` / „Trainingsende"** · Art: nach der Messung entschieden
— ⭐ **BERICHTIGT (entschieden) durch 42.1 (D5)** · Quelle: 24d Abschnitt 1

„**Messbitte, nur das Ob:** Liest irgendeine Grösse, die der Lauf oder die Benchmark-Tabelle verwendet, heute `purge_tage`?"

Entschieden in 25a Abschnitt 1 (1), zeichengleich: „**(1) `purge_tage` hat keinen Leser im Lauf** — Fall „historischer Stand". Eintrag e aus 24d ist damit entschieden: Tatsachennotiz, keine Neuherleitung, `G8` prüft ein Relikt."

**Stand, gemessen:** `purge_tage`, `embargo_tage` und
`training_bis_ausschliesslich` sind aus dem gerechneten Plan entfernt (TB-104,
`f334a7b`); `faltenplan.py` nennt sie nur noch im Kopfkommentar. `G8` ist
angepasst, nicht gelöscht. Hash-Übergang in 42.5.

**C6 (f) — Modus-Lauf = Resolver-Modus; Hilfsordner kein Nachweis** · Art:
Registertext (Ergänzung zu 5e und zur Resolver-Pflicht) · Quelle: 24d Abschnitt
3

> **Registertext, Ergänzung zu 5e und zur Resolver-Pflicht (24c):** Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers (`shared/paths.py`, `TB_SELEKTIONSWURZEL`). Eine Anordnung des Snapshot-Inhalts in Repo-Form — Verknüpfungen, Hilfsordner, Ersatzwurzeln wie `TB30A_BASE_DIR`, `TB36_BASE_DIR`, `TB40_BASE_DIR` — ist **kein Modus-Lauf** und trägt keinen Nachweisteil (b). Ein Modul, das den Resolver nicht kennt, hat keinen Nachweis (2), bis es ihn kennt; ein Hilfsordner ersetzt den Resolver nicht. Als **Messwerkzeug** ausserhalb eines Nachweises (Störproben, Diagnose) bleibt die Anordnung zulässig und wird als solche benannt.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* (1) 23e: *„der Nachweis muss denselben Weg gehen wie der Lauf"* — der Lauf am Tag geht durch den Resolver; ein Hilfsordner prüft den **Inhalt** des Snapshots, nicht den **Weg** dorthin, und TB-98 Befund 1 war ein Fehler des Weges bei richtigem Inhalt. (2) Das Verknüpfungsskript des Hilfsordners ist selbst Pfadlogik ausserhalb des Resolvers — genau der Befund 1 der Lesequellen-Sonde, nur ausserhalb des Repos, wo die Sonde ihn nicht sieht. (3) 24c: eine Anordnung, ein Ort, der sie kennt. Kein Ergebnis.

**Stand, gemessen:** angewandt seit TB-103. `TB36_BASE_DIR` und `--daten` sind
seit TB-104 als Messwerkzeug benannt und brechen unter dem Modus mit 2 ab.
`TB30A_BASE_DIR` greift in `herkunft.py:51` auch unter gesetzten
Modus-Variablen (TB-106 A11) — offene Frage 25d (3), 42.6. Marke bei 39.6.

**C7 (g) — TB-92 A1b und TB-95 D1 waren Hilfsordner-Läufe** · Art:
Tatsachennotiz · Quelle: 24d Abschnitt 3

> **Tatsachennotiz dazu, damit niemand alte Läufe umdeutet:** TB-92 A1b (39.6: *„`TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` nicht (0 Treffer)"*) und TB-95 D1 waren nach dieser Regel beide Hilfsordner-Läufe. Ihre Ergebnisvergleiche bleiben Tatsachen (fünfmal `64fb2912…`); als Nachweise sind sie 2 — aus zwei Gründen, von denen 39.8 der ältere ist.

Marke bei 39.6.

**C8 (h) — „TB-91 A1b" lies „TB-92 A1b"** · Art: Berichtigung an 24c · Quelle:
24d Abschnitt 3 · berichtigt 41.2 (B8)

> **Erst mein Fehler, dann der Widerspruch.** Ich habe in 24c „TB-91 A1b" geschrieben. Das Register nennt den Modus-Nachweis der Benchmark-Tabelle **TB-92 A1b** (Kopf von 39.6: *„Fable 23e, TB-92 A1b"*; 39.5: `benchmark.py` `3960375a…` → `d6bdd558…` ist TB-91, die Neurechnung). Eine Auftragsnummer, nicht gemessen — dieselbe Klasse wie TB-94/TB-96 in 24a. **Angenommen; siebter Fall.** Ihr habt konsequenterweise in den TB-91-Belegen gesucht.

**C9 (i) — „Lesehaken erst TB-95" gegen 39.6/39.8** · Art: nach Messung
eingetragen · Quelle: 24d Abschnitt 3

> **Der Widerspruch:** Ihr schreibt *„Der Lesehaken entstand erst mit TB-95."* Das Register sagt in 39.6 (Tabelle, Zeile „Lesequellen") über TB-92 A1b: *„Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (11 Prozesse): 0 Lesezugriffe auf `data/` oder `config/` des Repos; 222 CSV und 2 Universumsdateien aus dem Snapshot. Dazu Eingaben ausserhalb des Snapshots — 39.8"* — und 39.8 heisst *„Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand"* und nennt als Beleg `docs/belege/TB-92/a1b_lesequellen_kinder.txt`. **Das habe ich im Register gelesen, nicht im Repo gemessen.** Eines von beiden stimmt nicht: entweder existiert dieser Beleg mit diesem Inhalt (dann ist eure Aussage falsch und der Haken ist vom 23.09., TB-92), oder er existiert nicht (dann ist 39.6 falsch, und das wäre ein Registerbefund). *[Voraussetzung, zu messen: `docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4.]*

**Die Messung — der Widerspruch geht zugunsten des Registers auf:**
`docs/belege/TB-92/a1b_lesequellen_kinder.txt` (1756 B) und
`docs/belege/TB-92/a1b_lesehaken.py` (858 B) existieren, beide hinzugefügt mit
`0292e92` am 23.09.2026, 18:42; die Datei beginnt mit „== Lauf 3" und führt die
Zugriffe je Datei. ⇒ **Der Lesehaken stammt von TB-92; 39.6 und 39.8 hatten
recht. Der Satz „erst mit TB-95" war ein Fehler des steuernden Chats** — eine
Nummer übernommen statt geprüft (`docs/projektfuehrung/UEBERGABE_2026-09-25.md`,
Block 7 Nr. 1). Fable dazu, 25a Abschnitt 1 (3), zeichengleich:
„**(3) Der Lesehaken ist von TB-92; euer Satz war falsch, das Register hatte recht.** Angenommen, und die Ursache benennt ihr richtig: eine Nummer übernommen statt geprüft — meine falsche Nummer, eure ungeprüfte Übernahme, eine Kette."
Und die Folge: „Die Folgerung steht: Der Benchmark-Nachweis ist 2 aus seinem eigenen Protokoll; führbar nach beiden Eingaben, dann als Neurechnung mit beiden Teilen."
Marke bei 39.8.

