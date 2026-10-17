# FABLE-Anfrage 17.10.c — R101 Festlegungen S-B1; KI-Sammler und Leseregel; t3-Embargo aus gefundenen Trades; Startkapital; R107 (b)

*Steuernder Chat, 17.10.2026, HEAD `5031cd0`. Erste Anfrage im neuen Chat „Fable Trading Bots-17.10.2026 b“. **Registerfrage.** Dateien in der Projektablage unter projektfuehrung/. Zitate per Skript zeichengleich (Fettdruck entfernt).*

## Teil 0 — Kenntnis

Register `docs/VORREGISTRIERUNG_neuselektion.md`, Commit `7fe6342`, 12 596 Zeilen, sha256 `945ba13f…` (= HEAD), Abschnitte 0–66, eingetragen bis R106. **R107** steht in FABLE_ANTWORT_2026-10-17b (noch nicht im Register; Eintrag mit TB-175) — dein Block beginnt bei **R108**.

## Frage (a) — S-B1: Festlegungen nach R101 (a)–(c)

Betreiber 17.10. (gewählte Antworten): Festlegung 1 „Ändern (Recommended)“ — 10a.2 vor dem Tag ändern, Gold/Silber als ETC-Paar, Grund aus dem Text: kein UCITS-Fonds auf ein einzelnes Edelmetall. Festlegung 2 „Währungsbereinigt (Recommended)“. Festlegung 3 „Zeitraum-Renditen (Recommended)“; die Länge legst du fest.

R101 (a), Z. 12319: „Zulässig ist sie mit einem Grund aus dem Text, nicht mit dem Grund, dass sonst die Untergrenze aus (d) greift;“ und „[Voraussetzung, zu messen: dass die Kandidatenliste (Abschnitt 9 der S-B1-Vorregistrierung) Gold und Silber führt und ein UCITS-Fonds auf ein einzelnes Edelmetall nicht besteht; dann trägt der Grund.]“ (b): „ist währungsbereinigt, mit Nennung von Währung, Wechselkursquelle und Tageszuordnung.“ (c): „Nettoinventarwert zum US-Schluss am gleichen Tag, oder Renditen über einen Zeitraum, der den Versatz deckt“.

Gemessen: `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` (Commit `1bc2d57`) führt die Liste in Abschnitt 2 (Z. 74), Z. 85: „| Metalle | `GLD` (Gold), `SLV` (Silber) |“; Z. 76–78: die Liste ist „Teil der Sperrliste (Abschnitt 9)“; `research/etf_trendfolge/register.py` Z. 140–143 GLD, SLV. **Offen:** dass kein UCITS-Fonds auf ein einzelnes Edelmetall besteht, ist im Repo nicht belegt (allgemeiner Umstand, wie R101 Quelle).

**Bitte:** Registerblock zu R101 (a)–(c): Wortlaut der Änderung von 10a.2 (ETC-Paar, Registerzeile, Bericht), Währung und **Wechselkursquelle**, **Tageszuordnung**, **Länge des Zeitraums** der Renditen. Trägt der Grund mit der Teilmessung (Liste ja, UCITS offen)?

## Frage (b) — KI-Sammler nach R107 (d)

Betreiber 17.10.: „A: KI-Sammler bauen“; Modell „Haiku, 3 $/Monat“; Auswerteplan „Ja, vorher an Fable“. Bauplan (erschlossen, noch nicht gebaut): Quellen mit Vintage (ALFRED/FRED, Fear&Greed, VIX/Indizes), je Abruf Zeitstempel, Rohkopie, sha256; Prompt nur aus dem eingefrorenen Abruf, **keine Websuche**; fester Fragenkatalog v1, **je Markt** (Krypto, Aktien) sechs Fragen, Skala −2..+2, Zuversicht, Begründung, Modell, Prompt- und Quellen-Hash; eigene DB `marktzustand/marktzustand.db` ausserhalb des Laufbereichs (`shared/`, `strategies/`); Kachel nur GET (`/api/marktzustand`, sqlite read-only); Monatsdeckel aus eigener DB; **Wachen-Test** (kein Import aus `strategies/` u. a., Schreibziel nur eigene DB, kein Modul in `shared/`/`strategies/` nennt den Sammler); Cron 1× täglich, Ausfall als Zeile. Handelscode unberührt.

R107 (d): „seine Zustände erst gegen Bot-Ergebnisse gelesen werden, wenn die Regel dafür steht (24.3)“.

**Fragen:** Genügen die Bedingungen aus R107 (d)? Welche Regel muss stehen, bevor Zustände gegen Bot-Ergebnisse gelesen werden (24.3), und wird sie jetzt registriert oder mit dem Auswerteplan vor dem Erstlauf?

## Frage (c) — t3_supertrend: Embargo aus gefundenen Trades (R107 (e))

Befund (gerechnet auf den abgelegten Listen, Test nicht gelaufen): über alle gefundenen Trades t3 P95 10,8417 → Embargo **12**; über ausgeführte 11,2083 → **13** (`daten/embargo.json`). Der Test D4 (`research/faltenplan_neun/test_faltenplan_neun.py` Z. 357–359, P90 gegen TB-24, Toleranz 5e-3) ergibt für t3 P90 8,6833 statt 9,5000; die übrigen acht gleich. P90 steht nicht im Register.

Register: 16.6, Z. 2319: „`t3_supertrend` 13 Handelstage (P95 = 11,21).“ 41.3 C2 (b), Z. 8907: „Das 95. Perzentil der Haltedauer wird aus den gefundenen Trades gerechnet“; Z. 8911: „Die Wirkung kenne ich nicht (der Wert 13 kann sich bewegen)“.

**Fragen:** Wird 13 neu hergeleitet, und wann (jetzt auf den alten Listen, vor R44, oder mit der Neuerzeugung)? Was gilt für D4 (Vergleich gegen TB-24 streichen, umstellen, Ausnahme t3)? **Neigung:** Herleitung mit der Neuerzeugung (R44), 16.6 bis dahin unverändert, D4 vergleicht künftig gegen die eigene Herleitung.

## Frage (d) — Startkapital (zur Kenntnis, Reihenfolge)

`research/mtm_drawdown/grundlage.py` Z. 189 `meta.get("startkapital")`, Z. 198 `float(meta["startkapital"])` (Meta-Zeile); `research/wf_kapital_dd/messung.py` Z. 120 `startkapital = float(es.STARTING_CAPITAL)` (Code-Konstante; erschlossen: das Modul des Bots; je `strategies/<bot>/equity_simulation.py` steht `STARTING_CAPITAL = 10_000.0`). R107 (e): „das Startkapital nimmt er aus dem Register (29.3), nicht aus einer Meta-Zeile (37.5 (2))“. 37.5 (2), Z. 7191: „Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie.“

**Frage:** Reihenfolge: Umstellung beider Leser vor ihrer nächsten Messung, mit dem Bauauftrag der Leser (TB-175/176) oder nach R44? Sind die neun Kopien in `equity_simulation.py` ein Befund zu 37.5 (2)?

## Frage (e) — R107 (b): reicht die Teilmessung?

R107 (b): „führt TB-169 3b t3_supertrend, ist sie es, sonst nachgeholt.“ Gemessen durch Lesen: TB-169 3b führt t3 (Beleg `e_abnahme.txt` Z. 85, Wiedergabe: „3b spaetes Symbol CCC gleich mit/ohne Schranke · 16/16“); Wachen an. Zwei Einschränkungen: (A) verglichen wird Lauf B **mit** Schranke am natürlichen Tag, nicht ohne Schranke; dass B dort leer läuft, ist erschlossen. (B) Prüfung 8 (fremde Lesepfade) prüft nur A und B, nicht 3b; für 3b erschlossen. **Frage:** Ist die Voraussetzung damit erfüllt, oder wird eine Prüfung ohne Schranke nachgeholt?

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_15, _16, _24, _29, _37, _41, _58, _62, _66; FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md; VORREGISTRIERUNG_S-B1_etf_trendfolge.md. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, docs/belege/. Antwort höchstens 10 KB als projektfuehrung/FABLE_ANTWORT_2026-10-17c_<stichwort>.md: Kurz (je Frage „einverstanden“ oder „anders, weil …“), Registerblock zeichengleich kopierbar ab R108, Leseprotokoll nach R56 (b), Ampel.
