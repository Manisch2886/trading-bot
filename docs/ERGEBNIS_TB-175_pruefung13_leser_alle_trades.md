# ERGEBNIS TB-175 — Register 67 (Fable 17b, R107, neun Marken) und Prüfung 13 in `test_haltedauer_kern.py` erneuert (Teil 1, ohne E2)

**Sitzung:** TB-175, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md` · **Zweig:** `main`
**Commits:** `b470dc4` (S0, Fable 17.10.b und Auftrag) · `3a00cf8` (R, Register 67 und neun Marken) · `9d72a7f` (K, Registerkopie, Index, Dialog-Index) · `9c31a65` (E, Prüfung 13 erneuert) · der Abgabe-Commit „TB-175 Abgabe: Ergebnis, BACKLOG, Journal FL“, der dieses Ergebnis enthält · danach „TB-175 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-175/` · **Journal:** FL · **Kein Abbruch.**

## Kurz

Anfrage und Antwort von Fable 17.10.b liegen seit `b470dc4` unverändert im Repo (R56 (b), md5 vorher = nachher). Register 67 trägt R107 mit Quellenzeile zeichengleich aus dem Registerblock der Antwort (Z. 13–16), dazu die Kettenzeile und 67.2 mit dem Voraussetzungsbeleg und den Tatsachennotizen (a) bis (d). Neun Marken nach R107 (f) stehen an 16.4, 16.8, 55.4, 56.3, 57.3, 58.4, 62.3, 64.1 und 66.1. Sonst ist das Register nur angehängt. Die seit TB-98 rote Prüfung 13 im Alt-Test der Haltedauern ist erneuert. Sie prüft jetzt jeden Schreibaufruf einzeln. Für `positionen_holen.py` verlangt sie: Ziel nur aus dem Pflicht-`--ziel`, Schreiben nur über `_schreibe_einmal` mit `O_EXCL`. Auf Python 3.9.6 ist der Test grün und an verfälschten Kopien rot. Die drei git-Aufrufe im Test laufen mit `--no-optional-locks`. Die Umstellung der Leser (E2) ist nicht enthalten. Kein Handelscode, kein Lauf auf Kursen, kein Live, kein Broker.

## Schritt 0

0a: Zweig `main`, HEAD = origin/main = `5031cd0207234379d4a427de6734d42f6f814a0e`, genau die vier Soll-Einträge (`0a_status.txt`), Karte gefüllt; letzte Zeile `0a gut (4 Eintraege)`. Holbefehl: `tb175_werkzeug.py 30b0d207aa24e4fafac1873253756fecd9f3031989f2cd81d0cecc04fbce49e2`, `test_haltedauer_kern.py b73adc87d57c764eb71ee00f725019dcedb70164599a20c7e9c77e6d065f8cba`, `Dateien 2`. Die zwei Fable-Dateien mit den zwei `cp`-Zeilen kopiert. S0 = `b470dc4` (6 Dateien), gepusht, porcelain danach leer.

`0a_md5.txt`, wörtlich:

```
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17b/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md = nachher docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md = d13e691973d3b98528b72c67ac000eb9
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17b/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md = nachher docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md = af2c861a88a083dd7652dcbc07650d8f
Pruefungen: 2, NEIN: 0
rc 0
```

## Schritt V — Voraussetzungen

`v_voraussetzung.txt`, letzte Zeilen wörtlich (41 Prüfungen, vollständig im Beleg und in 67.2):

```
ja    Register: 66 da, 67 nicht; R107 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 62.3: Einfuegestelle nach Z. 12327 eindeutig, R107 dort noch nicht genannt
ja    Ort 55.4: Einfuegestelle nach Z. 11797 eindeutig, R107 dort noch nicht genannt
ja    Ort 66.1: Einfuegestelle nach Z. 12538 eindeutig, R107 dort noch nicht genannt
ja    Ort 64.1: Einfuegestelle nach Z. 12456 eindeutig, R107 dort noch nicht genannt
ja    Ort 56.3: Einfuegestelle nach Z. 11903 eindeutig, R107 dort noch nicht genannt
ja    Ort 57.3: Einfuegestelle nach Z. 12024 eindeutig, R107 dort noch nicht genannt
ja    Ort 16.4: Einfuegestelle nach Z. 2254 eindeutig, R107 dort noch nicht genannt
ja    Ort 16.8: Einfuegestelle nach Z. 2464 eindeutig, R107 dort noch nicht genannt
ja    Ort 58.4: Einfuegestelle nach Z. 12107 eindeutig, R107 dort noch nicht genannt
ja    Index-Kopf Z. 3 nennt 0–66
ja    Index: Zeile 66, Pflegezeile TB-173, Pflege-Anker je genau einmal; kein Abschnitt 18
ja    Dialog-Index: 17b noch nicht
ja    E2-Ausgang: research/faltenplan_neun/embargo_neun.py md5 b93af1460411
ja    E2-Ausgang: research/mtm_drawdown/grundlage.py md5 81cf1c93243a
ja    E2-Ausgang: research/mtm_drawdown/messung.py md5 00eb23079f1b
ja    E2-Ausgang: research/mtm_drawdown/test_mtm_kern.py md5 80f1511a18d2
ja    E2-Ausgang: research/wf_kapital_dd/messung.py md5 94c091f4c4e1
ja    Fundstelle abn: docs/belege/TB-169/e_abnahme.txt Z. 85 unveraendert (Bau-Stand)
ja    Fundstelle aus_lade: research/tb24_haltedauern/auswertung.py Z. 69–71 unveraendert (Bau-Stand)
ja    Fundstelle emb: research/faltenplan_neun/embargo_neun.py Z. 232 unveraendert (Bau-Stand)
ja    Fundstelle gl_meta: research/mtm_drawdown/grundlage.py Z. 189–198 unveraendert (Bau-Stand)
ja    Fundstelle mg: research/vorregistrierung/messgroessen.py Z. 230–231 unveraendert (Bau-Stand)
ja    Fundstelle tle_aus: research/tb24_haltedauern/test_listen_erzeuger.py Z. 87–88 unveraendert (Bau-Stand)
ja    Fundstelle tle_modus: research/tb24_haltedauern/test_listen_erzeuger.py Z. 161 unveraendert (Bau-Stand)
ja    Fundstelle tle_p8: research/tb24_haltedauern/test_listen_erzeuger.py Z. 177 unveraendert (Bau-Stand)
ja    Fundstelle tle_tag: research/tb24_haltedauern/test_listen_erzeuger.py Z. 159–163 unveraendert (Bau-Stand)
ja    Fundstelle tle_wachen: research/tb24_haltedauern/test_listen_erzeuger.py Z. 85–86 unveraendert (Bau-Stand)
ja    Fundstelle wf: research/wf_kapital_dd/messung.py Z. 120 unveraendert (Bau-Stand)
Pruefungen: 41, NEIN: 0
rc 0
```

## Schritt R — Register 67 und neun Marken

Datum 17.10.2026 (`TZ=Europe/Berlin`). `r_probe.txt`: 5/0, rc 0. `r_eintrag.txt`: 8/0, rc 0 (nachher neun Marken je genau einmal, R107 mit Quellenzeile je genau einmal zeichengleich, append-only bis auf die neun Marken). R = `3a00cf8`.

Abschnitt 67 (`## 67. Fable 17b — Registerblock R107 (TB-175)`) ab **Z. 12624**. Die neun Marken aus `r_daten.json`:

| Ort | Kopf der Marke | Zeile |
|---|---|---|
| 16.4 | 16.4 ERGÄNZT durch R107 (67.1) | 2256 |
| 16.8 | 16.8 ERGÄNZT durch R107 (67.1) | 2469 |
| 55.4 | 55.4 R81 ERGÄNZT durch R107 (67.1) | 11805 |
| 56.3 | 56.3 R86 ERGÄNZT durch R107 (67.1) | 11914 |
| 57.3 | 57.3 R92 ERGÄNZT durch R107 (67.1) | 12038 |
| 58.4 | 58.4 R97 ERGÄNZT durch R107 (67.1) | 12124 |
| 62.3 | 62.3 R102 ERGÄNZT und BERICHTIGT durch R107 (67.1) | 12347 |
| 64.1 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1) | 12479 |
| 66.1 | 66.1 R106 ERGÄNZT durch R107 (67.1) | 12564 |

## Schritt K — Kopien, Index, Dialog-Index

| Beleg | rc |
|---|---|
| `k_registerkopie.txt` (sechs Teile, Abschnitt 67 in Teil 6, bytegleich, sha256 `8f464607b313cfe7`) | 0 |
| `k_abschnitte.txt` (68 Dateien, neu `REGISTER_KOPIE_ABSCHNITT_67.md`, bytegleich) | 0 |
| `k_pruefen.txt` | 0 |
| `k_index_zeilen.txt` (475 Zeilenangaben umgeschrieben, 337 geändert) | 0 |
| `k_index.txt` (5/0: T6, Kopf 0–67, Zeile 67, Abschnitt 18, Pflegezeile TB-175) | 0 |
| `k_handfelder.txt` | 0 |
| `k_dialog_index.txt` (68 von 68 Zeilen) | 0 |
| `k_dialog_pruefen.txt` | 0 |

Keine weitere Teildatei entstanden. Wie in TB-173 ändern sich die Köpfe aller Abschnittskopien mit. K = `9d72a7f`, porcelain danach leer.

## Schritt E — Teil 1: Prüfung 13

Prüfung 13 aus `e_alt.txt` (alter Test, am Stand vor E), wörtlich:

```
13. Wache: die Untersuchung fasst nichts ausserhalb ihres Ordners an
  ok    dieser Testlauf hat den Arbeitsbaum nicht veraendert
  FEHLT wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])

1 Pruefung(en) fehlgeschlagen:
  - wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])
rc 1
```

Prüfung 13 aus `e_neu.txt` (Test aus Anhang B), wörtlich:

```
13. Wache: die Untersuchung fasst nichts ausserhalb ihres Ordners an
  ok    dieser Testlauf hat den Arbeitsbaum nicht veraendert
  ok    wer schreibt, schreibt nur an einen erlaubten Ort (aussen vor: keine)
  ok    Gegenprobe 13: --ziel mit Voreinstellung -> positionen_holen.py faellt auf
  ok    Gegenprobe 13: --ziel nicht Pflicht -> positionen_holen.py faellt auf
  ok    Gegenprobe 13: ZIEL_DIR nicht aus --ziel -> positionen_holen.py faellt auf
  ok    Gegenprobe 13: O_EXCL durch O_TRUNC ersetzt -> positionen_holen.py faellt auf
  ok    Gegenprobe 13: open(..., "w") statt _schreibe_einmal -> positionen_holen.py faellt auf
  ok    Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf

Alle Pruefungen bestanden.
rc 0
```

ok-Zeilen vor Prüfung 13: **alt 50, neu 50, gleich** (`e_nachher.txt`).

`e_gegenprobe.txt`, ja-Zeilen wörtlich:

```
ja    Kopie kontrolle (/var/folders/b_/yqcfpq996cxb1_v02m180f580000gn/T/tb175_kontrolle_yq4qv7n8): Pruefung 13 gruen, FEHLT 0
ja    Kopie voreinstellung: Ersetzung 1-mal, Pruefung 13 rot: ["wer schreibt, schreibt nur an einen erlaubten Ort (aussen vor: [('positionen_holen.py', '--ziel mit Voreinstellung (default)')])"]
ja    Kopie open_w: Ersetzung 1-mal, Pruefung 13 rot: ["wer schreibt, schreibt nur an einen erlaubten Ort (aussen vor: [('positionen_holen.py', 'Z. 352 open ausserhalb von _schreibe_einmal')])", 'Gegenprobe 13: open(..., "w") statt _schreibe_einmal -> positionen_holen.py faellt auf (trifft 0-mal)']
Pruefungen: 3, NEIN: 0
rc 0
```

`e_nachher.txt`: 11/0, rc 0. Die fünf Programme der Gruppe sind unverändert, der Test im Repo ist gleich Anhang B (sha256 `b73adc87…`), Prüfung 13 hat 8 ok. Gelaufen mit `trading-env` (Python 3.9.6). Am Bau lief es auf 3.10.12 mit demselben Bild. Die Kopien der Gegenprobe liegen in `$TMPDIR`, ausserhalb des Repos. E = `9c31a65`.

## Teil (a) — entschieden (steuernder Chat, 17.10.2026: Vorschlag B)

Der Test rief `git status --porcelain` (Z. 317, 364) und `git diff` (Z. 319) ohne `--no-optional-locks`. git durfte dabei `.git/index` auffrischen und kurz `.git/index.lock` anlegen, was im porcelain nicht sichtbar ist. Hier läuft der Test nach ⟨S0⟩, wie in TB-169. Die Schwäche: Eine Inhaltsänderung an einer schon geänderten Datei ausserhalb der acht Produktivordner sieht (a) nicht. Gebaut ist nur `git --no-optional-locks` an diesen drei Aufrufen. Die Schwäche bleibt, denn Vorschlag A (Vergleich ohne git) ist nicht gebaut.

## Offen

- **Schwäche von (a):** Eine Inhaltsänderung an einer schon geänderten Datei ausserhalb der acht Produktivordner bleibt unsichtbar (Vorschlag A, nicht gebaut).
- **D4-Frage an den Verfahrensprüfer:** Über alle gefundenen Trades ergäbe D4 (`test_faltenplan_neun.py`) für t3_supertrend P90 8,6833 statt 9,5000 und Embargo 12 statt 13. Damit ändert sich eine registrierte Herleitung. Die übrigen acht Bots bleiben gleich. **Danach E2:** `auswertung.py` und `embargo_neun.py` auf alle gefundenen Trades (R107 (e)), als eigener Bauauftrag.
- **`research/mtm_drawdown/grundlage.py`** liest Startkapital und TB-24-Liste aus der Meta (Z. 189–198). Das widerspricht R107 (e) und 37.5 (2). Umstellen auf Rekonstruktion nach R97 (b) mit Startkapital aus Register 29.3.
- **`research/wf_kapital_dd/messung.py` Z. 120:** Das Startkapital kommt aus `es.STARTING_CAPITAL` statt aus Register 29.3. Das geht zur nächsten Fable-Anfrage.
- **67.2 (a)** ist eine Teilmessung: Verglichen wird mit Lauf B, und Prüfung 8 prüft den 3b-Lauf nicht. Zur Kenntnis an den Verfahrensprüfer.
- Aus R107 als eigene Bauaufträge vor R44: (a) der Zeilenschnitt bei `rsi2_mean_reversion`, `turtle_soup_stocks` und `volatility_breakout` (Handelscode, 37.3) und (c) die Modus-Wache im Listen-Erzeuger. Nach (d) laufen Kandidaten mit Orders nicht vor ihrer Zulassung. Alles steht in BACKLOG Rang 1.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-175.*
