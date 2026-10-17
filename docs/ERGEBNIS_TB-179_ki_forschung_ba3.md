# Ergebnis TB-179 — KI-Forschung BA3: Regelblätter, Fragenkatalog v1, Prompts mit Manifest (sha256), Regel-Test

**Sitzung:** Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-179_ki_forschung_ba3.md` · **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6) · **Belege:** `docs/belege/TB-179/`

**Commits (alle auf `main`, gepusht):**

| Schritt | Commit | Inhalt |
|---|---|---|
| S0 | `cb62aee` | Auftrag (und `AKTUELLER_AUFTRAG.md`) |
| B | `afa5676` | `ki_forschung/regeln/` (fünf Blätter), `ki_forschung/prompts/` (zehn Prompts + `manifest.json`), `test_ki_regeln.py`, eine Zeile in `test_ki_wachen.py`; Belege 0a, V, B, T |
| A | dieser Commit | Ergebnis, BACKLOG, Journal FP |
| F | folgt | porcelain und numstat |

## Kurz

Alle Schritte liefen ohne Abbruch und ohne Nachfrage. Die 17 neuen Dateien sind sha256-gleich mit den Anhängen, `test_ki_wachen.py` nach der einen Zeile ebenfalls (`821c2120…`). Der Regel-Test meldet auf 3.9.6 `Pruefungen: 14, FEHLT: 0` (alle elf Gegenproben rot), der Wachen-Test `Pruefungen: 50, FEHLT: 0`, beide rc 0. Kein `.db`, kein `__pycache__` im Arbeitsbaum. Kein Abruf, kein API-Aufruf, kein Schlüssel, kein Handelscode; keine Regel, kein Prompt, kein Wert geändert. Keine Abweichung vom Soll.

## Schritt 0

0a: `0a gut (2 Eintraege)` (` M docs/auftraege/AKTUELLER_AUFTRAG.md`, `?? docs/auftraege/MAC_TB-179_ki_forschung_ba3.md`); Freigabe-Karte gefüllt. Holbefehl: 17 Anhänge mit den Soll-sha256, `Dateien 17`. Nach S0 war `git status --porcelain` leer.

## Schritt V

`v_voraussetzung.txt`, letzte Zeilen:

```
ja   ki_forschung/regeln fehlt
ja   ki_forschung/prompts fehlt
ja   ki_forschung/test_ki_regeln.py fehlt
ja   kein Modul in shared/strategies/notifications nennt ki_forschung []
Pruefungen: 11, NEIN: 0
rc 0
```

## Schritt B

`b_sha.txt` wörtlich:

```
regeln/sammler.md a12425d493e516018b64351708b79b36a02d24e62e29faaae5bd3d5128c838b4
regeln/filter.md 567c469ba8495776bc1d1f12347f605971b64ce54367521f98febe1d4faa38ac
regeln/regime_bot.md abe56d30393bb9a82adf506bc146fad57adc82070bb2eabb5dec50982022b070
regeln/rotations_bot.md d866551f8f06bb8f87827e3267e88d10f988b3770a96955d70bbb72e50b73bca
regeln/nachrichten_bot.md f4592c17a404530492e820f914264c8520cfedd73ee87c3870b8055152968705
prompts/nachrichten_bot.txt d7e6532dedc270c8d08d5dad6ca7227515948b86a3fb64d26c14ee5c4b85ae54
prompts/regime_bot.txt f6ab08a6dfc5321136c3b715f5e93c44173dc02bcbc0533c7a05211b769d33bc
prompts/rotations_bot.txt 9641a17bdf193eb687a6779918c6a91ea04c1f2ebfa58f851b16cd96795fd339
prompts/sammler_f1_risikoneigung.txt 8657c39a39c5719a775db6d45cd5f8734e01c27425debe0f2cda0673a3a89242
prompts/sammler_f2_trend.txt 8c2c15ca26dea29fa5e8b8489feb8f8585ae69d314197a15eb782033f2813c85
prompts/sammler_f3_vola_regime.txt 2eb59a1cf257835ddbb9b6a4d215fe18c062b9a095850063ddc6a5eae5f137f9
prompts/sammler_f4_makro.txt 3eb0022cd60567cfc50ed7af983ee5daab7a91c8533c76a80d45a664af550744
prompts/sammler_f5_liquiditaet.txt 8d42479b8cb10e324686225e874edd3ca43e37fe4eb4a56633422bdd8d9b7d85
prompts/sammler_f6_ereignisrisiko.txt d9c1ae746ad45ecd748d20701a23ffb7afd80698b9fd66bf252942e0a90f4e67
prompts/sammler_system.txt 2ca4331535326ff1ac7e1b6dd860058cb45ebaa8c5490484e77551f634b4bd10
prompts/manifest.json e4f6ac618ce869ee821eee7b084403d3685179f63d4bf5492cb2218f86d5c847
test_ki_regeln.py e800dd9521298395b016bc0acb2fb55b0e40d16be79dfe266cc664d63d7365ba
test_ki_wachen.py 821c2120a196311816b68112136613902d294f9ea64b6c674675d41ed975eae4
rc 0
```

## Schritt T

`t_regeln.txt` wörtlich:

```
Regel-Test KI-Forschung (TB-179)
  ok   R1-R3 Manifest: Modell, Prompts und Regelblaetter mit sha256
  ok   R4-R5 Regelblaetter: Pflichtfelder und Inhalt (5 Blaetter)
  ok   R6 Prompts: JSON verlangt, keine Websuche, keine Adresse
  ok   G1 Prompt um ein Zeichen geaendert wird rot   ['sha256 weicht ab: prompts/regime_bot.txt']
  ok   G2 Prompt ohne Manifest-Eintrag wird rot   ['Prompt ohne Eintrag: zusatz.txt']
  ok   G3 Modell im Manifest getauscht wird rot   ["Modell 'claude-sonnet-5xclaude-haiku-4-5-20251001' statt 'claude-haiku-4-5-20251001'"]
  ok   G4 Regelblatt nach dem Hash geaendert wird rot   ['sha256 weicht ab: regeln/filter.md']
  ok   G5 Pflichtfeld Ausstieg entfernt wird rot   ['regime_bot.md: Pflichtfeld Ausstieg fehlt']
  ok   G6 ISIN mit falscher Pruefziffer wird rot   ['regime_bot.md: ISIN IE00B5BMR088 Pruefziffer falsch']
  ok   G7 US-ETF im Universum wird rot   ['regime_bot.md: US-ISIN US78462F1030 (nur UCITS)']
  ok   G8 'nie Zulassungsgrund' entfernt wird rot   ["filter.md: Status ohne 'nie Zulassungsgrund'"]
  ok   G9 Rotation mit neun Krypto wird rot   ['rotations_bot.md: nicht genau 10 ETF und 10 Krypto']
  ok   G10 Pflichtfeld doppelt wird rot   ['sammler.md: Pflichtfeld Version doppelt']
  ok   G11 Websuche im Prompt wird rot   ["nachrichten_bot.txt nennt 'web_search'"]
Pruefungen: 14, FEHLT: 0
rc 0
```

`t_wachen.txt`, letzte drei Zeilen:

```
Pruefungen: 50, FEHLT: 0
temporaere Ordner entfernt: 18
rc 0
```

`t_status.txt` genau wie Soll: ` M ki_forschung/test_ki_wachen.py`, `?? docs/belege/TB-179/`, `?? ki_forschung/prompts/`, `?? ki_forschung/regeln/`, `?? ki_forschung/test_ki_regeln.py` (kein `.db`, kein `__pycache__`).

## A

`a_backlog_journal.txt`: sechs Prüfungen `ja`, `Kennung FP`, `Pruefungen: 6, NEIN: 0`, `rc 0`. Die Zeile hängt an der Rang-1-Zelle von `BACKLOG.md` nach dem TB-178-Anker, der Block FP steht im Journal vor `## Wiederkehrende Lehren`.

## Kurzfassungen

- **Sammler:** Jeden Morgen fragt der Sammler das KI-Modell sechs feste Fragen zu Krypto und zu Aktien (Risikoneigung, Trend, Schwankung, Makro, Liquidität, Termine), Antwort je −2 bis +2 mit kurzer Begründung. Er liest nur vorher eingefrorene Marktdaten, nie die Bots. Fällt ein Tag aus, bleibt er leer. Kosten geschätzt 0,75 $ im Monat.
- **Filter:** Steht die Risikoneigung eines Markts auf −2, wird nur nachgerechnet, was gewesen wäre, wenn die Bots dieses Markts an dem Tag nicht neu eingestiegen wären; die neun handeln unverändert. Verglichen werden gesperrte Einstiege, ihr Gewinn oder Verlust, Endstand und tiefster Rückgang mit und ohne Sperre, am 30.04.2027. Nur Bericht, nie Zulassungsgrund.
- **Regime-Bot:** Fragt jeden Morgen selbst, ob Bitcoin und der S&P 500 (UCITS-ETF) eher steigen oder fallen. Bei +1/+2 ist die jeweilige Hälfte des Papierkapitals investiert, bei −1/−2 nichts, bei 0 bleibt alles. Kein Stopp. Start 10 000, Gebühren wie die neun. Fällt das Konto 25 % unter seinen Höchststand, hört er auf. Auswertung 30.04.2027.
- **Rotations-Bot:** Jeden Montag ordnet das Modell zehn UCITS-ETFs und zehn Kryptowerte nach erwarteter Stärke, nur anhand vorher berechneter Kennzahlen. Gehalten werden je die ersten drei zu gleichen Teilen; was herausfällt, wird verkauft. Je die Hälfte von 10 000 für ETF und Krypto. Abbruch bei 25 % unter Höchststand. Auswertung 30.04.2027.
- **Nachrichten-Bot:** Täglich bewertet das Modell eingefrorene Schlagzeilen zu fünf Kryptowerten und fünf Index-ETFs mit −2 bis +2. Gekauft wird nur bei +2 und Kurs über dem 20-Tage-Schnitt, 1 000 je Kauf. Verkauft wird nach 5 Handelstagen oder bei −5 %. Start 10 000, Abbruch bei 25 % unter Höchststand, Auswertung 30.04.2027.

## Offene Entscheide (nicht in diesem Auftrag entschieden)

- **E1 Vorschläge:** mit der Karte vom 17.10.2026 bestätigt (ISINs und Symbole der Universen — Prüfziffer im Test geprüft, Existenz und Xetra-Handel nicht; Aktien-Instrument des Regime-Bots; Währung je Teiltopf; Uhrzeiten 06:15/06:30/06:45/07:00 UTC; Auswertedatum 30.04.2027; Abbruch bei 25 % unter Höchststand; Ausfallregeln; Filter-Nachrechnung ohne Neuanlage; Rotations-Kennzahlen; Nachrichten-Grössen, Stopp, Feeds, 30 Meldungen; ALFRED-Serien; F6 aus FRED-Release-Terminen; `max_tokens` 900). Ab dem B-Commit `afa5676` v1 und fest.
- **E2 Startkapital-Ort:** nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die Blätter nennen den Wert 10 000 der neun. Trägt der Ort denselben Wert, liest BA4 ihn dort (keine v2).
- **E3 Feed-Adressen (BA4) und Release-Auswahl für F6 (BA2):** vor dem ersten Lauf als Nachtrag mit Hash.
- **E4 Kosten (erschlossen, nicht gemessen):** Sammler rund 0,75 $/Monat; Bots rund 1,4 $/Monat; BA7 misst.
- **E5 MI1 (b)/K24:** Regime und Rotation entscheiden rein KI, nur für Paper gebrochen; nie Zulassungsgrund, nie im Selektionslauf.
- **E6 Auswerteplan (R108 (b)):** ob `filter.md` für den Filtervergleich als Auswerteplan genügt, entscheidet der Verfahrensprüfer.

## In einfacher Sprache

Die Spielregeln der KI-Versuche stehen jetzt fest im Repo: was der Sammler jeden Tag fragt, wann der Filter einen Einstieg der neun nur rechnerisch sperren würde, und wie die drei KI-Bots auf dem Papier kaufen und verkaufen. Jede Anweisung an das KI-Modell liegt als Datei mit Fingerabdruck (sha256) daneben, und ein Test schlägt an, wenn auch nur ein Zeichen abweicht oder eine Pflichtangabe fehlt — das wurde an elf absichtlich verfälschten Kopien nachgewiesen. Abgerufen, bezahlt oder gehandelt wurde heute nichts.
