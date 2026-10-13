## ET — TB-157: Regelwerk-Nachtrag 13.10.2026 und Nachtrag zum Ergebnis TB-156
*Quelle: `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md`, Commits ⟨S0⟩ `0f2664e`, ⟨E⟩ `18fb519`, ⟨F⟩ = der Commit „TB-157 Abgabe: Ergebnis, Journal ET“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** Die Mac-Sitzung TB-157 hat am 13.10.2026 mit dem Werkzeug aus Anhang B des Auftrags 32 Stücke eingetragen — Fehler Nr. 55 bis 73, die Lehre zu `pgrep`, den Chatnamen mit ausgeschriebenem Datum und die Regeln des Betreibers vom 11.10.2026 (Eröffnung Punkt 9) in `ARBEITSWEISE.md` Abschnitt 0, den Chatnamen auch in `UMZUG.md` Abschnitt 6, einen Block in `BACKLOG.md` Abschnitt 5, den Nachtrag ABN156 (A1, A2, B4) am Ende des Ergebnisses TB-156 — und die zwei Verweise auf das fehlende `ERGEBNIS_TB-155_…` in `LIESMICH.md` und `BACKLOG.md` auf das Ergebnis TB-156 gesetzt. Kein Abbruch; kein Aufruf abgelehnt, keine Bestätigung verlangt.

### Was gemessen ist
- **0a:** HEAD `d9a05fb` und die vier Einträge wie Soll; sha256 des Werkzeugs `d3148fcf…d31d` wie Soll.
- **0b:** die fünf Zieldateien mit Zeilenzahl und md5 wie Soll (2574, 439, 488, 402, 54 Z.); `UEBERGABE.md` 4019 Z., md5 `d2c79950…aced8`.
- **E:** Probe 32 Stücke, 45 eingefügte Zeilen, alle Dateien „gleich“, rc 0; Einfügen rc 0; Vergleich 32 × „Vorkommen 1 · GLEICH“, rc 0; zweiter Lauf rc 2 mit allen 32 Kennungen, md5 vorher und nachher gleich.
- **numstat ⟨S0⟩..⟨E⟩:** ARBEITSWEISE 27/0, UMZUG 2/0, BACKLOG 9/1, LIESMICH 1/1, Ergebnis TB-156 8/0, keine weiteren Dateien, rc 0.
- **J:** Kennung ET wie erwartet (letzte ES).

### Was offen bleibt
- Die Probe des Wächters (EIGEN mit `pgrep -a -x claude` oder über die Elternkette) — eigener Auftrag; bis dahin gilt die Vorsichtsregel, vor jedem Start in Chrome zu prüfen, dass keine andere Sitzung im Repo arbeitet.
- Die Formhinweise der Abnahmen TB-151 und TB-152 und „(o) E10“ — als offener Posten in `BACKLOG.md` geführt, nicht eingeordnet.
- ABN156 B1, B2, B3, B5 sowie Eröffnung Punkt 6 und der Helferauftrag zum Umzug — nicht Teil von TB-157.

*Geschrieben 13.10.2026, 16:35 von der Mac-Sitzung TB-157. Quellenvermerk: siehe Kopf.*
