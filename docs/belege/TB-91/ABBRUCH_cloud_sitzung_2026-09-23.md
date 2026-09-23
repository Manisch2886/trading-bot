# TB-91 — Abbruch in Schritt 0a (Cloud-Sitzung statt Gerät)

**Datum:** 23.09.2026 · **Sitzung:** Cloud-Sitzung (Claude Code im Web-Container), Branch `claude/tb-91-auftrag-1pgsg0`
**Auftrag:** `docs/auftraege/MAC_TB-91_benchmark_absichern_und_neurechnung.md` (Zeiger-Zeile TB-91 in `AKTUELLER_AUFTRAG.md`, `HEAD` `d23bdd1`)

⛔ **ABBRUCH nach Abschnitt 8, erste Zeile:** Die Umgebungsprüfung (0a) beantwortet Frage (b) nicht.
Nichts aus Schritt 0b, Block A–D ist ausgeführt; keine Datei ausser diesem Beleg ist geändert.

## Die vier Fragen, gemessen

| | Frage | Messung | Ergebnis |
|---|---|---|---|
| (a) | Repo-Wurzel | `pwd` = `git rev-parse --show-toplevel` = `/home/user/trading-bot`; `HEAD` `d23bdd1` (neuer als `40bda97`) | ja — aber **Container-Klon**, nicht `~/trading-bot` auf dem Mac |
| (b) | `trading-env` | `ls -d trading-env` → *No such file or directory*; System-Python `3.11.15`; `import binance, yfinance, pandas` → `ModuleNotFoundError: No module named 'binance'` | ⛔ **nein** |
| (c) | Berechtigungen | `.claude/settings.local.json` vorhanden: `allow` 83, `deny` 68, `ask` 8 | Zählung erfüllt; gewöhnliche Befehle liefen ohne Nachfrage |
| (d) | Abo | aus dem Container nicht ablesbar (keine Kopfzeile/Statusanzeige sichtbar) | offen |

## Ursache

Die Sitzung wurde als **Cloud-Sitzung** gestartet (Linux-Container, frischer Klon), nicht auf dem
**Gerät** (`trading-bot · main`, Laptop-Symbol). `ARBEITSWEISE.md` Abschnitt 14 sagt ausdrücklich:
*„⛔⛔ NICHT die Cloud wählen. Cloud-Sitzungen (Wolkensymbol) haben kein lokales Repo: keine
Kursdaten, kein `trading-env` …"* — genau das ist hier gemessen.

⚠️ Ergänzend: Der erste Start dieser Sitzung fand TB-91 noch **nicht** im Zeiger (`origin/main` stand
auf `40bda97`); erst nach dem Push von `d23bdd1` war die Zeile da.

## Was die Probe für die Umstellung heisst

Die Probe hat **nicht** viermal ja gesagt — nicht weil die Geräte-Sitzung versagt, sondern weil
sie gar nicht auf dem Gerät lief. Für die Frage „ist Termius erledigt?" ist sie **ohne Aussage**.
Neuanlauf: in der App „Neue Sitzung" → **Gerät** wählen, dann derselbe TB-91-Satz.
