# TB-56 — Rückfrage an den Betreiber (Regel 6), gestellt 2026-09-19 nach Teil A

**Befund:** Die Schranke, die den festgehaltenen Faltenplan
`research/faltenplan_neun/daten/faltenplan.json` und die Tabelle in 15.6 erzeugt
hat, ist NICHT `ERSTE_MOEGLICHE_FALTE` in `research/vorregistrierung/registerdaten.py`,
sondern deren **Kopie** `FRUEHESTE_FALTE = 2019` in
`research/faltenplan_neun/faltenplan_neun.py:120` (Kommentar darüber:
`# registerdaten.py::ERSTE_MOEGLICHE_FALTE`). `faltenplan_neun.py` importiert
`registerdaten.py` nicht. Dazu prüft `test_faltenplan_neun.py` Probe F0
„unmutiert beginnt jeder Plan 2019".

Der Auftrag gibt nur `registerdaten.py` und `faltenplan.py` (beide
`research/vorregistrierung/`, Verfahren A, Krypto als Platzhalter) frei.
Werden nur diese beiden geändert, rechnet das Werkzeug, aus dem die
Registertabelle stammt, weiter mit der Schranke — der Zweck („die Schranke
geht", F14) wäre am Wortlaut vorbei verfehlt.

**Frage 1:** Darf `research/faltenplan_neun/faltenplan_neun.py` (Schranke
`FRUEHESTE_FALTE` entfernen, `schranke_bindet`/Ausgabe anpassen) und
`test_faltenplan_neun.py` (Probe F an den Plan ohne Schranke angleichen)
zusätzlich geändert werden — oder bleibt es beim Wortlaut (nur die beiden
Vorregistrierungsdateien; der neue Plan entsteht dann aus dem neuen
Messskript mit im Speicher ausgeschalteter Schranke, und `faltenplan_neun.py`
behält seine Schranke samt Verweis auf eine Konstante, die es nicht mehr gibt)?

**Frage 2 (hängt an Frage 1):** Woher soll `plan_aktien()` in
`research/vorregistrierung/faltenplan.py` die erste Falte je Bot nehmen?
(a) aus der Datenlage mit derselben Regel wie `faltenplan_neun.py`
(`erstes_faltenjahr`, Import über den Pfad, reine Standardbibliothek) —
eine Regel an einer Stelle; (b) aus der neuen Plandatei neben
`faltenplan.json` lesen; (c) als Pflichtparameter ohne Vorgabe.

---

## Antwort des Betreibers (wörtlich, über die Auswahl in der Sitzung, 2026-09-19)

**Zu Frage 1:** „Ja, beide zusätzlich freigeben" — *(Beschreibung der gewählten
Option: Zweck vor Wortlaut: FRUEHESTE_FALTE aus faltenplan_neun.py entfernen,
Probe F im Test auf den Plan ohne Schranke umstellen. Der neue Plan kommt dann
direkt aus dem Werkzeug.)*

**Zu Frage 2:** „Aus der Datenlage, Regel von faltenplan_neun" — *(Beschreibung
der gewählten Option: faltenplan.py importiert faltenplan_neun (reine
Standardbibliothek) über den Pfad und ruft dessen erstes_faltenjahr — eine
Regel, eine Stelle.)*
