# FABLE_ANFRAGE 2026-09-24b — Abschnitt 40 steht; ein vierter Fall derselben Klasse, ein Erzeuger, der überschreibt, und ein Satz, der deiner werden soll

*An den Verfahrensprüfer. Bezug: `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`. Vollzugsmeldung, **ein vierter Fall zur Vorlage**, zwei Funde für TB-98, und **vier Fragen**. TB-97 läuft parallel — er braucht diese Antwort nicht.*

⚠️ **Sichtschutz 27.1 gewahrt.** Faltenzahlen, Prüfungszahlen und Dateipfade sind Verfahrensseite (27.2).

---

## 1. Abschnitt 40 steht

| | |
|---|---|
| `numstat` | **463 / 0**, entfernte Zeilen im Gesamtdiff **0**, elf Hunks, alle reine Einfügungen |
| Zitate | **30** (22 ganze Zeilen, 8 Teilzitate), **30 × `diff` rc 0** |
| Stellen | Abschnitt 40 (40.1–40.10), **Nachtrag am Ende von 39.8**, **neun Marken** am alten Ort |
| Geändert | **keine `.py`**, nichts gerechnet; 28 Hashes vorher = nachher; ausserhalb `docs/` **0** Änderungen |
| Sonde | vorher und nachher 0 Befunde, 15/15, (ii) `0` |

⭐ Deine zwei Anpassungen sind umgesetzt: **40.5 entfällt als eigener
Unterabschnitt** (mit einem Satz, der auf den Nachtrag in 39.8 verweist — sonst
sucht später jemand eine Nummer, die es nicht gibt), und **40.6** trägt deine
Entscheidung, sodass der Nachtrag nicht mit „Einordnung steht aus" endet.

⚠️ **Eine Marke ging nicht an den Ort, den der Auftrag nannte.** Er sagte
„23d-Abschnitt im Register" — **einen Abschnitt 23d gibt es nicht**, 23d ist eine
Antwortdatei von dir. Die Marke steht an **39.6**, wo die Notiz „nicht
eingetragen" steht; das nannte der Auftrag selbst als Ort.

## 2. ⚠️⚠️ Ein vierter Fall derselben Klasse — vorgelegt, nicht berichtigt

Du schreibst in 24a Abschnitt 3:

> Die Listen sind Ergebnisdateien der neun Backtests mit heutigen Parametern; **TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren.**

**Gemessen:** TB-90 **B6** hat die neun Backtest-Skripte **vor und nach dem
Kostenmodul** verglichen (`cmp` 9/9) — am selben Tag und auf `data/`. Der
Erzeuger der TB-24-Listen (`alle_bots.py` → `positionen_holen.py`, gefundene
Trades) **war nicht beteiligt**, und auf dem Snapshot lief nichts.

⭐ **Deine Regel trägt trotzdem**, weil sie ihren eigenen Nachweis verlangt: der
Modus-Lauf, zweimal, bytegleich (23e). Wir haben deshalb **nicht berichtigt**,
sondern als Tatsachennotiz in 40.6 und 40.9 vorgelegt. ⚠️ **Aber es ist dieselbe
Klasse wie deine drei angenommenen Fälle:** eine Tatsache über den Bestand
behauptet statt als Voraussetzung genannt. Du hast gesagt, du zählst sie mit —
hier ist der vierte.

## 3. Zwei Funde für TB-98

**(a) ⚠️⚠️ Der Erzeuger überschreibt.** `positionen_holen.py` schreibt **fest**
nach `research/tb24_haltedauern/daten/` (`DATEN_DIR`, `to_csv`, **kein
Schalter**). Ein unveränderter Aufruf **überschriebe die alten Listen** — genau
die, die nach deinem Registertext „liegen bleiben als historischer Stand mit
Tatsachennotiz". ⇒ Für TB-98 ist ein **neuer Erzeuger nach 36.1** Voraussetzung,
nicht Handwerk am Rand. Steht in 40.6.

**(b) Der Parameterstand — deine Unsicherheit, gemessen.** Du fragtest, ob 5.4
die Schwelle „mit heutigen Parametern" nennt.

| | gemessen |
|---|---|
| Die **Schwelle** | ⭐ **registriert** — „30 Trades je Jahr" als **Festlegung 7** und in **5.1 Nr. 6**; `faltenplan.py` liest sie aus `registerdaten`, **null** Vergleiche mit einem Literal |
| Der **Parameterstand** | ⛔ **nicht im Register.** 5.4 nennt ihn nicht; `78e2bc6` kommt im ganzen Register **0**-mal vor |
| Ausserhalb des Registers | Der TB-24-Bericht sagt „mit den heutigen `live_params.py`" (Stand 13.09.). Die neun `live_params.py` haben sich seit `78e2bc6` **nur in drei Kommentarzeilen** geändert, **keine Zuweisung**. Die `<bot>_meta.json` enthalten **keine** Strategieparameter |
| ⚠️ Nicht gemessen | der übrige Code (Bots, Simulation, TB-38, TB-90) |

⇒ Deine Forderung nach einer Tatsachennotiz zum Parameterstand ist berechtigt,
und sie ist **erfüllbar**: Die Parameterdateien sind unverändert, ihre Hashes
gehören je Bot in die Notiz. Steht so in 40.6 und im Auftrag TB-98.

## 4. ⭐ Ein Satz, der deiner werden soll

Im Nachtrag zu 39.8 steht ein Satz, den **die Sitzung formuliert hat**, nicht du:

> Eine Störprobe nach „geht es ein?" wird in **beide** Richtungen geführt: klein genug, dass nichts passieren darf, und gross genug, dass etwas passieren muss.

Er verallgemeinert deinen Fall. Anlass: Die Probe, wie unser Auftrag sie
vorschlug („eine Zeile entfernen genügt"), hätte **allein das falsche ‚nein'**
ergeben — dieselbe Fehlerklasse wie `F4`, nur bei einer Messung statt bei einer
Prüfung. ⚠️ **Er steht als Tatsache der Sitzung im Register, nicht als
Registertext.** Wir legen ihn dir vor.

## 5. Vier Fragen

**(1) Der vierte Fall (Abschnitt 2)** — nimmst du ihn an, und soll die
Tatsachennotiz in 40.6 als **Berichtigung** umgeschrieben werden, oder bleibt sie
eine Vorlage, bis TB-98 den eigenen Nachweis geführt hat? ⭐ *Wir neigen zum
Zweiten: Die Notiz sagt heute, was gemessen ist, und TB-98 liefert, was fehlt.*

**(2) Der Satz aus Abschnitt 4** — Registertext von dir, oder bleibt er eine
Tatsache der Sitzung?

**(3) ⚠️ Welche acht sind die acht Mutationsproben?** Abschnitt 12 nennt die
**Zahl**, aber **keine Namen** — gemessen in TB-96. Deine Regel aus 40.7 verlangt
Gegenproben für „alle acht". TB-97 benennt sie deshalb zuerst aus dem Code und
legt die Liste vor. ⭐ **Die eigentliche Frage:** Soll die Liste danach **in den
Registertext von 12**, damit die Zahl künftig an Namen hängt statt an einer
Zählung? *Eine Zahl ohne Namen ist eine Kopie des Codes im Register, und Kopien
altern — deine Regel aus 23a, angewandt auf 12.*

**(4) `beispieldaten.py` — Prüfung oder Werkzeug?** Es ist **keine** Prüfung,
enthält aber zwei der vier Jahresliterale (Z. 69/77). Nach deiner Antwort in 24a
Abschnitt 6 werden sie aus dem Plan genommen. ⚠️ Bei einem Bot mit Doppeljahren
trifft Z. 69 **nie**, und Z. 77 macht nach seinem eigenen Docstring den
Zufalls-Timing-Test **entartet**. ⇒ Ist das eine Umstellung wie die anderen —
oder ein **Befund am Testrahmen**, der eine eigene Notiz braucht?

## 6. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend.
⚠️ `belege/` bleibt nach 27.1 für dich gesperrt; du hast in 24a bestätigt, dort
nichts zu lesen. Brauchst du eine Passage, kommt sie zitiert.

---

## In einfacher Sprache

Der neue Regelwerksabschnitt steht: 463 Zeilen dazu, keine entfernt, jedes deiner
Zitate maschinell mit dem Original verglichen.

Beim Eintragen sind zwei Dinge aufgefallen. **Erstens:** Du hattest
vorausgesetzt, die Reproduzierbarkeit der neun Handelslisten sei schon gezeigt.
Gezeigt war sie für verwandte Programme, nicht für das, das diese Listen erzeugt
hat. An deiner Entscheidung ändert das nichts — sie verlangt ohnehin einen
eigenen Nachweis —, aber es ist derselbe Fehlertyp wie die drei Stellen, die du
heute früh zurückgenommen hast, und deshalb legen wir ihn vor. **Zweitens:** Das
alte Programm würde beim nächsten Aufruf die alten Listen überschreiben, die
laut deinem Text liegen bleiben sollen. Für die Neu-Erzeugung braucht es deshalb
ein neues Programm, das in eine neue Datei schreibt.

Deine offene Frage nach den Parametern ist beantwortet: Die Schwelle steht im
Regelwerk, der Parameterstand nicht — und die Parameterdateien sind seit damals
unverändert, ihre Prüfsummen können also in die Notiz.

Und eine Frage, die grösser ist, als sie aussieht: Das Regelwerk sagt, es gebe
acht Gegenproben, nennt aber keine Namen. Wer die Namen nicht kennt, kann nicht
prüfen, ob es acht sind — und merkt es nicht. Wir schlagen vor, die Namen
einzutragen.
