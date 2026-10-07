# REGISTER-KOPIE Teil 4 von 5 — Abschnitte 43–53 — Commit ad1fc0d3e5397cec6eb75c5e62de3b1bb7868c24 — 2026-10-07 — Original sha256 ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd — KOPIE, nicht das Register

## 43. Ausgänge der Auswertung, null Trades als Wert, die zweite Öffnung von `herkunft.py` — die Einträge aus Fable 25d und 25e und die Tatsachennotizen TB-108 und TB-109 (TB-110, 26.09.2026)

### 43.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **41.0**.
Der Verfahrensprüfer hat am 25.09.2026 zwei weitere Antworten gegeben, 25d
(auf das Ergebnis TB-106) und 25e (auf das Ergebnis TB-107). Beide überschreiben
ihre Liste für das Register mit „Auf Register 41/42, zusätzlich"; 41 und 42
waren da schon eingetragen (TB-108, `f4d3e2a`). **Die Einträge stehen deshalb
hier, in 43.** Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-110_register_43.md`, Freigabe des Betreibers
25.09.2026, 23:04), nicht Fable; eine andere Zuordnung wäre eine Umnummerierung
mit Vermerk, keine Änderung der Einträge.

**Die Kette zu 42:** 42.6 führt unter (1) und (2) „Fable 25d" und „Fable 25e"
als offen, mit dem Ziel „Abschnitt 43". **Beantwortet in 43.1 (25d) und 43.2
(25e).** 42.6 (3), Fable 25f (Gesamtanalyse), bleibt offen; ⛔ nichts aus 25f
steht hier. Die Zeilen in 42.6 bleiben zeichengleich; eine Marke darunter
verweist hierher.

**Gliederung:** 43.1 die Einträge aus 25d · 43.2 die aus 25e · 43.3 eine
Berichtigung des steuernden Chats an 25e (3), **vorläufig** · 43.4 die
Tatsachennotizen aus TB-107 (Fables Liste), TB-108 und TB-109 · 43.5 was offen
bleibt · 43.6 was hier nicht getan wurde, mit der Liste der Marken.

**Bauart je Eintrag:** Kennung aus der Arbeitsliste des Auftrags (43-1 bis
43-15) · Fables Text **eingesetzt, nicht abgetippt** (Blockzitat; Teilzitate in
„…"), mit Quelle · Art · Stand, gemessen in TB-110
(`docs/belege/TB-110/0_stand.txt`) bzw. im genannten Ergebnisdokument, ohne
Ergebnisgrössen (27.1) · Kette. Je Zitat ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-110/d2_zitate.txt`).

⚠️ **Tatsachennotiz zur Herkunft der Quellen (wie 41.0):** Die zwei
Antwortdateien `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25d_…` und `…25e_…`
hat der steuernde Chat aus der Projektablage **abgeschrieben**, nicht byteweise
übertragen. **Die Zitate hier sind zeichengleich mit der Datei im Repo; ob diese
zeichengleich mit Fables Ablage ist, ist nicht gemessen.**

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag, der einen alten Satz
ergänzt oder beantwortet, steht zusätzlich als **Marke** beim alten Satz; die
Liste steht in 43.6. Die alten Sätze bleiben zeichengleich; `git diff
--numstat` auf dieses Register zeigt für TB-110 in der zweiten Spalte `0`.
⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)); die
Tatsachennotiz zu Sperrlistenpunkt 4 (43-2) steht deshalb hier, in 43.1.

### 43.1 Aus Fable 25d (`FABLE_ANTWORT_2026-09-25d_kopie_pruefansicht_abbruch_zwei.md`)

Fables Liste für das Register, 25d Abschnitt 3, zeichengleich:

> | | Eintrag |
> |---|---|
> | a | Tatsachennotiz zu Punkt 4: Interpolation unterhalb der ersten Stützstelle gegen (0, 0), Grenzwert 0 (A5) |
> | b | Kopie in `faltenplan_neun.py`: Abbruch gleich, zweiter Ort, Auflösung nach TB-100 (1) |
> | c | `herkunft.py`: Prüfansicht übergibt `paths.DATA_DIR`; `TB30A_BASE_DIR` unter dem Modus 2 — eine Öffnung, mit oder vor dem Erzeuger (2, 3) |
> | d | Ersteintrag: Ausgänge von `auswertung.py` — 0 oder 2, kein 1 (4) |
> | e | Tatsachennotizen TB-106: sieben Ersatzwerte ⇒ 2, unerreichbar mit registrierten Eingaben; Kette hasht im Modus den registrierten Datenstand; `register()` `0ece95e2…`, `herkunft.py` `351f24c2…`, Abbild `40ffe18d…`; `registerbericht.py --pruefen` rot bis 40.8 (h) |

**43-1 — Ersteintrag: Ausgänge von `auswertung.py` — 0 oder 2, kein 1** · Art:
Registertext (Ersteintrag, Ergänzung zu 36.5) · Quelle: 25d 2 (4), 3 (d)

> **Ergänzung zu 36.5 — Ausgänge von `auswertung.py`:** `auswertung.py` endet mit 0, wenn es gerechnet und berichtet hat; mit **2**, wenn es nicht rechnen konnte — jeder Bruch des Datenvertrags (fehlende Datei oder Spalte, Zelle ausserhalb des Rasters, Plan ohne Selektionsfalte, weniger als drei gemeinsame Tage, unbekannter Bedingungstext) ist ein 2, weil der Lauf dann über den Selektionsraum nichts aussagt. Einen Ausgang 1 hat `auswertung.py` nicht: Die Abbruchkriterien (a)–(d) sind **Ergebnisse** eines gelungenen Laufs (Bleibt/Geht, rc 0), keine Befunde über die Eingabe; Befunde über Plan und Abbild meldet der Laufwrapper (35.4), nicht der Auswerter.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 36.5 (2 = nicht prüfbar; der Auswerter prüft nicht die Eingabe, er rechnet auf ihr — kann er das nicht, hat er nicht gemessen), 12 (kein Auffüllen), 25c (1) (Register-Code-Widerspruch ist 2). Kein Ergebnis. Eure Beobachtung, dass die Meldungen „nicht entscheidbar" sagen, ist der Wortlaut dieser Regel. Umsetzung: eine Zeile an der Klasse, mit der nächsten planmässigen Öffnung von `auswertung.py` (Punkte 3/5/14) — und die 12 Stellen (nicht 13) als Tatsachennotiz.

*Und seine Voraussetzung, zeichengleich:* „Das Register legt für `auswertung.py` keinen Rückgabewert fest"
— Abschnitt 12 sagt nur, dass es abbricht.

**Stand, gemessen (TB-110, `0_stand.txt`):** **Nicht vollzogen.**
`research/vorregistrierung/auswertung.py` `83c6bc3c…` (letzter Commit
`5cc1de4`, TB-106) trägt `class Abbruch(SystemExit)` (Z. 118) und **12** Stellen
`raise Abbruch`; `Abbruch` endet heute mit **1** (42.4, G5; gemessen TB-106,
`docs/belege/TB-106/a10_abbruch_rc.txt`). Die Umsetzung ist eine Zeile an der
Klasse, mit der nächsten planmässigen Öffnung von `auswertung.py` (Punkte 3/5/14,
neues Abbild) — 43.5. **Die zwölf Stellen sind die Tatsachennotiz, die Fable
verlangt:** zwölf, nicht dreizehn (TB-106 A10).

**Kette:** beantwortet die Frage aus **42.4, G5** („ob 1 oder 2, ist Frage 25d
(4)") und die offene Zeile in der Marke unter **36.5** („Ob `auswertung.Abbruch`
mit 1 statt 2 endet, ist offen"). Beide Sätze bleiben zeichengleich. **Marken
am alten Ort:** unter **36.5** und in **12**, unter dem Satz über den Abbruch.

> ⭐ **Vollzogen, siehe 44.1 (44-1; TB-111 `6c98c38`, TB-113, 26.09.2026):**
> `Abbruch` endet mit 2; zwölf Stellen, Meldung byte-gleich. `auswertung.py`
> `83c6bc3c…` ⇒ `a864b216…`. „Nicht vollzogen“ oben beschreibt den Stand auf
> `main` vor dem Zusammenführen und bleibt zeichengleich.

**43-2 — Tatsachennotiz zu Sperrlistenpunkt 4: die Interpolation unterhalb der
ersten Stützstelle** · Art: Tatsachennotiz (zu Punkt 4; ⛔ **nicht** in
Abschnitt 10) · Quelle: 25d Abschnitt 1, 3 (a)

*Fables Tatsachennotiz, zeichengleich:*
„Die Interpolationsregel läuft unterhalb der ersten Stützstelle linear gegen (0, 0); `nachschlagen(t, 0) = 0` ist ihr Grenzwert, gemessen TB-106."

*Seine Begründung, zeichengleich:* „Kein neuer Registertext — die Regel ist über den Code registriert (Punkt 4 nennt ihn) —, aber ein Leser soll nicht raten müssen."

**Stand, gemessen:** `research/vorregistrierung/benchmark.py` `aeeec9b8…`
(letzter Commit `a08c13a`, TB-106), `nachschlagen()` unverändert. Die Messung
steht in `docs/ERGEBNIS_TB-106_ersatzwerte_eingefroren_und_herkunft.md` (A5)
und 42.4, G4. **Verweis:** Sperrlistenpunkt 4 (Abschnitt 10); dort keine Marke.

**43-3 — Die Kopie in `faltenplan_neun.py`: Abbruch gleich, zweiter Ort,
Auflösung nach TB-100; `f5fdb53` steht** · Art: Tatsachennotiz (Entscheidung
über einen gebauten Commit) · Quelle: 25d 2 (1), 3 (b); 25e Kopf

> **(1) Die Kopie in `faltenplan_neun.py` — mit TB-107, `f5fdb53` steht.** Eure Neigung ist richtig, aus eurem Grund: Das Modul liegt im Laufbereich, der Laufbereich wird am Tag über alle Lauf-Typen gemessen, und eine Kopie derselben Regel mit dem alten Ersatzwert ist ein zweiter Ort (24b B4). Der Abbruch ist der Mindestschritt. **Die Kopie selbst bleibt als Befund benannt:** Sobald `fn.json` als Vergleichsgrösse nicht mehr gebraucht wird (nach TB-100, wenn das Faltenplan-Abbild die Vergleichsgrösse ist), ruft `faltenplan_neun.py` die Regel aus `faltenplan.py` statt sie zu tragen. Bis dahin Tatsachennotiz „zweiter Ort, Abbruch gleich, Auflösung nach TB-100". Kein `revert`.

*25e, Kopf, zeichengleich:* „Block C (die Kopie in `faltenplan_neun.py`) ist in 25d (1) bestätigt — kein `revert`."

**Stand, gemessen:** `f5fdb53` liegt auf `main`, kein `revert` im Log;
`research/faltenplan_neun/faltenplan_neun.py` `251029be…`, letzter Commit
`f5fdb53`. **Kette:** schliesst die Zeile „⚠️ `f5fdb53` … ist vor Fables
Antwort auf 25d gebaut" in **42.4** (zeichengleich stehen gelassen). Offen: die
Auflösung der Kopie nach TB-100 (43.5).

**43-4 — `herkunft.py`: Prüfansicht und `TB30A_BASE_DIR` unter dem Modus, in
einer Öffnung** · Art: Registertext (Plan) · **noch nicht vollzogen** · Quelle:
25d 2 (2), (3), 3 (c)

> **(2) Die Prüfansicht unter dem Modus — die eine Zeile, nicht rc 2.** Eure Neigung ist richtig: `--pruefen` liest das Protokoll als registrierte Eingabe (25c 4 (4)(b)); eine Prüfung, die unter dem Modus nicht laufen kann, prüft nicht, wo sie gebraucht wird — am Tag. Ein 2 an dieser Stelle wäre ehrlich, aber es macht die Wache stumm, wo sie wachen soll.

> **(3) `TB30A_BASE_DIR` in `herkunft.py` unter dem Modus — ja, rc 2 vor dem Lesen (24d Abschnitt 3), und (2) und (3) in einer Öffnung.** *Wann:* Die Regel aus 37.3 (Handwerk: Abbilder nach Bündeln, nicht nach jeder Änderung) gilt für Öffnungen genauso. **Mit dem Erzeuger**, wenn der Erzeuger `herkunft.py` ohnehin öffnet; sonst als eigener kleiner Auftrag **vor** dem Erzeuger — denn der Erzeuger ruft `register()` und `commit()`, und ein `commit()`, das unter einer Ersatzwurzel `"unbekannt"` liefert und trotzdem einen Hash schreibt, ist genau die Klasse, die 24b A2 verbietet: ein Wert, der so tut, als wäre er gemessen. Welches von beiden, entscheidet ihr am Erzeuger-Auftrag.

**Stand, gemessen:** `research/vorregistrierung/herkunft.py` `351f24c2…`
(letzter Commit `5791b4c`, TB-106), **seit der ersten planmässigen Öffnung
unverändert**; `TB30A_BASE_DIR` wird in Z. 51 gelesen (42.4, G6). Die Öffnung
ist als Auftrag TB-111 formuliert und läuft in einem eigenen Arbeitsbaum
(Zweig `tb-111`); **auf `main` ist nichts davon vollzogen.** **Kette:** zweite
planmässige Öffnung nach **42.3, F2** (erste: TB-106); die Entscheidung in
**37.4** („Nicht öffnen") und ihre Berichtigung durch 42.3 F2 bleiben
zeichengleich. **Marke am alten Ort:** in **37.4**, unter der Berichtigung
durch 42.3 F2.

> ⭐ **Vollzogen, siehe 44.1 (44-2; TB-111 `6cacfa4`, TB-113, 26.09.2026):**
> Prüfansicht mit `paths.DATA_DIR`, `TB30A_BASE_DIR` unter dem Modus 2 vor
> dem Lesen, in einer Öffnung. `herkunft.py` `351f24c2…` ⇒ `5bbfc9e0…`.
> „noch nicht vollzogen“ oben beschreibt den Stand vor dem Zusammenführen und
> bleibt zeichengleich.

**43-5 — Tatsachennotizen TB-106** · Art: Tatsachennotiz · Quelle: 25d 3 (e);
Kenntnisnahme 25d Abschnitt 1

*Fables Kenntnisnahme, zeichengleich (Anfang):* „TB-106: sieben Ersatzwerte ⇒ 2, unabhängig vom Modus; unbekannter Bedingungstext ⇒ 2, an einer Stelle gedeutet; tote Felder und Zeile weg"

**Stand:** die Werte aus 25d 3 (e) sind die aus TB-106 und stehen gemessen in
**42.4, G4** und **42.5**. Seit TB-106 geändert hat sich davon nur
`herkunft.register()`: `0ece95e2…` ⇒ `c85dd6c3…` durch den Eintrag von 41/42
(TB-108) — `register()` hasht dieses Register mit (42.5). Abbild `40ffe18d…`
und `herkunft.py` `351f24c2…` unverändert (TB-110, `0_stand.txt`).

**43-6 — `registerbericht.py --pruefen` rot bis 40.8 (h)** · Art:
Tatsachennotiz · Quelle: 25d Abschnitt 1

> **Zur roten `registerbericht.py --pruefen`:** bekannt (39.1, dritte Zeile: der ERZEUGT-Block ist nicht neu erzeugt). TB-106 ändert am Block eine Zeile; die Neuerzeugung kommt mit dem Raster-Nachzug (40.8 (h)), nicht vorher — sonst wird der Block zweimal neu.

**Stand, gemessen:** `registerbericht.py --pruefen` rc **1** (TB-110,
`0_stand.txt`; wie TB-108 D6 und vor TB-106, 42.4 G7). **Kette:** 39.1 (dritte
Zeile), 40.8 (h); die Neuerzeugung kommt mit dem Raster-Nachzug (43.5).

### 43.2 Aus Fable 25e (`FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md`)

Fables Liste für das Register, 25e Abschnitt 3, zeichengleich:

> | | Eintrag |
> |---|---|
> | a | Tatsachennotizen TB-107: `_min_history` genau ein Treffer; Kopie mit Abbruch; `getattr` weg; `tb40_lauf_*` nach (iv) erfüllt; Laufbereich 81 Module am Stand `f61bd97`; Gegenprobe aus der Messdatei |
> | b | Klasse (iv): das Aufräumen erscheint im Audit als (iv), nicht als (i) ausserhalb (Handwerk am Audit) |
> | c | Ergänzung „null Trades ist ein Wert" (2); die zehn Stellen wie die vierzehn; Gegenprobe erweitert |
> | d | `pfadvergleich.py`: Stummel, benannt (3) |

**43-7 — Ergänzung zu 24b A2 / 36.5 — null Trades** · Art: Registertext
(Ergänzung) · Quelle: 25e 2 (2), 3 (c)

> **Ergänzung zu 24b A2 / 36.5 — null Trades:** Ein Lauf des Laufbereichs, der keine Trades findet oder ausführt, schreibt dieses Ergebnis (leere Liste, Sharpe 0 nach 1c) und endet mit 0; er endet nie ohne Ausgabe. Unter dem Modus endet ein `exit()` ohne geschriebenes Ergebnis mit 2, gleich was ihm vorausgeht.

*Seine Quelle des Grundes und die Umsetzung, zeichengleich:*

> *Quelle des Grundes:* 5.1 Nr. 8, 1c, 36.5. Kein Ergebnis. Umsetzung: die Gegenprobe (`test_main_gegenprobe.py`) zählt künftig jedes `exit()` ohne vorherige Ausgabe, nicht nur die nach fehlender Eingabe; die zehn Stellen bekommen die Modus-Abfrage wie die vierzehn. Dass `__main__` heute von keinem Lauf-Typ erreicht wird, ändert daran nichts — dieselbe Lage wie bei (c). Für den Laufcode (TB-30b) heisst es: Der Erzeuger schreibt für eine Zelle ohne Trades die Nullzeile, nie nichts.

*Und der Befund, den er daraus macht, zeichengleich:* „Ein Skript, das bei null Trades ohne Ausgabe mit 0 endet, ist für den Aufrufer von „gerechnet und geschrieben" nicht unterscheidbar; das ist die TB-45-Klasse, gleich ob die Leere aus fehlender Eingabe oder aus einer Rechnung stammt."

**Stand, gemessen — vollzogen in TB-109** (`docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md`):
die zehn Stellen `if trades.empty: … exit()` in den neun
`strategies/*/equity_simulation.py` enden unter dem Modus mit 2 (Meldung auf
stderr), ohne Modus zeichengleich (`53896e4`); die Gegenprobe
`shared/test_main_gegenprobe.py` zählt jedes vorzeitige `exit()` im `__main__`
ohne geschriebenes Ergebnis (`a02f035`) — Einzelheiten 43.4 (TB-109). Der Satz
für den Laufcode (Nullzeile im Erzeuger) ist **nicht** vollzogen; er gehört zu
TB-30b (43.5). **Kette:** ergänzt **36.5** und **41.1** (24b A2); stützt sich
auf **5.1 Nr. 8** und **15.3 (Registertext 1c)**, beide zeichengleich. **Marken
am alten Ort:** unter **5.1 Nr. 8** und unter der Tatsachennotiz zu **1c** in
15.3.

> ⭐ **43-7 PRÄZISIERT durch R33 (48.1)** (Fable 29b R33, nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**43-8 — Die zwei weiteren Ablagen wie `tb40_lauf_*`** · Art: Registertext
(Anwendung von Klasse (iv), 42.2) · Quelle: 25e 2 (1)

> **(1) `tb40_faltenplan_*` und `tb40_proben_*` — wie `tb40_lauf_*`.** Eure Neigung ist richtig: Klasse (iv) fragt nicht, welcher Lauf den Ordner anlegt, sondern ob ein Modul des Laufbereichs Ablagen hinterlässt. Dass `hole_faltenplan()` ohne JSON von keinem gemessenen Lauf-Typ gerufen wird, ist eine Tatsache über heute; der Laufbereich wird am Tag gemessen. Kleiner Auftrag, dieselbe Bauart (`finally`, Pfad in der Meldung, wenn kein Ergebnis).

**Stand, gemessen — vollzogen in TB-109** (`29640ca`): `hole_faltenplan()`
entfernt `tb40_faltenplan_*`, `stille_filter()` entfernt `tb40_proben_*`, je im
`finally` nach dem Lesen des Ergebnisses; ohne Ergebnis bleibt der Ordner, sein
Pfad steht in der Meldung. **Kette:** Klasse (iv) in **42.2**; `tb40_lauf_*`
TB-107 (42.4, G8 ff.).

**43-9 — Klasse (iv) im Audit** · Art: Registertext (Handwerk am Audit) ·
Quelle: 25e Abschnitt 1, 3 (b)

*Fable, 25e Abschnitt 1, zeichengleich:* „dass das Aufräumen im Lese-Audit als zehn Verzeichnis-Öffnungen in (i) erscheint, ist genau der Grund, warum Klasse (iv) eine Klasse ist und keine Erlaubnis — der Audit soll diese Zugriffe als (iv) führen, nicht als (i) ausserhalb; Handwerk am Audit, klein."

**Stand, gemessen — gebaut in TB-109** (`a02f035`,
`docs/belege/TB-109/d_auswerten.py`; die Fassung TB-104 bleibt): Ein
Verzeichnis im Temp-Verzeichnis, das ein Prozess des Laufs selbst anlegt, ist
eine eigene Ablage; **jeder** lesende Zugriff darauf oder darin steht unter
(iv). ⚠️ **Tatsachennotiz zur Reichweite:** Fables Satz nennt das Aufräumen
(die zehn Verzeichnis-Öffnungen). Gebaut ist mehr: Auch das Lesen des
Ergebnisses in der eigenen Ablage steht unter (iv). Im Benchmark-Lauf fällt
Klasse (i) ausserhalb damit von 31 auf **11**, nicht auf die 21 aus TB-106.
Welche Reichweite gilt, ist bei Fable gefragt (Ergebnis TB-109, Frage 2) —
**offen**, 43.5. Schreibzugriffe bleiben unter (iii).

**43-10 — `pfadvergleich.py`: der benannte Stummel** · Art: Tatsachennotiz ·
Quelle: 25e 2 (3), 3 (d)

> **(3) `pfadvergleich.py` — der Stummel, wie bei Probe A.** Eure Neigung trifft, mit dem Grund, den ihr nennt (ein Werkzeug, das dauerhaft 1 meldet, verwässert 1), und mit einer Bedingung: Der Stummel wird als solcher benannt (*„Fassung TB-52 plus `selektionsmodus = lambda: False`, weil der heutige Nachbar die Funktion verlangt"*) — das Werkzeug vergleicht dann weiter, was es vergleichen soll (Pfadauflösung), und behauptet nicht, TB-52 habe die Funktion gehabt. Dass `test_paths` Probe A genau das schon tut, ist der Konsistenzgrund. Das Werkzeug liegt ausserhalb des Laufbereichs; Live-Freigabe wie gehabt.

**Stand, gemessen — vollzogen in TB-109** (`8570ce8`):
`research/resolver_selektion/pfadvergleich.py` hängt an die Fassung aus TB-52
den Stummel `def selektionsmodus(): return None` an, benannt im Kommentar;
eigenständig rc **0** („GRUEN"). ⚠️ **Mit `None`, nicht mit Fables `False`** —
43.3.

### 43.3 ⚠️ Berichtigung des steuernden Chats an 25e (3) — vorläufig, von Fable nicht bestätigt

**43-11** · Art: Berichtigung (vorläufig) · Quelle: Ergebnis TB-109, Block D

Fables Wortlaut für den Stummel, zeichengleich: „Fassung TB-52 plus `selektionsmodus = lambda: False`, weil der heutige Nachbar die Funktion verlangt"

**Die Berichtigung:** „`selektionsmodus = lambda: False`" lies
„`selektionsmodus()` → `None`". **Grund:** `shared/strategy_paths.py` fragt seit
TB-107 `paths.selektionsmodus() is not None`; `False is not None` ist wahr. Mit
`False` hält `strategy_paths` den Modus für aktiv. `shared/test_paths.py` Probe
A benutzt aus demselben Grund `return None`.

**Verhaltensbeleg (TB-109, `docs/belege/TB-109/d_stummel_probe.txt`):** Mit
`None` legt `strategy_paths` im Wegwerfbaum des Werkzeugs in **9 von 9** Bots
`results/` und `logs/` an, wie jeder Aufruf ohne Modus; mit `False` in **0 von
9**. ⚠️ **Das Werkzeug selbst meldet in beiden Fällen 0 Unterschiede** — es
vergleicht Zeichenketten, und die sind in beiden Zweigen gleich. Der
Widerspruch zeigt sich also am durchlaufenen Zweig, nicht an der Ausgabe des
Werkzeugs.

⚠️ **Diese Berichtigung ist vorläufig:** Sie stammt vom steuernden Chat
(`docs/auftraege/MAC_TB-109_nulltrades_ablagen_stummel.md`, Abschnitt
„Ein Widerspruch in Fable 25e (3)"), nicht von Fable. Fable ist sie mit dem
Ergebnis TB-109 vorgelegt; **bis er sie bestätigt, steht sie hier als
Vorschlag.** Fables Satz in 43-10 bleibt zeichengleich stehen. Bestätigt er
sie, kommt ein Eintrag „berichtigt durch …" dazu; widerspricht er, wird der
Stummel zurückgebaut, mit Grund.

> ⭐ **Von Fable bestätigt (26a 3 (1)), siehe 45.1** (TB-114, 26.09.2026).
> Überschrift und Text oben bleiben zeichengleich.

### 43.4 Tatsachennotizen aus TB-107, TB-108 und TB-109

**43-12 — Tatsachennotizen TB-107:** *Fables Liste, 25e 3 (a) — zeichengleich oben in 43.2. Gemessen steht
TB-107 in **42.4** (G8–G10 und die Zeile zu `f5fdb53`); hier nichts doppelt.*

*TB-108 und TB-109: eigene Fassung der Sitzungen, gemessen; kein
Fable-Wortlaut.*

| | Tatsache | Ergebnisdokument, Commit |
|---|---|---|
| 43-13 | **TB-108:** Abschnitte **41** und **42** eingetragen, in einem Commit mit allen Marken; **67** Einträge (41: A1–A12, B1–B8, C1–C9; 42: D1–D12, E1–E8, F1–F8, G1–G10); **108** Zitate eingesetzt, `diff` 108/108 rc 0; **20** Marken an 19 Stellen; `numstat` 1134/0; `herkunft.register()` `0ece95e2…` ⇒ `c85dd6c3…`. **Nicht gesetzte Marken:** keine in Abschnitt 10 (F3 und F8 stehen deshalb in 42.3); keine in 38.x (der Modus-Nachweis steht in 39.6). Befunde: H6 bis heute nicht eigenständig (41.1, A4); ein dritter Hash-Übergang an einem gesperrten Pfad (`messgroessen.py`, TB-103, 42.5) | `ERGEBNIS_TB-108_register_41_42`; `f4d3e2a`, `486032d` |
| 43-14a | **TB-109, die zehn Stellen:** unter dem Modus Meldung auf stderr und Rückgabewert 2, Abfrage an der Stelle über `paths` (Bauart der vierzehn, 42.4 G2); **ohne Modus**: Trade-Listen der neun Bots vorher = nachher (Hash), `research/tb27_kapitalsimulation/vergleich.py --pruefen` rc 0, `test_ergebniskurven` 44/44; neue Proben `shared/test_nulltrades_modus.py` 34/34 | `ERGEBNIS_TB-109` B; `53896e4` |
| 43-14b | **TB-109, A3 — erreicht ein Cron-Lauf heute eine der zehn Stellen? Nein.** Die `__main__`-Blöcke wie von `shared/kurven_lauf.py` gestartet (Stubs, `data/`, ohne Modus), anweisungsweise bis vor `simulate_portfolio`: an allen zehn Stellen Trade-Liste **nicht leer**, neun von neun Läufen erreichen `simulate_portfolio`. Tatsache über den Datenstand `d9449faf…` | `ERGEBNIS_TB-109` A3 |
| 43-14c | **TB-109, Gegenprobe:** gezählt wird jedes vorzeitige `exit()`/`sys.exit()`/`quit()` im `__main__` ohne vorher geschriebenes Ergebnis — **24** Stellen im Laufbereich (14 + 10), **alle** mit Abfrage, keine weitere gefunden; 16 reguläre Blockenden (`sys.exit(main())` u. ä.) ausgewiesen, nicht gezählt. Grenze: `main()`-Funktionen prüft sie nicht | `ERGEBNIS_TB-109` E1; `a02f035` |
| 43-14d | **TB-109, Ablagen:** `tb40_faltenplan_*` und `tb40_proben_*` entfernt (43-8); ein Lauf der alten Fassung hinterliess 1 + 9 Ordner, seit C 0; `ut.json`, `sf.json` bytegleich | `ERGEBNIS_TB-109` C; `29640ca` |
| 43-14e | **TB-109, Audit (iv):** wie 43-9; im Benchmark-Lauf (Repo und Klon) 10 eigene Ablagen, 20 lesende Zugriffe (10 Verzeichnis-Öffnungen, 10 Ergebnis-JSON), alle entfernt | `ERGEBNIS_TB-109` E2 |
| 43-14f | **TB-109, Abnahme:** Benchmark-Tabelle `64fb2912…` im Modus (Repo und frischer Klon) und ohne Modus bytegleich — als Nachweis nach 41.2 (B4) weiter **2**; acht Werkzeugausgaben ohne Modus bytegleich; Trockenlauf 9 × rc 0; Sonde gegen `40ffe18d…` vorher = nachher; `register()` `c85dd6c3…` unverändert; `test_vorregistrierung` 196/196 | `ERGEBNIS_TB-109` F; `723281f` |

### 43.5 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **`auswertung.Abbruch` ⇒ 2** (43-1) — eine Zeile an der Klasse | nächste planmässige Öffnung von `auswertung.py` (Punkte 3/5/14, neues Abbild) |
| (2) | **Die zweite Öffnung von `herkunft.py`** (43-4): Prüfansicht mit `paths.DATA_DIR`, `TB30A_BASE_DIR` unter dem Modus 2 | mit dem Erzeuger oder vor ihm (Auftrag TB-111, Zweig `tb-111`, nicht auf `main`) |
| (3) | **Die Auflösung der Kopie in `faltenplan_neun.py`** (43-3) | nach TB-100 (Faltenplan-Abbild als Vergleichsgrösse) |
| (4) | **Die Neuerzeugung des ERZEUGT-Blocks** (43-6) | mit dem Raster-Nachzug, 40.8 (h) |
| (5) | **Die Nullzeile im Erzeuger** für eine Zelle ohne Trades (43-7, Satz für den Laufcode) | TB-30b |
| (6) | **Die Reichweite von (iv) im Audit** (43-9) und die **Bestätigung der Berichtigung 43-11** | Fable (Ergebnis TB-109, Fragen 1 und 2) |
| (7) | **Die Erweiterung von 19 auf den Laufbereich** (42.6 (4)) | eigener Auftrag |
| (8) | **Der Erzeuger auf dem Signalpfad**; **das Faltenplan-Abbild** (42.6 (5), (6)) | Plan-Punkte 3, 5 und 7 (TB-101) |
| (9) | **Fable 25f** (Gesamtanalyse; 42.6 (3)) | eigener Eintrag, nach Fables Antwort |

### 43.6 Was hier ausdrücklich NICHT getan wurde

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert, nichts gerechnet** — auch wo ein Eintrag eine Codeänderung verlangt (43-1, 43-4) | 43.5 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`), Sonde vorher und nachher gleich (`docs/belege/TB-110/0_sonde_vorher.txt`, `c_sonde_nachher.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — Marken sind neue Zeilen, nichts entfernt | — |
| ⛔ | **Keine Marke in Abschnitt 10**; die Tatsachennotiz zu Punkt 4 (43-2) steht in 43.1 | — |
| ⛔ | **Nichts aus 25f** | 43.5 (9) |
| ⭐ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums; „Trade-Liste leer ja/nein" je Bot ohne Zahl | — |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich): 5.1
Nr. 8 · 12 · 15.3 (unter der Tatsachennotiz zu 1c) · 36.5 · 37.4 · 42.6.

*Dieser Abschnitt ist rein additiv: Er trägt die Einträge des Verfahrensprüfers
aus zwei Antworten zeichengleich ein, dazu eine vorläufige Berichtigung des
steuernden Chats mit Verhaltensbeleg und die Tatsachen aus drei Aufträgen — und
entfernt nichts. Gebaut und gerechnet wird nichts.*

## 44. Vollzug: `herkunft.py` im Modus, `auswertung.py` endet mit 2, 19 über den Laufbereich — Tatsachennotizen TB-111 und TB-112 (TB-113, 26.09.2026)

### 44.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Tatsachen**, Bauart wie **43** (TB-110). Kein
Fable-Wortlaut ist neu hinzugekommen; eingetragen wird, **was zwei Aufträge
vollzogen haben**, deren Plan schon im Register steht:

- **TB-111** (Fable 25d (2)–(4), Register **43-1** und **43-4**): die zweite
  planmässige Öffnung von `herkunft.py` und die Umstellung von
  `auswertung.Abbruch` auf 2. TB-111 lief **auf einem eigenen Zweig**
  (`tb-111`, Worktree `~/trading-bot-tb111`, Eingang `f4d6d6d`, Commits
  `6cacfa4`, `6c98c38`, `1dcf273`, `49f0868`) und ist mit dem Auftrag dieses
  Abschnitts nach `main` zusammengeführt (`257e7db`, `git merge --no-ff`,
  `merge-tree` vorher rc 0, Schnittmenge der geänderten Dateien leer,
  `docs/belege/TB-113/0c_vorbedingungen.txt`).
- **TB-112** (Register **19**, **42.2 E2**, **42.3 F8**; Fable 25f O6): die
  Sauberkeitsprüfung der Startprüfung über den Laufbereich, nur unter dem
  Modus, mit der namentlichen Ausnahme des registrierten Protokolls
  (`e731207`, `9d711dc`, `e65e57c`, `21f4cac`, `af6042f`, direkt auf `main`).

Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-113_zusammenfuehrung_tb111_register_44.md`, Freigabe
des Betreibers 26.09.2026, 14:28). **Die Kette zu 43:** 43.5 führt (1)
`auswertung.Abbruch` ⇒ 2, (2) die zweite Öffnung von `herkunft.py` und (7) die
Erweiterung von 19 als offen. **Alle drei sind hier als vollzogen eingetragen**
(44.1, 44.2). Die Zeilen in 43 bleiben zeichengleich; Marken darunter verweisen
hierher.

**Bauart je Eintrag:** Kennung (44-1 bis 44-12) · Art · Stand, gemessen im
genannten Ergebnisdokument und nach dem Zusammenführen in TB-113
(`docs/belege/TB-113/`), ohne Ergebnisgrössen (27.1) · Kette. Wo ein Wortlaut
aus einem Ergebnisdokument, dem Code oder einem früheren Registerstand
übernommen ist, ist er **eingesetzt, nicht abgetippt**; je Zitat ein `diff`
gegen die Quelle mit rc 0 (`docs/belege/TB-113/c2_zitate.txt`).

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)).

### 44.1 TB-111 — `herkunft.py` im Modus und `auswertung.py` endet mit 2

*Eigene Fassung der Sitzung TB-111, gemessen
(`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`, Belege
`docs/belege/TB-111/`); nach dem Zusammenführen nachgemessen in TB-113.*

**44-1 — 43-1 vollzogen: `auswertung.Abbruch` endet mit 2** · Art:
Tatsachennotiz (Vollzug) · Commit `6c98c38`

`class Abbruch(SystemExit)` setzt im eigenen `__init__` den Rückgabewert aus
`paths.RUECKGABEWERT_STARTPRUEFUNG`; die Zeile im Code, zeichengleich:
„super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)". Der
Kommentar an der Klasse nennt die Regel aus 43-1, zeichengleich: „Ausgaenge von `auswertung.py`: 0 oder 2, kein 1".

- **12 Stellen** `raise Abbruch(`, zeichengleich wie vorher (TB-111 A3;
  nachgezählt in TB-113: 12).
- **Meldung byte-gleich:** An vier Brüchen (leere Rohergebnisse, fehlende
  Spalte, Zelle ausserhalb des Rasters, weniger als drei gemeinsame Tage) geht
  der Rückgabewert von 1 auf **2**; stderr und stdout sind vorher und nachher
  auf **denselben Eingaben** per `cmp` gleich (TB-111 C1,
  `c_proben_vorher.txt`/`c_proben_nachher.txt`). Der Fall ohne Bruch bleibt rc 0.
- Kein Test erwartete rc 1 von `auswertung.py`; kein Test wurde umgestellt.
  Neue Proben: `test_ersatzwerte.py` Teil G (6, mit Mutation und Gegenprobe).
- **Sichtbar geändert:** Die Meldung wird beim **Erzeugen** von `Abbruch`
  ausgegeben, nicht erst beim Prozessende; `str(e)` eines gefangenen `Abbruch`
  ist `"2"`, die Meldung steht in `e.meldung` (Frage an Fable, 44.3).

**Kette:** vollzieht **43-1** (Ergänzung zu 36.5); beantwortet damit die offene
Zeile der Marke unter **36.5** (TB-108) auch im Code. **Marken am alten Ort:**
unter **43-1** und unter der TB-110-Marke in **36.5**.

**44-2 — 43-4 vollzogen: die zweite planmässige Öffnung von `herkunft.py`** ·
Art: Tatsachennotiz (Vollzug) · Commit `6cacfa4`

- **Prüfansicht:** `main()` übergibt unter dem Modus `paths.DATA_DIR` an
  `block("pruefung", …)`, dieselbe Form wie `--anhaengen` seit TB-106; ohne
  Modus `None` wie vorher. Gemessen: im Modus rc 0, Datenstand `d9449faf…`/223.
- **`TB30A_BASE_DIR` unter dem Modus rc 2 vor dem Lesen:** eine neue Funktion
  `_ersatzwurzel_pruefen()` ist die **erste Zeile** von `commit()`,
  `register()` und `block()`; sie bricht unter dem Modus mit 2 ab, wenn die
  Variable gesetzt ist oder `BASE_DIR` von der eigenen Wurzel abweicht. Die
  Meldung beginnt, zeichengleich: „TB30A_BASE_DIR ist unter dem Selektionsmodus gesetzt".
  Ein Lesehaken sieht dabei **0 Zugriffe** unter der Ersatzwurzel (Proben
  F-b bis F-b4 in `test_ersatzwerte.py`).
- **`_paths()` aus der eigenen Wurzel:** `paths.py` wird aus `_WURZEL` (dem
  Baum, in dem `herkunft.py` liegt) geladen, nicht mehr aus `BASE_DIR`.
- `EINGEFROREN`, `datenstand()`, `kette_pruefen()`, `anhaengen()` und
  `verankerung()` zeichengleich; der Import bleibt unter dem Modus unverändert
  (kein `paths` geladen). Neue Proben: Teil F (15, drei Mutationen je mit
  Gegenprobe).

**Kette:** vollzieht **43-4** (Fable 25d (2), (3)) — die zweite planmässige
Öffnung nach **42.3 F2** (erste: TB-106). Die Entscheidung in **37.4** („Nicht
öffnen"), ihre Berichtigung durch 42.3 F2 und die TB-110-Marke dort bleiben
zeichengleich. **Marken am alten Ort:** unter **43-4** und unter der
TB-110-Marke in **37.4**.

**44-3 — Befund A2b: die Modus-Abfrage las unter der Ersatzwurzel** · Art:
Tatsachennotiz (Befund, vor dem Vollzug gemessen)

Vor TB-111 lud `_paths()` die Datei `paths.py` aus `BASE_DIR/shared`, also
**unter** `TB30A_BASE_DIR`. Unter dem Modus mit einer nicht existierenden
Ersatzwurzel endete die Prüfansicht deshalb mit **rc 1**
(`ModuleNotFoundError`), **nicht mit 2**; schon die Frage „Modus?“ las unter
der Ersatzwurzel (TB-111 A2b, `docs/belege/TB-111/a_vormessung.txt`). Mit der
echten Wurzel als Ersatz fiel das nicht auf. Die Umstellung von `_paths()` in
44-2 ist die Folge; ohne sie wäre „erst 2, dann lesen“ (24d Abschnitt 3) nicht
erfüllbar gewesen. Kein Test setzte `TB30A_BASE_DIR` zusammen mit dem Modus.

**44-4 — Hash-Übergänge** · Art: Tatsachennotiz

| Datei bzw. Wert | vorher | nachher | durch |
|---|---|---|---|
| `research/vorregistrierung/herkunft.py` | `351f24c2d6a3a512dc1eb1a80b536b99d47c266db38f7dd93b9d1c0199397eef` | `5bbfc9e085d7ec70f43eb8aaaf63b957de27e3647023e143d17e9dd8c60448fa` | TB-111 `6cacfa4` |
| `research/vorregistrierung/auswertung.py` | `83c6bc3c9b683d0bfd9d8c445492060f93759a551d0dcf329b2bd21b0f1cc5a1` | `a864b2168a19405d5f1516a17146f78ef44bbca6f4f8d242c9ccb25f937467f3` | TB-111 `6c98c38` |
| `herkunft.register()` auf `tb-111` | `c85dd6c3…` | `e7d82547…` | TB-111 (nur `auswertung.py` hat sich von den elf Teilen geändert; `herkunft.py` steht nicht in `EINGEFROREN`) |
| `herkunft.register()` auf `main` | `c92900a8…` (nach Register 43) | **`469272dfbedf06492f1094bdb636295daeb76a9a7d4cc3fd98e89bcb400c0535`** | Zusammenführen `257e7db` (Register mit 43 **und** `auswertung.py` `a864b216…`; weder `e7d82547…` noch `c92900a8…`) |

⚠️ **Selbstbezug:** `register()` hasht dieses Register mit (42.5). Der Wert
**nach** dem Eintrag dieses Abschnitts kann hier nicht stehen; er steht im
Ergebnisdokument von TB-113.

**44-5 — Das gültige Abbild der Sperrliste: `e655c1c8…`** · Art:
Tatsachennotiz (36.6: „Das aktuelle Abbild steht selbst mit Hash im Register")

`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26.json`,
**9192 B, `e655c1c8c8e576faa1de8021357354b1d9f0b44e9adae3a176c944087b3aacd9`**,
gezogen von TB-111 auf `6c98c38` (Commit `1dcf273`); 14 Punkte, 15
Pfadnennungen, Gruppen `bestimmt` 0, `eingefroren` 10. Es löst
`sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`, 43.6) ab; das alte bleibt
(36.6).

- **Sonde gegen das alte `40ffe18d…`** auf dem Code-Stand von TB-111:
  Befund **genau** an Punkt **3, 5, 11, 12, 14** und in der Gruppe
  **`eingefroren`** — die Punkte, die `auswertung.py` oder `herkunft.py`
  nennen; kein anderer (`docs/belege/TB-111/d2_sonde_alt.txt`). Das ist der
  Befund `1` vor dem Tag nach **37.3**: beauftragt (Freigabe 25.09.2026,
  23:14), geschlossen durch ein **neues** Abbild.
- **Sonde gegen das neue, nach dem Zusammenführen auf `main`** (TB-113,
  `a_messung.txt`, `a_sonde_nach_merge.txt`): Pfad-Bestandteile **25/0/0**,
  (ii) **0**, Listentext wie bei Erzeugung. Das Abbild nennt Register-Z.
  894–1007; auf `main` steht der Listentext seit TB-110 in Z. 901–1014 —
  (ii) vergleicht den Listentext, nicht die Zeilen. rc 2 nur wegen der Punkte,
  die die Sonde nicht prüfen kann, wie in TB-110, TB-111 und TB-112.

**44-6 — Nach dem Zusammenführen gemessen (TB-113)** · Art: Tatsachennotiz

Am Merge-Commit `257e7db` (Baum `e44e1abf…` = Vorhersage von `merge-tree`):
Hashes `herkunft.py`/`auswertung.py` wie in 44-4; Benchmark-Tabelle im Modus im
Repo **und** in einem frischen Klon bytegleich **`64fb2912…`**; ohne Modus
acht Werkzeugausgaben bytegleich; Trockenlauf aller neun Bots im Modus 9 × rc
0; `herkunft_protokoll.jsonl` existiert nicht. Tests und Einzelheiten:
`docs/ERGEBNIS_TB-113_zusammenfuehrung_tb111_register_44.md`.

**Wechselwirkung TB-111 × TB-112, festgehalten:** Die in TB-112 erweiterte
Sauberkeitsprüfung (44.2) **bindet `research/vorregistrierung/auswertung.py`**
— die Datei liegt im Laufbereich und steht als Einzeldatei in
`ARBEITSBAUM_PFADE`. **`herkunft.py` bindet sie nicht:** Kein Lauf-Typ des
Laufbereichs lädt das Modul (Laufbereich 81 Module, TB-107 F1 = TB-112 A2; dort
0 Zeilen `herkunft.py`). Eine uncommittete Änderung an `herkunft.py` hielte die
Startprüfung also heute nicht an. Kommt das Modul in den Laufbereich (mit dem
Erzeuger, der `register()` und `commit()` ruft, 43-4), zeigt es die nächste
Laufbereichsmessung, und die Liste wird mit ihr erneuert (44-8).

> ⭐ **44-6 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 44.2 TB-112 — Sauberkeit über den Laufbereich

*Eigene Fassung der Sitzung TB-112, gemessen
(`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md`, Belege
`docs/belege/TB-112/`).*

**44-7 — E2 und F8 vollzogen** · Art: Tatsachennotiz (Vollzug) · Commit
`9d711dc`

- **`shared/paths.py` `ARBEITSBAUM_PFADE`: 15 Einträge** — `shared`,
  `strategies`, `requirements.lock` wie bisher, dazu die **12 Module des
  Laufbereichs ausserhalb** dieser Ordner **als einzelne Dateien** (11 unter
  `research/`, 1 unter `notifications/`). Einzeldateien statt Ordner, weil
  `research/vorregistrierung/ergebnisse/` Laufausgaben aufnimmt; der Preis: ein
  **neues** Modul im Laufbereich ist ungeprüft, bis Liste und Messung
  nachgezogen sind.
- **`REGISTRIERTE_PROTOKOLLE`** = genau
  `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`, im
  `git status` als `:(exclude)`-Pfadangabe — **namentlich**, nicht zufällig
  (ohne die Ausnahme deckt heute kein geprüfter Pfad das Protokoll). `data/`
  bleibt ausgenommen wie in 19.
- **Nur unter dem Modus wirksam:** gelesen nur in `_pruefe_codeherkunft`, das
  nur im Modus-Zweig läuft; ohne Modus 0/0/0 `git`-, Paket- und
  `os.system`-Aufrufe, 144 Pfade zeichengleich, acht Werkzeugausgaben
  bytegleich.
- **Vorher/nachher:** Am Eingang lief der Import unter dem Modus mit einer
  uncommitteten Änderung in `benchmark.py`, `faltenplan_neun.py` oder
  `manual_close.py` durch (rc 0) — der Befund aus E2 beschrieb den Stand.
  Nachher: jede der 12 Dateien einzeln rc 2 mit Dateiname; Protokoll neu oder
  verändert rc 0; `data/` und eine Ausgabe unter `ergebnisse/` rc 0. Proben:
  `shared/test_arbeitsbaum_laufbereich.py` 26/26 (frischer Klon, Mutationen
  mit Gegenprobe).
- `shared/paths.py` `b8bb5cf97fdf2d5908cc7019cdd2a40c8d3085a509f86e335bf1adbf965961fd`
  ⇒ `1478d9a09895614e90246f781b3c4dc5979121318c7e9a79b3aded4a778dc404`.

**Kette:** vollzieht **42.2 E2** und **42.3 F8** und damit den Kasten
„Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen“ in **19**;
schliesst **43.5 (7)**. Die Reihenfolge, die F8 verlangt (die Ausnahme vor der
Erweiterung im Register), ist eingehalten. **Marken am alten Ort:** unter dem
Kasten in **19**, unter „Stand, gemessen“ in **42.2 E2** und in **42.3 F8**.

**44-8 — Die Tatsachennotiz neben der Laufbereichsmessung** · Art:
Tatsachennotiz

E2 verlangt, zeichengleich: „Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert."

**Das ist diese Datei:** `docs/belege/TB-112/arbeitsbaum_pfade.txt` (die 15
geprüften Einträge je mit Art, die eine Ausnahme, „nicht geprüft: `data/` und
alles übrige“), gelesen per Import ohne Modus am Stand `21f4cac`. Sie steht
neben `docs/belege/TB-112/a2_laufbereich.txt`, der Laufbereichsmessung, die
`shared/test_arbeitsbaum_laufbereich.py` als Gegenprobe liest. Am Tag-Commit
ersetzt die Tag-Messung beide.

**44-9 — Laufbereich 81 = TB-107** · Art: Tatsachennotiz

Laufbereich am Eingang von TB-112 (Werkzeug TB-104 D1, drei Lauf-Typen:
Trockenlauf aller neun, Benchmark im Modus, `auswertung.py`-Import): **81
Module, identisch mit TB-107 F1**, auch die Lauf-Typen je Modul; 12 davon
ausserhalb `shared/`/`strategies/`. Am Endstand von TB-112 erneut gleich.

**44-10 — Lese-Audit: 0 Code-Zugriffe ausserhalb der Liste; Randbefund 10
Eingaben** · Art: Tatsachennotiz (Befund offen bei Fable)

- In den Modus-Läufen (Repo und frischer Klon) liest **kein** Prozess eine
  `.py` unter der Codewurzel, die `ARBEITSBAUM_PFADE` nicht deckt (**0**).
- ⚠️ **Randbefund, nicht behoben:** Der Benchmark liest **10 versionierte
  Eingabedateien ausserhalb der Liste** — `research/vorregistrierung/ergebnisse/messgroessen.json`
  (durch die Sonde gedeckt, Gruppe `eingefroren`) und die neun
  `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (von nichts
  gedeckt; sie gehen über die Faltenlängen in den Plan ein, TB-95). E2 bindet
  Code, nicht Eingaben; eine uncommittete Änderung daran hielte die
  Startprüfung nicht an. **Offen bei Fable** (44.3).

**44-11 — Nebennotiz: db-Sicherung und `tb40_test_*`** · Art: Tatsachennotiz
(ausserhalb des Selektionsverfahrens)

Mit TB-112 kamen zwei Dinge, die das Verfahren nicht berühren und nur der
Vollständigkeit halber hier stehen: `docs/werkzeuge/db_sicherung/db_sicherung.sh`
sichert die Datenbanken der Bots lesend nach iCloud (Fable 25f O6; die
Cron-Zeile trägt der Betreiber ein), und
`research/universum_trockenlauf/test_universum_trockenlauf.py` räumt seine
Wegwerfordner selbst auf (vorher 18 je Lauf, nachher 0). Keine Datei des
Laufbereichs, der Sperrliste oder von `EINGEFROREN` ist dabei geändert.

### 44.3 Was offen bleibt

**44-12 — Fragen an Fable aus TB-109, TB-111 und TB-112, zeichengleich aus den
Ergebnisdokumenten:**

*TB-109* (`docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md`, Abschnitt 8):

> 1. **Stummel und Probe.** Bestätigst du die Berichtigung `None` statt `False`? Soll das Werkzeug zusätzlich prüfen, dass der Stummel den Nicht-Modus-Zweig nimmt (z. B. die angelegten Ordner im Wegwerfbaum zählen)? Heute würde ein falscher Stummel grün durchgehen.
> 2. **(iv) im Audit – welche Zugriffe?** Gebaut ist: **alle** lesenden Zugriffe auf die eigene Ablage, also die Verzeichnis-Öffnung beim Aufräumen **und** das Lesen des Ergebnisses darin. Damit ist (i) außerhalb 11. Der Auftrag erwartete 21, also nur die Verzeichnis-Öffnungen umgeordnet. Welche Lesart meint 25e 3 (b)? Und gehört die Tempfile-Probe von `mkdtemp` (von `tempfile` angelegt und sofort entfernt, ohne `mkdir`) ebenfalls zu (iv)?
> 3. **Grenze der Gegenprobe.** Sie prüft `__main__`-Blöcke, nicht `main()`-Funktionen, die mit `return 0` ohne Ausgabe enden könnten. Soll die Erweiterung auf `main()` für den Laufcode (TB-30b) kommen, oder reicht der Satz aus 25e, dass der Erzeuger für eine Zelle ohne Trades die Nullzeile schreibt?

*TB-111* (`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`, Abschnitt 6):

> 1. **`datenstand(None)` im Modus** liest weiter `BASE_DIR/data`, mit oder ohne TB30A. Ich habe das wegen B3 (zeichengleich) nicht geändert. Die Aufrufer im Betrieb übergeben einen Pfad, und `block()` verlangt ihn im Modus. Soll `datenstand()` bei der nächsten Öffnung im Modus ohne Pfad ebenfalls mit 2 enden?
> 2. **Veralteter Satz im Docstring von `auswertung._abbruch_2`:** „(`Abbruch` oben endet mit 1 und bleibt, wie er ist.)“ ist seit Block C falsch. Die Freigabe lautete „Sonst nichts“, deshalb habe ich ihn **nicht** geändert. Soll er mit der nächsten Öffnung von `auswertung.py` gestrichen werden, oder als Tatsachennotiz stehen bleiben?
> 3. **`str(e)` eines gefangenen `Abbruch`** ist jetzt `"2"`, die Meldung steht in `e.meldung`. Heute liest niemand `str(e)`. Reicht das als Tatsachennotiz?

*TB-112* (`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md`, Abschnitt 6):

> 1. **Eingaben außerhalb der Liste.** Das Audit findet 10 versionierte Dateien, die der Benchmark als **Daten** liest und die kein Pfad der Sauberkeitsprüfung deckt: `ergebnisse/messgroessen.json` (durch die Sonde gedeckt, Gruppe `eingefroren`) und die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (von nichts gedeckt; sie gehen über die Faltenlängen in den Plan ein, TB-95). Eine uncommittete Änderung daran hielte die Startprüfung nicht an. Sollen die neun Listen in `ARBEITSBAUM_PFADE` (dann heißt die Liste „Laufbereich und seine versionierten Eingaben“) oder in das Abbild der Sperrliste? Oder bindet E2 bewusst nur Code?
> 2. **Pflege der Liste.** Die Liste ist eine Tatsache vom 26.09. und steht als Literal im Resolver; die Gegenprobe liest die Messdatei. Soll der Tag-Commit die Liste aus der Tag-Messung **erzeugen** (ein Schritt, der `paths.py` schreibt), oder bleibt es beim Literal mit Gegenprobe (heute gebaut)?
> 3. **Schlüssel-Muster der db-Sicherung.** Englisch nach 25f (`key|secret|token|api|passw`), 0 Treffer. Die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` trifft es nicht; laut Code enthält sie nur `erstlauf_am` ⇒ Zeitstempel. Soll das Muster deutsche Wörter mitnehmen? Dann würde diese Datei zurückgehalten, bis der Betreiber entscheidet.

| | Sache | wohin |
|---|---|---|
| (1) | **Die Fragen oben**, dazu die Bestätigung der vorläufigen Berichtigung **43-11** (TB-109 Frage 1) | Fable |
| (2) | **Der Erzeuger** auf dem Signalpfad (43.5 (8)); mit ihm wird `herkunft.py` Teil des Laufbereichs (44-6) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde (43.5 (8)) | Plan-Punkt 7 (TB-101) |
| (4) | Weiter offen aus 43.5: (3) die Kopie in `faltenplan_neun.py`, (4) der ERZEUGT-Block, (5) die Nullzeile im Erzeuger, (9) Fable 25f | wie in 43.5 |

**Aus 43.5 geschlossen:** (1) `auswertung.Abbruch` ⇒ 2 (44-1), (2) die zweite
Öffnung von `herkunft.py` (44-2), (7) 19 über den Laufbereich (44-7). (6) ist
in (1) oben aufgegangen.

> ⭐ **Beantwortet in Fable 26a, siehe 45** (TB-114, 26.09.2026): die Fragen
> aus TB-109, TB-111 und TB-112 in 45.1 bis 45.8, die Bestätigung von 43-11 in
> 45.1. Fragen und Tabelle oben bleiben zeichengleich.

### 44.4 Was hier ausdrücklich NICHT getan wurde

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert, nichts gerechnet** ausser den Nachmessungen nach dem Zusammenführen; die einzige Codeänderung auf `main` ist der Merge selbst (`257e7db`) | — |
| ⛔ | **Kein neues Abbild** — gültig bleibt `e655c1c8…` (44-5); Sonde vorher und nachher gleich (`docs/belege/TB-113/`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — Marken sind neue Zeilen, nichts entfernt | — |
| ⛔ | **Keine Marke in Abschnitt 10** | — |
| ⛔ | **Keine Antwort an Fable vorweggenommen**; der veraltete Satz im Docstring von `auswertung._abbruch_2` steht weiter im Code (TB-111 Frage 2) | 44.3 |
| ⭐ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums | — |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich): 19
· 36.5 · 37.4 · 42.2 E2 · 42.3 F8 · 43-1 · 43-4.

*Dieser Abschnitt ist rein additiv: Er trägt die Tatsachen aus zwei Aufträgen
ein, die zwei Pläne aus 43 und einen Beschluss aus 42 vollzogen haben, und
entfernt nichts.*

## 45. Messbitten nach dem Tag, Reichweite (iv), Eingaben im Abbild, Pflege der Pfadliste, Abnahmebedingungen des Erzeugers — die Einträge aus Fable 26a (TB-114, 26.09.2026)

### 45.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **43**
(TB-110). Anlass ist die **erste gesammelte Tagesanfrage** an den
Verfahrensprüfer — Fable, zeichengleich: „Erste gesammelte Tagesanfrage."
— mit dem neuen Fable-Takt, einmal je Tag: „diese Antwort ist die erste im neuen Takt."
Sie beantwortet die Ergebnisse TB-109 bis TB-113 und die Fragen, die
**44.3** (44-12) zeichengleich sammelt.

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md`
(md5 `e2a492165d44f6ee3d02eba99d2acf2c`, 22 331 Bytes, committet in TB-114
Schritt 0, `79c2dfa`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R1–R8. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0):** Die
Datei hat der steuernde Chat übertragen; die Zitate hier sind zeichengleich
mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage ist, ist nicht
gemessen.

**Die Kette zu 43 und 44:** 43.3 führt die Berichtigung „`None` statt
`False`" als **vorläufig**; 44.3 (1) führt die Fragen aus TB-109, TB-111 und
TB-112 als offen bei Fable. **Beide sind hier beantwortet** (45.1 bis 45.8).
Die Zeilen in 43 und 44 bleiben zeichengleich; Marken darunter verweisen
hierher. Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md`,
Freigabe des Betreibers 26.09.2026, ca. 16:30), nicht Fable.

**Bauart je Eintrag:** 45.1 bis 45.8 tragen je einen Baustein R1 bis R8
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-114/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 45.9 ist eine
Tatsachennotiz des steuernden Chats, 45.10 die Liste des Offenen; der Vollzug
in TB-114 folgt als 45.11.

**Einordnung von R6 — Fables drittes „Unsicher", zeichengleich:**
„Ob R6 eine Ergänzung zu 27 oder zu 7.1 ist — ich schlage 27 vor (es geht um Lesen nach dem Tag); Handwerk der Einordnung."
Eingeordnet ist R6 als Ergänzung zu **27**, wie sein Titel sagt; die Marke
steht **an beiden Orten** (am Ende von 27 und unter 7.1), weil 7.1 die Regel
ist, auf die R6 sich für „Bleibt oder Geht" beruft.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)).

### 45.1 R1 — Marke an 43.3 (Bestätigung)

> **R1 — Marke an 43.3 (Bestätigung).** Die Berichtigung „`selektionsmodus = lambda: None` statt `lambda: False`" ist von Fable bestätigt (26a 3 (1)). Grund: Der Stummel soll das Werkzeug so laufen lassen wie am Stand TB-52; gemessen tut das nur `None` (`strategy_paths` legt 9 von 9 Ordner an), `False` nimmt den Modus-Zweig und meldet trotzdem 0 Unterschiede. Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt". Handwerk als Beifang: Das Werkzeug zählt künftig die angelegten Ordner im Wegwerfbaum und meldet den durchlaufenen Zweig.
> *Quelle des Grundes:* Messung TB-109/TB-113, Prüfprinzip A5. Kein Ergebnis.

**Kette:** bestätigt **43-11** (43.3, „vorläufig, von Fable nicht
bestätigt"); die Überschrift und der Text von 43.3 bleiben zeichengleich, die
Marke steht darunter. Die Zweigprüfung im Werkzeug ist Beifang, kein Auftrag.

### 45.2 R2 — Ergänzung zu 42 (Klasse (iv), Reichweite)

> **R2 — Ergänzung zu 42 (Klasse (iv), Reichweite).** Klasse (iv) umfasst jeden lesenden Zugriff eines Laufs auf seine eigene Zwischenablage: die Verzeichnis-Öffnung beim Aufräumen und das Lesen des darin abgelegten Ergebnisses. Die Probe, die `tempfile` beim Anlegen einer Ablage selbst macht (kein `mkdir` im Protokoll, sofort entfernt), ist Umgebung — Klasse (ii) — und wird als Tatsachennotiz geführt.
> *Quelle des Grundes:* 25b (Definition von (iv): angelegt mit `mkdtemp`, vom Lauf selbst gelesen, entfernt oder im Beleg), 25e 3 (b). Kein Ergebnis.

**Kette:** ergänzt **42.2 E1** (Klasse (iv)); beantwortet TB-109 Frage 2
(44.3). Marke unter 42.2 E1.

### 45.3 R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`)

> **R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`).** Versionierte Dateien, die ein Lauf des Laufbereichs als Daten liest und die kein Code sind, gehören mit ihrem Hash in die Gruppe `eingefroren` des Abbilds — namentlich die neun Listen `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, aus denen der Faltenplan seine Faltenlängen herleitet (TB-95). Die Startprüfung nach 19/E2 bindet Code; das Abbild bindet Eingaben. Dass eine Änderung der Listen den Plan und damit dessen Abbild änderte, ersetzt die Bindung der Eingabe nicht: Der Nachweis verlangt die Eingabe bytegleich und gelesen (24c).
> *Quelle des Grundes:* 25b (Klasse „Code" gegen Eingaben), 24c (zwei Teile des Nachweises), 24c B1. Kein Ergebnis.

**Kette:** ergänzt **30.2 (3)** und **33.3**; beantwortet TB-112 Frage 1
(44.3). Marken unter 30.2 und 33.3. Die Voraussetzung dafür, dass die Gruppe
`eingefroren` diese Pfade aufnehmen kann, ist in **45.9** gemessen; der
Vollzug steht in **45.11**.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitat und Kette oben bleiben zeichengleich.

> ⭐ **45.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 45.4 R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`)

> **R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`).** Die Liste der Pfade der Sauberkeitsprüfung steht als Literal im Resolver; eine Gegenprobe liest die Laufbereichsmessung aus der Messdatei und vergleicht. Am Tag-Commit wird der Laufbereich neu gemessen; weicht die Messung von der Liste ab, ist das ein Befund: Die Liste wird vor dem Tag nachgezogen, nie durch ihn. Die Liste wird nicht aus der Messung erzeugt.
> *Quelle des Grundes:* Prüfprinzip B3 (ein Gegenbeweis gegen eine bewegliche Referenz prüft nichts), 25b E5 (Messung am Tag-Commit). Kein Ergebnis.

> ⭐ **45.4 (R4) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **19** und **42.2 E2**; beantwortet TB-112 Frage 2 (44.3).
Heute gebaut ist genau diese Form (Literal in `shared/paths.py`, Gegenprobe
in `shared/test_arbeitsbaum_laufbereich.py` gegen
`docs/belege/TB-112/a2_laufbereich.txt`, 44-8). Marken unter 19 (unter der
TB-113-Marke) und unter 42.2 E2.

### 45.5 R5 — Abnahmebedingungen des Erzeugers

> **R5 — Abnahmebedingungen des Erzeugers (Ergänzung zu 24b A12 / Plan-Punkt 10).**
> (a) Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `research/vorregistrierung/herkunft.py`; `ARBEITSBAUM_PFADE` ist danach nachgezogen (R4). Bis dahin ist `herkunft.py` am committeten Stand über die Sperrliste (Punkte 11/12) und das Abbild gebunden; die Lücke im Arbeitsbaum ist als Tatsachennotiz in 44 benannt.
> (b) `zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen; eine Zelle ohne Trades trägt die Nullzeile (Sharpe 0 nach Registertext 1c, leere Trade-Liste), nie nichts. Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang.
> (c) `herkunft.datenstand()` endet unter dem Modus ohne übergebenen Pfad mit 2; Beifang der nächsten Öffnung von `herkunft.py`, kein eigener Auftrag.
> *Quelle des Grundes:* 24b A10 (kein Fallback unter dem Modus), 25e (2) (null Trades ist ein Wert), 36.5, 26a 5. Kein Ergebnis.

> ⭐ **45.5 (R5) (a) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **45.5 (b) BERICHTIGT durch R33 (48.1)** (Fable 29b R33, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **41.1 A12** und die Zeile **(5)** in **42.6** (der
Erzeuger auf dem Signalpfad); beantwortet TB-109 Frage 3 (b) und TB-111
Frage 1 (c) (44.3) und Fables Punkt (5) zur Wechselwirkung (a). **(c) ist in
TB-114 vollzogen** (Block B, 45.11). Marken unter 41.1 A12 und in 42.6
Zeile (5).

> ⭐ **45.5 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **45.5 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 45.6 R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag)

> **R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag).** Nach dem signierten Tag werden auf dem Selektionsraum dieses Durchgangs nur die Messungen gerechnet, die vor dem Tag als Messbitte registriert sind (R7). Jede weitere Messung auf denselben Zellen ist ein Versuch: Sie wird im Versuchsregister geführt und zählt in N des nächsten Durchgangs. Keine Messung nach dem Tag — registriert oder nicht — ändert Bleibt oder Geht; das sagt 7.1. Registrierte Messbitten sind Bericht, nicht Tor.
> *Quelle des Grundes:* 7.1, Festlegung 11, Literatur (Story-telling und Data Snooping nach dem Ergebnis, López de Prado; „every backtest must be reported with all trials"). Kein Ergebnis.

**Kette:** ergänzt **27**; beruft sich auf **7.1**. Registertext **vor** dem
Tag, weil er am Tag danach schon gelten muss (Fable 26a 3 (6)). Marken am
Ende von 27 und unter 7.1.

### 45.7 R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a

> **R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a.**
> 1. PBO je Bot über alle Zellen (CSCV, S = 16) — 25f V3.
> 2. MinTRL und Lo-Standardfehler je Gewinnerzelle — 25f V7.
> 3. Netto-Sharpe der Gewinnerzellen unter 0,5 %, 1,0 % und 1,6 % Roundtrip — 25f K2.
> 4. Implizite Kelly-Fraktion je Bot gegen die feste Positionsgrösse — 25f P5.
> 5. Krypto-Umkehr-Bots nach Liquiditätsdrittel des Universums — 25f S8.
> 6. Block-Bootstrap-Band je Gewinnerzelle für den Vergleich mit der Bestätigungsperiode — 25f O2.
> Verfahrensmessungen nach 27.2 (vor dem Tag zulässig, nicht Teil dieser Liste): Adjustierungsstand und Herkunft der 150 Aktienreihen im Snapshot; Nutzung von Preisniveaus je Bot; ob alle neun Bots die geschlossene Kerze lesen; ob TB-85 die Kette Erzeuger → Auswertung deckt. Ergänzungen dieser Liste vor dem Tag sind zulässig und werden datiert; nach dem Tag ist die Liste geschlossen.
> *Quelle des Grundes:* R6. Kein Ergebnis.

**Kette:** Anhang zu **45.6**. Die vier Verfahrensmessungen nach 27.2 sind
nicht Teil der Liste; drei davon sind in 45.10 als offen geführt. Ergänzungen
vor dem Tag werden datiert angehängt, hier oder in einem späteren Abschnitt
mit Marke hier.

> ⭐ **Nr. 7: siehe 46.7 (a)** (Fable 27a R16 (a), TB-117, 26.09.2026). Zitat
> und Kette oben bleiben zeichengleich.

### 45.8 R8 — Tatsachennotizen 26a

> **R8 — Tatsachennotizen 26a.**
> (a) `auswertung._abbruch_2`: Der Docstring sagt „`Abbruch` … endet mit 1"; falsch seit TB-111, stehen geblieben wegen der Freigabe „sonst nichts"; Streichung mit der nächsten planmässigen Öffnung.
> (b) `str(e)` eines gefangenen `Abbruch` ist `"2"`, die Meldung steht in `e.meldung`; im Laufbereich (81 Module, Stand TB-113) liest kein Aufrufer `str(e)` — Suchmuster in der Notiz nennen, Messung am Tag-Commit wiederholen.
> (c) db-Sicherung (25f O6): Schlüssel-Muster `key|secret|token|api|passw`, 0 Treffer über 12 Datenbanken; die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` enthält laut Code nur `erstlauf_am`; deutsche Wörter nicht aufgenommen — Betrieb, nicht Lauf.
> (d) N = 653 (Register 9): Was das Versuchsregister nicht zählt und nicht rekonstruieren kann, steht dort in 3.4 und 5.1–5.4; ein Verweis aus Register 9 auf Abschnitt 5 des Versuchsregisters wird nach dem Tag eingetragen. Folge für die Lesart: N_nominal ist eine Untergrenze.
> (e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genannt.
> *Quelle des Grundes:* Messungen TB-111, TB-112, TB-113, 26a 3 (a)/(b). Kein Ergebnis.

**Kette:** (a) und (b) beantworten TB-111 Fragen 2 und 3, (c) TB-112 Frage 3
(44.3). ⛔ **(a) ist nicht vollzogen:** Der Docstring von
`auswertung._abbruch_2` bleibt bis zur nächsten planmässigen Öffnung von
`auswertung.py` stehen. ⛔ **(d) ist nicht vollzogen:** Der Verweis aus
Register 9 kommt **nach** dem Tag; in 9 steht deshalb heute keine Marke.

### 45.9 Tatsachennotiz des steuernden Chats zu R3 — zwei Pfadregeln

Fables erstes „Unsicher", zeichengleich:
„Ob die Gruppe `eingefroren` des Abbilds heute Dateien ausserhalb `research/vorregistrierung/` aufnehmen kann"

**Gemessen am 26.09.2026 über die Brücke am Stand `0df8c64`, nur lesend** (vom
steuernden Chat; in TB-114 am Stand `79c2dfa` wiederholt, beide Dateien
unverändert):

- `herkunft.register()` löst jeden Eintrag von `EINGEFROREN` mit
  `os.path.join(_HIER, rel)` auf, also immer relativ zu
  `research/vorregistrierung/` — die Zeile, zeichengleich:
  `pfad = os.path.normpath(os.path.join(_HIER, rel))`
- `shared/sperrlistensonde.py::_aufloesen` löst einen Eintrag nur dann
  relativ zu `research/vorregistrierung/` auf, wenn er kein `/` enthält oder
  mit `ergebnisse/` beginnt; sonst repo-relativ (Feld `pfadregel` im Abbild) —
  die Zeile, zeichengleich:
  `if "/" not in pfad or pfad.startswith("ergebnisse/"):`
- **Folge:** Ein Eintrag für `research/tb24_haltedauern/daten/…` wäre in einem
  der beiden Programme nicht auffindbar. `register()` führt eine nicht
  gefundene Datei in `fehlend` und rechnet ohne sie weiter:
  `fehlend.append(rel)`
- Die zehn heutigen Einträge sind von der Abweichung nicht betroffen: jeder
  hat entweder kein `/` oder das Präfix `ergebnisse/`, beide Regeln liefern
  denselben Ort.
- **Vollzug:** Block B von TB-114 (45.11).

### 45.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | Die drei Verfahrensmessungen nach 27.2: ob alle neun Bots die **geschlossene Kerze** lesen; **Adjustierungsstand und Herkunft der 150 Aktienreihen** im Snapshot; ob **TB-85** die Kette Erzeuger → Auswertung deckt | TB-115 |
| (2) | **Der Erzeuger** auf dem Signalpfad, mit den Abnahmebedingungen aus 45.5 (a) und (b) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde | Plan-Punkt 7, TB-101 |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3; Fable 26a 2 (a), R8 (e)) | Stufe IV |
| (5) | R8 (a) Docstring `auswertung._abbruch_2`; R8 (d) Verweis in Register 9 | nächste Öffnung von `auswertung.py`; nach dem Tag |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
7.1 · 19 · 27 · 30.2 · 33.3 · 41.1 A12 · 42.2 E1 · 42.2 E2 · 42.6 Zeile (5)
· 43.3 · 44.3. ⛔ Keine in Abschnitt 10, keine in 9.

> ⭐ **Beantwortet und fortgeschrieben in 45.11 und 46** (Fable 27a, TB-117,
> 26.09.2026). Tabelle und Text oben bleiben zeichengleich.

### 45.11 R11 — Abbild gültig; Tatsachennotiz zum Abbruch TB-114 (Fable 27a, TB-117, 26.09.2026)

> **R11 — 45.11 (Abbild gültig; Tatsachennotiz zum Abbruch TB-114).** Gültiges Abbild ist `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json`, `5e5ad109…` (10 805 B, 14 Punkte, `eingefroren` 19, HEAD `0b7ab4b`); Sonde dagegen 34/0/0, (ii) 0, gemessen TB-114 C und TB-115 0b (vorher = nachher). Tatsachennotiz: TB-114 endete in Block C mit Abbruchkriterium, weil der Auftrag gegen das alte Abbild `e655c1c8…` „die neun neuen Einträge in `eingefroren`" als Befund erwartete; die Sonde meldet Zuwachs in `EINGEFROREN` gegen ein altes Abbild nur mittelbar über den Hash von `herkunft.py` (Punkte 11/12). Zwei Ursachen: eine ungemessene Erwartung im Auftrag (Regel des steuernden Chats: Erwartungen an ein Werkzeug nur mit Fundstelle) und eine einseitige Sonde (R9). Der Abbruch war regelgerecht; nichts wurde repariert. Nach dem Bündel (R9, R10, R14, R15) folgt ein neues Abbild nach 37.3.
> *Quelle des Grundes:* Messungen TB-114/TB-115, Nachtrag 6d (Abbruchkriterium führt zu Abbruch, nie zu Rückfrage). Kein Ergebnis.

**Kette:** Vollzug der in **45.0** angekündigten Nummer 45.11 — nicht durch
TB-114 (Abbruch in Block C, `e07fefd`/`90307cb`), sondern mit Fables Antwort
27a (T114-2) in TB-117. Das Abbild ist seit TB-114 unverändert; gemessen am
Eingang von TB-117 (`753ec11`, `docs/belege/TB-117/0b_ausgang.txt`): sha256
`5e5ad1097909b3531e19b238153cabc46e7b551bb25e369ddc6735836e71cd06`, Sonde
dagegen 34/0/0. Der Satz in R11 „Nach dem Bündel (R9, R10, R14, R15) folgt
ein neues Abbild nach 37.3" wird in TB-117 Block E vollzogen; das Ergebnis
steht in **46.11**. Bis dahin gilt `5e5ad109…`. Die Marke unter 45.10 zeigt
hierher und auf 46.

## 46. Sonde zweiseitig, `fehlend` im Modus, zwei Erzeuger, Snapshot-Bindung, Herkunftsprüfung in `auswertung.py` — die Einträge aus Fable 27a (TB-117, 26.09.2026)

### 46.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **45**
(TB-114). Anlass ist die Tagesanfrage 27a an den Verfahrensprüfer
(`FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md`) zu den Ergebnissen **TB-114** (Register 45,
dritte Öffnung von `herkunft.py`, Abbruch in Block C) und **TB-115** (drei
Verfahrensmessungen, nur lesend). Fables Einordnung, zeichengleich:
„**Ein Bündel, eine Freigabekarte je Sperrlistendatei** (`herkunft.py`, `auswertung.py`, Sonde), dann ein Abbild."

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md`
(md5 `d4367c65a9dcad4b28cceb6f50706d59`, 30 836 Bytes, committet in TB-117
Schritt 0, `753ec11`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R9–R17. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0,
45.0):** Die Datei hat der steuernde Chat übertragen; die Zitate hier sind
zeichengleich mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage
ist, ist nicht gemessen.

**Die Kette zu 45:** R11 ist die in 45.0 angekündigte Nummer **45.11** und
steht deshalb am Ende von 45, nicht hier. R9, R10, R12 bis R17 stehen als
**46.1 bis 46.8** in der Reihenfolge des Codeblocks. 45.7 (R7) bekommt mit
R16 (a) eine Nummer 7 der Liste; 45.5 (R5) mit R16 (b) einen Punkt (d); 45.8
(R8 (a)) wird mit der Öffnung von `auswertung.py` in TB-117 vollzogen (46.11).
Die Nummer 46 hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20), nicht Fable.

**Bauart je Eintrag:** 45.11 und 46.1 bis 46.8 tragen je einen Baustein
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-117/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 46.9 ist eine
Lesart des steuernden Chats, 46.10 die Liste des Offenen; der Vollzug in
TB-117 folgt als 46.11.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)); die
Tatsachennotiz „an Punkt 8" aus R15 (a) steht deshalb in **46.6**, mit
Verweis auf Punkt 8. ⛔ **In Abschnitt 9 steht keine Marke.**

### 46.1 R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite)

> **R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite).** Die Sonde prüft die Gruppe `eingefroren` aus dem Abbild heraus (Abbild → Dateien) **und** vergleicht die heutige Menge `herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds (Liste → Abbild). Ein Eintrag, der in einer der beiden Mengen fehlt, ist ein Befund ⇒ 1, mit Nennung des Eintrags und der Seite. Die Gruppen kommen weiter aus dem Abbild; neu ist nur der Vergleich der Mengen.
> *Quelle des Grundes:* Prüfprinzip C4 (eine Prüfung, die nicht sagt, gegen was sie prüft; zweiseitiger Nachweis), Messung TB-114 Block C. Kein Ergebnis.

**Kette:** ergänzt **40.8 (e)** (die Sonde liest die Gruppen aus dem Abbild);
beantwortet T114-2 (Fable 27a Abschnitt 2). Marke in 40.8 als eigene
Tabellenzeile direkt unter der Zeile (e). **Fables erstes „Unsicher",
zeichengleich:**
„Ob `sperrlistensonde.py` selbst im Abbild oder auf der Sperrliste steht — wenn ja, folgt der Sonden-Öffnung ein Abbild nach 37.3; wenn nein, nicht. Nicht gemessen."
**Gemessen (TB-117, am Stand `753ec11`, nur lesend):** Der Listentext von
Abschnitt 10 nennt `sperrlistensonde` 0-mal; das Abbild `5e5ad109…` nennt die
Sonde einmal, und zwar nur als Parser im Feld `erzeugt`
(`"parser": "shared/sperrlistensonde.py::lies_abschnitt_10"`), in keinem
Punkt und in keiner Gruppe. Das neue Abbild nach dem Bündel folgt trotzdem, weil
`herkunft.py` und `auswertung.py` geöffnet werden (R11). Vollzug in TB-117
Block B (46.11).

### 46.2 R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`)

> **R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`).** `register()` und `block()` enden unter dem Modus mit 2, wenn `fehlend` nicht leer ist; die Meldung nennt die fehlenden Einträge. Ohne Modus bleibt `fehlend` ein Feld und eine Druckzeile der Prüfansicht. Die neun TB-24-Listen werden nicht in `ARBEITSBAUM_PFADE` aufgenommen (R3: die Sauberkeitsprüfung bindet Code); eine fehlende Liste wird über `register()` ⇒ 2, die Sonde (Gruppe `eingefroren`) und den Abbruch in `faltenplan.py` sichtbar. Umsetzung mit der nächsten Öffnung von `herkunft.py`, zusammen mit dem Nachtrag im Modulkopf (R17 a).
> *Quelle des Grundes:* 24b A2 (ein Wert, der so tut, als wäre er gemessen), 41.1 A10. Kein Ergebnis.

**Kette:** ergänzt **41.1 A10** (kein Fallback unter dem Modus); beantwortet
T114-1. Marke unter dem „Stand, gemessen" von A10. Der Nachtrag im Modulkopf
(R17 (a), 46.8) gehört zu derselben Öffnung. Vollzug in TB-117 Block C
(46.11).

### 46.3 R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen)

> **R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen).** Es gibt zwei Erzeuger: den **Listen-Erzeuger** auf dem Signalpfad (40.6, 41.1 A12; heute `research/tb24_haltedauern/positionen_holen.py`, `--ziel`, Einmal-Schreibsperre), der die Trade-Listen vor dem Tag einmal auf dem Snapshot neu erzeugt, und den **Zellen-Erzeuger** (Plan-Punkt 10, R5), der `zellen.csv`, `tagesreihen/` und `herkunft.json` schreibt. `herkunft.py::EINGEFROREN` bindet die neun heutigen Listen unter `research/tb24_haltedauern/daten/`, bis die Listen nach 40.6 neu erzeugt sind und `faltenplan.py` sie über die registrierte Pfadkonstante liest; dann treten die neuen Listen an ihre Stelle, die alten bleiben als historischer Stand liegen und verlassen `EINGEFROREN` (gebunden wird, was gelesen wird, R3); ihre Hashes stehen in `docs/belege/TB-114/`. Die Öffnung von `herkunft.py` dafür erfolgt mit der Neuerzeugung, nicht davor. Der Pfad der neuen Listen ist bis dahin nicht registriert (TB-114 B3).
> *Quelle des Grundes:* 40.6, 41.1 A12, R3, R5. Kein Ergebnis.

**Kette:** Tatsachennotiz zu **40.6**, **41.1 A12** und **45.3**; beantwortet
T114-3 und berichtigt die Lesart der Anfrage („folgt dann dem Pfad des
Erzeugers (R5)" — gemeint ist 40.6). Marken am Ende von 40.6, unter der
TB-114-Marke von 41.1 A12 und am Ende von 45.3. ⛔ **Nicht vollzogen und nicht
Teil von TB-117:** Die Listen werden nicht neu erzeugt, `EINGEFROREN` behält
die neun heutigen Listen.

> ⭐ **46.3 ERGÄNZT durch R39 (48.7)** (Fable 29b R39, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 46.4 R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4)

> **R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4).**
> (a) `XAUTUSDT_1h.csv` im Datenstand `d9449faf…` endet auf einer Teilkerze (letzte Kerze `2026-08-30 18:00`, geschrieben 18:39:01 UTC, 21 min vor Kerzenschluss). Kein Lauf liest sie, weil vier Ausschlussmengen das Symbol streichen: `shared/symbols_config.py::EXCLUDE_SYMBOLS`, `messgroessen.py::AUSGESCHLOSSEN`, `faltenplan_neun.py::KRYPTO_AUSSCHLUSS`, `benchmark.py:145`. Wache: eine Probe liest die vier Mengen ein und verlangt Gleichheit (Handwerk, keine Sperrlistennähe). Zusammenlegung auf einen Ort mit der jeweils nächsten planmässigen Öffnung, nicht vor dem Tag.
> (b) 175 Dateien des Datenstands (150 Aktien-1d, 25 Krypto-1h) haben keinen feineren Zeugen für `rand_letzte`; ihr Rand ist durch Schreibpfad und Zeitstempel belegt (TB-115 M1: Aktien letzte Kerze `2026-09-01`, geschrieben 02.09. 04:20–04:22 UTC; Krypto gemeinsamer Stand 15.09. 09:00–09:59 UTC). Der Beleg gilt als Tag-Vorbedingung erfüllt; keine laufende Prüfung eingefrorener Daten.
> (c) Adjustierungsstand der 150 Aktienreihen: split- und dividendenbereinigt, rückwärts, Schnitt je Symbol am letzten Ex-Tag vor dem 02.09.2026 (`yf.download(…, auto_adjust=True)`, kein `Adj Close`); Abrufcode nicht versioniert, nächstliegend `0f6491b`; yfinance-Fassung nicht belegbar; keine Regel eines Aktien-Bots nutzt ein absolutes Preisniveau (P1 = 0 Fundstellen, TB-115 M2 (c)). Schliesst die Verfahrensmessung D3 aus R7.
> (d) Stufe 3 der Zuteilungskaskade (`shared/zuteilung.py`, Punkt 10) reiht nach dem Median von `close × volume` über 20 Tage über Symbole hinweg; `volume` ist split-bereinigt, `close` split- und dividendenbereinigt — das Dollar-Volumen eines Dividendenzahlers ist in der Vergangenheit um das Produkt seiner späteren Ausschüttungen zu klein ausgewiesen. Stufe 3 entscheidet bei `volatility_breakout`, `elliott_wave_stocks`, `turtle_soup_stocks` (keine Signalspalte) bei leerem Buch; Krypto nicht betroffen. Eigenschaft der eingefrorenen Eingabe; **keine Änderung vor dem Tag** (die Korrektur bräuchte Daten, die der Snapshot nicht hat; Ersatzgrössen änderten die Bedeutung der Regel). Wie oft Stufe 3 entscheidet, ist Messbitte R7 Nr. 7.
> (e) Papierpfad: Die beiden Elliott-Bots messen die Signalfrische (`SIGNAL_FRESHNESS_HOURS`) an `pd.Timestamp.utcnow()` statt an `entscheidungskerze.laufbeginn()`; keine Kerzenwahl, wirksam nur an der 48-h-Grenze. Betrieb, mit der nächsten Öffnung von `forward_test.py`, nach dem Tag.
> (f) Tatsachennotiz zu 16.4 (Evidenz der Leiter): `forward_test.py` legt `entry_price`/`stop_price` (Elliott auch `target_price`) als absolute Zahlen ab und vergleicht sie in späteren Läufen mit neu bereinigten Reihen; über einen Ex-Tag oder Split hinweg passen Niveau und Reihe nicht mehr zusammen. Betroffen sind die Bots mit Stop (`volatility_breakout`, `elliott_wave_stocks`) und `pnl_pct` aller vier Aktien-Bots. Der Selektionspfad ist frei davon. Behebung im Betrieb nach dem Tag, vor dem ersten Stufenwechsel der Leiter, der sich auf Papier-Evidenz stützt.
> *Quelle des Grundes:* Messungen TB-115 M1/M2, 31.3, 37.3, Plan-Punkt 6, 16.4 (i). Kein Ergebnis.

> ⭐ **46.4 R13 ERGÄNZT durch R79 (55.2)** (Fable 07a R79, Unterpunkt (d), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** beantwortet F1-1 bis F2-3 (Fable 27a Abschnitt 3, M1 und M2).
Marke unter **16.4** („Prüfung vor dem Tag") für (f). Die Notizen (a) bis (e)
stehen hier und nicht an 5e, 28, 31 und Punkt 10, weil diese Stellen
Registertext bzw. Sperrlistentext sind (Punkt 10 liegt in Abschnitt 10, dort
steht keine Marke). ⭐ **(a) Die Probe** (vier Ausschlussmengen gleich) wird
in TB-117 Block E gebaut, ausserhalb der Sperrlistendateien; die Mengen
werden nur gelesen (46.11). ⛔ **(d) ändert vor dem Tag nichts** an
`shared/zuteilung.py`; die Messbitte steht als R7 Nr. 7 in 46.7 (a).

### 46.5 R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`)

> **R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`).** `auswertung.py` liest `<wurzel>/<bot>/herkunft.json` für jeden Bot und endet mit 2, wenn die Datei fehlt, wenn der Commit-Hash vom Tag-Commit (5e, `TB_SELEKTIONSCOMMIT`) abweicht, wenn der Datenstand-Hash vom registrierten Datenstand `d9449faf…` abweicht, wenn der Register-Hash von `herkunft.register()` zur Laufzeit der Auswertung abweicht, oder wenn die neun `herkunft.json` untereinander abweichen. Der Bericht trägt Commit, Datenstand und Register-Hash in seinem Kopf. Der Schreiber von `herkunft.json` (Zellen-Erzeuger) prüft sich nicht selbst; der Auswerter prüft ihn. Umsetzung: eine Öffnung von `auswertung.py` (Punkte 3/5/14) vor dem Tag, zusammen mit der Streichung aus R8 (a); Hash-Übergang nach 37.3.
> *Quelle des Grundes:* Docstring von `auswertung.py` Z. 51–52 (nennt `herkunft.json` als Teil des Vertrags), Abschnitt 12 (Vertragsbruch ⇒ Abbruch), 36.5, 25c (1) (Register-Code-Widerspruch ist 2), Prüfprinzip A8. Kein Ergebnis.

> ⭐ **46.5 (R14) ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.5 (R14) ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.5 (R14), Bedingung 5 ERGÄNZT durch R27 (47.10)** (Fable 27c R27, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **12** (Vollständigkeitstest; `auswertung.py` bricht bei
jeder Verletzung des Datenvertrags ab) und **36.5** (Ausgänge); beantwortet
F3-3. Marken am Ende von 12 und am Ende von 36.5. Was R14 ohne Modus
bedeutet, sagt R14 nicht; die Lesart des steuernden Chats steht in **46.9**.
Vollzug in TB-117 Block D (46.11), zusammen mit R8 (a) (45.8).

### 46.6 R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8

> **R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8.**
> (a) Das Abbild der Sperrliste führt in der Gruppe `eingefroren` zusätzlich `snapshots/<hash>/MANIFEST.json` und die Snapshot-Kopien von `config/top25_symbols.txt` und `config/sp500_top150.txt` (heute bytegleich mit dem Repo, `3afc95a4…`, `6acba892…`). Punkt 8 bleibt im Wortlaut (bindet die Repo-Dateien); Tatsachennotiz an Punkt 8: unter dem Modus liest der Lauf die Snapshot-Kopien, gebunden über das Abbild.
> (b) Tag-Vorbedingung: `snapshot.py --pruefen` endet am Tag-Commit mit UNVERAENDERT (rc 0), Beleg im Tag-Ordner. Die Startprüfung vergleicht `TB_SELEKTIONSHASH` weiter mit dem im MANIFEST notierten Hash; sie rechnet den Snapshot nicht nach — den gerechneten Datenstand trägt die Kette (R5 (d), R14).
> *Quelle des Grundes:* R3 (das Abbild bindet Eingaben), Prüfprinzip A8 (Selbstauskunft ist keine Wache), 25f A3 (keine Wache doppelt). Kein Ergebnis.

**Kette:** beantwortet F3-1 und F3-2. ⭐ **Tatsachennotiz an Punkt 8 der
Sperrliste (Abschnitt 10), hier statt dort, weil in 10 keine Marke steht:**
Punkt 8 bleibt im Wortlaut und bindet die Repo-Dateien
`config/top25_symbols.txt` und `config/sp500_top150.txt`; unter dem Modus
liest der Lauf die Snapshot-Kopien, gebunden über das Abbild (Gruppe
`eingefroren`, R15 (a)). (a) wird in TB-117 Block C vollzogen
(`herkunft.py::EINGEFROREN`) und im neuen Abbild (Block E) gebunden
(46.11). (b) ist Tag-Vorbedingung und wird am Tag-Commit gemessen, nicht in
TB-117.

### 46.7 R16 — Ergänzungen zu R5 und R7

> **R16 — Ergänzungen zu R5 und R7.**
> (a) R7 Nr. 7: Wie oft entscheidet Stufe 3 der Zuteilungskaskade je Aktien-Bot und Falte, und wie oft wäre die Rangfolge unter Stückzahl × Split-Faktor eine andere? Bericht, kein Tor (R13 d).
> (b) R5 (d): Der Zellen-Erzeuger schreibt in `herkunft.json` den mit `herkunft.datenstand(<Snapshot-Datenordner>)` **gerechneten** Datenstand-Hash, nicht den im MANIFEST notierten, dazu Commit und `herkunft.register()`.
> *Quelle des Grundes:* R6/R7, R14, R15. Kein Ergebnis.

**Kette:** (a) ist **Nr. 7** der Liste in **45.7** (R7), vor dem Tag
ergänzt und damit nach 45.7 zulässig, datiert 26.09.2026 (Fable 27a);
Marke unter 45.7. (b) ist Punkt **(d)** zu **45.5** (R5); gilt für den
Zellen-Erzeuger, der noch nicht gebaut ist.

### 46.8 R17 — Tatsachennotizen 27a

> **R17 — Tatsachennotizen 27a.**
> (a) Modulkopf von `herkunft.py` beschreibt `register` als Hash über „die Registerdatei, die Module dieses Ordners und die vorab berechneten Tabellen"; seit TB-114 B3 gehören die neun TB-24-Listen dazu. Nachtrag mit der nächsten Öffnung (R10).
> (b) Testannahmen TB-114 nach Grundsatz 40: `test_ersatzwerte.py` E-bM (Mutation der ersten Wache endet an der zweiten mit 2 statt 0; Ort `block` weiter verlangt), `test_sperrlistensonde.py` 8a (10 ⇒ 19), H7f (25 ⇒ 34); die Fassungen am Stand `77147f7` brechen genau dort (60/61, 57/59).
> (c) M1 (TB-115): 9/9 Bots entscheiden auf der geschlossenen Kerze — Papierpfad über `entscheidungskerze.lade` (je 1 Aufruf, 0 Abrufe an der Schicht vorbei), Selektionspfad über den Rand des Datenstands. Schliesst die Verfahrensmessung aus R7. Randbefund R2 (Endgültigkeit des yfinance-Schlusskurses um 20:15 UTC) ist Betrieb, nicht gemessen.
> (d) M3 (TB-115): Die Sonde bindet von der Kette Datenstand → Zellen-Erzeuger → `zellen.csv` → `auswertung.py` → Bericht nur Glied 4 samt Importen und Tabellen; Glieder 1, 3 und 5 werden über R14 und R15 gebunden, Glied 2 mit dem Zellen-Erzeuger (R5). Damit ist die vierte Verfahrensmessung aus R7 („deckt TB-85 die Kette") beantwortet: nein.
> *Quelle des Grundes:* Messungen TB-114/TB-115. Kein Ergebnis.

**Kette:** (a) wird mit der Öffnung von `herkunft.py` in TB-117 Block C
vollzogen (46.11). (b) bis (d) sind Tatsachen; (c) und (d) schliessen die
Verfahrensmessungen aus 45.7 (R7) und damit Zeile (1) von 45.10.

### 46.9 Lesart des steuernden Chats zu R14 ohne Modus — von Fable zu bestätigen (Tatsachennotiz)

R14 nennt die fünf Abbruchbedingungen, sagt aber nicht, ob sie auch ohne
Selektionsmodus gelten. Der steuernde Chat hat im Auftrag eine Lesart
festgelegt und für Fable benannt, zeichengleich
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20):

„R14 unter dem Modus vollständig: Jede der fünf Bedingungen endet mit 2. Ohne Modus liest `auswertung.py` `herkunft.json`, wenn vorhanden, und zeigt Commit, Datenstand und Register-Hash im Kopf des Berichts, bricht aber nicht ab. Grund: Ohne Modus laufen Beispieldaten und Tests, und `beispieldaten.py` schreibt Nullwerte (Z. 210 ff.). Dieselbe Bauart wie R10 (`fehlend` ⇒ 2 nur unter dem Modus)."

⚠️ **Vorläufig, bis Fable bestätigt.** TB-117 setzt diese Lesart in Block D
um; weicht Fables Antwort ab, ist das eine weitere Öffnung von
`auswertung.py`.

> ⭐ **46.9 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 46.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **Leiter-Lesarten** zu 16.4 (TB-116, fünf Stellen L1–L5) | Fable |
| (2) | **Der Listen-Erzeuger** nach 40.6 (41.1 A12, 45.5, 46.3) | Plan-Punkte 3 und 5 |
| (3) | **Der Zellen-Erzeuger** (Stufe V; 45.5, 46.7 (b)) | Stufe V |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3) | Stufe IV |
| (5) | Bestätigung der Lesart **46.9** | Fable |
| (6) | R15 (b) `snapshot.py --pruefen` als Tag-Vorbedingung | am Tag-Commit |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
12 · 16.4 · 36.5 · 40.6 · 40.8 (e) · 41.1 A10 · 41.1 A12 · 45.3 · 45.7 ·
45.10. ⛔ Keine in Abschnitt 10, keine in 9.

### 46.11 Vollzug in TB-117 (Tatsachennotiz)

**Gemessen in TB-117, 26./27.09.2026** (Belege `docs/belege/TB-117/`, Ergebnis
`docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`). Eingang `8b342ab`, Schritt 0
`753ec11`, Block A `4c5615d` (45.11 und 46.0–46.10). Freigabe des Betreibers
26.09.2026, ca. 22:20 (Auswahlkarte, wörtlich im Auftrag). Kein
Abbruchkriterium ausgelöst.

**Hash-Übergänge nach 37.3:**

| Block | Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|---|
| B | `shared/sperrlistensonde.py` | `f88e54ee…` | `98c02e0e…` | `42ef509` | R9 (46.1) |
| C | `research/vorregistrierung/herkunft.py` | `ed521ac1…` | `c6c13388…` | `ff2f254` | R10 (46.2), R15 (a) (46.6), R17 (a) (46.8) |
| D | `research/vorregistrierung/auswertung.py` | `a864b216…` | `8ec45123…` | `852f253` | R14 (46.5), Lesart 46.9, R8 (a) (45.8) |

**`herkunft.register()`:** `5acb4c19…` (Eingang) ⇒ `6bcb4f58…` (nach
Block A) ⇒ `b8f2cc33…` (nach Block C; 23 Teile, `fehlend` leer) ⇒
`e87a4d8e…` (nach Block D, gemessen vor diesem Eintrag). Der Wert nach
diesem Eintrag kann hier nicht stehen (er hasht diesen Text); er steht im
Ergebnis.

**B (R9):** Die Sonde vergleicht zusätzlich die heutige Liste
`herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds; ein
Eintrag nur auf einer Seite ist Befund 1 mit Eintrag und Seite
(„Liste → Abbild fehlt“ bzw. „Abbild → Liste fehlt“). Gegen das alte Abbild
`e655c1c8…` meldet sie die neun TB-24-Listen „nur in der Liste“ — die Zeile,
die R11 als fehlend beschreibt.

**C (R10, R15 (a), R17 (a)):** `register()` und `block()` enden unter dem
Modus mit 2, wenn `fehlend` nicht leer ist (je eigene Fundstelle, Meldung
nennt die Einträge); ohne Modus unverändert. `EINGEFROREN` führt zusätzlich
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json`
und die beiden Kopien `…/config/top25_symbols.txt` und
`…/config/sp500_top150.txt` des Snapshots aus Register 18 — versioniert,
repo-relativ, in `herkunft.py` und Sonde gleich aufgelöst; **keine dritte
Pfadauflösung**. Die `config/`-Kopien stecken im Snapshot-Hash (225 Dateien),
nicht im Datenstand (223). Die Tatsachennotiz an Punkt 8 steht in 46.6.

**D (R14, Lesart 46.9, R8 (a)):** `auswertung.py` liest `herkunft.json`
unter dem Modus für alle neun Bots und endet mit 2 bei jeder der fünf
Bedingungen; der registrierte Datenstand steht als Konstante
`REGISTRIERTER_DATENSTAND` mit Fundstelle Register 18. Ohne Modus: nur
Anzeige. Der Kopf des Berichts trägt Commit, Datenstand und Register-Hash.
Der Satz „`Abbruch` … endet mit 1“ ist berichtigt; damit ist Zeile (5) von
45.10 für R8 (a) erledigt.

**Gültiges Abbild ab jetzt** (nach R11 „nach dem Bündel ein neues Abbild“):
`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`,
sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f`
(11 432 B, 14 Punkte, `eingefroren` 22 = `EINGEFROREN`, HEAD `852f253`).
Sonde dagegen 37/0/0, (ii) 0, Mengenvergleich 22/22 ohne Befund. Es ersetzt
`5e5ad109…` (45.11); nichts ist überschrieben.

**Sonde gegen `5e5ad109…`, jeder Eintrag zugeordnet:** Punkte 3, 5, 14 und
Gruppe `eingefroren`: `auswertung.py` (Block D); Punkte 11, 12:
`herkunft.py` (Block C); Gruppe `eingefroren`, „Liste → Abbild fehlt“:
MANIFEST und die zwei Snapshot-`config/`-Kopien (Block C). Kein Eintrag ohne
Zuordnung.

**Probe R13 (a):** `shared/test_ausschlussmengen.py` liest die vier
Ausschlussmengen mit `ast` (keine importiert, keine geändert) und verlangt
Gleichheit samt `XAUTUSDT` — 9/9, drei Mutationen je mit Gegenprobe. Die
Zusammenlegung bleibt der jeweils nächsten planmässigen Öffnung.

**Unverändert gemessen:** Benchmark im Modus Repo und frischer Klon
`64fb2912…`; acht Ausgaben ohne Modus bytegleich mit TB-114; Trockenlauf
9 × rc 0; `faltenplan.json` `0e54ac5c…`; Laufbereich 81 Module (= TB-114).
Tests am Stand `54ce889`:
44 Dateien, 41 rc 0 (darunter `test_vorregistrierung` 196/196,
`test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65,
`test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44,
`test_arbeitsbaum_laufbereich` 26/26); ohne rc 0 nur die drei bekannten
ohne Bezug zu diesem Auftrag (`test_drawdown_beide_masse` terminiert nicht,
`test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben
Stellen wie TB-114).

**Nicht vollzogen in TB-117:** R12 (Neuerzeugung der Listen), R15 (b) (am
Tag-Commit), R16 (a) (nach dem Tag) und (b) (mit dem Zellen-Erzeuger), die
Bestätigung von 46.9 durch Fable.

## 47. Fable 27c — Registerblock R18–R32 (TB-126)

Reines Eintragen von Registertext, Bauart wie 46 (46.0). Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`, md5 `ff96392ed654fdcae2e991e51e424dc5`, 48 420 B, am Commit `0f56aeb`, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert“, Z. 161–209. Die Datei hat der steuernde Chat am 29.09.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` rc 0; Bytegleichheit mit der Ablage war mit dem Werkzeug nicht messbar. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern hat der steuernde Chat vergeben (Auftrag TB-126, Einzelfreigabe des Betreibers), nicht Fable. Die Regel aus 34 gilt weiter: Marke am alten Ort, der alte Satz bleibt zeichengleich. ⛔ In Abschnitt 10 steht keine Marke; was dorthin gehört, steht in der Kette und als Indexzeile in `REGISTER_INDEX.md`. Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 50.1.

### 47.1 R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1)

> **R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1).** Das Buch wird zuerst nach dem Klassenschlüssel (l) auf die Anlagen geteilt. Der Zellenanteil in (m) ist der Anteil der Zelle am Budget ihrer Anlage: zu gleichen Teilen unter den Zellen dieser Anlage nach (g). „Aktive Zellen teilen das Buch zu gleichen Teilen" in (h) ist innerhalb der Anlage zu lesen. Eine Zusammensetzung von (h) und (m), die Buch unverteilt lässt, ist keine Lesart: 7.1 sagt „nicht in Kasse", und 16.4 kennt keinen Anteil, der weder in Bots noch in einer Benchmark-Position liegt.
> *Quelle des Grundes:* (l) „skaliert die Zellen einer Anlage gemeinsam" (eine Gruppe gemeinsam skalieren legt ihre Summe fest); (j) nennt die Benchmark-Position „ihrer Anlage" als Behälter der Zelle; 7.1. Kein Ergebnis.

**Kette:** Marken: 16.4 (m); 16.4 (h); 16.4 (l).

### 47.2 R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4)

> **R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4).** Die Zahl der Zellen in (h) ist die Zahl der Zeilen in (g), nicht die Zahl der gerade aktiven Zellen. Eine Zelle, in der kein Bot auf Grundbudget oder Bestätigt steht, behält ihren Anteil und hält ihn nach (j) als statische Benchmark-Position ihrer Anlage; die übrigen Zellen wachsen nicht. Eine neue Zelle im Sinn von (k) entsteht nur durch eine neue Zeile in (g) — einen nach 16.8 zugelassenen Bot, dessen Quelle × Anlage in (g) noch nicht steht. Erhält ein Bot einer bestehenden Zelle über einen neuen registrierten Lauf wieder Grundbudget (6 (d), 7.1), geht der Anteil seiner Zelle aus der Benchmark-Position an ihn zurück; die Zahl der Zellen ändert sich nicht. Ein neu zugelassener Bot in einer bestehenden Zelle tritt in deren Teilung nach (i) ein; auch das ändert sie nicht. Die Zahl der Zellen hat keine Vorgeschichte.
> *Quelle des Grundes:* (j) „nicht an andere Zellen"; das Prinzip „Die Leiter bewegt Bots. Sie bewegt keine Zellen."; (g) „die Zuordnung … ändert sich nur mit dem Bot"; (k) „folgt aus Zulassung, nicht aus Ergebnis". Kein Ergebnis.

**Kette:** Marken: 16.4 (h); 16.4 (j); 16.4 (k).

### 47.3 R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3)

> **R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3).** Der Klassenschlüssel (l) gilt auch dann, wenn eine Anlage keine aktive Zelle hat. Ihr Anteil nach (l) hält die statische Benchmark-Position dieser Anlage; er geht nicht an die andere Anlage.
> *Quelle des Grundes:* (l) ist ein Betreiberentscheid über den Risikobeitrag (Begründung 80/20 in 16.4), gültig bis Netting, und nicht danach gesetzt, welche Anlage läuft; (j) „nicht an andere Zellen"; 7.1 „nicht zu den Überlebenden". Kein Ergebnis.

**Kette:** Marken: 16.4 (l); 16.4 (j).

### 47.4 R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4…

> **R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4; Prüfung vor dem Tag).** Der Faktor 0 in (i) ist der Multiplikator jedes Bots auf Schatten. Wohin sein Budgetanteil geht, hängt an der Herkunft der Stufe: (1) Schatten durch Abstieg nach (d) — Quartalsprüfung, Out-of-Sample — zählt in der Teilung der Zelle mit Faktor 0; die übrigen Bots der Zelle teilen das Zellenbudget nach (i) ((j)). (2) Schatten aus jedem anderen Grund — nach (b) im Selektionslauf, nach 15.6 (c) unterbestimmt, nach 16.5/17.7 „Backtester nicht bestätigt", nach (e) Notbremse — behält den Anteil, den (i) ihm auf Grundbudget gäbe (Faktor 1 in der Summe der Faktoren der Zelle); dieser Anteil wird als statische Benchmark-Position seiner Anlage gehalten ((b), 7.1). Steigt ein Bot derselben Zelle auf Bestätigt, gilt (i) über alle Faktoren der Zelle einschliesslich dieses Anteils. Die Benchmark-Position einer ganz inaktiven Zelle nach (j) ist die Summe der Grundbudget-Anteile ihrer Bots. Die Eingabe des Leiter-Skripts ist je Bot die Stufe und, bei Schatten, ob die Stufe aus (d) stammt; die Herkunft steht im Journal ((b): Ergebnis des eingefrorenen Skripts; (d): Quartalsprüfung; (e): protokolliert nach 22.4). Die Prüfung vor dem Tag in 16.4 zählt jede mögliche Eingabe auf — vier Zustände je Bot, 4⁹ = 262 144 —, nicht nur die 3⁹ Stufentabellen; sie verlangt für jede Eingabe einen eindeutigen Multiplikatorvektor und eindeutige Benchmark-Anteile je Anlage, ohne Eingabe des Betreibers.
> *Quelle des Grundes:* 7.1 „nicht zu den Überlebenden" (Betreiber-Festlegung, Sperrlistenpunkt 5) und (b) für den Ausfall im Lauf; (j) „die übrigen teilen es nach (i)" für den Abstieg; das Prinzip: Out-of-Sample-Evidenz über einen Bot bewegt Kapital zwischen Bots, ein In-Sample-Ausfall nicht (22.4). Beide Sätze stehen; keiner wird gestrichen. Kein Ergebnis.

**Kette:** Marken: 7.1; 16.4 (b); 16.4 (i); 16.4 (j).

### 47.5 R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt" vor Netting; L5)

> **R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt" vor Netting; L5).** Der Faktor 2 in (i) gilt ab der ersten Quartalsprüfung, die einen Bot nach (c) auf Bestätigt setzt. „Rang-5-Gewichtung, sobald Netting existiert" in (a) betrifft die Gewichtung im Netting, nicht den Stufenfaktor.
> *Quelle des Grundes:* Das Register bedingt in (l) ausdrücklich auf Netting und in (i) nicht; ein Faktor 1 bis Netting machte (c) wirkungslos. Kein Ergebnis.

**Kette:** Marken: 16.4 (a); 16.4 (i).

### 47.6 R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3)

> **R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3).** Der Budgetanteil eines Bots auf Schatten ist ein Budget (R21). Die statische Benchmark-Position darin ist in Höhe seines mittleren Exposures: der mittleren Exposure des Plateau-Gewinners über die Selektionsfalten, wie Abschnitt 7 (c) und der Bericht nach Abschnitt 8 sie führen. Der übrige Teil des Budgets ist nicht Kasse im Sinn von 7.1, sondern der nicht investierte Teil des Budgets, wie ihn der Bot selbst mit derselben mittleren Exposure hielte; 7.1 verbietet, das Budget aus dem Buch zu ziehen oder den Überlebenden zu geben. Das Leiter-Skript gibt Budgets aus (Multiplikatoren je Bot, Benchmark-Anteile je Anlage); die Höhe der Position ist nachgelagert und kein Parameter der Prüfung vor dem Tag.
> *Quelle des Grundes:* 4.2 (Benchmark als statische Position in Höhe der mittleren Exposure), 7 (c) (mittlere Exposure des Gewinners), 7.1. Kein Ergebnis.

**Kette:** Marken: 7.1; 15.6 (c); 16.4 (b).

### 47.7 R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5)

> **R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5).** Unter R18–R20 trägt in der Stufentabelle „alle Grundbudget" ein Bot, der allein in seiner Zelle steht, zwei Fünftel des Buchs (TB-116: `volatility_breakout` 3,6-fach seiner heutigen Grösse; die drei Umkehr-Aktien-Bots je 1,2; die Krypto-Bots 0,45 und 0,3 — Budgetanteile aus aufgezählten Tabellen). Das ist eine Folge des Registertexts, keine Lesart und kein Fehler: (h) macht die Zelle zur Einheit der Teilung, (g) nennt die Besetzung. Eine Teilung nach Zahl der Bots je Zelle liesse Bots Zellen bewegen. Ein Deckel je Bot gehört nach 4.3 in das Netting (Rang 5), das nicht existiert; ein Deckel vor Netting wäre ein neuer, als willkürlich gekennzeichneter Registertext des Betreibers (Rest in die Benchmark-Position der Anlage), dessen Quelle des Grundes der Risikoappetit ist, nie die Zahl. Entscheidungsvorlage: (a) so lassen — Empfehlung des Verfahrensprüfers; (b) Deckel je Bot vor Netting — Betreiber.
> *Quelle des Grundes:* (h) „die einzige Aufteilung, die kein Ergebnis verwendet", das Prinzip, 4.3. Kein Ergebnis.

**Kette:** Marken: 16.4 (h); 16.4 (g). Entscheid: 50.6.

### 47.8 R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1)

> **R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1).** Die Herkunftsprüfung nach R14 ist Teil des Datenvertrags von `auswertung.py` unter dem Selektionsmodus: jede der fünf Bedingungen endet mit 2. Ohne Modus ist `herkunft.json` keine Pflichteingabe; sie wird gelesen, wenn vorhanden, für die ausgewerteten Bots, im Kopf des Berichts angezeigt, und ihr Fehlen oder Abweichen ist kein Abbruch. Grund: Ein Lauf dieses Registers ist ein Lauf unter dem Modus (5e/19, 42.2 E5); ohne Modus läuft `auswertung.py` gegen Beispieldaten mit erfundenen Werten (12), und eine Herkunft, die zu bezeugen wäre, gibt es dort nicht. Die übrigen Vertragsbrüche (43-1, 42.3 F1) bleiben unabhängig vom Modus 2: Ohne sie kann nicht gerechnet werden; ohne `herkunft.json` kann nicht bezeugt werden. Der Docstring, der `herkunft.json` als Teil des Vertrags nennt, trägt den Zusatz „unter dem Modus" [Voraussetzung, zu messen: ob seit TB-117 Block D vorhanden]; wenn nicht, Nachtrag mit der nächsten planmässigen Öffnung von `auswertung.py`, keine eigene.
> *Quelle des Grundes:* 12, 5e/19, 42.2 E5, R10 (dieselbe Bauart), 25c (1). Kein Ergebnis.

**Kette:** Marken: Abschnitt 12; 46.5, Block R14; 46.9. Voraussetzung gemessen: 50.1.

### 47.9 R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; --bot; T117-2)

> **R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; `--bot`; T117-2).** Unter dem Modus prüft `auswertung.py` die `herkunft.json` aller neun Bots, auch wenn nur ein Bot ausgewertet wird; ohne Modus nur die der ausgewerteten. Ein Lauf mit `--bot` unter dem Modus wertet nicht alle neun aus und ist kein Bericht dieses Registers (12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun). Der Bericht des Tages ist der Lauf ohne `--bot`. Der Laufwrapper (35.4) startet `auswertung.py` unter dem Modus nur ohne `--bot`; `auswertung.py` selbst wird dafür nicht geöffnet. [Voraussetzung, zu messen: dass `--bot` unter dem Modus heute bis zum Bericht durchläuft; TB-117 J-7 hat den Modus im Prozess nachgestellt.]
> *Quelle des Grundes:* 12, 14, R14 „für jeden Bot", 21b (3) (Prüfungen wandern dorthin, wo geändert werden darf). Kein Ergebnis.

> ⭐ **47.9 R26 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: Abschnitt 12; 35.4; 46.5, Block R14. Voraussetzung gemessen: 50.1.

### 47.10 R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3)

> **R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3).** Bedingung 5 (die neun `herkunft.json` untereinander gleich) bleibt; neben 2–4 ist sie redundant, ausser beim Commit, der nach 19 als Präfix eines 7–40-stelligen `TB_SELEKTIONSCOMMIT` verglichen wird. Tag-Vorbedingung: Am Tag ist `TB_SELEKTIONSCOMMIT` der volle Hash des Tag-Commits (40 Zeichen); der Tag referenziert seinen Hash (17.2), und ein Präfix ist nicht sein Hash. Bedingung 5 wird nicht gestrichen: Redundanz in einer Wache ist kein Grund aus der Struktur.
> *Quelle des Grundes:* 17.2, 19, Prüfprinzip C4. Kein Ergebnis.

**Kette:** Marken: 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile).

### 47.11 R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4)

> **R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4).** Der registrierte Datenstand `d9449faf…` steht in Register 18 (Quelle) und als Codekopie in `shared/snapshot.py::VERANKERTER_DATENSTAND` und `research/vorregistrierung/auswertung.py::REGISTRIERTER_DATENSTAND`. Das ist der Zustand aus 32.5 (c) — Literal mit Probe gegen den Registertext — und als benannter Zwischenstand zulässig, wenn jede Kopie ihre Probe hat; für `auswertung.py` ist es J-r (TB-117) [Voraussetzung, zu messen: ob `snapshot.py` eine Probe gegen Register 18 hat; wenn nein, Handwerk ohne Sperrlistennähe]. Zusammenlegung innerhalb des Laufbereichs mit 40.8 (h): die Konstante wandert nach `registerdaten.py`, `auswertung.py` liest sie von dort. `snapshot.py` bleibt ausserhalb des Laufbereichs und behält seine gebundene Kopie; ein Import zöge es hinein.
> *Quelle des Grundes:* 21j/37.5 (ein Wert, ein Ort), 32.5, 42.2 E5. Kein Ergebnis.

**Kette:** Marken: Abschnitt 18. Voraussetzung gemessen: 50.1.

### 47.12 R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (herkunft.py im Laufbereich; T117-5)

> **R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (`herkunft.py` im Laufbereich; T117-5).** Der Lauf-Typ „`auswertung.py` samt Laufwrapper" (E5) ist ein Lauf, kein Import. Der echte Modus-Lauf von `auswertung.py` lädt seit TB-117 Block D `research/vorregistrierung/herkunft.py`; `herkunft.py` gehört damit zum Laufbereich, vor dem Zellen-Erzeuger. Die Laufbereichsmessung misst den Lauf-Typ „auswertung" als echten Modus-Lauf (Beispieldaten mit `herkunft.json`, wie TB-117 E); eine Messung über `import auswertung` ist für diesen Lauf-Typ keine Messung nach E5. `ARBEITSBAUM_PFADE` wird nach R4 vor dem Tag nachgezogen — mit der Öffnung von `paths.py`, die der Zellen-Erzeuger braucht, spätestens vor der ersten Laufbereichsmessung, die als Tag-Messung gilt; `test_arbeitsbaum_laufbereich.py` zieht mit (Grundsatz 40). Bis dahin ist `herkunft.py` am committeten Stand über Sperrlistenpunkte 11/12 und das Abbild gebunden und am Tag über die Sonde im Laufwrapper (36.2 (b)); eine uncommittete Änderung hielte die Startprüfung nicht an, die Sonde wohl. R5 (a) gilt mit diesem Grund fort.
> *Quelle des Grundes:* 42.2 E5 (Vereinigung aller Lauf-Typen, gemessen als Lauf), R4 (Liste vor dem Tag nachgezogen, nie durch ihn), 25f A3 (keine Öffnung doppelt), Messung TB-117 E. Kein Ergebnis.

**Kette:** Marken: 42.2, Eintrag E5 (e); 44.1, Eintrag 44-6; 45.4, Block R4; 45.5, Block R5, Punkt (a).

### 47.13 R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6)

> **R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6).** Der Zellen-Erzeuger und `auswertung.py` laufen am Tag-Commit (`TB_SELEKTIONSCOMMIT` = HEAD, 19). Zwischen dem Schreiben der `herkunft.json` und der Auswertung ändert sich weder das Register noch eine Datei aus `EINGEFROREN`; sonst endet die Auswertung nach R14 mit 2, und das ist ein Befund, kein Fehler der Wache. Registereinträge zum Lauf kommen nach dem Bericht. Ein späterer Lauf von `auswertung.py` auf demselben Selektionsraum läuft am Tag-Commit, sonst 2; nach R6 ist er nur als registrierte Messbitte zulässig oder ein Versuch.
> *Quelle des Grundes:* 14 (Reihenfolge), 19 (Tag-Commit = HEAD), R14 (Register-Hash zur Laufzeit), 17.2, R6. Kein Ergebnis.

> ⭐ **47.13 R30 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: keine. Abschnitt 10: Indexzeile, keine Marke.

### 47.14 R31 — Tatsachennotizen 27c

> **R31 — Tatsachennotizen 27c.**
> (a) R8 (a) ist in TB-117 Block D berichtigt statt gestrichen; der neue Satz nennt den Ausgang 2 und die Quelle 44.1. Angenommen; „Streichung" in R8 (a) und R14 war Handwerk am Wortlaut.
> (b) `shared/test_sperrlistensonde.py` (8a, H7f) wurde in TB-117 Block C nach Grundsatz 40 nachgezogen, obwohl nur für Block B freigegeben; die alten Fassungen brechen genau dort. Angenommen. Regel: Eine Freigabe je Sperrlistendatei nennt deren Tests ausdrücklich mit.
> (c) Der TB-117-Auftrag nannte einen 0b-Wert für `auswertung.py`, den TB-116 nicht gemessen hatte; die Sitzung hat gegen das Abbild `5e5ad109…` gemessen. Regel des steuernden Chats (Zahlen aus früheren Ergebnissen nur mit Fundstelle) steht.
> (d) Zu 27.3: Die Registerkopie liegt in der Ablage seit TB-118 in vier Teilen mit festen Namen (`REGISTER_KOPIE_teil1–4.md`, Abschnitte 0–23 / 24–37 / 38–43 / 44–46, Commit `1e11457`, sha256 `18e39ee2…`, KOPIE) und `REGISTER_INDEX.md`; der Verfahrensprüfer hat am 29.09.2026 alle vier vollständig gelesen (je ein Suchtreffer, Abschnitt 0 dieser Antwort).
> (e) `FABLE_ANTWORT_2026-09-26a_…` liegt nicht in der Ablage (Übergabe 29.09. sagt das Gegenteil); ihr Registertext steht zeichengleich in 45.
> *Quelle des Grundes:* ERGEBNIS_TB-117, Übergabe 29.09., `project_info` 29.09.2026. Kein Ergebnis.

**Kette:** Marken: 27.3 (im Zitatblock 27.1 bis 27.5).

### 47.15 R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026)

> **R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026).** Der Chat des Verfahrensprüfers wurde am 29.09.2026 neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand ist: der Wortlaut von `FABLE_UEBERGABE_2026-09-29_neuer_chat.md`; `REGISTER_INDEX.md` und `REGISTER_KOPIE_teil1–4.md` (Register 0–46, Commit `1e11457`, sha256 `18e39ee2…`, vollständig gelesen); aus der Ablage gelesen: `FABLE_ANFRAGE_2026-09-27c_…`, `ERGEBNIS_TB-116_leiter_lesarten.md`, `ERGEBNIS_TB-117_wachen_vor_dem_tag.md`, `FABLE_ANTWORT_2026-09-27a_…`, `FABLE_ANTWORT_2026-09-27b_…`, `UEBERGABE.md` (Stand 29.09.2026, 07:15), die Dateiliste der Ablage (43 Dokumente); als Suchausschnitt gesehen, nicht geöffnet: `BACKLOG_ENTSCHEIDUNGEN.md` (Einträge F2, Q1, E2) und `FABLE_UEBERGABE_2026-09-24_neuer_chat.md` (Abschnitt 2). Darin enthaltene Grössen, die an 27.1 grenzen: die Verfahrensgrössen des Registers (23.4, 24.6, 25.4, 32.2), gemessen nach vorher geschriebener Regel (27.2); die Budgetanteile und Multiplikatoren aus TB-116 (aufgezählte Stufentabellen, keine Kennzahl eines Parametersatzes). `BACKLOG.md`, `BACKLOG_ENTSCHEIDUNGEN.md`, `FABLE_ANTWORT_2026-09-25f_…`, `docs/belege/`, `ergebnisse/` und Trade-Listen: nicht gelesen. Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.
> *Quelle des Grundes:* 27, Tatsachennotiz zum Anfangsbestand (Bauart 21.09.); Übergabe 29.09. Kein Ergebnis.

**Kette:** Marken: Abschnitt 27.

## 48. Fable 29b — Registerblock R33–R52 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md`, md5 `898d5bd53b6617209b7ce4f7e8992941`, 73 703 B, am Commit `0f56aeb`, Abschnitt „Registerblock … (ab R33)“, Z. 190–267. Übertragen wie 27c (47). Die Marken für Register 0–12 setzt dieser Abschnitt nach R51 (48.19); darunter steht **eine Marke in Abschnitt 9** (R48 (b)), die R51 ausdrücklich verlangt. Der Verweis aus R8 (d) in Register 9 (45.8) ist ein anderer und kommt weiter nach dem Tag; die Sätze „in 9 steht … keine Marke“ in 45.8 und 46.0 (und die Listen in 45.10, 46.10) beschreiben den damaligen Stand, ihr einziger Grund war dieser Verweis. Für R48, R49 und R50 stehen Marken an allen Orten, die der Unterpunkt nennt, und an denen der R51-Liste (Vereinigung). Für Abschnitt 10 und den vollen Datenstand-Hash (17.3, 17.9, 18) verlangt R51 Indexzeilen statt Marken.

### 48.1 R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv)

> R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv). „zellen.csv enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen“ lies: „zellen.csv enthält für jede Zelle des Rasters und jede Falte des Faltenplans des Bots — Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile; die Zeilenzahl je Bot ist Zellen × (Selektionsfalten + 1). Eine (Zelle, Falte) ohne Trades trägt die Nullzeile: Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0, nie nichts.“ Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang. Es gibt keine Trade-Liste je Zelle als Rohergebnis; „leere Trade-Liste“ in 45.5 (b) und 43-7 bezeichnet den Fall „keine Trades gefunden“, dessen Ergebnis beim Listen-Erzeuger eine leere Liste und beim Zellen-Erzeuger die Nullzeile ist. F-1, F-2.
> Quelle des Grundes: Datenvertrag von auswertung.py (Sperrlistenpunkte 3/5/14; „genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des Faltenplans, Bestaetigungsperiode eingeschlossen“), 15.3 (1c: Falten-Sharpe je Falte), 43-7. Der Vertrag stand vor R5 (b); R5 (b) war Kurzform ohne Nachlesen — elfter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. Kein Ergebnis.

> ⭐ **48.1 R33 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.1 R33 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (c), vom steuernden Chat nach R65 (a) bestimmt, TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.1 R33 ERGÄNZT durch R82 (55.5)** (Fable 07a R82, Unterpunkt (a), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 45.5, Block R5, Punkt (b). Voraussetzung gemessen: 50.1.

### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)

> R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht). Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv mit genau einer Zeile je Zelle und den Feldern: die drei Werte aus 22.2 (Ertragsanteil der besten Selektionsfalte, des besten Symbols, der fünf besten Trades), haltedauer_median_handelstage (15.3 (b), R41) und bestaetigung_ab_effektiv (R37). Grundlage der drei Anteile: realisierte Erträge der ausgeführten Trades (Summe pnl_pct), Faltenzuordnung nach dem Einstiegstag (2b), nur Selektionsfalten; Anteil = Beitrag ÷ Gesamtertrag; bei Gesamtertrag ≤ 0 wird kein Anteil gebildet, das Feld trägt „nicht definiert“. auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie (22.2: Bericht, kein Tor; N unverändert); es rechnet die Werte nicht. Die Feldliste von zellenbericht.csv ist Registertext (R39). F-3, F-4, F-6.
> Quelle des Grundes: 22.2 (Werte des Laufs für den Gewinner), 12 (auswertung.py hat keinen Schalter und liest Rohergebnisse), Punkt 14 (Reihenfolge Selektion → Bestätigung → Bericht), 2b. Kein Ergebnis.

> ⭐ **48.2 R34 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (g), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.2 R34 ERGÄNZT durch R82 (55.5)** (Fable 07a R82, Unterpunkt (b), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 22.2; 45.5.

### 48.3 R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz

> R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz. 15.3 (a)/(b) regeln die Bauart eines Bootstrap-Intervalls; sie verlangen keines. Abschnitt 8 (Sperrlistenpunkt 13) führt keine Bootstrap-Zeile; der Lauf rechnet kein Intervall. Angewandt wird 15.3 auf die Messbitte R7 Nr. 6 (Block-Bootstrap-Band je Gewinnerzelle, nach dem Tag), gerechnet auf tagesreihen/<zelle>.csv mit L nach 15.3 (b) aus haltedauer_median_handelstage in zellenbericht.csv (R34). Tatsachennotiz: „im Auswertungsskript“ (15.3 (a)) trifft heute keinen Code (0 Treffer bootstrap, TB-120). F-4.
> Quelle des Grundes: 8 (abschliessende Berichtsliste), 15.3 im Wortlaut („jedes … wird … gerechnet“), R6/R7. Kein Ergebnis.

**Kette:** Marken: 15.3.

### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt)

> R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt). zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2). Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet. auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2. Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals. Festlegung 3 und Abschnitt 8 („drei tiefste Falten-Drawdowns“, „Kapital-Drawdown je Falte“) beziehen sich auf kapital_drawdown_mtm_pct; der ereignisindizierte Wert steht daneben als eigene Zeile. Vollzieht K4j (1) und (2); (3) folgt mit 40.8 (h). F-5, M49, M62.
> Quelle des Grundes: 24.2, 24 (Festlegung 1 präzisiert), 24.6 (Bauart der Faltenmessung), 29.3, 2a, 24b A2 (ein Wert, der nachgerechnet werden kann, tut nicht, als wäre er gemessen), 12. Kein Ergebnis.

> ⭐ **48.4 R36 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (c) und (d), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 24.2; 45.5. Voraussetzung gemessen: 50.1.

### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name)

> R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name). Der Begriff „Bestätigungsperiode“ bezeichnet zwei Zeiträume. (i) Die Bestätigungsperiode des Selektionslaufs ist die Spanne nach 35.1 (Beginn „Bestätigung ab“, 21.4; Ende Go-Live-Schnitt, ausschliesslich; registrierter Bestand 2026-01-01/2026-09-01), gerechnet auf dem Snapshot; sie wächst nicht (5c: ein zweiter Snapshot ist ein neuer Lauf). Die Bedingung aus 16.6 gilt an ihrem Beginn: Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3). (ii) Die Bestätigungsperiode der Leiter (16.4 (c)/(d)) ist der Papierpfad ab Go-Live; sie wächst; 5.1 Nr. 7 („wächst jeden Monat“), 15.4 2d („Go-Live-Tag plus Embargo“) und der Wortlaut von 16.6 („nach Go-Live“, „im Journal vermerkt“) beschreiben sie; dort gilt dieselbe Bedingung mit der Grenze Go-Live und den Positionsdaten des Papierpfads als Quelle. „Alle Falten“ in Abbruchkriterium (b) sind die Selektionsfalten (4.1); die Bestätigungsperiode ist keine Falte im Sinn von 4a (35.1) und wird ausgewertet, nachdem die Auswahl steht (5.1 Nr. 7). F-6, W39, M53.
> Quelle des Grundes: 15.1 (Out-of-Sample des Laufs ist allein die Bestätigungsperiode des gewählten Satzes), 5.2 (Forward-Test geht in keine Selektion ein, auch nicht in die Bestätigungsperiode), 35.1, 4.1, 16.4. Kein Ergebnis.

> ⭐ **48.5 R37 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.5 R37 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (a), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 5.1, Nr. 7; 16.4 (c); 16.4 (d); 16.6; 35.1.

### 48.6 R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen)

> R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen). Die Faltenkohärenz (Spearman-Rangkorrelation der Zellen-Rangfolge einer Falte gegen die Rangfolge nach dem Median der übrigen Selektionsfalten) rechnet auswertung.py aus zellen.csv, je Bot und Falte; sie braucht alle Zellen und existiert nur dort. Symbolzahl, Anteil am Universum und die Liste der ausgelassenen Symbole mit Grund schreibt der Zellen-Erzeuger je Bot und Falte in symbole_je_falte.csv aus dem Ladeprotokoll (42.1 D3/D7); auswertung.py berichtet sie. 16.11 Zeile 7 wird damit geschlossen. F-7.
> Quelle des Grundes: 16.7 (d) im Wortlaut („nach dem Lauf die Faltenkohärenz“), 5e. Kein Ergebnis.

**Kette:** Marken: 16.7 (d).

### 48.7 R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als…

> R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als Registertext). Ausgaben des Zellen-Erzeugers je Bot: zellen.csv (R33, R36), tagesreihen/<zelle>.csv, benchmark_tagesreihen/<bot>.csv, zellenbericht.csv (R34), symbole_je_falte.csv (R38), herkunft.json mit teile (37.4) und dem gerechneten Datenstand-Hash (46.7 (b)), Lese-Audit (5e). Die Benchmark-Tagesreihe ist je Bot, nicht je Markt (23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot); „benchmark_tagesreihen/<markt>.csv“ im Vertrag lies „<bot>.csv“. Sie wird über benchmark.py::bh_tagesrenditen (Sperrlistenpunkt 6, unverändert) gerechnet — derselbe Code wie für die Benchmark-Tabelle, kein zweiter Rechenweg. Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12) und wird im Registerauftrag E-2 aus dem Docstring von auswertung.py gemessen eingetragen, nicht abgeschrieben. F-8, A68.
> Quelle des Grundes: 23.3, 16.7 (b), 37.5 (2) (ein Wert, ein Ort), 33.3, 41.1 A12, 5e. Kein Ergebnis.

> ⭐ **48.7 R39 ERGÄNZT durch R67 (53.2)** (Fable 02c R67, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.7 R39 ERGÄNZT durch R69 (53.4): R39 ist bestätigt** (Fable 02c R69, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.7 R39 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (b), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 46.3. Feldliste: 50.2.

### 48.8 R40 — Ersteintrag — Schreibregel für Ausgaben der Erzeuger

> R40 — Registertext, Ersteintrag — Schreibregel für Ausgaben der Erzeuger. Die Ausgaben des Listen-Erzeugers und des Zellen-Erzeugers unterliegen 36.1 (2) und (3): --ziel ist Pflicht, die Voreinstellung ist nie ein Pfad, an dem etwas liegt; existiert eine Zieldatei, endet der Erzeuger mit 1 und schreibt nichts, auch nicht bei gleichem Inhalt. Ein zweiter Lauf schreibt an ein neues Ziel und ist als zweiter Lauf im Lese-Audit und im Protokoll (10.1) sichtbar. Die Hashes aller Ausgaben stehen im Bericht. F-9.
> Quelle des Grundes: 36.1 (1) deckt Ergebnisse nicht („für sie bestimmt“); 10.1 („Wer Vorher und Nachher vergleicht, hat wieder eine Wahl“ — ein überschriebenes Ergebnis macht den Vergleich unmöglich und unsichtbar zugleich), 5e, Prüfprinzip D6. Kein Ergebnis.

**Kette:** Marken: keine.

### 48.9 R41 — Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken)

> R41 — Registertext, Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken). haltedauer_balken ist die Zahl der Kerzen des Zeitrahmens des Bots von der Einstiegskerze bis zur Ausstiegskerze, beide eingeschlossen — die Zählregel, die positionen_holen.py heute anwendet (TB-120 C1). Einheit: Kerzen des Zeitrahmens (1d, 4h, 1h). Umrechnung in Handelstage für den Deckel (16.6) und für L (15.3 (b)): 1d-Bots Balken = Tage (Krypto: Kalendertage, 15.4 Anmerkung 1); 4h-Bots Balken ÷ 6, 1h-Bots Balken ÷ 24, aufgerundet (15.4 Anmerkung 4). Die Donchian-Untergrenze (41.2 B3, median_balken) nutzt dieselbe Einheit. [Voraussetzung, zu messen: ob TB-24 die Haltedauer in 15.4 (t3_supertrend 11,21 Tage) als Kerzenzahl oder als Zeitstempeldifferenz gebildet hat; bei Abweichung trägt die Neurechnung nach 41.3 C2 diese Zählregel, und 15.4 erhält eine Tatsachennotiz.] F-10.
> Quelle des Grundes: 15.4 Anmerkungen 1 und 4, 41.2 B3/B6/B7, 41.3 C2. Kein Ergebnis.

**Kette:** Marken: 15.3 (b); 15.4; 41.2, Eintrag B6/B7. Voraussetzung gemessen: 50.1.

### 48.10 R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen)

> R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen). Die neun neu erzeugten Trade-Listen werden als neuer Punkt 15 in Abschnitt 10 aufgenommen (Pfad, je Liste Hash; Fortschreibung des Listentexts vor dem Tag, neues Abbild nach 37.3) und stehen zugleich in herkunft.py::EINGEFROREN und der Gruppe eingefroren des Abbilds (R3, R12). Der Punkt ist die Regel, die Gruppe ihre Umsetzung; R3 erfüllt 40.6 nicht, weil ein Abbild den Registertext nicht ersetzt (30.2 (2)). Dass ein Pfad in einem Punkt und in eingefroren steht, gilt heute schon für faltenplan.py, benchmark.py und auswertung.py. F-11.
> Quelle des Grundes: 40.6 („als Punkt auf die Sperrliste“), 30.2 (2), 36.6, 37.3. Kein Ergebnis.

**Kette:** Marken: 40.6; 45.3; 46.3. Abschnitt 10: Indexzeile, keine Marke.

### 48.11 R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2

> R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2. Der Zellen-Erzeuger rechnet jede Zelle über den Signalpfad (collect_all_trades mit den Achsenwerten) und die Zuteilung (simulate_portfolio → shared/zuteilung.py::simuliere_portfolio, Punkt 10); evaluate_combination_multi der neun Optimierer bleibt ausserhalb des Laufs und wird nicht zum Zellen-Kern umgebaut (es verwirft Zellen und kennt keine Falten; 43-7). Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (29.4, 34.5) steht im Zellen-Erzeuger — an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5 —, nicht in den neun multi_symbol_optimise.py; „in allen neun multi_symbol_optimise.py“ lies „im Zellen-Erzeuger, für alle neun Bots“; die neun Optimierer erhalten eine Tatsachennotiz „nicht im Laufpfad“. Tatsachennotiz zu 11.2: Die Voraussetzung „evaluate_combination_multi liefert den Kapital-Drawdown“ wird für den Lauf gegenstandslos; den Kapital-Drawdown liefert der Zellen-Kern (R36); Agent 2 ist Regelbetrieb. Posten 5 des Plans ist neu zu fassen (Handwerk). F-12, M60.
> Quelle des Grundes: 43-7 (null Trades ist ein Wert; ein Kern, der Zellen verwirft, rechnet ein anderes Raster), Prüfprinzip A8 (eine Wache ist, was ausgeführt wird), 29.3, 34.5 (Reichweite: alle neun Bots — sie bleibt), Punkt 11 (Optimierer nicht ohne Not öffnen). Kein Ergebnis.

> ⭐ **48.11 R43 ERGÄNZT durch R81 (55.4)** (Fable 07a R81, Unterpunkte (b) und (g), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 11.2; 29.4; 34.5.

### 48.12 R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung)

> R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung). Die neun Listen werden nach der letzten Änderung am Signalpfad erzeugt — nach TB-30b Posten 3 (Durchreichung der Achsen) und Posten 4 (Horizont je Bot, 26.2/29) —, am Stand, den der Tag signiert. Eine Erzeugung vor einer dieser Änderungen ist Probe, kein Nachweis. Danach: Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (40.6), dann das Abbild des Faltenplans (40.8 (g)). F-13.
> Quelle des Grundes: 40.6 („mit dem registrierten Code“), 37.3 (das letzte Abbild trägt die Hashes des Tag-Commits), 40.8 (g). Kein Ergebnis.

**Kette:** Marken: 40.6.

### 48.13 R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen)

> R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen). shared/zuteilung.py::simuliere_portfolio gibt zusätzlich die ausgeführten Positionen (Symbol, Einstiegs- und Ausstiegszeit, Grösse, Preise) heraus — additiv, als weiteres Feld oder weiteren Rückgabewert; Zuteilungsreihenfolge, SEED und Rechnung unverändert; kein Feld, das der Laufcode liest, wird beschrieben (A9). Beauftragte Änderung nach 37.3 mit Nachweis in der Bauart von 10.1: Trade-Listen und equity_curve aller neun Bots bytegleich vor und nach der Änderung; Mutationsprobe: Rückgabe entfernt ⇒ Zellen-Erzeuger endet mit 2; Hash-Übergang Punkt 10, neues Abbild. Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen. F-14.
> Quelle des Grundes: 24.2/1a (die MtM-Reihe braucht die Positionen), 37.3, 10.1 („bitidentisch“), 41.1 A9, 37.5 (2) (ein Wert, ein Ort). Kein Ergebnis.

**Kette:** Marken: keine. Abschnitt 10: Indexzeile, keine Marke.

### 48.14 R46 — Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag

> R46 — Registertext, Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag. Vor dem signierten Tag läuft der Zellen-Erzeuger nicht auf dem registrierten Snapshot mit dem registrierten Raster. Abgenommen wird er im Selektionsmodus gegen einen Test-Snapshot aus synthetischen Kursdaten (mit snapshot.py gezogen, eigener Hash, als Probe benannt; kein Lauf dieses Registers nach 5c/5e), durch die ganze Kette bis auswertung.py und Bericht (der Kettenlauf aus 25f A3 (1); Glied 2 aus 46.8 R17 (d)). Geprüft werden Struktur und Verfahren: Zeilenzahl nach R33, Nullzeile, Feldlisten nach R39, Lese-Audit, Ausgänge nach 36.5, Schreibregel R40, Nachrechnung R36 — nie eine Zahl des Selektionsraums. Der Hash des Test-Snapshots steht in der Tatsachennotiz der Abnahme. F-15.
> Quelle des Grundes: 27.1, 24.3 (die Regel steht vor der Messung), 23e und 41.3 C6 (der Nachweis geht denselben Weg wie der Lauf; ein Hilfsordner ist kein Modus-Lauf), 5c, Prüfprinzip A8. Kein Ergebnis.

> ⭐ **48.14 R46 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (d) und (f), vom steuernden Chat nach R65 (a) bestimmt, TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.14 R46 ERGÄNZT durch R78 (55.1) und R81 (55.4)** (Fable 07a R78, Unterpunkt (e), und R81, Unterpunkt (h), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: keine.

### 48.15 R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“)

> R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“). Parameterdateien eines Bots sind die Module, aus denen sein Signalpfad zur Laufzeit Handelsparameter bezieht — gemessen am Import-Audit des Modus-Laufs des Listen-Erzeugers (Lauf-Typ nach 42.2 E5), nicht per Namensliste; heute mindestens live_params.py und backtest_*.py je Bot. Nach TB-30b Posten 3 ist SMA_TREND_PERIOD Rasterachse, keine Parameterdatei mehr. Die Tatsachennotiz zu 5.4 nennt je Bot die Liste mit Hash und Commit. F-17.
> Quelle des Grundes: 40.6, 5e (der Lauf belegt, woraus er gelesen hat), 37.5 (2). Kein Ergebnis.

**Kette:** Marken: 40.6.

### 48.16 R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle

> R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle.
> (a) Festlegung 4 trägt im Wortlaut kein Exposure-Argument; die registrierte Lesart ist 4.2 (12, Lesart 1). Marke an Festlegung 4 (R51). W42.
> (b) Abschnitt 9: N je Bot ist N_historisch(Bot) + Zellen(Bot) (Tabelle in 3: N nominal = Zellen + N historisch je Zeile, Summe 3 069); „N = 653 plus die Zellen dieses Laufs, je Bot getrennt“ ist die Kurzform. M47.
> (c) Abschnitt 7 (d): Ist der Gewinner eine Spitze und erfüllt der beste Nicht-Spitzen-Punkt (a) nicht, ist (d) nicht erfüllt; der Bot bleibt mit dem Plateau-Gewinner, die Spitze ist Markierung (6, 8); (d) tauscht den Gewinner nie aus (22.5). [Voraussetzung, zu messen: die von auswertung.py in diesem Fall ausgegebene Zelle; Abweichung ist ein Register-Code-Widerspruch nach 25c (1).] M48.
> (d) Exposure: DD_Toleranz(e) und DD_Benchmark(f, e) werden mit der mittleren Exposure des Parametersatzes in der jeweiligen Falte ausgewertet (4.2). Die mittlere Exposure der Kapitalregel (7.1, 7 (c), 16.4 (b), 15.6 (c)) ist die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“). Mittlere Exposure = Mittel über die Handelstage des Zeitraums (Krypto Kalendertage, 15.4 Anmerkung 1) des Anteils des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a). [Voraussetzung, zu messen: Bildung von mittlere_exposure im Vertrag/auswertung.py und in mtm_kern.py; der Registertext folgt dem Code, wo er ihn hat.] M50, M54, A69.
> (e) Benchmark: Gewichte täglich gleich (23.3, 23.5), Höhe statisch in der mittleren Exposure (4.2, 7 (c)); „statische Position“ meint die Höhe, „point-in-time“ die Menge (23.7). M51.
> (f) Kante (2.5): jeder Gewinner, der auf mindestens einer Achse auf der ersten oder letzten Stufe liegt, Zusatzstufen („kein“, „structural“) und die Obergrenze des Positionslimits eingeschlossen; die Markierung sagt, wo der Gewinner liegt, nicht, ob erweitert würde. [Voraussetzung, zu messen: auswertung.py markierungen.] M52.
> (g) Zufalls-Timing (8.1): über die aneinandergehängten Selektionsfalten (dieselben Tage wie 7 (c)); verglichen wird die Summe der täglichen Renditen (2a) der zyklisch verschobenen Exposure-Reihe auf den Benchmark-Tagesrenditen mit der Rendite des Satzes über dieselben Tage; das 95. Perzentil ist das empirische Perzentil über alle T − 1 Verschiebungen. [Voraussetzung, zu messen: Perzentilbildung im Code.] M56.
> (h) haltedauer (2.2) ist eine Messung aus gefundenen Trades (Grenzsatz „gemessene Median-Haltedauer“; 41.2 B3); „Hypothese“ im Kopf von 3 ist erzeugter Text und bleibt. Bei elliott_wave gilt „gefunden“ ohne Ausnahme (41.3 C4). M57, M58.
> (i) Die Ziffernregel aus 2.1 gilt für Grenzsätze; Spaltenköpfe der Messgrössentabelle („Median 20-Balken-Spanne“) sind keine Grenzsätze. [Voraussetzung: pruefe_grenzsaetze.py prüft die Satzfelder.] M61.
> (j) Festlegung 3 bei weniger als drei Selektionsfalten: Der Fall tritt nicht ein — 4b verlangt mindestens 3, sonst 4c (keine Selektion). A75.
> (k) Präzisierung zu 10.1: „Stichproben-Hash-Vergleich“ lies „Hash-Vergleich aller Ausgabedateien des Laufs nach dem Lese-Audit“; eine Stichprobe hätte eine Ziehung, also eine Wahl, und der Vollvergleich kostet nichts. A74.
> Quelle des Grundes: die genannten Fundstellen; 22.5; 24b A2; Prüfprinzip C4. Kein Ergebnis.

> ⭐ **48.16 R48 (g) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.16 R48 (d) ERGÄNZT durch R60 (51.5)** (Fable 01a R60, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.16 R48 (d) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.16 R48 (d) ERGÄNZT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 1, Tabelle, Zeile 4; 1, Tabelle, Zeile 3; 2.1; 2.2; 2.5; 7, Tabelle, Zeile (d); 8.1; 9, erster Absatz. Voraussetzung gemessen: 50.1. Abschnitt 10: Indexzeile, keine Marke.

### 48.17 R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort

> R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort.
> (a) Zu 2.2: Der erzeugte Abschnitt 3 verwendet ableitung an zwei Stellen (Obergrenze Positionslimit; bb_squeeze_percentile oben) und methode an drei (take_profit_fib; Stop-Zusatzstufe „kein“; bb_lookback unten); 2.2 nennt je ein Beispiel. Massgeblich ist der erzeugte Block (registerbericht.py --pruefen). W40.
> (b) Zu 2.7: Die Quantil-Achsen (rsi_threshold, adx_threshold) folgen einer dritten Stufungsart — Quantile der gemessenen Verteilung (Grenzsätze in 3) —, die 2.7 nicht nennt. Messbitte (Verfahrensmessung, 27.2), nur das Wie: die Funktion in registerdaten.py, die die Quantil-Stufen bildet, und ihre Eingabe aus messgroessen.json (Zeitraum, Zeitrahmen, Universum); Ergebnis als Tatsachennotiz zu 2.7. W41, A71.
> (c) Zu 3 und 4.4: Zahlenteil und Beispiel zeigen den Stand 14.09.2026 (benchmark_drawdowns.json, a163c498…); die Tabelle, die der Lauf liest, ist ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json (39.2, 64fb2912…); der ERZEUGT-Block wird mit 40.8 (h) neu erzeugt (43-6); die in 40.8 (b) verlangte Tatsachennotiz an 4.4 steht dort noch nicht. W43.
> (d) Zu 12: Die Zahl der Prüfungen ist Tatsachennotiz mit Stand; die jüngste Marke gilt (41.1 A1: 196, db50e187…; Mutationsproben H1–H7, H6 offen nach 41.1 A4). W44.
> (e) Zu 38.2: Die Regel gilt auch für Marken. Die Marke in 6 nennt registerdaten.py:605 ohne Commit; die Zeile ist über 42.3 F1 gedeckt („unverändert seit vor 4faef05“). Künftig nennen Marken Bezeichner, nicht Zeilen. W45.
> (f) Zum Kopf des Registers: „Stand: 14.09.2026“ ist der Stand der Erstfassung; das Register ist append-only, sein Stand ist der Commit im Kopf der Kopie (27.3) beziehungsweise HEAD. W46.
> (g) Zu Abschnitt 10, Tatsachennotiz vom 15.09.2026: „nach dem Lauf“ bezeichnet den nativen Neuaufbau der 72 Krypto-Kursdateien (TB-34, shared/kursdaten_neuaufbau.py), keinen Selektionslauf. M59.
> (h) Zu 11: „die beiden Bug-Fixes“ sind 11.1 und 11.2; 11.3 ist eine dritte Voraussetzung des Laufs (ohne Durchreichung ist das registrierte Raster nicht rechenbar; TB-30b Posten 3, E-1). Stand: 11.1 erfüllt (42.3 F3), 11.2 für den Lauf gegenstandslos (R43), 11.3 offen (E-1). M60.
> Quelle des Grundes: Messungen TB-120/TB-121, die genannten Fundstellen. Kein Ergebnis.

**Kette:** Marken: Kopf, Absatz „Stand: 14.09.2026“; 2.2; 2.7; 3, Zahlenteil (nach ENDE ERZEUGT); 4.4; Abschnitt 11; Abschnitt 12; 38.2. Voraussetzung gemessen: 50.1. Abschnitt 10: Indexzeile, keine Marke.

### 48.18 R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121

> R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121. Die Definitionen der Kennzahlen des Laufs — Falten-Sharpe (15.3), Calmar und Annualisierung, Alpha/Beta, DSR-Eingaben (Sharpe, T, Schiefe, Wölbung, Streuung), mittlere Exposure, Korrelationsmass und Operator der Clusterschwelle, Zellenname und Gleichstandsschlüssel, Ausstiegskonvention je Ausstiegsart, Interpolation an den Rändern (43-2) — sind im eingefrorenen Code registriert (Sperrliste 3, 5, 7, 9; Abschnitt-0-Menge), nicht im Text von 0–12. Vor dem Tag wird je Kennzahl eine Tatsachennotiz eingetragen: Datei und Bezeichner (38.2), und wo das Register eine Formel nennt (15.3; 7 „Calmar bei Drawdown 0 ist 0,0“; 4.2; 9), die gemessene Übereinstimmung; eine Abweichung ist ein Register-Code-Widerspruch (25c (1)) und wird gemeldet, nicht eingetragen. Der Registertext legt keine dieser Definitionen neu fest. Messbitte (27.2), nur das Ob: trägt registerdaten.py für jede der 34 Rastergrenzen einen Grenzsatz, und fasst registerbericht.py gleiche Sätze zusammen? (Der erzeugte Block führt für t3_slow_length, donchian_period oben und stop_mode unten/oben keinen eigenen Satz; 2.1 verlangt einen je Grenze.) Tatsachennotiz zu TB-121: 85 Befunde (B 19, V 19, W 8, M 16, A 15, Z 8), jedes Zitat maschinell geprüft; Vollständigkeitstest kalt: 3 von 12 Bausteinen aus 0–12 schreibbar; die Sitzung hatte Zusammenfassungen der Abschnitte 15–46 im Gedächtnis (Claude Code MEMORY.md), deshalb ist die Befundliste eine Untergrenze und „3 von 12“ eine Obergrenze; ihre Vollständigkeit ist nicht belegt. A63, A64, A65, A72, A76, M55, A73, Frage 78.
> Quelle des Grundes: 13 („Das Urteil ist Code“), 12, Sperrliste 3/5/7/9, 38.2, 25c (1), 2.1, Messung TB-121. Kein Ergebnis.

> ⭐ **48.18 R50 ERGÄNZT durch R81 (55.4) und R83 (55.6)** (Fable 07a R81, Unterpunkt (e), und R83, Unterpunkt (c), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: Abschnitt 12. Voraussetzung gemessen: 50.1.

### 48.19 R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich)

> R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich). Festlegung 4 → 4.2 (12, Lesart 1) [W42]. Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63]. 3, Zahlenteil und 4.4 → 39.2 (Tabelle des Laufs), 40.8 (h), R49 (c) [W43, A67]. 4.2 → 43-2 (Interpolation an den Rändern) [A70]. 5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66]. 9 → R48 (b) [M47]. 10, Tatsachennotiz 15.09. → R49 (g) [M59] — als Indexzeile, in Abschnitt 10 steht keine Marke. 11 → R49 (h) [M60]. 12 → R50. Kopf → R49 (f) [W46]. Datenstand-Hash voll: 17.3/17.9/18 — Indexzeile, keine Marke in 10 [A77].
> Quelle des Grundes: 34 (Marke am alten Ort), 27.3, REGISTER_INDEX. Kein Ergebnis.

> ⭐ **48.19 R51 PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 1, Tabelle, Zeile 2; 4.2; 5.3; 7, Tabelle, Zeile (a); 15.6. Abschnitt 10: Indexzeile, keine Marke.

### 48.20 R52 — Tatsachennotizen 29b

> R52 — Tatsachennotizen 29b. (a) 27b B3 („die datierten Kopien … sind im Repo committet“) war für vier von sechs Registerkopien falsch (TB-118 A3); zehnter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. (b) 45.5 (b) („für jede Zelle genau eine Zeile“) widersprach dem Datenvertrag; berichtigt in R33; elfter Fall. (c) Der Chat des Verfahrensprüfers ist zwischen 29a und 29b einmal verdichtet worden; die Registerteile 1–4, 27b und 25f wurden danach erneut vollständig gelesen; die Umzugsampel steht deshalb auf 🟡, Umzug nach E-2.
> Quelle des Grundes: Messungen TB-118, TB-120; Leseprotokoll 29b. Kein Ergebnis.

**Kette:** Marken: keine.

## 49. Fable 30a — Registerblock R53–R55 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md`, md5 `f9cdbbef543ec54ed07ee0566c336dde`, 12 925 B, am Commit `0f56aeb`, Z. 25–32. Die Datei ist eine Abschrift aus einem Text-Anhang ohne Markdown-Auszeichnung. Die drei Blöcke sind bytegleich mit Fables Ablage-Fassung (`FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md`, md5 `5e5401bcc6b5551a7a61a8a1b4331fee`), geprüft vom steuernden Chat am 30.09.2026 (R53 `cbaeea5b…`, R54 `914ddd1d…`, R55 `1f3e534b…`). R54 berichtigt 2a und R48 (g) (48.16); die Marken stehen an 15.4 und unter 48.16.

### 49.1 R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick

> R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick. Der Indikator-Vorlauf eines Bots nach 4a (i) ist der grösste Vorlauf über alle Zellen seines Rasters: je Rückblick-Achse die oberste registrierte Stufe (Abschnitt 3) zuzüglich der festen Fenster des Bots (etwa Bollinger-Fenster, Donchian-Zusatz), gerechnet gegen den Horizontbeginn (28.6). Er wird aus registerdaten.py gerechnet, nicht als Voreinstellung geführt und nicht als Literal gesetzt; der Faltenplan trägt ihn je Bot als Feld. Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf (TB-122 F1, Handwerk). Tatsachennotiz: Die Nachmessungen in 25.2 (rsi2_crypto, 150 Balken), 15.5 und 21.4 stammen aus der Zeit vor TB-30b Posten 3; die erste Falte ist nach dieser Präzisierung neu abzuleiten (Verfahrensmessung nach 27.2; Wirkung bekannt und kein Grund).
> Quelle des Grundes: 2.7 (ein Raster je Bot, identisch über alle Falten), 29.3 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte), 4a (i), 24.3 (Bauart). Kein Ergebnis.

> ⭐ **49.1 R53 PRÄZISIERT durch R57 (51.2)** (Fable 01a R57, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **49.1 R53 ERGÄNZT durch R59 (51.4)** (Fable 01a R59, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 15.5; 21.4; 25.2; 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile); 28.6. Voraussetzung gemessen: 50.1. Zählweise: 50.5.

### 49.2 R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen)

> R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen). „Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage“ lies „Die Falten-Rendite ist die verkettete Rendite dieser Tage, ∏(1 + r_t) − 1 über die täglichen Netto-Mark-to-Market-Renditen“. Renditen über mehrere Tage — je Falte, über die Selektionsfalten (7 (c)), im Zufalls-Timing (8.1), für die konstante Exposure — werden überall verkettet; Drawdowns stehen auf dem verketteten Kapitalpfad (24.2). In R48 (g) lies „die Summe der täglichen Renditen (2a)“ als „die verkettete Rendite (2a)“. Der Falten-Sharpe (15.3: Mittel und Standardabweichung der täglichen Renditen) und die Faltenzuordnung (2a, 2b) sind unberührt. kennzahlen.py (gesamtrendite_pct, Zufalls-Timing, cumprod) bleibt unverändert; es rechnet, was das Register nach dieser Berichtigung sagt. Kategorie: Berichtigung (Registertext an Registertext — Kapitalpfad und Drawdown waren schon verkettet).
> Quelle des Grundes: 29.3 (Startkapital, durchgehender Pfad), 2a zweiter Satz (Kapitalstand über die Faltengrenzen), 24.2, 7 (c) (Calmar gegen Calmar auf einer Rechenart), 13 (das Urteil ist Code). Kein Ergebnis.

**Kette:** Marken: 15.4 (a); 48.16 (R48), neu in TB-126. Voraussetzung gemessen: 50.1.

### 49.3 R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz

> R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz. Gibt es keinen zulässigen Nicht-Spitzen-Punkt, ist Abbruchkriterium (d) nicht erfüllt; der Bot bleibt mit dem Plateau-Gewinner (R48 (c)), markiert als Spitze, und der Bericht führt die Zeile „Spitze ohne zulässigen Nicht-Spitzen-Punkt“ — Bericht, kein Tor. Ist keine Zelle zulässig, greift (b); der beste Nicht-Spitzen-Punkt wird dann über alle Zellen bestimmt und berichtet, wie der Plateau-Gewinner in 7. Tatsachennotiz: Der Schlüssel d_spitze_ohne_tragfaehige_alternative in auswertung.py ist ein Name, keine Regel; Umbenennung mit der nächsten planmässigen Öffnung. Eine Prüfung für die leere Menge mit Gegenprobe (40.7) wird ergänzt (Handwerk); heute prüft kein Test den Fall.
> Quelle des Grundes: Wortlaut von 7 (d) und der Präzisierung (Und-Bedingung), 6 („Ist N(x) leer, ist x keine Spitze“), 12 Lesart 4 (kein undefinierter Fall), 22.5 (ein nicht registriertes Kriterium disqualifiziert nicht), 7.1, 22.1. Kein Ergebnis.

**Kette:** Marken: 7, Tabelle, Zeile (d). Voraussetzung gemessen: 50.1.

## 50. Tatsachennotizen zu E-2 (TB-126)

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 27c, 29b und 30a „zu messen“ nennt, dazu die Vollzugsnotizen TB-122 und TB-124 nach 37.3. Gemessen über die Geräteanbindung, nur lesend, am 29. und 30.09.2026 (`docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md` samt Nachträgen); die Sitzung TB-126 hat in Schritt 0 gemessen, dass die genannten Code-Dateien seither unverändert sind (`docs/belege/TB-126/0f_unveraendert.txt`). Zeilenangaben gelten am Commit `0f56aeb`. Kein Ergebnis gelesen (27.1). Eine Voraussetzung, deren Messung abweicht, steht hier mit dem Befund. Der Block steht trotzdem in 47–49, wo Fable den Abweichungsfall im Block selbst regelt oder beantwortet hat (R41: 30a, Teil 0; R48 (g): R54). Wo ein Befund eine Lesart des steuernden Chats braucht, steht das ausdrücklich da; sie geht mit der nächsten Anfrage an Fable (R48 (d), 50.5). Die Nummer hat der steuernde Chat vergeben, nicht Fable.

### 50.1 Voraussetzungen und Befunde

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R25 (47.8) | Docstring trägt „unter dem Modus“ seit TB-117 Block D | `research/vorregistrierung/auswertung.py:53–62` (nicht 51–52): „unter dem Selektionsmodus fuer JEDEN der neun Bots geprueft, sonst Abbruch mit 2“ | passt; Fundstelle berichtigt |
| R26 (47.9) | `--bot` läuft unter dem Modus bis zum Bericht (Fable nannte J-7) | Gemessen in TB-117 E (`docs/belege/TB-117/e_auswertung_modus.txt`, HEAD `852f253`, „modus_gut: rc 0“), nicht in J-7; `auswertung.py` seither unverändert (TB-126, 0f). Ein Laufwrapper nach 35.4 wurde nicht gefunden | passt in der Sache am Stand `852f253` (Fundstelle E statt J-7, von Fable bestätigt, 30a, Teil 0); an `0f56aeb` ohne Lauf nicht neu gemessen (50.7) |
| R28 (47.11) | Probe von `snapshot.py` gegen Register 18 | fehlte am 29.09.2026; gebaut in TB-124 D: `shared/test_verankerter_datenstand.py`, 3/3, Commit `7453469` (`docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Abschnitt 5, `docs/belege/TB-124/d_probe.txt`). Nebenbefund: ein weiteres Literal des Datenstands, `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`, ohne eigene Registerprobe; R28 nennt es nicht | erfüllt; Nebenbefund offen (50.7) |
| R33 (48.1) | der Vertrag führt die Trade-Zahl je (Zelle, Falte) | `n_trades`, `auswertung.py:39`, Pflichtspalte Z. 133 | passt |
| R36 (48.4) | MtM-Drawdown in der Falte, Basis Faltenbeginn | `research/mtm_drawdown/mtm_kern.py:296–304` (Basis: letzter Rastertag vor `von`), Raster Z. 135–139. Der Vertrag führt heute nur `kapital_drawdown_pct`; die zwei Spalten nach R36 kommen mit dem Zellen-Erzeuger | passt |
| R41 (48.9) | Haltedauer in 15.4: Kerzenzahl oder Zeitstempeldifferenz? | Zeitstempeldifferenz: `research/faltenplan_neun/embargo_neun.py:36–37, 236–238` | weicht ab ⇒ Abweichungsfall nach R41, von Fable bestätigt (30a, Teil 0); Marke an 15.4; Neurechnung nach 41.3 C2 offen (50.7) |
| R48 (c) (48.16) | die von `auswertung.py` im Fall Spitze ausgegebene Zelle | `auswertung.py:554–556`; ausgegeben wird immer der Plateau-Gewinner mit Markierung (Z. 710–719) | passt; den Randfall ohne zulässigen Nicht-Spitzen-Punkt regelt R55 (49.3) |
| R48 (d) (48.16) | Bildung von `mittlere_exposure` im Vertrag, in `auswertung.py` und in `mtm_kern.py` | nicht gebildet: `auswertung.py:405` liest sie als Eingabe; `mtm_kern.py` führt keine Exposure (nur `gebunden`, zum Einstand, Z. 186–188); `research/exposure_messung/exposure_kern.py` und `research/exposure_messung/auswertung.py:234` teilen `gebunden / kapital_start`, bewertet zum Einstand | An den drei Orten, die R48 (d) nennt, nicht gebildet; ausserhalb davon zum Einstand bewertet. **Lesart des steuernden Chats:** Wo der Code die Grösse nicht hat, gilt der Registertext (R48 (d): „der Registertext folgt dem Code, wo er ihn hat“). An Fable (50.7); offen bis zum Zellen-Erzeuger |
| R48 (f) (48.16) | Markierungen in `auswertung.py`: Kante einschliesslich der Zusatzstufen | Kante nach Position (`auswertung.py:466`); „kein“ ist immer die letzte Stufe, „structural“ wird nach Weite einsortiert (`research/vorregistrierung/registerdaten.py:574–583`) | passt nach Fables Lesart „eingeschlossen = zählt als Stufe mit“ (30a, Teil 0) |
| R48 (g) (48.16) | Perzentilbildung im Code | T − 1 Verschiebungen (`research/vorregistrierung/kennzahlen.py:197`), `np.percentile` (Z. 201); die Rendite wird verkettet (`np.prod`, Z. 199) | T − 1 und Perzentil passen; „Summe“ berichtigt durch R54 (49.2) |
| R48 (i) (48.16) | `pruefe_grenzsaetze.py` prüft die Satzfelder | `research/vorregistrierung/pruefe_grenzsaetze.py:100–148` | passt |
| R49 (b) (48.17) | eine Funktion in `registerdaten.py` bildet die Quantil-Stufen | gebildet in `research/vorregistrierung/messgroessen.py::je_zeitrahmen` (Z. 169–219); `registerdaten.py:558–565` (`achse_werte`) liest nur. Universum aus `config/sp500_top150.txt` und `config/top25_symbols.txt`; der Zeitraum steht nur in `datenbereiche`, nicht in einem eigenen Feld | gemessen; der Ort weicht ab (nicht `registerdaten.py`) |
| R50 (48.18) | Grenzsatz je Rastergrenze; fasst `registerbericht.py` gleiche Sätze zusammen? | Jede Grenze trägt `satz` über `_grenze` (`registerdaten.py:270`); Dubletten werden zusammengefasst (`research/vorregistrierung/registerbericht.py:111–120`). Der Zellenname steht in `auswertung.py::zelle_id` (Z. 272–274), die Cluster in `kennzahlen.py::cluster_anzahl` | Ob: ja und ja; Orte teils anders als in R50; die Zahl „34“ nicht gemessen (50.7) |
| R53 (49.1) | oberste Stufe jeder Rückblick-Achse und feste Fenster je Bot maschinell aus `registerdaten.py` lesbar? | Stufen: `registerdaten.raster()` über `achse_werte`, die oberste ist der letzte Wert je Achse; Bollinger-Fenster: `regel_wert({"regel": "bollinger_fenster"}, …)` gibt 20.0 (Z. 213–216). Für weitere feste Fenster (`VOLUME_AVG_PERIOD`, fester Warm-up der Turtle-Soup-Bots) gibt es keinen Eintrag; `donchian_period` ist eine Rasterachse | teilweise. R53 sagt „nicht als Literal“; „Literal mit Test nach 32.5 (c)“ nennt Fable nur unter „Unsicher“ (30a) — Reibung, an Fable; entschieden wird mit R53 (a) (50.7). Zählweise: 50.5 |
| R54 (49.2) | liest und rechnet irgendein Code `netto_rendite_pct` aus dem Vertrag? | Pflichtspalte `auswertung.py:134`; gelesen nur für die Bestätigungsperiode (Z. 624), berichtet in Z. 823; `netto_rendite_pct_ueber_selektionsfalten` (Z. 675) kommt aus `bereinigung["strategie_rendite_pct"]`, nicht aus der Spalte | trifft zu: Berichtsgrösse ohne Leser im Urteil |
| R55 (49.3) | Nebenfall „keine Zelle zulässig“ | nicht gemessen; im Hauptfall rechnet der Code `None ⇒ False` | Hauptfall passt; Nebenfall erschlossen, Probe offen (50.7) |

> ⭐ **50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8** (Fable 01a R60, Unterpunkt (d), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.2 R39 (48.7) — Feldliste der Ausgaben, gemessen aus dem Docstring von `auswertung.py`

R39 verlangt, die Feldliste jeder Ausgabe des Zellen-Erzeugers als Registertext „aus dem Docstring von auswertung.py gemessen“ einzutragen, nicht abgeschrieben. Gemessen am Commit `0f56aeb`, `research/vorregistrierung/auswertung.py` Z. 36–67, zeichengleich:

```
DIE ROHERGEBNISSE - DER VERTRAG
------------------------------------------------------------------------------
    <wurzel>/<bot>/zellen.csv
        zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,
        netto_sharpe, netto_rendite_pct, kapital_drawdown_pct,
        mittlere_exposure
        -> genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des
           Faltenplans, Bestaetigungsperiode eingeschlossen.

    <wurzel>/<bot>/tagesreihen/<zelle_id>.csv
        datum, netto_rendite, exposure
        -> Tagesreihe ueber alle Falten. Verlangt wird sie fuer jede
           ZULAESSIGE Zelle; gelesen wird sie nur fuer die Zellen, die das
           Programm braucht (Gewinner, bester Nicht-Spitzen-Punkt).

    <wurzel>/<bot>/herkunft.json
        Commit-Hash, Datenstand-Hash, Register-Hash - siehe herkunft.py.
        -> TB-117 (Fable 27a R14, Register 46.5; Lesart 46.9): unter dem
           Selektionsmodus fuer JEDEN der neun Bots geprueft, sonst Abbruch
           mit 2 - Datei fehlt; Commit nicht der Tag-Commit
           (`TB_SELEKTIONSCOMMIT`, Praefix); Datenstand nicht der
           registrierte (Register 18); Register-Hash nicht
           `herkunft.register()` zur Laufzeit; die neun untereinander
           verschieden. Ohne Modus gelesen, wenn vorhanden, und im Kopf des
           Berichts angezeigt, ohne Abbruch (Beispieldaten und Tests tragen
           Nullwerte). Der Kopf des Berichts traegt Commit, Datenstand und
           Register-Hash in beiden Faellen.

    <wurzel>/benchmark_tagesreihen/<markt>.csv
        datum, netto_rendite
        -> das gleichgewichtete point-in-time-Universum, taeglich. Grundlage
           der Beta-Bereinigung und des Zufalls-Timing-Tests.
```

„`benchmark_tagesreihen/<markt>.csv`“ im Zitat lies „`<bot>.csv`“ (R39). Für `zellenbericht.csv` (R34), `symbole_je_falte.csv` (R38) und das Lese-Audit führt der Docstring heute keine Feldliste; sie kommt mit dem Zellen-Erzeuger (R46) und wird dann hier nachgetragen.

### 50.3 Vollzug TB-122 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` Z. 235–275 (Commit `0f56aeb`). Der „Stand 11.3“ darin ist der vom 29.09.2026; den dort offenen Scanbeginn hat TB-124 geschlossen (50.4).*

> **Vollzug TB-30b Posten 3 (11.3) in TB-122 (Tatsachennotiz nach 37.3)**
>
> **Gemessen in TB-122, 29.09.2026** (Belege `docs/belege/TB-122/`, Ergebnis
> `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`). Eingang `04f07ef`, Schritt 0 `c064405`. Freigabe des
> Betreibers 27.09.2026, ca. 20:20 (Auswahlkarte „E-1: TB-30b Posten 3“), Nachtrag 29.09.2026, ca. 14:52 (bis zu drei
> Testdateien; 27c R31 (b)). Kein Abbruchkriterium ausgelöst.
>
> **Grund:** 11.3 — `sma_trend_filter` war bei `rsi2_mean_reversion` eine Konstante; `bb_squeeze_percentile` und
> `bb_lookback` erreichten bei beiden Volatility-Breakout-Bots die Indikatorberechnung nicht. Ohne die Durchreichung
> ist das registrierte Raster (Abschnitt 3) für diese drei Bots nicht rechenbar (R49 (h): 11.3 ist E-1).
>
> **Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“):
>
> | Datei | vorher | nachher | Commit | vollzieht |
> |---|---|---|---|---|
> | `strategies/rsi2_mean_reversion/backtest_rsi2.py` | `c0a59a43…` | `836b032a…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `9b2d2a2f…` | `777f5cb0…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/equity_simulation.py` | `3a29a4f1…` | `864907fb…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/multi_symbol_optimise.py` | `93799bdd…` | `f0a4ee43…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/equity_simulation.py` | `fde65dbb…` | `7cbc7f00…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | `e7710d4d…` | `02548e2e…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/equity_simulation.py` | `c760c6b8…` | `11094387…` | `ab31314` | 11.3 |
>
> Neu (kein Vorher), Commit `08153e4`: `strategies/rsi2_mean_reversion/test_posten3_durchreichung.py` `1b4edfbc…`,
> `strategies/volatility_breakout/test_posten3_durchreichung.py` `50e872e2…`,
> `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` `3f78f6da…`.
>
> **`herkunft.register()`:** `01f5997a…` vorher = nachher. Die sieben Dateien gehören nicht zu den eingefrorenen
> Teilen; die Sonde gegen `46f0ad5d…` ist vorher und nachher byte-gleich (Punkt 11 „nicht prüfbar“). Der Übergang
> steht deshalb nur hier und im Commit.
>
> **Nachweis:** Mit den Voreinstellungen (200; 126 / 25.0) sind die Ausgaben von B6, Signalpfad, Kapitalkurve und
> Optimierer-Kurzlauf **13/13 bytegleich**; der Trockenlauf ohne Modus ist 18/18 zeichengleich. Die erste
> Registerstufe (26; 20 / 5) kommt nachweislich in der Indikatorberechnung an (16/16, 12/12, 12/12); am Stand vor
> dem Umbau scheitert dieselbe Probe (40.7).
>
> **Folge aus R47 (Fable 29b, F-17):** Nach Posten 3 ist `SMA_TREND_PERIOD` bei `rsi2_mean_reversion` **Rasterachse**
> (`sma_trend_filter`), nicht Parameterdatei; der Name in `backtest_rsi2.py` bleibt als Voreinstellung.
>
> **Stand 11.3:** geschlossen bis zur Indikatorberechnung; offen der Scanbeginn der Breakout-Bots
> (`backtest_breakout.py::WARMUP_PERIOD`, TB-122 Befund F1).

### 50.4 Vollzug TB-124 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Z. 289–323 (Commit `0f56aeb`). Abgenommen vom steuernden Chat am 30.09.2026; die Befunde der Abnahme berühren keinen Satz dieses Entwurfs. Der Schlusssatz („Der Scanbeginn der Zelle liegt an ihrem Vorlauf …“) folgt der Lesart in 50.5.*

> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn, in TB-124 (Tatsachennotiz nach 37.3)**
>
> **Gemessen in TB-124, 30.09.2026** (Belege `docs/belege/TB-124/`, Ergebnis
> `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md`). Eingang `0034960`, Schritt 0 `baf18a2`. Freigabe des Betreibers
> 30.09.2026, 19:13 (Sachentscheid „TB-122 F1 … geht in TB-124“), Nachtrag 19:44 (zwei Testdateien; 27c R31 (b)).
> Handwerksvorgabe Nachtrag 1 (steuernder Chat, ca. 20:15) nach Fable 30a R53. Kein Abbruchkriterium ausgelöst.
>
> **Grund:** 11.3 (TB-122 Befund F1) — bei beiden Volatility-Breakout-Bots erreichte `bb_lookback` die
> Indikatorberechnung (TB-122), der Scanbeginn hing aber an der Voreinstellung (`WARMUP_PERIOD + 1` = 127). Bei den
> Stufen 20 und 97 schnitt er mögliche Einstiege ab (Balken 39–126 bzw. 116–126); bei den Stufen über 126 lag er vor dem
> Vorlauf der Zelle.
>
> **Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11):
>
> | Datei | vorher | nachher | Commit | vollzieht |
> |---|---|---|---|---|
> | `strategies/volatility_breakout/backtest_breakout.py` | `8dce183d…` | `3fd0cef6…` | `f90135e` | 11.3 |
> | `strategies/volatility_breakout_crypto/backtest_breakout.py` | `b7923b08…` | `3c7ccbe7…` | `f90135e` | 11.3 |
> | `strategies/volatility_breakout/test_posten3_durchreichung.py` | `50e872e2…` | `9a360566…` | `499d68b` | 11.3 (Probe) |
> | `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` | `3f78f6da…` | `5a5ad774…` | `499d68b` | 11.3 (Probe) |
>
> **`herkunft.register()`:** `01f5997a…` alt = neu. Die vier Dateien gehören nicht zu den eingefrorenen Teilen; die
> Sonde gegen `46f0ad5d…` ist vorher und nachher byte-gleich (Punkt 11 „nicht prüfbar“). Der Übergang steht deshalb nur
> hier und im Commit.
>
> **Nachweis:** Mit den Voreinstellungen (126 / 25.0) sind B6, Signalpfad, Kapitalkurve und Optimierer-Kurzlauf
> **13/13 bytegleich**; der Trockenlauf ohne Modus ist 18/18 zeichengleich. Für jede Registerstufe von `bb_lookback`
> beginnt der Scan am ersten Index, an dem die Einstiegsbedingung definiert ist (`BB_PERIOD + L − 1`), und ein
> Einstieg genau dort wird über Signal- und Optimierer-Pfad gefunden (43/43, 42/42); am Stand vor dem Umbau scheitert
> dieselbe Probe (40.7).
>
> **Stand 11.3:** geschlossen — `sma_trend_filter` (rsi2_mean_reversion), `bb_squeeze_percentile` und `bb_lookback`
> (beide Breakout-Bots) erreichen Indikatorberechnung und Scanbeginn. **Der Scanbeginn der Zelle liegt an ihrem Vorlauf
> (Fable 30a, R53):** er ist der erste Index, an dem die Einstiegsbedingung der Zelle definiert ist — bei den
> Breakout-Bots `BB_PERIOD + L − 1`, nie früher, nicht später.

> ⭐ **50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt** (Fable 01a R57, nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.5 Lesart des steuernden Chats zu R53 (49.1) — Zählweise des Vorlaufs

⚠️ **Vorläufig, bis Fable bestätigt** (Bauart 46.9).

R53 nennt die Regel, nicht die Werte (30a, „Unsicher“ zu Frage 1). Wörtlich addiert ergäbe „oberste Stufe zuzüglich der festen Fenster“ bei den zwei Volatility-Breakout-Bots L + 20 (Bollinger-Fenster 20). Aus dem Code hergeleitet ist der erste Balken, an dem die Einstiegsbedingung einer Zelle definiert ist, `BB_PERIOD + L − 1`, also L + 19. Das Bollinger-Fenster über `close` und das Squeeze-Fenster L über `bb_width` sind zwei hintereinanderliegende rollende Fenster ohne `min_periods`, die sich einen Balken teilen (`docs/belege/TB-124/b1_herleitung.txt`, je Stufe von `bb_lookback` und Voreinstellung; Nachtrag 1 zu TB-124). Dieser Eintrag liest R53 als den hergeleiteten Wert, also den ersten definierten Index, nicht als Summe von Fensterlängen. Das ist eine Lesart des steuernden Chats; sie geht mit der nächsten Anfrage an Fable zur Bestätigung. Für die übrigen sieben Bots ist der Vorlauf noch nicht hergeleitet; das geschieht mit R53 (a) (50.7).

> ⭐ **50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt** (Fable 01a R57, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.6 Tatsachennotiz zu R24 (47.7) — Entscheid des Betreibers

Zur Entscheidungsvorlage in R24 hat der Betreiber am 29.09.2026 per Auswahlkarte „(a) So lassen“ gewählt, die Empfehlung des Verfahrensprüfers (T116-5; `docs/projektfuehrung/UEBERGABE_ARCHIV.md`, Nachtrag 29.09.2026, 12:25, und Umzug 29.09.2026, 20:48, Block 6). Ein Deckel je Bot vor dem Netting ist damit nicht registriert.

### 50.7 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R41: Neurechnung von 15.4 nach 41.3 C2 (Kerzenzählung) | Mac-Messung vor dem Tag |
| 2 | R48 (d): `mittlere_exposure` im Vertrag bilden, bewertet wie die MtM-Reihe | mit dem Zellen-Erzeuger (R46) |
| 3 | R50: die Zahl „34“ (Zählweise), die Ausstiegskonvention der neun `backtest_*.py`; Nebenbefund DSR-Einheiten `kennzahlen.py:222–224` (Vormessung 29.09.2026, Abschnitt 2) | vor dem Tag |
| 4 | R53 (a): Vorlauf je Bot aus `registerdaten.py` rechnen; feste Fenster ohne Eintrag; Herleitung für die übrigen sieben Bots | Handwerk (BACKLOG „Aus Fable 30a“) |
| 5 | R55: Probe „leere Menge ⇒ (d) nicht erfüllt“ mit Gegenprobe, dazu der Nebenfall | Handwerk (BACKLOG „Aus Fable 30a“) |
| 6 | R28: das Literal in `pruefe_abschnitt17.py:97` | Fable zur Kenntnis, dann Handwerk |
| 7 | R39: Feldlisten für `zellenbericht.csv`, `symbole_je_falte.csv`, Lese-Audit | mit dem Zellen-Erzeuger |
| 8 | R42: Punkt 15 im Listentext von Abschnitt 10 | vor dem Tag, nach R42 |
| 9 | R21: Anforderung an das Leiter-Skript, Stufe IV | mit dem Leiter-Skript |
| 10 | R8 (d): Verweis aus Register 9 (45.8) | nach dem Tag; die Marke in 9 aus R51 ist eine andere |
| 11 | R31 (b), R49 (e): Regeln für das Regelwerk (Freigabe nennt die Tests; Marken nennen Bezeichner) | Dokumentationsauftrag |
| 12 | Lesarten und Reibung: 50.5 (Zählweise), R48 (d) (Registertext gilt, wo der Code die Grösse nicht hat), R53 („Literal mit Test“ gegen „nicht als Literal“) | nächste Anfrage an Fable |
| 13 | R26: Lauf von `auswertung.py --bot` unter dem Modus an einem Stand nach `0f56aeb` | vor dem Tag, mit den Tag-Vorbedingungen |

## 51. Fable 01a — Registerblock R56–R62 (TB-129)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md`, md5 `4995260b7af91d2f4c058b1e2c49e788`, 22 084 B, im Repo seit Commit `7238842`, unverändert am Commit `477cef2`, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R56)“, Z. 113–132. Die Datei hat der steuernde Chat am 01.10.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` gleich (`docs/projektfuehrung/UEBERGABE.md` am Commit `477cef2`, Nachtrag 01.10.2026, ca. 23:35). Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern 51.1–51.7 hat der steuernde Chat vergeben (Auftrag TB-129, Einzelfreigabe des Betreibers), nicht Fable. Dieser Kopf nennt Datei, md5 und Commit; das ist für die Antwort 01a die Bindung nach R56 (b). Gesetzt sind die Marken, die R61 (b) aufzählt: sieben Zeilen als Nachtrag zu E-2 und fünf aus dieser Antwort, zusammen 14 Marken, weil 4.2 und 49.1 je zwei Blöcke nennen. ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke. Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 51.8; eine Lesart des steuernden Chats steht in 51.9 und ist vorläufig; was offen bleibt, steht in 51.10. 51.8 bis 51.10 sind Text des steuernden Chats, nicht Fables.

### 51.1 R56 — Ergänzung zu 27.4 und 27.6 (Anfangsbestand eines neu begonnenen Chats des Verfahrensprüfers)

> R56 — Ergänzung zu 27.4 und 27.6 (Anfangsbestand eines neu begonnenen Chats des Verfahrensprüfers). (a) Der Anfangsbestand eines neu begonnenen Chats wird festgehalten durch den Wortlaut seines Eröffnungstextes und durch das Leseprotokoll seiner ersten Antwort; ein eigener Registerblock je Chat ist dafür nicht nötig. (b) Bedingungen: Der Eröffnungstext liegt mit Commit im Repo, bevor die Antwort eingetragen wird. Das Leseprotokoll der ersten Antwort nennt, was der Chat vollständig gelesen hat, was nur als Ausschnitt, was nicht, was die Plattform ohne sein Zutun geladen hat (Projekt-Erinnerung, Dateiliste), die Grössen, die an 27.1 grenzen, und schliesst mit dem Satz, dass er weitere Grössen nach 27.1 nicht kennt. Die Antwortdatei liegt mit Commit im Repo; trägt sie Registertext, nennt der Kopf des Abschnitts Datei, md5 und Commit. (c) Ein eigener Block nach der Bauart von R32 bleibt nötig, wenn ein Chat mehr weiss, als Eröffnungstext und Leseprotokoll nennen: nach einer Verdichtung, bei Wissen aus einem Vorgängerchat, nach einer Treffermeldung mit Inhalt (27.7). (d) Die Projekt-Erinnerung der Plattform ist ein Träger zwischen Chats. Der Verfahrensprüfer liest aus ihr nur Dateien, die der steuernde Chat auf Grössen nach 27.1 gemessen und im Eröffnungstext genannt hat; alle anderen stehen unter derselben Sperre wie BACKLOG.md. (e) Vor dem signierten Tag schliesst eine Tatsachennotiz die Protokollkette: je Chat des Verfahrensprüfers seit R32 der Eröffnungstext (Datei, Commit) und die Antwortdateien (md5, Commit). Ein Chat ohne Antwortdatei hat nichts entschieden und steht nicht in der Kette. Der Chat vom 01.10.2026 (Antwort 01a) hat keinen eigenen Block; sein Anfangsbestand ist das Leseprotokoll von 01a. [Voraussetzung, zu messen: dass sein Eröffnungstext mit Commit im Repo liegt.]
> Quelle des Grundes: 27.4 (Leseprotokoll in jeder Antwort, Selbstauskunft, Prüfung beim steuernden Chat), 27.6 (die Kette beginnt mit einer Tatsachennotiz, die selbst Selbstauskunft ist), R32 (Bauart), 27.7, Bauart der Abschnittsköpfe 47 bis 49. Kein Ergebnis.

**Kette:** Marken: Abschnitt 27. Voraussetzung gemessen: 51.8.

### 51.2 R57 — Präzisierung zu R53 (49.1) und Bestätigung von 50.5 (Zählweise des Vorlaufs)

> R57 — Präzisierung zu R53 (49.1) und Bestätigung von 50.5 (Zählweise des Vorlaufs). Der Vorlauf einer Zelle ist die Zahl der Balken, die vor dem ersten Balken liegen, an dem die Einstiegsbedingung der Zelle definiert ist — der nullbasierte Index dieses Balkens, gezählt ab dem ersten Balken ab Horizontbeginn (28.6), bei Bots ohne Horizont (26.2) ab dem ersten Balken des Bestands. Er wird aus dem Signalpfad hergeleitet und ist nicht die Summe der Fensterlängen: Hintereinanderliegende Fenster teilen Balken, nebeneinanderliegende addieren sich nicht. „Zuzüglich der festen Fenster“ in R53 nennt die Bestandteile, nicht die Rechenart. Der Vorlauf des Bots ist der grösste Vorlauf über die Zellen, die nach Abschnitt 6 existieren. Dieselbe Zählweise trägt 25.2 mit 32.2: 150 Balken Vorlauf, warm ab dem Balken mit 150 Balken davor. Die Lesart in 50.5 und der Schlusssatz von 50.4 sind damit bestätigt. [Voraussetzung, zu messen: dass BB_PERIOD + L − 1 in backtest_breakout.py ein nullbasierter Index ist und dass faltenplan.py einen Vorlauf v als „v Balken liegen davor“ anwendet; weicht eines ab, gilt diese Definition, und die Formel folgt ihr.]
> Quelle des Grundes: R53 („Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf“), 25.3 (i) („am 1. Januar der Indikator-Vorlauf erfüllt“), 25.2, 32.2, 28.6, 26.2, Abschnitt 6. Kein Ergebnis.

**Kette:** Marken: 49.1 (R53); 50.5. Voraussetzung gemessen: 51.8.

### 51.3 R58 — Tatsachennotiz zu 25.3 (i) (Verhältnis der Marken 26.2 und R53)

> R58 — Tatsachennotiz zu 25.3 (i) (Verhältnis der Marken 26.2 und R53). Bedingung (i) hat zwei Teile. „Im registrierten Datenhorizont des Bots“ ist präzisiert durch 26.2 (absolutes Datum je Bot; Wert in 28.4). „Am 1. Januar der Indikator-Vorlauf erfüllt“ ist präzisiert durch 28.6 (gerechnet gegen den Horizontbeginn) und durch R53 mit R57 (Grösse und Zählweise des Vorlaufs). Die Marken stehen nebeneinander; keine ersetzt die andere. Gültig ist 25.3 im Wortlaut mit 26.2, 28.6, R53 und R57.
> Quelle des Grundes: Wortlaut von 25.3, 26.2, 28.6, R53. Kein Ergebnis.

**Kette:** Marken: 25.3, Ersatztext.

### 51.4 R59 — Ergänzung zu R53 (49.1) (kein Rückfall auf ein Literal; Eingaben der Rechnung)

> R59 — Ergänzung zu R53 (49.1) (kein Rückfall auf ein Literal; Eingaben der Rechnung). (a) „Nicht als Literal gesetzt“ gilt ohne Ausnahme. Der Satz „sonst Literal mit Test nach 32.5 (c)“ aus Fable 30a stand unter „Unsicher“ und ist kein Registertext; das Register nennt für den Vorlauf keinen Wert, gegen den ein Test ein Literal halten könnte. (b) Eingaben der Rechnung sind die registrierten Stufen (Abschnitt 3, über registerdaten.py) und die festen Fenster des Bots. Ein festes Fenster, für das registerdaten.py keinen Eintrag hat, erhält dort einen Eintrag; das ist eine Änderung am Träger der Festlegungen und braucht die Freigabe des Betreibers (26.6, 32.5 (a)). Jeder solche Eintrag ist die Kopie einer Konstante des Bot-Codes und trägt eine Probe gegen diese Konstante, mit Gegenprobe (40.7). (c) Die Formel, die aus Stufen und Fenstern den Vorlauf einer Zelle bildet, trägt je Bot eine Probe gegen den Signalpfad: Ein Einstieg genau am Vorlauf wird gefunden, davor ist die Bedingung nicht definiert (Bauart TB-124, 50.4), mit Gegenprobe. (d) Der Faltenplan trägt den gerechneten Wert je Bot als Feld (R53); sichtbar wird der Wert dort, nicht in einer Konstante.
> Quelle des Grundes: R53, 32.5 (a) und (c), 26.6, R28 (Kopie mit Probe als benannter Zwischenstand), 37.5 (ein Wert, ein Ort), 40.7, 50.4. Kein Ergebnis.

**Kette:** Marken: 49.1 (R53). Bestand gemessen: 51.8.

### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger)

> R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger). (a) Wo der Code des Urteils die Grösse nicht bildet, gilt die Definition in R48 (d). Code des Urteils ist der Code auf der Sperrliste und im Laufbereich (R50); ein Messwerkzeug ausserhalb legt keine Definition fest. [Voraussetzung, zu messen: dass research/exposure_messung/ nicht zum Laufbereich gehört.] (b) auswertung.py::beta_bereinigung bildet eine mittlere Exposure als arithmetisches Mittel der Spalte exposure der Tagesreihe und gibt sie unter dem Schlüssel mittlere_exposure zurück. Das ist eine Bildung im Sinn von R48 (d). Der Registertext folgt ihr in der Aggregation (Mittel über die Tage). Die Bewertung der Spalte exposure legt dieser Code nicht fest; sie folgt R48 (d): Anteil des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a). [Voraussetzung, zu messen: über welche Tage beta_bereinigung mittelt; R48 (d) und 7 (c) verlangen die Selektionsfalten des Gewinners; eine Abweichung ist ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet.] (c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe. auswertung.py wird dafür nicht geöffnet. (d) Die Zeile zu R48 (d) in 50.1 ist unvollständig; sie wird als Tatsachennotiz um die Fundstelle in beta_bereinigung ergänzt.
> Quelle des Grundes: R48 (d), R50 (Definitionen im eingefrorenen Code), 4.2, 7 (c), 37.5 (ein Wert, ein Ort), R36 (Bauart: ein Wert, der nachgerechnet werden kann), R46. Kein Ergebnis.

> ⭐ **51.5 R60 (a) PRÄZISIERT durch R63 (52.1)** (Fable 02a R63, TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **51.5 R60 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **51.5 R60 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 4.2; 48.16 (R48). Voraussetzung gemessen: 51.8. Lesart, vorläufig: 51.9. Offen: 51.10 Nr. 6.

### 51.6 R61 — Marken nach E-2 (Regel, Nachtrag, eine Berichtigung)

> R61 — Marken nach E-2 (Regel, Nachtrag, eine Berichtigung). (a) Nennen R51 und ein Unterpunkt von R48, R49 oder R50 denselben Ort, trägt der Ort eine Marke, die auf den Unterpunkt zeigt; sie erfüllt beide. Zwei Marken an einem Ort sind keine Doppelung, wenn sie auf verschiedene Inhalte zeigen (Abschnitt 12: R49 (d) und R50). (b) Eine Marke steht dort, wo ein Block dem Wortlaut eines Ortes eine Bedeutung gibt oder ihm etwas hinzufügt (34). Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, der im erzeugten Block liegt oder in Abschnitt 10. Danach sind nachzutragen, der alte Satz bleibt zeichengleich: 16.4, „Prüfung vor dem Tag“ — PRÄZISIERT durch R21 (47.4). Abschnitt 1, Tabelle, Zeile 3 — PRÄZISIERT durch R36 (48.4). Abschnitt 8, Tabelle — PRÄZISIERT durch R36 (48.4). Abschnitt 8, Tabelle — ERGÄNZT durch R55 (49.3). Abschnitt 7, Tabelle, Zeile (b) — PRÄZISIERT durch R37 (48.5). 4.2 — PRÄZISIERT durch R48 (48.16), Unterpunkte (d) und (e), und durch R60. 43.2, Eintrag 43-7 — PRÄZISIERT durch R33 (48.1). Dazu aus dieser Antwort: 27 — ERGÄNZT durch R56. 49.1 — PRÄZISIERT durch R57 und ERGÄNZT durch R59. 50.5 — bestätigt durch R57. 25.3 — ERGÄNZT durch R58. 48.16 — ERGÄNZT durch R60. Ohne Marke bleiben, vom Index geführt: R27, R28, R30, R54 an 7 (c), R52 (b), R38, R41 an 41.2 B3, R47 an 5.4, R48 (h), R49 (c) und (e), R31 (a) und (e), R39, R43, R25. (c) Berichtigung: In R26 (47.9) und R30 (47.13) lies „14“ als „Sperrlistenpunkt 14 (Abschnitt 10)“; Abschnitt 14 des Registers ist der Nulltest S-E1 und nicht gemeint. [Voraussetzung, zu messen: der Wortlaut von Sperrlistenpunkt 14; hier nach REGISTER_INDEX.]
> Quelle des Grundes: 34 (Marke am alten Ort, nach der Wiedergabe in 43.0), R51, Kopf von 48 („Vereinigung“), Wortlaut der genannten Orte, Abschnitt 14. Kein Ergebnis.

> ⭐ **51.6 R61 (b) PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **51.6 R61 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken, nachgetragen nach (b): 1, Tabelle, Zeile 3; 4.2; 7, Tabelle, Zeile (b); 8, Tabelle (R36 und R55); 16.4, „Prüfung vor dem Tag“; 43.2, Eintrag 43-7. Voraussetzung gemessen: 51.8. Orte ohne Marke: 51.10 Nr. 7.

### 51.7 R62 — Tatsachennotizen 01a

> R62 — Tatsachennotizen 01a. (a) 25.2: „der 150. Balken liegt am 2018-01-14“ ist um einen Balken ungenau. Bei Daten ab 2017-08-17 und 137 Balken bis 2017-12-31 ist der 150. Balken der 2018-01-13; der 2018-01-14 ist der Balken mit 150 Balken davor. „Warm ab 2018-01-14“ (32.2) bleibt richtig; die Zählweise steht in R57. Der Satz in 25.2 bleibt zeichengleich. [Kalenderrechnung des Verfahrensprüfers; zu messen: dass die Tagesdatei im Januar 2018 lückenlos ist.] (b) Das Literal SOLL_DATENSTAND in research/registernachtrag_tb48/pruefe_abschnitt17.py ist ein vierter Ort des Datenstands neben den drei aus R28; zur Kenntnis genommen, Probe oder Auflösung ist Handwerk. (c) Der Chat des Verfahrensprüfers vom 01.10.2026 hat das Register als Kopie je Abschnitt gelesen (REGISTER_KOPIE_ABSCHNITT_<nn>.md, Commit db108a6, sha256 b5804659…, KOPIE): 24 von 51 Abschnitten vollständig, die übrigen nicht. Er hat keinen Helfer und keinen Suchlauf benutzt.
> Quelle des Grundes: 25.2, 32.2, R28, 50.1, Leseprotokoll 01a. Kein Ergebnis.

**Kette:** Marken: keine. Voraussetzung gemessen: 51.8.

### 51.8 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 01a „zu messen“ nennt. Gemessen über die Geräteanbindung, nur lesend, am 02.10.2026 am Stand `560ca75`; die Sitzung TB-129 hat in Schritt 0 jede Fundstelle am Commit `477cef2` nachgemessen (`docs/belege/TB-129/0d_vorpruefung.txt`). Zeilenangaben gelten am Commit `477cef2`. Kein Ergebnis gelesen (27.1); die Kalenderzählung in den Kursdateien ist eine Verfahrensmessung nach 27.2.

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R56 (51.1) (b), (e) | der Eröffnungstext des Chats vom 01.10.2026 liegt mit Commit im Repo | `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` trägt den Eröffnungstext in zwei Fassungen: Fassung 2 seit `eaea530` (01.10.2026), Fassung 3 seit `7238842` (02.10.2026). `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_neuer_chat.md` und die Antwort 01a liegen seit `7238842` im Repo | erfüllt für beide Fassungen, vor diesem Eintrag. Im Chat kam nach Angabe des Betreibers Fassung 2 an (Auswahlkarte, 02.10.2026); das gehört in die Tatsachennotiz nach R56 (e) (51.10) |
| R57 (51.2) | `BB_PERIOD + L − 1` in `backtest_breakout.py` ist ein nullbasierter Index | `strategies/volatility_breakout_crypto/backtest_breakout.py:119–122, 129` und `strategies/volatility_breakout/backtest_breakout.py:160–163, 170`: „0-basiert, rolling ohne min_periods“, „der Einstieg bei i braucht is_squeeze[i - 1]; also i >= BB_PERIOD + L - 1“, `start_i = BB_PERIOD + squeeze_lookback_days - 1` | trifft. Der Index ist nullbasiert, und die Bedingung liest die Vorkerze; beides zusammen ergibt L + 19 (01a, „Unsicher“ 1) |
| R57 (51.2) | `faltenplan.py` wendet einen Vorlauf v als „v Balken liegen davor“ an | `research/vorregistrierung/faltenplan.py:242` ruft `symbolbeginn`; `research/faltenplan_neun/faltenplan_neun.py:415–428` (`symbolbeginn`) ruft `warm_ab` (Z. 402–412), das `balken_datum(pfad, eig["vorlauf_balken"], anker)` zurückgibt; `balken_datum` (Z. 301–318): „Das Datum des `nummer`-ten Balkens (0-basiert) ab `anker`“ | trifft: „warm ab“ ist der Balken mit Index v, v Balken liegen davor |
| R60 (51.5) (a) | `research/exposure_messung/` gehört nicht zum Laufbereich | `shared/paths.py:242` (`ARBEITSBAUM_PFADE`) und `docs/belege/TB-112/a2_laufbereich.txt:8` führen `research/exposure_messung/bot_lauf.py` (Lauf-Typ `trockenlauf`); es ist in beiden die einzige Datei des Ordners. `exposure_kern.py` und `research/exposure_messung/auswertung.py` (Z. 234, 50.1) stehen nicht darin; `bot_lauf.py` importiert `exposure_kern` nicht | trifft für den Ordner **nicht**; trifft für die zwei Stellen, die die Grösse bilden ⇒ Lesart 51.9, an Fable |
| R60 (51.5) (b) | über welche Tage `beta_bereinigung` mittelt | `research/vorregistrierung/auswertung.py:502–503`: Fenster sind die Falten des Plans, deren Name in `selektionsfalten` steht, halboffen (Z. 510–511); die Reihe ist die der Gewinnerzelle (Aufruf Z. 665); gemittelt wird über die gemeinsamen Tage von Tagesreihe und Benchmark (`gemeinsam`, Z. 517; Spalte `exposure`, Z. 523; `np.mean`, Z. 528), zurück unter `mittlere_exposure` (Z. 537) | Falten und Zelle: trifft (R48 (d): „die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“)“). Tage: gemittelt wird über die gemeinsamen Tage mit dem Benchmark; ob das alle „Handelstage des Zeitraums“ nach R48 (d) sind, ist **nicht gemessen** ⇒ offen, an Fable mit R60 (c) (51.9, 51.10 Nr. 6) |
| R60 (51.5) (d) | die Zeile zu R48 (d) in 50.1 wird um die Fundstelle in `beta_bereinigung` ergänzt | Tatsachennotiz zu 50.1: Die Zeile nennt für `auswertung.py` nur Z. 405 (Eingabe aus `zellen.csv`). Dazu kommt: `auswertung.py::beta_bereinigung` bildet eine mittlere Exposure als arithmetisches Mittel der Spalte `exposure` der Tagesreihe (Z. 523, 528) und gibt sie als `mittlere_exposure` zurück (Z. 537) | ergänzt; die Zeile in 50.1 bleibt zeichengleich |
| R61 (51.6) (c) | der Wortlaut von Sperrlistenpunkt 14 | Abschnitt 10, Punkt 14: „Die Reihenfolge Selektion → Bestätigungsperiode → Bericht — im Kopftext von `auswertung.py` als Ablauf festgeschrieben“. Abschnitt 14 heisst „Der Nulltest S-E1“. R26 (47.9) schreibt „(12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun)“; R30 (47.13) heisst „Ergänzung zu 14 und zu den Tag-Vorbedingungen“ | trifft: gemeint ist Sperrlistenpunkt 14 |
| R62 (51.7) (a) | die Tagesdatei ist im Januar 2018 lückenlos | `data/BTCUSDT_1d.csv` und `data/ETHUSDT_1d.csv`, je: erster Balken 2017-08-17, 137 Balken bis 2017-12-31, Index 149 (nullbasiert) = 2018-01-13, Index 150 = 2018-01-14, 31 Tage im Januar 2018, keine Lücke und kein doppeltes Datum bis 2018-01-31 | trifft für beide Dateien: Der 150. Balken ist der 2018-01-13, der 2018-01-14 hat 150 Balken vor sich |
| R62 (51.7) (c) | 24 von 51 Abschnitten gelesen | Das Leseprotokoll von 01a nennt 24 Abschnittsdateien als vollständig gelesen und 27 Abschnitte als nicht gelesen; zusammen 51 (Abschnitte 0–50). Register am `db108a6`, sha256 `b5804659…` | passt |
| R59 (51.4) (b) | Bestand, keine Voraussetzung Fables | `research/vorregistrierung/registerdaten.py:213–216` führt das Bollinger-Fenster als Regel `bollinger_fenster` (20.0); `BB_PERIOD = 20` steht in `strategies/volatility_breakout_crypto/backtest_breakout.py:69` und `strategies/volatility_breakout/backtest_breakout.py:101`. Ob diese Regel der Eintrag nach R59 (b) ist und ob eine Probe gegen `BB_PERIOD` besteht, ist nicht gemessen | offen (51.10) |

### 51.9 Lesart des steuernden Chats zu R60 (a) (51.5) — Reichweite der Voraussetzung

⚠️ **Vorläufig, bis Fable bestätigt** (Bauart 46.9).

R60 (a) setzt voraus, dass `research/exposure_messung/` nicht zum Laufbereich gehört. Für den Ordner trifft das nicht zu: `bot_lauf.py` steht in der Pfadliste (51.8). Die zwei Stellen, die die Grösse zum Einstand bilden (`exposure_kern.py` und `research/exposure_messung/auswertung.py`, 50.1), stehen nicht darin. `bot_lauf.py` selbst nennt in seinem Docstring (Z. 21–22) als Bedarf einer Exposure-Messung je Zeitpunkt die offenen „Positionen samt gebundenem Kapital“; ob es damit die Grösse im Sinn von R60 (a) bildet, ist nicht gemessen und geht mit an Fable. Dieser Eintrag liest R60 (a) für die Stellen, die die Grösse bilden, nicht für den Ordner: Die Bewertung zum Einstand in diesen zwei Dateien legt keine Definition fest; es gilt R48 (d). Das ist eine Lesart des steuernden Chats; sie geht mit der nächsten Anfrage an Fable. Mit ihr geht die Frage zu R60 (b) und (c): „über die Tage der Falte“ sagt nicht, ob die Tage der Tagesreihe oder die gemeinsamen Tage mit dem Benchmark gemeint sind; `beta_bereinigung` schneidet auf die gemeinsamen Tage, und ob das alle Handelstage des Zeitraums nach R48 (d) sind, ist nicht gemessen (51.8).

> ⭐ **51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt** (Fable 02a R63, TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 51.10 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R56 (d): die Dateien der Projekt-Erinnerung, die die Plattform einem Chat des Verfahrensprüfers lädt (01a nennt `preferences.md` und `ways-of-working.md`), auf Grössen nach 27.1 messen und im Eröffnungstext nennen | steuernder Chat, vor der nächsten Eröffnung eines Fable-Chats |
| 2 | R56 (e): Tatsachennotiz, die die Protokollkette schliesst (je Chat seit R32 Eröffnungstext und Antwortdateien mit md5 und Commit); darin die Fassung des Eröffnungstextes vom 01.10.2026 | vor dem signierten Tag |
| 3 | R59 (b): Einträge für feste Fenster in `registerdaten.py`, je mit Probe gegen die Konstante und Gegenprobe | Umsetzungsauftrag mit Einzelfreigabe des Betreibers (26.6, 32.5 (a)) |
| 4 | R59 (c), (d) und R57: Probe der Formel je Bot gegen den Signalpfad; Feld im Faltenplan; Herleitung des Vorlaufs für die übrigen sieben Bots | mit R53 (a) (50.7 Nr. 4) |
| 5 | R60 (c): beide Träger aus einer Rechnung, Probe in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
| 6 | R60 (a), (b) und (c): die Lesart 51.9; die Tage in (b) (gemeinsame Tage mit dem Benchmark gegen „Handelstage des Zeitraums“, nicht gemessen) und in (c) | nächste Anfrage an Fable; die Messung zu (b) vor dem Tag |
| 7 | Orte, die R61 (b) nicht aufzählt und die deshalb keine Marke tragen: 47.9 und 47.13 (R61 (c): „14“ lies „Sperrlistenpunkt 14“), 25.2 (R62 (a)), 50.1 (R60 (d)), 50.4 (R57: Schlusssatz bestätigt). Sie stehen als Indexzeilen in `REGISTER_INDEX.md` | nächste Anfrage an Fable |
| 8 | R62 (b): das Literal `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py`, Probe oder Auflösung | Handwerk (50.7 Nr. 6) |

## 52. Fable 02a — Registerblock R63–R65 (TB-130)

Reines Eintragen von Registertext, Bauart wie 51. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md`, md5 `a7821eeb4f61faad5f74f72ec7201797`, 21 709 B, im Repo seit Commit `b0c7a35`, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R63)“, Z. 112–119. Die Datei hat der steuernde Chat am 02.10.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` gleich; das Lesewerkzeug lieferte Text und keine Datei, die Bytegleichheit mit der Ablage ist deshalb nicht gemessen. Der Eröffnungstext des Chats (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02_eroeffnung.md`) und die Anfrage liegen seit `b0c7a35` im Repo; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern 52.1–52.3 hat der steuernde Chat vergeben (Auftrag TB-130, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind zwölf Marken: die fünf, die R65 (b) aufzählt, und sieben nach der Regel in R65 (a) an den Orten, die R63, R64 und R65 selbst als Bezug nennen (4.2, 48.16, 48.19, 51.5 zweimal, 51.6, 51.9). Diese sieben hat der steuernde Chat bestimmt, nicht Fable. Die Marke an 25.2 steht direkt unter dem berichtigten Satz, vor der Marke aus R53 (R65, Quelle des Grundes, 34.3). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke (R65 (d)). Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 52.4; was offen bleibt, steht in 52.5. 52.4 und 52.5 sind Text des steuernden Chats, nicht Fables.

### 52.1 R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner)

> R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner). (a) Massgeblich in R60 (a) ist, ob eine Stelle die Grösse bildet, nicht in welchem Ordner sie liegt. Eine Stelle bildet die mittlere Exposure, wenn sie je Tag den Anteil des Kapitals in offenen Positionen rechnet oder daraus ein Mittel; eine Stelle, die Positionen liefert, bildet sie nicht. (b) In der Voraussetzung von R60 (a) lies „research/exposure_messung/“ als „die Stellen, die die Grösse zum Einstand bilden: research/exposure_messung/exposure_kern.py und research/exposure_messung/auswertung.py (50.1)“. Sie liegen ausserhalb von Sperrliste und Laufbereich (51.8) und legen keine Definition fest; es gilt R48 (d) mit R60 (b). Die Lesart 51.9 ist damit bestätigt. (c) research/exposure_messung/bot_lauf.py gehört zum Laufbereich (51.8). [Voraussetzung, zu messen, durch Lesen des Codes und nicht durch Wortsuche: dass bot_lauf.py keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus rechnet.] Trifft sie nicht zu, ist das ein Register-Code-Widerspruch nach 25c (1) zur Bewertung in R48 (d) und R60 (b) und wird gemeldet, nicht eingetragen. (d) Der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus bot_lauf.py oder dessen Ausgabe; die Positionen kommen aus simuliere_portfolio (R45), die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c)).
> Quelle des Grundes: R60 (a), erster und zweiter Satz (die Regel nennt Code und Grösse; den Ordner nennt nur die Voraussetzung), R48 (d) („der Registertext folgt dem Code, wo er ihn hat“), R50, 38.2 (Fundstellen als Datei und Bezeichner; hier nach R49 (e)), R45 (kein zweiter Rechenweg), 24.4 (bewertet zum Marktpreis, nicht zum Einstand), 25c (1). Kein Ergebnis.

**Kette:** Marken: 51.5 (R60); 51.9. Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 4.

### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird)

> R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird). (a) „Handelstage des Zeitraums“ in R48 (d) lies: die Tage des Zeitraums, an denen der Benchmark des Bots definiert ist (23.3), wie benchmark_tagesreihen/<bot>.csv sie führt (R39); die Tatsachennotiz zu 23.3 (erster Kurstag) gilt mit. Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2) und für die des Gewinners über seine Selektionsfalten (7 (c)). (b) Der Schnitt auf die gemeinsamen Tage in auswertung.py::beta_bereinigung ist die Regel aus Abschnitt 7 („Beide Reihen werden auf gemeinsame Tage gebracht“; „über dieselben Tage“) und kein Register-Code-Widerspruch. Ein Tag der Tagesreihe ohne Benchmark-Tag geht in keine mittlere Exposure ein; er ist kein Befund. (c) Ein Benchmark-Tag des Bots in einer Falte des Faltenplans, zu dem die Tagesreihe einer Zelle keine Zeile führt, ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft im Lauf für jede Tagesreihe, dass sie jeden solchen Tag führt (auch flache Tage, 1a), und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. (d) „Über die Tage der Falte“ in R60 (c) lies: über die Tage nach (a), die in die Falte fallen (halboffen wie im Faltenplan; 2a). Der Wert des Gewinners in beta_bereinigung ist dann das mit der Zahl dieser Tage gewichtete Mittel seiner Werte je Selektionsfalte in zellen.csv; die Abnahme nach R46 prüft auch diese Gleichheit, mit Gegenprobe. (e) Welche Tage die Tagesreihe über die Tage nach (a) hinaus führt, legt dieser Block nicht fest. auswertung.py wird für nichts davon geöffnet. [Voraussetzung, zu messen: dass beta_bereinigung ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weglässt; dass an einem Tag ohne Benchmark-Tag keine Zelle eine offene Position führen kann, ausser am Tag aus der Tatsachennotiz zu 23.3.]
> Quelle des Grundes: Abschnitt 7, Präzisierungen zu (c); 24.2 („auf denselben Tagen wie der Benchmark (3b (c))“); 23.3 („Bot und Benchmark leben an jedem Tag in derselben Menge“; ein Tag ohne handelbares Symbol „gehört nicht zum Benchmark“); 23.2, Grund 2 (keine Grösse aus Nichtteilnahme); 4.2; R36; 1a; 2a; R33; R46. Bekannte Richtung der Wirkung, nicht Grund: Unter der zweiten Voraussetzung ist in einer Falte, in der der Benchmark nicht an allen Tagen definiert ist, das Mittel nach (a) nie kleiner als das Mittel über alle Tage der Falte; die Grösse ist nicht gemessen und für die Entscheidung ohne Belang (Bauart 24.3). Kein Ergebnis.

> ⭐ **52.2 R64 ERGÄNZT durch R66 (53.1)** (Fable 02c R66, zu (e), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R71 (53.6): erster Kurstag** (Fable 02c R71, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R72 (53.7): Benchmark-Tag** (Fable 02c R72, Unterpunkt (b), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 4.2; 48.16 (R48); 51.5 (R60). Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 1 bis 3, 5 bis 7 und 9.

### 52.3 R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form)

> R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form). (a) Die Aufzählungen in R51 und R61 (b) wenden die Regel aus 34 an und schliessen sie nicht ab. Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte nach R61 (b), zweiter Satz. Eine Tabelle von Befunden ist keine Statusliste im Sinn von R61 (b), soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem Zusatz, was bestätigt ist (Bauart der Marke an 46.9). (b) Danach sind nachzutragen, der alte Satz bleibt zeichengleich: 47.9 (R26) — BERICHTIGT durch R61 (51.6), Unterpunkt (c). 47.13 (R30) — BERICHTIGT durch R61 (51.6), Unterpunkt (c). 25.2 — BERICHTIGT durch R62 (51.7), Unterpunkt (a), und durch diesen Block, Unterpunkt (c). 50.1, Zeile R48 (d) — ERGÄNZT durch R60 (51.5), Unterpunkt (d), und 51.8. 50.4, Schlusssatz — ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt. (c) Berichtigung zu 25.2: „der 150. Balken liegt am 2018-01-14“ lies „der Balken mit 150 Balken davor liegt am 2018-01-14; der 150. Balken ist der 2018-01-13“. Das Ergebnis von 25.2 (Bedingung (i) ist am 1. Januar 2018 nicht erfüllt) bleibt unberührt, ebenso „warm ab 2018-01-14“ (32.2, nach R62 (a)). (d) Die Marken zu R26 und R30 stehen in 47; in Abschnitt 10 steht weiter keine Marke, R30 bleibt dort Indexzeile.
> Quelle des Grundes: 34 (Kopf: die Marke steht am alten Ort; 34.3: ein „lies“ trägt die Marke direkt unter dem berichtigten Satz), 43.0, R61 (b), erster Satz, und (c), R62 (a) mit der Messung in 51.8 (Index 149 = 2018-01-13, Index 150 = 2018-01-14, zwei Dateien), R57, R60 (d), die Marken an 46.9 und unter 48.16. Kein Ergebnis.

> ⭐ **52.3 R65 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 48.19 (R51); 51.6 (R61); nachgetragen nach (b): 25.2; 47.9 (R26); 47.13 (R30); 50.1, Zeile R48 (d); 50.4, Schlusssatz. In Abschnitt 10 steht weiter keine Marke (R65 (d)).

### 52.4 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02a „zu messen“ nennt. Gemessen am 02.10.2026 am Stand `1833839`, nur lesend, durch einen Helfer des steuernden Chats, der den Code gelesen hat; die Sitzung TB-130 hat in Schritt 0 die genannten Zeilen und Zählungen am Commit `b0c7a35` nachgemessen (`docs/belege/TB-130/0d_vorpruefung.txt`). Aussagen über ein Fehlen (kein Tagesraster, kein Filter, kein Erzeuger) sind Lesung des Helfers; gezählt sind nur Aufrufe von `mean` (`.mean(`, `np.mean`) in `bot_lauf.py` und `dropna` in `auswertung.py`, je 0. Zeilenangaben gelten am Commit `b0c7a35`. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R63 (52.1) (c) | `bot_lauf.py` rechnet keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus; zu messen durch Lesen, nicht durch Wortsuche | `research/exposure_messung/bot_lauf.py` ganz gelesen: Positionen Z. 227–231 (`allocation` Z. 229, `capital_after` Z. 230), geschrieben Z. 242 als `<BOT>_positionen.csv` mit den Spalten `trade_zeile`, `symbol`, `entry_time`, `exit_time`, `pnl_pct`, `allocation`, `capital_after`. Kapital kommt als `es.STARTING_CAPITAL` (Z. 135–136, 246, 254–255) und als `final_capital` (Z. 253–254) vor; Z. 254 teilt beide zur Gesamtrendite. Kein Tagesraster, kein Aufruf von `mean` | trifft: kein Anteil je Tag, kein Mittel |
| R63 (52.1) (d) | Bestand, keine Voraussetzung Fables | `shared/zuteilung.py:657` `def simuliere_portfolio` (R45: `shared/zuteilung.py::simuliere_portfolio`). Die neun `strategies/*/equity_simulation.py` führen je ein `simulate_portfolio`; `bot_lauf.py:133–136` ruft `es.simulate_portfolio` | R63 (d) nennt die Funktion aus R45 |
| R64 (52.2), erste | `beta_bereinigung` lässt ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weg | `research/vorregistrierung/auswertung.py`: `lies_tagesreihe` (Z. 361–370) und `lies_benchmark` (Z. 378–386) lesen, prüfen Spalten und sortieren nach `datum`; kein `dropna`, kein Filter. `beta_bereinigung`: Fenstermaske Z. 510–514, Schnitt Z. 517, Auswahl Z. 522–524, Mittel Z. 528 | trifft. Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft (52.5) |
| R64 (52.2), zweite | an einem Tag ohne Benchmark-Tag kann keine Zelle eine offene Position führen, ausser am Tag aus der Tatsachennotiz zu 23.3 | nicht entscheidbar: Den Kalender der Tagesreihe legt noch kein Code fest; `benchmark_tagesreihen` schreibt bisher kein Erzeuger des Laufs | offen (52.5). Nach 02a, „Unsicher“ 2: Trifft die Voraussetzung nicht zu, bleibt die Regel, und der Satz zur Richtung der Wirkung gilt dann nicht streng |
| R64 (52.2) (a) | Bestand, keine Voraussetzung Fables | R39 (48.7) nennt `benchmark_tagesreihen/<bot>.csv`; `auswertung.py:379` bildet `<markt>.csv` (`markt` aus `rd.BOTS[bot]["markt"]`, Z. 498); 50.2 schreibt dazu „im Zitat lies „`<bot>.csv`“ (R39)“ | Bestand. Wann der Code den Namen je Bot liest, ist nicht festgelegt; `auswertung.py` wird nach R64 (e) nicht geöffnet (52.5) |
| R65 (52.3) (c) | — | die Messung steht in 51.8 (Zeile R62 (a)): Index 149 = 2018-01-13, Index 150 = 2018-01-14, in beiden Kursdateien | trägt die „lies“-Form |

> ⭐ **52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (e), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.4, Zeile „R64 (52.2) (a)“ BERICHTIGT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 52.5 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R64, zweite Voraussetzung: keine offene Position an einem Tag ohne Benchmark-Tag | Messung mit dem Zellen-Erzeuger, vor dem Tag |
| 2 | 02a, „Unsicher“ 1: Zeitachse des Falten-Sharpe in Falten mit teilweisem Benchmark (ob die Tagesreihe Tage vor dem ersten Handelbar-Tag führt); R64 (e) lässt es offen | Vorprüfung (16, 21, 29, 33), dann Anfrage an Fable; vor dem Zellen-Erzeuger |
| 3 | R64 (c) und (d): Wache im Lauf mit Ausgang 2; Probe über das tagegewichtete Mittel in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
| 4 | R63 (d): der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus `bot_lauf.py` | mit dem Zellen-Erzeuger (Abnahme) |
| 5 | `beta_bereinigung` behandelt und prüft weder fehlende Werte noch doppelte Daten (52.4) | Vorprüfung, ob der Datenvertrag beides ausschliesst; sonst an Fable |
| 6 | 02a, „Unsicher“ 4: ob `bestaetigung_ab_effektiv` (R37) den Beginn der Tage nach R64 für die Bestätigungsperiode verschiebt | Vorprüfung, dann an Fable |
| 7 | Benchmark-Datei: R39 nennt `<bot>.csv`, `auswertung.py:379` liest `<markt>.csv` (52.4) | Vorprüfung, dann an Fable |
| 8 | Von 51.10 sind Nr. 6 und Nr. 7 durch R63–R65 beantwortet; die Messung aus 51.10 Nr. 6 lebt in 52.5 Nr. 1 fort; 51.10 Nr. 1 bis 5 und Nr. 8 bleiben | wie dort |
| 9 | Marke an 7 (c) zu R64 (a): nicht gesetzt. Die Präzisierungen in Abschnitt 7 tragen die Regel selbst, und R61 (b) führt 7 (c) als Ort ohne Marke | nächste Anfrage an Fable |

## 53. Fable 02c — Registerblock R66–R73 (TB-132)

Reines Eintragen von Registertext, Bauart wie 52. Quelle ist allein `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md`, md5 `6aad30eca53d038b65f24577680f7774`, 30 216 B, im Repo seit Commit `57ae0d8`, Abschnitt „Registerblock — zeichengleich kopierbar (R66–R71 in der Fassung 02c, sie ersetzen die Fassung 02b vollständig; R72 und R73 neu)“, Z. 134–156. Sie ersetzt die Fassung der Blöcke R66–R71 aus der Antwort 02.10.b vollständig. Die Antwort 02.10.b (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md`) bleibt im Repo; ihre Blöcke sind nie eingetragen worden. Zum Dialog gehören ausserdem die Anfrage 02.10.b (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md`) und die Anfrage 02.10.c (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md`). Die Antwortdatei 02.10.c hat der steuernde Chat am 02.10.2026 aus Fables Ablage übertragen, in zwei unabhängigen Abschriften, `cmp` gleich; die Bytegleichheit mit der Ablage ist nicht gemessen. Die Eröffnungstexte (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md`), die zwei Anfragen und die Antwort 02.10.b liegen seit `57ae0d8` im Repo; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Den Anfangsbestand des Chats hält R73 (53.8) fest: Die Antwort 02.10.c stammt aus dem Chat der Antwort 02.10.b. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Überschriften von 53.1, 53.4 und 53.7 sind am Ende gekürzt („…“, wie 47.4 und 48.7); der Block darunter steht vollständig. Die Nummern 53.1–53.8 hat der steuernde Chat vergeben (Auftrag TB-132, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind 21 Marken: die 20, die R70 (c) aufzählt, und eine an 23.3, Registertext 3b (c), die der steuernde Chat nach R65 (a) bestimmt hat (53.10 Nr. 8). Die Marken zur Tatsachennotiz in 23.3 stehen unter dem Blockzitat der Notiz (R70 (c), Vorbild 25.2). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke. Ohne Marke bleiben 7 (c), 17.5 und 50.7 Nr. 3 (R70 (b), Indexzeilen) sowie 24.2 und 29.3 (R70 (c)). Die Wiederholung der Probe in der Lock-Umgebung, die R71 und R72 vor dem Eintrag verlangen, ist in TB-132 vor diesem Eintrag gelaufen (53.9). Die Voraussetzungen und Tatsachen der Blöcke stehen mit Befund in 53.9; was offen bleibt, steht in 53.10. Die Vormessung des steuernden Chats liegt unter `docs/belege/TB-132/vormessung/`. 53.9 und 53.10 sind Text des steuernden Chats, nicht Fables.

### 53.1 R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des…

> R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des Falten-Sharpe). (a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots. (b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.] (c) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe gerechnet, die in die Falte fallen (2a; halboffen wie im Faltenplan), nicht nur über die Tage, an denen der Benchmark definiert ist. Ein Tag ohne Benchmark-Tag geht mit Rendite 0 ein. Dasselbe gilt für den Sharpe in der Zeile der Bestätigungsperiode, ab dem Tag nach R68. Der Zellen-Erzeuger bildet ihn mit der Sharpe-Funktion aus kennzahlen.py; sie ist die registrierte Definition (R50), ein zweiter Rechenweg wird nicht gebaut. [Voraussetzung, zu messen: dass der Aufruf mit 252 Perioden je Jahr, bei Krypto 365, die Formel aus 15.3 trifft; den Bezeichner trägt die Tatsachennotiz nach R50 (38.2).] (d) Auf den Tagen des Benchmarks stehen: der Drawdown der Nebenbedingung (24.2, R36), die mittlere Exposure (R64), Beta-Bereinigung und Calmar-Vergleich (7 (c)) und das Zufalls-Timing (R48 (g): dieselben Tage wie 7 (c)). Auf dem Kapitalpfad nach (a) steht der Falten-Sharpe und mit ihm die Selektionsstatistik (15.2). Diese Aufzählung ist abschliessend; sie legt die Tage keiner weiteren Kennzahl fest. Die DSR-Eingaben des Gewinners bildet der eingefrorene Code aus den Renditen der Beta-Bereinigung, also auf den gemeinsamen Tagen mit dem Benchmark; das ist die registrierte Definition (R50), Abschnitt 9 nennt keine Tage, und es ist kein Register-Code-Widerspruch. R64 bleibt unberührt. (e) Führt die Tagesreihe einer Zelle an einem Tag, der kein Benchmark-Tag des Bots ist (R72 (b)), eine Rendite ungleich 0 oder eine Exposure ungleich 0, ist das ein Befund über Erzeuger oder Daten, kein Ausgang (Bauart R33); ausgenommen ist der Tag aus der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in der Fassung R71. Der Zellen-Erzeuger prüft das im Lauf für jede Tagesreihe und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. Die zweite Voraussetzung aus R64 wird damit im Lauf geprüft. (f) Tatsachennotizen: Kein Code auf der Sperrliste oder im Laufbereich bildet den Falten-Sharpe aus der Tagesreihe oder rechnet ihn nach; die Sharpe-Funktion in kennzahlen.py hat heute keinen Aufrufer, auswertung.py liest netto_sharpe aus zellen.csv. Der Fall, dass der Benchmark nicht an allen Tagen einer Falte definiert ist, tritt in vier ersten Falten auf (33.2, 23.4). Der Sharpe im DSR steht auf den gemeinsamen Tagen, die Schwelle des DSR kommt aus der Selektionsstatistik auf allen Tagen; das gehört zum Nebenbefund der DSR-Einheiten (50.7 Nr. 3) und wird mit ihm vor dem Tag behandelt. Die DSR ist Bericht, nicht Tor (Festlegung 11).
> Quelle des Grundes: 1c im Wortlaut („aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung); 1a („Flache Tage stehen mit Rendite 0 in der Reihe“); 2a („Jeder Handelstag gehört zu der Falte, in die sein Datum fällt“); 29.3; 17.5 („Der Handelskalender kommt nicht aus einer Datei, sondern aus dem Paket“; „Umgebung, nicht Eingabe“); 3a („Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei“) mit 15.5, Lesart A („trägt für diese Tage 0 bei“); daraus der Schluss des Verfahrensprüfers, dass Nichtteilnahme in der Selektionsstatistik als 0 geführt und nicht ausgeschlossen wird (die Tatsachennotiz zu 1c spricht von Falten ohne Trade, nicht von Tagen ohne Benchmark); 23.2, Grund 2 (der Schaden dort entsteht aus dem Vergleich zweier Reihen; der Falten-Sharpe hat eine); 24.1 und 24.2 (Bewertungsachse; die Zeitachse ist für den Drawdown genannt und bewegt ihn unter (e) nicht: 23.4, Wirkung 3); 23.3 (zur Entstehung: der Kapitalpfad hatte keinen Kalender); R50 („Der Registertext legt keine dieser Definitionen neu fest“); Abschnitt 9; R33; R64 (c); R46; die Messungen des steuernden Chats zur Anfrage 02.10.c, Fragen 1 und 2 (vom Verfahrensprüfer nicht gemessen). Bekannte Richtung der Wirkung, nicht Grund: Über alle Tage der Falte ist der Falten-Sharpe dem Betrag nach nie grösser als über die Benchmark-Tage allein, bei gleichem Vorzeichen (Rechnung des Verfahrensprüfers); die Grösse ist nicht gemessen und für die Entscheidung ohne Belang (Bauart 24.3). Kein Ergebnis.

> ⭐ **53.1 R66 PRÄZISIERT durch R74 (54.1)** (Fable 04a R74, TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.1 R66 PRÄZISIERT durch R78 (55.1)** (Fable 07a R78, Unterpunkt (a), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.1 R66 ERGÄNZT durch R81 (55.4)** (Fable 07a R81, Unterpunkte (e) und (g), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 15.3 (a); 15.3 (c); 52.2 (R64); 52.4, Zeile „R64 (52.2), zweite“. Indexzeilen ohne Marke (R70 (b)): 17.5; 50.7 Nr. 3. Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 1, 5 und 7.

### 53.2 R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen)

> R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen). In jeder Tagesreihe (tagesreihen/<zelle>.csv) und in jeder Benchmark-Tagesreihe (benchmark_tagesreihen/<bot>.csv) ist datum eindeutig, kein Feld leer und jeder Zahlenwert endlich. Ein flacher Tag trägt 0, nie nichts (1a). Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33): Der Zellen-Erzeuger prüft jede dieser Dateien im Lauf, nachdem er sie geschrieben hat, und endet sonst mit 2. Die Abnahme nach R46 prüft die Wache mit Gegenprobe, je für ein doppeltes Datum, ein leeres Feld und einen nicht endlichen Wert; der registrierte Lauf trägt die Wache selbst. auswertung.py wird dafür nicht geöffnet. Für zellen.csv gilt R33.
> Quelle des Grundes: R33 („Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang“; „nie nichts“), R39 (die Feldliste jeder Ausgabe ist Registertext), R64 (c) (Bauart), R46, die Messung in 52.4 (lies_tagesreihe, lies_benchmark und beta_bereinigung behandeln und prüfen weder fehlende Werte noch doppelte Daten). Kein Ergebnis.

> ⭐ **53.2 R67 ERGÄNZT durch R78 (55.1) und R82 (55.5)** (Fable 07a R78, Unterpunkt (e), und R82, TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 48.7 (R39). Offen: 53.10 Nr. 5.

### 53.3 R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv)

> R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv). (a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). Die Spanne bleibt, was 35.1 sagt; ihre Tage vor diesem Tag gehören weder zu einer Selektionsfalte noch zur Bestätigungsstatistik. (b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil. (c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure. (d) Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe (16.6: „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“). Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b) als Frage an den Verfahrensprüfer. Tatsachennotiz: Die Fassung von 2d in 15.4 (d) („Tage im Embargo gehören zu keiner Periode“) ist durch 16.6 vollständig ersetzt und trägt diesen Block nicht.
> Quelle des Grundes: R37 (i) („Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist“; „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“), R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen), 16.6 (Attribution je Position), R64 (a), R63 (d) (Bauart: Exposure aus derselben Rechnung wie die MtM-Reihe), die Messung des steuernden Chats zur Anfrage 02.10.c, Teil 0 Nr. 2. Kein Ergebnis.

> ⭐ **53.3 R68 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 48.1 (R33); 48.5 (R37); 52.2 (R64). Tatsache gemessen: 53.9. Offen: 53.10 Nr. 2 und 5.

### 53.4 R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2)…

> R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2) und R60 (c) (51.5). (a) Dass auswertung.py benchmark_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50). Er wird zugunsten von R39 aufgelöst; R39 ist damit bestätigt und wird nicht berichtigt. Die Benchmark-Reihe unterscheidet sich je Bot (23.3; 16.7 (b)); eine Datei je Markt kann sie nicht tragen. (b) Vor dem signierten Tag liest auswertung.py die Datei unter dem Namen des Bots. Das ist eine beauftragte Änderung nach 37.3 (Auftrag, Freigabe, alter und neuer Hash) mit neuem Abbild und einem Nachweis mit Gegenprobe (Bauart R55, R64). Sie gehört zur planmässigen Öffnung von auswertung.py, die R36 (zwei Drawdown-Spalten, Nachrechnung), R37 (bestaetigung_ab_effektiv), R34 (zellenbericht.csv) und R55 (Umbenennung) verlangen. Beispieldaten und Tests, die den Namen je Markt schreiben oder lesen, folgen in derselben Änderung. (c) In R64 (e) lies „auswertung.py wird für nichts davon geöffnet“ als „für nichts, was dieser Block in (a) bis (d) regelt, wird auswertung.py geöffnet“. „Dafür“ in R60 (c) bindet ebenso nur die Gleichheit der zwei Träger. Die Öffnung nach (b) berührt beides nicht.
> Quelle des Grundes: R39 mit seinem Grund (23.3: die Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot), 37.3, R45 (Bauart einer beauftragten Änderung), R36, R37, R34, R55, 50.1 und 50.2 (Stand des Vertrags), die Messung des steuernden Chats zur Anfrage 02.10.c, Teil 0 Nr. 1 (auswertung.py kennt weder zellenbericht noch kapital_drawdown_mtm_pct noch bestaetigung_ab_effektiv). Bauart, nicht Quelle: 23.5 („ein Name, der etwas anderes verspricht als das Verhalten“, dort zu einem Docstring). Kein Ergebnis.

> ⭐ **53.4 R69 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (h), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 48.7 (R39); 51.5 (R60); 52.2 (R64); 52.4, Zeile „R64 (52.2) (a)“. Tatsache gemessen: 53.9. Offen: 53.10 Nr. 4.

### 53.5 R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3)

> R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3). (a) 7 (c) trägt keine Marke zu R64. Abschnitt 7 nennt seine Tage selbst („gemeinsame Tage“, „über dieselben Tage“); R64 gibt das „lies“ R48 (d) und R60 (c), nennt 7 (c) als Geltungsbereich und bestätigt in (b) den Code, nicht den Wortlaut von 7. Ein Ort, den ein Block nur als Geltungsbereich einer Regel nennt, deren „lies“ einem anderen Ort gilt, bleibt ohne Marke und wird vom Index geführt, wie R54 an 7 (c) (R61 (b)). Nennt der Wortlaut eines Ortes die Sache nicht und gibt der Block sie ihm, trägt der Ort die Marke: so 4.2 zu R64, 15.3 (a) zu R66 und 48.1 zu R68. (b) Indexzeilen ohne Marke: 7 (c) — mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). 17.5 — Handelskalender der Aktien-Tagesreihe, R66 (a) und (b). 50.7 Nr. 3 — Tagesbasis des DSR, R66 (f). (c) Marken zu dieser Antwort, der alte Satz bleibt zeichengleich: 15.3 (a) — PRÄZISIERT durch R66, Unterpunkte (a) und (b). 15.3 (c) — PRÄZISIERT durch R66, Unterpunkt (c). 48.1 (R33) — PRÄZISIERT durch R68. 48.5 (R37) — PRÄZISIERT durch R68. 48.7 (R39) — ERGÄNZT durch R67; ERGÄNZT durch R69: R39 ist bestätigt. 48.16 (R48 (d)) — ERGÄNZT durch R72, Unterpunkt (c). 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c). 51.6 (R61) — PRÄZISIERT durch R70, Unterpunkt (a). 52.2 (R64) — ERGÄNZT durch R66 (zu (e)), PRÄZISIERT durch R68, durch R69, Unterpunkt (c), und durch R71 und R72, Unterpunkt (b) (Benchmark-Tag; erster Kurstag). 52.3 (R65) — PRÄZISIERT durch R70, Unterpunkt (a). 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66, Unterpunkte (a) und (e). 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69, Unterpunkt (c). 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71 und ERGÄNZT durch R72; die Marke steht unter dem Blockzitat der Notiz (Vorbild 25.2). 27 — ERGÄNZT durch R73. Ohne Marke bleiben 24.2, 29.3 und 7 (c) zu R66 (Geltungsbereich oder Quelle des Grundes).
> Quelle des Grundes: R61 (b), erster und zweiter Satz, und die Zeile „R54 an 7 (c)“; R65 (a) (auch: eine Tabelle von Befunden ist keine Statusliste; eine Bestätigung trägt ERGÄNZT mit Zusatz); 34 (Kopf: die Marke steht am alten Ort; nach der Wiedergabe in R61 und R65); Wortlaut von Abschnitt 7, 4.2, 15.3 (a) und R33. Kein Ergebnis.

> ⭐ **53.5 R70 PRÄZISIERT durch R77 (54.4)** (Fable 04a R77, Unterpunkt (b), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 51.6 (R61); 52.3 (R65). Nach (c) gesetzt: 20 Marken, je in der Kette des Blocks, der sie auslöst. Indexzeilen ohne Marke nach (b): 7 (c); 17.5; 50.7 Nr. 3. Offen: 53.10 Nr. 8 und 9.

### 53.6 R71 — Berichtigung der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in 23.3 (welcher Tag ausgelassen wird)

> R71 — Berichtigung der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in 23.3 (welcher Tag ausgelassen wird). „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil pct_change dort keine Rendite liefert“ lies „Die Umsetzung lässt den ersten Kurstag ab dem frühesten Handelbar-Tag des Bots aus, weil pct_change dort für kein Symbol eine Rendite liefert; das geschieht einmal je Bot, nicht in jeder Falte, und der Tag fällt nur dann in eine Falte, wenn er nicht vor der ersten Falte des Bots liegt“. Der Satzteil „höchstens ein Tag je Falte“ bleibt als Schranke richtig; die übrigen Sätze der Notiz bleiben. R64 (a) („erster Kurstag“) und R66 (e) meinen diesen Tag. Gemessen ist das an einer Probe mit synthetischen Kursen unter pandas 2.3.3, ausserhalb der Lock-Umgebung. [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; weicht sie ab, wird gemeldet, nicht eingetragen.]
> Quelle des Grundes: 23.4, Wirkung 3 (unter C_lit ändern sich vier Falten um je einen Tag, „der Tag des ersten Kurses, an dem noch keine Rendite vorliegt“, nicht jede Falte); 23.5 („die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag“); die Probe des steuernden Chats zur Anfrage 02.10.c, Frage 4 (vom Verfahrensprüfer nicht gemessen). Kein Ergebnis.

**Kette:** Marken: 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 52.2 (R64). Voraussetzung gemessen: 53.9.

### 53.7 R72 — Tatsachennotiz zu Registertext 3b (c) (23.3) (Kurslücke und Reihenende im Benchmark) und Ergänzung zu R48 (d) (48.16)…

> R72 — Tatsachennotiz zu Registertext 3b (c) (23.3) (Kurslücke und Reihenende im Benchmark) und Ergänzung zu R48 (d) (48.16) (Bewertung am Lückentag). (a) Unter der registrierten Umgebung (17.5) schreibt bh_tagesrenditen den letzten Kurs eines Symbols fort: An einem Tag, an dem ein handelbares Symbol keinen Kurs trägt und ein anderes handelbares einen trägt, geht das Symbol mit Rendite 0 in das Mittel ein, am nächsten Kurstag mit der Rendite über die Lücke. Das ist, was der Code tut, und kein Widerspruch zu 3b (c): Das Symbol bleibt nach 3b (b) handelbar, und der Bot kann es über die Lücke halten. (b) Benchmark-Tag des Bots im Sinn von 23.3, R64 und R66 ist ein Tag, an dem mindestens ein nach 3b (b) handelbares Symbol des Bots einen Kurs trägt; ausgenommen ist der Tag aus R71. Ein Handelstag, an dem kein handelbares Symbol einen Kurs trägt, ist kein Benchmark-Tag. (c) Der Zellen-Erzeuger bewertet eine offene Position an einem Tag ohne Kurs ihres Symbols zum letzten Kurs; die Position trägt an diesem Tag Rendite 0 und bleibt in der Exposure. Er berichtet je Bot die Zahl solcher Positionstage (Bauart 24.6). Bot und Benchmark werden am Lückentag damit gleich bewertet. (d) Nach dem letzten Kurs eines Symbols führte derselbe Code das Symbol an jedem Folgetag mit Rendite 0 im Mittel weiter. Das wäre mit 3b (c) nicht vereinbar: Ein Symbol ohne weitere Kurse gehört nicht mehr zu der Menge, in der der Bot lebt. Am Bestand vom 02.10.2026 endet keine Reihe früher. Vor dem signierten Tag wird am Snapshot gemessen (Verfahrensmessung nach 27.2), dass keine Kursreihe eines Symbols der zwei Universumsdateien vor dem letzten Kurstag ihres Marktes endet, und wie viele Symbol-Tage Lücke im Zeitraum nach R66 (a) liegen. Endet eine Reihe früher, wird gemeldet und vor dem Tag entschieden. benchmark.py wird für nichts in diesem Block geöffnet. (e) Das Verhalten nach (a) hängt an der pandas-Fassung des Locks: Gemessen füllt 2.3.3 auf, 3.0.5 nicht. Die Prüfung der Umgebung nach 5f deckt das im Lauf. Eine Änderung der pandas-Fassung im Lock vor dem Tag verlangt die Wiederholung der Probe; weicht das Verhalten ab, wird gemeldet. [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c).]
> Quelle des Grundes: 23.3 („nur eines darf im Register stehen, und es muss das sein, was der Code tut“; „Bot und Benchmark leben an jedem Tag in derselben Menge“; „handelbar“ nach 3b (b)); 23.4 („der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen Kurs hat“); 23.2 (die Menge, in der ein Bot lebt); 17.5 (registrierte Umgebung, Abbruch bei Abweichung); 24.6 (Bauart: fortgeschriebene Kurstage werden gezählt); R48 (d) (bewertet wie die MtM-Reihe); die Probe und die Zählung des steuernden Chats zur Anfrage 02.10.c, Frage 4 (vom Verfahrensprüfer nicht gemessen). Kein Ergebnis.

> ⭐ **53.7 R72 PRÄZISIERT durch R78 (55.1)** (Fable 07a R78, Unterpunkte (a) bis (d) und (f), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.7 R72 BERICHTIGT durch R78 (55.1)** (Fable 07a R78, Unterpunkt (g), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.7 R72 ERGÄNZT durch R79 (55.2)** (Fable 07a R79, Unterpunkt (c), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 23.3, Registertext 3b (c) (vom steuernden Chat bestimmt, 53.10 Nr. 8); 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 48.16 (R48); 52.2 (R64). Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 3, 5, 6 und 10.

### 53.8 R73 — Tatsachennotiz zu 27 nach R56 (c) (die Antwort 02c stammt aus dem Chat der Antwort 02b)

> R73 — Tatsachennotiz zu 27 nach R56 (c) (die Antwort 02c stammt aus dem Chat der Antwort 02b). Die Eröffnung 02.10.c war für einen neuen Chat geschrieben und kam als zweite Nachricht in dem Chat an, der am 02.10.2026 die Antwort 02b geschrieben hat. Der Betreiber hat am 02.10.2026 per Auswahlkarte entschieden, dass dieser Chat antwortet; die Chatgrösse war dabei gemessen 351 798 und lag über der Umzugsschwelle. Der Anfangsbestand dieses Chats ist der Eröffnungstext 02.10.b und das Leseprotokoll der Antwort 02b; beim Schreiben von 02c kannte er darüber hinaus alles, was das Leseprotokoll von 02b nennt, den eigenen Verlauf zu 02b und die Abschnitte 9, 16 und 17, vollständig gelesen. Eine Verdichtung des Chats hat der Verfahrensprüfer nicht bemerkt. Er hat keinen Helfer und keinen Suchlauf benutzt. Weitere Grössen nach 27.1, als die Leseprotokolle von 02b und 02c nennen, kennt er nicht.
> Quelle des Grundes: R56 (a) bis (c), 27.4, Leseprotokolle 02b und 02c. Kein Ergebnis.

**Kette:** Marken: Abschnitt 27. Keine Voraussetzung (53.9).

### 53.9 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02c „zu messen“ nennt, und zu den Tatsachen, die die Blöcke über Code und Daten führen. Gemessen am 02.10.2026 am Stand `0779453`, nur lesend, durch Helfer des steuernden Chats; die Berichte liegen unter `docs/belege/TB-132/vormessung/` (`v1_register.md` bis `v5_code_02c.md`, dazu zwei Proben und die zwei Ausgaben der Probe zu R71). Die Sitzung TB-132 hat in Schritt 0 die genannten Zeilen und Zählungen an Code und Register am Commit `57ae0d8` nachgemessen (`docs/belege/TB-132/0d_vorpruefung.txt`) und die Probe zu R71 in der Lock-Umgebung wiederholt. Die Zählungen am Datenbestand und die Kalendervergleiche hat sie nicht wiederholt. Zeilenangaben zum Code gelten am Commit `57ae0d8`. „REG Z.“ nennt Registerzeilen am Stand `ad351d5`, also vor diesem Eintrag. Aussagen über ein Fehlen (kein Aufrufer, kein Kalender im Lauf, kein Zellen-Erzeuger) sind Lesung der Helfer, soweit keine Zählung genannt ist. Gezählt sind Datumszeilen, Zeilennummern und Fassungen. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R66 (53.1) (b) | welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | Das Paket `pandas_market_calendars` importiert im Repo nur `notifications/boersenkalender.py` (Z. 81); dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). Die Datei steht nicht auf der Sperrliste und nicht im Laufbereich, weder in `ARBEITSBAUM_PFADE` (`shared/paths.py:239–253`) noch in der gemessenen Hülle (`docs/belege/TB-112/a2_laufbereich.txt`, 84 Pfadzeilen, davon 3 Messumschläge). `shared/entscheidungskerze.py` erreicht sie in Z. 384 (`import boersenkalender`). Diese Datei zählt über den Ordner `shared` zu `ARBEITSBAUM_PFADE`; zur gemessenen Hülle zählt sie nicht. Importiert wird sie von den neun `strategies/*/forward_test.py`, von Tests und von Forschungsskripten, von keinem Modul der gemessenen Hülle: Der Aufruf kommt aus dem Live-Pfad, nicht aus dem Selektionslauf. In den Pfaden der Hülle und in den neun Dateien der Sperrliste und der Gruppe „eingefroren“ steht kein Import und kein Aufruf des Pakets (vier Treffer der Suche in der Hülle sind Kommentar oder Docstring). Das Feld `kalender` aus TB-47 (`research/snapshotgrenze/erhebung_eingaben.py:606–610`) führt Importstellen und Paketfassung, keinen Kalendernamen; 17.5 nennt keinen. Am Bestand vom 02.10.2026 (nur Datumsspalten, nicht der Snapshot des Laufs): 16 275 Kurstage des Aktienmarktes von 1962-01-02 bis 2026-09-01; gegen den Kalender „NYSE“ des Pakets (4.6.1) 0 Tage nur im Kalender und 0 Tage nur in den Daten. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche sind Ersatzmessungen ausserhalb der Lock-Umgebung: Python 3.10 und pandas 2.3.3 des Systems, die Kalenderpakete in den Fassungen des Locks aus `trading-env` | nicht entscheidbar: Der Code des Laufs benutzt heute keinen Kalender; welchen Namen der Zellen-Erzeuger nimmt, ist offen (53.10 Nr. 1). Die Wache nach R66 (b) prüft die Wahl im Lauf |
| R66 (53.1) (c) | dass der Aufruf mit 252 Perioden je Jahr, bei Krypto 365, die Formel aus 15.3 trifft | `research/vorregistrierung/kennzahlen.py:95–108` (`sharpe`) rechnet `s = float(np.std(r, ddof=1))` (Z. 105) und gibt `float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)` zurück (Z. 108); Standardabweichung 0 oder weniger als zwei Werte ergeben 0. Formel im Register: REG Z. 1449–1450; 1c: REG Z. 1442–1443. Registrierte Konstante ist `registerdaten.py:109` `HANDELSTAGE_JE_JAHR = 252`; die 365 steht als Literal in `auswertung.py:264–265` | trifft für die Funktion; einen Aufruf gibt es noch nicht (der Zellen-Erzeuger fehlt). Den Nenner der Standardabweichung nennt das Register nicht; der Code legt n − 1 fest (R50). Ein nicht endlicher Wert in der Reihe ergäbe still 0; R67 schliesst ihn aus |
| R66 (53.1) (f) | Tatsachen im Block, keine Voraussetzung | `sharpe` (`kennzahlen.py:95–108`) hat keinen Aufrufer in `research/vorregistrierung`, `shared`, `strategies` und `docs/belege` (Suche nach `kz.sharpe(`, `kennzahlen.sharpe(` und `sharpe(`: nur die Definition); `sharpe_fn=` in `beispieldaten.py` (Z. 144, 180) und in den Tests reicht andere Funktionen weiter (`standard_sharpe`, Lambdas), nicht `kennzahlen.sharpe`; `auswertung.py` liest `netto_sharpe` nur aus `zellen.csv` (Z. 353–354, 395, 577, 622–623, 684); `bootstrap` 0 Treffer in `research/vorregistrierung/*.py`. DSR: `auswertung.py:670` mit den Renditen aus `beta_bereinigung` (Schnitt Z. 517, Fenster Z. 511), `kennzahlen.py:219–246`; die Schwelle des DSR kommt aus der Varianz der Selektionsstatistik über die Zellen (`auswertung.py:587–588`). Vier erste Falten: 33.2 (REG Z. 5972, 5973, 5975 und 5976), 23.4 (REG Z. 4009–4014) | trifft |
| R68 (53.3) (b) | Tatsache im Block („auswertung.py liest sie für kein Urteil“) | `mittlere_exposure` wird in `auswertung.py` an zwei Stellen gelesen: Z. 405 in `zulaessigkeit`, nur über die Selektionsfalten (Z. 403); Z. 626 in `bestaetigungsperiode`, nur für den Bericht (Z. 728) | trifft |
| R69 (53.4) | Tatsache in der Quelle des Grundes (was `auswertung.py` nicht kennt) | `zellenbericht` 0 Treffer in `auswertung.py`; `kapital_drawdown_mtm_pct` und `bestaetigung_ab_effektiv` 0 Treffer in allen `*.py` des Repos (ohne `ergebnisse/` und `trading-env/`); `kapital_drawdown_pct` in `auswertung.py` Z. 40, 134, 413–414, 625, 681–682 und 824; `auswertung.py:379` liest `f"{markt}.csv"` | trifft |
| R71 (53.6) | die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; weicht sie ab, wird gemeldet, nicht eingetragen | `docs/belege/TB-132/vormessung/r71_probe.py`, in TB-132 vor diesem Eintrag mit dem Python der Lock-Umgebung (`trading-env/bin/python3`) wiederholt; die Ausgabe liegt unter `docs/belege/TB-132/probe_lock_r71.txt` und ist ab der Zeile „A - Faelle …“ zeilengleich mit `docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt` | trifft (Rückgabewert 0; bei Abweichung wäre dieser Abschnitt nicht entstanden) |
| R72 (53.7), erste | die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner | dieselbe Probe; die Ausgabe zeigt das Fortschreiben an der Lücke und nach dem Reihenende, wie (a) und (d) es beschreiben. Unter pandas 3.0.5 (`docs/belege/TB-132/vormessung/ausgabe_pandas_3.0.5.txt`) füllt `pct_change()` nicht auf | trifft |
| R72 (53.7), zweite | dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c) | Einziger vorhandener Kern für eine tägliche MtM-Reihe ist `research/mtm_drawdown/mtm_kern.py`; Z. 166–168 schreibt den letzten Kurs fort (`eigene.ffill()`), Z. 244–247 lässt die Position in `n_offen` und `gebunden` und zählt den Positionstag in `fortgeschrieben`. Probe auf synthetischen Daten (`docs/belege/TB-132/vormessung/p3_probe.py`, pandas 2.3.3, ausserhalb der Lock-Umgebung): Änderung 0 am Lückentag. `exposure_kern.py`, `bot_lauf.py` und der Zellen-Kern nach R43 bewerten nicht täglich. Daneben steht eine Näherung, `research/exposure_messung/auswertung.py::mtm_reihen` (Z. 305–341): Sie schreibt am Lückentag ebenfalls fort (Z. 323), füllt aber vor dem ersten Kurs rückwärts auf und überspringt ein Symbol ohne Kursreihe (Z. 321–322) | trifft für diesen Kern. Nicht von selbst erfüllt: `tagesraster` (Z. 135–148) lässt einen Tag aus, an dem kein übergebenes Symbol einen Kurs hat (das Raster nach R66 (a) gibt der Erzeuger); `gebunden` steht zum Einstand. Welchen Kern der Zellen-Erzeuger übernimmt, legt kein Registertext fest |
| R72 (53.7) (d) | Tatsache im Block („Am Bestand vom 02.10.2026 endet keine Reihe früher“) | Am Bestand (nur Datumsspalten; Dateien vom 02.09.2026 und 15.09.2026): Krypto, je Bot 24 Symbole, 2017-08-17 bis 2026-09-14: keine Lücke, kein Tag ohne jedes Symbol, keine früher endende Reihe, kein doppeltes Datum. Aktien, 150 Symbole: zwei Symbol-Tage Lücke (1974-06-03 `LMT`, 2026-08-10 `MNST`), keine früher endende Reihe, kein doppeltes Datum. Nicht gemessen: Zeilen ohne `close`, der Handelbar-Schnitt je Bot | trifft |
| R73 (53.8) | keine Voraussetzung | Die Angaben sind die des Verfahrensprüfers; der steuernde Chat kann sie nicht messen. Der Eröffnungstext 02.10.c (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md`) liegt im Repo; er war nicht Anfangsbestand | Tatsachennotiz des Verfahrensprüfers |
| R66–R73, Zitate und Verweise | — | 98 Stellen gegen den Wortlaut gemessen (`docs/belege/TB-132/vormessung/v4_register_02c.md`). Sinngemäss treffen zehn: R72 (b) fasst den Benchmark-Tag enger als der Wortlaut von 23.3 (REG Z. 3933–3936), das ist der Inhalt der Präzisierung; R72 nennt im Kopf den Registertext 3b (c), R70 (c) setzt die Marke nur an die Tatsachennotiz (53.10 Nr. 8); „TB-47, Feld kalender“ steht nur in der Erläuterung unter 17.5 (REG Z. 2847); „Dafür“ steht in R60 (c) klein (REG Z. 11196); „Bauart R55, R64“ in R69 (b) meint Prüfungen mit Gegenprobe, die Bauart der beauftragten Änderung steht in R45 (REG Z. 10857); von einer Öffnung spricht unter R36, R37, R34 und R55 nur R55; „R54 an 7 (c)“ ist in R61 (b) ein Glied der Aufzählung, keine Zeile (REG Z. 11209); 24.6 (REG Z. 4471) berichtet eine Zählung in einer Messung; R56 (c) (REG Z. 11168) nennt drei Fälle, der von R73 ist keiner davon; 23.2, Grund 2 (REG Z. 3908) ist Deutung des Verfahrensprüfers | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (53.10 Nr. 9) |

> ⭐ **53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (b) und (f), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.9, Zeile „R72 (53.7), zweite“ ERGÄNZT durch R78 (55.1) und R83 (55.6)** (Fable 07a R78, Unterpunkt (a), und R83, Unterpunkt (e), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **53.9, Zeile „R72 (53.7) (d)“ ERGÄNZT durch R79 (55.2) und R78 (55.1)** (Fable 07a R79, Unterpunkt (c), und R78, Unterpunkt (d), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 53.10 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | Kalendername für die Aktien-Tagesreihe (R66 (a), (b)): Der Code des Laufs benutzt keinen; im Repo steht nur „NYSE“ im Live-Pfad (53.9) | nächste Anfrage an Fable |
| 2 | Deckelfall (R68 (d)): Behandlung in den Gleichheitsproben nach R60 (c) und R64 (d) und in der Nachrechnung nach R36 | Frage an Fable vor der Öffnung nach R69 (b) |
| 3 | Verfahrensmessung am Snapshot (R72 (d)): keine Kursreihe endet vor dem letzten Kurstag ihres Marktes; Zahl der Symbol-Tage Lücke im Zeitraum nach R66 (a) | vor dem signierten Tag |
| 4 | Planmässige Öffnung von `auswertung.py` (R69 (b)): Dateiname je Bot, mit R36, R37, R34 und R55; Beispieldaten und Tests folgen | eigener Umsetzungsauftrag mit Freigabe, vor der Abnahme nach R46 |
| 5 | Zellen-Erzeuger: Kalender und Raster nach R66 (a); Wachen nach R66 (b), R66 (e) und R67; Falten-Sharpe über die Sharpe-Funktion aus `kennzahlen.py` (R66 (c)); Bewertung am Lückentag und Zahl der Positionstage je Bot (R72 (c)); Zeile der Bestätigungsperiode nach R68 | mit dem Zellen-Erzeuger, Abnahme nach R46 |
| 6 | Wiederholung der Probe bei einer Änderung der pandas-Fassung im Lock (R72 (e)) | bei Anlass, vor dem Tag |
| 7 | Tagesbasis des DSR (R66 (f)): gehört zum Nebenbefund 50.7 Nr. 3 | vor dem Tag |
| 8 | Marke an 23.3, Registertext 3b (c): PRÄZISIERT durch R72 (b). R70 (c) nennt sie nicht; der steuernde Chat hat sie nach R65 (a) bestimmt | nächste Anfrage an Fable, zur Kenntnis |
| 9 | Die sinngemässen Verweise aus 53.9 (letzte Zeile) | nächste Anfrage an Fable, zur Kenntnis |
| 10 | `tagesschluss` (`benchmark.py:155`, `159–160`) normalisiert `open_time` nicht und prüft keine doppelten Daten; am Bestand vom 02.10.2026 folgenlos | mit der Verfahrensmessung nach Nr. 3 |

Von 52.5 sind damit erledigt: Nr. 2 durch R66 (a) und (c), Nr. 5 durch R67, Nr. 6 durch R68 (a) und (b), Nr. 7 durch R69, Nr. 9 durch R70 (a). Nr. 1 (zweite Voraussetzung zu R64) wird nach R66 (e) im Lauf geprüft. Nr. 3 bleibt; der Deckelfall (R68 (d), hier Nr. 2) berührt die Probe dort. Nr. 4 und 8 bleiben, wie sie dort stehen.

