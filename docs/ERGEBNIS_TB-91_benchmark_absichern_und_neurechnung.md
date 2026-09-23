# ERGEBNIS TB-91 — ⛔ ABBRUCH in Schritt 0a: die App-Sitzung lief in der Cloud, nicht auf dem Mac

**Sitzungstitel in der App:** `TB-91 Auftrag aus AKTUELLER_AUFTRAG.md`
**Auftrag:** `docs/auftraege/MAC_TB-91_benchmark_absichern_und_neurechnung.md`
**HEAD beim Start:** `d23bdd1` (Nachfolger von `40bda97`)
**Zeitpunkt:** 23.09.2026, 08:56 UTC
**Belege:** `docs/belege/TB-91/0a_umgebungspruefung.txt`

---

## Kurz

⛔ **Abbruch nach Abschnitt 8, erstes Kriterium:** Die Umgebungsprüfung (0a)
beantwortet Frage **(b)** mit **nein** — es gibt kein `trading-env`, und
`import binance` scheitert. Nach Auftrag: **ABBRUCH und Meldung, keine Rückfrage,
keine Notlösung.** Block A bis D sind **nicht** begonnen; `benchmark.py` und alle
Tabellen sind **unberührt**.

⭐⭐ **Der eigentliche Befund:** Die aus der Claude-App (iOS) gestartete Sitzung
lief **nicht auf dem Mac**, sondern in einem **Cloud-Container von Anthropic**
(`environment_kind: anthropic_cloud`, `origin: ios`, Linux-VM, Python 3.11.15,
frischer Klon von `main` auf den Zweig `claude/tb-91-auftrag-b47rmj`). Die in
ARBEITSWEISE Abschnitt 14 angenommene „App-Sitzung in der angemeldeten
Mac-Sitzung" ist **so nicht eingetreten**. *Genau diese Probe war der Zweck von
Schritt 0a — sie hat angeschlagen.*

---

## 1. Die vier Antworten der Umgebungsprüfung

| | Frage | Antwort | Beleg |
|---|---|---|---|
| **(a)** | Repo-Wurzel, `HEAD` ≥ `40bda97`? | ⚠️ **formal ja** — `pwd` = `git rev-parse --show-toplevel` = `/home/user/trading-bot`, `HEAD` `d23bdd1`, `40bda97` ist Vorfahr. **Aber:** das ist ein Cloud-Klon, nicht `~/trading-bot` auf dem Mac | Beleg, Abschnitt 1 |
| **(b)** | ⭐⭐ `trading-env` da und benutzbar? | ⛔ **NEIN** — `ls: cannot access 'trading-env'`; System-Python 3.11.15; `ModuleNotFoundError: No module named 'binance'` | Beleg, Abschnitt 2 |
| **(c)** | Berechtigungen? | ⚠️ **Datei ja, Wirkung nein** — `.claude/settings.local.json` liegt im Klon: `allow` 83, `deny` 68, `ask` 8 mit den vier Sperrlisten-`.py` (je `Write`/`Edit`). Die Sitzung lief jedoch im Modus `auto` der Cloud-Umgebung; ob die lokale Datei dort gilt, ist **nicht gemessen**. Gewöhnliche Befehle liefen ohne Nachfrage | Beleg, Abschnitt 3 |
| **(d)** | Abo statt API-Abrechnung? | ⚠️ **keine Kopfzeile sichtbar** (Cloud-Sitzung, kein Terminal). Die Sitzungsmetadaten nennen `rateLimitType: five_hour`, `isUsingOverage: false` — das spricht für Abo-Kontingent, ist aber **keine** Anzeige „Claude Max". Kein Hinweis auf „API Usage Billing" | Beleg, Abschnitt 4 |

⭐ **Ergebnis der Probe für die Umstellung:** **nicht viermal ja.** Termius ist für
Aufträge **nicht** erledigt, solange die App keine Sitzung **auf dem Mac**
startet.

## 2. Hashes (nur gelesen)

| Datei | sha256 |
|---|---|
| `benchmark.py` | `3960375a539de8324ccfafaa42596a056fb5dd5c154cd2e05c0ba6a634f3611b` |
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` |
| `faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` |
| `benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` |
| `benchmark_drawdowns_tb72.json` | `e4ba341d3177d455b1c3151f4bb2e0cf7f16fbd516d9b30edd45d0c7dc005e56` |

Vorher = nachher, da nichts ausserhalb von `docs/` geschrieben wurde. ⚠️ Gemessen
im Cloud-Klon, nicht auf dem Mac — gleich nur, soweit der Mac-Stand gepusht ist.

## 3. Schritt 0b

Der Arbeitsbaum war beim Start **sauber** (`git status --porcelain` leer): Die drei
Dateien vom steuernden Chat (`ARBEITSWEISE.md` Abschnitt 14, der Auftrag samt
Zeiger, `FABLE_ANFRAGE_2026-09-23c…`) sind bereits in `d23bdd1` committet. Nichts
zu committen.

## 4. Block A–D

⛔ **Nicht begonnen.** Kein Edit an `benchmark.py`, keine Mutationsprobe, keine
Neurechnung, kein Determinismusvergleich, keine Wache. *Block A wäre technisch
auch ohne `trading-env` machbar gewesen, Block B nicht — der Auftrag bindet aber
die ganze Sitzung an 0a, und eine halbe Abarbeitung in einer anderen Umgebung wäre
genau die Notlösung, die er verbietet.* Zudem gilt nach `CLAUDE.md`: grün in der
Cloud (3.11) heisst nicht grün auf dem Mac (3.9.6).

## 5. Abweichungen vom Auftrag

| | |
|---|---|
| ⚠️ | Die Sitzung lief nicht auf dem Mac — der Auftrag setzt das voraus (`MAC_`-Präfix) |
| ⚠️ | (d) konnte nicht an der Kopfzeile abgelesen werden; ersatzweise Sitzungsmetadaten |
| ⚠️ | Push geht auf den von der Cloud-Umgebung vorgegebenen Zweig `claude/tb-91-auftrag-b47rmj`, nicht auf `main` |

## 6. Was der Betreiber tun müsste

1. In der App prüfen, **wo** eine neue Sitzung läuft: Für Mac-Aufträge muss die
   Sitzung **auf dem Mac** laufen (Desktop-App oder `claude --remote-control` auf
   dem Mac, dann aus der App **verbinden**) — nicht eine neue Cloud-Sitzung aus
   der App heraus anlegen.
2. TB-91 danach unverändert neu starten; Schritt 0a wiederholen.

## In einfacher Sprache

Die Sitzung wurde aus der App gestartet und landete **nicht auf dem Mac**,
sondern auf einem Rechner von Anthropic in der Cloud. Dort fehlt die
Python-Umgebung mit den Handelsbibliotheken, ohne die die Tabelle nicht neu
gerechnet werden kann. Der Auftrag sagt für genau diesen Fall: sofort aufhören
und melden. Das ist geschehen; es wurde nichts verändert.
