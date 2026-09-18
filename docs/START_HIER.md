# START HIER — Trading-Bot-Projekt

**Der Einstieg für jede neue Sitzung.** Angelegt 18.09.2026 (TB-51).

> ⚠️ **Diese Datei wird bei jeder Sitzungsübergabe auf den Stand gebracht**
> (`ARBEITSWEISE.md` Abschnitt 10, Schritt 2). *Ein Einstiegsdokument, dessen
> Stand von letzter Woche ist, führt die nächste Sitzung in die Irre.*

---

## 1. Was das Projekt ist

**Ein regelbasiertes Papierhandelssystem mit neun Bots** — vier auf Aktien, fünf
auf Krypto, alle long-only, nur Spot, nur OHLCV-Daten ab Stundenauflösung, ein
Konto. Es läuft auf einem MacBook per Cronjob und handelt **kein echtes Geld**.

**Die Frage, an der alles gemessen wird:**

> ***Verdient dieses System Geld — und woher wissen wir das?***

⚠️ **Der grösste Teil der Arbeit ist derzeit keine Strategieentwicklung, sondern
die Reparatur der Grundlage**, auf der diese Frage überhaupt beantwortbar wird:
ein vorregistrierter Selektionslauf, dessen Ergebnis nicht nachträglich wählbar
ist.

---

## 2. In dieser Reihenfolge lesen

| # | Datei | wofür |
|---:|---|---|
| **1** | `docs/projektfuehrung/ARBEITSWEISE.md` | ⚠️ **Wie der Betreiber arbeiten möchte. Verbindlich.** Zuerst lesen, nicht überfliegen |
| **2** | `docs/PRUEFPRINZIPIEN.md` | Die Lehren aus fehlgeschlagenen Prüfungen. **Jedes Prinzip hat einen Fall hinter sich** |
| **3** | `docs/projektfuehrung/BACKLOG.md` | Die aktiven Punkte. **Die kanonische Quelle** — bei Widerspruch zu Notizen gilt diese Datei |
| **4** | `docs/UMGEBUNGEN.md` | Mac gegen Cloud. ⭐ *„Grün in der Cloud heisst strukturell nicht grün auf dem Mac."* |
| **5** | `docs/projektfuehrung/JOURNAL.md` | **Das Archiv, rund 4 000 Zeilen.** ⚠️ **Nur öffnen, wenn es um eine konkrete frühere Messung geht** — die Blockbuchstaben werden im Backlog referenziert |

**Daneben, bei Bedarf:** `docs/VORREGISTRIERUNG_neuselektion.md` (das Register,
rund 2 500 Zeilen) · `docs/UEBERGABEPROTOKOLL.md` · die Nachtragsdateien unter
`docs/projektfuehrung/` (Belege, nicht fortgeschrieben).

---

## 3. Die Kette — woran gerade gearbeitet wird

| Rang | Schritt | Stand |
|---:|---|---|
| ~~0–0,82~~ | Vorregistrierung, Krypto-Historie, Ausstiegspfade, Snapshot-Werkzeug, Registernachträge | **erledigt** |
| **0,84** | **Snapshot ziehen** | ⚠️ **technisch möglich seit TB-49 — wird aber erst am Tag des signierten Tags gezogen** (Registertext 5, Backlog F1a) |
| **0,85** | ⭐ **Der grosse Umbau:** 90 Selektionsmodule auf den Snapshot · **Resolver-Modus in `shared/paths.py` als eigener kleiner Schritt** · zwei AST-Tests (kein eigener Datenpfad · **keine Wanduhr**) · Lese-Audit · Cache nach Snapshot-Hash **und** Commit | **die nächste grosse Aufgabe** |
| **0,95** | `auswertung.py` auf **Verfahren B** | danach |
| **Q1** | **Fable-Querprüfung** — ⚠️ **zwischen Auswerter-Umbau und Tag**, nicht früher und nicht später | danach |
| **Tag** | **Signierter Tag + Zeitanker**, und **am selben Tag der Snapshot** | danach |
| **1–5** | TB-30b Mass-Reparatur → Neuselektion → Beta-Bereinigung → `S-B1` → Netting | danach |

---

## 4. Was man wissen muss, bevor man etwas anfasst

| | |
|---|---|
| ⚠️ **Sperrliste** | `strategies/*/live_params.py`, `forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py`, `shared/entscheidungskerze.py`, `shared/paths.py` — **nur mit ausdrücklicher Freigabe des Betreibers** |
| ⚠️ **Die neun `*.db`** | gitignoriert, **nur auf dem MacBook**, **nicht neu berechenbar** — seit Verfahren B die **einzige** OOS-Evidenz des Projekts. **Jede Mac-Sitzung sichert sie als Schritt 0** |
| ⚠️ **`data/`** | 223 Kursdateien, Datenstand-Hash **`d9449faf…`** — **der eine verankerte Wert des Projekts.** Jede Änderung entwertet den registrierten Zustand |
| ⚠️ **Der Umstellungstag** | **2026-09-16T04:42:24Z** — ab hier läuft das einzige Vergleichsfenster Backtest gegen Live |
| ⚠️ **Secrets** | **Es wird gar kein Befehl vorgeschlagen, dessen Ausgabe einen Schlüssel enthalten könnte.** Geprüft wird die Existenz, nie der Wert |
| **Interpreter** | ⭐ immer **`trading-env/bin/python3`** — `/usr/bin/python3` hat kein `binance` |

---

## 5. Was beim Betreiber offen ist

| | |
|---|---|
| ⚠️ **T34.10** | **Mindesttraining 4 Jahre oder 2.** Zwei Faltenpläne mit verschiedenen ersten Falten liegen im Repo, **nur einer steht im Register** — und die Jahreszahl im Registertext stammt aus dem anderen. **Vor dem Tag** |
| ⚠️ **Freigabe `entscheidungskerze.py`** | für die Bündelung aus **Gleichheitsprüfung** aller Quellen · **Datencron** mit Prüfung vor den Bot-Läufen (`TZ=UTC`) · **Kein-Entscheid-Datensatz** in `melde()` · **Drift-Protokollierung**. ⚠️ **In einem Zug**, weil jede Einzeländerung das Objekt bewegt, gegen das Registertext 7 den Backtest vergleicht |
| **Zweiter Umstellungstag** | ins Register, sobald sein Datum existiert: der erste Tag, an dem **alle neun** Bots ohne Rückfall aus `data/` lesen — **aus den Logs zu belegen** |
| **Signierter Tag + Zeitanker** | vorbereitet (SSH-Signierschlüssel liegt), noch nicht gesetzt |

---

## 6. In einfacher Sprache

**Neun Computerprogramme handeln seit Monaten auf dem Papier — mit echten
Kursen, aber ohne echtes Geld.** Die Frage ist, ob sie Geld verdienen würden.

**Das lässt sich heute noch nicht sagen**, und der Grund ist nicht Ungeduld,
sondern Ehrlichkeit: Wer aus vielen Einstellungen die beste heraussucht, findet
immer eine, die in der Vergangenheit gut aussah. **Deshalb wird vorher
aufgeschrieben, wie ausgewählt wird — und danach nicht mehr geändert.**

**Woran gerade gearbeitet wird:** dass dieser Auswahllauf auf einem
**eingefrorenen** Datenstand rechnet, der sich später Stück für Stück nachprüfen
lässt. Das ist unspektakulär und aufwendig — und es ist der Unterschied zwischen
einem Ergebnis, das man glauben muss, und einem, das man prüfen kann.
