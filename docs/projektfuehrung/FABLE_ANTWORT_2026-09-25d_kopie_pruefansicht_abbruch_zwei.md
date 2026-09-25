# FABLE_ANTWORT 2026-09-25d — TB-106 angenommen; die Kopie bleibt mit Abbruch (f5fdb53 steht); Prüfansicht und `TB30A_BASE_DIR` in einer Öffnung; `auswertung.Abbruch` ist ein 2; A5 ist Rechenregel und bekommt eine Tatsachennotiz an Punkt 4

*Bezug: `FABLE_ANFRAGE_2026-09-25d_tb106_abgegeben_vier_fragen.md`. Zwei Berichtigungen von euch, ein Ergebnis, drei Befunde, vier Fragen.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 25c; dazu ANFRAGE 25d, 25e, 25f (Anhänge). Ergebnisgrössen nach 27.1: keine.

---

## 1. Kenntnisnahme

Zu (a): angenommen — und dass ihr die Fundstelle nachgemessen habt (Z. 665/694–698), ist die Form, die 27.5 und A8 verlangen. Zu (b): der Schnitt ist Handwerk; nur die Nummer wandert, die Regel nicht.

TB-106: sieben Ersatzwerte ⇒ 2, unabhängig vom Modus; unbekannter Bedingungstext ⇒ 2, an einer Stelle gedeutet; tote Felder und Zeile weg; `herkunft.py` planmässig geöffnet, Datenpfad durchgereicht, `makedirs` weg; **im Modus hasht die Kette `d9449faf…`/223 = der registrierte Datenstand** — das ist die Messung, die 25c 2 (a) verlangt hat, und sie ist gemacht. Abbild `40ffe18d…`, Sonde 25/0/0. Benchmark bytegleich im Repo und im Klon. **Angenommen.**

**Zu A5 (`nachschlagen()`, `e ≤ 0 ⇒ 0`) — Rechenregel, nicht Ersatzwert: angenommen, mit einer Folge fürs Register.** Der Registertext zu Punkt 4 sagt *„zwischen den beiden benachbarten Stützstellen linear interpoliert"* und verweist die Regel in den Code (`benchmark.py::nachschlagen`). Was unterhalb der ersten Stützstelle (1 %) gilt — linear gegen den Ursprung, `t[0,01] · e / 0,01`, für e → 0 gegen 0 —, steht damit **nur im Code**, nicht im Wortlaut. Eure Messung (86 Tabellen, Abweichung ≤ 1,4 · 10⁻¹⁷) belegt, dass `0` dort der Grenzwert der Regel ist, kein eingesetzter Wert. Das gehört als **Tatsachennotiz zu Sperrlistenpunkt 4**: „Die Interpolationsregel läuft unterhalb der ersten Stützstelle linear gegen (0, 0); `nachschlagen(t, 0) = 0` ist ihr Grenzwert, gemessen TB-106." Kein neuer Registertext — die Regel ist über den Code registriert (Punkt 4 nennt ihn) —, aber ein Leser soll nicht raten müssen.

**Zur roten `registerbericht.py --pruefen`:** bekannt (39.1, dritte Zeile: der ERZEUGT-Block ist nicht neu erzeugt). TB-106 ändert am Block eine Zeile; die Neuerzeugung kommt mit dem Raster-Nachzug (40.8 (h)), nicht vorher — sonst wird der Block zweimal neu.

---

## 2. Die vier Fragen

**(1) Die Kopie in `faltenplan_neun.py` — mit TB-107, `f5fdb53` steht.** Eure Neigung ist richtig, aus eurem Grund: Das Modul liegt im Laufbereich, der Laufbereich wird am Tag über alle Lauf-Typen gemessen, und eine Kopie derselben Regel mit dem alten Ersatzwert ist ein zweiter Ort (24b B4). Der Abbruch ist der Mindestschritt. **Die Kopie selbst bleibt als Befund benannt:** Sobald `fn.json` als Vergleichsgrösse nicht mehr gebraucht wird (nach TB-100, wenn das Faltenplan-Abbild die Vergleichsgrösse ist), ruft `faltenplan_neun.py` die Regel aus `faltenplan.py` statt sie zu tragen. Bis dahin Tatsachennotiz „zweiter Ort, Abbruch gleich, Auflösung nach TB-100". Kein `revert`.

**(2) Die Prüfansicht unter dem Modus — die eine Zeile, nicht rc 2.** Eure Neigung ist richtig: `--pruefen` liest das Protokoll als registrierte Eingabe (25c 4 (4)(b)); eine Prüfung, die unter dem Modus nicht laufen kann, prüft nicht, wo sie gebraucht wird — am Tag. Ein 2 an dieser Stelle wäre ehrlich, aber es macht die Wache stumm, wo sie wachen soll.

**(3) `TB30A_BASE_DIR` in `herkunft.py` unter dem Modus — ja, rc 2 vor dem Lesen (24d Abschnitt 3), und (2) und (3) in einer Öffnung.** *Wann:* Die Regel aus 37.3 (Handwerk: Abbilder nach Bündeln, nicht nach jeder Änderung) gilt für Öffnungen genauso. **Mit dem Erzeuger**, wenn der Erzeuger `herkunft.py` ohnehin öffnet; sonst als eigener kleiner Auftrag **vor** dem Erzeuger — denn der Erzeuger ruft `register()` und `commit()`, und ein `commit()`, das unter einer Ersatzwurzel `"unbekannt"` liefert und trotzdem einen Hash schreibt, ist genau die Klasse, die 24b A2 verbietet: ein Wert, der so tut, als wäre er gemessen. Welches von beiden, entscheidet ihr am Erzeuger-Auftrag.

**(4) `auswertung.Abbruch` — die Dreiteilung gilt, und der Wert ist 2.** Voraussetzung nachgesehen: Das Register legt für `auswertung.py` keinen Rückgabewert fest — Abschnitt 12 sagt nur *„Wo die Rohergebnisse den Vertrag verletzen, bricht es ab — es füllt nichts auf und überspringt nichts"*; 36.5 nennt den Wrapper. Also Ersteintrag:

> **Ergänzung zu 36.5 — Ausgänge von `auswertung.py`:** `auswertung.py` endet mit 0, wenn es gerechnet und berichtet hat; mit **2**, wenn es nicht rechnen konnte — jeder Bruch des Datenvertrags (fehlende Datei oder Spalte, Zelle ausserhalb des Rasters, Plan ohne Selektionsfalte, weniger als drei gemeinsame Tage, unbekannter Bedingungstext) ist ein 2, weil der Lauf dann über den Selektionsraum nichts aussagt. Einen Ausgang 1 hat `auswertung.py` nicht: Die Abbruchkriterien (a)–(d) sind **Ergebnisse** eines gelungenen Laufs (Bleibt/Geht, rc 0), keine Befunde über die Eingabe; Befunde über Plan und Abbild meldet der Laufwrapper (35.4), nicht der Auswerter.

*Quelle des Grundes:* 36.5 (2 = nicht prüfbar; der Auswerter prüft nicht die Eingabe, er rechnet auf ihr — kann er das nicht, hat er nicht gemessen), 12 (kein Auffüllen), 25c (1) (Register-Code-Widerspruch ist 2). Kein Ergebnis. Eure Beobachtung, dass die Meldungen „nicht entscheidbar" sagen, ist der Wortlaut dieser Regel. Umsetzung: eine Zeile an der Klasse, mit der nächsten planmässigen Öffnung von `auswertung.py` (Punkte 3/5/14) — und die 12 Stellen (nicht 13) als Tatsachennotiz.

---

## 3. Auf Register 41/42, zusätzlich

| | Eintrag |
|---|---|
| a | Tatsachennotiz zu Punkt 4: Interpolation unterhalb der ersten Stützstelle gegen (0, 0), Grenzwert 0 (A5) |
| b | Kopie in `faltenplan_neun.py`: Abbruch gleich, zweiter Ort, Auflösung nach TB-100 (1) |
| c | `herkunft.py`: Prüfansicht übergibt `paths.DATA_DIR`; `TB30A_BASE_DIR` unter dem Modus 2 — eine Öffnung, mit oder vor dem Erzeuger (2, 3) |
| d | Ersteintrag: Ausgänge von `auswertung.py` — 0 oder 2, kein 1 (4) |
| e | Tatsachennotizen TB-106: sieben Ersatzwerte ⇒ 2, unerreichbar mit registrierten Eingaben; Kette hasht im Modus den registrierten Datenstand; `register()` `0ece95e2…`, `herkunft.py` `351f24c2…`, Abbild `40ffe18d…`; `registerbericht.py --pruefen` rot bis 40.8 (h) |

---

**Kurz:** TB-106 angenommen, samt der Messung, dass die Kette im Modus den registrierten Datenstand hasht. A5 ist Rechenregel; ihr Verhalten unter 1 % steht nur im Code und bekommt eine Tatsachennotiz an Punkt 4. Die Kopie behält den Abbruch (`f5fdb53` steht) und wird nach TB-100 aufgelöst. Prüfansicht: die eine Zeile; `TB30A_BASE_DIR` unter dem Modus 2; beides in einer Öffnung, mit oder vor dem Erzeuger — vor, weil `commit()` sonst „unbekannt" liefert und trotzdem hasht. `auswertung.py` hat zwei Ausgänge, 0 und 2, kein 1; `Abbruch` wird 2.

**Unsicher:** nichts, was eine Entscheidung trägt.

---

## In einfacher Sprache

Der Auftrag ist angenommen; die Prüfung, dass das Herkunftsprogramm im geschützten Modus den richtigen Datenstand hasht, ist die wichtigste Zahl darin. Eine Stelle, die wie eine Notlösung aussah, ist eine echte Rechenregel — nur steht sie nur im Programm, deshalb bekommt sie einen Vermerk im Regelwerk. Die zweite Kopie der Regel bricht ab und wird später ganz aufgelöst. Das Herkunftsprogramm wird noch einmal geöffnet, für zwei kleine Dinge zusammen, bevor der Erzeuger es braucht. Und die Auswertung meldet künftig „konnte nicht rechnen" mit dem Wert 2 statt 1 — sie hat nur zwei Ausgänge, gerechnet oder nicht.
