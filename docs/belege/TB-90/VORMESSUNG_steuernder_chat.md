# TB-90 — Vormessung des steuernden Chats (Block A, Block C)

⚠️⚠️ **DAS IST EINE VORMESSUNG, KEIN NACHWEIS.** Sie ist in der **Brücken-VM**
gerechnet, nicht auf dem MacBook mit `trading-env` — andere Python-Fassung,
andere Paketversionen. **Die Mac-Sitzung misst jede Zahl hier nach und
berichtigt, wo sie abweicht** (Betreiberentscheidung 23.09.2026, Prüfprinzip
`A8`: *eine Selbstauskunft ist erst dann eine Wache, wenn ein anderer sie
gegenprüfen kann*). Weicht die Nachmessung ab, **gilt die Nachmessung**, und die
Abweichung kommt ausdrücklich ins Ergebnisdokument.

**Gemessen am:** 23.09.2026, 07:50–08:00 UTC
**Stand:** HEAD `66eec94`, `faltenplan.py` mit Block A **uncommittet** im
Arbeitsbaum (`numstat 2 0`)
**Womit:** Brücken-VM, Linux, Systempython; `python-binance` und `yfinance`
nachinstalliert (siehe `docs/werkzeuge/bruecke_ausstatten.sh`)

⛔ **Nichts geschrieben:** keine Datei in `ergebnisse/`, keine `.py` geändert,
`faltenplan.py main()` nie aufgerufen — nur `faltenplan.faltenplan()` im
Speicher. Arbeitsbaum vor und nach der Vormessung gleich.

---

## Der Anlass

TB-90 brach dreimal ab, zuletzt **nach** der Änderung in `faltenplan.py` und
**vor** den Nachweisen. Der Grund war nicht die Arbeit, sondern die Verbindung.
⭐ Gemessen: Die beiden Pakete, an denen die Brücken-VM bisher scheiterte, lassen
sich dort nachinstallieren. Damit rechnet der Faltenplan in der VM, und
`test_vorregistrierung.py` läuft bis an **dieselbe** Stelle wie auf dem Mac.

---

## Block A

### A1 ⭐⭐ — Bezeichner je Bot: **9 von 9**

Alle neun tragen `2026-01-01/2026-09-01` — **genau die Zahl aus Registertext
35.1**, gebildet aus 21.4 („Bestätigung ab" `2026-01-01`, 9/9) und 5.2
(Go-Live-Schnitt `2026-09-01`, ausschliesslich).

| Bot | Bezeichner |
|---|---|
| `elliott_wave` · `elliott_wave_stocks` · `rsi2_crypto` · `rsi2_mean_reversion` · `t3_supertrend` · `turtle_soup_crypto` · `turtle_soup_stocks` · `volatility_breakout` · `volatility_breakout_crypto` | **`2026-01-01/2026-09-01`** |

Beleg: `vormessung_a1_a4.txt`, Plan als `vormessung_a2_plan_nachher.json`.

### A2 ⭐⭐ — Ausgabevergleich: **genau ein Name je Bot**

Verglichen gegen `a2_plan_vorher.json` (von der Mac-Sitzung vor der Änderung
erzeugt). Je Bot verschwindet **ein** Faltenname und kommt **ein** neuer dazu;
**alle gemeinsamen Falten sind zeichengleich** (`0` ungleich, je Bot):

| Bot | weg | neu |
|---|---|---|
| `elliott_wave` | `2026-2027` | `2026-01-01/2026-09-01` |
| die übrigen acht | `2026` | `2026-01-01/2026-09-01` |

⭐ *Bei `elliott_wave` ist damit auch der Fall erledigt, den 35.1 ausdrücklich
unzulässig nennt: ein Doppeljahr, das Kalenderjahre ausserhalb der Spanne nennt.*

### A3 — `selektionsfalten` tragen keine Spanne

Alle neun: **kein** Eintrag mit Schrägstrich. Faltenzahl je Bot 4 bis 9.
⭐ Das ist Fables Argument aus 22h in Zahlen: Die Bestätigungsperiode ist keine
Selektionsfalte und steht deshalb nicht in dieser Liste.

### A4 — Embargo-Listen unverändert

`embargo_nach_falten` der **Selektionsfalten** vor und nach der Änderung
identisch, alle neun Bots. *Erwartbar, weil die Bestätigungsfalte die letzte ist
und damit in keiner Embargo-Liste vorkommt — aber gemessen, nicht erschlossen.*

### A5 ⭐ — Abbruchstelle des Tests: **dieselbe**

`test_vorregistrierung.py`, in der Brücken-VM:

```
auswertung.py, Funktion zulaessigkeit
KeyError: '2017'
```

⭐ **Dieselbe Stelle wie vor der Änderung** (TB-88, `m4_lauf2_trading_env.txt`,
auf dem Mac) — **keine neue, keine frühere**. Weg (A) verschiebt den Absturz
nicht; er hängt weiter allein an Plan-Punkt 8.

⚠️ **Das ist der Nachweis, der die Vormessung am dringendsten braucht:** Die
Mac-Sitzung muss bestätigen, dass die Stelle auch mit `trading-env` dieselbe ist.

### A6 — Simulation: Gegenprobe bestätigt, Tausch-Fall offen

Die TB-88-Simulation, mit `PY=python3` für die VM (`vormessung_a6_simulation.sh`):
Gegenprobe endet mit `KeyError: '2017'` wie im Repo ✔. Der Tausch-Fall lief bei
Abgabe dieser Vormessung noch. ⚠️ **Offen; die Mac-Sitzung misst ihn.**
*Vergleichswert aus TB-88: 163 bestanden, 2 gescheitert (`G6`, `H3`).*

---

## Block C ⭐⭐ — die Tabellen gegen den Plan, nach der Änderung

Mit `c_falten_abgleich.py` (von der Mac-Sitzung gebaut), Ausgabe
`vormessung_c_nachher.txt`.

| | `benchmark_drawdowns_tb72.json` | `benchmark_drawdowns_vt.json` |
|---|---|---|
| **Selektionsfalten** | ⭐⭐ **gleich bei allen NEUN** | bei `t3_supertrend` **Übermenge** (Falte `2018`), sonst gleich |
| **Bestätigungszeile** | ⚠️ **verschieden bei allen neun** | ⚠️ **verschieden bei allen neun** |

**Die Bestätigungszeile, je Bot:** Plan `2026-01-01/2026-09-01`, Tabelle `2026`
— bei `elliott_wave` `2026-2027`.

⇒ ⭐⭐ **Das bestätigt Fables Entscheidung aus 23b Punkt für Punkt:**
`_tb72.json` erfüllt seine Bedingung für die **Selektionsfalten** bereits
vollständig; der **einzige** Unterschied ist die Bestätigungszeile, und genau
dafür hat er **(ii)** entschieden — einmal neu rechnen. ⭐ Und seine
Determinismusbedingung wird dadurch scharf prüfbar: Die Neurechnung darf **genau
eine Zeile je Bot** ändern, sonst nichts.

⚠️ `_vt.json` fällt damit endgültig aus: Bei `t3_supertrend` trägt sie zusätzlich
eine Falte, die der Plan nicht kennt — zu der Abweichung der Bestätigungszeile
käme also eine zweite.

---

## Was die Mac-Sitzung tun muss

| | |
|---|---|
| **1** | **Jede Zahl oben nachmessen** — mit `trading-env`, nicht mit der VM. Weicht etwas ab: die Nachmessung gilt, und die Abweichung kommt ausdrücklich ins Ergebnisdokument |
| **2** | **A6 zu Ende messen** (Tausch-Fall), gegen den TB-88-Wert 163/2 |
| **3** | Die drei JSON-Hashes und den Hash von `faltenplan.py` je **vorher und nachher** |
| **4** | ⭐ Berichten, **ob beim Ändern von `faltenplan.py` gefragt wurde** — die Regel steht seit heute unter `ask` statt `deny`, gemessen ist die Wirkung nicht |
| **5** | Das Ergebnisdokument schreiben; **diese Vormessung ist keines** |

---

## In einfacher Sprache

Die Mac-Sitzung ist dreimal an der Mobilfunkverbindung gescheitert — beim letzten
Mal, nachdem sie die eigentliche Änderung schon gemacht hatte, aber bevor sie sie
belegen konnte.

⭐ **Deshalb sind die Belege jetzt hier vorgerechnet.** Möglich wurde das, weil
sich die beiden fehlenden Programmbibliotheken in der Arbeitsumgebung der
Geräteanbindung nachinstallieren liessen; seither rechnet dort dasselbe wie auf
dem MacBook.

**Das Ergebnis ist durchweg sauber:** Alle neun Bots tragen den richtigen neuen
Namen, und bei jedem Bot hat sich **genau dieser eine Name** geändert — sonst
nichts. Das Prüfprogramm bricht an exakt derselben Stelle ab wie vorher, die
Änderung hat also nichts verschlechtert.

⚠️ **Aber das ist ausdrücklich noch kein Nachweis.** Die Umgebung hier ist nicht
das MacBook, und im Projekt gilt: Wer misst, prüft nicht sich selbst. Die
Mac-Sitzung misst alles nach — **sie muss dafür nur noch nachrechnen, nicht mehr
suchen**, und braucht dafür ein paar Minuten statt einer ganzen Sitzung.
