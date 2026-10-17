# FABLE-Anfrage 17.10.e — R109: Tag in 3b gesetzt; Ort des Startkapitals ohne Sperrlisten-Pfad; Probe der Ergebniskurven

*Steuernder Chat, 17.10.2026, HEAD `e79ca2c`. **Registerfrage**, drei Befunde beim Bau zu R109 (TB-178, an einer Kopie gemessen, nichts gebaut). Dateien in der Projektablage unter projektfuehrung/.*

## Teil 0 — Kenntnis

Register `docs/VORREGISTRIERUNG_neuselektion.md`, Commit `53e8d54` (seither unverändert), 12 785 Zeilen, sha256 `c968a0ec5a2a92ea…`, Abschnitte 0–68, eingetragen bis R108. R109 steht in FABLE_ANTWORT_2026-10-17d (noch nicht eingetragen; Abschnitt 69 gibt es noch nicht). Dein Block beginnt bei **R110**.

## Frage (a) — R109 (b): Voraussetzung gemessen nicht erfüllt

R109 (b): „Ein von einem Test gesetzter Tag ist kein Handelbar-Tag nach R87 (a). [Voraussetzung, zu messen …] Stand: elliott_wave_stocks erfüllt mit TB-169 3b …“.

Gemessen: der Tag in 3b ist **vom Test gesetzt**. test_listen_erzeuger.py (Stand TB-169) Z. 74–77: `hb()` ersetzt `handelbar_ab` und überschreibt die Rechnung mit den übergebenen Tagen (`x.update(t)`); 3b (Z. 161): Tag von CCC = frühester alter Einstieg von CCC. Nicht aus der Rechnung nach 23.5. Damit trägt 3b auch elliott_wave_stocks nicht.

Gebauter Fall (Kopie, ohne data/, Skript probe_r109b.py; Symbol SPAET mit spätem Datenbeginn; **Tag aus der Rechnung**, kein Tag gesetzt), je 6 von 6 für t3_supertrend, elliott_wave, elliott_wave_stocks: rc 0 mit und ohne Schranke, bytegleich, Zählzeile 0; SPAET 3 / 1 / 2 Trades, keiner vor dem Tag. Gegenprobe ohne ruhigen Vorlauf: Lauf ohne Schranke rc 2 (R87 (c)). **Dafür tragen alle Symbole des Falls** (AAA, BBB, CCC, BTCUSDT, SPAET) einen ruhigen Vorlauf ohne Signal bis zu ihrem Tag; sonst handeln sie ab Datenbeginn vor dem Tag. Schwach: wenige Trades an SPAET, andere Seeds nicht gemessen.

**Frage:** Läuft elliott_wave_stocks am gebauten Fall mit (Stand-Satz in R109 (b) und Lesung von R106 (c))? Ist der ruhige Vorlauf aller Symbole des Falls zulässig, oder nur am eingesetzten Symbol?

## Frage (b) — R109 (a): Ort des Startkapitals

R109 (a): „sein Ort ist eine Konstante im Modul aus 38.5, mit Hash auf der Sperrliste; die Sonde prüft Datei und Wert (37.5 (1)).“

Gemessen: das Register nennt das Modul aus 38.5 (`shared/handelskosten.py`) nirgends (Volltext, 0 Treffer). Abschnitt 10 Punkt 9 spricht vom neuen Modul, „das mit Hash auf diese Liste kommt“, nennt aber keinen Pfad; letztes Abbild der Sperrliste (TB-117): 0 Treffer. Die Sonde (`shared/sperrlistensonde.py` Z. 17–23) misst Konstanten grundsätzlich nicht und meldet sie mit 2.

**Frage:** Braucht es vor dem Handelscode einen Registertext zur Sperrliste (Datei mit Pfad aufnehmen) und eine andere Bauart der Sonde für „Datei und Wert“ — oder genügt der Datei-Hash?

## Frage (c) — Folge für die Probe der Ergebniskurven

Gemessen: `shared/test_ergebniskurven.py` mutiert zur Probe den Text „STARTING_CAPITAL = 10_000.0“ in equity_simulation.py und prüft, dass er genau einmal ersetzt wurde (Z. 190–192, 289). Nach dem Umzug der Konstante wird der Test rot.

**Frage:** Ist die Anpassung der Probe (Mutation am Ort der Konstante) Handwerk?

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_10, _29, _37, _38, _56, _66, _67, _68 (Kopf `53e8d54`); FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, docs/belege/. Antwort höchstens 5 KB als projektfuehrung/FABLE_ANTWORT_2026-10-17e_<stichwort>.md: Kurz je Frage, Registerblock ab R110, Leseprotokoll nach R56 (b), Ampel.
