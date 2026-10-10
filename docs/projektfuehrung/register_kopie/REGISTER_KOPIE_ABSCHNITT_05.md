# REGISTER-KOPIE Abschnitt 5 (von 0–56) — Register-Z. 588–749 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 5. Der Faltenplan

### 5.1 Die Regeln

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026), Registertext 0, 2 und 4.**
> Der Text bleibt hier stehen — der Verlauf soll lesbar bleiben; das ist der
> Sinn eines Registers. Massgeblich ist der Nachtrag.
> Betroffen sind **Nr. 1** (verankert, expandierend), **Nr. 2** (Aktien: Training
> mindestens vier Jahre), **Nr. 3** zusammen mit 5.3 (Krypto-Platzhalter) und
> **Nr. 5** (Purge und Embargo zwischen den Falten). Sie stammen aus **Verfahren A**
> (faltenweise Auswahl mit Trainingsfenster); es gilt **Verfahren B** — eine
> einmalige Auswahl über das ganze Raster, ohne Trainingsfenster.
> **Unberührt** bleiben Nr. 4 (2020 und 2022 sind keine Trainingsjahre — unter
> Verfahren B gibt es gar kein Training), Nr. 6 (Faltenlänge, siehe 5.4),
> Nr. 7 (die letzte Falte ist die Bestätigungsperiode) und Nr. 8 (Falten ohne
> Trade zählen mit Sharpe 0 — Registertext 1c schärft das nur nach).

1. **Verankert, expandierend** (nicht rollierend). Das Training beginnt immer
   am Datenbeginn und endet am Faltenrand, abzüglich der Purge-Länge. Ein
   Verfahren, das alte Jahre vergisst, wählt im Zweifel die Parameter des
   letzten Marktzustands.
2. **Aktien:** Testfalten sind die Kalenderjahre **2019 bis zum
   Go-Live-Schnitt**, Training ab Datenbeginn, mindestens **vier Jahre** vor
   der ersten Falte.
3. **Krypto: Platzhalter mit Regel, keine Jahreszahlen** — siehe 5.3.
4. **2020 und 2022 sind Testfalten, keine Trainingsjahre.** Der Satz steht
   hier, weil dies die einzige Stelle wäre, an der die Versuchung entstünde,
   ein schweres Jahr ins Training zu schieben. `test_vorregistrierung.py`
   Teil G prüft es maschinell.

   > ⭐⭐ **`G6` liest diese Zeile maschinell — Wortlaut nicht ändern (40.2,
   > Fable 24a, TB-96, 24.09.2026).** `test_vorregistrierung.py`
   > (`_testjahre_aus_register`, Teil G) sucht im ganzen Register genau eine
   > Zeile, die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**`
   > beginnt, und liest die Jahre daraus. Umformuliert — auch nur Satzzeichen
   > oder Hervorhebung — oder eine zweite Zeile mit diesem Anfang ⇒ `None` ⇒
   > `G6` rot für alle neun Bots. Eine Änderung der Sache braucht einen eigenen
   > Registereintrag **und** die Anpassung von `G6` im selben Auftrag.

   > ⭐ **Zwei Leser, ein Parser (41.1 A6, Fable 24b, TB-108, 25.09.2026):**
   > Diese Zeile lesen seit TB-97 **zwei** Stellen — `G6` in
   > `test_vorregistrierung.py` und die Krisenfalten in `beispieldaten.py` —
   > über **eine** Funktion, `beispieldaten.py::jahre_aus_register_5_1_nr_4`.
   > Ein zweiter Parser derselben Zeile wäre ein zweiter Ort (Fable 24b B4).
   > Die Warnung oben gilt für beide Leser.

5. **Purge und Embargo** in Höhe der **maximalen gemessenen Haltedauer** des
   Bots, aus `research/tb24_haltedauern/`. Purge: der Rand vor der Falte
   fällt aus dem Training. Embargo: nach dem Ende einer Falte fällt dieselbe
   Länge aus dem Training aller **späteren** Falten — sonst lernt Falte *f+1*
   auf Positionen, die in Falte *f* noch offen waren.
6. **Faltenlänge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je
   Jahr.** Welche Bots das trifft, steht vorher fest (5.4).
7. **Die letzte Falte wird NICHT selektiert.** Sie ist die
   **Bestätigungsperiode**: einmal ausgewertet, nachdem die Auswahl steht,
   berichtet wie sie ausfällt. Kein Veto, aber die einzige Zahl ohne
   Selektion. **Und sie wächst jeden Monat.**

> ⭐ **5.1 Nr. 7 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

8. **Falten ohne Trade zählen mit Sharpe 0.** *„Auslassen belohnt Sätze, die
   in schweren Jahren nicht handeln."*

   > ⭐ **Null Trades ist ein Wert — auch für den Lauf (43.2, 43-7, Fable 25e,
   > TB-110, 26.09.2026):** Aus Nr. 8 und 1c (15.3) folgt für jeden Lauf des
   > Laufbereichs: Findet oder führt er keine Trades aus, schreibt er dieses
   > Ergebnis und endet mit 0; er endet nie ohne Ausgabe. Unter dem Modus endet
   > ein `exit()` ohne geschriebenes Ergebnis mit 2. Wortlaut in **43.2, 43-7**;
   > vollzogen an zehn Stellen in TB-109. Der Satz oben bleibt zeichengleich.

Zu 8 eine Eigenschaft, die auffallen sollte, bevor sie jemand für einen
Fehler hält: die Selektionsstatistik ist ein **Median**. Bei sieben
Selektionsfalten verschiebt eine einzelne gesetzte Null ihn oft gar nicht.
Das ist kein Grund, die Regel wegzulassen — sie wirkt, sobald mehrere Falten
leer bleiben, und das ist genau der Fall, den sie treffen soll.

### 5.2 Der Go-Live-Schnitt

**`2026-09-01`, ausschliesslich.** Alle neun Bots laufen seit Anfang
September 2026 im Paper-Trading; die Kursdateien dieses Repos enden am
2026-09-01 (Aktien) bzw. 2026-08-31 (Krypto). Alles davor ist
Backtest-Material, alles ab diesem Tag ist Forward-Test und geht in **keine**
Selektion ein — auch nicht in die Bestätigungsperiode.

> ⭐ **5.2 PRÄZISIERT durch R81 (55.4)** (Fable 07a R81, Unterpunkte (a), (b) und (f), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **5.2 ERGÄNZT durch R83 (55.6)** (Fable 07a R83, Unterpunkt (d), TB-139, 07.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 5.3 Krypto: Platzhalter mit Regel

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026), Registertext 3 und 4.**
> Der Text bleibt hier stehen — der Verlauf soll lesbar bleiben; das ist der
> Sinn eines Registers. Massgeblich ist der Nachtrag.
> Der Platzhalter ist eingelöst: die Krypto-Faltenpläne stehen im Nachtrag mit
> Jahreszahlen. Die hier zitierte Regel („mindestens vier Jahre Kursdaten je
> Symbol", point-in-time-Ausschluss) gilt **nicht mehr** — es gibt kein
> Mindesttraining, und kein Symbol wird aus einer Falte ausgeschlossen.

Die Kursdaten dieses Repos beginnen für Krypto am **2021-09-01**. Nach vier
Jahren Mindesttraining blieben **zwei** Testfalten — zu wenig für einen
Median über Falten. **TB-31** lädt die Historie über `/api/v3/klines` zurück.

**Der Krypto-Faltenplan wird geschrieben, sobald TB-31 gemeldet hat, ab wann
die Daten je Symbol reichen.** Bis dahin steht hier die Regel:

> Erste Testfalte ist das erste volle Kalenderjahr, vor dem **je Symbol**
> mindestens vier Jahre Kursdaten liegen, frühestens 2019. Danach lückenlose
> Falten der jeweiligen Länge bis zum Go-Live-Schnitt; die letzte Falte ist
> die Bestätigungsperiode. Ein Symbol geht in eine Falte nur ein, wenn seine
> Kursdaten mindestens vier Jahre vor Faltenbeginn einsetzen
> (point-in-time).

`auswertung.py` weigert sich, einen Bot mit Platzhalter-Faltenplan
auszuwerten — es gibt dann keine Zahl, die so tut, als gäbe es eine.

> ⭐ **5.3 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 5.4 Welche Bots Zweijahres-Falten bekommen

Gerechnet aus den **gefundenen** Trades je vollem Kalenderjahr
(`research/tb24_haltedauern/daten/<bot>_alle_trades.csv`). Gefunden, nicht
ausgeführt: ob ein Trade ausgeführt wird, hängt am Positionslimit — und das
ist in diesem Lauf ein Rasterparameter. Eine Faltenlänge, die vom
Positionslimit abhinge, wäre keine Festlegung vor dem Lauf.

Angeschnittene Randjahre zählen nicht mit; sie zögen die Trades je Jahr nach
unten und schöben einen Bot fälschlich in die Zweijahres-Falten.

**Ergebnis: genau ein Bot.** `elliott_wave` liegt bei **26,0** gefundenen
Trades je Jahr und bekommt Zweijahres-Falten; die übrigen acht liegen
zwischen 50,9 und 1.202,2. Die Zahlen stehen in der Faltenplan-Tabelle in
Abschnitt 3.

> ⭐⭐ **Eingabedateien nach 23d (40.6, Fable 24a, TB-96, 24.09.2026):** Die
> neun Listen oben (`78e2bc6`, 13.09.2026) sind Eingabe einer Herleitung von
> Registertext (33.2) und fallen unter 23d in voller Form. Sie werden vor dem
> Tag **einmal auf dem registrierten Snapshot mit dem registrierten Code neu
> erzeugt** (Erzeuger unter 36.1), kommen als Punkt auf die Sperrliste, und die
> Faltenlänge wird danach nach dieser Regel neu abgeleitet und gegen 33.2
> verglichen (TB-98). Die alten Listen bleiben als historischer Stand liegen.
> ⚠️ **Nicht registriert ist der Parameterstand, mit dem die Listen erzeugt
> wurden** — dieser Abschnitt nennt ihn nicht; die Neu-Erzeugung trägt ihn als
> Tatsachennotiz hierher (Parameterdateien, Commit, Snapshot, Modus, Hash je
> Liste). Die Schwelle selbst ist registriert (Festlegung 7, 5.1 Nr. 6). Der
> Regeltext oben bleibt zeichengleich.

> ⭐⭐ **Reichweite und `elliott_wave` (41.2 B1, 41.3 C4, Fable 24c/24d, TB-108,
> 25.09.2026):** Der Grundsatz dieses Abschnitts — keine Festlegung vor dem Lauf
> aus Grössen, die vom Positionslimit **oder von der Ausführung** abhängen — gilt
> für **alle** Festlegungen, die vor dem Lauf stehen (Faltenlänge, Purge,
> Embargo, Trainingsende, Rastergrenzen); Herleitungen aus Trades verwenden
> gefundene Trades (Registertext in **41.2, B1**). Bei `elliott_wave`, dessen
> Positionslimit keine Rasterachse ist (2.4), greift „gefundene" über die
> Ausführung (Kapitalschranke) — Tatsachennotiz in **41.3, C4**. Der Regeltext
> oben bleibt zeichengleich.

---

