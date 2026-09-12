# Übergabe: Übersicht der `research`-Urteile

**Stand: 2026-09-12** · Branch `claude/new-session-4huwsy` · Ergebnis:
`docs/UEBERSICHT_RESEARCH.md` (neu), dazu `docs/ERGEBNIS_uebersicht_research.md`
(Kurzfassung zum Kopieren) und diese Übergabe.

**Kein Produktivcode angefasst.** `git diff origin/main HEAD --name-only` listet
ausschliesslich drei neue Dateien unter `docs/`. Keine Untersuchung wiederholt,
keine Zahl nachgerechnet — jede Zahl ist aus einem `BERICHT.md` zitiert.

---

## 1. Zuerst: die Ordner, deren Urteil überholt sein könnte

### 1.1 `hrp_portfolio` — das grösste Risiko, und die Vorerhebung ist selbst überholt

**⚠ Der wichtigste Einzelbefund dieser Erhebung.** Die Aufgabenstellung hielt fest,
die HRP-Kernaussage sei beim dritten Mal gekippt und HRP liege *„mit heutigen Kurven
+0,14 Calmar vorn"*. Das ist der Stand von **Nachtrag Z**. Es gibt zwei weitere
Nachträge:

| Fassung | HRP − Gleichgewichtung | Kernaussage |
|---|---:|---|
| Erstfassung (2026-09-06) | −0,1905 | HRP nicht besser |
| Nachtrag N (1. Korrektur) | −0,4627 | hält |
| Nachtrag Z (2. Korrektur) | **+0,1424** | hält nicht |
| **Nachtrag V (2026-09-08)** | **−0,0432** | **hält doch** |
| Nachtrag W (2026-09-10) | unverändert | reine Wartung, bestätigt V byteweise |

Nachtrag V hat den Vorsprung am selben Tag zurückgedreht: er hing an **einer
einzigen Kurve** — `volatility_breakout_crypto` war die einzige der neun ohne den
live aktiven BTC-Regimefilter. Der Bericht nennt den Vorzeichenwechsel aus Z
*„ein Artefakt genau dieser einen Lücke"*.

**Gültig ist heute: HRP bringt keinen risikoadjustierten Vorteil — bei einem
Abstand von 0,7 %** (−0,0432 auf ein Calmar-Niveau von rund 6,17). Der Bericht
schreibt selbst: *„Das Vorzeichen ist eindeutig; die Grösse ist es nicht."* Die
Grundlage sind eingefrorene Kurven vom **2026-09-08**; PR #57 und PR #81 liegen
danach. Bei diesem Abstand kann eine erneut verschobene Kurve das Vorzeichen wieder
drehen.

### 1.2 `trend_overlay` — dieselbe Grundlage, eine Korrekturrunde weniger

Die Studie ist bei der **zweiten** Korrektur stehen geblieben und hat **kein**
Gegenstück zu HRPs Nachtrag V bekommen. Ihre eigene Annahme Z4.1 benennt die Lücke
wörtlich: die `volatility_breakout_crypto`-Kurve dieser Grundlage (71,26 %) ist
*„nicht live-konform"*, live läge sie bei 49,03 %. **Das ist exakt die Lücke, die
bei HRP das Ergebnis getragen hat.**

Die Kernaussage hält in allen drei Teilaussagen, zwei davon sind aber knapp:
– die Nuance „kostet out-of-sample Rendite" ist bereits einmal gekippt und einmal
zurückgekippt (−0,41 → +0,81 → 0,00);
– Teilaussage T2 hält, weil der letzte aktive Signaltag der **2025-04-21** ist und
der IS/OOS-Split am **2025-04-23** liegt — **zwei Tage**. Der Bericht hält das selbst
fest, *„damit die Zahlengleichheit nicht robuster wirkt, als sie ist"*.
Robust dagegen: T1 (+7,31 Calmar) und T3 (85 % der Signaltage in 2022, weil das
Signal aus BTC und dem Aktien-Proxy kommt und die Bot-Kurven gar nicht berührt).

### 1.3 `order_sensitivity` — die gemessene Konfiguration existiert nicht mehr

Der Bericht rechnet ausdrücklich auf den Modulkonstanten von `equity_simulation.py`
(Annahme 1) und nennt in Abschnitt 8 selbst, dass diese bei vier Bots von
`live_params.py` abwichen — genau diese vier sind seither angeglichen. Die
Schlagzeile der Studie (`rsi2_mean_reversion`, Calmar-Spanne **12,1×**) ist mit
**Limit 8 / 10 % Allokation** gerechnet; live gelten **20 / 5 %**. Die
Elliott-Zeilen stammen aus dem look-ahead-behafteten Backtest.

**Was hält:** die strukturelle Aussage. Der Engpass ist praktisch immer das
**Positionslimit**, nie das Kapital, und **keine** der sechs geprüften Entscheidungen
kippt — weil Entscheidungen gepaarte Vergleiche sind und die Reihenfolge-Willkür
beide Seiten gleich trifft. Gefährdet sind die absoluten Kennzahlen, Perzentile und
Einstufungen je Bot.

### 1.4 Zweite Reihe

* **`volatility_scaled_sizing`** — beide Elliott-Zeilen auf look-ahead-behafteter
  Grundlage; für `elliott_wave` unterstellt Annahme 3 zusätzlich ein Positionslimit
  von 8, das dieser Bot **nicht hat**. Die Kernaussage („schadet bei 8 von 9") ist
  davon nicht bedroht, der einzige Gewinner `rsi2_crypto` steht auf einer bis heute
  unveränderten Kurve.
* **`elliott_wave_params`** — Urteile gut abgestützt (Aktien: +398 % gegen +756 %
  Buy-and-Hold), aber dünne Krypto-Basis (130 Trades in 5 Jahren, 31
  out-of-sample) und starke Reihenfolge-Streuung beim Aktien-Sieger (+212 % bis
  +509 %). PR #81 betraf laut eigenem Nachtrag **24 von 48** Rasterkombinationen
  dieses Bots — die Live-Kombination allerdings nicht.
* **`oos_take_profit`** — kein Grundlagen-, sondern ein Reihenfolgenproblem: seine
  Kennzahlen (+70,37 % / −10,11 % / 6,96) sind durch den unmittelbar folgenden
  PR #48 ersetzt (+72,39 % / −9,69 % / 7,47).
* **`sync_check`** — Schlussaussage („alle neun synchron") aktuell, Wirkungstabelle
  in Abschnitt 3 durch den Look-Ahead-Fix teilweise historisch.

---

## 2. Die Urteile in einem Satz je Ordner

| Ordner | Urteil |
|---|---|
| `backtest_defaults` | umgesetzt: 9 Konstanten in 5 Bots gekoppelt, **keine** Wertabweichung gefunden |
| `datenluecke_wurzelkorrektur` | **nein** zur Wurzelkorrektur; Weg B (Cronjob später) ist die flachere Änderung |
| `elliott_wave_lookahead` | Look-Ahead **bestätigt**, gravierend; beide Kanäle im Bot behoben, Live-Bot war nie betroffen |
| `elliott_wave_params` | Krypto **ja** (10 %/6 %, übernommen); Aktien **nein** — keine von 252 Kombinationen schlägt Buy-and-Hold |
| `exposure_messung` | −1,43 % ist **keine Risikokennzahl**; die Vermutung „überwiegend Kasse" ist **falsch** |
| `forward_test_sync` | umgesetzt, Verhalten nachweislich identisch (11/11 bzw. 15/15) |
| `hrp_portfolio` | **offengelassen**; aktuell: HRP nicht besser, Abstand 0,7 % — dreimal gekippt |
| `oos_positionslimit` | Fehler behoben; **14 von 128** Trades betroffen, nicht 8 |
| `oos_take_profit` | Fehler behoben — es war ein Absturz, kein falscher Wert; keine Rückwirkung |
| `order_sensitivity` | betroffen **ja**, bis 12,1× Calmar-Spanne; **keine** der 6 Entscheidungen kippt |
| `parameter_doku` | **kein Bericht** — Docstring: 2 von 20 dokumentierten Fundstellen waren sofort falsch |
| `pnl_2025_fixed_size` | **bewusst kein Urteil** — reine Informationsauswertung |
| `sync_check` | erst 5 von 9 abweichend, nach der Sync-Reihe **alle neun synchron** |
| `trailing_stops` | **nein** — nur die Drawdown-Wirkung ist belegbar, bei keinem Bot die Calmar-Verbesserung |
| `trend_overlay` | **hält**: gesamt besser, out-of-sample wirkungslos, Wirkung auf 2022 konzentriert |
| `uebersprungene_trades` | **kein Bericht** — Docstring: alle 115 Übersprünge wegen **Limit**, keiner wegen Kapital |
| `vbc_deepdive` | die „doppelte Bestätigung" **trägt nicht**; übrig bleibt die Drawdown-Reduktion |
| `volatility_scaled_sizing` | **nein** — schadet bei **8 von 9**; einziger Gewinner `rsi2_crypto` |

---

## 3. Die Einsichten, die über den Einzelfall hinausreichen

1. **Jeder Mechanismus, der die Ertragsverteilung oben beschneidet, kostet bei
   diesen Bots mehr, als er an Risiko spart.** Vol-Skalierung verkleinert die
   Position genau dann, wenn Trendfolger am meisten verdienen; ein Trailing-Stop
   beendet die Position, sobald die Bewegung stockt. Zwei Untersuchungen mit völlig
   verschiedenen Mechanismen kommen unabhängig auf dasselbe Muster.
2. **Der Engpass ist das Positionslimit, nicht das Kapital** — über alle neun Bots
   praktisch 100 % der Ablehnungen. Die verbreitete Formulierung „nicht genug freies
   Kapital" beschreibt nicht, was passiert.
3. **Messungen, die etwas anderes messen als gemeint, sehen besonders beruhigend
   aus.** Die Bot-Kapitalkurven bewegen sich nur an Ausstiegstagen; zwei überwiegend
   aus Nullen bestehende Reihen korrelieren mechanisch nahe null. Zu Marktpreisen
   bewertet tritt ein Beta bis +0,82 hervor.
4. **Eine Abweichung, die kein Parameter ist, findet keine Konstanten-Prüfung.** Der
   BTC-Regimefilter fehlte im Backtest als *Verhalten* — er durchdrang alle fünf
   Profitabilitäts-Studien.
5. **Ein Prüfer kann den Erfolg der Aufräumarbeit bestrafen.** 15 gemeldete
   Sync-Abweichungen waren Falschmeldungen, weil die Werte inzwischen per Import
   statt per Zuweisung kamen.
6. **Die Aussagekraft eines Backtests hängt von der Fragestellung ab, nicht nur von
   seiner Korrektheit.** Derselbe Elliott-Backtest war für drei Untersuchungen
   brauchbar und für die Trailing-Stop-Frage unbrauchbar.

---

## 4. Was das für die nächste Sitzung bedeutet

**Keine dieser Zeilen ist ein Auftrag** — die Entscheidung liegt beim Nutzer.

* Wer HRP oder den Trend-Overlay zitieren will, sollte wissen, dass beide auf
  Kurven vom 2026-09-08 stehen und dass HRPs Vorzeichen an 0,7 % hängt.
* Wer eine Zahl aus `order_sensitivity` zitiert, zitiert eine Konfiguration, die es
  nicht mehr gibt — die *Schlussfolgerungen* halten trotzdem.
* Die fünf veralteten `results/*/equity_curve.csv` sind kein reines
  Research-Problem: dieselben Dateien speisen laut Protokoll 4.3b die Montags-Mail
  und die Dashboard-Portfolio-Sicht, solange ein Bot unter zehn geschlossenen
  Live-Trades liegt — und das tun derzeit alle neun (Protokoll-Punkt 15).
* Zwei Ordner hätten gern je ein `BERICHT.md`: `parameter_doku` und
  `uebersprungene_trades`.
* `docs/UEBERGABEPROTOKOLL.md` Abschnitt 5 nennt „17 Ordner"; es sind 18.

---

## 5. Wie die Erhebung gearbeitet hat

* Alle 18 Ordner erfasst: `BERICHT.md` vorhanden? Grösse, Datum, Zahl der Commits,
  Zahl der Nachträge — per `git log` je Datei.
* Je Bericht gelesen: Blockzitate am Anfang, Kurzfassung/Entscheidungsgrundlage,
  Gesamteinschätzung, alle Nachtrags-Abschnitte. **Nachträge haben Vorrang**; wo
  sie der Gesamteinschätzung widersprechen, sind beide genannt.
* Datengrundlage je Bericht bestimmt: abgelegte `equity_curve.csv` / eigener Lauf
  gegen `live_params.py` / Kurs- und Codestand.
* Merges seit den Berichten aus `git log --merges` und `git show --stat` belegt,
  nicht aus Commit-Titeln geraten.
* Nichts ausgeführt, nichts nachgerechnet, nichts geändert.
