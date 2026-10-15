## EX — TB-162: Register 58 (R94–R97), Kapital-Drawdown E und M je WF-Abschnitt als Bericht (9 von 9, 0 nicht zuordenbar)
*Quelle: `docs/ERGEBNIS_TB-162_wf_kapital_dd.md`, Commits ⟨S0⟩ `9a1bc7a`, ⟨R⟩ `0e1e662`, ⟨K⟩ `4ec04df`, ⟨M⟩ `ac3e9f2`, ⟨F⟩ = der Commit „TB-162 Abgabe: Ergebnis, Journal EX“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** Die Mac-Sitzung TB-162 hat am 15.10.2026 den Auftrag `docs/auftraege/MAC_TB-162_wf_kapital_dd.md` in der Reihenfolge 0 ⇒ V ⇒ R ⇒ K ⇒ M ⇒ E abgearbeitet: Fable-Dateien 14.10.a/b in ⟨S0⟩, Voraussetzungen, Registerabschnitt 58 mit R94–R97 und 8 Marken, Registerkopien, Index und Dialog-Index, dann die Messung E und M der heutigen Parameter je Abschnitt des bot-eigenen Walk-Forward mit rekonstruierten Positionen (R97 (b)). Belegt unter `docs/belege/TB-162/`. Kein Abbruch; kein Aufruf abgelehnt, keine Bestätigung verlangt. Die Zahlen entscheiden nichts (24.3); sie stehen im Ergebnis als Vorschlag einer Tatsachennotiz, nicht im Register.

### Was gemessen ist
- **0a/Holbefehl:** Zweig `main`, HEAD `7b9f9ac`, genau die 10 Einträge; alle sechs sha256 (Werkzeug und fünf Moduldateien) wie Soll.
- **V:** `Pruefungen: 25, NEIN: 0`, rc 0.
- **R:** Probe 15/0, Eintrag 17/0, je rc 0; Abschnitt 58 ab Z. 12043, 8 Marken (Z. 5238, 5241, 10971, 10974, 11014, 11867, 12059, 12069); R94–R97 je genau einmal zeichengleich.
- **K:** alle acht Belege rc 0; neue Teildatei `REGISTER_KOPIE_teil6.md` (Abschnitt 58) wie in der Simulation; Kopien BYTEGLEICH mit dem Register am ⟨R⟩; 432 Zeilenangaben umgeschrieben, 251 geändert; Index 9/0; Dialog-Index 61 von 61 (offen 9, ohne Registertext 12, registriert 40).
- **M:** `test_fenster.py` 9 von 9, `test_rekonstruktion.py` 10 von 10; `messung.py --alle` rc 0, 9 von 9 Bots rc 0, Sperrliste vorher = nachher, Laufzeit 74,5 s auf Python 3.9.6.
- **Rekonstruktion:** bei allen neun Bots 0 nicht zuordenbar, alle Zuordnungen eindeutig nach Z1 (Z2 0, Z3 0); `kursdaten_symbole` > 0 bei allen; Trades nach dem Lauf unverändert.
- **E und M gesamt (Prozent):** elliott_wave −13,97/−16,42; elliott_wave_stocks −22,97/−20,91; rsi2_crypto −16,60/−25,02; rsi2_mean_reversion −19,53/−22,38; t3_supertrend −22,40/−24,36; turtle_soup_crypto −34,85/−38,55; turtle_soup_stocks −29,07/−33,93; volatility_breakout −22,46/−23,94; volatility_breakout_crypto −16,29/−19,30.
- **„M flacher als E“ (Befund, 24.6):** elliott_wave_stocks gesamt und IS (+2,06 pp), turtle_soup_stocks gemischt (+0,11 pp), volatility_breakout_crypto gemischt (+0,46 pp).
- **Grenzenstreuung:** rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout 1,0 Tag (Abschnitt „gemischt“ fast leer); elliott_wave_stocks 542 Tage; die fünf Krypto-Bots 724 bis 831 Tage.

### Was offen bleibt
- Abnahme der Handfelder 14a und 14b im Dialog-Index (Wortlaut des Baus) durch den steuernden Chat.
- Ob die vorgeschlagene Tatsachennotiz ins Register kommt (nicht in diesem Auftrag; F3).
- Frischer Gegenleser (F8).

### In einfacher Sprache
Die vier neuen Regeln R94–R97 stehen jetzt im Register. Danach wurde für jeden der neun Bots gemessen, wie tief das Konto mit den heutigen Einstellungen zwischendurch fiel, einmal nur an Ausstiegen und einmal täglich, auch getrennt nach den Zeitabschnitten des Walk-Forward. Die ausgeführten Positionen wurden aus einem unveränderten Lauf zurückgerechnet; keine einzige blieb ohne Zuordnung. Die Zahlen sind ein Bericht und entscheiden nichts.

*Geschrieben 15.10.2026 von der Mac-Sitzung TB-162. Quellenvermerk: siehe Kopf.*
