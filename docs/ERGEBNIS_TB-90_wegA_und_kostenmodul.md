# TB-90 — Ergebnis: ⛔ ABBRUCH vor Block A (Zwischenstand)

**Sitzungstitel:** `TB-90` · **Stand:** 23.09.2026 · **HEAD beim Abbruch:** `04d6ce6`
**Auftrag:** `docs/auftraege/MAC_TB-90_wegA_und_kostenmodul.md` · Belege: `docs/belege/TB-90/`

⚠️ **Dieses Dokument ist eine Abbruchmeldung, nicht das Ergebnisdokument nach
Abschnitt 6.** Es wird von der Sitzung vervollständigt, die Block A ausführt.

---

## 1. Der Abbruchgrund

Der Auftrag erwartet für `research/vorregistrierung/faltenplan.py` **eine
Genehmigungsfrage** („EIN Genehmigungsklick ist gewollt"). Gemessen: In
`.claude/settings.local.json` steht die Datei unter **`deny`**
(`Write(research/vorregistrierung/faltenplan.py)`,
`Edit(research/vorregistrierung/faltenplan.py)`), und `ask` ist leer. Ein
deny-Eintrag fragt nicht, er lehnt ab. Das Edit-Werkzeug hat ohne Frage
abgelehnt:

```
File is in a directory that is denied by your permission settings.
```

⛔ **Die Sperre wurde nicht umgangen** (kein Schreiben über Bash oder Python).
Sie ist genau dafür da. Block A, A1–A6 nachher und C2 sowie der Nachher-Teil
von C3 sind deshalb **nicht ausgeführt**.

**Was es zum Weitermachen braucht (Betreiber):** Die beiden
`faltenplan.py`-Einträge von `deny` nach `ask` verschieben (oder für eine
Sitzung entfernen). Die TB-86-Absicht, dass „der einzige Klick bleibt", wird
nur mit `ask` erreicht.

---

## 2. Was vor dem Abbruch erledigt ist

| | Stand | Beleg |
|---|---|---|
| Schritt 0 | committet `53b35ce`; Hashes und lesender Sondenlauf vorher | `schritt0_hashes_vorher.txt`, `schritt0_sonde_vorher.txt` (rc 1, Befund Punkt 2 wie seit TB-86) |
| A2 vorher | Plan im Speicher (`faltenplan()`, nie `main()`) | `a2_plan_vorher.json`, `plan_dump.py` |
| A5 vorher | `KeyError: '2017'` in `auswertung.py:237` (`zulaessigkeit`) | `a5_test_vorher.txt` |
| A6 vorher | 163 bestanden / 2 gescheitert (G6, H3) | `a6_simulation_vorher.txt` |
| **Block B** | ⭐ **vollständig**, committet `04d6ce6`: B3 0/9, B4, B5 Mutationsprobe mit vollständiger Rücknahme, B6 bitidentisch 9/9, B7 importierbar 9/9 | `b*.txt`, `b6_csv/` |
| C1/C3 vorher | tb72: 9× gleich; vt: 8× gleich, `t3_supertrend` Übermenge (`2018`) | `c_vorher.txt` |
| **Punkt 4** | Herkunft der Faltennamen, rein lesend (unten) | `d_benchmark_name_herkunft.txt` |

**Hashes beim Abbruch:** Alle zwölf JSON-Dateien in `ergebnisse/` und
`faltenplan.py` sind **zeichengleich mit Schritt 0**, darunter
`benchmark_drawdowns.json` `a163c498…`, `faltenplan.json` `0e54ac5c…`,
`benchmark_drawdowns_vt.json` `4549395f…` und `faltenplan.py` `fd3e5018…`
(noch **nicht** geändert). Keine Datei in `ergebnisse/` entstanden.

---

## 3. Punkt 4 — Herkunft der Faltennamen in den Benchmark-Tabellen

⚠️ **Abweichung:** Die Anweisung zu Punkt 4 kam in der Sitzung **abgeschnitten** an
(sie beginnt mit „…ESE ZAHL NICHT, MISS SIE NACH"). Welche Zahl nachzumessen war,
ist nicht überliefert. Gemessen wurde deshalb die Herkunft vollständig, und
**es gilt diese Messung**.

`benchmark.py` (Hash `3960375a…`, nur gelesen) bildet **keinen eigenen Namen**:

| Zeile | |
|---|---|
| 220 | `plan = fp.faltenplan(mess)` |
| 224 | `p = plan[bot]` |
| 246 | `for f in p["falten"]:` |
| **266** | `eintrag["falten"][f["name"]] = {` — die **einzige** Schlüsselbildung (AST: 1 Zuweisung) |

Der Name entsteht nur in `faltenplan.py:291` (`_jahresfalten`). Nach Weg (A)
trüge eine **neu gerechnete** Tabelle deshalb `2026-01-01/2026-09-01` als
Bestätigungsschlüssel. Die vorhandenen Tabellen tragen weiter `2026` bzw.
`2026-2027` (`elliott_wave`), in `tb72` und `vt` bei allen neun Bots.
`benchmark_drawdowns.json` hat Falten nur für die vier Aktien-Bots
(Bestätigung `2026`, Selektion 2019–2025); die fünf Krypto-Bots stehen dort
ohne Falten. Einzelheiten im Beleg.

---

## 4. Offen für die Fortsetzung

Block A (die Änderung in `_plan`), A1–A6 nachher, C2, C3 nachher, der
Sondenlauf am Ende mit altem und neuem `faltenplan.py`-Hash, danach das
vollständige Ergebnisdokument und der Journalblock. ⛔ Kein Journalblock in
dieser Sitzung: Der Auftrag ist nicht abgeschlossen.
