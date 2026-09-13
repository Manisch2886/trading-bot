# TB-25 — Fib-Score-Stufen: Ergebnis

**Kurzfassung zum Kopieren.** Ausführlich: `research/fib_score_stufen/BERICHT.md`.
Übergabe: `docs/UEBERGABE_TB25_fib_score_stufen.md`.

**Untersuchung, keine Änderung.** Kein Produktivcode angefasst, keine
Parametrisierung. `git diff origin/main HEAD --name-only` listet ausschliesslich
`research/` und `docs/`.

---

## Welcher der drei Ausgänge ist eingetreten?

### **Ausgang 2 — „Kein Unterschied zwischen den Stufen", für beide Bots.**

> *„Dann bleibt vom Elliott-Wave-Bot ein Zigzag-Detektor mit Stop."*

Die Punktwerte steigen monoton. **Kein einziger Schritt von Stufe zu Stufe** ist
von null zu unterscheiden — und der bestbelegte Schritt ist exakt null:

| Schritt | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe 1 gegen Stufe 0 | +3,83 pp, CI [−0,04; +7,91], p = 0,059 | +0,99 pp, CI [−1,90; +4,06], p = 0,54 |
| **Stufe 2 gegen Stufe 1** | **+0,12 pp**, CI [−5,17; +5,40], p = 0,97 | **+0,21 pp**, CI [−3,86; +4,56], p = 0,92 |
| Stufe 3 gegen Stufe 2 | +6,40 pp, CI [−7,79; +20,77], p = 0,36 | +3,72 pp, CI [−3,99; +12,29], p = 0,44 |

Zwischen „eine Bedingung erfüllt" und „zwei erfüllt" liegt bei beiden Bots
nichts. **Eine Anhebung der Schwelle auf ≥ 2 ist von den Daten nicht gestützt.**

---

## Die Zahlen

### Nettorendite je Stufe — mit den echten Ausstiegsregeln des Bots

**`elliott_wave`** (Krypto, 1 h, Zigzag 10 % / Stop 6 % / Ziel Fib 0,618,
18 Symbole, 2021-09 bis 2026-08)

| Stufe | n | Mittel | Median | CI 95 % (Trades) | CI 95 % (Symbole) | Treffer |
|---|---:|---:|---:|---|---|---:|
| 0 | 95 | 0,07 % | −6,30 % | [−2,13; +2,55] | [−2,31; +2,43] | 28,4 % |
| 1 | 83 | 3,90 % | −6,30 % | [+0,86; +7,33] | [+1,37; +6,19] | 43,4 % |
| 2 | 42 | 4,02 % | −6,30 % | [+0,05; +8,29] | [+0,80; +7,35] | 42,9 % |
| 3 | **5** | 10,42 % | +6,74 % | [−3,69; +24,54] | [−6,30; +21,57] | 60,0 % |

**`elliott_wave_stocks`** (Aktien, 1 Tag, Zigzag 5 % / Stop 3 % / kein Kursziel,
147 Symbole, 2016-08 bis 2026-09)

| Stufe | n | Mittel | Median | CI 95 % (Trades) | CI 95 % (Symbole) | Treffer |
|---|---:|---:|---:|---|---|---:|
| 0 | 303 | 3,61 % | −3,30 % | [+1,77; +5,52] | [+1,92; +5,50] | 20,1 % |
| 1 | 363 | 4,59 % | −3,30 % | [+2,48; +7,05] | [+2,67; +6,94] | 20,1 % |
| 2 | 127 | 4,81 % | −3,30 % | [+1,64; +8,52] | [+1,68; +8,78] | 22,0 % |
| 3 | **20** | 8,53 % | −3,30 % | [+1,78; +16,48] | [+2,42; +15,85] | 40,0 % |

**Stufe 3 trägt keine Aussage** (5 bzw. 20 Trades). Der **Median ist in sieben
von acht Gruppen exakt der Stop** — was sich zwischen den Stufen bewegt, ist nicht
der typische Trade, sondern der Rand der Verteilung. Gemessen wurde mit den
echten Ausstiegsregeln des Bots (Stop, Kursziel, Zeitausstieg), nach Gebühren und
Slippage.

### Der eine Vorbehalt: die Schwelle beim Krypto-Bot

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe ≥ 1 gegen Stufe 0 | **+4,12 pp**, CI [+0,70; +7,48], p = **0,028** | +1,19 pp, CI [−1,45; +3,93], p = 0,41 |
| Cluster-Intervall über Symbole | [+1,26; +7,29] | [−1,31; +3,70] |
| Trefferquote | 43,8 % gegen 28,4 % | 21,4 % gegen 20,1 % |
| Weglassprobe (jedes Symbol einmal raus) | +3,20 bis +4,76 pp, Vorzeichen bleibt | +0,72 bis +1,59 pp |
| Spearman(Stufe, PnL) | +0,164, p = 0,014 | +0,039, p = 0,27 |

Ein auffälliger Vergleich unter **22** — rein zufällig wäre gut einer zu
erwarten. Und er ist **kein Stufeneffekt**, siehe unten.

### Die Zerlegung — das ist der eigentliche Befund

Die Stufe zählt, **wie viele** Bedingungen gelten. Die drei sind aber nicht
gleichwertig:

| Bedingung | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Welle 2 / Welle 1 ∈ [0,5; 0,618] | +3,53 pp, CI [−0,90; +8,03], p = 0,10 | +1,68 pp, p = 0,33 |
| Welle 3 / Welle 1 ∈ [1,4; 1,8] | **−0,24 pp**, p = 0,91 | **−0,79 pp**, p = 0,63 |
| Welle 4 / Welle 3 ∈ [0,236; 0,382] | **+4,88 pp**, CI [+0,85; +9,13], p = **0,012** | +1,82 pp, p = 0,22 |

**Dieselbe Reihenfolge bei beiden Bots: Welle 4 > Welle 2 > Welle 3**, und
Welle 3 liegt bei beiden **unter null**. Der Krypto-Schwellenbefund von oben
löst sich hier auf — er stammt fast vollständig aus der Welle-4-Bedingung
allein, nicht aus dem Zählen.

*Vorbehalt:* beim Aktien-Bot ist **keine** der drei Bedingungen von null zu
unterscheiden, und das Cluster-Intervall des Krypto-Welle-4-Befundes berührt die
Null ([−0,05; +9,80]).

### Das Rundungsartefakt (0,33 gegen 0,34)

**Die Erwartung bestätigt sich: kein Renditeunterschied.**

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| 0,34 gegen 0,33 (Stufe 1) | +0,59 pp, CI [−6,20; +7,56], p = **0,87** | +2,77 pp, CI [−2,80; +9,39], p = **0,34** |
| 0,67 gegen 0,66 (Stufe 2) | +1,98 pp, p = 0,65 | −2,41 pp, p = 0,52 |

**Welche Bedingung trägt die 0,34?** Die **Welle-2-Bedingung** — und nur sie
(exhaustiv geprüft; dasselbe gilt für 0,67). Der Tie-Break ist damit nicht
zufällig, sondern deterministisch. Die unangenehme Stelle: die 0,33-Gruppe ist
eine Mischung aus der **schlechtesten und der besten** Einzelbedingung.

| Stufe-1-Untergruppe | Score | Krypto | Aktien |
|---|---:|---|---|
| nur Welle 2 | **0,34** | n = 27, 4,30 % | n = 75, 6,79 % |
| nur Welle 3 | 0,33 | n = 23, **−0,06 %** | n = 94, **1,94 %** |
| nur Welle 4 | 0,33 | n = 33, **6,34 %** | n = 194, **5,03 %** |

Der Rundungsvorzug hebt die Welle-2-Gruppe über eine Gruppe, in der die
bestlaufende Einzelbedingung steckt. *Ein Tie-Break, den niemand gewählt hat —
und der, wenn überhaupt, in die falsche Richtung zeigt.*

---

## Die Nebenfrage: Gibt es unter dem Score eine stetige Grösse?

**Ja.** Alle drei Bedingungen prüfen ein Wellenlängen-**Verhältnis** gegen ein
Intervall. Es sind allerdings **Intervalle, keine Toleranzen um ein Ziel** — die
kanonischen Fibonacci-Werte liegen bei Welle 2 (0,618) und Welle 4 (0,382) auf
dem **oberen Rand** des Intervalls, bei Welle 3 (1,618) unsymmetrisch im Inneren.

**Gemessen trägt sie nicht mehr als die Stufe** (Rangkorrelation gegen die
Nettorendite):

| Grösse | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe (0–3) | ρ = +0,164, p = 0,014 | ρ = +0,039, p = 0,27 |
| stetige Nähe | ρ = +0,109, p = 0,10 | ρ = +0,038, p = 0,28 |
| stetige Nähe, weiche Fassung | ρ = +0,130, p = 0,052 | ρ = +0,054, p = 0,12 |

**Als Primärschlüssel taugt sie — als Auswahlkriterium nicht.**

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Anteil Muster mit Gleichstand je Symbol, `fib_score` | 85,8 % | 73,6 % |
| dasselbe für die weiche stetige Nähe | **0,0 %** | **0,0 %** |

Eindeutigkeit ohne Trennschärfe ersetzt einen willkürlichen Tie-Break durch einen
sauberer aussehenden, nicht durch einen begründeten.

---

## Was daraus folgt — und was nicht

| Frage | Antwort |
|---|---|
| Filtert `min_fib_score = 0.3` etwas? | **Aktien: nein** (+1,19 pp, CI [−1,45; +3,93]). **Krypto: ja, aber aus dem falschen Grund** — der Effekt ist die Welle-4-Bedingung, nicht die Anzahl |
| Schwelle auf ≥ 2 anheben? | **Von den Daten nicht gestützt.** Der Schritt 1 → 2 ist +0,12 bzw. +0,21 pp |
| Ist die Rangfolge nach `fib_score` begründet? | **Nein.** Praktisch folgt daraus heute nichts: TB-20 hat gemessen, dass sie in 0 von 20 114 Läufen eine Auswahl traf |
| Gibt es einen stetigen Primärschlüssel? | **Ja**, eindeutig — aber ohne gemessene Trennschärfe |

**Keine Empfehlung wurde umgesetzt.** Was folgt, entscheidet der Nutzer.

---

## Belastbarkeit

| | |
|---|---|
| Datengrundlage | 225 Muster (Krypto, 18 Symbole, 5 Jahre) · 813 Muster (Aktien, 147 Symbole, 10 Jahre) |
| Übereinstimmung mit `elliott_wave_params` | 130 bzw. 510 Trades oberhalb der Schwelle — **dieselben Zahlen** |
| Stufe 0 sauber danebengestellt | Lauf mit `min_fib_score = 0.0`; Stufen 1–3 **Zeile für Zeile identisch** zum Bot-Lauf |
| Look-Ahead | korrigierter Pfad (PR #26), **mechanisch** nachgewiesen — `run_backtest` verweigert Wellen ohne `entry_idx` |
| Survivorship | Aktienuniversum ist „Top 150 nach **heutiger** Marktkapitalisierung"; trifft alle Stufen gleich, die **absoluten** Renditen sind aber zu optimistisch |
| Mehrfachvergleiche | 22 je Bot — kein Einzelvergleich wird „signifikant" genannt |
| Trennschärfe | Ein Unterschied von 1–2 pp wäre hier **nicht** zu finden gewesen (nötig: ~740 bzw. ~1 560 Trades je Gruppe). „Kein Unterschied" heisst: keiner ab rund 5 pp |
| Selbsttests | **29/29** je Bot |
| `shared/ergebniskurven.py` | **9× AKTUELL** (vor und nach dem Lauf) |

---

## Reproduktion

```bash
cd research/fib_score_stufen && python3 run_all.py     # ~10 Minuten
python3 shared/ergebniskurven.py                       # muss 9x AKTUELL melden
```
