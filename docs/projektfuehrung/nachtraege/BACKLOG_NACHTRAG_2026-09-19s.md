# Backlog-Nachtrag (s) — TB-56b, die Registerberichtigung (19.09.2026)

⚠️ **Nummern nach K2i:** Dieser Nachtrag nennt **keine Nummer, die er nicht
selbst gemessen hat.** Gemessener Stand, `HEAD` `9235880`, 22:0x Ortszeit,
`docs/projektfuehrung/BACKLOG.md` (951 Zeilen, letzter Commit `fef279c`):

| | gemessen | nächste freie |
|---|---|---|
| Blockbezeichner Abschnitt 2 | höchster **`2r`** (Überschrift Zeile 634) | **`2s`** |
| K-Nummern Abschnitt 4 | höchste **`K2k`** | **`K2l`** |
| Kettenzeilen Abschnitt 3 | höchste **`0,97`** | — |
| Nachtragsbuchstabe | Backlog **`(r)`**, Journal **`(f)`** | Backlog **`(s)`**, Journal **`(g)`** |

**Die Vergabe der Nummern gehört der einarbeitenden Sitzung**, nicht diesem
Nachtrag.

---

## Neuer Block für Abschnitt 2 — *„Aus TB-56b, die Registerberichtigung"*

*(nächste freie Nummer, gemessen: `2s`)*

| # | Punkt |
|---|---|
| **T56b.1** | ⭐⭐ **DER SATZ BEGRÜNDETE SICH SELBST.** Abschnitt 15.6 Punkt 2 sagte *„die Schranke dafür ist das Register, nicht die Datenlage"*. **Gemessen: kein Registertext nennt eine Jahreszahl** — 4a sagt „erstes Jahr mit Daten und Vorlauf", 3b (a) sagt „ab einem handelbaren Symbol". `ERSTE_MOEGLICHE_FALTE = 2019` stand **nur im Code und in diesem Satz**. Berichtigt in **Abschnitt 21**, null entfernte Zeilen. *Fehlerklasse C4: eine Angabe, die nicht sagt, gegen was sie prüft* |
| **T56b.2** | ⭐ **BETREIBERENTSCHEIDUNG 19.09.2026: Wo 4a und 3b (a) verschiedene erste Falten ergeben, bindet 3b (a).** Betroffen genau ein Bot: `t3_supertrend`, dessen Zeile dadurch **unverändert** bei 2019 / 7 Falten bleibt (Loader `MIN_HISTORY_DAYS = 730`, BTC/ETH handelbar erst ab 2019-08-17, Falte 2018 hat 0 Symbole). ⚠️ Begründung **strukturell**, nicht ergebnisbezogen: eine Falte ohne handelbares Symbol erzeugt keinen Falten-Sharpe |
| **T56b.3** | ⚠️⚠️ **OFFEN, BETREIBER: Amendment zu Sperrliste Punkt 4.** `DD_Toleranz` ändert sich bei **`rsi2_mean_reversion`** und **`volatility_breakout`** auf **allen 100** Exposure-Stufen, und zwar **tiefer, also nachgiebiger**: −8,55 → **−12,89** bei 100 % Exposure. Bei `elliott_wave_stocks` und `turtle_soup_stocks` **unverändert** (sie gewinnen zwei Falten statt einer). **Vorlage mit drei Wegen und Empfehlung A in Abschnitt 21.6.** ⚠️ *Eine Schranke zu lockern, nachdem die Richtung bekannt ist, ist genau die Entscheidung, die das Register verhindern soll — deshalb Vorlage, nicht Ausführung* |
| **T56b.4** | ⚠️ **Die vier Aktien-Bots teilen keinen Faltenplan mehr.** `elliott_wave_stocks` und `turtle_soup_stocks` beginnen **2017**, `rsi2_mean_reversion` und `volatility_breakout` **2018**. Abschnitt 3 des Registers sagt dreimal *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"*. **Diese Prämisse trägt nicht mehr**; gehört mit T56b.3 in denselben Zug |
| **T56b.5** | ⚠️ **Fünf von neun Bots haben KEINE `DD_Toleranz.`** Die Krypto-Bots stehen in **beiden** Benchmark-Tabellen als `status: platzhalter` mit leerer `dd_toleranz`; das hängt an TB-31. **Gemessen, nicht vermutet.** Die Drawdown-Bedingung (Abschnitt 4) braucht die Zahl — **vor dem Tag** |
| **T56b.6** | **Zwei Code-Kopien der Schranke stehen noch:** `research/faltenplan_neun/faltenplan_neun.py:120` und `research/krypto_historie/faltenplan.py:64`. ⚠️ **Der Kommentar in `faltenplan_neun.py:119` verweist auf `registerdaten.py::ERSTE_MOEGLICHE_FALTE` — eine Konstante mit 0 Treffern im Quelltext.** Eigene Aufgabe **mit Mac-Lauf**; Freigabe liegt seit TB-56 vor, nicht in Anspruch genommen. ⚠️ **Dabei mit zu lösen: `test_faltenplan_neun.py:519` (Probe F) verfälscht genau diese Konstante** — fällt sie weg, misst die Probe nichts mehr (A5) |
| **T56b.7** | **„Änderung an Registertext 5f" ist nicht spezifiziert.** Die Übergabe vom 19.09. führt sie als Punkt; **gemessen: im gesamten Repo steht nirgends, worin sie bestehen soll** (einziger Treffer ist die Übergabezeile selbst). Der offene Teil von 5f — der fehlende Lock-Hash — ist mit Abschnitt 20 geschlossen. **Nichts erfunden; Rückfrage an den Betreiber** |
| **T56b.8** | **Abschnitte 18 und 20 bestehen den Tatsachennotiz-Test** (jeder Satz Messwert mit Herkunft oder Verweis, Schlussabsatz nennt die Grenzen). ⚠️ **Ein Formbefund:** beide verweisen auf *„die Form der Tatsachennotiz zu 4d (Abschnitt 15.6)"* — und genau diese Tabelle ist jetzt ERSETZT. Der Verweis bleibt gültig (er zeigt auf die Form), ist aber in Abschnitt 21.7 festgehalten, damit er nicht stillschweigend in die Irre führt |

---

## ⭐⭐ Für `ARBEITSWEISE.md` und die Übergabe — die Reichweite der Geräteanbindung

*(nächste freie K-Nummer, gemessen: `K2l`)*

| # | Punkt |
|---|---|
| **K2l** | ⚠️⚠️ **DIE GERÄTEANBINDUNG IST KEIN TERMINAL AUF DEM MACBOOK.** Gemessen am 19.09.2026: `uname -a` meldet **`Linux … Ubuntu 22.04.5 LTS`**, `python3 -V` **3.10.12**, das Repo hängt per **FUSE** unter `/sessions/…/mnt/trading-bot`. **`trading-env/bin/python3` ist als Datei da, lässt sich aber nicht ausführen** (`No such file or directory` — macOS-Binärdatei auf Linux). ⇒ ⭐ **Die Regel: _Die Anbindung liest das Repo, sie rechnet nicht darin._** Lesen, `grep`, `wc`, `cmp`, `shasum`, lesende git-Befehle und Ablage unter `docs/` gehen; Basislauf, Trockenlauf, Registerprüfer, `snapshot.py` und **jede Messung, deren Ergebnis ins Register soll**, brauchen weiterhin einen **Mac-Lauf**. ⚠️ **`UEBERGABE_2026-09-19.md`, Nachtrag 2 ist an dieser Stelle zu weit gefasst und gehört berichtigt** — dort steht „wo eine Sitzung über die Geräteanbindung auf `~/trading-bot` zugreifen kann, MESSE ICH SELBST", ohne die Grenze zu nennen |

⭐ **Die Fehlerregel dazu, nach `DOKUMENTATIONSSTANDARD.md` Regel 3:**

| Fehler | ⇒ Regel |
|---|---|
| Beinahe „gemessen über die Geräteanbindung" geschrieben, ohne den **Interpreter** zu nennen — und `3.9.6` stand als Erwartung im Kopf, weil es im Register steht | ⭐ **Eine Messung nennt die Umgebung, in der sie lief, nicht die, in der sie hätte laufen sollen.** Eine Umgebung ist so wenig ein Messwert wie ein Name |

---

## Zum Journal

*(nächster freier Journal-Buchstabe, gemessen: `(g)`)*

Der Ergebnisblock zu TB-56b steht in
`docs/ERGEBNIS_TB-56b_registerberichtigung.md` und trägt „In einfacher Sprache"
am Ende. Für das Journal genügt der Verweis plus die drei Zahlen, die tragen:
**Abschnitt 21 angehängt, 0 entfernte Zeilen, keine gesperrte Datei berührt.**

---

## Nachgetragen nach dem TB-56b-Commit `8e87414` — ein geprüfter und verworfener Weg

*(nächste freie K-Nummer nach dem oben vorgeschlagenen `K2l`: `K2m`)*

| # | Punkt |
|---|---|
| **K2m** | ⛔ **FABLE-ANTWORTEN SELBST ABHOLEN — GEPRÜFT UND VERWORFEN (19.09.2026).** Betreiberwunsch: statt Fables Antwort einzufügen nur „fable fertig" schicken, und die Sitzung holt sie sich. ⭐ **Gemessen, nicht vermutet:** Der Browser-Bereich der Claude-Desktop-App erreicht `claude.ai`, ist dort aber **nicht angemeldet** — er führt ein **eigenes Profil**, getrennt von Chrome und von der Desktop-App selbst (es erschien die Anmeldeseite, nicht die Unterhaltungsliste). ⇒ Der Weg wäre gangbar, aber **nur nach einer einmaligen Anmeldung durch den Betreiber** im Browser-Bereich; Zugangsdaten gibt die Sitzung grundsätzlich nicht ein. **Betreiberentscheidung 19.09.2026: so lassen** — Fables Antworten werden weiter als Text in den Chat eingefügt. ⚠️ **Nicht erneut vorschlagen.** Preis der Entscheidung, benannt: der Handgriff bleibt beim Betreiber. ⚠️ **Nebenbefund:** Für den Browser-Bereich wurde `claude.ai` mit Geltung „site" freigegeben; **diese Freigabe bleibt bestehen, bis sie in den Einstellungen der Desktop-App entfernt wird.** Der geöffnete Reiter ist geschlossen, angemeldet wurde nichts, gelesen wurde nur die Anmeldeseite |

⭐ **Warum das hier steht, obwohl nichts daraus folgt:** `BACKLOG.md`, Abschnitt 5 verlangt, dass auch **verworfene** Ideen mit Begründung eingetragen werden, damit sie nicht in sechs Monaten erneut vorgeschlagen werden. ⚠️ **Und die Begründung trägt nur in ihrer genauen Form:** Der Weg ist **technisch offen**; verworfen wurde er als **Entscheidung**, nicht als Unmöglichkeit. Wer das später verkürzt zu „geht nicht", hat den Eintrag falsch gelesen.

---

## Berichtigung zu T56b.3 in diesem Nachtrag — die Entscheidung ist gefallen

⚠️ **T56b.3 oben lautet „OFFEN, BETREIBER". Das gilt nicht mehr; bei Widerspruch
gilt dieser Block.** Der Punkt wird beim Einarbeiten in dieser Fassung übernommen.

| # | Punkt |
|---|---|
| **T56b.3** *(berichtigt)* | ⭐ **BETREIBERENTSCHEIDUNG 19.09.2026: Das Amendment zu Sperrliste Punkt 4 wird EINMAL vollzogen, nach TB-31, für alle neun Bots.** `DD_Toleranz` wird dabei bei `rsi2_mean_reversion` und `volatility_breakout` **nachgiebiger** (100 % Exposure: −8,55 → **−12,89**); die Zahlen stehen gemessen in Registerabschnitt 21.6, die Entscheidung in **21.9**. ⭐ **Der Grund ist die Reihenfolge, nicht die Richtung:** fünf von neun Bots haben gemessen **keine** `DD_Toleranz` (Krypto, `status: platzhalter`), ein Amendment jetzt bewegte die gesperrte Zahl zweimal. ⚠️ **Ausdrücklich nicht entschieden wurde, die Lockerung zu vermeiden** — sie steht so oder so und wird durch Warten nicht kleiner |

⇒ **Damit rückt TB-31 (Krypto-Falten) auf die Kette vor den Tag.** Es ist jetzt
nicht mehr nur Vorbedingung des Faltenplans, sondern auch die des Amendments und
damit des signierten Tags.
