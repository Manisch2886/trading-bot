## EQ — TB-152: Regelwerk-Nachtrag 10.10.2026, 36 Stücke in `ARBEITSWEISE.md`, `UMZUG.md` und `BACKLOG.md`

*Quelle: `docs/ERGEBNIS_TB-152_regelwerk_nachtrag_1010.md`*

**Quelle:** Mac-Sitzung **TB-152**, 11.10.2026, Auftrag `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md` (gebaut am HEAD `6d700d4`). Commits und Hashes stehen im Ergebnis, Belege unter `docs/belege/TB-152/`. Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026). Die Texte der Stücke standen wörtlich im Auftrag; die Sitzung hat sie mit dem abgeleiteten Werkzeug `tb152_einfuegen.py` eingefügt und keinen Wortlaut geändert.

### Was gemessen ist

| | |
|---|---|
| **0** | Arbeitsbaum beim Start genau die vier Einträge aus 0a, HEAD `6d700d4`; die Eröffnungsdatei ist verfolgt, `ablage_soll.py` nennt sie 2-mal. Werkzeug aus dem Werkzeug TB-146 mit 11 Ersetzungen abgeleitet, sha256 `d5855393…f70f5` wie Soll. Ausgang der vier Zieldateien in Zeilen und md5 wie Soll (`0a_status.txt`, `0b_ausgang.txt`) |
| **A** | Prozesszeile der Sitzung trägt `--permission-mode manual` (`a_modus.txt`) |
| **E** | `probe` und `einfuegen` rc 0: 36 Stücke, 131 Zeilen, jeder Anker genau eine Zeile; `vergleich` rc 0, 36-mal zeichengleich; zweiter Lauf rc 2, md5 der drei Dateien unverändert; numstat `ARBEITSWEISE.md` 43/0, `UMZUG.md` 47/0, `BACKLOG.md` 41/0, keine weitere Datei ausser Belegen (`e_*.txt`) |

### Was offen bleibt

- Die Posten (a) bis (p) unter „Nicht in TB-152“ im Auftrag bleiben beim steuernden Chat, darunter die strittige Frage, ob bestehende Zeilen (UMZUG Z. 228, 260, 270–272; ARBEITSWEISE Z. 118, 212, 2480) ersetzt statt nur ergänzt werden (E10).
- Die eingefügten Klarstellungen stehen neben den älteren Zeilen, die noch die alte Lage der Eröffnungsdatei nennen; wer liest, muss beide zusammen lesen, bis darüber entschieden ist.
- Nächste Journalkennung nach EQ: **ER**.

*Geschrieben 11.10.2026 von der Mac-Sitzung TB-152. Quellenvermerk: siehe Kopf.*
