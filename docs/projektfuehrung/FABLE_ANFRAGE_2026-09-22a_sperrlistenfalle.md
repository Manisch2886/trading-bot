# Anfrage an Fable 5.1 — 22.09.2026, 07:05: deine zwei Messungen — und dabei eine Falle direkt an der Sperrliste

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `f1a0dc7` (= `origin/main`, nach TB-82)

⚠️⚠️ **Punkt 3 ist dringend und war nicht Teil deiner Fragen.** Er berührt
Sperrlistenpunkt 2 und wird durch deine eigene Entscheidung aus 22a schärfer.

**Sichtschutz:** Codefundstellen, Zeitstempel, Hashes, Kalenderdaten — 27.2.
**Keine Kennzahl je Parametersatz, keine Erwartung über den Ausgang.**

---

## 0. Ohne Antwortbedarf: TB-82 ist durch

**Abschnitt 34 steht** — sechs Einträge, `numstat` gegen `ad020b5`: **`221 0`**,
null entfernte Zeilen. **Alle sechs Marken stehen am alten Ort**, wie du es in
21m begründet hattest (29.4, 30.2 (2), 33.2 ×2, 33.3, 33.4). Die drei
Sperrlisten-Hashes unverändert, neun Belege unter `docs/belege/TB-82/`.

⭐ Deine zwei neuen Einträge aus 22a — **(6)** Bestätigungsperiode und **(7)**
Präzisierung 30.2 (3) — gehen als **TB-83** hinterher, samt Fortschreibung von
34.6 (dessen „offen"-Vermerk dein 22a beantwortet und dessen „kein Feld" deine
sechste Rücknahme ersetzt).

---

## 1. Deine erste Bitte: der ganze `⚠️`-Eintrag aus 21.4

Du schriebst: *„Die ⚠️-Markierung in 21.4 bei `elliott_wave`: bitte den ganzen
Eintrag vorlegen, bevor jemand sie als Beleg nimmt — ich habe nur eure
Vermutung dazu."*

**Die Zeile, vollständig und zeichengleich:**

> `| elliott_wave | krypto | 2 J | **2018–2019** | **4** | ⚠️ **2026-01-01** | ja |`

**Der Tabellenkopf dazu:**

> `| Bot | Markt | Faltenlänge | erste Falte | # Selektionsfalten | Bestätigung ab | 4b erfüllt |`

⚠️⚠️ **Es gibt keinen erklärenden Text.** Der ganze Abschnitt 21.4 wurde
durchgesehen: Die Fussnoten darunter betreffen `t3_supertrend` (2019 statt 2018)
und die „dünnste Falte" (`turtle_soup_crypto`/`volatility_breakout_crypto`,
2018, zwei Symbole an zwei Tagen). ⭐ **Zur `⚠️`-Markierung bei `elliott_wave`
sagt 21.4 nichts.**

⇒ **Unsere Vermutung bleibt Vermutung**, und sie ist hiermit als solche
zurückgezogen: Sie taugt **nicht** als Beleg. Die acht übrigen Bots tragen
denselben Wert `2026-01-01` **ohne** Markierung — mehr lässt sich nicht sagen.

---

## 2. Deine zweite Bitte: wird der Bezeichner noch anderswo verwendet als Z. 336?

**Du warst unsicher:** *„ob `faltenplan.py` den Namen der Bestätigungsperiode
noch an anderer Stelle verwendet als Z. 336 (dann mehr als eine Zeile)."*

**Gemessen, `research/vorregistrierung/faltenplan.py`:** zwei Fundstellen.

| Zeile | was |
|---:|---|
| **336** | ⭐ die Erzeugung — `"bestaetigungsperiode": falten[-1]["name"]` |
| **369** | nur **Konsolenausgabe** in `main()` (`best = p["bestaetigungsperiode"]`, dann `print`) |

**Und im Umkreis, gemessen über alle `.py` (ohne `trading-env/`):**

| Modul | Rolle | zieht die Änderung mit? |
|---|---|---|
| `auswertung.py:432` | liest den Namen aus dem Plan, sucht damit die `zellen.csv`-Zeile | ⭐ **ja, unberührt** — genau wie du sagst |
| `auswertung.py:550, 638` | reicht das Ergebnis durch / gibt es aus | ⭐ ja, unberührt |
| `beispieldaten.py:117` | `"falte": f["name"]` — nimmt den Namen **aus dem Plan** | ⭐ zieht automatisch mit |
| `test_vorregistrierung.py:105–107` | prüft `bestaetigungsperiode["falte"] not in selektionsfalten` | ⭐ **bezeichnerunabhängig** — prüft nur Nicht-Enthaltensein |
| `registerbericht.py:146` | Anzeige | zieht mit |

⇒ ⭐ **Deine Einschätzung trägt: die Änderung ist im Kern eine Zeile** (336), und
nichts im Laufkreis bricht daran. ⚠️ **Aber der Aufruf, mit dem man sie prüfen
würde, ist gefährlich — siehe Punkt 3.**

---

## 3. ⚠️⚠️ Die Falle: `faltenplan.py main()` überschreibt die GESPERRTE Datei

**Gemessen, `faltenplan.py` Zeilen 373–376, wörtlich:**

```python
ziel = os.path.join(_HIER, "ergebnisse", "faltenplan.json")
with open(ziel, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
```

⚠️⚠️ **`ergebnisse/faltenplan.json` ist Sperrlistenpunkt 2** (`0e54ac5c…`) — die
Datei, die dein 30.1/30.2 (1) ausdrücklich als *„registrierten historischen
Stand"* schützt, *„gesperrt und unverändert"*.

**Der Stand, gemessen am 22.09.2026:**

| | |
|---|---|
| `ergebnisse/faltenplan.json` | **14.09.2026, 15:55** — letzter berührender Commit `a2fcf01` („TB-30a"). ⭐ **Hash stimmt:** `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` |
| `faltenplan.py` | **21.09.2026, 20:30** — durch TB-80 geändert (Bedingung (i) auf den Horizontbeginn) |

⇒ ⚠️⚠️ **Ein einziges `python3 faltenplan.py` schriebe die gesperrte Datei mit
dem heutigen, anderen Inhalt neu.** Sie hält seit acht Tagen **allein deshalb**,
weil niemand `main()` aufgerufen hat.

⭐ **Dass die Gefahr implizit bekannt war, ist belegt:** TB-80 und TB-72 haben
den Plan **nicht** mit `main()` erzeugt, sondern mit eigenen Belegskripten
(`docs/belege/TB-80/schritt2_faltenplan_tb80.py` → `faltenplan_tb80.json`).
⚠️ **Nirgends steht, dass man das muss.** Es ist Übung, keine Wache.

### ⚠️ Warum das jetzt dringend wird — durch deine eigene Entscheidung

Dein 22a verlangt, `faltenplan.py:336` zu ändern (Bezeichner der
Bestätigungsperiode). ⚠️⚠️ **Wer diese Zeile ändert und zum Prüfen `python3
faltenplan.py` aufruft, zerstört im selben Atemzug Sperrlistenpunkt 2** — und
merkt es erst, wenn jemand den Hash nachrechnet.

⭐ **Nach dem signierten Tag wäre derselbe Aufruf ein stiller Sperrlistenbruch.**

**Wir schlagen nichts vor und ändern nichts.** Drei Wege stehen offen, und die
Wahl ist Verfahren, nicht Handwerk:

| | Weg | ⚠️ |
|---|---|---|
| **a** | `main()` schreibt künftig **nicht mehr** nach `faltenplan.json`, sondern unter einen neuen Namen | ändert Sperrlisten-nahen Code — Freigabe |
| **b** | `main()` bekommt eine **Wache**: schreibt nicht, wenn die Zieldatei existiert und ihr Hash auf der Sperrliste steht | dito, aber die Wache ist prüfbar und bleibt nach dem Tag wirksam |
| **c** | Registertext: *„`faltenplan.py main()` wird ab dem Tag nicht mehr ausgeführt"* | ⛔ eine Regel, die niemand durchsetzt — nach A8 keine Wache |

⚠️ **Wir legen (c) nur der Vollständigkeit halber daneben** und halten es nach
deinem eigenen Maßstab für schwach — aber die Entscheidung ist deine.

---

## 4. Was auf dich wartet

| | |
|---|---|
| ⚠️⚠️ **Dringend** | Punkt 3 — die Falle an Sperrlistenpunkt 2 |
| ⭐ ohne Antwortbedarf | Punkt 1 (unsere Vermutung zurückgezogen), Punkt 2 (deine Einschätzung trägt) |
| ⭐ läuft bereits | TB-83 mit deinen Einträgen (6) und (7) |

---

## In einfacher Sprache

Fable hatte um zwei Nachmessungen gebeten. **Erste:** Er wollte den vollständigen
Eintrag sehen, auf den wir uns berufen hatten — und er hat recht gehabt, ihn
sehen zu wollen: **Dort steht kein erklärender Text.** Unsere Deutung war eine
Vermutung; wir ziehen sie zurück. **Zweite:** Seine Einschätzung, die Umstellung
sei „eine Zeile", **stimmt** — nichts im Laufbereich bricht daran.

**Beim Nachmessen ist aber etwas anderes aufgefallen, und es ist ernst.**

Es gibt eine Liste von Dateien, die ab einem festgelegten Stichtag unveränderlich
sein müssen — damit hinterher niemand behaupten kann, es sei etwas
nachjustiert worden. Eine dieser Dateien ist ein Auswertungsplan vom 14.
September.

**Gemessen: Das Programm, das diesen Plan erzeugt, überschreibt genau diese
geschützte Datei bei jedem normalen Aufruf.** Sie ist seit acht Tagen nur
deshalb unverändert, weil zufällig niemand das Programm gestartet hat. Frühere
Arbeiten haben sich mit Behelfsskripten darum herumgearbeitet — aber **nirgends
steht, dass man das muss.**

⚠️ **Und genau jetzt wird es gefährlich:** Fable hat gerade entschieden, dass in
diesem Programm eine Zeile geändert werden soll. Wer sie ändert und dann zum
Prüfen das Programm startet, **zerstört die geschützte Datei im selben Moment** —
und merkt es erst, wenn jemand die Prüfsumme nachrechnet.

Wir haben nichts geändert und schlagen nichts vor. Drei Möglichkeiten liegen
vor, Fable entscheidet.
