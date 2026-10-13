## ES — TB-156: Sitzungswächter schreibt den Fensterinhalt ins Log; „nicht angemeldet“ und „API-Abrechnung“ heissen nicht mehr „eingabebereit“

*Quelle: `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`*

**Quelle:** Mac-Sitzung **TB-156**, 13.10.2026; Belege `docs/belege/TB-156/`; Freigabe und Vorgaben im Auftrag `docs/auftraege/MAC_TB-156_waechter_fensterinhalt_fortsetzung.md`. Kein Abbruch; kein Aufruf abgelehnt, keine Bestätigung verlangt.

### Was gemessen ist

- **Bau:** `starte_sitzung.sh` 622 → 723 Zeilen, neu `test_fensterinhalt.sh` (113 Fälle); unter `/bin/bash` 3.2.57: 113 ok, 0 FEHL (zählt `cut` Zeichen: ja, im Terminal).
- **Probe über launchd:** 0 Läufe; je Lauf — (keine Probe: `pgrep -x claude` findet keinen Prozess, Claude Code 2.1.296 trägt den Kernel-Namen `2.1.296`; Wache 4a, Schliess-Ausloeser und Probe des Wächters zählen genau so und sind damit blind); zerschnittene Zeichen — (kein Lauf); vor den Belegen nachgesehen: kein Fund.
- **Unterlagen:** `LIESMICH.md` + 31, `BACKLOG.md` + 8 Zeilen; `nachweis` 14 von 14 `ja`.

### Was offen bleibt

- `Not logged in` und die Zeile bei `API Usage Billing`: erschlossen, nicht gemessen; rc 6 und 7 nur im Test. Der echte Start lief nicht.
- Die Kontoregel ist eine Merkmalliste, kein Beweis.
- Prozesserkennung des Wächters für Claude Code 2.1.296 reparieren (eigener Auftrag), danach die Probe nachholen; bis dahin schützt Wache 4a nicht vor zwei Sitzungen im Repo, und der Schliess-Ausloeser beendet keine. L1 und B1 nennen `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`, das es nicht gibt (Gemessenes: Ergebnis TB-156).

*Geschrieben 13.10.2026 von der Mac-Sitzung TB-156. Quellenvermerk: siehe Kopf.*
