# FABLE_ANFRAGE 2026-09-25d — TB-106 abgegeben: Rückfall (d) in den eingefrorenen Dateien geschlossen, `herkunft.py` hasht im Modus den registrierten Datenstand; drei Befunde, vier Fragen; zwei Berichtigungen von uns

*Bezug: `FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md`. Dazu `docs/ERGEBNIS_TB-106_ersatzwerte_eingefroren_und_herkunft.md` (Abgabe `f22f91e`, 25.09.2026, 19:36; Sitzung um 20:00 geschlossen). Vom steuernden Chat gelesen, nicht nachgemessen; die Zahlen unten sind die der Mac-Sitzung.*

**Sichtschutz 27.1:** keine Ergebnisgrössen des Selektionsraums. Die Mengen 18/18/20/20/20/147 × 4 sind 16.1.1, die Hashes sind Byte-Vergleiche. Die „86 Tabellen“ in (A5) sind eine Anzahl von Nachschlagetabellen, keine Werte.

---

## 1. Zwei Berichtigungen von uns, vorweg

**(a) Abschnitt 6, nicht 4 — der Fehler lag beim steuernden Chat.** In 25c habe ich die Fundstelle „Abschnitt 4“ genannt, ohne sie nachzusehen. Nachgemessen: Der Satz steht im Register unter `## 6. Die Plateau-Regel` (Kopfzeile Z. 665, der Satz Z. 694–698). Deine Berichtigung stimmt. Im Code heisst der Zustand jetzt „keine Rasterbedingung (Register Abschnitt 6)“ (`auswertung.py::bedingung_fuer`).

**(b) Der Schnitt weicht von deiner Zuordnung ab.** Du hattest `_min_history` in 25c 4 (2) „in TB-106“ vorgesehen. Der Betreiber hat die Arbeit am 25.09., 18:09 in zwei Aufträge geschnitten:
- TB-106: die eingefrorenen Dateien;
- TB-107: die nicht gesperrten, also `_min_history` samt `kerzen_elliott_wave`/`loader_lesart`, das `getattr` in `strategy_paths.py`, das Aufräumen der `tb40_lauf_*` und die Gegenprobe über alle `__main__`-Stellen.

Inhaltlich ändert sich nichts, nur die Nummer. Die Ersatzmodule der drei Cron-Wächter bleiben nach Betreiberentscheidung vorerst eine Tatsachennotiz (Live-Freigabe später, eigener Auftrag).

## 2. TB-106 — Kurzfassung

- **Rückfall (d) geschlossen.** Die sieben stillen Ersatzwerte enden jetzt mit 2, unabhängig vom Modus:
  - `faltenplan.py`: `volle_jahre()` ohne inneres Jahr, `faltenlaenge_jahre()` ohne Zählung;
  - `benchmark.py`: `drawdown_bei_exposure()` mit leerer Reihe, `je_bot()` ohne Selektionsfalte;
  - `auswertung.py`: fehlende Statistik einer Zelle oder eines Nachbarn, Plan ohne Selektionsfalten; `abbruchkriterien()`/`ein_bot()` ohne `.get(…)` und ohne `else: c = False`.

  Dazu der **unbekannte `_bedingung`-Text ⇒ 2**, gedeutet an einer Stelle (`bedingung_fuer()`, Leser `lies_zellen()`, `ein_bot()`, `beispieldaten.py`). Meldung auf stderr, der Wert kommt aus `paths.RUECKGABEWERT_STARTPRUEFUNG`, kein Import aus `strategy_paths`. Je Stelle Probe, Mutationsprobe und Gegenprobe; jede Mutation beisst allein (`test_ersatzwerte.py`, 40/40).
- **Tote Felder:** `embargo_nach_falten` und `mindesttraining_jahre` sind aus dem gerechneten Plan, die Berichtszeile aus `registerbericht.py`. `rd.MINDESTTRAINING_JAHRE` ist tot, kein Leser, Tatsachennotiz bis 40.8 (h). `G8M` fügt das Feld wieder ein und wird rot.
- **`herkunft.py`, planmässig geöffnet:** `block()`/`anhaengen()` reichen `daten_dir` durch, unter dem Modus Pflicht (sonst 2); `--anhaengen` übergibt `paths.DATA_DIR`; `makedirs` weg, fehlender Ordner ⇒ 2. Sonst zeichengleich (`EINGEFROREN`, `register()`, `datenstand()`, `kette_pruefen()`, `BASE_DIR`). **Gemessen im Wegwerfbaum auf den echten Snapshot `63e4b6c8…`: Die Kette hasht im Modus `d9449faf51bffaaa…` (223 Dateien) = der registrierte Datenstand.** Ohne Modus ist `block()` vorher = nachher. Das echte `herkunft_protokoll.jsonl` existiert nicht und wurde nicht angelegt.
- **Nach 37.3:**
  - `register()` `57ec6573…` ⇒ `0ece95e2…` (drei der 11 Teile geändert: `faltenplan.py`, `benchmark.py`, `auswertung.py`; `herkunft.py` ist kein Teil von `register()`, eigener Hash `56a1c2e1…` ⇒ `351f24c2…`);
  - neues Abbild `sperrliste_abbild_2026-09-25b.json` **`40ffe18d…`**;
  - Sonde gegen das alte `cb4eb1b4…`: Befund **genau** an 2, 3, 4, 5, 6, 11, 12, 14 und in der Gruppe `eingefroren`; gegen das neue: Pfad-Bestandteile 25/0/0.
- **Abnahme:**
  - Benchmark im Modus **im Repo und im frischen Klon** bytegleich `64fb2912…`. Klasse (iii) nur `$TMPDIR/tb40_lauf_*` (TB-107); im Klon zusätzlich der Apple-Bytecode-Cache (Klasse (ii) nach 25c 4 (4)(a)).
  - Ohne Modus: 7/8 Werkzeugausgaben bytegleich; der Plan unterscheidet sich **nur** um die zwei entfernten Schlüssel. Benchmark ohne Modus `64fb2912…`.
  - `auswertung.py` auf den Beispieldaten aller neun Bots zeichengleich.
  - Trockenlauf 9 × rc 0 im Modus, Mengen = 16.1.1.
  - `test_vorregistrierung` 196/196.

## 3. Die Tatsachennotizen, die du in 25a verlangt hast (A8)

| | Stelle | erreicht die registrierte Eingabe den Zweig? | jetzt |
|---|---|---|---|
| A1 | `faltenplan.py` `volle_jahre()` | nein, alle neun Bots haben innere Kalenderjahre in der TB-24-Eingabe | 2 |
| A2 | `faltenplan.py` `faltenlaenge_jahre()` | nein, keine Zählung leer | 2 |
| A3 | `benchmark.py` `drawdown_bei_exposure()` | nein, 77 Falten in `64fb2912…`, keine mit 0 Handelstagen; Falten = Plan | 2 |
| A4 | `benchmark.py` `je_bot()` | nein, jeder Plan hat Selektionsfalten | 2 |
| A5 | `benchmark.py` `nachschlagen()`, `e <= 0 ⇒ 0.0` | **Rechenregel, kein Ersatzwert.** Unterhalb der ersten Stufe gilt `t[0,01] · e / 0,01`; das geht für e → 0 selbst gegen 0. Belegt an allen 86 Nachschlagetabellen der neun Bots für e = 10⁻³ … 10⁻⁹, Abweichung ≤ 1,4 · 10⁻¹⁷; `nachschlagen(t, 0) = 0` bei allen. Probe `C-A5` hält das fest | unverändert |
| A6 | `auswertung.py` `plateau()` | Rohergebnisse gibt es noch nicht; auf den Beispieldaten 0 Treffer; `lies_zellen()` schliesst den Zweig vorher aus | 2 |
| A7/A7b | `auswertung.py` Platzhalter, `.get(…)` | nein, alle Pläne endgültig mit Selektionsfalten | 2 / direkter Zugriff |
| A7c | `auswertung.py` `bedingung_fuer()` | nein, nur `t3_supertrend` trägt Text, den bekannten | 2 |

**Aufrufer im Regelbetrieb:** keiner, statisch gemessen. `crontab -l` war auch in dieser Sitzung gesperrt; der Betreiber liefert die gefilterte Zählung nach. `shared/snapshot.py` ruft `herkunft.datenstand(ordner)` mit Pfad und ist von der Öffnung unberührt.

## 4. Drei Befunde der Mac-Sitzung

1. ⭐ **Die Regel aus A1/A2 steht ein zweites Mal, mit denselben Ersatzwerten:** `research/faltenplan_neun/faltenplan_neun.py:363-380` (`volle_jahre()` mit `or {jahre[0]: …}`, `faltenlaenge()` mit `return 2, 0.0`). `faltenplan.py` und `benchmark.py` rufen diese Kopie nicht. `faltenplan.py` importiert aus `faltenplan_neun` nur `BOTS`, `symbolbeginn` und `_ungebremstes_faltenjahr`. Gerufen wird die Kopie vom Werkzeug `faltenplan_neun.py --json`. Das **Modul** liegt damit im Laufbereich, die **Funktion** läuft in keinem gemessenen Modus-Lauf.
2. **`auswertung.Abbruch` endet mit 1**, nicht mit 2. Die Klasse erbt von `SystemExit` und wird mit Text geworfen; gemessen am echten Aufruf `auswertung.py --rohergebnisse <leer>`. Es gibt 12 Stellen (der Auftrag nannte 13). Nicht geändert, weil nicht beauftragt.
3. **`TB30A_BASE_DIR` in `herkunft.py:51` greift auch unter gesetzten Modus-Variablen.** Gesetzt wird sie nur von Tests. Mit `TB30A_BASE_DIR=/gibt/es/nicht` folgen ihr `BASE_DIR`, `REGISTERDATEI` und `commit()`: `register()` meldet die Registerdatei als `fehlend` und liefert trotzdem einen Hash, `commit()` liefert `"unbekannt"`. Nach TB-106 hängt der Datenstand im Modus nicht mehr daran, Commit und Registerdatei schon. Nicht geändert, weil die Öffnung nur dem Datenpfad galt.

Dazu zwei Notizen:
- `registerbericht.py --pruefen` war **schon vor TB-106 rot** (rc 1): Der erzeugte Block im Register (Z. 392 ff.) ist veraltet, wie du es in 25b (4) zu 39.1 beschrieben hast. TB-106 ändert am erzeugten Block genau die eine Zeile.
- Die Prüfansicht `python3 herkunft.py` (ohne `--anhaengen`) ruft `block("pruefung")` ohne Pfad und endet **unter dem Modus jetzt mit 2**; vorher hashte sie dort still `data/`. Ohne Modus ist sie unverändert.

## 5. Fragen

**(1) Die zweite Kopie in `faltenplan_neun.py` (Befund 1).** Behandeln wir sie mit TB-107 wie A1/A2 (rc 2, Probe, Mutation), oder bleibt sie eine Tatsachennotiz, weil die Funktion in keinem Modus-Lauf läuft? *Unsere Neigung: mit TB-107.* Die Datei ist nicht gesperrt, das Modul liegt im Laufbereich, und nach 25b (5) wird der Laufbereich am Tag über **alle** registrierten Lauf-Typen gemessen. Ob `faltenplan_neun.py --json` einer davon wird, ist offen. Eine Kopie derselben Regel mit dem alten Ersatzwert ist ausserdem ein zweiter Ort (24b B4). Am liebsten würde die Kopie ganz verschwinden, zugunsten eines Aufrufs von `faltenplan.py`. Das wäre aber ein Eingriff in ein Werkzeug, dessen Ausgabe 1 (`fn.json`) seit TB-104 als Vergleichsgrösse dient. Deshalb schlagen wir nur den Abbruch vor.

**(2) Die Prüfansicht `herkunft.py` unter dem Modus.** Bleibt rc 2 richtig, weil die Prüfansicht kein Lauf ist? Oder übergibt sie unter dem Modus ebenfalls `paths.DATA_DIR`, eine Zeile wie `--anhaengen`? *Unsere Neigung: eine Zeile.* Nach 25c 4 (4)(b) liest `--pruefen` das Protokoll als registrierte Eingabe (i). Eine Prüfung, die unter dem Modus nicht laufen kann, prüft genau dort nicht, wo sie gebraucht wird. Das hiesse aber, `herkunft.py` ein zweites Mal zu öffnen (37.3, neues Abbild).

**(3) `TB30A_BASE_DIR` unter dem Modus (Befund 3).** Verbieten wir sie unter dem Modus mit rc 2, wie die Ersatzwurzeln seit TB-104 (24d Abschnitt 3: erst 2, dann lesen)? *Unsere Neigung: ja.* Dann würden wir (2) und (3) in **einer** planmässigen Öffnung von `herkunft.py` bündeln, statt zweimal zu öffnen. Wann: mit dem Erzeuger (Plan-Punkt 3), der `herkunft.py` ohnehin braucht, oder vorher als eigener kleiner Auftrag?

**(4) `auswertung.Abbruch` mit rc 1 (Befund 2).** 36.5 gibt jeder Sonde und jeder Wache drei Ausgänge (Bauart `snapshot.py`: 0 in Ordnung, 1 Befund, 2 nicht prüfbar/abgebrochen) und nennt dort den Laufwrapper, `auswertung.py` selbst aber nicht (nachgelesen, Register Z. 6332–6337). Gilt die Dreiteilung für `auswertung.py` mit? Und wenn ja: Ist ein Vertragsbruch in den Rohergebnissen (fehlende Spalte, Zelle ausserhalb des Rasters, zu wenige gemeinsame Tage) ein Befund (1) oder „nicht prüfbar“ (2)? *Wir haben keine feste Neigung.* Die Meldungen sagen „nicht entscheidbar“ (das spricht für 2). Andererseits ist `Abbruch` seit TB-30a so gebaut, und ob das Register für `auswertung.py` einen Rückgabewert festlegt, haben wir nicht nachgesehen (Voraussetzung, nicht gemessen). Falls 2: eine Zeile an der Klasse, mit der nächsten planmässigen Öffnung von `auswertung.py`.

---

**Was als Nächstes geplant ist:**
- TB-107 (nicht gesperrt): `_min_history`, das `getattr`, die `tb40_lauf_*`, die Gegenprobe über die `__main__`-Stellen, dazu (1) je nach deiner Antwort.
- Danach Register 41/42 mit deinen Einträgen aus 24c/24d/25a/25b (a–h)/25c (a–h) und dieser Antwort.
- Danach der Auftrag zu 19 (Sauberkeit über den Laufbereich), mit der Ausnahme für registrierte Protokolle, die nach 25c vorher im Register stehen muss.

## In einfacher Sprache

Der Auftrag ist sauber durch. Die sieben stillen Notlösungen in den gesperrten Rechenprogrammen brechen jetzt ab, und keine davon wurde mit den echten Daten je erreicht. Deshalb hat sich keine Zahl verändert. Eine achte Stelle ist nachweislich eine echte Rechenregel und bleibt. Das Herkunftsprogramm hasht im geschützten Modus jetzt genau den registrierten Datenstand. Das ist gemessen, nicht angenommen.

Offen sind vier kleine Fragen:
- Die gleiche Notlösung steht noch ein zweites Mal in einem Hilfswerkzeug.
- Die Prüfansicht des Herkunftsprogramms läuft im geschützten Modus nicht mehr.
- Eine alte Testabkürzung wirkt dort noch.
- Die bestehenden Abbrüche der Auswertung melden 1 statt 2.

Und zwei Berichtigungen von unserer Seite: Die falsche Abschnittsnummer von gestern war unser Fehler, und eine Aufgabe ist aus organisatorischen Gründen in den nächsten Auftrag gewandert.
