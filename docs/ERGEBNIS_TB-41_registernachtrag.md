# TB-41 — Registernachtrag: Ergebnis

**Stand: 16.09.2026.** Basis `main` = `c104abf` (TB-40, PR #113 enthalten).
Datenstand `d9449faf51bffaaa…`, 223 Dateien — **vor und nach der Arbeit
identisch**, als Test nachgewiesen.

> ⚠️ **Kein Amendment. Es hat kein Selektionslauf stattgefunden** — kein Raster
> gerechnet, kein Parametersatz bewertet, kein Ergebnis erzeugt, kein
> signierter Tag gesetzt. Es wurde **nachgetragen, bevor gerechnet wird**.

---

## Die drei Antworten zuerst

### 1. Welche Tatsachennotizen waren falsch — und wie lauten sie jetzt?

| # | Falsch war | Richtig ist | Beleg |
|---:|---|---|---|
| 1 | **Symbolzahl je Falte** (15.5): acht der neun Reihen **zu hoch** | die Reihen unten; **es kommt nirgends ein Symbol hinzu** | TB-40-Trockenlauf des Laufcodes |
| 2 | **„Symbole ohne Faltenevidenz"**: eine Liste **je Markt** | Listen **je Bot** — 11 / 7 / 6 / 5 statt 6 und 1 | derselbe |
| 3 | **Die Klammer in 15.5**: „26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`" | **„25 Zeilen abzüglich `XAUTUSDT`"** — Ergebnis 24 bleibt richtig | `config/top25_symbols.txt`, `shared/symbols_config.py:23` |
| 4 | ⚠️ **neu gefunden:** „die **fünf** Werte" von `MIN_HISTORY_*` | **vier** Werte (17 520 · 730 · 500 · 1 825) in zwei Einheiten | die neun Bot-Dateien, gelesen |

**Die korrigierte Symbolzahl je Falte** (Lesart H, Register 16.1.1):

| Bot | Symbolzahl je Selektionsfalte | Bestätigung | Universum |
|---|---|---:|---:|
| `elliott_wave` | 6 / 13 / 13 | 18 | 24 |
| `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |
| `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| die vier Aktien-Bots | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |

**Was das an Regeln ändert: nichts.** Regel 4b (mindestens 3 Selektionsfalten)
bleibt für alle neun erfüllt, keine Falte ist leer, Regel 4c greift weiterhin
für keinen. ⚠️ `t3_supertrend` hat 2019 nur **drei** Symbole — das zählt, steht
aber im Bericht.

**Die Lesart:** Es gilt **H** („an mindestens einem Handelstag der Falte
handelbar") — der Wortlaut von Registertext 3b. **Das ist eine Bestätigung,
keine Änderung.** Sie wurde behalten, **weil sie registriert war**, und es war
dabei bekannt, dass die Alternative F `elliott_wave` auf 2 von 3 Falten drücken
und ihn „unterbestimmt" machen würde. *Eine Wahl nach dem Ergebnis wurde
bewusst vermieden.* H ist zusätzlich in der Sache richtig: F würde ein Symbol,
das im März handelbar wird, für das ganze Jahr streichen.

### 2. Welche Registertexte sind neu?

| Registertext | Was er festlegt | Status |
|---|---|---|
| **5 — Datenstand** | `data/live/` gegen `data/snapshots/<hash>/`; der Registerhash bezeichnet den **Snapshot**; Snapshot am Tag des Tags; alle Cronjobs in **UTC** | **ersetzt** 15.7 |
| **6 — Budgetstufen** | Schatten / Grundbudget / Bestätigt, Auf- und Abstieg quartalsweise, kein Betreiberentscheid nach oben, D5 erst nach zwei Quartalen „Bestätigt" | **neu** |
| **6 — Zellenbudget** | Zellen = Quelle × Anlage, Gleichteilung aktiver Zellen, Stufenfaktor 0/1/2, **Klassenschlüssel Aktien 80 / Krypto 20**, Multiplikator `m_b` | **neu** |
| **7 — Backtester-Prüfung** | simulierter Pfad gegen Papierpfad seit dem Umstellungstag, Schwelle 95 %, **Boden bei wenigen Signalen**, 10⁻⁵-Abweichung wird gezählt | **neu** |
| **2d — Embargo** | Beginn der Bestätigungsperiode am ersten flachen Tag, alte Frist als **Deckel**, Ausnahme von der Ein-Pfad-Regel | **ersetzt** 15.4 |
| **3b (a)–(e)** | Falte zählt ab einem Symbol, die fünf `MIN_HISTORY_*`, Benchmark auf den **geladenen** Symbolen, Berichtspflichten, Faltenkohärenz | **neu** |
| **Kandidatenregeln** | nie gegeneinander ranken, N = Rastergrösse, kein Raster für Neue, Familienbuchführung, Prior-Reihenfolge, **Overlays erst nach dem Lauf** | **neu** |
| **Vorab-Filter** | Darf er das handeln? Ist das Instrument zugelassen? Ko-Einstiegsquote > 1,5 ⇒ Variante | **neu** |
| **Short-Sleeves** | nur Indexinstrumente, 20 % Notional, Stop beim Broker, Fill zum Stress-Sprung, **Abbruch bei Überschreitung des Stress-Tagesverlusts** | **neu** |
| **S-B1 Proxy-Tabelle** | Signal auf US-ETFs, Handel auf UCITS; Korrelation ≥ 0,97; Abbruch unter acht Paaren / vier Anlageklassen; Short-Arm nur auf eigener Kursreihe | **neu**, in `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` |

**Der Schlüssel 80/20 mit seiner Messung** (2 271 gemeinsame Handelstage,
2017-08-18 bis 2026-09-01): Krypto **74,7 %** Jahresschwankung gegen Aktien
**19,6 %**, Verhältnis **3,82 ×**, Korrelation **0,32**. Bei 60/40 kämen **80 %
des Risikos** aus Krypto; gleicher Risikobeitrag läge bei 79/21. ⚠️ **Der
Ertrag wurde bewusst nicht gemessen** — der Zeitraum enthält einen der grössten
Krypto-Aufschwünge.

**Eine Festlegung bleibt offen und gehört dem Betreiber:** die **Mindestzahl
von Signalen** in Registertext 7. Bis sie feststeht, ist Registertext 7
berichtsfähig, aber nicht anwendbar.

### 3. Wo fallen Registertext und Umsetzung auseinander?

**Elf Stellen**, vollständig in Register 16.11. Die tragenden:

| Registertext | Was der Code heute tut |
|---|---|
| **5 (a)–(c)** Snapshot / Live | Es gibt **einen** Ordner `data/`; **101 Module** lesen ihn direkt |
| **5 (d)** UTC | Crontab in dieser Aufgabe nicht angefasst, `TZ=UTC` hier nicht geprüft |
| **6** Budgetstufen | **kein Leiter-Skript**, kein Bot liest `m_b`, alle neun rechnen faktisch 1/9 |
| **7** Backtester-Prüfung | **kein Vergleichswerkzeug**; die 95-%-Schwelle hat nichts zu messen |
| **7** Mindestzahl Signale | **offen — Betreiber** |
| **2d** Embargo | `auswertung.py` kennt nur das alte feste Embargo und ist **eingefroren** |
| **3b (d)** Liste der ausgelassenen Symbole | **drei Bots sortieren lautlos aus** — die Liste liesse sich heute nicht aus den Logs erzeugen |
| **16.1.1** korrigierte Zahlen | das TB-40-Werkzeug liest weiter die **historische** Tabelle in 15.5 und meldete bei einem erneuten Lauf wieder acht Abweichungen |

*Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.*

---

## Was nachgewiesen ist

| Nachweis | Wie |
|---|---|
| **Null entfernte Zeilen** im Register | `git diff --numstat` gegen die Basis: `655 0` und `85 0` — nur ergänzt |
| **Jede ersetzte Fassung steht noch da und trägt den Verweis** | fünf Stellen, je Suchtext und Verweis geprüft; Mutationsprobe G |
| **Die Symbolzahlen sind nicht abgetippt** | zwei getrennte Parser auf zwei Dateien, maschinell verglichen; Mutationsproben D und E |
| **Die fünf `MIN_HISTORY_*`-Werte stimmen mit den Bot-Dateien** | aus `strategies/<bot>/multi_symbol_optimise.py` **gelesen**; Mutationsprobe F |
| **Der Umstellungstag stimmt für alle neun Bots** | `docs/umstellungstag_entscheidungskerze.json`, `2026-09-16T04:42:24Z` |
| **Der Datenstand-Hash ist vor und nach der Arbeit identisch** | `d9449faf51bffaaa…`, 223 Dateien; `git status -- data` leer |
| **Zwei Wachen gegen dasselbe Risiko, einzeln geprüft** | Hash **allein** und git **allein** finden dieselbe veränderte Kursdatei (Teil I) |
| **Alle Mutationsproben beobachten den Ablauf** | jede kopiert, ändert **eine** Zeile und startet das Werkzeug als **eigenen Prozess** |

```
python3 research/registernachtrag_tb41/pruefe_register.py            -> KEIN BEFUND
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py -> 41/41
```

**In der Cloud nicht prüfbar:** `pandas`/`numpy` fehlen, Binance und yfinance
sind mit 403 gesperrt. Die Symbolzahlen wurden deshalb gegen das **committete
Ergebnisdokument von TB-40** verglichen, nicht gegen eine frische Messung.
`docs/TESTAUFTRAG_TB-41_registernachtrag.md`, Schritt 3, holt das auf dem Mac
nach — dort ruft dasselbe Werkzeug den Trockenlauf auf.

---

## Was diese Arbeit nicht tut

* **Kein Selektionslauf, kein Raster, keine Parameterübernahme.** Kein Amendment.
* **Kein Datenordner-Umbau** (`data/live/`, `data/snapshots/` — 101 Module).
* **Kein Logging-Fix** für die drei lautlos aussortierenden Bots.
* **Kein `m_b`** in den `forward_test.py`.
* **Keine Umstellung von `auswertung.py`** auf Verfahren B — unberührt.
* **Kein Snapshot, kein signierter Tag, kein Zeitanker** — Betreiber.
* **Keine Kursdatei angefasst**, nichts unter `broker/` oder `shared/`, keine
  Crontab, kein `results/*.csv`.
* **`research/faltenplan_neun/`, `research/universum_trockenlauf/`,
  `research/etf_trendfolge/` unberührt** — Belegquellen.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Vor jedem grossen Rechendurchgang wird aufgeschrieben, **nach welchen Regeln**
gerechnet wird — dieses Vorab-Dokument heisst „Register". Seit dem letzten Mal
sind zwölf neue Festlegungen entstanden, und drei aufgeschriebene Tatsachen
hatten sich als **falsch** herausgestellt. Die Frage war: Lässt sich beides in
**einem Zug** eintragen, ohne dass dabei etwas verlorengeht?

**Was herauskam.**
Ja. Vier falsche Angaben sind korrigiert — drei waren bekannt, eine ist beim
Nachzählen neu aufgefallen. Zehn neue Regelblöcke sind eingetragen, darunter
die **Budgetstufen-Leiter**: wie viel Geld ein Handelsprogramm bekommt und
wodurch es mehr oder weniger bekommt. Die stand bisher **nirgends
aufgeschrieben**, weshalb sie jedes Mal neu erfunden wurde — und jedes Mal
anders.

Wichtig: **Es wurde nichts gerechnet.** Kein Gewinn, kein Verlust, keine
Kennzahl, kein Programm neu eingestellt. Nur aufgeschrieben.

**Warum das so ist.**
Wer erst rechnet und dann die Regeln aufschreibt, kann sich selbst nicht mehr
glauben — die Regeln passen dann immer zufällig zum schönsten Ergebnis. Deshalb
kommt alles **vorher** ins Register. Und deshalb wird auch nichts
überschrieben: die alten, falschen Zahlen bleiben stehen und bekommen einen
Vermerk „ersetzt durch …". Am Ende sind in dieser Arbeit **null Zeilen
gelöscht** worden, nur welche dazugekommen. So bleibt nachlesbar, was wann
wieso geändert wurde.

Eine Entscheidung war zu treffen, und sie ist **so gefallen, wie es vorher
aufgeschrieben war**, nicht so, wie das Ergebnis es nahegelegt hätte: Ein
Handelswert zählt zu einem Jahr, wenn er *irgendwann* in diesem Jahr handelbar
war — nicht erst, wenn er es schon am 1. Januar war. Die andere Lesart hätte
einem Programm (`elliott_wave`) einen Prüfzeitraum genommen und es damit
ausgeschlossen. Genau deshalb durfte sie nicht nachträglich gewählt werden.

**Was das für dich heisst.**
Drei Dinge:

1. **Das Register ist jetzt vollständig.** Danach wird nichts mehr geändert,
   bevor die Kursdaten eingefroren („Snapshot") und der Stand digital
   unterschrieben ist. Das ist **dein** nächster Schritt.
2. **Eine Zahl fehlt noch, und nur du kannst sie setzen:** Ab wie wenigen
   Handelssignalen ist ein Vergleich nicht mehr aussagekräftig? Ohne diese
   Untergrenze bestraft die 95-Prozent-Regel Programme, die selten handeln —
   nicht weil sie schlechter sind, sondern weil bei acht Signalen schon ein
   einziger Unterschied durchfällt.
3. **Einiges steht im Register, bevor der Code es kann** — der getrennte
   Datenordner, die Budget-Leiter, der Backtester-Vergleich. Das ist so
   gewollt und **einzeln benannt** (Register 16.11, elf Stellen). Jede dieser
   Stellen ist eine eigene, schon freigegebene Aufgabe.

---

*TB-41, 16.09.2026. Kein Selektionslauf, kein signierter Tag, keine
Parameterübernahme.*
