# TB-90 — Ergebnis: Weg (A) in `faltenplan.py` und das Kostenmodul

**Sitzungstitel:** `TB-90` · **Stand:** 23.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-90_wegA_und_kostenmodul.md` · **Belege:** `docs/belege/TB-90/`
**Eingang:** `563fb54` · Commits: `53b35ce` (Schritt 0), `04d6ce6` (Block B),
`5194a0a` (Abbruchmeldung, zweiter Anlauf), `66eec94`/`709caf2` (Fortsetzung
Schritt 0, Vormessung, Berechtigungen), **`303a7fd`** (Block A: `faltenplan.py`
und die neun Nachher-Belege), Abgabe-Commit (dieses Dokument, Abschlussbelege,
Journalblock CR).
**Umgebung aller Nachweise:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Der Auftrag ist abgeschlossen.** Block A, B und C sind ausgeführt und
belegt; kein Abbruchkriterium hat gegriffen. Dieses Dokument ersetzt die
Abbruchmeldung aus `5194a0a` vollständig.

⚠️ **Wer was gemacht hat:** TB-90 lief in **vier Anläufen** (Verbindungsabbrüche,
einmal eine deny-Sperre). Block B und alle Vorher-Messungen: erster Anlauf.
Die Änderung an `faltenplan.py`: Sitzung `3d9a74f7`. Die Nachher-Messungen
A1–A6, C2/C3: vierter Anlauf, auf dem Mac. **Diese Abschlusssitzung** hat die
Belege gelesen, die Hashes nachher, den Sondenlauf nachher und den Vergleich
gegen die Vormessung **selbst gemessen** und das Dokument geschrieben — sie hat
`faltenplan.py` nicht angefasst.

---

## 1. Hashes vorher und nachher

| Datei | vorher (`schritt0_hashes_vorher.txt`, 07:27:40 CEST, `53b35ce`) | nachher (`abschluss_hashes_nachher.txt`, 10:17 CEST, `709caf2` + Arbeitsbaum) | |
|---|---|---|---|
| `ergebnisse/benchmark_drawdowns.json` | `a163c498…36d1ee` | `a163c498…36d1ee` | ✔ gleich |
| `ergebnisse/faltenplan.json` | `0e54ac5c…d32339` | `0e54ac5c…d32339` | ✔ gleich |
| `ergebnisse/benchmark_drawdowns_vt.json` | `4549395f…18745d` | `4549395f…18745d` | ✔ gleich |
| ⭐ `research/vorregistrierung/faltenplan.py` | **`fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79`** | **`7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb`** | geändert — **planmässig nach 37.3** |

Alle **zwölf** Dateien in `ergebnisse/` sind vorher und nachher zeichengleich;
es ist keine entstanden (12 vorher, 12 nachher). Einzige abweichende Zeile im
Hash-Vergleich ist `faltenplan.py`.

---

## 2. Block A — Weg (A)

**Die Änderung** (`git diff`, numstat `2 0`), in `_plan`, in der Schleife, die
`f["rolle"]` vergibt:

```python
         f["rolle"] = "bestaetigung" if i == len(falten) - 1 else "selektion"
+        if f["rolle"] == "bestaetigung":
+            f["name"] = "%s/%s" % (f["von"], f["bis_ausschliesslich"])
         f["training_bis_ausschliesslich"] = (von - timedelta(days=purge)).isoformat()
```

`_jahresfalten`, die Zeile `"bestaetigungsperiode": falten[-1]["name"] …`,
`auswertung.py`, `beispieldaten.py`, `registerbericht.py`: **unberührt**. Der
Plan wurde nur im Speicher gerechnet (`plan_dump.py` → `faltenplan()`),
`python3 faltenplan.py` nie aufgerufen.

| | Ergebnis | Beleg |
|---|---|---|
| ⭐⭐ **A1** | ✔ **9/9** tragen `2026-01-01/2026-09-01` — die Zahl aus 35.1 | `a1_a4_nachher.txt` |
| ⭐ **A2** | ✔ je Bot **ein** Faltenname ersetzt (`2026` → Spanne, bei `elliott_wave` `2026-2027` → Spanne); gemeinsame Falten ungleich **0**, übrige Planfelder ungleich **0**, an der umbenannten Falte ausser dem Namen nichts ungleich **0** — neunmal | `a1_a4_nachher.txt`, `a2_diff.txt`, `a2_plan_vorher.json`, `a2_plan_nachher.json` |
| **A3** | ✔ `selektionsfalten` bei allen neun **ohne** Schrägstrich, je Bot gleich wie vorher (4 bis 9 Falten) | `a1_a4_nachher.txt`, `a2_plan_dump_nachher.txt` |
| **A4** | ✔ `embargo_nach_falten` der Selektionsfalten bei allen neun gleich; die Bestätigungsfalte steht in keiner Embargo-Liste | `a1_a4_nachher.txt` |
| ⭐ **A5** | ✔ **dieselbe** Abbruchstelle: vorher und nachher `KeyError: '2017'` in `auswertung.py:237` (`zulaessigkeit`), aus `teil_a` → `lauf()` Z. 90, rc 1. Beide Belege sind bis auf die Kopfzeile zeichengleich. Keine neue, keine frühere Stelle | `a5_test_vorher.txt`, `a5_test_nachher.txt` |
| ⭐⭐ **A6** | ✔ **nicht schlechter:** vorher **163/2**, nachher **163/2**, dieselben zwei (`G6`, `H3`), **keine dritte**. Gegenprobe beide Male `KeyError: '2017'` | `a6_simulation_vorher.txt`, `a6_simulation_nachher.txt` |

⚠️ **Zu A2 — wie „genau ein String" gezählt ist:** Der Text-`diff` der Plan-JSON
zeigt **zwei** Zeilen je Bot (18 insgesamt): den Faltennamen **und** das Feld
`bestaetigungsperiode`. Das zweite ist kein zweiter veränderter String, sondern
die unveränderte Zeile 338, die den ersten liest (`falten[-1]["name"]`) — der
Auftrag verbietet ausdrücklich, sie zu ändern, *„unter (A) liest sie das
Richtige"*. Gezählt ist deshalb je Bot **ein** veränderter Name; das
Abbruchkriterium „mehr als ein String" hat nicht gegriffen.

⚠️ **Zu A6 — die Meldung von G6 hat sich verändert, die Prüfung nicht:** vorher
`['2018-2019', …, '2026-2027']`, nachher `['2018-2019', …, '2026-01-01/2026-09-01']`.
Die Prüfung sucht weiter `"2020"`/`"2022"` und scheitert aus demselben Grund
(Zweijahresnamen bei `elliott_wave`, TB-88 Antwort 2). H3 ist zeichengleich.

**A7:** Der Auftrag nennt in Abschnitt 6 „A3–**A7** einzeln", definiert aber
nur A1–A6. ⚠️ **Es gibt kein A7** — Abweichung im Auftrag, nichts ausgelassen.

---

## 3. Block B — das Kostenmodul (committet `04d6ce6`)

| | Ergebnis | Beleg |
|---|---|---|
| **B1** | `shared/handelskosten.py`: zwei Konstanten, Modulkopf mit Ort, Sperrlistenpunkt 9, 37.5/38.5, 0,30 % je Rundlauf; keine Funktion, kein Import. Nicht auf die Sperrliste gesetzt | `shared/handelskosten.py` |
| **B2** | neun Ersetzungen; `t3_supertrend/backtest_trend.py` hat den `sys.path`-Block nach dem Muster der anderen acht bekommen | `b2_ersetzen.py`, `git show 04d6ce6` |
| **B3** | ✔ `grep -c "^TRADING_FEE_PCT\|^SLIPPAGE_PCT"` über die neun: **0**; `from handelskosten import`: **9** (heute nachgezählt: 9). Unberührt: je 2 Kopien in den neun `forward_test.py`, `GEBUEHR_PCT` in `messgroessen.py` | `b3_grep.txt` |
| **B4** | ✔ neunmal `0.1 / 0.05`, aus `handelskosten` geladen | `b7_import_nachher.txt` |
| ⭐⭐ **B5** | ✔ Mutation `TRADING_FEE_PCT = 0.999` nur im Modul → **alle neun** lesen `0.999`; Rücknahme → `git diff` zeigt nur die neun geplanten Ersetzungen, das Modul wieder `0.1`, alle neun wieder `0.1 / 0.05`. Nie committet | `b5_mutationsprobe.txt` |
| ⭐ **B6** | ✔ je Bot ein Backtest vorher/nachher, **byte-identisch 9/9** (`cmp`) | `b6_vergleich.txt`, `b6_csv/` |
| **B7** | ✔ alle neun importierbar, rc 0, auch `t3_supertrend` | `b7_import_vorher.txt`, `b7_import_nachher.txt` |

---

## 4. Block C — die Tabellen gegen den Plan (rein lesend)

Werkzeug `c_falten_abgleich.py` (nach TB-88 `m5_falten_abgleich.py`).

| Bot | C1 `_tb72` vorher | C2 `_tb72` nachher | C3 `_vt` vorher | C3 `_vt` nachher |
|---|---|---|---|---|
| `elliott_wave` | gleich | Selektion gleich; Bestätigung Plan `2026-01-01/2026-09-01`, Tabelle `2026-2027` | gleich | wie `_tb72` |
| `t3_supertrend` | gleich | Selektion gleich; Bestätigung Plan Spanne, Tabelle `2026` | **Übermenge** (`2018`) | Selektion **Übermenge** (`2018`); Bestätigung Plan Spanne, Tabelle `2026` |
| übrige sieben | gleich | Selektion gleich; Bestätigung Plan Spanne, Tabelle `2026` | gleich | wie `_tb72` |

⭐ Nach Block A stehen **alle 18 Zeilen** auf „verschieden" — **nur** wegen der
Bestätigungszeile; die Selektionsfalten sind in `_tb72` bei allen neun gleich,
in `_vt` bei acht. Das ist die im Auftrag erwartete Abweichung (Anfrage 23b).
**Nichts gefolgert, nichts repariert, keine Tabelle angefasst.**
Belege: `c_vorher.txt`, `c_nachher.txt`.

**Punkt 4 aus dem zweiten Anlauf** (Herkunft der Faltennamen in `benchmark.py`,
rein lesend) steht unverändert in `d_benchmark_name_herkunft.txt`: `benchmark.py:266`
übernimmt `f["name"]` aus dem Plan und bildet keinen eigenen Namen. ⚠️ Die
Anweisung dazu kam damals abgeschnitten an („…ESE ZAHL NICHT, MISS SIE NACH").

---

## 5. Sondenlauf am Ende (lesend)

`abschluss_sonde_nachher.txt` gegen `schritt0_sonde_vorher.txt`, Abbild
`sperrliste_abbild_2026-09-22.json` (`6a1b732e…`), **kein neues Abbild**:

| | vorher | nachher |
|---|---|---|
| Punkt 2, `faltenplan.py` | `ABWEICHUNG fd3e5018…` (soll `6f96b95d…`) | `ABWEICHUNG 7aa0b8cc…` (soll `6f96b95d…`) |
| Punkt 2, `ergebnisse/faltenplan.json` | gleich `0e54ac5c…` | gleich `0e54ac5c…` |
| Bilanz | 1 in Ordnung, **1 Befund (Punkt 2)**, 12 nicht prüfbar; (ii) 0 | **identisch** |
| Rückgabewert | 1 | 1 |

Sonst ist die Ausgabe zeichengleich (Diff: nur Kopfzeilen und diese zwei Zeilen).

⚠️ **Abweichung vom Auftrag:** Er erwartete „jetzt einen **zweiten** Befund `1`
(Punkt 2, zweiter Pfad `faltenplan.py`)". Gemessen: Der Befund an genau diesem
Pfad bestand **schon vorher**. Das Abbild trägt noch den Hash vor TB-86
(`6f96b95d…`); seit TB-86 (`4daa254`) weicht `faltenplan.py` ab (37.3, erster
Anwendungsfall). TB-90 ändert den Ist-Wert dieses Befunds, nicht die Zahl der
Befunde. **Tatsachennotiz:** `faltenplan.py` war `fd3e5018…` (Stand TB-86) und
ist jetzt `7aa0b8cc…` (Stand TB-90). Planmässig nach 37.3; das neue Abbild
kommt gebündelt nach Punkt 8.

---

## 6. Vergleich gegen die Vormessung des steuernden Chats

Vormessung: `VORMESSUNG_steuernder_chat.md`, Brücken-VM, 07:50–08:00 UTC.
Die Mac-Nachmessung ist ausgeführt; **es gilt die Nachmessung**.

| | Vormessung (VM) | Nachmessung (Mac) | |
|---|---|---|---|
| A1 | 9/9 Spanne | 9/9 Spanne, Zeilen zeichengleich | ✔ |
| A2 | Plan nachher | `a2_vergleich_vormessung.txt`: **inhaltsgleich True**; in dieser Sitzung nachgeprüft: `json.load`-Gleichheit True, 9/9 Bots. Die Dateien sind verschieden gross (33 850 / 38 980 Byte) — **nur Formatierung** | ✔ |
| A2 (Zählung) | „weg/neu, gemeinsame ungleich 0" | zusätzlich geprüft: übrige Planfelder ungleich 0, Bestätigungsfalte ausser Name ungleich 0 | ✔, strenger |
| A3 | keine Spanne, 4–9 Falten | gleich, dazu „gleich vorher: True" | ✔ |
| A4 | unverändert | gleich | ✔ |
| A5 | `KeyError: '2017'` in `zulaessigkeit` (VM) | dieselbe Stelle mit `trading-env`, Z. 237 | ✔ |
| A6 | Gegenprobe ✔, **Tausch-Fall offen** | Tausch-Fall **163/2**, G6 und H3, keine dritte | ergänzt |
| C2/C3 | 18 Zeilen | 18 Zeilen, **zeichengleich** | ✔ |

**Abweichungen von der Vormessung:** keine in den Zahlen. Ausdrücklich zu nennen:
(a) Die Vormessung liess A6-Tausch offen — jetzt gemessen. (b) Die Plan-Dateien
sind byte-verschieden, inhaltlich gleich. (c) Die Vormessung stellt A2 als
„genau ein Name je Bot" dar; der Text-`diff` zeigt zwei Zeilen je Bot (Abschnitt
2). Gezählt ist dasselbe, aber das steht jetzt ausdrücklich da.
Beleg der Nachprüfung: `abschluss_vergleich_vormessung.txt`.

---

## 7. Wurde beim Ändern von `faltenplan.py` gefragt?

Beleg: `abschluss_frage_ask.txt`, aus den lokalen Sitzungsprotokollen gelesen.

| Anlauf | Regel | Edit aufgerufen | Ergebnis |
|---|---|---|---|
| `ffd44be8` | **deny** | 06:46:20.029Z | **nach 4 ms** abgelehnt: *„File is in a directory that is denied by your permission settings."* |
| `3d9a74f7` | **ask** (seit `66eec94`, 07:05:44Z) | 07:06:28.093Z | **nach 35 min 06 s** erfolgreich, ohne einen Protokolleintrag dazwischen |

⭐ **Indiz für „ja, es wurde gefragt":** allow führt in Millisekunden aus, deny
lehnt in Millisekunden ab (gemessen). Eine Wartezeit von 35 Minuten bis zum
Erfolg passt nur zu einer offenen Genehmigungsfrage, die dann bestätigt wurde.
⚠️ **Das ist kein direkter Nachweis:** Das Protokoll verzeichnet die Frage
selbst nicht. Ob der Dialog tatsächlich erschien und bestätigt wurde, kann nur
der Betreiber bestätigen. *Diese Abschlusssitzung hat `faltenplan.py` nicht
geändert und wurde deshalb nicht gefragt.*

---

## 8. Abbruchkriterien — keins gegriffen

| | |
|---|---|
| drei JSON-Hashes | gleich ✔ |
| Datei in `ergebnisse/` entstanden/geändert | nein, 12 = 12 ✔ |
| `python3 faltenplan.py` aufgerufen | nein ✔ |
| A1 | 9/9 ✔ |
| A2 mehr als ein String je Bot | nein (Zählung Abschnitt 2) ✔ |
| A5 Absturz vorverlegt/anders | nein ✔ |
| B5 Rücknahme unvollständig | nein ✔ |
| Datei ausserhalb der erlaubten Menge geändert | Durch **TB-90-Arbeit** nein: `faltenplan.py`, `shared/handelskosten.py`, die neun `backtest_*.py`, `docs/`. ⚠️ Seit `563fb54` ist zusätzlich `.claude/settings.local.json` geändert (`709caf2`, deny → ask) — das ist die Betreiberänderung, die Block A erst möglich machte, keine Änderung dieses Auftrags |

---

## 9. Abweichungen vom Auftrag, gesammelt

1. **Vier Anläufe statt einer Sitzung**; ein Anlauf brach an `deny` statt `ask`
   ab (`5194a0a`). Behoben durch `66eec94`/`709caf2`.
2. **A2** zeigt zwei `diff`-Zeilen je Bot; gezählt ist ein Name (Abschnitt 2).
3. **A7** ist im Auftrag nicht definiert.
4. **Sonde:** kein *zweiter* Befund, sondern derselbe Befund an Punkt 2 mit neuem
   Ist-Hash (Abschnitt 5).
5. **Frage bei `ask`:** nur indirekt belegt (Abschnitt 7).
6. **Punkt 4** aus dem zweiten Anlauf: Anweisung abgeschnitten angekommen.
7. `faltenplan.py` lag von 07:41Z bis zum Abschluss uncommittet im
   Arbeitsbaum; committet in `303a7fd` zusammen mit den neun Nachher-Belegen.

## 10. Offen

Punkt 8 mit Neurechnung nach (A) (Fable 23b); danach das neue Abbild, das den
Befund an Punkt 2 schliesst (37.3). G6 und H3 bleiben rot, beide am Faltenplan
(TB-88). Die neun `forward_test.py` tragen weiter eigene Kosten (eigene Freigabe,
38.5). `handelskosten.py` auf die Sperrliste: Registertext, eigener Schritt.
