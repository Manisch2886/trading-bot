# TB-69, Schritt 4 — Regelliste NACHHER und der Nachweis, dass nichts verloren ging

**Stand:** `docs/projektfuehrung/ARBEITSWEISE.md` auf `3b74651` (Arbeitsbaum = HEAD), 80 018 B, 1 428 Zeilen, **26** Abschnitte (`## …`, neu: 0), 15 Unterabschnitte (unverändert).
**Vorher:** `5a1f5e1`, 70 905 B, 1 293 Zeilen, 25 Abschnitte — Liste in `regelliste_vorher.md`, **SOLL 117 Regeln (76 A, 41 S)**.

## 1. Jede Regel der Vorher-Liste findet sich wieder — je Nummer, mit neuem Ort

Spalte „Ort im Text“ = derselbe Abschnitt wie vorher, Zeilen um die Einfügungen verschoben (Zeilen 1–22: +0; 23–25: +3, Kopfvermerk; 26–667: +133, Kopfvermerk + Checkliste; ab 668: +135, dazu der 6d-Vermerk). Spalte „Checkliste“ = die Zeile in Abschnitt 0, die die Regel abhakt (nur A-Regeln). Der Wortlaut im Text ist bei allen 117 zeichengleich (Nachweis 3 unten); die Ortsangabe wurde aus der Vorher-Liste mit dem gemessenen Versatz berechnet und an den drei Hunk-Grenzen gegen `git diff` geprüft.

| Nr | Ort im Text (neue Zeilen) | Checkliste (Abschnitt 0) | Befund |
|---:|---|---|---|
| R1 | Kopf (6) | — (S) | wiedergefunden |
| R2 | Kopf (8) | — (S) | wiedergefunden |
| R3 | 1 (161) | Z. 41 | wiedergefunden |
| R4 | 1 (164–169) | — (S) | wiedergefunden |
| R5 | 1 (171–177) | Z. 125 | wiedergefunden |
| R6 | 1 (179–185, 198–199) | Z. 104 | wiedergefunden |
| R7 | 1 (187–196) | Z. 125 | wiedergefunden |
| R8 | 1 (201–204) | Z. 71 | wiedergefunden |
| R9 | 1 (206–207) | — (S) | wiedergefunden |
| R10 | 2 (217–222) | Z. 69 | wiedergefunden |
| R11 | 2 (223–234) | Z. 70 | wiedergefunden |
| R12 | 2 (235–250) | Z. 72 | wiedergefunden |
| R13 | 2 (252–266) | Z. 107 | wiedergefunden |
| R14 | 2 (268–274) | — (S) | wiedergefunden |
| R15 | 2 (275–279) | Z. 47 | wiedergefunden |
| R16 | 2 (281–285) | Z. 79 | wiedergefunden |
| R17 | 2 (286–307) | — (S) | wiedergefunden |
| R18 | 2 (309–313) | — (S) | wiedergefunden |
| R19 | 2 (315–319) | Z. 148 | wiedergefunden |
| R20 | 2 (321–328) | Z. 73 | wiedergefunden |
| R21 | 3 (333–349) | Z. 146 | wiedergefunden |
| R22 | 3 (346–349) | Z. 146 | wiedergefunden |
| R23 | 4 (354–362) | Z. 138 | wiedergefunden |
| R24 | 4 (364–379) | Z. 138 | wiedergefunden |
| R25 | 5 (383–384) | — (S) | wiedergefunden |
| R26 | 5 (385–387) | — (S) | wiedergefunden |
| R27 | 5 (388–389) | — (S) | wiedergefunden |
| R28 | 5 (390–391) | Z. 80 | wiedergefunden |
| R29 | 5 (392–398) | — (S) | wiedergefunden |
| R30 | 5b (403–412) | — (S) | wiedergefunden |
| R31 | 5b (414–429) | — (S) | wiedergefunden |
| R32 | 5b (431–445) | — (S) | wiedergefunden |
| R33 | 5b (447–452) | Z. 155 | wiedergefunden |
| R34 | 5b (454–462) | Z. 155 | wiedergefunden |
| R35 | 5b (471–495) | Z. 139 | wiedergefunden |
| R36 | 5b (497–514) | — (S) | wiedergefunden |
| R37 | 5b (516–517) | — (S) | wiedergefunden |
| R38 | 5b (519–521) | — (S) | wiedergefunden |
| R39 | 6 (527–528) | Z. 83 | wiedergefunden |
| R40 | 6 (530–537) | Z. 82 | wiedergefunden |
| R41 | 6 (539–545) | Z. 81 | wiedergefunden |
| R42 | 6b (550–552) | Z. 100 | wiedergefunden |
| R43 | 6b (554–560) | Z. 101 | wiedergefunden |
| R44 | 6b (562–565) | Z. 102 | wiedergefunden |
| R45 | 6b (567–573) | Z. 103 | wiedergefunden |
| R46 | 6b (575–580) | Z. 100 | wiedergefunden |
| R47 | 6b/Editor (582–612) | Z. 105 | wiedergefunden |
| R48 | 6b/Editor (614–616) | Z. 106 | wiedergefunden |
| R49 | 6b/Start (619–640) | Z. 124 | wiedergefunden |
| R50 | 6b/Start (653–659) | Z. 132 | wiedergefunden |
| R51 | 6b/Ende (661–679) | Z. 128 | wiedergefunden |
| R52 | 6b/Ende (681–689) | Z. 129 | wiedergefunden |
| R53 | 6b/Ende (691–700) | Z. 129 | wiedergefunden |
| R54 | 6b/Ende (702–709) | Z. 130 | wiedergefunden |
| R55 | 6b/Ende (711–713) | Z. 131 | wiedergefunden |
| R56 | 6b/Ende (715–717) | Z. 126 | wiedergefunden |
| R57 | 6bb (723–739) | Z. 60 | wiedergefunden |
| R58 | 6bb (747–748) | Z. 61 | wiedergefunden |
| R59 | 6c (752–760) | Z. 43 | wiedergefunden |
| R60 | 6d (765–781) | Z. 91 | wiedergefunden |
| R61 | 6d/Form (803–827) | Z. 90 und 92 | wiedergefunden |
| R62 | 6d (834–837) | Z. 93 | wiedergefunden |
| R63 | 7 (840) | Z. 113 | wiedergefunden |
| R64 | 7 (841–842) | — (S) | wiedergefunden |
| R65 | 7 (843) | — (S) | wiedergefunden |
| R66 | 7 (844–867) | Z. 114 | wiedergefunden |
| R67 | 7 (868–870) | Z. 115 | wiedergefunden |
| R68 | 7 (871–883) | — (S) | wiedergefunden |
| R69 | 7 (884–888) | — (S) | wiedergefunden |
| R70 | 7 (890–899) | — (S) | wiedergefunden |
| R71 | 7 (901–912) | — (S) | wiedergefunden |
| R72 | 7 (914–920) | — (S) | wiedergefunden |
| R73 | 7 (922–925) | Z. 42 | wiedergefunden |
| R74 | 7 (926–932) | Z. 140 | wiedergefunden |
| R75 | 7 (933–936) | Z. 116 | wiedergefunden |
| R76 | 7b (944–962) | — (S) | wiedergefunden |
| R77 | 7b (964–972) | — (S) | wiedergefunden |
| R78 | 7b (974) | Z. 114 | wiedergefunden |
| R79 | 7c (978–993) | Z. 154 | wiedergefunden |
| R80 | 8 (998–1001) | — (S) | wiedergefunden |
| R81 | 8 (1002–1004) | — (S) | wiedergefunden |
| R82 | 9 (1009–1010) | Z. 44 | wiedergefunden |
| R83 | 9 (1011–1012) | Z. 45 | wiedergefunden |
| R84 | 9 (1013–1014) | Z. 46 | wiedergefunden |
| R85 | 10 (1020–1028) | — (S) | wiedergefunden |
| R86 | 10 (1025–1026) | Z. 84 | wiedergefunden |
| R87 | 10 (1032–1033) | — (S) | wiedergefunden |
| R88 | 10 (1034–1037) | — (S) | wiedergefunden |
| R89 | 10 (1038–1039) | — (S) | wiedergefunden |
| R90 | 10 (1041–1044) | — (S) | wiedergefunden |
| R91 | 11 (1060) | Z. 149 | wiedergefunden |
| R92 | 11 (1061) | Z. 149 | wiedergefunden |
| R93 | 11 (1062) | — (S) | wiedergefunden |
| R94 | 12 (1071–1083) | Z. 148 | wiedergefunden |
| R95 | 13 (1088–1103) | Z. 62 | wiedergefunden |
| R96 | 13 (1105–1111) | Z. 94 | wiedergefunden |
| R97 | 13 (1113–1116) | Z. 117 | wiedergefunden |
| R98 | 13 (1118–1123) | Z. 63 | wiedergefunden |
| R99 | 14/Regel 0 (1139–1181) | Z. 126 | wiedergefunden |
| R100 | 14/Regel 1 (1186–1195) | Z. 125 | wiedergefunden |
| R101 | 14/Regel 2 (1197–1213) | Z. 127 | wiedergefunden |
| R102 | 14/Regel 3 (1218–1222) | Z. 152 | wiedergefunden |
| R103 | 14/Regel 3 (1224–1232) | Z. 152 | wiedergefunden |
| R104 | 14/Regel 3 (1234–1242) | Z. 153 | wiedergefunden |
| R105 | 14/Regel 3 (1244–1257) | Z. 153 | wiedergefunden |
| R106 | 14/Regel 4 (1259–1280) | — (S) | wiedergefunden |
| R107 | 14/Regel 4 (1282–1283) | Z. 118 | wiedergefunden |
| R108 | 15 (1289–1307) | Z. 48 | wiedergefunden |
| R109 | 15 (1309–1312) | — (S) | wiedergefunden |
| R110 | 15 (1319–1338) | Z. 151 | wiedergefunden |
| R111 | 16 (1345–1346) | — (S) | wiedergefunden |
| R112 | 16 (1347–1349) | — (S) | wiedergefunden |
| R113 | 16 (1350–1351) | — (S) | wiedergefunden |
| R114 | 17 (1359–1378) | Z. 54 | wiedergefunden |
| R115 | 18 (1387–1388) | — (S) | wiedergefunden |
| R116 | 18/P.3 (1390–1405) | — (S) | wiedergefunden |
| R117 | 18/P.4 (1407–1428) | Z. 147 und 150 | wiedergefunden |

**117 von 117 wiedergefunden, 0 fehlen.** Die 76 A-Regeln belegen alle 65 Checklistenzeilen; keine Checklistenzeile ist ohne Regel dahinter, keine A-Regel ohne Zeile. Wo eine Zeile mehrere Nummern trägt, sind es Facetten derselben Vorschrift (z. B. R42 „Schritt für Schritt“ + R46 „auch wenn trivial“; R66 Secrets + R78 „gilt für alle Zugänge“; R5 + R7 + R100 der Startbefehl; R21 + R22 der Auftragskopf; R23 + R24 „In einfacher Sprache“ mit ihrer Eingrenzung; R51 Ablegen/Schliessen; R52 + R53 die Schliessfolge; R102 + R103 und R104 + R105 die Mac-Abgabe; R33 + R34 der Dokumentationsauftrag; R91 + R92 Verbote und Prüfwerkzeuge; R19 + R94 Verweis statt Abschrift). R117 (P.4) ist auf zwei Zeilen verteilt, weil es zwei verschiedene Handgriffe sind.

## 2. Was neu ist

| | Zeilen | Bytes | was |
|---|---|---:|---|
| ⭐ **Abschnitt 0** | 29–158 (130 Zeilen) | 8 835 | die Checkliste: 65 Zeilen zum Abhaken in elf Lagen, je Regelkern + Zeiger; ein fünfzeiliger Vorspann, der sagt, wozu sie da ist und warum sie vorn steht und 0 heisst |
| Kopfvermerk | 23–25 (3 Zeilen) | 213 | im Fassungskasten: *„Ergänzt 21.09.2026 (TB-69): Abschnitt 0 …“* — dieselbe Form wie die Vermerke vom 18.09. und 20.09. darüber |
| 6d-Vermerk | 801 (+ Leerzeile) | 65 | *„Erledigt 21.09.2026 (TB-69): die Liste ist Abschnitt 0.“* unter der Herleitung von TB-69 — sonst sagte der Abschnitt weiter, es gebe keine solche Liste |
| **Summe** | 135 Zeilen | 9 113 | = 80 018 − 70 905 ✓ |

⚠️ **Ehrlich benannt:** Der Auftrag sagt *„Was neu ist, ist nur die Checkliste selbst.“* Neu sind ausserdem die zwei Vermerke (278 B, 3 %). Beide sind keine Regeln, sondern Änderungsvermerke — der eine nach dem bestehenden Muster des Fassungskastens, der andere, damit 6d nicht weiter einen Zustand beschreibt, der seit heute nicht mehr gilt (`DOKUMENTATIONSSTANDARD.md` Regel 9: *jede Änderung sagt, was sie ablöst*). Wer sie nicht will, entfernt zwei Zeilen; die Checkliste hängt nicht daran.

## 3. Zeichengleich, wo nicht umgeschrieben wurde

Es wurde **nichts** umgeschrieben. Drei Messungen:

| | Messung | Ergebnis |
|---|---|---|
| a | `git diff --numstat 5a1f5e1 HEAD -- docs/projektfuehrung/ARBEITSWEISE.md` | **135 / 0** — 135 Zeilen hinzu, 0 entfernt; jede Änderung einer Zeile zählte als 1 entfernt + 1 hinzu |
| b | `git diff` zeigt genau zwei Hunks: `@@ -20,6 +20,139 @@` (Kopfvermerk + Abschnitt 0) und `@@ -665,6 +798,8 @@` (6d-Vermerk) | keine dritte Stelle |
| c | Teilfolgenprobe (Python, in `schritt4_teilfolge.txt`): jede der 1 293 alten Zeilen wird **in ihrer Reihenfolge und byteweise gleich** in der neuen Datei wiedergefunden | **1 293 / 1 293, 0 fehlen** |

Damit stehen alle Messungen, Anlässe, Zitate und Berichtigungen wörtlich da — auch die, die heute überholt klingen (*„ZIP hat immer funktioniert“*, Abschnitt 2; *„der erste Befehl jeder Mac-Sitzung ist `/login`“*, 14 Regel 0 — siehe Nebenbefunde N1–N5 in `regelliste_vorher.md`).

## 4. Was absichtlich gestrichen wurde

**Nichts.** Ausdrücklich: keine Regel, keine Messung, kein Anlass, kein Vermerk wurde entfernt oder gekürzt — `numstat` 0 entfernte Zeilen. Die fünf Nebenbefunde (N1–N5) sind Kandidaten für eine spätere Bereinigung durch den steuernden Chat; sie sind hier nur benannt, nicht behoben (Auflage des Auftrags: *„nichts inhaltlich umformuliert“* gilt für 5b-Aufträge, und dieser Auftrag verlangt für Streichungen die Einzelbegründung — es gab keinen Grund, der die Regel „Messungen bleiben wörtlich“ überwiegt).

## 5. Grösse vorher und nachher (Nachweis 8)

| | Bytes | Zeilen |
|---|---:|---:|
| vorher (`5a1f5e1`) | 70 905 | 1 293 |
| nachher (`HEAD`) | 80 018 | 1 428 |
| Zuwachs | **+9 113** | +135 |
| davon Checkliste (Abschnitt 0) | **8 835 (97 %)** | 130 |
| davon Vermerke | 278 (3 %) | 5 |
