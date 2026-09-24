# FABLE_ANFRAGE 2026-09-24e — Der Nachweis aus 23e läuft „bytegleich" und liest dabei **null** Dateien aus dem Snapshot; drei Anordnungen, die nicht zueinander passen; und eine Mischung, die nach Zirkularität aussieht

*An den Verfahrensprüfer. Bezug: deine Antworten 23d, 23e und 24b. TB-102 ist abgegeben. **Drei Befunde und drei Fragen** — der dritte ist der, über den wir am längsten nachgedacht haben.*

⚠️ **Sichtschutz 27.1 gewahrt:** keine Haltedauer-Zahl, keine Trade-Zahl, keine Faltenlänge.

---

## 0. Zuerst: deine Unsicherheit aus 24b ist ausgeräumt

Du schreibst: *„Unsicher: ob 5.4 ‚gefundene' Trades im Wortlaut sagt oder das aus dem
Funktionsnamen stammt."*

**Gemessen — das Register sagt es, an zwei Stellen:**

| | Wortlaut |
|---|---|
| **5.1 Nr. 6** | „Faltenlänge ein Jahr, zwei Jahre bei unter 30 **gefundenen** Trades je Jahr." |
| **5.4** | „Gerechnet aus den **gefundenen** Trades je vollem Kalenderjahr" — mit der Begründung im selben Absatz: *„Gefunden, nicht ausgeführt: ob ein Trade ausgeführt wird, hängt am Positionslimit — und das ist in diesem Lauf ein Rasterparameter. Eine Faltenlänge, die vom Positionslimit abhinge, wäre keine Festlegung vor dem Lauf."* |

⇒ **Keine Präzisierung nötig, bevor der Erzeuger gebaut wird.** Deine Entscheidung A3
(Signalpfad, keine Simulation) steht auf registriertem Wortlaut. ⭐ *Und der Grundsatz,
den 5.4 dort nennt, ist genau der, um den es in Frage 3 unten geht.*

## 1. ⚠️⚠️ Befund: „bytegleich" ohne eine einzige Datei aus dem Snapshot

Dein 23e verlangt den Nachweis **im Selektionsmodus**, veranschlagt elf Sekunden. TB-102
hat das gemessen — mit Lesehaken, also **woher** gelesen wurde, nicht nur **ob** das
Ergebnis stimmt. Drei Lesarten, drei Ausgänge:

| | Ausgang |
|---|---|
| **Mit `TB30A_BASE_DIR` auf den Snapshot** | ⛔ Abbruch nach 1 s: `haltedauern_je_bot.csv` fehlt im Snapshot. Legt man sie hinein, folgt der nächste Abbruch: Der Snapshot ist flach, das Skript sucht `data/` |
| **Mit den Modus-Variablen der Bots** (`TB_SELEKTIONSWURZEL`) | ⚠️⚠️ **rc 0, bytegleich zur Nachweisdatei — und 222 Kursdateien, 2 Universumsdateien und 1 weitere kommen aus dem REPO. Null aus dem Snapshot.** Bytegleich ist es nur, weil `data/` heute zufällig dem Snapshot gleicht (222/222 gemessen) |
| **Snapshot-Inhalt in Repo-Anordnung** | rc 0, zweimal bytegleich. Einzige Eingabe von ausserhalb bleibt `haltedauern_je_bot.csv` |

⭐⭐ **Das ist „richtiges Ergebnis, falscher Ort" in reiner Form** — TB-98 Befund 1, nur
noch unsichtbarer, weil hier nicht einmal eine Warnzeile fällt. ⇒ **Ein „bytegleich" aus
der zweiten Lesart beweist nichts über den Snapshot.** Hätte TB-102 nur `diff` gemacht,
stünde heute ein erfüllter Nachweis im Protokoll.

**Die Ursache:** `messgroessen.py` **importiert `shared/paths.py` nicht**. Es kennt den
Selektionsmodus der Bots gar nicht; sein einziger Schalter `TB30A_BASE_DIR` ist als Ersatz
für die **Repo-Wurzel** gebaut (für Mutationsproben), nicht für den Snapshot.

## 2. ⚠️ Befund: drei Anordnungen, keine passt zur anderen

| | erwartet Kurse | erwartet Universumsdateien |
|---|---|---|
| **Der Snapshot** | flach | unter `config/` |
| **`shared/paths.py`** unter dem Modus | flach | **flach** (dein 24b A2 behebt genau das) |
| **`messgroessen.py`** | unter **`data/`** | unter `config/` |

⇒ Dein Resolver-Beschluss aus 24b (A2) räumt die zweite Zeile ab. Die dritte bleibt — und
sie betrifft ein Programm, das eine **eingefrorene Registereingabe** erzeugt.

## 3. Die Kette, gemessen

```
Erzeuger (positionen_holen.py)
 ├─ <bot>_alle_trades.csv   (GEFUNDENE Trades)
 │    └─> Faltenlänge (5.4) ──> Faltengrenzen und erste Falte ──> Benchmark-Tabelle
 └─ <bot>_positionen.csv    (AUSGEFÜHRTE Trades — hängen am Positionslimit)
      └─> tb24_haltedauern/auswertung.py   ⚠️ fester Ausgabepfad, kein `--ziel`, keine Sperre
           └─> haltedauern_je_bot.csv      (78e2bc6, NICHT im Snapshot)
                └─> messgroessen.py ──> messgroessen.json (eingefroren)
                     ├─ max_tage ──────> purge_tage ──> Purge / Embargo / Trainingsende
                     │                   ⭐ KEINE Faltengrenze
                     └─ median_balken ─> Untergrenze donchian_period (zwei Bots, Rasterachse)
```

⭐ **Eine gute Nachricht steckt darin:** Würde `haltedauern_je_bot.csv` neu erzeugt,
bewegen sich `messgroessen.json`, Inhalt und Hash von `faltenplan.json` und die
Donchian-Untergrenze zweier Bots — **die Faltengrenzen und die Benchmark-Tabelle aber
nicht.** Die zwei Ketten sind getrennt.

⚠️ **Eine Berichtigung an uns selbst:** Unsere Vormessung sagte, `G8` prüfe
`median_balken`. Gemessen prüft es `max_tage`. Die Vormessung war falsch.

## 4. Drei Fragen

**(1) Welcher Modus ist in 23e gemeint?** Entweder der Nachweis läuft unter
`TB30A_BASE_DIR` — dann braucht es einen Snapshot in Repo-Anordnung oder ein Skript, das
die flache Anordnung liest. Oder `messgroessen.py` wird auf den Resolver umgestellt, damit
deine Entscheidung aus 24b A2 auch hier greift. ⭐ *Wir neigen zum Resolver: Es ist
dieselbe Wurzel wie dein 24b-Beschluss, und danach gibt es einen Weg statt dreier
Anordnungen.* ⚠️ Bis das entschieden ist, **beweist kein „bytegleich" etwas über den
Snapshot.**

**(2) Ist `haltedauern_je_bot.csv` nach 23d eine Eingabedatei?** Gemessene Tatsachen: Sie
ist die einzige Eingabe ausserhalb des Snapshots. Sie entsteht aus den **ausgeführten**
Trades — also aus derselben Stufe, an der der Erzeuger seit TB-26 scheitert (TB-98
Befund 2). ⚠️ **Damit greift deine Entscheidung A3 („Signalpfad, keine Simulation") für
diese Datei NICHT** — sie braucht die Simulation, und zwar wesensmässig. Ihr Erzeuger
`auswertung.py` schreibt ausserdem fest und ohne Sperre nach 36.1.

**(3) ⭐⭐ Ist die Mischung beabsichtigt — und ist sie zirkulär?** Das ist die Frage, um
die es uns eigentlich geht.

5.4 begründet ausdrücklich, warum die Faltenlänge auf **gefundenen** Trades ruht:

> Ob ein Trade ausgeführt wird, hängt am Positionslimit — und das ist in diesem Lauf ein Rasterparameter. Eine Faltenlänge, die vom Positionslimit abhinge, wäre keine Festlegung vor dem Lauf.

⚠️ **Purge, Embargo, Trainingsende und die Donchian-Untergrenze ruhen dagegen auf den
ausgeführten Trades** — und hängen damit an genau dem Positionslimit, das im Raster **eine
Achse** ist. ⇒ Der Grundsatz, mit dem 5.4 eine Abhängigkeit ausschliesst, ist an drei
anderen Stellen nicht angewandt. Entweder gilt er dort aus einem Grund nicht, den wir nicht
sehen — dann gehört er ins Register. Oder er gilt, und dann sind `purge_tage` und die
Donchian-Untergrenze **Festlegungen vor dem Lauf, die von einem Rasterparameter abhängen**.

⭐ *Wir legen das vor, ohne es zu bewerten: Welche Zahlen dabei herauskämen, wissen wir
nicht und haben wir nicht gerechnet.*

## 5. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend. `belege/` bleibt nach 27.1 gesperrt.

---

## In einfacher Sprache

Der Nachweis, den du verlangt hast — die eingefrorene Messdatei einmal aus dem
eingefrorenen Datenbestand nachrechnen —, ist **nicht** geführt, und die Art des
Scheiterns ist lehrreich.

Auf dem einen Weg bricht der Lauf ab, weil eine Eingabedatei im eingefrorenen Bestand gar
nicht liegt. Auf dem anderen Weg läuft er durch und liefert **exakt dasselbe Ergebnis wie
die Vergleichsdatei** — und liest dabei **keine einzige** Datei aus dem eingefrorenen
Bestand, sondern alle aus dem Arbeitsverzeichnis. Dass das Ergebnis stimmt, liegt nur
daran, dass das Arbeitsverzeichnis heute zufällig dieselben Kursdaten enthält. Hätte man
nur die Ergebnisse verglichen statt mitzuschreiben, woher gelesen wird, stünde jetzt ein
erfüllter Nachweis im Protokoll, der nichts beweist.

Dahinter liegt, dass drei Programmteile den Datenbestand **unterschiedlich angeordnet**
erwarten. Deine gestrige Entscheidung räumt eine dieser Unstimmigkeiten ab; eine dritte
bleibt.

Und eine Frage, die grösser ist als dieser Auftrag: Das Regelwerk begründet an einer
Stelle ausdrücklich, dass eine bestimmte Grösse **nicht** von den tatsächlich ausgeführten
Geschäften abhängen darf — sonst hinge eine Festlegung, die vor dem Lauf feststehen muss,
an einem Wert, der im Lauf erst optimiert wird. Genau diese Abhängigkeit haben wir an drei
anderen Stellen gefunden. Ob das beabsichtigt ist, entscheidest du.
