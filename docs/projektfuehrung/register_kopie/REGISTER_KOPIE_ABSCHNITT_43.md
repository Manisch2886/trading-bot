# REGISTER-KOPIE Abschnitt 43 (von 0–52) — Register-Z. 9514–9830 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

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

