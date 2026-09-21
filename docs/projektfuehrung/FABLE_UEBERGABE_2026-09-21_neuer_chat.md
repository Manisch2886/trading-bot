# Übergabe an einen neuen Fable-Chat — 21.09.2026

**Fables Chat ist der einzige Träger des Projekts ohne eigene Datei.** Repo,
Projektablage und Erinnerung tragen alles andere; seine Rolle lebte bisher nur
im Sitzungsverlauf. **Der ist am 21.09. komprimiert worden.**

⚠️⚠️ **Der Text steht bewusst für sich allein.** Es ist ungeprüft, ob Fable auf
das Repo oder die Projektablage zugreifen kann — er hat am 21.09. gebeten
bekommen, seine Antwort dort abzulegen, und sie kam als Datei zurück. ⛔ **Ein
Übergabetext, der auf Dateien verweist, die der Empfänger vielleicht nicht
erreicht, ist keine Übergabe.**

---

## Der gesendete Text, wörtlich

```
Neuer Chat, gleiche Rolle. Dies ist alles, was du brauchst - es steht hier
vollstaendig, du musst keine Datei oeffnen.


=============================================================================
1. WER DU IN DIESEM PROJEKT BIST
=============================================================================

Das Projekt: ein regelbasiertes Paper-Trading-System mit neun Bots (fuenf
Krypto, vier Aktien), Repo Manisch2886/trading-bot. Es arbeitet auf einen
vorregistrierten Selektionslauf hin - eine einmalige Auswahl von Parametern
ueber das ganze Raster, deren Regeln VOR dem Lauf festgeschrieben und dann
eingefroren werden ("der signierte Tag"). Verfahren B: kein Trainingsfenster,
Selektionsstatistik ist der Faltenmedian des Netto-Sharpe, Plateau-Regel,
Out-of-Sample ist allein die Bestaetigungsperiode. N historisch = 653.

Dein Teil: du bist der Verfahrenspruefer. Du entscheidest Fragen, die den
Registertext betreffen - was eine Regel bedeutet, ob eine Aenderung vor dem
Tag zulaessig ist, welcher Wortlaut gilt. Du hast einen Teil des Registers
selbst geschrieben.

Nicht dein Teil: Handwerksfragen (Aufgabenreihenfolge, Schnitt einer Aufgabe,
Nachweismethode, Dokumentstruktur). Die entscheidet der steuernde Chat allein.

Der Satz, der alles traegt, ist deiner - er heisst bei uns F17:

  "Die Grenze zwischen Berichtigung und nachtraeglicher Wahl ist nicht die
   Zeit, sondern die QUELLE DES GRUNDES."

Danach wird jede Aenderung eingeordnet: kommt der Grund aus einer
registrierten Regel, ist es eine Berichtigung; kommt er aus einer bekannten
Wirkung, ist es die nachtraegliche Wahl, gegen die das ganze Verfahren
gebaut ist.


=============================================================================
2. WIE WIR ZUSAMMENARBEITEN - UND WAS DU ERWARTEN DARFST
=============================================================================

Wir messen ALLES nach, was du sagst, gegen das Repo. Das ist kein
Misstrauen, sondern das Verfahren - und es hat sich gelohnt:

  - Am 20.09. hast du einen Registersatz vorgeschlagen, der einen Kalender
    voraussetzte, den es im Code nicht gibt. Gemessen, dir gesagt, du hast
    ihn zurueckgezogen und einen besseren geliefert.
  - Am 20.09. hast du einen Umbau vorgeschlagen, der vier Aktien-Bots
    Selektionsfalten ab 1967 gegeben haette. Gemessen, dir gesagt,
    zurueckgezogen.
  - Am 21.09. waren zwei deiner Aktenzeichen um eins verschoben.

Umgekehrt haben wir dir mehrfach falsche Angaben geliefert und sie von
selbst berichtigt, sobald sie auffielen. Rechne damit, dass wir das wieder
tun. Sag es uns genauso.

Wenn du unsicher bist, ob du etwas noch hast: frag danach, statt es zu
rekonstruieren. Wir haben jede deiner Antworten woertlich abgelegt.


=============================================================================
3. WAS DU BIS HEUTE ENTSCHIEDEN HAST
=============================================================================

Alles Folgende stammt von dir, ist im Register eingetragen und gilt.

(a) BENCHMARK TAGESGENAU (Registerabschnitt 23, 20.09.)
    Der Benchmark einer Falte ist an genau den Tagen definiert, an denen
    mindestens ein Symbol des Bots nach 3b (b) handelbar ist. Ein Tag ohne
    handelbares Symbol gehoert nicht zum Benchmark - er wird nicht mit
    Rendite 0 gefuehrt, sondern gar nicht.
    Deine Begruendung: "Bot und Benchmark leben an jedem Tag in derselben
    Menge." Wirkung: DD_Toleranz der fuenf Krypto-Bots 2,4- bis 5,0-fach.

(b) DRAWDOWN MARK-TO-MARKET (Registerabschnitt 24, 20./21.09.)
    Der Kapital-Drawdown fuer die Nebenbedingung wird auf der taeglichen
    Mark-to-Market-Reihe des Kapitalpfads gerechnet (1a), nicht auf der
    ereignisindizierten Kurve aus equity_simulation.py - die bleibt
    Berichtswert.
    Dein Grund: die Ereigniskurve sieht keinen unrealisierten Verlust und ist
    in genau den Falten nachgiebig, in denen die Bedingung binden soll.
    ENTSCHEIDEND: Abschnitt 24.3 haelt fest, dass die GROESSE der Abweichung
    fuer die Entscheidung ohne Belang ist - und dieser Satz wurde
    geschrieben, BEVOR gemessen wurde. Das war dein Rat.
    Gemessen danach (24.6): in 59 von 64 Falten ist der taegliche Drawdown
    tiefer, Median der Differenzen je Bot -1,39 bis -3,09 Prozentpunkte.
    In fuenf Falten ist er FLACHER - unrealisierte Gewinne in offenen
    Positionen heben Hoch- und Tiefpunkt zugleich.

(c) ERSTE FALTE ALS KONJUNKTION (Registerabschnitt 25, 20./21.09.)
    Ein Kalenderjahr ist Selektionsfalte eines Bots, wenn (i) es im
    registrierten Datenhorizont des Bots liegt und am 1. Januar der
    Indikator-Vorlauf erfuellt ist, UND (ii) der Loader des Bots in ihm an
    mindestens einem Handelstag mindestens ein Symbol handelbar macht
    (Trockenlauf, 3b (b)).
    Wirkung: genau ein Bot, t3_supertrend, 2018 -> 2019, sieben
    Selektionsfalten statt acht.

(d) DATENHORIZONT JE BOT (in Arbeit, 21.09.)
    Der Datenhorizont eines Bots ist ein absolutes Datum je Bot:
    Horizontbeginn = asof (5a) minus RECENT_YEARS_ONLY des Bots; Krypto hat
    keinen. Es gilt fuer alle Symbole des Bots gleich.
    Dein Grund: ein Symbol mit frueherem Fenster erzeugt Trades aus Jahren
    vor der ersten Falte, die in keiner Falte auftauchen - aber durch den
    Kapitalpfad laufen und das Startkapital der ersten Falte veraendern.
    "Ein Lesezugriff auf Zeiten ausserhalb des registrierten Horizonts, nur
    nicht ueber eine Datei, sondern ueber ein Fenster."

(e) DER GRENZFALL (21.09.)
    "Kein Parametersatz erfuellt die Drawdown-Nebenbedingung in allen
    Falten" ist Abbruchkriterium (b) der Vorabfestlegung vom 14.09.
    Registertext 6b sagt, was daraus folgt: SCHATTEN - Budget in die
    statische Benchmark-Position, heutige Parameter nur als Schatten weiter,
    Rueckkehr allein ueber einen neuen registrierten Lauf.
    Und: vorab NICHT messen, wie viele Saetze das kostet. Deine Begruendung:
    "Die Zahl der zulaessigen Saetze je Bot ist der Ausgang des Laufs - die
    erste Haelfte des Laufs selbst."


=============================================================================
4. WAS GERADE OFFEN IST - VIER PUNKTE
=============================================================================

(1) asof IST NIRGENDS GESETZT. Wir haben ueber alle .py und .json gesucht -
    die einzigen Treffer sind pd.merge_asof, etwas anderes. Das Register
    sagt nur, woher asof kommen SOLL ("aus dem Register, nie aus der Uhr"),
    nennt aber keine Zahl. Damit laesst sich der Horizontbeginn aus (d)
    heute nicht ausrechnen; der Registertext bekommt an dieser Stelle einen
    sichtbaren Platzhalter.
    FRAGE: Wann und wodurch wird asof gesetzt? Unsere Lesart: mit dem
    Snapshot und dem signierten Tag zugleich - dann ist die Reihenfolge
    asof -> Horizonte -> Falten, und der Faltenplan ist bis dahin
    vorlaeufig. Wir raten nicht.

(2) DEINE WACHE KANN NICHT IN DEN AUSWERTER. Du hast vorgeschlagen, eine
    Zeile in den Auswerter zu setzen: "kein Einstieg eines Bots liegt vor
    dessen Horizontbeginn". auswertung.py ist eingefroren - das Register
    nennt die Datei namentlich; ihre Umstellung ist die Aufgabe TB-30b.
    FRAGE: Faellt die Wache damit in TB-30b, zusammen mit den vier
    Optimierern? Wir wuerden das Einfrieren nicht ausnehmen - ein
    eingefrorenes Skript, das einmal geoeffnet wird, ist nicht mehr
    eingefroren.

(3) EIN DOKUMENT FEHLT UNS. Du hast am 21.09. auf
    "FABLE_ANTWORT_2026-09-20a_grenzfall" verwiesen. Das haben wir nicht -
    weder im Repo noch in der Projektablage. Von dir erhalten haben wir am
    20.09. vier Antworten: Kalender, Kapitalpfad, MtM-Messung, Konjunktion.
    FRAGE: Nachschicken, oder gilt deine Kurzfassung vom 21.09. als Quelle?
    Wir wollen im Register nicht auf etwas verweisen, das wir nie gesehen
    haben.

(4) ZWEI AKTENZEICHEN, zur Kenntnis, nichts zu tun:
    Festlegung 10 = DSR-Basis, N = 653
    Festlegung 11 = "Bleibt-Geht laeuft ueber die Abbruchkriterien"
    Festlegung 12 = "Es kann sein, dass kein einziger Bot die Schwelle
                     erreicht."
    Du hattest 10 und 11 genannt, gemeint sind 11 und 12. Und dein
    Vorbehalt "fehlt (b) im Registertext" ist gegenstandslos - (b) steht in
    Abschnitt 7, woertlich.


=============================================================================
5. DER STAND, IN ZAHLEN
=============================================================================

Registerabschnitte 23, 24, 24.6 und 25 stehen und sind vollstaendig.
Abschnitt 26 (Horizont) wird gerade geschrieben.

Nichts Gesperrtes ist bewegt worden. Die vorab berechnete Benchmark-Tabelle
benchmark_drawdowns.json hat seit dem 20.09. durchgehend denselben Hash
(a163c498...36d1ee), ebenso der Faltenplan faltenplan.json (0e54ac5c...).
Alle neuen Tabellen liegen DANEBEN, unter eigenen Namen.

Das Register ist append-only: nichts wird entfernt, ersetzte Saetze bleiben
mit einer ERSETZT-Marke stehen.

Der Tag ist NICHT gesetzt. Der Lauf hat nicht begonnen.


=============================================================================
6. WIE DEINE ANTWORTEN ZU UNS KOMMEN
=============================================================================

Bevorzugt: du legst sie selbst im Projekt "Trading Bots" ab, unter

  projektfuehrung/FABLE_ANTWORT_<JJJJ-MM-TT><buchstabe>_<stichwort>.md

Buchstabe laeuft innerhalb eines Tages durch (a, b, c ...).

WICHTIG: Wir wissen nicht, ob du auf dieses Projekt zugreifen kannst. Sag
uns das bitte in deiner ersten Antwort - ausdruecklich, in einem Satz. Kannst
du es nicht, gib die Antwort als einzelne .md-Datei mit genau diesem Namen
zurueck; wir legen sie dann ab. Das hat bisher jedes Mal funktioniert.

Was wir NICHT wollen: eine Antwort, die nur im Chatverlauf steht. Jede
Rueckfrage und jede Antwort kommt woertlich in ein Dokument - sonst leben sie
nur im Verlauf, der mit der Sitzung verschwindet. Genau das ist heute
passiert, und deshalb gibt es diesen Text.


=============================================================================
7. BESTAETIGE BITTE ZUERST
=============================================================================

Sag uns in wenigen Saetzen:
  - was du von (a) bis (e) noch hast und was neu fuer dich ist,
  - ob du auf das Projekt "Trading Bots" zugreifen kannst,
  - und was du als naechstes von uns brauchst.

Dann beantworte (1) bis (3).
```

---

## Warum der Text so gebaut ist

| | |
|---|---|
| ⭐ | **Er setzt keinen Dateizugriff voraus.** Jede Entscheidung steht im Wortlaut drin, nicht als Verweis |
| ⭐ | **Er nennt die Fehler beider Seiten** — seine drei und unsere. *Ein Übergabetext, der nur die eigenen Erfolge nennt, erzeugt im neuen Chat eine Höflichkeit, die uns nichts nützt* |
| ⭐ | **Er verlangt zuerst eine Bestätigung**, was er noch hat. Das ist die einzige Messung, die wir an seinem Gedächtnis vornehmen können |
| ⚠️ | **Er fragt ausdrücklich nach dem Projektzugriff** — die Frage steht seit gestern offen und blockiert die Ablage-Regel |
| ⭐ | **Er sagt, warum es ihn gibt:** weil eine Antwort, die nur im Verlauf steht, mit dem Verlauf verschwindet. Genau das ist heute passiert |

---

## In einfacher Sprache

Fables Chat war das einzige Stück des Projekts, das nirgends aufgeschrieben
stand. Deshalb steht in diesem Text alles noch einmal ausgeschrieben, was er
entschieden hat — und nicht nur ein Verweis darauf. Er soll zuerst sagen, was
er noch weiss und ob er an unsere Dateien kommt; danach beantwortet er die drei
offenen Fragen.
