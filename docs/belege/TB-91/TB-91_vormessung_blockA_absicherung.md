TB-91 Block A — Vormessung des steuernden Chats: benchmark.py nach 36.1 abgesichert
================================================================================
Zeitpunkt: 2026-09-23 10:55:30 UTC
HEAD:      d23bdd13f6b1d27f0f81bfad69846a08f36be575
Womit:     Bruecken-VM (Linux, Systempython) — NICHT der Mac mit trading-env

⚠️⚠️ DAS IST EINE VORMESSUNG, KEIN NACHWEIS (Pruefprinzip A8).
     Die Mac-Sitzung misst jede Zahl nach. Weicht sie ab, gilt die Nachmessung.
     Der Befund selbst (fehlende Schreibsperre) ist davon unberuehrt — er ist
     am Quelltext abgelesen, nicht gerechnet.

--------------------------------------------------------------------------------
1. DER BEFUND, DER TB-91 AUSGELOEST HAT
--------------------------------------------------------------------------------
benchmark.py verletzte 36.1 an beiden Stellen:
  (2) Einmal-Schreibsperre : fehlte — open(ziel, "w"), bedingungsloses Ueberschreiben
  (3) Voreinstellung       : ergebnisse/benchmark_drawdowns.json = Sperrlistenpunkt 4

Ein blosses `python3 benchmark.py` ohne Argument haette Sperrlistenpunkt 4
ueberschrieben. Der Kommentar im Quelltext benannte diese Gefahr selbst und
liess die Voreinstellung stehen.

--------------------------------------------------------------------------------
2. HASHES VORHER / NACHHER
--------------------------------------------------------------------------------
  benchmark.py            vorher                 3960375a539de832… (Abbildstand)
  benchmark.py            nachher                d6bdd55805344da0…

  ⭐ DIE GESCHUETZTEN DATEIEN — unveraendert:
    benchmark_drawdowns.json                 a163c49814b9af0c…
    faltenplan.json                          0e54ac5cf6d554d2…
    Dateien in ergebnisse/                   12 (vorher 12)

  Der Hash von benchmark.py aendert sich PLANMAESSIG — Register 37.3.

--------------------------------------------------------------------------------
3. DER AENDERUNGSUMFANG: numstat 101 12
--------------------------------------------------------------------------------
  101	12	research/vorregistrierung/benchmark.py

  Hunk-Koepfe (die einzigen beruehrten Stellen):
    @@ -82,0 +83 @@ import argparse
    @@ -85,0 +87 @@ import sys
    @@ -294,0 +297,70 @@ def erlaubt(dd_benchmark: float, dd_toleranz: float) -> float:
    @@ -296,4 +368,10 @@ def main(argv=None):
    @@ -301 +379,3 @@ def main(argv=None):
    @@ -303,4 +383,12 @@ def main(argv=None):
    @@ -310,3 +398,4 @@ def main(argv=None):

  ⇒ Beruehrt sind: zwei Importzeilen, der Bereich NACH erlaubt(), und main().

--------------------------------------------------------------------------------
4. ⭐⭐ DIE GESPERRTEN RECHENFUNKTIONEN SIND UNBERUEHRT (AST-Vergleich)
--------------------------------------------------------------------------------
Verglichen wird der GEPARSTE Funktionskoerper (ast.dump), nicht der Text —
Kommentare und Leerzeilen koennen das Ergebnis also nicht verschleiern.

  Die vier Rechenfunktionen der Sperrlistenpunkte 4 und 6:
    bh_tagesrenditen         GLEICH   b303f69f9e9dfdc1
    drawdown_bei_exposure    GLEICH   0aa05326b1078577
    nachschlagen             GLEICH   e99ede767fd1ab08
    erlaubt                  GLEICH   b11a05fbb67b88a2

  Uebrige Funktionen:
    _schluessel              gleich
    _sha256_datei            NEU
    je_bot                   gleich
    main                     GEAENDERT
    schreibe_tabellen        NEU
    symbole                  gleich
    tagesgenau               gleich
    tagesschluss             gleich
    universumsdatei          gleich
    voreinstellung_ziel      NEU

  ⇒ Drei neue Funktionen, main() angepasst. KEINE Rechenfunktion beruehrt.

  ⚠️ BERICHTIGUNG an uns selbst: Wir zaehlten frueher `median` zu den
     gesperrten Rechenfunktionen und meldeten dafuer `0 Treffer`. Gemessen:
     `median` existiert in benchmark.py ueberhaupt nicht. Die Null bedeutete
     Abwesenheit, nicht Unberuehrtheit. Es sind VIER Rechenfunktionen, nicht fuenf.

  ⚠️ ZWEITE BERICHTIGUNG: Ein Rohtreffer `grep -c "def erlaubt"` auf dem Diff
     meldet 1, nicht 0. Gemessen ist das die HUNK-KOPFZEILE (@@ …), in der git
     die umgebende Funktion nennt — Zeichen 1–2 sind `@@`. Geaenderte Zeilen
     (+/-), die `erlaubt` nennen: 0. Der AST-Koerper ist identisch (oben).

--------------------------------------------------------------------------------
5. ⭐⭐ DIE MUTATIONSPROBE — 36.1 (2) greift
--------------------------------------------------------------------------------
Der Lauf wird bewusst auf den Sperrlistenpfad gerichtet. Er MUSS abbrechen.

  $ python3 benchmark.py --ziel ergebnisse/benchmark_drawdowns.json

  ABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben.
    Pfad:    ergebnisse/benchmark_drawdowns.json
    SHA-256: a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee
  rc=1

  Hash der Zieldatei vorher : a163c49814b9af0c…
  Hash der Zieldatei nachher: a163c49814b9af0c…  ⇒ GLEICH
  Dateien in ergebnisse/    : 12 vorher, 12 nachher

  ⭐ Der Abbruch kam OHNE Rechenzeit. Die Sperre liegt VOR der Rechnung, nicht
     dahinter — ein Lauf gegen ein vorhandenes Ziel verbraucht nichts und
     beruehrt nichts. Der Rueckgabewert ist 1, wie 36.1 (2) ihn verlangt.

--------------------------------------------------------------------------------
6. ⭐ 36.1 (3) — die Voreinstellung ist kein Sperrlistenpfad mehr
--------------------------------------------------------------------------------
  vorher : ergebnisse/benchmark_drawdowns.json          ⛔ Sperrlistenpunkt 4
  nachher: ergebnisse/benchmark_drawdowns_<UTC-Stempel>.json

  Zwei Aufrufe im Abstand von Sekunden liefern verschiedene Namen:
    benchmark_drawdowns_2026-09-23-105424.json
    benchmark_drawdowns_2026-09-23-105426.json

  Gleich dem Sperrlistennamen: False        Existiert schon: False

  ⚠️ NICHT GEAENDERT und absichtlich nicht: json.dump(..., indent=1,
     sort_keys=True). Jede Abweichung hier haette die Neurechnung mit
     _tb72.json unvergleichbar gemacht und Fables Determinismusnachweis (23b)
     entwertet.

--------------------------------------------------------------------------------
7. ⭐⭐ DER SONDENLAUF — was die Absicherung an der Sperrliste bewirkt
--------------------------------------------------------------------------------
  $ python3 shared/sperrlistensonde.py --abbild .../sperrliste_abbild_2026-09-22.json

                          TB-90 nachher        TB-91 nach Block A
  in Ordnung (0)                     1                       1
  Befund     (1)                     1                       3
  nicht pruefbar (2)                12                      10
  (ii) Registertext                  0                       0
  Rueckgabewert                      1                       1

  Befundpunkte vorher: [2]        nachher: [2, 4, 6]

  ⚠️ DIE BILANZ IST NICHT SCHLECHTER GEWORDEN. Gemessen:
     Punkt 4 und Punkt 6 nennen BEIDE dieselbe Datei — benchmark.py — und
     melden BEIDE denselben Uebergang 3960375a539d… -> d6bdd5580534….
     Es ist EIN Sachverhalt, an zwei Sperrlistenpunkten sichtbar.

  ⭐ Und hier ist das Verhalten der Sonde gemessen, das vorher nicht bekannt war:
     Beide Punkte standen vorher auf [2 NICHT PRUEFBAR], weil sie
     Nicht-Dateibezogenes nennen (Interpolationsregel; gleichgewichtete
     Tagesrenditen). Sobald eine der genannten Dateien im Hash abweicht,
     stuft die Sonde den Punkt auf [1 BEFUND] hoch.
     ⇒ Ein Punkt kann von 2 nach 1 wandern. Die Zahl der nicht pruefbaren
       Punkte ist also KEINE feste Groesse, und A2 ("konnte nicht messen ist
       ein eigenes Ergebnis") bedeutet nicht "bleibt fuer immer unmessbar".

  ⭐ Punkt 4 fuehrt beide Dateien getrennt auf:
       benchmark.py                    ABWEICHUNG   (planmaessig, 37.3)
       ergebnisse/benchmark_drawdowns.json  gleich   ⇐ DIE GESCHUETZTE DATEI
     Genau das ist der Zweck der Uebung: Der Waechter aendert sich, das
     Bewachte nicht.

  Dies ist der ZWEITE und DRITTE Anwendungsfall von 37.3. Der erste war
  faltenplan.py an Punkt 2 (seit 4daa254, TB-86) und steht unveraendert.

--------------------------------------------------------------------------------
8. WAS DIE MAC-SITZUNG NACHMESSEN MUSS
--------------------------------------------------------------------------------
  1  Den Hash von benchmark.py nachher — hier d6bdd5580534…
  2  Den AST-Vergleich der vier Rechenfunktionen (Abschnitt 4)
  3  Die Mutationsprobe, mit trading-env statt Systempython
  4  Den Sondenlauf: Bilanz 1/3/10, Befundpunkte [2, 4, 6]
  5  ⭐⭐ BLOCK B–D — die Neurechnung. SIE GEHOERT NICHT HIERHER:
        Sie muss _tb72.json in ALLEN Werten reproduzieren (Fable 23b), und eine
        fremde Python-Umgebung waere eine zweite Fehlerquelle, die den
        Determinismusnachweis entwertet. Die Vormessung hat sie deshalb
        BEWUSST NICHT gerechnet.
  6  Ob beim Aendern von benchmark.py gefragt wurde (ask statt deny)

--------------------------------------------------------------------------------
9. WAS DIESE VORMESSUNG NICHT GETAN HAT
--------------------------------------------------------------------------------
  ⛔ Keine Neurechnung — kein benchmark.py-Lauf, der etwas geschrieben haette.
  ⛔ Keine Datei in ergebnisse/ angelegt, geaendert oder geloescht (12 = 12).
  ⛔ messgroessen.py NICHT angefasst. Der schlimmere Fall (fest verdrahtet,
     kein --ziel, Ziel Abschnitt-0-eingefroren) liegt bei Fable, Anfrage 23c.
  ⛔ Kein Commit, kein Push, kein git add.
  ⛔ Das Sperrlisten-Abbild NICHT neu erzeugt — der Befund an 2/4/6 soll
     sichtbar bleiben, bis 37.3 ihn am signierten Tag aufloest.

--------------------------------------------------------------------------------
IN EINFACHER SPRACHE
--------------------------------------------------------------------------------
Das Programm, das die Vergleichstabelle rechnet, hatte eine offene Tuer: Ruft man
es ohne Zusatzangabe auf, haette es genau die geschuetzte Datei ueberschrieben,
auf die sich das ganze Register beruft. In seinem eigenen Kommentar stand, dass
das passieren wuerde. Es ist nie passiert — aber nur, weil niemand den Befehl
getippt hat.

Die Tuer ist jetzt zu, und zwar doppelt: Das Programm zielt voreingestellt auf
einen Namen mit Zeitstempel, und es weigert sich, eine vorhandene Datei
anzufassen. Beides ist geprueft — die Weigerung wurde absichtlich ausgeloest,
und die geschuetzte Datei ist danach Byte fuer Byte dieselbe.

Wichtig ist, was NICHT geaendert wurde: keine der vier Rechenfunktionen. Das ist
nicht behauptet, sondern maschinell verglichen — und zwar am geparsten Programm,
wo Kommentare nichts verstecken koennen.

Die Pruefsonde meldet jetzt drei Beanstandungen statt einer. Das sieht schlechter
aus, als es ist: Es ist dieselbe eine Datei, die an drei Stellen der Schutzliste
vorkommt, und sie soll sich geaendert haben. Die geschuetzten Ergebnisdateien
selbst sind unberuehrt — die Sonde bestaetigt das ausdruecklich.

Was noch fehlt, ist die Neurechnung. Die wurde hier bewusst NICHT gemacht: Sie
muss ein altes Ergebnis auf die Nachkommastelle genau wiederholen, und dafuer
braucht es dieselbe Programmumgebung wie damals — die gibt es nur auf dem
MacBook.
