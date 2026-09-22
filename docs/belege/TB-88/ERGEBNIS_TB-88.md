# TB-88 — Ergebnis: Nachmessung vor Plan-Punkt 3 und Punkt 8

**Sitzung:** Mac, `TB-88`, 22.09.2026 (18:41–20:20 UTC)
**Auftrag:** `docs/auftraege/MAC_TB-88_messung_punkt3_punkt8.md`
**Eingang:** `afe6192` · Schritt-0-Commit `8851f67` · Messstand aller Zahlen: `8851f67`
**Umgebung:** Mac, Python 3.9.6. Alle Läufe mit `trading-env/bin/python3`; M4 Lauf 2
mit **aktiviertem venv** (`source trading-env/bin/activate`), wie im Auftrag verlangt.

⛔ **Keine Programmdatei ausserhalb von `docs/belege/TB-88/` geändert, kein Abbild,
keine Registerzeile, `python3 faltenplan.py` nie aufgerufen.** Der Plan wurde nur
im Speicher über `fp.faltenplan()` berechnet (schreibt nichts). Die drei Hashes
und alle zwölf Dateien in `ergebnisse/` sind vorher und nachher gleich (M6).

---

## Die fünf Antworten

### 1. ⭐⭐ Ist der Bezeichner ein Schlüssel? — **Ja.**

**Die Vergleichszeile** (`research/vorregistrierung/auswertung.py`):

```python
432:    name = plan[bot]["bestaetigungsperiode"]
435:    zeile = df[(df["zelle_id"] == zid) & (df["falte"] == name)]
436:    if zeile.empty:
437:        raise Abbruch(f"{bot}: die Bestaetigungsperiode '{name}' fehlt fuer den "
```

**Die Probe M2** (`m2_bezeichner_probe.py`, Ausgabe `m2_ausgabe.txt`): Beispieldaten
mit dem unveränderten Plan, `ein_bot` mit `bestaetigungsperiode =
"2026-01-01/2026-09-01"` nur im Speicher →

```
auswertung.Abbruch
turtle_soup_stocks: die Bestaetigungsperiode '2026-01-01/2026-09-01' fehlt fuer den Gewinner.
research/vorregistrierung/auswertung.py Z. 437 in bestaetigungsperiode
```

Die Kontrolle mit unverändertem Plan läuft durch (`falte: '2026'`). ⭐ **Die
Vormessung ist in ihrem Kern bestätigt.**

⚠️ Aber nur mit den Tabellen aus `_vt.json`: Mit der registrierten
`benchmark_drawdowns.json` scheitert **schon die Kontrolle**, lange vor Z. 437
(`KeyError: '2017'` in `zulaessigkeit`, Z. 237) — siehe Antwort 2.

⭐⭐ **Zusatzmessung M2b — die beiden Wege aus 22h** (`m2b_wege_a_b_probe.py`,
`m2b_ausgabe.txt`, ebenfalls nur im Speicher):

| Weg | Lage | Ergebnis |
|---|---|---|
| **(A)** | letzte Falte heisst die Spanne; Bezeichner = Faltenname (Z. 338 unverändert) | ✔ **läuft durch**, `falte: '2026-01-01/2026-09-01'` |
| **(B)** | Faltenname bleibt `2026`, Bezeichner = Spanne, **`zellen.csv` trägt den Bezeichner** | ⛔ `Abbruch` an **`auswertung.py:180`** (`lies_zellen`): *„Falten stimmen nicht mit dem Faltenplan ueberein"* |
| **(B′)** | wie (B), `zellen.csv` trägt den Faltennamen (= M2) | ⛔ `Abbruch` an `auswertung.py:437` |

⚠️⚠️ **Das ändert Weg (B) aus 22h:** `auswertung.py:177–182` vergleicht die
**Menge** der `falte`-Werte je Zelle gegen `[f["name"] for f in plan[bot]["falten"]]`.
Schreibt der Erzeuger den Bezeichner in `falte`, bricht es **dort** ab. Weg (B) ist
damit **nicht** nur eine Anforderung an Erzeuger und `beispieldaten.py` — er
braucht zusätzlich eine Änderung an `auswertung.py` (eingefroren, Sperrliste 10
Nr. 5) oder an den Faltennamen des Plans (dann ist es Weg A). *Weg A ist in der
Probe der einzige, der ohne Änderung an `auswertung.py` durchläuft* — gemessen für
`turtle_soup_stocks` mit `_vt.json`-Tabellen; nicht gemessen, was in Registertext,
Abbild und Berichten an Faltennamen hängt (33.3).

**M1 im Einzelnen:**

| | Stelle | gemessen |
|---|---|---|
| (a) | `faltenplan.py:338` | `"bestaetigungsperiode": falten[-1]["name"] if falten else None,` |
| (b) | `faltenplan.py:307` | `f["rolle"] = "bestaetigung" if i == len(falten) - 1 else "selektion"` — ✔ die Bestätigungsfalte **ist** die letzte der Liste. Für `turtle_soup_stocks`: `falten[-1]` = `'2026'`, Rolle `bestaetigung`, Bezeichner `'2026'`, derselbe String (M2-Ausgabe) |
| (c) | `auswertung.py:432/435/437` | **verglichen**, nicht nur berichtet (Zitat oben). Berichtet wird er zusätzlich in Z. 442 (`"falte": name`) und Z. 638 ff. |
| (d) | `beispieldaten.py:117` | `"falte": f["name"], "rolle": f["rolle"], "n_trades": n,` — der **Faltenname**. Dazu Z. 179: `teil[teil["falte"] == f["name"]]` (Tagesreihen, auch Faltenname) |
| (e) | alle `.py` ohne `trading-env/` | 33 Fundstellen ohne die TB-88-Belege (`grep -rn --include='*.py'`; Liste unten). ⭐ **Eine weitere vergleichende Stelle** für diesen Plan: `test_vorregistrierung.py:105–107` (A3: `bp["falte"] not in selektionsfalten`) — vergleicht, bleibt aber mit jeder Spanne wahr. Nur ausgebend: `faltenplan.py:460`, `registerbericht.py:146`, `auswertung.py:550/638`. ⚠️ **Und eine vergleichende Stelle über den Faltennamen:** `auswertung.py:179` (siehe M2b) |

Die übrigen Fundstellen gehören zu **anderen** Planformaten (`bestaetigungsperiode`
ist dort ein Dict mit `von`/`jahre`/`symbole_a`), nicht zu dieser Schlüsselkette:
`research/faltenplan_neun/{faltenplan_neun,test_faltenplan_neun,faltenschranke_messung}.py`,
`research/krypto_historie/{faltenplan,test_faltenplan}.py`,
`research/turn_of_month/auswertung.py`, `research/universum_trockenlauf/universum_trockenlauf.py:278`,
und der historische Beleg `docs/belege/TB-72/schritt3_faltenplan_tb72.py:37/98`
(Feldvergleich zweier Pläne, kein Laufcode).

---

### 2. ⭐ Welche Prüfungen sind rot, und woran hängt jede?

**(d) zuerst — der Test läuft keine einzige Prüfung.** Er stürzt im ersten
Aufruf von Teil A ab, bevor `pruefe()` einmal gerufen ist:

| Lauf | Umgebung | Ausgang |
|---|---|---|
| 1 (`m4_lauf1_python3.txt`) | `python3` = `/usr/bin/python3` 3.9.6, **ohne** venv, wörtlich wie im Auftrag | `RuntimeError: Loader elliott_wave: ModuleNotFoundError: No module named 'binance'` (aus `fp.faltenplan` → Trockenlauf der Loader), rc 1 |
| 2 (`m4_lauf2_trading_env.txt`) | venv **aktiviert** | `KeyError: '2017'` an `auswertung.py:237` (`zulaessigkeit`), aus `teil_a` → `lauf()` Z. 90, rc 1 |

**(a)/(b):** Es gibt **keine Liste gescheiterter Prüfungen** — `0 bestanden,
0 gescheitert`, die Schlusszeile wird nie gedruckt, Rückgabewert **1** (unbehandelte
Ausnahme). ⚠️ *„rot" heisst heute: der Test stürzt ab. Es heisst nicht: einzelne
Prüfungen scheitern.*

**(c) Woran es hängt — gemessen, nicht vermutet:**

`test_vorregistrierung.py:82` liest `ergebnisse/benchmark_drawdowns.json`. Diese
Datei (TB-30a-Stand) trägt für `turtle_soup_stocks` die Falten `2019`–`2026`; der
heutige Plan beginnt bei **`2017`** (`m5_falten_abgleich.txt`). `zulaessigkeit`
schlägt je Selektionsfalte nach → `KeyError: '2017'`. ⭐ **Der Absturz hängt
direkt am Vollzug von Punkt 8.**

**Gegenprobe — was nach Punkt 8 rot bliebe** (`m4_simulation_punkt8.sh`,
`m4_simulation_ausgabe.txt`): der Ordner in ein Wegwerf-Verzeichnis kopiert (wie
Teil H es selbst tut; alles andere per Symlink, damit `test_vorregistrierung.py:533`
die Repo-Wurzel findet), **nur in der Kopie** trägt `benchmark_drawdowns.json`
den Inhalt von `_vt.json`:

| Fall | Ergebnis |
|---|---|
| Gegenprobe (Kopie unverändert) | `KeyError: '2017'`, rc 1 — wie im Repo ✔ |
| Tausch | **163 bestanden, 2 gescheitert**, rc 1 |

| Prüfung | Meldung | hängt an |
|---|---|---|
| **G6** | `elliott_wave - 2020 und 2022 sind Testfalten, keine Trainingsjahre - ['2018-2019', '2020-2021', '2022-2023', '2024-2025', '2026-2027']` | ⚠️ **nicht an Punkt 8.** Die Prüfung sucht die Namen `"2020"` und `"2022"`; `elliott_wave` hat seit TB-61 (`plan_krypto`) **Zweijahresfalten** mit Namen `JJJJ-JJJJ`. Die Annahme der Prüfung stammt aus TB-30a, als alle Krypto-Bots Platzhalter waren (G5-Zweig). Liest keine Benchmark-Tabelle |
| **H3** | `ohne die gesetzte Null aendert sich die Statistik - 'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'` | ⚠️ **nicht an Punkt 8.** Die Probe setzt **vier** Falten (`2019`–`2022`) ohne Trade und rechnet laut eigenem Kommentar mit **sieben** Selektionsfalten (4 von 7 → Median kippt). Seit der ersten Falte `2017` hat `turtle_soup_stocks` **neun** Selektionsfalten: 4 Nullen gegen 5 × 0,10 → Median 0,10 mit und ohne gesetzte Null. Die Probe ist durch die Faltenzahl wirkungslos geworden, nicht durch die Tabelle |

⭐ **Folgerung:** Punkt 8 behebt den **Absturz** — aber der Test wird danach
nicht grün, sondern **163/2**. Die zwei verbleibenden Prüfungen hängen am
Faltenplan (TB-56/TB-61/TB-72), nicht an der Benchmark-Datei. ⚠️ *Und die
Simulation zeigt nur, was der Test mit dem Inhalt von `_vt.json` tut; wie der
Test nach dem Vollzug an diesen Inhalt kommt (Pfad in Z. 82 ändern oder anders),
ist Teil der Vollzugsform — siehe Antwort 4.*

---

### 3. ⭐ Welche Zeilennummern gelten heute, und seit wann weichen sie ab

(`m3_zeilennummern.txt`, Zeile je Commit aus `git show <c>:faltenplan.py`)

| Stelle | Register 35.1 | heute | Zeile entstanden (`git blame`) |
|---|---|---|---|
| Erzeugung `"bestaetigungsperiode": falten[-1]["name"] …` | 336 | **338** | `a2fcf01` (TB-30a) |
| Konsolenausgabe `best = p["bestaetigungsperiode"]` in `main()` | 368 | **460** | `3d46a7b` (TB-61) |

| Commit | Erzeugung | Ausgabe |
|---|---|---|
| `a2fcf01` TB-30a | 168 | 227 |
| `7387cc5` TB-56 | 212 | 271 |
| `3d46a7b` TB-61 | 216 | 248 |
| `e7a4108` TB-72 | 274 | 306 |
| `76c20ec` TB-80 | **336** | **368** |
| **`4daa254`** TB-86 Schritt 2/3 | **338** | **460** |

⭐ **Seit `4daa254`** (TB-86 Schritt 2 und 3: `--ziel`, Voreinstellung,
Einmal-Schreibsperre; +100/−10 Zeilen). Die Vermutung „TB-86 hat oberhalb
eingefügt" stimmt; genannt war `ee4e65c`, das ist der Abschlussbeleg von TB-86 —
der verschiebende Commit ist `4daa254`.

---

### 4. ⭐ Was der Vollzug von Punkt 8 berührt — und ob der Protokollort existiert

(`m5_vollzug_punkt8.txt`, `m5_falten_abgleich.txt`)

**(a)** `registerbericht.py:178` liest `f['symbole_point_in_time']` — ✔ Z. 178 wie
in 23.5. Die Datei dazu wird in **Z. 64** geöffnet:
`ergebnisse/benchmark_drawdowns.json`. Z. 157 nennt denselben Pfad im Berichtstext.

**(b)** `_vt.json` trägt `symbole_handelbar_in_falte` **statt** des alten
Schlüssels — geprüft über **alle** Falten aller neun Bots (nicht nur Stichprobe):
der einzige `symbole*`-Schlüssel ist `symbole_handelbar_in_falte`. ⇒ Mit
`_vt.json` als Eingabe endet `registerbericht.py:178` in `KeyError`. Zusätzlich
trägt `_vt.json` je Bot drei neue oberste Schlüssel (`benchmark`, `handelbar_ab`,
`loader_schranke`).

**(c)** `status` in `_vt.json`: **neunmal `endgueltig`** ✔ (23.5 stimmt). In der
registrierten Datei: vier `endgueltig`, fünf `platzhalter` (alle fünf Krypto-Bots).

**(d) Wer `benchmark_drawdowns.json` liest oder nennt** (alle `.py` ohne
`trading-env/`):

| Stelle | Art |
|---|---|
| `research/vorregistrierung/test_vorregistrierung.py:82` | **liest** (Teile A–H) |
| `research/vorregistrierung/auswertung.py:590` | **liest** (`main()`, auch die Teil-H-Unterprozesse) — ⚠️ Sperrliste 10 Nr. 5 |
| `research/vorregistrierung/registerbericht.py:64` (+ Text Z. 157, Schlüssel Z. 178) | **liest** |
| `research/vorregistrierung/herkunft.py:61` | nennt (Liste `EINGEFROREN`, Eingabe von `register()`) |
| `research/vorregistrierung/benchmark.py:304–305` | Standard-**Ausgabe**pfad (Kommentar Z. 298: hält die Datei bis zum Amendment) |
| `shared/sperrlistensonde.py:105` (+ Doku Z. 71), `shared/test_sperrlistensonde.py:334–335` (H7c) | nennen **`_vt.json`** als „bestimmt, nicht eingetragen" — ändern sich mit dem Vollzug mit |
| `docs/belege/TB-56/…/benchmark_vergleich.py:8`, `docs/belege/TB-80/schritt0_ausgangsstand.py:28` | historische Belege, lesend |

**Faltenabgleich** Plan (im Speicher) gegen die Tabellen: in der registrierten
Datei fehlen für **alle neun** Bots Falten (fünf Krypto-Bots ganz, vier
Aktien-Bots `2017`/`2018` bzw. `2018`). In `_vt.json` fehlt **keine**; ⚠️ **eine
zusätzliche: `t3_supertrend` trägt `2018`**, der Plan beginnt seit TB-72 bei
`2019`. Die Falte stört den Nachschlag nicht (nur Selektionsfalten werden
gelesen), **aber `dd_toleranz` von `t3_supertrend` ist in `_vt.json` und
`_tb72.json` verschieden** (gemessen, Werte nicht wiedergegeben). ⚠️ *Ob Punkt 8
für `t3_supertrend` `_vt.json` oder den TB-72-Stand vollzieht, steht nicht im
Auftrag — offen.*

**(e) Protokollort — `test -f`, nicht geöffnet:**

| Datei | Befund |
|---|---|
| `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl` | **fehlt** |
| `research/vorregistrierung/ergebnisse/herkunft.json` | **fehlt** |
| gleichnamig im Repo | nur `research/turn_of_month/ergebnisse/herkunft_protokoll.jsonl` |
| Pfaddefinition | `research/vorregistrierung/herkunft.py:54`: `PROTOKOLL = os.path.join(_HIER, "ergebnisse", "herkunft_protokoll.jsonl")` |

⚠️ `herkunft.json` ist in `research/vorregistrierung/` **nicht** als
`ergebnisse/herkunft.json` definiert, sondern im Datenvertrag als
`<wurzel>/<bot>/herkunft.json` (`auswertung.py:51`) — also je Bot im
Rohergebnis-Ordner; geschrieben wird sie heute nur von `beispieldaten.py:142`
(in Wegwerf-Ordner). `register()` (Z. 109) ruft im Laufbereich niemand auf; die
Importeure von `herkunft` liegen in `turn_of_month/` (eigenes `herkunft.py`),
`universum_trockenlauf/` und `shared/test_*` (nur `datenstand()`). ✔ Deckt sich
mit 37.4.

---

### 5. ⚠️ Abweichungen von der Vormessung (22h / Auftrag)

| | Vormessung sagt | gemessen ist |
|---|---|---|
| 1 | `auswertung.py`: Filter `zeile = df[…]` auf **Z. 437** | Filter auf **Z. 435**; Z. 437 ist die `raise Abbruch`-Zeile |
| 2 | Weg (B): Anforderung an den Erzeuger, `beispieldaten.py` mitziehen — sonst wird der Test rot | ⚠️⚠️ **zu kurz:** mit dem Bezeichner in `falte` bricht `auswertung.py:180` (Faltenabgleich gegen die Faltennamen des Plans) ab. (B) braucht zusätzlich eine Änderung an `auswertung.py` (Sperrliste Nr. 5). (A) läuft in der Probe durch |
| 3 | „Beide Wege berühren `beispieldaten.py`" | Weg (A) in der Probe **ohne** Änderung an `beispieldaten.py`: es schreibt `f["name"]`, und der ist unter (A) die Spanne (Wirkung liegt im Plan) |
| 4 | Die Zeile hat sich durch TB-86 **`ee4e65c`** verschoben | verschiebender Commit ist **`4daa254`** (TB-86 Schritt 2/3); `ee4e65c` ist der Abschlussbeleg |
| 5 | `test_vorregistrierung.py` „rot" (implizit: Prüfungen scheitern) | **stürzt ab**, 0 Prüfungen gelaufen (`KeyError: '2017'`); nach Punkt 8 simuliert **163/2** — nicht grün |
| 6 | (nicht in der Vormessung) | ohne venv scheitert der Test auch auf dem Mac an `binance` — mit aktiviertem `trading-env` nicht |
| 7 | (nicht in der Vormessung) | `_vt.json` trägt für `t3_supertrend` eine Falte `2018`, die der Plan seit TB-72 nicht mehr hat; `dd_toleranz` dort ≠ `_tb72.json` |

Bestätigt ohne Abweichung: Z. 338 und Z. 307 wörtlich, `beispieldaten.py:117`
wörtlich, die Ausgabe auf **460**, Z. 432, der Wortlaut der `Abbruch`-Meldung,
`herkunft.py:54`, das Fehlen beider Protokolldateien, `registerbericht.py:178`,
neunmal `endgueltig`.

---

## M6 — Hashes

| Datei | vorher (18:41:06Z) | nachher (20:13Z, erneut vor dem Commit) |
|---|---|---|
| `benchmark_drawdowns.json` | `a163c498…36d1ee` | gleich |
| `faltenplan.json` | `0e54ac5c…d32339` | gleich |
| `benchmark_drawdowns_vt.json` | `4549395f…18745d` | gleich |

Alle zwölf Dateien in `ergebnisse/`: `m6_ergebnisse_alle_vorher.txt` =
`…_nachher.txt`. Kein Abbruchkriterium gegriffen.

## Arbeitsbaum

⚠️ **Während der Sitzung vom Betreiber geändert, nicht von TB-88, nicht
committet:** `.claude/settings.local.json`, `docs/projektfuehrung/ARBEITSWEISE.md`,
`docs/projektfuehrung/NACHTRAG_ARBEITSWEISE_6d_richtungsweisend.md` (geändert),
`docs/settings_local_json_2026-09-22_gelockert.vorschlag` (neu). Nach der am
selben Abend in `ARBEITSWEISE.md` eingetragenen Regel ist eine Datei ohne
Anweisung keine Entscheidung dieser Sitzung — sie bleiben liegen. `git status`
ist deshalb am Ende **nicht** leer; die TB-88-Dateien sind alle committet.

## Offen

- **Fable:** Punkt 3 Weg (A)/(B) — mit Abweichung 2 und 3 steht (B) auf einer
  Änderung an `auswertung.py`; 35.1-Zeilennummern 338/460 seit `4daa254`.
- **Fable:** Punkt 8, 10.1 oder 37.3, Form (i)/(ii)/(iii) — und dazu neu: welche
  Tabelle für `t3_supertrend` (`_vt.json` oder TB-72-Stand), und dass der Vollzug
  drei **lesende** Stellen berührt (`test_vorregistrierung.py:82`,
  `auswertung.py:590`, `registerbericht.py:64/178`), eine davon auf der Sperrliste.
- **G6 und H3** bleiben nach Punkt 8 rot; beide hängen am Faltenplan und brauchen
  eine eigene Entscheidung (Testannahmen aus TB-30a).
