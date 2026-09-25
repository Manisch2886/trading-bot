# TB-110 — Register 43: die Einträge aus Fable 25d und 25e und die Tatsachennotizen TB-108 und TB-109

**Sitzungstitel:** `TB-110` (läuft als Anschluss in der Sitzung TB-109, siehe dort Block H) · **Angelegt:** 25.09.2026, 23:25, vom steuernden Chat
**Grundlage:**
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25d_kopie_pruefansicht_abbruch_zwei.md` (Abschnitt 1, 2 und 3 a–e);
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md` (Abschnitt 1, 2 und 3 a–d);
- die Ergebnisse TB-108 und TB-109;
- Bauart: `docs/auftraege/MAC_TB-108_register_41_42.md`, das Muster für 41/42 (eingesetzte Blockzitate, `diff` rc 0, Ketten, Marken, keine Marke in Abschnitt 10).

**Vorgänger:** TB-109 · **Aufwand:** hoch
⭐ **Reine Registerarbeit: keine `.py`, nichts gerechnet, kein neues Abbild.**

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 23:04:** *„Soll nach TB-108 auch Register 43 (Fable 25d und 25e, gut zehn Einträge) als eigener Auftrag vorbereitet werden?“* ⇒ **„Ja, als TB-110 (Empfohlen)“**: reine Registerarbeit wie TB-108, kein Code, läuft nach TB-109.

| freigegeben | Pfad |
|---|---|
| ✔ | `docs/VORREGISTRIERUNG_neuselektion.md`: Abschnitt 43 **anhängen**, Marken additiv |
| ✔ | `docs/belege/TB-110/`, `docs/ERGEBNIS_TB-110_register_43.md`, Journalblock |

⛔ Alle Verbote aus TB-108 gelten unverändert. Vor allem: **keine Zeile im Listentext von Abschnitt 10**; kein Satz umgeschrieben; Sichtschutz 27.1; nichts aus 25f (Gesamtanalyse).

⚠️ **Herkunft der Quellen:** 25d und 25e wurden vom steuernden Chat aus der Projektablage **abgeschrieben**. Die Zitate sind zeichengleich mit der Datei im Repo, der Abgleich mit Fables Ablage ist nicht byteweise gemessen. So in 43.0 festhalten wie in 41.0.

---

## 0. Vorbedingungen

- Der Abgabe-Commit von TB-109 liegt vor, `git status` ist leer, und TB-109 hat **kein** Abbruchkriterium ausgelöst.
- Register-Zeilenzahl und `numstat` am Eingang festhalten.
- `herkunft.register()` vorher.
- Sonde gegen `40ffe18d…` vorher (erwartet 25/0/0, (ii) 0).

## Block A — Einträge und Stand

Arbeitsliste (Fable 25d Abschnitt 3 a–e und 25e Abschnitt 3 a–d, dazu die Registertexte in beiden Antworten):

| | Eintrag | Quelle | Art |
|---|---|---|---|
| 43-1 | **Ersteintrag „Ergänzung zu 36.5 — Ausgänge von `auswertung.py`“**: 0 oder 2, kein 1 | 25d 2 (4), Blockzitat | Registertext |
| 43-2 | Tatsachennotiz zu Punkt 4: Interpolation unterhalb der ersten Stützstelle gegen (0, 0), Grenzwert 0, gemessen TB-106 | 25d Abschnitt 1 und 3 (a) | Tatsachennotiz (**in 43**, nicht in Abschnitt 10) |
| 43-3 | Kopie in `faltenplan_neun.py`: Abbruch gleich, zweiter Ort, Auflösung nach TB-100; `f5fdb53` steht, kein Revert | 25d 2 (1), 3 (b); 25e Kopf | Tatsachennotiz |
| 43-4 | `herkunft.py`: Prüfansicht übergibt unter dem Modus `paths.DATA_DIR`; `TB30A_BASE_DIR` unter dem Modus rc 2 vor dem Lesen; eine Öffnung, mit dem Erzeuger oder vor ihm | 25d 2 (2), (3), 3 (c) | Registertext (Plan), noch nicht vollzogen |
| 43-5 | Tatsachennotizen TB-106 | 25d 3 (e) | Tatsachennotiz |
| 43-6 | `registerbericht.py --pruefen` rot bis 40.8 (h); Neuerzeugung mit dem Raster-Nachzug | 25d Abschnitt 1 | Tatsachennotiz |
| 43-7 | **„Ergänzung zu 24b A2 / 36.5 — null Trades“** | 25e 2 (2), Blockzitat | Registertext |
| 43-8 | Die zwei weiteren Ablagen wie `tb40_lauf_*` | 25e 2 (1) | Registertext (Anwendung von (iv)); Vollzug TB-109 |
| 43-9 | Klasse (iv) im Audit als (iv), nicht (i) ausserhalb | 25e 3 (b) | Registertext; Vollzug TB-109 |
| 43-10 | `pfadvergleich.py`: benannter Stummel | 25e 2 (3), 3 (d) | Tatsachennotiz |
| 43-11 | ⚠️ **Berichtigung des steuernden Chats an 25e (3):** Stummel `selektionsmodus()` → `None`, nicht `lambda: False`, weil `strategy_paths` seit TB-107 `is not None` fragt. Verhaltensbeleg aus TB-109 Block D. **Von Fable noch nicht bestätigt**, als solche kennzeichnen | Ergebnis TB-109 | Berichtigung (vorläufig) |
| 43-12 | Tatsachennotizen TB-107 | 25e 3 (a) | Tatsachennotiz |
| 43-13 | Tatsachennotizen TB-108: Abschnitte 41/42 eingetragen, Zahl der Einträge, Zitate rc 0, `register()` alt/neu, nicht gesetzte Marken | Ergebnis TB-108 | Tatsachennotiz |
| 43-14 | Tatsachennotizen TB-109: 10 Stellen unter dem Modus rc 2, ohne Modus gleich; Gegenprobe 24 Stellen; Ablagen entfernt; Audit (iv); A3 (Cron erreicht die Stellen ja/nein) | Ergebnis TB-109 | Tatsachennotiz |
| 43-15 | Was offen bleibt: `auswertung.Abbruch` ⇒ 2 mit der nächsten Öffnung von `auswertung.py` (Punkte 3/5/14); `herkunft.py`-Öffnung (43-4); Erweiterung von 19; Erzeuger; Faltenplan-Abbild; 25f (Gesamtanalyse) | — | Liste |

Je Eintrag: Fables Text als eingesetztes Blockzitat (`diff` rc 0), Art, gemessener Stand (Commit, Hash, rc; **keine Ergebnisgrössen**), Kette.

## Block B — Abschnitt 43

`## 43. …` am Ende des Registers, Überschrift sinngemäss: „Ausgänge der Auswertung, null Trades als Wert, die zweite Öffnung von `herkunft.py` — die Einträge aus Fable 25d und 25e (TB-110, 26.09.2026)“ (Datum des tatsächlichen Eintrags einsetzen).

- **43.0 Kopf:** Anlass, Quellen-Herkunftsnotiz, Verweis auf 41/42.
- **43.1:** 25d; **43.2:** 25e; **43.3:** Berichtigung 43-11; **43.4:** Tatsachennotizen TB-108/TB-109; **43.5:** offen.
- **Ketten:** In 42 steht „offen: 25d, 25e“ ⇒ an dieser Stelle **keine** Änderung, aber in 43.0 der Satz „beantwortet in 43.1/43.2“. Dazu eine Marke **unter** dem betreffenden Absatz in 42 (additiv).

## Marken am alten Ort

| Marke | wohin (Zielabschnitt vorher lesen) |
|---|---|
| Ausgänge von `auswertung.py`: 0 oder 2 | **36.5**, unter dem Registertext; **12**, wo der Abbruch beschrieben ist |
| null Trades ist ein Wert | **5.1 Nr. 8** und **1c** |
| Interpolation unter 1 %, Grenzwert 0 | ⛔ nicht in Abschnitt 10; stattdessen in **43.1**, mit Verweis „Sperrlistenpunkt 4“ |
| zweite Öffnung von `herkunft.py` geplant | **37.4** |
| offen 25d/25e ⇒ beantwortet | **42.6** (bzw. der Absatz „Was offen bleibt“ in 42) |

## Block C — Nachweise

Wie TB-108 Block D:
- `numstat` zweite Spalte 0;
- `diff` je Zitat rc 0;
- Sonde gegen `40ffe18d…` vorher = nachher, (ii) 0;
- `register()` alt/neu;
- `test_vorregistrierung` 196/196;
- Hashes: nur das Register und `docs/` geändert.

**Commits:** (1) Abschnitt 43 und Marken in **einem** Commit · (2) Belege, Ergebnis `docs/ERGEBNIS_TB-110_register_43.md` („Für Fable“, „In einfacher Sprache“), Journalblock.

## ⚠️ Abbruchkriterien

Wie TB-108:
- `numstat` ≠ 0;
- Sonde (ii) ≠ 0;
- ein Eintrag verlangt, einen bestehenden Satz zu ändern.

Dann melden, nicht reparieren.

## In einfacher Sprache

Der Prüfer hat zwei weitere Antworten gegeben: Die Auswertung soll nur noch zwei Ausgänge kennen (gerechnet oder nicht), und „keine Geschäfte“ ist ein Ergebnis, kein Grund aufzuhören. Beides wird wortgleich ins Regelwerk übernommen, zusammen mit dem, was in den Aufträgen TB-106 bis TB-109 gemessen und umgesetzt wurde. Einen kleinen Denkfehler des Prüfers beim Aufsatz für das alte Prüfwerkzeug trägt der steuernde Chat als vorläufige Berichtigung ein, bis der Prüfer sie bestätigt.
