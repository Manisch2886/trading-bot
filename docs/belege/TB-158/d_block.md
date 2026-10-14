## EV — TB-158: Probe des Wächters; EIGEN mit `pgrep -a`, cwd und Elternkette
*Quelle: `docs/ERGEBNIS_TB-158_waechter_probe.md`, Commits ⟨S0⟩ `e7b31f8`, ⟨0⟩ `e80cc05`, ⟨A⟩ `0002a28`, ⟨B⟩ `3e18410`, ⟨Abgabe⟩ = der Commit „TB-158 Abgabe: Ergebnis, Backlog, Journal EV“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** Die Mac-Sitzung TB-158 hat am 14.10.2026 zuerst die eigene `claude`-PID (EIGEN) über `pgrep -a -x claude`, das cwd und die Elternkette gemessen (`docs/belege/TB-158/a_eigen.txt`) und dann zwei Probeläufe über den echten Weg (Auslöser `probe_67799` → launchd → `starte_sitzung.sh`) gefahren, belegt in `docs/belege/TB-158/b_probe1_log.txt`, `b_probe2_log.txt`, `b_nach1.txt`, `b_nach2.txt` und `b_probe.txt`. Kein Abbruch; kein Aufruf abgelehnt, keine Bestätigung verlangt.

### Was gemessen ist
- **0a:** HEAD `882b487` und die zwei Einträge wie Soll; sha256 des Werkzeugs `f0a3c21b…c896` wie Soll.
- **0b:** `starte_sitzung.sh` 723 Z., md5 `8ea9eaaa…7f` wie Soll; `BACKLOG.md` 497 Z. und `JOURNAL.md` 10977 Z. mit md5 wie Soll; sha256 von `tb156_werkzeug.py` `86521eba…c0ea` wie Soll.
- **A:** rc 0; (a) `pgrep -x claude` keine, (b) `pgrep -a -x claude` 67799, nur in (b) 67799 — die Handbuchstelle (ohne `-a` fehlen der eigene Prozess und seine Vorfahren) ist damit am Mac bestätigt; Elternkette 68619 → 67799 (claude) → 67796 (login) → 52069 (Terminal); EIGEN 67799, `Probe: ja` wie Soll.
- **B, Lauf 1:** Fenster 24412, eingabebereit nach 15 s, Anmeldung Abo, Ablaufwarnung nein, 8 Zeilen `   | …`, davon 1 ersetzt, Adresse ja, Fenster geschlossen, rc 0; danach im Repo nur EIGEN.
- **B, Lauf 2:** Fenster 24414, eingabebereit nach 6 s, sonst wie Lauf 1, rc 0; danach im Repo nur EIGEN.
- **beleg:** alle fünf Belege 0 zerschnittene Zeichen, 0 Zeilen mit `@`.

### Was offen bleibt
- Der Zweig des echten Starts (Wache 4a, `starte_sitzung.sh` Z. 573–622) ist nicht geprobt.
- Regelwerk-Nachtrag zu Fassung 2 und Fehler ab Nr. 74 — eigener Auftrag.
- Bereinigung der Heimordner-Pfade (in Rohausgaben des Wächter-Logs, etwa „Gemerkt in …“).

*Geschrieben 14.10.2026, 07:10 von der Mac-Sitzung TB-158. Quellenvermerk: siehe Kopf.*
