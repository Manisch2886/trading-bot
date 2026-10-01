# REGISTER-KOPIE Abschnitt 28 (von 0–50) — Register-Z. 5168–5308 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 28. `asof` ist gesetzt — Berichtigung zu 26.3 und 26.6, und der Vorlauf-Satz gilt fort (TB-78, 21.09.2026)

⭐ **Drei Berichtigungen, Kategorie „Berichtigung" nach F17** (Registertext an
Registertext; die Quelle des Grundes ist eine Entscheidung des
Verfahrensprüfers, kein Ergebnis).

⚠️ **Abschnitt 26 bleibt zeichengleich stehen.** Was dort überholt ist, wird
hier benannt und trägt seine ERSETZT-Marke an dieser Stelle.

### 28.1 Warum es eine Berichtigung braucht — der Auftrag lief mit überholter Prämisse

**Gemessen 21.09.2026:** TB-77 hat durchgehend gegen die ursprüngliche
Auftragsfassung gearbeitet; der Nachtrag, der zwei Blocker aufhob, ist nie
angekommen (`grep` über Ergebnisdokument und `docs/belege/TB-77/` nach
*„Nachtrag zu TB-77"* und `FABLE_ANTWORT_2026-09-21b`: **0 Treffer**).

⭐ **Regel daraus, festgehalten, weil sie teuer war:** *Nach jeder Antwort des
Verfahrensprüfers werden die **laufenden** Aufträge gegen sie geprüft, nicht nur
die kommenden. Ein Nachtrag in eine laufende Sitzung ist billiger als eine
Berichtigung im Register.*

### 28.2 Registertext 5a, Ergänzung — woher `asof` kommt

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`,
Abschnitt (2), zeichengleich.

> **Registertext 5a, Ergänzung:** asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. Es wird im `MANIFEST.json` als Feld `asof` geführt und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof.

**Fables Begründung, warum das Erstellungsdatum und nicht das Datenende** — im
Wortlaut, weil sie den Unterschied trägt:

> *„Das Datenende (grösstes `open_time` über alle Kursdateien) wäre eine zweite aus dem Inhalt abgeleitete Grösse — genau die Bauart, die ich bei `fensteranker` abgelehnt habe, weil sie mit den Daten wandert. […] Dieser Abstand ist eine Frische-Tatsache und gehört als eigenes Manifest-Feld (`datenende`) dorthin, nicht in asof. Das Erstellungsdatum ist bereits registriert, von niemandem anders berechenbar und unabhängig davon, welches Symbol zuletzt eine Kerze hatte."*

**Bekannte Wirkung auf die Zulässigkeit, aus derselben Quelle:** Der
Horizontbeginn verschiebt sich gegenüber dem Datenende um vier Tage (19.09.
statt 15.09.). Die erste Falte nach 4a beginnt am 1. Januar eines Jahres; eine
Verschiebung im September ändert das Jahr nicht. ⭐ *Das ist eine
Kalenderaussage, keine Ergebnisaussage.*

### 28.3 Tatsachennotiz — der Wert von `asof`

| | Wert | Fundstelle |
|---|---|---|
| **`asof`** | **`2026-09-19`** | Abschnitt 18, `zeitpunkt_utc` = `2026-09-19T06:49:32+00:00`, gelesen aus `snapshots/63e4b6c8…/MANIFEST.json` |
| Snapshot | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | Abschnitt 18, Commit `1075dec` |

⭐ **Der Wert ist keine neue Messung.** Er stand seit dem 19.09. als Tatsache im
Register; was fehlte, war die Zeile, die ihn `asof` nennt.

### 28.4 ⚠️ ERSETZT: die Platzhalter-Tabelle in 26.3

**Die vier Platzhalter-Zeilen in 26.3** — *„[PLATZHALTER — `asof` ist nicht
gesetzt; Datum folgt, sobald 5a einen Wert hat]"* — **gelten als ERSETZT.** Sie
bleiben dort zeichengleich stehen (append-only). Die gültige Fassung:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | **2016-09-19** |
| `turtle_soup_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `volatility_breakout` | aktien | 10 Jahre | **2016-09-19** |

⚠️ **Die Konstante ist aus dem Code gelesen** (Fundstellen 26.1), nicht
registriert. Ob sie als registrierte Grösse nach `registerdaten.py` gehört,
bleibt offen — siehe 28.7.

⚠️ **Abgegrenzt, damit es niemand verwechselt:** 15.6 Punkt 3 nennt
*„gemessen vom letzten Kurstag (2026-09-01) zurück auf 2016-09-01"*. Das ist die
**Datenuhr**, genau der Bezug, den 26.2 ablöst — **kein `asof`**. Die
Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des
Kalenders und kein Hinweis darauf, dass es dasselbe wäre.

### 28.5 ⚠️ ERSETZT: die zwei Zeilen in 26.6, die `asof` als offen führen

**Zeile 1 von 26.6** — *„`asof` setzen. Wann und wodurch, ist Fables Frage (1)
im neuen Chat; die Lesart ‚mit Snapshot und Tag zugleich' ist nicht entschieden.
Bis dahin bleibt 26.3 ein Platzhalter"* — **ist ERSETZT.** Entschieden seit
21b: **durch den Snapshot, nicht durch den Tag.** Fable, wörtlich: *„Nicht mit
dem signierten Tag — der Tag friert ein, was das Register sagt; er erzeugt keine
Zahl."*

**Zeile 2 von 26.6** — *„Tatsachennotiz 4d füllen: vier Daten in 26.3"* — **ist
mit 28.4 erledigt.**

**Zeile 4 von 26.6** (die Wache in `auswertung.py`) — **ist ERSETZT.** Fable hat
seinen eigenen Vorschlag am 21.09. zurückgezogen: *„Mein Vorschlag ‚in den
Auswerter' war falsch adressiert."* Die Wache geht in die vier
`multi_symbol_optimise.py` (TB-30b). ⚠️ **Und sie prüft nicht gegen den
Horizontbeginn, sondern gegen den Beginn der ersten Selektionsfalte** —
siehe Abschnitt 29.

**Zeile 5 von 26.6** (`FABLE_ANTWORT_2026-09-21a` liegt in keinem Träger) — **ist
mit Schritt 0 dieser Aufgabe erledigt**; die Datei liegt unter
`docs/projektfuehrung/`.

⭐ **Unverändert offen bleiben:** Zeile 3 (die vier Optimierer, TB-30b), Zeile 6
(`RECENT_YEARS_ONLY` als registrierte Grösse, Entscheidungsvorlage) und Zeile 7
(nicht gemessen, wie viele Einstiege vor einem Horizontbeginn liegen).

### 28.6 Registertext 4a, Präzisierung, Ergänzung — der Vorlauf-Satz gilt fort

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.1, zeichengleich.

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn nicht ersetzt, sondern ausgelassen.

**Quelle des Grundes,** Fable wörtlich: *„Ein Vorlauf, der auf Kursen vor dem
Horizontbeginn rechnet, ist derselbe Zugriff"*, den Abschnitt 26 verbietet.
Kategorie: **Berichtigung** (Registertext an Registertext). Kein Ergebnis.

**Die Messung dazu, 21.09.2026, 17:48 durch den steuernden Chat:** Der Satz
*„Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten Kurs im
Bestand"* steht im Register **genau einmal**, in **Z. 4307** — und zwar
**innerhalb des Zitats der als ersetzt markierten Fassung** in 26.2. Er steht
also im Register ausschliesslich als Teil dessen, was ausser Kraft ist.

⭐ **Und die Tatsache, die Fables Unsicherheit auflöst** (*„ob ich den Satz
absichtlich gestrichen habe"*): Die Fassung vom 20.09. ist **nie** in einen
Registertext übernommen worden — gemessen, `grep` im Register: *„Horizontbeginn"*
**0 Treffer**, *„4a, Präzisierung"* **0 Treffer**. Es gab nichts zu streichen;
der Satz ist zwischen zwei Antworten verlorengegangen, nicht im Register.

> ⭐ **28.6 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 28.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Das Feld `asof` ins `MANIFEST.json` schreiben.** 28.2 verlangt es, aber der Snapshot ist nach 17.1 *„nach seiner Erzeugung nicht mehr geschrieben"*. Ob das Manifest Teil dieses Schreibverbots ist, sagt kein Registertext. ⭐ *Fable hält in 21b fest, dass der Snapshot-Hash über den Dateien liegt und nicht über dem Manifest — eine Ergänzung änderte den Hash also nicht.* **Das ist eine Verfahrensfrage vor dem Tag und wird nicht nebenbei entschieden** | Verfahrensprüfer / Betreiber |
| ⛔ | **Das Feld `datenende` ins `MANIFEST.json`** — derselbe Grund | dito |
| ⛔ | **`registerdaten.py` anfassen** | — |
| ⛔ | **Den Faltenplan nach 4a ableiten.** Er hängt an einer offenen Frage an den Verfahrensprüfer (Status des gesperrten `faltenplan.json`, `FABLE_ANFRAGE_2026-09-21b`, Abschnitt C) | eigene Aufgabe, nach seiner Antwort |

---

