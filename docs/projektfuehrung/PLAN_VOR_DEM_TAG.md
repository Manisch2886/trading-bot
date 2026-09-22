# Was vor dem signierten Tag fertig sein muss — die konsolidierte Liste

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**Stand:** 22.09.2026, **19:00** Ortszeit · **HEAD:** `ee4e65c`
⭐ **Fortgeschrieben** nach TB-86 und Fable 22f (Punkt 2 fertig, Punkt 2b neu,
eine Zuschreibung berichtigt)
**Geprüft von:** Fable 5.1, `FABLE_ANTWORT_2026-09-22e_liste_vor_dem_tag.md`
**Art:** Planungsdokument. ⛔ **Kein Registertext.** Bei jeder Abweichung gilt
das Register.

⚠️ **Warum es dieses Dokument gibt:** Die Vorbedingungen des Tags standen bisher
an **sieben** Stellen verstreut — Registerabschnitte 10, 11, 13, 16.4, 16.11,
17.10, 19, 21.9, 23.7, 36.3, dazu Fables drei Reihenfolgen aus 36.3, 22d und
22e. **Niemand hatte sie je zusammengeführt.**

---

## Fables Massstab, wörtlich — daran ist jeder Punkt gemessen

> *Der Tag friert zwei Dinge ein: den **Registertext** und den **Commit**, mit dem der Lauf läuft (5e: HEAD = registrierter Commit, sauberer Baum). Daraus folgt der Massstab, und er ist kein Ermessen:*
> - ***Registertext**, der nach dem Tag noch geändert werden müsste, wäre ein Amendment → vor dem Tag.*
> - ***Code**, den der Lauf oder seine Auswertung braucht und der am Tag nicht im Commit ist, könnte nur durch Amendment nachkommen → vor dem Tag.*
> - ***Code, den erst der Betrieb nach dem Lauf braucht** (Live-Pfad, Berichte, die keine Selektionsentscheidung tragen) → nicht vor dem Tag, es sei denn, das Register sagt es ausdrücklich.*

---

## Die Liste, in Fables Reihenfolge (22e Abschnitt b)

### Stufe I — sofort, blockiert nichts

| # | Was | Stand |
|---|---|---|
| **1** | Sperrlisten-Sonde, Abbild, Selbstprüfung, Nullpunkt-Lauf | ⭐⭐ **fertig** (TB-85, `755b3c4`) |
| **2** | `faltenplan.py main()` absichern — Zielpfad und Einmal-Schreibsperre (36.1 (4)) | ⭐⭐ **fertig** (TB-86, `ee4e65c`, 22.09.). ⭐ **M4 bestanden:** `main()` auf den echten gesperrten Pfad → Rückgabe `1`, *„die Datei wurde nicht einmal geöffnet zum Schreiben"*, `0e54ac5c…` unverändert |
| **2b** | ⚠️⚠️ **NEU — das Abbild der Sperrliste ist überholt** | ⛔ **nicht beauftragt.** Sperrlistenpunkt 2 nennt **zwei** Pfade; `faltenplan.py` hat sich durch TB-86 beauftragt geändert (`6f96b95d…` → `fd3e5018…`). ⭐ **Die Sonde meldet es als Befund (`1`) und hat nichts repariert** — genau nach 36.2. Nach **36.6** braucht es ein **neues Abbild unter neuem Namen**, das alte bleibt |
| **4** | Registertext aus 22c/22d: Präzisierung 36.5 (je Bestandteil) · Ergänzung 36.6 (Gruppe „bestimmt") · Tatsachennotiz zu Abschnitt 10 · Registertext „Ort registrierter Werte" samt Tatsachennotiz | ⛔ nicht beauftragt |

### Stufe II — untereinander unabhängig

| # | Was | Stand |
|---|---|---|
| **3** | `faltenplan.py:336` — Bezeichner der Bestätigungsperiode (35.1) | ⛔ **eigene Freigabe**; ⚠️ **erst nach 2** (36.3) |
| **7** | Abbild des **Faltenplans** + Faltenplan-Sonde + Hash (33.3, 30.2 (3)) | ⛔ Freigabe. ⭐ Fable: **7 vor 10** |
| **5** | Messung: woher beziehen die neun Optimierer und Equity-Simulationen Kosten und Slippage? | ⛔ offen — ⚠️ **Voraussetzung von 6** |
| **8** | **Vollzug der Sperrlisten-Änderung** `benchmark_drawdowns_vt.json` (21.9, 23.7) — ⭐ **erweitert:** fertig erst, wenn `test_vorregistrierung.py` **grün** ist und `registerbericht.py` den neuen Schlüssel liest (23.5) | ⛔ Freigabe. ⚠️⚠️ **Blockiert den Tag** (roter Test) — ⭐ **Fable: nicht nach hinten stellen** |

⛔ **Gestrichen aus Punkt 8:** der Zusatz *„plus die Entscheidung W oder C aus
23.3"*. ⭐ **Registerabschnitt 23.7, Nachtrag TB-71** (zitiert in Fable 22e):
*„die Wahl W oder C ist durch den Satz zur Zeitachse gegenstandslos … der
Vollzug braucht nur noch die Betreiberfreigabe aus 21.9."*
⚠️ **Wer den Zusatz in einen Auftrag übernimmt, wartet auf eine Entscheidung, die
es nicht mehr gibt.**

> ⚠️ **Berichtigt am 22.09.2026 nach Fable 22f:** Die erste Fassung schrieb
> diesen Satz **Fable** zu (*„Fable, 22e: …"*). **Er ist Registertext.** Fables
> Begründung, wörtlich: *„Wer in einem Jahr liest, der Verfahrensprüfer habe
> W/C für gegenstandslos erklärt, sucht die Begründung bei mir und findet sie
> nicht — sie steht im Register, und dort gehört sie hin."* ⭐ Dieselbe
> Sorgfalt, die das Projekt bei Aktenzeichen verlangt.

### Stufe III — nach Stufe II

| # | Was | Stand |
|---|---|---|
| **6** | Handwerk „ein Wert, ein Ort" — Punkte 7 und 9 der Sperrliste (22d) | ⛔ Freigabe; ⚠️ **nach 5** |
| **9** | **TB-30b**, Posten 1, 3, 4, 5 (siehe unten) | ⛔ nicht beauftragt; ⚠️ **vor 10** |

### Stufe IV — parallel zu III möglich

| # | Was | ⭐ von Fable ergänzt |
|---|---|---|
| **L** | **Leiter-Skript + die 3⁹-Prüfung** (Registertext 6 (a)–(m), 16.4, 16.11 Zeile 3 und 9), dazu die **Zellenzuordnung** | ⚠️⚠️ **Das Register nennt es wörtlich „Prüfung vor dem Tag"** — aus jeder der **19 683** Stufentabellen muss ein eindeutiger Multiplikatorvektor folgen, **ohne Nachfrage**: *„ein Fall, in dem es fragt, ist ein Fall, in dem das Register unvollständig ist"* |
| **B** | **Vergleichswerkzeug zu Registertext 7** (Backtester-Prüfung; 16.5, 17.7, 16.11 Zeile 4) | ⚠️ Registertext 7: *„**vor dem Selektionslauf** wird für jeden Bot der simulierte Kapitalpfad gegen den Papierpfad gestellt"*. ⭐ **Das Werkzeug muss am Tag im Commit sein; die Messung selbst darf danach liegen** |

### Stufe V — der grösste Posten

| # | Was | Stand |
|---|---|---|
| **10** | ⚠️⚠️ **Der Erzeuger** — schreibt `zellen.csv`, `tagesreihen/`, **`herkunft.json` samt Feld `teile`** (22d), erzeugt den **Lese-Audit** (5e, 17.4), trägt TB-30b **Posten 2 und 6**, unterliegt der Schreibregel 36.1 von Anfang an, und enthält die **Wache gegen Walk-Forward-Aufrufe** | ⛔ **nicht beauftragt, Umfang ungemessen** |

### Stufe VI — zuletzt

| # | Was |
|---|---|
| **11** | Sperrlisten-Vollzug insgesamt · Sonden-Lauf mit Ergebnis `0` oder dokumentierten `2` · Fables Registerprüfgang · **dann der Tag** |
| **13** | ⚠️ **Vorbedingung des Tags selbst:** GPG-Schlüssel und Netzzugang für OpenTimestamps (Registerabschnitt 13, *„offen — Betreiber"*). ⭐ Fable: *„Handwerk vor Punkt 11, kein Verfahren"* |

---

## TB-30b im Einzelnen — was nötig ist und was nicht

| Posten | Inhalt | nötig vor dem Tag? |
|---|---|---|
| **1** | Regimewache an drei Stellen (11.1) — ⭐ Code fertig in `shared/regimewache.py` | ⭐⭐ **ja — Sperrbedingung** |
| **2** | Kapital-Drawdown in `evaluate_combination_multi` (11.2) | ⭐⭐ **ja — Sperrbedingung**, ⭐ **im Erzeuger (10)** |
| **3** | Zwei Achsen durchreichen (11.3) | ⭐ **ja** — ⚠️ **gemessen 22.09.: die Achsen stehen in Registerabschnitt 2**, also im registrierten Raster |
| **4** | `entry_cutoff` je Bot aus dem Register (26.1) | ⭐ **ja** |
| **5** | Die Wache aus 29.4 — ⚠️ **in allen neun** Optimierern (Berichtigung 34.5) | ⭐ **ja** |
| **6** | Embargo 2d und `3b (a)–(e)` | ⭐ **ja — im Erzeuger (10)** |
| **7** | Werkzeugpflege (Symbolzahl 16.1.1, `MIN_HISTORY`-Angleichung 15.8 Nr. 4) | ⛔ **nein** — ⚠️ **mit Fables Bedingung:** *„sofern der Lauf (ii) nicht neu rechnet. Rechnet der Erzeuger oder die Faltenplan-Sonde den Trockenlauf zur Laufzeit nach, doch — dann ist es Teil von 10"* |
| **8** | Neun Walk-Forward-Rechner ersetzen | ⛔ **nein** — ⭐ *„nötig ist nur eine **Wache**, dass keiner im Lauf aufgerufen wird — eine Zeile im Laufwrapper. Das Ersetzen ist Aufräumen nach dem Tag"* |

**Der Schlusssatz der Sperrliste, wörtlich:** *„Der Lauf darf nicht beginnen,
bevor die beiden Bug-Fixes aus Abschnitt 11 eingebaut sind."*

---

## Was diese Prüfung erledigt hat

| | |
|---|---|
| ⭐ | **Ein möglicher vierter Grossposten ist entfallen.** Gemessen 22.09.: Der Selektionsmodus in `shared/paths.py` liest aus dem Snapshot, und der **Live-Pfad ist dabei nicht erreichbar** (`LIVE_DATA_DIR` wird nicht gesetzt, jede Anfrage wirft). Die Optimierer bauen keinen eigenen Pfad |
| ⭐ | **Zwei Posten gestrichen** (TB-30b 7 und 8), **ein Zusatz gestrichen** (W/C) |
| ⚠️ | **Drei Posten hinzugekommen** (L, B, Lese-Audit) — ⭐ **alle drei stehen wörtlich als „vor dem Tag" oder „vor dem Selektionslauf" im Register.** Fable: *„Wer es weglässt, ändert nicht die Liste, sondern das Register"* |
| ⛔ | **Kein Fristurteil.** Fable beurteilt es ausdrücklich nicht; das ist Betreibersache |

---

## In einfacher Sprache

Bis heute stand an **sieben verschiedenen Stellen** im Regelwerk, was vor dem
großen Stichtag fertig sein muss — und an drei weiteren, in welcher Reihenfolge.
**Zusammengeführt hatte es nie jemand.** Das ist hiermit geschehen, und Fable hat
die Liste geprüft.

**Sein Maßstab ist einfach:** Der Stichtag friert Regelwerk und Programmstand ein.
Was danach noch fehlt, ließe sich nur mit einer förmlichen Änderung nachtragen —
also muss alles, was der Lauf braucht, vorher da sein.

**Ergebnis:** Zwei Posten sind gestrichen, ein veralteter Zusatz auch, und ein
befürchteter großer Posten hat sich in Luft aufgelöst — die Kursdaten kommen
bereits aus dem eingefrorenen Bestand, und der laufende ist dabei gar nicht
erreichbar.

**Aber drei Dinge sind dazugekommen**, und keines davon ist klein: ein Programm,
das die Budgetstufen aus **19 683** möglichen Fällen ohne Nachfrage ableitet; ein
Werkzeug, das die Simulation gegen den echten Papierhandel stellt; und das
Leseprotokoll des Laufs. **Alle drei stehen wörtlich im Regelwerk als „vor dem
Tag" — sie waren nur nirgends aufgeschrieben.**

⚠️ **Und einer der Punkte blockiert den Tag schon heute:** Ein Test ist rot, seit
einer eigenen Änderung. Fable sagt ausdrücklich, er gehöre **nicht nach hinten**.
