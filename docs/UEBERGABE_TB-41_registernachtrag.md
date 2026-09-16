# TB-41 — Übergabe-Zusammenfassung

**Branch:** `claude/new-session-9dx5ul` · **Basis:** `main` = `c104abf`
(TB-40, PR #113 — geprüft, enthalten) · **Stand:** 16.09.2026

> ⚠️ **Kein Amendment. Es hat kein Selektionslauf stattgefunden** — kein Raster
> gerechnet, kein Parametersatz bewertet, kein Ergebnis erzeugt, kein
> signierter Tag gesetzt.

---

## 1. Welche Tatsachennotizen korrigiert wurden — und wie

| # | Was falsch war | Was jetzt dort steht | Wie korrigiert |
|---:|---|---|---|
| 1 | **Symbolzahl je Falte** (15.5): acht der neun Reihen **zu hoch** | `elliott_wave` 6/13/13·18 · `t3_supertrend` 3/6/9/13/13/13/17·18 · die drei Krypto-Tagesbots 6/9/10/13/13/17/18·20 · die vier Aktien-Bots 137/137/139/139/140/142/145·147 | neue Tabelle in **16.1.1**; die alte bleibt in 15.5 stehen und trägt den Vermerk „ERSETZT durch … 16.1.1" |
| 2 | **„Symbole ohne Faltenevidenz"**: eine Liste **je Markt** (krypto 6, aktien 1) | Listen **je Bot**: `elliott_wave` 11 · `t3_supertrend` 7 · die drei Krypto-Tagesbots 6 · die vier Aktien-Bots **5** (`APP`, `CEG`, `GEV`, `HOOD`, `SNDK`) | neue Tabelle in **16.1.2**, alte Fassung mit Vermerk stehengeblieben |
| 3 | **Die Klammer in 15.5**: „24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)" | **„24 (25 Zeilen abzüglich `XAUTUSDT`)"** — Ergebnis 24 und Hash bleiben | korrigierter **Rechenweg** in **16.1.3**; die falsche Klammer steht unverändert in der Tabelle und trägt daneben den Vermerk „KORRIGIERT in … 16.1.3" |
| 4 | ⚠️ **in dieser Arbeit neu gefunden:** Registertext 3b (b) sagt „die **fünf** Werte" von `MIN_HISTORY_*` | gezählt **vier** (17 520 · 730 · 500 · 1 825) in **zwei** Einheiten | **16.1.4** und Tatsachennotiz in **16.7**; der **Wortlaut bleibt unverändert**, weil er der registrierte ist — massgeblich ist die Tabelle |

**Die Zahlen sind nicht abgetippt.** `research/registernachtrag_tb41/pruefe_register.py`
liest sie aus dem Register **und** aus ihrer Quelle und vergleicht maschinell.

**Die Lesart ist bestätigt, nicht geändert:** Es gilt **H** („an mindestens
einem Handelstag der Falte handelbar") — der Wortlaut von Registertext 3b.
Sie wurde behalten, **weil sie registriert war**; dass die Alternative F
`elliott_wave` auf 2 von 3 Falten gedrückt und „unterbestimmt" gemacht hätte,
war zum Zeitpunkt der Entscheidung bekannt. *Eine Wahl nach dem Ergebnis wurde
bewusst vermieden.* Register **16.2**, beide Begründungen in der verlangten
Reihenfolge.

---

## 2. Welche Registertexte neu sind

**In `docs/VORREGISTRIERUNG_neuselektion.md`, Abschnitt 16:**

| Abschnitt | Registertext | Art |
|---|---|---|
| 16.3 | **5 — Datenstand:** `data/live/` gegen `data/snapshots/<hash>/`, Registerhash bezeichnet den **Snapshot**, Snapshot am Tag des Tags, alle Cronjobs in **UTC** | **ersetzt** 15.7 |
| 16.4 | **6 — Budgetstufen:** Schatten / Grundbudget / Bestätigt, Auf- und Abstieg quartalsweise, **kein Betreiberentscheid nach oben**, D5 erst nach zwei Quartalen „Bestätigt" | neu |
| 16.4 | **6 — Zellenbudget:** Zellen = Quelle × Anlage, Gleichteilung aktiver Zellen, Stufenfaktor 0/1/2, **Klassenschlüssel Aktien 80 / Krypto 20**, Multiplikator `m_b` | neu |
| 16.5 | **7 — Backtester-Prüfung:** simulierter Pfad gegen Papierpfad seit dem Umstellungstag, Schwelle 95 %, **Boden bei wenigen Signalen**, 10⁻⁵-Abweichung wird **gezählt** | neu |
| 16.6 | **2d — Embargo:** Beginn am ersten flachen Tag, alte Frist als **Deckel**, Attribution je Position als ausdrückliche Ausnahme | **ersetzt** 15.4 |
| 16.7 | **3b (a)–(e):** Falte zählt ab **einem** Symbol, die `MIN_HISTORY_*` je Bot mit Name und Einheit, Benchmark auf den **geladenen** Symbolen, Berichtspflichten, **Faltenkohärenz** | neu |
| 16.8 | **Kandidatenregeln:** nie gegeneinander ranken, N = Rastergrösse, kein Raster für Neue, Familienbuchführung, Prior-Reihenfolge, **Overlays erst nach dem Lauf** | neu |
| 16.9 | **Vorab-Filter:** Darf er das handeln? Ist das Instrument zugelassen? Ko-Einstiegsquote > 1,5 ⇒ Variante | neu |
| 16.10 | **Short-fähige Sleeves:** nur Indexinstrumente, 20 % Notional, Stop beim Broker, Fill zum Stress-Sprung, **Abbruch bei Überschreitung des Stress-Tagesverlusts** | neu |

**In `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`, Abschnitt 10a:**

**Registertext 3 — Proxy-Tabelle.** Signale auf den US-ETFs, **gehandelt wird
auf UCITS-Gegenstücken**; je Paar eine Registerzeile mit Korrelationsprüfung,
**unter 0,97 ist das Paar kein Proxy**; die Zeile nennt, **ab wann** die Prüfung
möglich war, der Bericht nennt die **ungeprüften Bärenepisoden**; Abbruch unter
**acht Paaren über vier Anlageklassen**. Dazu: ein Short-Arm darf **nicht** als
„Index × (−1)" gerechnet werden, sondern nur auf der **eigenen Kursreihe** —
und hat damit einen **anderen Faltenplan** als der Long-Arm.

**Der Klassenschlüssel 80/20 steht mit seiner Messung im Register** (2 271
gemeinsame Handelstage, 2017-08-18 bis 2026-09-01: Krypto 74,7 % gegen Aktien
19,6 %, Verhältnis 3,82 ×, Korrelation 0,32; bei 60/40 kämen 80 % des Risikos
aus Krypto, gleicher Risikobeitrag läge bei 79/21). ⚠️ **Der Ertrag wurde
bewusst nicht gemessen.**

**Der Befund aus TB-39 ist behoben:** Die Budgetstufen-Leiter stand nirgends im
Repo und musste nachgebaut werden. Sie steht jetzt in **16.4**.

---

## 3. Wo Registertext und Umsetzung auseinanderfallen

Vollständig in Register **16.11** (elf Stellen). Die tragenden:

| Registertext | Was der Code heute tut | Wer schliesst die Lücke |
|---|---|---|
| **5 (a)–(c)** Snapshot / Live | ein Ordner `data/`, **101 Module** lesen ihn direkt; kein Snapshot, keine Frischeprüfung | Datenordner-Umbau (eigene Aufgabe) |
| **5 (d)** UTC | Crontab **nicht angefasst**, `TZ=UTC` hier nicht geprüft | Betreiber, beim Umbau |
| **6** Budgetstufen und `m_b` | **kein Leiter-Skript**; kein Bot liest einen Multiplikator, alle neun rechnen faktisch 1/9; die 3⁹-Prüfung kann nicht laufen | `m_b` in die `forward_test.py` (freigegeben) |
| **7** Backtester-Prüfung | **kein Vergleichswerkzeug**; die 95-%-Schwelle hat nichts zu messen | eigene Aufgabe |
| **7** Mindestzahl Signale | **offen — Betreiber** | Betreiber |
| **2d** Embargo | `auswertung.py` kennt nur das alte feste Embargo, rechnet nach Verfahren A und ist **eingefroren** | TB-30b |
| **3b (a)–(e)** | gemessen ist das **einmal** (TB-40); `faltenplan_neun` antwortet weiter nach Lesart A | TB-30b |
| **3b (d)** ausgelassene Symbole mit Grund | **drei Bots sortieren lautlos aus** — die Liste liesse sich heute nicht aus den Logs erzeugen | Logging-Fix (freigegeben) |
| **6** Zellenzuordnung | steht im Register, **nirgends im Code** | mit dem Leiter-Skript |
| **16.10** Short-Sleeves | **kein Bot kann short** — reine Vorbedingung | wenn der erste Short-Kandidat antritt |
| **16.1.1** korrigierte Zahlen | das TB-40-Werkzeug liest als „eingetragen" weiter die **historische** Tabelle in 15.5 und meldete bei einem erneuten Lauf wieder acht Abweichungen | TB-30b, mit dem Auswerter |

*Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.*

---

## 4. Was geändert wurde

| Datei | Änderung |
|---|---|
| `docs/VORREGISTRIERUNG_neuselektion.md` | **+655 / −0** — Abschnitt 16 vollständig neu, fünf eingefügte „ERSETZT"/„KORRIGIERT"-Verweise in 15.4/15.5/15.7 |
| `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` | **+85 / −0** — Abschnitt 10a, ein Verweis in Abschnitt 2, Sperrlisten-Eintrag 20 |
| `research/registernachtrag_tb41/` | **neu** — `pruefe_register.py`, `test_registernachtrag_tb41.py`, `BERICHT.md` |
| `docs/ERGEBNIS_TB-41_registernachtrag.md` | **neu** — Ergebnis zum Kopieren |
| `docs/TESTAUFTRAG_TB-41_registernachtrag.md` | **neu** — autonomer Mac-Auftrag, verlangt ein ZIP in `~/Downloads` |
| `docs/UEBERGABE_TB-41_registernachtrag.md` | **neu** — dieses Dokument |

**Nicht angefasst:** `data/` (223 Dateien, Hash `d9449faf51bffaaa…` vor und
nach identisch), `research/vorregistrierung/auswertung.py`,
`research/faltenplan_neun/`, `research/universum_trockenlauf/`,
`research/etf_trendfolge/`, alle `live_params.py`, alle `forward_test.py`,
`equity_simulation.py`, `multi_symbol_optimise.py`,
`multi_symbol_walk_forward.py`, `broker/`, `shared/`, Crontab, `results/*.csv`.

---

## 5. Tests

```
python3 research/registernachtrag_tb41/pruefe_register.py            -> KEIN BEFUND (9 Pruefungen)
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py -> 41/41
python3 research/faltenplan_neun/test_faltenplan_neun.py             -> 145/145
python3 research/etf_trendfolge/test_etf_trendfolge.py               ->  64/64
python3 research/versuchsregister/test_versuchsregister.py           ->  41/41
```

| Geforderter Nachweis | Erbracht |
|---|---|
| Null entfernte Zeilen im Register, am Diff geprüft | `git diff --numstat`: `655 0` und `85 0` |
| Jede ersetzte Fassung ist gekennzeichnet **und** steht weiterhin da | fünf Stellen, je Suchtext **und** Verweis geprüft (Prüfung `ersetzt_gekennzeichnet`) |
| Symbolzahlen stimmen mit `research/universum_trockenlauf/` — maschinell | zwei getrennte Parser, zwei Dateien; auf dem Mac zusätzlich gegen einen **frischen Trockenlauf** |
| Die `MIN_HISTORY_*`-Werte stimmen mit den Bot-Dateien — gelesen | aus den neun `multi_symbol_optimise.py` per Regex gelesen |
| Datenstand-Hash vor und nach identisch | `d9449faf51bffaaa…`, 223 Dateien; `git status -- data` leer |
| Mutationsproben | sechs (D, E, F, G, H, I) — **jede** kopiert, ändert **eine** Zeile und startet das Werkzeug als **eigenen Prozess**; beobachtet wird der Ablauf |
| Zweite Wache verdeckt nicht das Fehlen der ersten | Teil I: Hash **allein** und git **allein** finden dieselbe veränderte Kursdatei |
| Alle bestehenden Tests bestehen weiterhin | siehe oben |

⚠️ **In der Cloud nicht lauffähig** (Umgebung, nicht TB-41):
`research/vorregistrierung/test_vorregistrierung.py` (kein `numpy`),
`research/universum_trockenlauf/test_universum_trockenlauf.py` (kein `pandas`).
Beide stehen in Schritt 7 des Testauftrags.

---

## 6. Was als Nächstes ansteht — und wem es gehört

1. **Betreiber:** die **Mindestzahl von Signalen** in Registertext 7 festlegen
   (als willkürlich zu kennzeichnen).
2. **Betreiber:** `docs/TESTAUFTRAG_TB-41_registernachtrag.md` auf dem Mac
   abarbeiten — dort läuft die Prüfung gegen eine **frische Messung** statt
   gegen ein Dokument.
3. **Betreiber:** **Snapshot ziehen, signierten Tag setzen, Zeitanker**.
   **Danach ist das Register zu.**
4. **Eigene Aufgaben, alle freigegeben:** Datenordner-Umbau (101 Module),
   Logging-Fix für die drei lautlos aussortierenden Bots, `m_b` in die
   `forward_test.py`, `auswertung.py` auf Verfahren B.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Vor einem grossen Rechendurchgang wird aufgeschrieben, **nach welchen Regeln**
gerechnet wird — dieses Vorab-Dokument heisst „Register". Seit dem letzten Mal
waren zwölf neue Festlegungen offen, und drei aufgeschriebene Tatsachen hatten
sich als **falsch** erwiesen. Die Frage: Lässt sich beides in einem Zug
nachtragen, ohne dass etwas verlorengeht?

**Was herauskam.**
Ja. **Vier** falsche Angaben sind korrigiert — drei waren bekannt, eine ist
beim Nachzählen neu aufgefallen. **Zehn** neue Regelblöcke sind eingetragen,
darunter die **Budgetstufen-Leiter**: wie viel Geld ein Handelsprogramm bekommt
und wodurch es mehr oder weniger bekommt. Die stand bisher **nirgends** — und
wurde deshalb jedes Mal neu erfunden, jedes Mal anders.

**Es wurde nichts gerechnet.** Kein Gewinn, kein Verlust, keine Kennzahl, kein
Programm neu eingestellt, keine Order.

**Warum das so ist.**
Wer erst rechnet und dann die Regeln aufschreibt, kann sich selbst nicht mehr
glauben — die Regeln passen dann immer zufällig zum schönsten Ergebnis. Deshalb
kommt alles **vorher** ins Register, und deshalb wird nichts überschrieben: Die
alten, falschen Zahlen bleiben stehen und bekommen einen Vermerk „ersetzt durch
…". In dieser Arbeit sind **null Zeilen gelöscht** worden, nur welche
dazugekommen. So bleibt nachlesbar, was wann wieso geändert wurde.

Eine Entscheidung ist so gefallen, **wie sie vorher aufgeschrieben war** — und
nicht so, wie das Ergebnis es nahegelegt hätte: Ein Handelswert zählt zu einem
Jahr, wenn er *irgendwann* in diesem Jahr handelbar war, nicht erst, wenn er es
schon am 1. Januar war. Die andere Lesart hätte einem Programm
(`elliott_wave`) einen Prüfzeitraum genommen und es damit ausgeschlossen. Genau
deshalb durfte sie nicht nachträglich gewählt werden.

**Was das für dich heisst.**
Drei Dinge, und alle drei gehören **dir**:

1. **Eine Zahl fehlt noch, und nur du kannst sie setzen:** Ab wie wenigen
   Handelssignalen ist ein Vergleich nicht mehr aussagekräftig? Ohne diese
   Untergrenze bestraft die 95-Prozent-Regel Programme, die **selten** handeln
   — nicht weil sie schlechter sind, sondern weil bei acht Signalen schon ein
   einziger Unterschied durchfällt.
2. **Ein Testauftrag liegt bereit.** Acht Schritte auf deinem MacBook,
   Ergebnisse als ZIP in `~/Downloads`. Dort läuft die Prüfung gegen eine
   **frische Messung**; in der Cloud ging nur der Abgleich mit dem
   aufgeschriebenen Ergebnis, weil dort Programmteile fehlen und die
   Kursanbieter gesperrt sind.
3. **Danach: Kursdaten einfrieren, Stand digital unterschreiben.** Ab dann ist
   das Register zu, und es wird gerechnet.

Und eine Einordnung, damit sie nicht überrascht: **Einiges steht im Register,
bevor der Code es kann** — der getrennte Datenordner, die Budget-Leiter, der
Backtester-Vergleich. Das ist so gewollt und **einzeln benannt** (elf Stellen).
Ein Regelwerk, das etwas beschreibt, was die Programme noch nicht können, ist
in Ordnung — solange **dasteht**, dass es so ist.

---

*TB-41, 16.09.2026. Kein Selektionslauf, kein signierter Tag, keine
Parameterübernahme.*
