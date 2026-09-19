# Belege TB-58 — Herkunft

Nachgeholt in **TB-58b** (19.09.2026), Auftrag Punkt 8: *„ein Beleg in
`~/Downloads` ist kein Beleg; er existiert auf einem Rechner und in keiner
Version"* (T54.5).

| | |
|---|---|
| Quelle | `~/Downloads/TB-58_startpruefungen.zip`, SHA-256 `3dd53a96f0321085a69e6177a1bafbfd4fad10753380a53d54bedd9c421cde2b`, 37 Einträge (33 Dateien) im Ordner `tb58_startpruefungen_20260919T144616Z/` |
| Übernommen | **25** Dateien, byteweise (`cp -p`), Liste in `tb58_kopierliste.txt` |
| Nicht übernommen | **8** Dateien, weil sie **byteweise identisch** mit bereits versionierten Ständen sind (je `cmp` geprüft): `ERGEBNIS_TB-58_startpruefungen.md` = `docs/ERGEBNIS_TB-58_startpruefungen.md` · `requirements.lock` = `requirements.lock` (Wurzel) · `entwurf/paths_neu.py` = `shared/paths.py` · `entwurf/test_startpruefungen.py` = `shared/test_startpruefungen.py` · `entwurf/paths_alt.py` = `624853b:shared/paths.py` · `entwurf/test_paths_alt.py` = `624853b:shared/test_paths.py` · `entwurf/test_strategy_paths_alt.py` = `624853b:shared/test_strategy_paths.py` · `auftrag_TB-58.md` = `logs/auftraege/TB-58.md`, liegt als **`docs/auftraege/TB-58.md`** |
| Nicht im ZIP, nicht übernommen | die Datenbankkopien der Sitzung (`db/` im Sicherungsordner `~/Sicherungen/tb58_startpruefungen_20260919T144616Z/`) — Sicherung, kein Beleg |
| Secrets | `grep -r -i -l -E "api_key|secret|passw|token|BINANCE_API"`: ein Treffer, das Wort „Secrets" in der Regelzeile des Auftrags |

Ergebnisdokument: `docs/ERGEBNIS_TB-58_startpruefungen.md` (Commit `6236c95`).
