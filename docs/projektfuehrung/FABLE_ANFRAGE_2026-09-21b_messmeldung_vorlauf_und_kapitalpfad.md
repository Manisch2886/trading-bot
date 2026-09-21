# Anfrage an Fable 5.1 — 21.09.2026, 18:50: Messmeldung zu 21c 3.1 und 3.2

**Erste Anwendung der neuen Regel** (`UEBERGABE_2026-09-19.md`, Nachtrag 4,
Ergänzung 3): *Jede Anfrage und jede Rückmeldung an Fable wird abgelegt wie seine
Antwort.* Bis heute lagen neun Antworten von ihm in der Ablage und **eine**
Anfrage von uns.

**Anlass:** 21c 3.1 und 3.2 lagen von 17:05 bis 17:50 unbearbeitet, weil der
steuernde Chat die Datei nur als Zusammenfassung kannte. Beide stehen vor dem
Ableiten der Falten.

**Sichtschutz:** Alle drei Messungen unten sind Verfahrensmessungen nach 27.2
(Kalender, Registertext, Feldnamen eines Plans). Keine Kennzahl je
Parametersatz, keine Erwartung über den Ausgang.

---

## Der gesendete Text, wörtlich

```
Messmeldung zu 21c 3.1 und 3.2. Drei Messungen, alle Verfahrensseite nach
27.2. Vorab: 21c 3.1 und 3.2 lagen bei uns fast eine Stunde unbearbeitet,
weil wir deine Datei nur als Zusammenfassung kannten und nicht im Wortlaut
gelesen hatten. Unser Fehler, nicht deiner.


(A) ZU 3.1 - DEIN BEFUND TRIFFT, UND SCHAERFER ALS DU VERMUTEST.

Der Satz "Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den
ersten Kurs im Bestand" steht im Register genau EINMAL: Zeile 4307. Und zwar
INNERHALB des Zitats deiner Fassung vom 20.09., das in 26.2 ausdruecklich als
ersetzt gekennzeichnet ist.

Er steht also im Register ausschliesslich an der Stelle, die ausser Kraft
ist. Deine Entscheidung aus 3.1 (der Satz gilt fort, als Berichtigung) geht
so ins Register - TB-78, Punkt 4.

Dazu eine Tatsache aus 26.2, die deine Unsicherheit aufloest ("ob ich den
Satz absichtlich gestrichen habe"): Die Fassung vom 20.09. ist NIE in einen
Registertext uebernommen worden - gemessen, grep im Register: "Horizontbeginn"
0 Treffer, "4a, Praezisierung" 0 Treffer. Es gab also nichts zu streichen.
Der Satz ist zwischen zwei Antworten von dir verlorengegangen, nicht im
Register.


(B) ZU 3.2 - DAS REGISTER REGELT DEN KAPITALPFAD-BEGINN NICHT.

Gesucht nach "Kapitalpfad" in Verbindung mit Beginn/Start/1. Januar/erste
Falte: EIN Treffer, Zeile 4296, und der beschreibt den Schaden, nicht die
Regel:

  "der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem
   Kapitalstand, der aus nicht registrierten Jahren stammt."

"Startkapital" kommt im Register ueberhaupt nicht vor (0 Treffer).

Damit ist dein Vorschlag aus 3.2 NEUER Registertext, keine Berichtigung zu
einem bestehenden Satz. Wir tragen ihn als solchen ein - TB-78, Punkt 5 -
und die angepasste Wache (fruehester Einstieg >= Beginn der ersten Falte,
drei Daten je Bot im Bericht) ersetzt in TB-30b die Fassung aus 21b.


(C) ZU DEINER MESSBITTE - NICHT BEANTWORTBAR, UND DER GRUND IST WICHTIGER
    ALS DIE FRAGE.

Du batest zu messen, ob faltenplan.json (0e54ac5c...) den Vorlauf gegen den
Horizontbeginn rechnet. An dieser Datei laesst sich das nicht entscheiden:

  - Sie fuehrt je Falte ein Feld training_bis_ausschliesslich (Beispiel:
    "2018-12-14") und ein Feld embargo_tage: 18. Verfahren B hat ausdruecklich
    KEIN Trainingsfenster. Die Datei stammt aus einem anderen Verfahrensstand.
  - Die erste Selektionsfalte von turtle_soup_stocks steht dort auf 2019 -
    nicht auf 2017 oder 2018, wie deine Frage unterstellt.
  - TB-72 hat einen neuen Plan DANEBEN gelegt (faltenplan_tb72.json). Der
    gesperrte Plan ist unberuehrt, aber er ist nicht der Plan nach 4a.

Nach unserem Prinzip A2 ist "nicht pruefbar" ein eigenes Ergebnis, kein
fehlendes. Wir melden es deshalb so, statt eine Zahl zu liefern, die aus der
falschen Datei stammt.

EINE FRAGE DARAUS, und sie ist groesser als 3.1: Wenn der gesperrte
faltenplan.json Felder eines Verfahrens traegt, das wir nicht mehr fahren -
was ist er dann noch? Sperrlistenpunkt 2 nennt ihn namentlich. Bleibt er
gesperrt als historischer Stand, oder muss der Plan nach 4a ihn ersetzen und
selbst auf die Sperrliste? Das ist eine Verfahrensfrage, und sie faellt vor
den Tag.


(D) ZWEI SACHEN ZUR KENNTNIS.

1. Deine Regel aus 21h nehmen wir an und wenden sie auf uns an: Wir legen dir
   Aktenzeichen ab jetzt nur noch mit dem ganzen Eintrag vor.

2. Du hattest in 21c 3.3 gemeldet, unsere Rueckmeldung von 16:24 liege in
   keinem Traeger. Gemessen: das gilt fuer fast alles von unserer Seite - du
   hast neun Antworten abgelegt, von uns lag EINE Anfrage in der Ablage.
   Neue Regel bei uns: jede Anfrage und jede Rueckmeldung an dich wird
   abgelegt wie deine Antwort. Diese hier ist die erste, die danach entsteht;
   die drei fehlenden von heute werden nachgelegt.

Wir ziehen gerade in einen neuen steuernden Chat um. Deine Antwort auf (C)
liest dort jemand, der dieselbe Uebergabe kennt wie du.
```

---

## In einfacher Sprache

Drei Messungen als Antwort auf Fables letzte beiden Punkte: Sein Befund zum
verlorenen Satz stimmt — der Satz steht nur noch an der Stelle, die für
ungültig erklärt wurde. Seine zweite Regel ist neuer Text, kein Flicken an
etwas Bestehendem. Und die Messung, um die er gebeten hatte, lässt sich nicht
durchführen, weil die betroffene Datei aus einem früheren Verfahren stammt —
was eine grössere Frage aufwirft als die ursprüngliche: was diese gesperrte
Datei heute überhaupt noch ist.
