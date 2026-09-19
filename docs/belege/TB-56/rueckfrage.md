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

---

## Zweite Rückfrage (Regel 6), 2026-09-19 nach der ersten Antwort

**Neuer Befund, der die erste Antwort betrifft:** `faltenplan_neun.py` ist nicht
frei stehend. An seinem Plan hängen drei Prüfer, die den **Code gegen das
Register** halten — und das Register trägt die 2019 noch (15.6, 16.1.1), bis
TB-56b es berichtigt:

1. `research/registernachtrag_tb41/pruefe_register.py` (Nachweis 7 „KEIN
   BEFUND") ruft den Trockenlauf auf, der seinen Faltenplan **live** aus
   `faltenplan_neun.py` holt, und vergleicht die Symbolzahl je Falte mit der
   Registertabelle 16.1.1. Ohne Schranke hätte der Plan 8–9 Falten; die
   Druckfunktion des Trockenlaufs stolpert dann über Falten, die im Register
   nicht stehen (gemessen: `TypeError` in `drucke`, JSON wird nicht
   geschrieben), und der Registerprüfer fiele **still** auf den Dokument-Beleg
   zurück und meldete „KEIN BEFUND", ohne gemessen zu haben (Prüfprinzip A1).
2. `research/faltenplan_neun/test_faltenplan_neun.py` Teil A vergleicht gegen
   das TB-31-Werkzeug `research/krypto_historie/faltenplan.py`, das eine
   **dritte** Kopie `FRUEHESTE_FALTE = 2019` trägt (nicht freigegeben); Teil B
   vergleicht gegen die Registertabelle; Proben F, G4 prüfen 2019. Alle würden
   rot — Nachweis 6 („keine neue rote Stufe") wäre nicht erfüllbar.

**Frage 3:** Soll `faltenplan_neun.py` **jetzt** ohne Schranke rechnen (dann
werden `test_faltenplan_neun.py` und der Registerprüfer rot bzw. still grün,
bis TB-56b Register, Prüfer, Test und TB-31-Werkzeug nachzieht — ich berichte
das dann als erwartet und nenne es), oder bleibt `faltenplan_neun.py` bis zur
Registerberichtigung unverändert (der neue Plan neben `faltenplan.json`
entsteht aus dem Messskript mit im Speicher ausgeschalteter Schranke —
inhaltsgleich mit dem, was `faltenplan_neun.py` ohne Schranke rechnet —, und
TB-56b entfernt die Schranke dort im selben Zug wie im Register)? Die beiden
Vorregistrierungsdateien werden in beiden Fällen jetzt geändert.

**Antwort des Betreibers zu Frage 3 (wörtlich, Auswahl in der Sitzung):**
„Bis TB-56b unverändert lassen" — *(Beschreibung der gewählten Option: Code und
Register wechseln im selben Zug (TB-56b: Registertabelle, faltenplan_neun.py,
Test, TB-31-Werkzeug, Trockenlauf-Druckfunktion). Jetzt: neuer Plan neben
faltenplan.json aus dem Messskript (inhaltsgleich mit faltenplan_neun ohne
Schranke), die beiden Vorregistrierungsdateien werden geändert, alle Nachweise
bleiben messbar.)*

**Folge für die erste Antwort:** Die Freigabe von `faltenplan_neun.py` und
`test_faltenplan_neun.py` wird damit **nicht in Anspruch genommen**; Antwort 2
(erste Falte aus der Datenlage nach der Regel von `faltenplan_neun`) bleibt und
wird über einen Pfad-Import der **unveränderten** `faltenplan_neun.py`
umgesetzt.

---

## Dritte Rückfrage (Regel 6), 2026-09-19 nach Teil B, vor Commit 2

**Befund:** Nach der Angleichung von `research/vorregistrierung/faltenplan.py`
an 4a (Aktienpläne ab 2017/2018) bricht `test_vorregistrierung.py` ab
(`auswertung.py:237 KeyError: '2017'`): die Auswertung nach Verfahren A liest
die **vorab berechneten Benchmark-Drawdowns** aus
`ergebnisse/benchmark_drawdowns.json`, und diese Tabelle kennt nur Falten ab
2019. Sie steht auf der **Sperrliste** (Register Abschnitt 10, Punkt 4:
„Drawdown-Bedingung, `DD_Toleranz` und die vorab berechneten
Benchmark-Drawdowns — `benchmark.py`, `ergebnisse/benchmark_drawdowns.json`")
und ist im Auftrag **nicht freigegeben**. Probeweise neu gerechnet (in den
Scratchpad, nichts überschrieben): alle registrierten Faltenzeilen 2019–2026
bleiben zeichengleich, 2017/2018 kommen hinzu — aber `DD_Toleranz` (Median über
die Selektionsfalten, registriert −4,33 % @ 50 %, −8,55 % @ 100 %) ändert sich
bei `rsi2_mean_reversion` und `volatility_breakout` auf −6,61 % / −12,89 %
(acht statt sieben Falten, gerader Median); bei den beiden anderen
Aktien-Bots bleibt er zufällig gleich (neun Falten, 2017 tief, 2018 hoch).

**Frage 4:** (a) `faltenplan.py` bleibt an 4a angeglichen; die neu gerechnete
Benchmark-Tabelle wird als **eigene Datei daneben** abgelegt
(`ergebnisse/benchmark_drawdowns_ohne_schranke.json`), die gesperrte bleibt
byteweise unverändert, und `test_vorregistrierung.py` ist **bis TB-56b rot**
(dort fällt mit der Registerberichtigung auch die Amendment-Entscheidung zu
Sperrliste 4) — benannt, nicht versteckt; Nachweis 6 weist damit eine neue
rote Datei aus. (b) `benchmark_drawdowns.json` jetzt neu schreiben —
gesperrter Wert `DD_Toleranz` ändert sich bei zwei Bots ohne Amendment, Test
grün. (c) Die Angleichung in `plan_aktien()` zurücknehmen — Teil B klemmt für
das Verfahren-A-Werkzeug, die Schranke käme über die Tabellenabdeckung durch
die Hintertür zurück.

**Antwort des Betreibers zu Frage 4 (wörtlich, Auswahl in der Sitzung):**
„Tabelle daneben, Test rot bis TB-56b" — *(Beschreibung der gewählten Option:
faltenplan.py bleibt an 4a angeglichen; neue Benchmark-Tabelle als eigene
Datei ergebnisse/benchmark_drawdowns_ohne_schranke.json, die gesperrte bleibt
byteweise unverändert; test_vorregistrierung.py ist bis zur
Amendment-Entscheidung in TB-56b rot — im Bericht benannt, Nachweis 6 weist
eine neue rote Datei aus.)*
