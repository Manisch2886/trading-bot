TB-93 Vormessung — messgroessen.py nach 36.1 abgesichert
================================================================================
Zeitpunkt: 2026-09-23 14:32:48 UTC
HEAD:      02f257428577460f1af661d1867f6af5b2f3effa
Womit:     Bruecken-VM (Linux, Systempython) — NICHT der Mac mit trading-env
Anlass:    Fable, Antwort 23c, Abschnitt 2 — Entscheidung: AENDERN

⚠️⚠️ VORMESSUNG, KEIN NACHWEIS (Pruefprinzip A8). Die Mac-Sitzung misst nach.
     ⛔ Der DETERMINISMUSNACHWEIS fehlt hier bewusst — siehe Abschnitt 6.

--------------------------------------------------------------------------------
1. FABLES UNSICHERHEIT AUS 23c — BEANTWORTET
--------------------------------------------------------------------------------
  Er schrieb: "Unsicher: ob messgroessen.py ausser ergebnisse/messgroessen.json
  weitere Dateien schreibt (dann gilt die Sperre fuer jede) - heute misst es
  der Auftrag."

  GEMESSEN, per AST ueber das ganze Modul (300 Zeilen):
    open()-Aufrufe:  Z. 88 lesend, Z. 283 SCHREIBEND  — sonst keiner
    json.dump:       Z. 284 — genau einer
    to_csv/to_json/write_text/os.open: keine

  ⇒ GENAU EIN SCHREIBZIEL. Die Sperre betrifft eine Datei, nicht mehrere.

--------------------------------------------------------------------------------
2. DER BEFUND, DEN DIE AENDERUNG BEHEBT
--------------------------------------------------------------------------------
  vorher, Z. 282-285:
      ziel = os.path.join(ERGEBNISSE, "messgroessen.json")   # fest verdrahtet
      with open(ziel, "w", encoding="utf-8") as f:            # ohne Sperre

  ⛔ Kein argparse im ganzen Modul (gemessen: 0 Treffer) — es gab keinen Weg,
     woanders hinzuschreiben. Wer es aufrief, ueberschrieb.
  ⚠️ Und das Ziel steht in herkunft.py::EINGEFROREN (Z. 60).

--------------------------------------------------------------------------------
3. HASHES
--------------------------------------------------------------------------------
  messgroessen.py   vorher           5f7075003c9dc291…
  messgroessen.py   nachher          623f8d771ffd5ae9…

  ⭐ DIE EINGEFRORENE DATEI — unveraendert:
    ergebnisse/messgroessen.json   2a9b91660a42f06a…
    Dateien in ergebnisse/         13 (vorher 13)

  numstat: 66	6	research/vorregistrierung/messgroessen.py
  ⚠️ Der Hash von messgroessen.py aendert sich planmaessig — 37.3.
  ⚠️ messgroessen.py steht SELBST in EINGEFROREN (Z. 59) ⇒ der Register-
     Gesamthash in herkunft.json wandert mit. Fable nennt das in 23c
     ausdruecklich: "planmaessig, vor dem Tag, benannt".

--------------------------------------------------------------------------------
4. ⭐⭐ FABLES BEDINGUNGEN, EINZELN GEMESSEN
--------------------------------------------------------------------------------
  (a) --ziel mit Zeitstempel-Voreinstellung (36.1 (3))          ✔
      Voreinstellung: ergebnisse/messgroessen_<UTC-Stempel>.json
      Gleich dem eingefrorenen Namen: False

  (b) O_CREAT|O_EXCL, Rueckgabe 1 VOR jeder Rechnung (36.1 (2)) ✔
      Die Existenzpruefung steht am Anfang von main(), vor universum()
      und je_zeitrahmen(). Ein Lauf gegen ein vorhandenes Ziel
      verbraucht nichts. Meldung: "nichts gerechnet, nichts geschrieben".

  (c) Messfunktionen per AST unveraendert                       ✔
      Verglichen wird der GEPARSTE Funktionskoerper (ast.dump),
      nicht der Text — Kommentare koennen nichts verschleiern.
        universum        GLEICH   2d965f89ddb1cc7a
        lies             GLEICH   1fe1f3e06e3082c2
        rsi              GLEICH   1b32d92b34641a0b
        adx              GLEICH   0b08e4665ec0992c
        rma              GLEICH   2db2f1415f91e965
        je_zeitrahmen    GLEICH   39c73ee202010241
        haltedauern      GLEICH   383bbc08dd240f89
        datenbereiche    GLEICH   0a49da24f614a678

      Neu: _sha256_datei, voreinstellung_ziel, schreibe_messgroessen
      Geaendert: main  ⇒ KEINE Messfunktion beruehrt.

  (d) Ausgabeformat unveraendert                               ✔
      Der json.dump-Aufruf, per AST verglichen:
        vorher  Z.284  json.dump(mess, f, indent=2, ensure_ascii=False, sort_keys=True)
        nachher Z.288  json.dump(mess, f, indent=2, ensure_ascii=False, sort_keys=True)
      ⇒ ZEICHENGLEICH, nur die Zeilennummer wandert.
      Der abschliessende f.write("\\n") steht unveraendert: 1 Treffer vorher wie nachher.

      ⚠️ Ein grep auf 'indent=2' meldet jetzt 2 statt 1 Treffer. Der zweite
         steht im DOCSTRING der neuen Funktion, wo er erklaert, warum das
         Format nicht angetastet werden darf. Der AST-Vergleich oben ist
         der belastbare Nachweis, nicht die Trefferzahl.

  (e) Mutationsprobe auf den eingefrorenen Pfad                 ✔

      $ python3 messgroessen.py --ziel ergebnisse/messgroessen.json

      ABBRUCH (36.1 (2)): Ziel existiert, nichts gerechnet, nichts geschrieben.
        Pfad:    ergebnisse/messgroessen.json
        SHA-256: 2a9b91660a42f06a33e3582b52359a3fba305c2e0da3b0a383fe5338036928c8
      rc=1

      Hash vorher : 2a9b91660a42f06a…
      Hash nachher: 2a9b91660a42f06a…   ⇒ GLEICH
      Dateien     : 13 vorher, 13 nachher

      ⭐ Der Abbruch kam OHNE Rechenzeit. Bei diesem Modul ist das mehr wert
         als bei benchmark.py: je_zeitrahmen() laeuft ueber alle Symbole
         aller Zeitrahmen.

--------------------------------------------------------------------------------
5. ⛔ WAS FEHLT: DER DETERMINISMUSNACHWEIS
--------------------------------------------------------------------------------
  Fable, 23c: "ein Lauf mit --ziel auf einen neuen Pfad reproduziert
  ergebnisse/messgroessen.json BYTEGLEICH - sonst Befund und Stopp."

  ⛔ NICHT GEMESSEN, und zwar mit Absicht (A2):
     (1) Er verlangt einen echten Lauf. Der rechnet ueber alle Symbole und
         legt eine Datei in ergebnisse/ an — einem Ordner unter
         Sperrlisten-Aufsicht. Das ist keine Vormessung mehr.
     (2) Die Bruecken-VM ist nicht der Mac. Dieselbe Begruendung wie bei
         TB-91 Block B: eine fremde Python- und Paketfassung ist eine
         zweite Fehlerquelle, die einen Bytevergleich entwertet.

  ⇒ Der Nachweis gehoert auf den Mac mit trading-env. Er ist der Kern
    des Auftrags TB-93, nicht dieser Vormessung.

--------------------------------------------------------------------------------
6. ⛔ WAS DIESE VORMESSUNG NICHT GETAN HAT
--------------------------------------------------------------------------------
  ⛔ Kein Lauf von messgroessen.py, der etwas geschrieben haette.
  ⛔ Keine Datei in ergebnisse/ angelegt, geaendert oder geloescht (13 = 13).
  ⛔ herkunft.py NICHT angefasst — EINGEFROREN unveraendert.
  ⛔ Kein Commit, kein Push.
  ⛔ Das Sperrlisten-Abbild NICHT neu erzeugt.

--------------------------------------------------------------------------------
IN EINFACHER SPRACHE
--------------------------------------------------------------------------------
Das Programm, das die Messgroessen berechnet, war der schlimmere der beiden
ungesicherten Faelle: Es schrieb fest auf eine geschuetzte Datei und hatte
nicht einmal die Moeglichkeit, woanders hinzuschreiben. Der Verfahrenspruefer
hat entschieden, dass es abgesichert wird.

Das ist jetzt geschehen: Das Programm nimmt einen Zielpfad entgegen, zielt
voreingestellt auf einen Namen mit Zeitstempel, und es weigert sich, eine
vorhandene Datei anzufassen — und zwar BEVOR es zu rechnen anfaengt. Die
Weigerung wurde absichtlich ausgeloest und hat gehalten.

Keine der acht Messfunktionen wurde angetastet. Das ist maschinell verglichen,
am geparsten Programm, wo Kommentare nichts verstecken koennen. Auch das
Ausgabeformat ist Zeichen fuer Zeichen dasselbe — das ist entscheidend, weil
der Verfahrenspruefer verlangt, dass ein neuer Lauf die alte Datei Byte fuer
Byte wiederholt.

Genau dieser Nachweis fehlt hier noch, und er fehlt mit Absicht: Er verlangt
einen echten Rechenlauf, und der gehoert auf das MacBook — nicht in diese
Arbeitsumgebung, die eine andere Programmfassung hat.
