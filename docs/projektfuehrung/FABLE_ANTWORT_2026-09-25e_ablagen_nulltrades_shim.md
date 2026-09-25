# FABLE_ANTWORT 2026-09-25e — TB-107 angenommen; zwei weitere Ablagen wie `tb40_lauf_*`; „null Trades" ist ein Wert, kein Ausstieg; das alte Werkzeug bekommt den Stummel, den die Probe schon hat

*Bezug: `FABLE_ANFRAGE_2026-09-25e_tb107_abgegeben_drei_fragen.md`. Ein Ergebnis, drei Fragen. Block C (die Kopie in `faltenplan_neun.py`) ist in 25d (1) bestätigt — kein `revert`.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 25d. Ergebnisgrössen nach 27.1: keine.

---

## 1. Kenntnisnahme

`_min_history` mit `re.findall`, genau ein Treffer, sonst 2; der Hinweis-Zweig war nie der echte Pfad — gemessen, gut. Die Kopie mit Abbruch. `getattr` weg, 101 Aufrufer ohne Modus vorher = nachher. `tb40_lauf_*` erfüllt (1)–(3); dass das Aufräumen im Lese-Audit als zehn Verzeichnis-Öffnungen in (i) erscheint, ist genau der Grund, warum Klasse (iv) eine Klasse ist und keine Erlaubnis — der Audit soll diese Zugriffe als (iv) führen, nicht als (i) ausserhalb; Handwerk am Audit, klein. Laufbereich 81, nur `regimewache.py` neu. Gegenprobe aus der Messdatei, zwei Mutationen beissen allein. **Angenommen.**

---

## 2. Die drei Fragen

**(1) `tb40_faltenplan_*` und `tb40_proben_*` — wie `tb40_lauf_*`.** Eure Neigung ist richtig: Klasse (iv) fragt nicht, welcher Lauf den Ordner anlegt, sondern ob ein Modul des Laufbereichs Ablagen hinterlässt. Dass `hole_faltenplan()` ohne JSON von keinem gemessenen Lauf-Typ gerufen wird, ist eine Tatsache über heute; der Laufbereich wird am Tag gemessen. Kleiner Auftrag, dieselbe Bauart (`finally`, Pfad in der Meldung, wenn kein Ergebnis).

**(2) Zehn Stellen `if trades.empty: exit()` — die Abgrenzung „nach einer Rechnung" ist nicht das Kriterium, und diese Stellen sind ein Befund.** Das Kriterium aus 36.5 ist: **Kein Aufruf endet mit 0, ohne dass gemessen wurde** — und „gemessen" heisst hier: das Ergebnis ist geschrieben. Ein Skript, das bei null Trades ohne Ausgabe mit 0 endet, ist für den Aufrufer von „gerechnet und geschrieben" nicht unterscheidbar; das ist die TB-45-Klasse, gleich ob die Leere aus fehlender Eingabe oder aus einer Rechnung stammt. **Und das Register sagt, was null Trades sind:** ein Wert. 5.1 Nr. 8 (*„Falten ohne Trade zählen mit Sharpe 0"*) und Registertext 1c (*„Ist die Standardabweichung 0 (kein Trade in der Falte), ist der Falten-Sharpe 0"*) machen „keine Trades" zu einem Ergebnis, das in die Statistik eingeht — nicht zu einem Grund, aufzuhören.

> **Ergänzung zu 24b A2 / 36.5 — null Trades:** Ein Lauf des Laufbereichs, der keine Trades findet oder ausführt, schreibt dieses Ergebnis (leere Liste, Sharpe 0 nach 1c) und endet mit 0; er endet nie ohne Ausgabe. Unter dem Modus endet ein `exit()` ohne geschriebenes Ergebnis mit 2, gleich was ihm vorausgeht.

*Quelle des Grundes:* 5.1 Nr. 8, 1c, 36.5. Kein Ergebnis. Umsetzung: die Gegenprobe (`test_main_gegenprobe.py`) zählt künftig jedes `exit()` ohne vorherige Ausgabe, nicht nur die nach fehlender Eingabe; die zehn Stellen bekommen die Modus-Abfrage wie die vierzehn. Dass `__main__` heute von keinem Lauf-Typ erreicht wird, ändert daran nichts — dieselbe Lage wie bei (c). Für den Laufcode (TB-30b) heisst es: Der Erzeuger schreibt für eine Zelle ohne Trades die Nullzeile, nie nichts.

**(3) `pfadvergleich.py` — der Stummel, wie bei Probe A.** Eure Neigung trifft, mit dem Grund, den ihr nennt (ein Werkzeug, das dauerhaft 1 meldet, verwässert 1), und mit einer Bedingung: Der Stummel wird als solcher benannt (*„Fassung TB-52 plus `selektionsmodus = lambda: False`, weil der heutige Nachbar die Funktion verlangt"*) — das Werkzeug vergleicht dann weiter, was es vergleichen soll (Pfadauflösung), und behauptet nicht, TB-52 habe die Funktion gehabt. Dass `test_paths` Probe A genau das schon tut, ist der Konsistenzgrund. Das Werkzeug liegt ausserhalb des Laufbereichs; Live-Freigabe wie gehabt.

---

## 3. Auf Register 41/42, zusätzlich

| | Eintrag |
|---|---|
| a | Tatsachennotizen TB-107: `_min_history` genau ein Treffer; Kopie mit Abbruch; `getattr` weg; `tb40_lauf_*` nach (iv) erfüllt; Laufbereich 81 Module am Stand `f61bd97`; Gegenprobe aus der Messdatei |
| b | Klasse (iv): das Aufräumen erscheint im Audit als (iv), nicht als (i) ausserhalb (Handwerk am Audit) |
| c | Ergänzung „null Trades ist ein Wert" (2); die zehn Stellen wie die vierzehn; Gegenprobe erweitert |
| d | `pfadvergleich.py`: Stummel, benannt (3) |

---

**Kurz:** TB-107 angenommen. Die zwei weiteren Ablagen werden wie `tb40_lauf_*` behandelt. Null Trades ist nach 5.1 Nr. 8 und 1c ein **Wert** — ein Skript, das dabei ohne Ausgabe mit 0 endet, ist TB-45; die zehn Stellen bekommen die Modus-Abfrage, die Gegenprobe zählt jedes `exit()` ohne Ausgabe. Das alte Werkzeug bekommt den benannten Stummel, wie Probe A.

**Unsicher:** nichts, was eine Entscheidung trägt.

---

## In einfacher Sprache

Der Auftrag ist angenommen. Zwei weitere Zwischenordner werden aufgeräumt wie der erste. Die zehn Stellen, die bei null Geschäften still mit „fertig" enden, sind ein Befund: Null Geschäfte ist im Regelwerk ausdrücklich ein Ergebnis mit dem Wert 0, kein Grund aufzuhören — ein Programm, das dann nichts schreibt, ist von einem unterscheidbar, das gerechnet hat, und genau das darf nicht sein. Das alte Prüfwerkzeug bekommt den kleinen Aufsatz, den ein Test schon benutzt, damit es nicht dauerhaft einen Fehler meldet, der keiner ist.
