# TB-91 — `benchmark.py` nach 36.1 absichern, dann die Tabelle einmal neu rechnen

**Sitzungstitel:** `TB-91`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD beim Schreiben:** `40bda97` (nach TB-90)
**Registergrundlage:** **36.1** (Schreibregel), **38.1** (Weg A, seit TB-90 im Code), Fable **23b** (Neurechnung nach (A), Determinismusbedingung)
**Freigaben:** Betreiber 22.09. (Punkt 3 und 8) · Betreiber 23.09., 10:40 (`benchmark.py` nach 36.1 absichern)

⭐⭐ **Diese Sitzung wird zum ersten Mal aus der Claude-App auf dem Gerät
gestartet, nicht über Termius.** Deshalb beginnt sie mit einer
Umgebungsprüfung — **mit ABBRUCH, nicht mit Rückfrage**, wenn etwas fehlt.

---

## 0. Der Anlass, in zwei Sätzen

⚠️⚠️ **`benchmark.py` trägt dieselbe Falle, die TB-86 bei `faltenplan.py`
geschlossen hat** — und ihr eigener Kommentar beschreibt sie: *„ohne diesen
Schalter überschriebe jeder Lauf sie"*. Die Voreinstellung von `--ziel` ist
`ergebnisse/benchmark_drawdowns.json` (**Sperrlistenpunkt 4**), und geschrieben
wird mit `open(ziel, "w")` — **ohne Einmal-Schreibsperre**.

⭐ Und genau dieses Programm soll die Tabelle neu rechnen (Fable 23b). **Erst
absichern, dann rechnen.**

---

## 1. ⭐⭐ Schritt 0a — die Umgebungsprüfung (nur bei App-Start)

**Vier Fragen, jede mit Beleg. Fehlt eine Antwort: ⛔ ABBRUCH und Meldung, keine
Rückfrage, keine Notlösung.**

| | zu prüfen | wie |
|---|---|---|
| **(a)** | Läuft die Sitzung in der **Repo-Wurzel**? | `pwd`, `git rev-parse --show-toplevel`, `git --no-optional-locks log --oneline -1` — `HEAD` muss `40bda97` sein oder neuer |
| **(b)** | ⭐⭐ Ist **`trading-env`** da und benutzbar? | `trading-env/bin/python3 --version` **und** ein Import, der die Bot-Abhängigkeiten braucht (etwa `python3 -c "import binance, yfinance, pandas"`). ⚠️ **Das ist die wichtigste Frage** — ohne das venv sind A5, A6 und jede Planrechnung nicht möglich |
| **(c)** | Greifen die **Berechtigungen**? | `.claude/settings.local.json` lesen: `allow` ≥ 83, `deny` ≥ 68, `ask` = 8 mit den vier Sperrlisten-`.py`. Und: Bist du für gewöhnliche Befehle **ohne Nachfrage** durchgekommen? |
| **(d)** | Läuft die Sitzung über das **Abo**? | Was die Kopfzeile/Statusanzeige nennt. ⛔ Steht dort „API Usage Billing", **ABBRUCH** |

**Alle vier Antworten kommen ins Ergebnisdokument**, auch wenn sie unauffällig
sind. ⭐ *Das ist die Probe für die Umstellung: Sagt sie viermal ja, ist Termius
für Aufträge erledigt.*

## 2. Schritt 0b — der Arbeitsbaum

Im Arbeitsbaum liegen zwei Dateien vom steuernden Chat, **beide committen:**
`docs/projektfuehrung/ARBEITSWEISE.md` (`numstat 75 0` — Abschnitt 14: App-Start,
Sitzungstitel, „Abbruch wird gemessen", `deny` gegen `ask`) und
`docs/auftraege/MAC_TB-91_benchmark_absichern_und_neurechnung.md` samt dem
umgestellten `AKTUELLER_AUFTRAG.md`; dazu
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-23c_zwei_erzeuger_ungesichert.md`
(die Anfrage, die den Befund aus Block A an den Verfährensprüfer meldet — sie nennt
⚠️ **zwei** ungesicherte Erzeuger: `benchmark.py` und `messgroessen.py`; ⛔ **du fässt `messgroessen.py` NICHT an**, das ist eingefroren und liegt bei Fable).
Danach `git status --porcelain` leer.

**Dann messen:** `sha256` von `benchmark.py` und von den drei
Sperrlisten-Tabellen (`benchmark_drawdowns.json`, `faltenplan.json`,
`benchmark_drawdowns_vt.json`) — **vorher**.

---

## 3. Block A ⭐⭐ — `benchmark.py` nach 36.1 absichern

⭐ **Das Muster steht fertig in `faltenplan.py`** (TB-86, Commit `4daa254`):
`voreinstellung_ziel()` und die Schreibsperre mit
`os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)`. **Lies es und bau
es gleichartig** — nicht neu erfinden, nicht „verbessern".

| | was zu tun ist | Registertext |
|---|---|---|
| **A1** | Die **Voreinstellung** von `--ziel` zeigt nicht mehr auf einen Sperrlistenpfad, sondern auf einen Pfad mit **Zeitstempel**, wie bei `faltenplan.py` | 36.1 (3) |
| **A2** | Geschrieben wird mit **`O_CREAT\|O_EXCL`** statt `open(…, "w")`. Existiert das Ziel: **Rückgabewert `1`**, Meldung, **die Datei wird nicht einmal zum Schreiben geöffnet** — auch bei identischem Inhalt | 36.1 (2), 36.5 |
| **A3** | `--ziel` bleibt und wirkt wie bisher | — |

⛔ **Sonst nichts an `benchmark.py`.** Keine Rechenfunktion, kein Docstring einer
gesperrten Funktion, keine Formatierung. ⭐ *Die vier gesperrten Rechenfunktionen
(23.5) dürfen in keiner Zeile berührt werden — belege das mit einem `diff`, der
nur `main()` und die neue Hilfsfunktion zeigt.*

### Die Mutationsprobe (wie TB-86 M4)

⭐⭐ **Setze `main()` testweise auf den echten gesperrten Pfad an**
(`--ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns.json`) und
belege: **Rückgabe `1`**, Meldung, und der Hash von `benchmark_drawdowns.json`
**unverändert**. ⛔ Weicht der Hash ab: **ABBRUCH**.

---

## 4. Block B ⭐⭐ — die Tabelle einmal neu rechnen

**Fable 23b, zeichengleich:**

> Die Tabelle, die der Lauf liest, wird **nach** der Umsetzung von Weg (A)
> (Punkt 3, TB-90) **einmal** neu gerechnet — mit `benchmark.py`
> (Sperrlistenpunkt 4/6, unverändert), auf dem dann gültigen Plan, mit `--ziel`
> auf einen neuen Pfad nach der Schreibregel 36.1, mit Beleg und Hash. Ihre
> Bestätigungszeile trägt den Bezeichner nach 35 (`2026-01-01/2026-09-01`).

**Ziel:** `research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`

⚠️ **Der Lauf rechnet lange.** Er darf nicht an einem Zeitlimit sterben — starte
ihn so, dass er durchläuft, und belege Anfang und Ende mit Zeitstempel.

**Zu belegen:** der Aufruf, die Laufzeit, der `sha256` der neuen Datei, und dass
die drei alten Tabellen **unverändert** sind.

---

## 5. Block C ⭐⭐⭐ — der Determinismusnachweis

**Fable 23b, zeichengleich:**

> **Bedingung an die Neurechnung — der Determinismusnachweis:** Die neu
> gerechnete Tabelle muss `benchmark_drawdowns_tb72.json` für **alle neun Bots
> in allen Werten reproduzieren**; der einzige zulässige Unterschied ist der Name
> der Bestätigungszeile (und, sofern die Tabelle ihn führt, ein Feld, das diesen
> Namen wiederholt). Ein `diff`, der etwas anderes zeigt, ist ein **Befund**,
> kein Ergebnis … Die Tabelle wird in diesem Fall **nicht** vollzogen.

**Der Vergleich, strukturiert statt als Text-`diff`:** Beide Dateien laden, je
Bot und je Falte **jeden Wert** vergleichen. Die Bestätigungszeile heisst in der
alten Tabelle `2026` (bei `elliott_wave` `2026-2027`), in der neuen
`2026-01-01/2026-09-01` — **diese Zuordnung ist die einzige zulässige
Abweichung**.

| | zu belegen |
|---|---|
| **C1** | Zahl der Bots, Falten, Felder, die verglichen wurden — ⭐ *ein Vergleich, der nichts findet, weil er nichts angesehen hat, ist kein Vergleich* |
| **C2** | **Jede** Abweichung ausser dem Namen der Bestätigungszeile, mit Bot, Falte, Feld, beiden Werten |
| **C3** | `dd_toleranz` je Bot: gleich? ⚠️ **Das ist die Zahl, die Sperrlistenpunkt 4 registriert** |
| **C4** | `status`: neunmal `endgueltig`? |

⛔⛔ **Findest du eine Abweichung ausser dem Namen: kein Abbruch der Sitzung,
sondern ein BEFUND.** Miss ihn vollständig aus — welcher Bot, welche Falte,
welches Feld —, schreib ihn ins Ergebnisdokument und **vollziehe nichts**. *Dann
hat sich zwischen TB-72 und heute etwas bewegt, das nicht der Name ist, und das
zu finden ist wertvoller als eine Tabelle.*

⚠️ **Sichtschutz 27.1:** Die Werte selbst gehören **nicht** in die Meldung an
Fable — nur „gleich" oder „an Stelle X verschieden". Ins Ergebnisdokument dürfen
sie.

---

## 6. Block D — die Wache aus 23a

Faltenmenge der **neuen** Tabelle je Bot gegen den gerechneten Plan — mit
`docs/belege/TB-90/c_falten_abgleich.py`. ⭐ **Erwartung: alle achtzehn Zeilen
„gleich", auch die Bestätigungszeile** — das ist der Punkt der ganzen Übung.
Weicht eine ab, gehört sie mit Bot und Falte ins Ergebnisdokument.

---

## 7. ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔ | **Kein Vollzug von Punkt 8** — kein Registertext, Sperrlistenpunkt 4 bleibt, wie er ist |
| ⛔ | **Kein neues Abbild**, die Sonde wird nicht angepasst |
| ⛔ | `benchmark_drawdowns.json`, `_vt.json`, `_tb72.json`, `faltenplan.json` werden **nicht angefasst** |
| ⛔ | `faltenplan.py` wird nicht geändert (TB-90 hat das erledigt) |
| ⛔ | `handelskosten.py` kommt **nicht** auf die Sperrliste — eigener Schritt |

## 8. ⛔ Abbruchkriterien

| | |
|---|---|
| ⛔ | Die Umgebungsprüfung (0a) beantwortet eine der vier Fragen nicht |
| ⛔ | Ein Hash von `benchmark_drawdowns.json`, `faltenplan.json`, `_vt.json` oder `_tb72.json` ändert sich |
| ⛔ | Die Mutationsprobe schreibt doch |
| ⛔ | Eine der vier gesperrten Rechenfunktionen in `benchmark.py` ist berührt |
| ⛔ | Eine Datei ausserhalb von `benchmark.py`, der **einen** neuen Tabelle und `docs/` ist am Ende geändert |

⭐ **Abbruchkriterium heisst ABBRUCH und Meldung — nie Rückfrage.**
⚠️ **Ein Befund in Block C ist KEIN Abbruchkriterium**, sondern das Ergebnis.

---

## 9. Ins Ergebnisdokument

`docs/ERGEBNIS_TB-91_benchmark_absichern_und_neurechnung.md`, Belege in
`docs/belege/TB-91/`.

1. ⭐ **Die vier Antworten der Umgebungsprüfung** — vollständig, auch wenn
   unauffällig
2. Der `diff` von `benchmark.py` und der Nachweis, dass die gesperrten
   Rechenfunktionen unberührt sind
3. Die Mutationsprobe mit Rückgabewert und Hash
4. Der Neurechnungslauf: Aufruf, Laufzeit, Hash der neuen Datei
5. ⭐⭐ **Block C vollständig** — Zählung des Verglichenen und jede Abweichung
6. Block D, alle achtzehn Zeilen
7. Die Hashes aller vier Tabellen und von `benchmark.py`, **vorher und nachher**
8. ⚠️ **Jede Abweichung** von diesem Auftrag ausdrücklich

**Danach Commit und Push**, Journalblock nach der üblichen Form.

---

## In einfacher Sprache

Zwei Dinge, und das erste ist eine Reparatur, die niemand geplant hatte.

**Das Programm, das die Vergleichstabelle rechnet, hat dieselbe Schwachstelle,
die vor zwei Tagen an anderer Stelle gefunden wurde:** Ruft man es ohne Angabe
auf, überschreibt es die geschützte Tabelle — und es hat keine Sperre, die das
verhindert. Im Programm steht sogar ein Kommentar, der genau das beschreibt.
Deshalb wird es zuerst abgesichert, nach demselben Muster wie damals, und die
Probe dafür ist, dass es sich weigert, die geschützte Datei anzufassen.

**Dann wird die Tabelle einmal neu gerechnet** — nötig, weil der
Bestätigungszeitraum seit gestern anders heisst.

⭐ **Und daraus wird zugleich ein Beweis, den es bisher nicht gibt:** Die neue
Tabelle muss der alten in **jeder einzelnen Zahl** gleichen; nur der eine
Zeilenname darf anders sein. Stimmt das, ist belegt, dass der Rechenweg
reproduzierbar ist und sich seit Monaten nichts verschoben hat. ⚠️ Stimmt es
nicht, wird **nichts** eingefroren — dann ist die Abweichung der eigentliche
Fund, und sie wird ausgemessen statt weggerechnet.
