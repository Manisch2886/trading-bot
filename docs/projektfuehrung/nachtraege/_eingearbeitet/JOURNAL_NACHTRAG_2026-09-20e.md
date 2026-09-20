# Journal-Nachtrag (e) — 20.09.2026, TB-62: die Nachträge (m) und (v), und das Ende der ZIP-Pflicht

**Quelle:** Mac-Sitzung **TB-62 Nachtraege m und v**, 20.09.2026, etwa 15:00 bis
15:45 Ortszeit, Ausgang `7a696be`, reine Dokumentation (kein Interpreter, keine
Kursdaten). Commits `e3a25ae`, `4b55a33`, `e270e63`, `62828df`, `73000be`,
`5cbd625` und der Abgabe-Commit. Ergebnisdokument
`docs/ERGEBNIS_TB-62_nachtraege_m_v.md`. **Einzuarbeiten als nächster Block
nach dem höchsten vorhandenen** (am 20.09.2026 gemessen: `BJ`; die Nachträge (g),
(20a)–(20d) stehen davor an — die Nummer vergibt die einarbeitende Sitzung).

---

## Was gemessen wurde

| | Messung |
|---|---|
| Nachtrag (v) | **22** Zeilen `K3k`–`K4f`, keine im Backlog oder Archiv belegt (Muster `^\| \*\*(K\d[a-z])\*\*`, ohne `-u`); als Block `2z` eingefügt, alle 22 zeichengleich (`grep -xF`, 22/22). `numstat 29/0` |
| Nachtrag (m) | sechs Nummern `K2l`–`K2q` an (s)/(t)/(n) vergeben — bestätigt. Zwei Regeln in keinem Regeldokument (nur als Zitat in `UEBERGABE_2026-09-19.md` 239/243) → `ARBEITSWEISE.md` 14 Regel 3 und 15. Vier Regeln „anderswo" — gemessen in `UEBERGABE_2026-09-19.md` Block 7 Punkte 7–10 und Block 8 Punkt 7, `ARBEITSWEISE.md` 14 und 15; **nicht** in `UMZUG.md` oder dem Protokoll, wie der Auftrag annahm; `K2m` nur in der Übergabe. Vermerk `K4g` |
| ⚠️ (m) darüber hinaus | Rückblick-Block „2s" mit **20** Zeilen (`T53.x`, `T58.x`, `T58b.x`, `B1`–`B7`) zu TB-53b/58/58b, eine überholte 0,85-Berichtigung, drei Kettenzeilen (eine — „Laufreproduktion gegen den Lock" — nirgends geführt). **Nicht eingearbeitet, Ort offen** (Empfehlung: Journal) |
| K1o/K1q | 64 Zeilen / 62 Nummern vorher — bestätigt; zusammengeführt, `numstat 2/4` (nicht 2/2, wie der Auftrag erwartete: die älteren Zeilen zählt git als entfernt und neu). Nachher **85 / 85 / 0 doppelt**, zwei unabhängige Zählungen |
| ZIP-Umbau | `ARBEITSWEISE.md` **37** Fundstellen (44 roh — das Muster traf „Prüfprinzipien" und „Disziplin"): 25 Vorschrift getauscht, 6 Redewendungen umformuliert, 4 historische Belege unverändert (byteweise geprüft), 2 ohne ZIP-Bezug. `UMZUG.md` 4: 2 Entstehung (bleiben), 2 in einer 23-zeiligen Kopie von Abschnitt 10, die nach Regel 9 entfernt ist (per `diff` zeichengleich mit der eingearbeiteten Fassung). Protokoll 1 (bleibt), `DOKUMENTATIONSSTANDARD.md` 0, `BACKLOG.md` 0 |
| Zeilen `BACKLOG.md` | 1469 → **1497** (`wc -l` und `awk`, gleich) |
| ausserhalb `docs/` | `git diff --stat 7a696be..HEAD -- . ':!docs'` → 0 |

## Was der Auftrag falsch hatte, und was daraus folgt

1. **Die ZIP-Pflicht stand in Abschnitt 2, nicht in Abschnitt 1.** Abschnitt 10
   verweist jetzt auf Abschnitt 2.
2. **Nachtrag (m) ist mehr als sechs Zeilen.** Der Auftrag hat ihn auf die
   Abschnitt-4-Ergänzungen verkürzt; 20 Rückblick-Zeilen und eine offene
   Kettenzeile blieben ungenannt. *Fehlerklasse wie K4a: die Suche nach den
   Nummern sah nur das, was Nummern trug.*
3. **Die Fundort-Tabelle der vier (m)-Regeln war teils erschlossen, nicht
   gemessen** — `UMZUG.md` und das Protokoll tragen die Regeln nicht.

## Was während der Sitzung passierte

Um 15:21–15:23 schrieb der Betreiber über die Geräteanbindung drei Dateien in
den Arbeitsbaum (`AKTUELLER_AUFTRAG.md` geändert, `MAC_TB-66_…` und
`FABLE_ANTWORT_2026-09-20_…` neu), während die Sitzung lief — der Fall von
`K2p`, folgenlos, weil es nicht die Dateien dieser Sitzung waren. **Die Sitzung
hat sie unverändert in `5cbd625` committet**, damit der Baum für TB-63 sauber
ist und nichts nur auf einem Rechner liegt.

## Fehler dieser Sitzung (Regel 3)

| Fehler | ⇒ Regel |
|---|---|
| „in sechs Schüben gewachsen" geschrieben, dann gezählt: 5 Überschriften | Kontextzahlen zählen wie Ergebniszahlen |
| Suchmuster traf „Prüfprinzipien" — 44 statt 37 | Treffer lesen, Ausschlüsse benennen |
| Commit-Text `73000be` mit falscher Gruppenzählung (24/5/6 statt 25/6/4) | Gruppenzahlen aus der Zeilenliste ableiten, nicht umgekehrt; berichtigt im Ergebnisdokument |

## In einfacher Sprache

Zwei liegengebliebene Notizzettel sind in die Aufgabenliste und die
Arbeitsweise übertragen, zwei verlorene Regeln wieder da, und „schick es als
ZIP" heisst überall „committe es". Offen bleibt, wohin zwanzig Zeilen Rückblick
aus dem älteren Zettel gehören — vorgeschlagen ist das Journal.
