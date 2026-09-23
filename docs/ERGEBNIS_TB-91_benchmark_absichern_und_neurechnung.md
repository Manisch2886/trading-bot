# TB-91 — ⛔ ABBRUCH in Schritt 0a (Umgebungsprüfung): Cloud-Sitzung statt Gerät

**Sitzungstitel:** `TB-91`
**Auftrag:** `docs/auftraege/MAC_TB-91_benchmark_absichern_und_neurechnung.md`
**HEAD beim Start:** `d23bdd1` (Nachfolger von `40bda97`)
**Gemessen:** 23.09.2026, 10:01 UTC
**Beleg:** `docs/belege/TB-91/0a_umgebungspruefung_cloud.txt`

## In einfacher Sprache

Die Sitzung ist in der **Cloud** gestartet worden, nicht auf dem Mac. Dort gibt
es kein `trading-env` und keine Kursdaten — die Neurechnung ist so nicht
möglich. Nach Auftrag Abschnitt 1 und 8 heisst das: **Abbruch, keine Notlösung.**
Es wurde **nichts** geändert ausser diesem Dokument und seinem Beleg.

## ⭐ Die vier Antworten der Umgebungsprüfung

| | Frage | Antwort | Beleg |
|---|---|---|---|
| **(a)** | Repo-Wurzel? | ✅ ja — `pwd` = `git rev-parse --show-toplevel` = `/home/user/trading-bot`, HEAD `d23bdd1`, `40bda97` ist Vorfahr. ⚠️ Aber: **Linux-Container** (`uname`: `Linux vm 6.18.44-fc-v37`), nicht `~/trading-bot` auf dem Mac | Beleg (a) |
| **(b)** | ⭐⭐ `trading-env` da und benutzbar? | ⛔ **NEIN** — `trading-env` existiert nicht (`No such file or directory`). System-Python 3.11.15; `import binance, yfinance, pandas` → `ModuleNotFoundError: No module named 'binance'` | Beleg (b) |
| **(c)** | Berechtigungen? | ✅ Zahlen stimmen: `allow` 83, `deny` 68, `ask` 8 mit den vier Sperrlisten-`.py` (je `Write`/`Edit`). Gewöhnliche Befehle liefen ohne Nachfrage. ⚠️ Das ist die **versionierte** Datei aus dem Klon — ob sie in dieser Sitzung **wirkt**, ist ungeprüft | Beleg (c) |
| **(d)** | Abo statt API-Abrechnung? | ⚠️ **Nicht messbar.** Eine Cloud-Sitzung hat keine Kopf- oder Statuszeile, die „Claude Max" oder „API Usage Billing" nennt | — |

⛔ **Abbruchgrund:** (b) ist mit Nein beantwortet, (d) bleibt offen. Beides ist
nach Abschnitt 1 („Fehlt eine Antwort: ⛔ ABBRUCH und Meldung") und Abschnitt 8
(erste Zeile) ein Abbruchkriterium.

## Diagnose

Das ist genau der Fall, den `ARBEITSWEISE.md` Abschnitt 14 (*„Die Sitzung wird
aus der Claude-App gestartet"*) ausschliesst: *„⛔⛔ NICHT die Cloud wählen.
Cloud-Sitzungen (Wolkensymbol) haben kein lokales Repo: keine Kursdaten, kein
`trading-env` …"*. Die Sitzung lief im Cloud-Container mit frischem Klon.

⭐ **Für die Umstellungsprobe heisst das:** Diese Probe hat die App-Sitzung
**auf dem Gerät** nicht geprüft — sie sagt nichts darüber, ob der App-Start
auf dem Mac funktioniert. Sie ist zu wiederholen, mit dem **Laptop-Symbol**
(`trading-bot · main`) in der Geräteauswahl.

## Was NICHT geschehen ist

| | |
|---|---|
| ⛔ | Schritt 0b entfiel — der Arbeitsbaum war beim Start bereits sauber (`git status --porcelain` leer); die dort genannten Dateien liegen seit `d23bdd1` im Repo |
| ⛔ | Block A–D nicht begonnen. `benchmark.py` nicht angefasst, keine Tabelle gerechnet |
| ⛔ | Keine der vier Tabellen angefasst. Hashes zur Kontrolle (nur gelesen): |

| Datei | sha256 |
|---|---|
| `benchmark.py` | `3960375a539de8324ccfafaa42596a056fb5dd5c154cd2e05c0ba6a634f3611b` |
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` |
| `faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` |
| `benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` |
| `benchmark_drawdowns_tb72.json` | `e4ba341d3177d455b1c3151f4bb2e0cf7f16fbd516d9b30edd45d0c7dc005e56` |

## Abweichungen vom Auftrag

- Kein Journalblock: Das ist ein Abbruch, keine Abgabe (Vorbild: TB-90-Abbruch `5194a0a`).
- Die Sitzung arbeitet auf dem vorgegebenen Cloud-Zweig `claude/focused-davinci-l0oouw`, nicht auf `main`.
- Rückfragen an den Betreiber: keine.

⭐ **Die Mac-Sitzung, die TB-91 wiederholt, ersetzt dieses Dokument vollständig**
(wie TB-90 nach seinem Abbruch).
