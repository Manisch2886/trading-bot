## EU — TB-159: Agent 1, 3 und 4 abgeschaltet über config/agenten_aus.txt
*Quelle: `docs/ERGEBNIS_TB-159_agenten_aus.md`, Commits ⟨S0⟩ `3a2a700`, ⟨A⟩ `3a5b7bc`, ⟨F⟩ = der Commit „TB-159 Abgabe: Ergebnis, Journal EU“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** Die Mac-Sitzung TB-159 hat am 13.10.2026 auf Wunsch des Betreibers (21:00, „schalte die bewertenden agents ab“) die Agenten 1 (`daily_interpreter.py`), 3 (`market_context_agent.py`) und 4 (`portfolio_interpreter_agent.py`) abschaltbar gemacht und abgeschaltet: Sie fragen zuerst `agent_abgeschaltet(name)` in `shared/claude_client.py`; steht ihr Name in der neuen verfolgten Datei `config/agenten_aus.txt` (Stand: agent1, agent3, agent4), rufen sie die API nicht auf und geben `""` zurück wie bei einem fehlgeschlagenen Aufruf. Der Einbau lief mit dem Werkzeug aus Anhang B zuerst in einer Kopie unter `$TMPDIR`, dort alle Tests grün, dann per `cp`/`cmp` ins Repo. Dazu der neue Test `shared/test_agenten_aus.py` und die Zeile K4v in `BACKLOG.md`. Kein Abbruch. Abgelehnt wurde nur ein zusätzlicher, nicht im Auftrag stehender Prüfaufruf des neuen Tests (nicht wiederholt, nicht umgangen).

### Was gemessen ist
- **0a:** HEAD `300ba31` und die vier Einträge wie Soll; sha256 des Werkzeugs `d5a403dd…c16d` wie Soll.
- **0b:** alle sechs Zieldateien mit Zeilenzahl und md5 wie Soll (134, 60, 84, 174, 496, 10953 Z.).
- **0c/0d:** 18 md5-Zeilen, alle neun Paare gleich; Datenstand 223 Zeilen.
- **Basislauf (3.9.6):** `test_empfehlung_format` 70 `[OK ]`, `test_agent2_kapitalmass` 34/34, `test_agent2_zielfunktion` 41 `[OK ]`, je rc 0.
- **Einbau:** Probe alle Anker „Vorkommen 1“, rc 0; Kopie 1101 Dateien; Einbau 6 Dateien; Vergleich in Kopie und Repo je 9 × GLEICH.
- **Kopie und Nachlauf:** dieselben drei Tests unverändert grün, dazu `test_agenten_aus` 30/30 („Alle 30 Pruefungen bestanden.“), je rc 0.
- **8a:** Datenstand nachher bytegleich mit vorher; `paper_trading_volatility_breakout.db` geändert — Cronjob dieses Bots um 22:50:50 (`forward_test.log` gleiche Zeit), nicht durch die Sitzung.
- **numstat ⟨S0⟩..⟨A⟩:** 21 Zeilen; `agenten_aus.txt` 13/0, `test_agenten_aus.py` 163/0, `claude_client.py` 32/0, die drei Agenten je 4/1 — alle wie Soll.

### Was offen bleibt
- Ob die nächste Wochen-Mail (Cron, Agent 4) ohne KI-Teil und mit der Logzeile „Agent 4 abgeschaltet (config/agenten_aus.txt)“ verschickt wird — erst beim nächsten Wochenlauf sichtbar.
- Die Zeile „Stand der Datei: aus = agent1, agent3, agent4“ des neuen Tests ist nicht eigens festgehalten (das Werkzeug speichert nur die letzte Zeile); der Inhalt der Datei ist über A1 und `cmp` belegt.
- Die irreführende Druckzeile „API-Key gesetzt?“ in den Aufrufern bleibt (ausserhalb von TB-159).

*Geschrieben 13.10.2026, 22:55 von der Mac-Sitzung TB-159. Quellenvermerk: siehe Kopf.*
