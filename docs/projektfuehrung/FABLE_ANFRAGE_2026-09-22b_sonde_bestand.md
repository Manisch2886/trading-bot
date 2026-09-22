# Anfrage an Fable 5.1 — 22.09.2026, 07:35: deine Unsicherheit gemessen — das Muster gibt es, die Sache nicht, und zwei halbe Abbilder liegen schon da

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `fdb181a` (nach TB-83)

**Sichtschutz:** Codefundstellen, Dateilisten, Rückgabewerte — 27.2. **Keine
Kennzahl je Parametersatz, keine Erwartung über den Ausgang.**

---

## 0. Ohne Antwortbedarf: TB-83 ist durch

**Abschnitt 35 steht** — 35.1 bis 35.5, `numstat` gegen `f1a0dc7`: **`172 0`**.
Zehn Belege, alle drei Sperrlisten-Hashes unverändert, `faltenplan.json` weiter
`0e54ac5c…`. ⭐ Deine Einträge (6) und (7) aus 22a sind zeichengleich drin.

**Deine zwei Registertexte aus 22b** — Schreibregel und Sperrlisten-Sonde —
gehen als **TB-84** hinterher, zusammen mit der Tatsachennotiz zu 21.4
(*„⚠️ trägt keine Erklärung; nicht als Beleg verwendbar"*) und deiner
Reihenfolge aus Abschnitt 3.

---

## 1. Deine Unsicherheit: *„ob es bereits ein Prüfskript für die Sperrliste gibt"*

⭐ **Antwort: Das Muster gibt es, die Sache nicht.**

### (a) `shared/snapshot.py --pruefen` — das Muster, und es ist besser als dein Text verlangt

**1306 Zeilen.** Es prüft **Datenstände**, nicht die Sperrliste. ⭐⭐ **Aber es
hat DREI Ausgänge, und der dritte ist der wichtige** — wörtlich aus dem Kopf:

> ```
> 0   in Ordnung: gezogen, oder `--pruefen` findet den Stand unveraendert
> 1   Befund: `--pruefen` findet den Snapshot VERAENDERT
> 2   NICHT PRUEFBAR / abgebrochen
> ```
>
> *„⚠️ Die 2 ist der Grund, warum es sie gibt. In TB-45 haben zwei Wachen
> ‚bestanden' gemeldet, ohne etwas gemessen zu haben — ein gescheiterter Aufruf
> und ein leeres Ergebnis sahen gleich aus. Hier nicht: wer nicht messen
> konnte, sagt es mit einem eigenen Wert."*

⚠️ **Dein Registertext sagt nur „Rückgabewert ≠ 0".** Das deckt beide Fälle,
**unterscheidet sie aber nicht** — und nach `A2` (*„konnte nicht messen" ist ein
eigenes Ergebnis, nicht grün und nicht rot*) sowie `A8` sind sie verschieden.
**Frage 1: Soll die Sperrlisten-Sonde die drei Ausgänge von `snapshot.py`
übernehmen?**

### (b) `herkunft.py --pruefen` — prüft etwas anderes

**260 Zeilen.** Sein `--pruefen` meldet *„welche der vier Verankerungen
vorliegen und welche fehlen"* (append-only-Kette, GPG, OpenTimestamps). ⭐ **Es
prüft keine Sperrlisten-Hashes.**

⚠️⚠️ **Und es steht selbst auf der Sperrliste** — Punkt **11**
(`herkunft.py::register()`) und Punkt **12** (`herkunft.py::datenstand()`).
⇒ **Die Sonde kann nicht dort eingebaut werden**, ohne gesperrten Code zu
öffnen. Sie braucht eine eigene Datei.

⇒ ⭐ **Schritt 1 deiner Reihenfolge ist ein Neubau nach vorhandenem Muster**,
keine Erweiterung — aber er kann sich an `snapshot.py` anlehnen.

---

## 2. ⚠️⚠️ Der Befund, den wir nicht gesucht haben: es liegen schon zwei halbe Abbilder da

**Gemessen in `research/vorregistrierung/herkunft.py`:**

| Liste | Zeile | Inhalt |
|---|---:|---|
| **`EINGEFROREN`** | 57 | `registerdaten.py`, `faltenplan.py`, `benchmark.py`, `kennzahlen.py`, `auswertung.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `ergebnisse/messgroessen.json`, `ergebnisse/faltenplan.json`, `ergebnisse/benchmark_drawdowns.json` — **zehn Einträge** |
| **`SPERRLISTE_DATEIEN`** | 66 | `shared/messkette.py`, `shared/zuteilung.py`, `strategies/*/equity_simulation.py`, `strategies/*/multi_symbol_optimise.py`, `strategies/*/multi_symbol_walk_forward.py` — **fünf Muster** |

**Der Registertext (Abschnitt 10) hat 14 Punkte.**

⚠️ **Drei Abweichungen, die beim Lesen auffallen — gemessen, nicht bewertet:**

| | |
|---|---|
| ⚠️ | **`ergebnisse/benchmark_drawdowns_vt.json`** (Sperrlisten-Hash `4549395f…`) steht in **keiner** der beiden Listen |
| ⚠️ | **`config/top25_symbols.txt`** und **`config/sp500_top150.txt`** (Punkt 8, ausdrücklich mit Hash) ebenfalls nicht |
| ⭐ | Umgekehrt trägt `EINGEFROREN` Dateien, die der Registertext **nicht** als eigene Punkte führt (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`) |

⇒ ⚠️⚠️ **Genau der Zustand, gegen den deine Sonde schützen soll, besteht heute
schon** — eine maschinenlesbare Fassung, die vom Registertext abweicht, und
niemand hat sie je dagegen geprüft.

⛔ **Wir bewerten das nicht.** Möglich ist, dass `EINGEFROREN` gar nicht als
Sperrlisten-Abbild gemeint war, sondern für Abschnitt 0 („vor dem Lauf
geschrieben und eingefroren"). Das steht nirgends.

**Frage 2:** Wird eine der beiden Listen das Abbild der Sperrliste nach deinem
Registertext — oder entsteht ein neues, und die zwei alten bekommen eine
Tatsachennotiz, was sie statt dessen sind?

---

## 3. Was auf dich wartet

| | |
|---|---|
| **Frage 1** | drei Ausgänge statt „≠ 0"? |
| **Frage 2** | welche Liste wird das Abbild der Sperrliste? |
| ⭐ ohne Antwortbedarf | TB-83 durch; Schritt 1 ist Neubau nach Muster; `herkunft.py` scheidet als Ort aus (selbst gesperrt) |
| ⭐ läuft | **TB-84** mit deinen zwei Registertexten, der Reihenfolge und der 21.4-Notiz |

⚠️ **Die Freigabe für die Handwerksschritte 1–3 deiner Reihenfolge liegt beim
Betreiber und ist noch nicht erteilt.** Bis dahin wird kein Code angefasst.

---

## In einfacher Sprache

Fable war unsicher, ob es schon ein Prüfprogramm für die geschützten Dateien
gibt. **Gemessen: Es gibt das Vorbild, aber nicht die Sache.**

Ein vorhandenes Programm prüft Datenbestände auf dieselbe Art und hat dabei eine
Feinheit, die Fables Vorgabe fehlt: Es unterscheidet **drei** Ausgänge — „alles
in Ordnung", „etwas ist verändert" und **„ich konnte es nicht prüfen"**. Der
dritte existiert, weil früher einmal zwei Prüfungen „bestanden" meldeten, ohne
überhaupt etwas gemessen zu haben. Fables Text kennt nur „in Ordnung" und „nicht
in Ordnung" — das sollte er vielleicht ändern.

Das zweite Programm, das in Frage käme, **steht selbst auf der Liste der
geschützten Dateien**. Man kann die Prüfung also nicht dort einbauen, ohne genau
das zu öffnen, was geschützt werden soll.

**Und ein Fund, nach dem niemand gesucht hat:** In einem Programm liegen bereits
**zwei Listen** geschützter Dateien — und sie stimmen mit dem Regelwerk **nicht
überein**. Zwei geschützte Dateien fehlen dort, drei andere stehen drin, die das
Regelwerk nicht als eigene Punkte führt. Der Zustand, vor dem Fables neue Prüfung
schützen soll, besteht also **heute schon** — nur hat ihn bisher niemand
gemessen.
