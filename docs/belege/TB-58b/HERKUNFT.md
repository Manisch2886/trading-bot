# Belege TB-58b — Herkunft

Sitzung **TB-58b** (19.09.2026, Mac, `trading-env/bin/python3` 3.9.6), Auftrag
`docs/auftraege/TB-58b.md` (= `logs/auftraege/TB-58b_v2.md`, die Fassung v2).
Sicherungsordner `~/Sicherungen/tb58b_registereintraege_20260919T172832Z/`
(dort zusätzlich `kopien/` mit den zwölf Datenbanken — Sicherung, kein Beleg).

| Datei | Was sie belegt |
|---|---|
| `db_liste.txt`, `db_sha256_vorher.txt`, `db_vergleich_nachher.txt` | 12 `*.db` ausserhalb `trading-env/`, Quersummen vorher, `shasum -c` nachher (12 OK) |
| `datenstand_vorher.txt`, `datenstand_nachher.txt` | `snapshot.py --quelle data --nur-hash`: `d9449faf…`/223 vorher und nachher |
| `snapshot_pruefen_vorher.txt`, `snapshot_pruefen_nachher.txt` | `snapshot.py --pruefen`: `UNVERAENDERT` |
| `registerpruefer_vorher.txt`, `registerpruefer_arbeitsbaum.txt`, `registerpruefer_nachher.txt` | `pruefe_register.py --basis a1e7fb4`: KEIN BEFUND vor der Änderung (A7), auf dem Arbeitsbaum, nach dem Commit |
| `ueberschriften_vorher.txt` | alle `## <Nummer>.`-Zeilen des Registers vor der Änderung — höchste 18 |
| `lock_gegen_metadata.txt` | die 67 Lock-Zeilen gegen `importlib.metadata`: 0 Abweichungen; SHA-256 `96a5c572…` |
| `probe_lock_vorher.txt`, `probe_lock_nachher.txt` | die rc-2-Probe im Wegwerf-Klon (vor dem Registercommit gegen `6236c95`, danach gegen `409d71d`): Kontrolle rc 0, abweichender Lock rc 2, schmutziger Baum rc 2, fehlender Lock rc 2, fremder Interpreter rc 2 |
| `skripte/abschnitte_19_20.md` | der Text, der an das Register angehängt wurde (160 Zeilen) |
| `skripte/lock_gegen_metadata.py`, `skripte/probe_lock.sh`, `skripte/wortlaut_vergleich.py` | die drei Messwerkzeuge |

⚠️ `probe_lock.sh` ist die **korrigierte** Fassung: der erste Entwurf rief
`git revert -q` (die Flagge gibt es nicht), der Revert lief nicht, und die
Proben 2 und 4 massen dadurch denselben Zustand wie Probe 1 bzw. 3. Benannt im
Ergebnisdokument, nicht still berichtigt.
