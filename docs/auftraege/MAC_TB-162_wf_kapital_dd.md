# TB-162 Kapital-Drawdown im Walk-Forward, zulässige Messung (R94 (b)) mit rekonstruierten Positionen (R97 (b)); Register R94–R97 — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 15.10.2026, 16:18** (Helfer BAU162B, per Skript aus Bausteinen, `$HOME/sc/tb162/bau2/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an einer Kopie simuliert. Urteil und Freigabe beim steuernden Chat; ein frischer Gegenleser ist Pflicht (F8). **Gebaut am HEAD `7b9f9ac`.**

**Sitzungstitel:** `TB-162` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `7b9f9aceddc68a5365737683d466671904a42762` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-162`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-162_wf_kapital_dd.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`; Werkzeug `docs/belege/TB-162/tb162_werkzeug.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-162/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-162_wf_kapital_dd.md`. **Journal:** nächste freie Kennung (am Bau-HEAD höchste EW ⇒ EX).
**Grundlage:** Entscheide F1–F8 des steuernden Chats vom 14.10.2026, 21:58, und Nachtrag F9–F12 vom 15.10.2026, 08:08 (gehen vor); Fable 14.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md`, md5 `c33799567a0205f66c502dbf5aaff5c5`), Registerblock Z. 84–83; Fable 14.10.b (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md`, md5 `4b02ae62279294f5b1df4b1472cc2435`), Registerblock Z. 52–51. **Zeitgrenze:** jeder Bash-Aufruf mit dem Parameter `timeout` des Bash-Werkzeugs, 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge (F7):** Schritt 0 ⇒ V (Voraussetzungen, F5) ⇒ R (Register 58, Marken) ⇒ K (Kopien, Index, Dialog-Index; F6) ⇒ M (Messung, F1/F2/F4) ⇒ E (Ergebnis, Journal, Abgabe). Scheitert M, bleiben ⟨R⟩ und ⟨K⟩. **Positionen (F9):** `positionen_holen.py` wird weder ausgeführt noch eingebunden (Doppellauf verstösst gegen A9, R97 (a)); das Modul rekonstruiert die ausgeführten Positionen aus einem Lauf mit unveränderten Trades (R97 (b) zweiter Satz).

## ⭐ Regel vor der Messung (F3; 24.3) — wörtlich aus dem Register, per Skript

Die Zahlen aus Schritt M dienen allein diesen Regeln, als Bericht:
- **24.2** (Register Z. 4338): „Der ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht bewertet.“
- **24.3** (Z. 4362): „Der Drawdown der Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe gerechnet (1a); die Grösse der Abweichung zur ereignisindizierten Kurve wird gemessen und berichtet und ist für die Entscheidung ohne Belang.“ — und (Z. 4371): „… Eine Zahl, die nichts entscheiden darf, sollte nicht auf dem Tisch liegen, während entschieden wird.“
- **R36** (Z. 10863): „Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals.“
- **11.2 mit R43** (Z. 10936): „Tatsachennotiz zu 11.2: Die Voraussetzung „evaluate_combination_multi liefert den Kapital-Drawdown“ wird für den Lauf gegenstandslos; den Kapital-Drawdown liefert der Zellen-Kern (R36); Agent 2 ist Regelbetrieb.“

**Die Zahl entscheidet nichts.** Kein Score, kein Raster, kein IS-Sieger, keine Rangfolge, kein Vergleich gegen andere Parametersätze (R94 (a), (c); F1). Das Ergebnis steht im Ergebnis als **Vorschlag einer Tatsachennotiz** (Bauart 24.6) und kommt in diesem Auftrag **nicht** ins Register (F3). Die Notiz nennt die Positionen **Rekonstruktion** (R97 (b)), mit Zuordnungsregel und Toleranz (Kopf von `research/wf_kapital_dd/ergebnisse/tabelle.md`) und der Zahl nicht zuordenbarer Positionen je Bot; ein Bot mit mehr als null steht als „nicht vollständig zugeordnet“ in der Tabelle (F9). Für den Wert gilt R95 (b) und (c): kein Nachweis, keine Probe, keine Definition.

## Freigabe und Grenzen

Betreiberkarten 14.10.2026 („Zulässige Messung bauen“; „R94–R96 mit dem nächsten Auftrag“) und 15.10.2026 („(a) Rekonstruktion“); Entscheide F1–F12. **Schreiben darf die Sitzung nur:** `docs/VORREGISTRIERUNG_neuselektion.md` (R, nur `WZ register`), `docs/projektfuehrung/REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), `research/wf_kapital_dd/` (M), `docs/belege/TB-162/`, `docs/projektfuehrung/JOURNAL.md` (`WZ journal`), das Ergebnis. **Nicht:** `strategies/`, `shared/`, `research/vorregistrierung/`, `research/mtm_drawdown/`, `research/tb24_haltedauern/`, `research/exposure_messung/`, `data/`, `config/`. `research/tb24_haltedauern/positionen_holen.py` wird nicht aufgerufen (F9); aus `research/exposure_messung/bot_lauf.py` nutzt das Modul nur `hole_trades` (Import; `bot_lauf.simuliere` nicht, weil es ohne Kursdaten simuliert; `bot_lauf.main()` mit dem Doppellauf läuft nie). Kein Netz (`bot_lauf.py` stubbt Binance/yfinance); kein `pip`, kein `brew`.

## Lage nach dem Auslegen

Am Bau-HEAD `7b9f9ac`: geändert `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/projektfuehrung/UEBERGABE.md`; unverfolgt `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md`, `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md`, `docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md`, `docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md`. Das Auslegen ändert dazu `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab. **Beim Start genau 10 Einträge** (Soll in 0a).

## Belegt · erschlossen · offen (am Bau)

**Belegt:** Sperrliste `research/vorregistrierung/herkunft.py` Z. 102–106 nennt die fünf Muster aus R94; Abschnitte 9, 11, 24, 37, 41, 51, 54 am Stand `3f2e97e` zeichengleich mit `d950e03` (37 und 41 am 15.10. vom steuernden Chat gemessen, F11 (2)); Register seit `3f2e97e` unverändert; `positionen_holen.py` und `shared/zuteilung.py` seit `7b9f9ac` unverändert (F11 (3)); die sechs Fable-Dateien 14.10.a und 14.10.b liegen unverfolgt im Arbeitsbaum und kommen in ⟨S0⟩ (F11 (1), R56 (b)). **An einer Kopie mit echter `data/` (Python 3.10):** `test_fenster.py` 9 von 9, `test_rekonstruktion.py` 10 von 10; `messung.py --alle` rc 0, neun Bots rc 0, Sperrliste vorher = nachher, **nicht zuordenbare Positionen je Bot: 0** bei allen neun. Am Bau gefunden und im Modul berücksichtigt: nach `entry_time` sortiert schliesst die Kapitalkette in `mtm_kern.ereignisreihenfolge` für `rsi2_mean_reversion` nicht (Gleichstand im Ausstieg mit Nullschritt); die Liste steht darum in der Buchungsreihenfolge der `equity_curve` (Spalte `kurvenzeile`).
**Zuordnungsregel und Toleranz (F9; `rekonstruktion.py`, Anhang A):** Z1 gleiches Symbol, `exit_time` = `time` der Kurvenzeile (UTC), |Δ pnl_pct| ≤ 1e-9; Z2 bei mehreren Kandidaten Kapitalprobe |allocation − allocation_pct × Kapital beim Einstieg| ≤ 0,01; Z3 inhaltsgleiche Kandidaten: kleinste Zeile; Z4 sonst nicht zuordenbar, gezählt und gemeldet. Der Lauf ist `simulate_portfolio` des Bots mit denselben Argumenten wie sein `__main__` (`all_data` als `kursdaten` per Keyword, `MAX_CONCURRENT_POSITIONS`, wo die Signatur es hat; Stufe 2 und 3 der Zuteilungskaskade aktiv); `kursdaten_symbole`, `final_capital`, `num_executed` und `num_skipped` der Rückgabe stehen in der Meta; ist `kursdaten_symbole` 0, bricht der Bot ab. Der Lauf bekommt die Trades unverändert; `trades.equals(Kopie vor dem Lauf)` wird geprüft, sonst Abbruch.
**Offen, nur am Mac messbar:** ob V dort mit `rc 0` endet; ob die Zahl nicht zuordenbarer Positionen dort ebenso 0 ist; Laufzeiten; ob Python 3.9 am Mac die Module so liest.

## Schritt 0 — Ausgang

**0a. Zuerst:** `git status --porcelain > "$TMPDIR/tb162_0a.txt"`, `git rev-parse HEAD` und `git rev-parse --abbrev-ref HEAD`. Soll: Zweig `main`, HEAD `7b9f9aceddc68a5365737683d466671904a42762` und genau diese 10 Einträge; sonst **ABBRUCH** (vor ⟨S0⟩ und vor jedem Push). Kein späterer Schritt wechselt den Zweig.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-162_wf_kapital_dd.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md
```

Werkzeug und Modul aus den Anhängen holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-162_wf_kapital_dd.md "$TMPDIR" <<'EOF'
import hashlib, os, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
os.makedirs(sys.argv[2] + "/tb162_modul", exist_ok=True)
for kopf, ziel in (("### Werkzeug", "tb162_werkzeug.py"), ("### research/wf_kapital_dd/fenster.py", "tb162_modul/fenster.py"), ("### research/wf_kapital_dd/messung.py", "tb162_modul/messung.py"), ("### research/wf_kapital_dd/rekonstruktion.py", "tb162_modul/rekonstruktion.py"), ("### research/wf_kapital_dd/test_fenster.py", "tb162_modul/test_fenster.py"), ("### research/wf_kapital_dd/test_rekonstruktion.py", "tb162_modul/test_rekonstruktion.py")):
    a = z.index("```python", z.index(kopf))
    t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
    open(sys.argv[2] + "/" + ziel, "w", encoding="utf-8").write(t)
    print(ziel, hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll genau: `tb162_werkzeug.py 34e70f6c9e8c732a6ea4e9a2b0526e6009903761aa05361ed769ea9207cb72c7` · `tb162_modul/fenster.py 203636cb4c28b7cf1b93195c04f54e008ba388128c07e17cab87d82a17ae6572` · `tb162_modul/messung.py 048187721460013b0048005b48a9417afc1c715de8eccba8fae0164bd52d1c21` · `tb162_modul/rekonstruktion.py 6a699e62f7604f196c3ed0d3588ebbcce1a52f46fe5bf010bd67ea1ef0ac97a4` · `tb162_modul/test_fenster.py be9c814766432e957250c8d4d11ec35d22521f0f227d496a448d6fbf9a1776c9` · `tb162_modul/test_rekonstruktion.py 6efca888f686f3a1c15c5c663100cb40de919d467db118a28beb11c0c1766d88`; sonst **ABBRUCH**. Commit `TB-162 Schritt 0: Stand des steuernden Chats vor TB-162` mit genau diesen Pfaden, pushen ⇒ **⟨S0⟩** (7 Zeichen). Erst danach: `mkdir -p docs/belege/TB-162`, `cp "$TMPDIR/tb162_0a.txt" docs/belege/TB-162/0a_status.txt`, `cp "$TMPDIR/tb162_werkzeug.py" docs/belege/TB-162/tb162_werkzeug.py` (je `diff` ohne Ausgabe).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-162_wf_kapital_dd.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md
```

## Schritt V — Voraussetzungen (F5)

```
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py voraussetzung > docs/belege/TB-162/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0`, davor `Pruefungen: 25, NEIN: 0`. Gemessen werden (F5 mit F11): Sperrliste Z. 102–106 (R94); neun Walk-Forward-Rechner verfolgt; Abschnitte 9, 11, 24, 37, 41, 51, 54 an `3f2e97e` = `d950e03` (R94, R96 (b), R97 (f)); Register seit `3f2e97e` unverändert; `positionen_holen.py` und `shared/zuteilung.py` am HEAD unverändert gegen `7b9f9ac` (F11 (3); Verhalten nach der Wiedergabe in 14.10.b); die sechs Fable-Dateien 14.10.a und 14.10.b verfolgt und gleich HEAD (F11 (1), R56 (b)); md5 beider Antworten; R94–R97 und 58 noch nicht im Register. **Endet V nicht mit `rc 0`: kein Registereintrag, keine Messung** (F11). Dann: Commit `TB-162 V: Voraussetzung verletzt, kein Registereintrag` mit den drei Zeilen unten, pushen, weiter mit **Schritt E** (Ergebnis nennt jede NEIN-Zeile wörtlich).

```
git add docs/belege/TB-162/0a_status.txt
git add docs/belege/TB-162/tb162_werkzeug.py
git add docs/belege/TB-162/v_voraussetzung.txt
```

## Schritt R — Register 58 und Marken (F5)

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-162/v_voraussetzung.txt --probe > docs/belege/TB-162/r_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/r_probe.txt
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-162/v_voraussetzung.txt > docs/belege/TB-162/r_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/r_eintrag.txt
```

Soll je `rc 0`, keine NEIN-Zeile; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach steht am Registerende `## 58. Fable 14a und 14b — Registerblock R94–R97 (TB-162)` mit 58.1–58.3 (R94–R96 zeichengleich aus dem Codeblock 14.10.a), 58.4 (R97 zeichengleich aus dem Codeblock 14.10.b; F10), je Zeilenpaar `> R9x — …` / `> Quelle des Grundes: …`, und 58.5 (die Zeilen aus `v_voraussetzung.txt`; bisher 58.4). Marken, der alte Satz bleibt zeichengleich: nach R96 (d) Abschnitt 27 und 48.14 (R46) ERGÄNZT durch R94 (58.1), 48.13 (R45) und 56.1 (R84) PRÄZISIERT durch R95 (58.2); nach R97 (e) 58.2 (R95) und 58.3 (R96) BERICHTIGT durch R97 (58.4), 48.13 (R45) und Abschnitt 27 ERGÄNZT durch R97 (58.4) — zusammen 8. Zählung (F12): R96 (c) bleibt zeichengleich, gilt in der Lesart von R97 (d) („Gezählt sind fünfzehn Fälle.“); die Indexzeilen 48.20 und 54.3 nennen fünfzehn (Schritt K). Commit `TB-162 R: Register 58 (R94–R97 zeichengleich), 8 Marken`, pushen ⇒ **⟨R⟩**.

```
git add docs/belege/TB-162/0a_status.txt
git add docs/belege/TB-162/tb162_werkzeug.py
git add docs/belege/TB-162/v_voraussetzung.txt
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-162/r_probe.txt
git add docs/belege/TB-162/r_eintrag.txt
git add docs/belege/TB-162/r_daten.json
```

## Schritt K — Kopien, Index, Dialog-Index (F5, F6)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-162/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-162/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-162/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨R⟩ > docs/belege/TB-162/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-162/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py handfelder docs/belege/TB-162/k_handfelder.json > docs/belege/TB-162/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-162/k_handfelder.json > docs/belege/TB-162/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-162/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. `registerkopie.py` schreibt die Teildateien und alle Abschnittskopien neu (darunter 9, 11, 24, 51, 54 und neu 58; F6); in der Simulation legt es für 58 die neue Teildatei `docs/projektfuehrung/REGISTER_KOPIE_teil6.md` an (Teilwechsel; im Block unten genannt) — entsteht sie nicht oder eine andere: festhalten, mit Namen anpassen, melden; `c2_index_zeilen.py` (aus TB-154, unverändert) schreibt die Zeilenangaben des Index von ⟨S0⟩ auf ⟨R⟩ um; `WZ index` setzt Kopf, Tabelle 4 (27, 48, 56), Zeile 58, Abschnitt 13 mit den 8 Marken und den Indexzeilen 48.20/54.3 (fünfzehn Fälle, R97 (d); F12) und Abschnitt 10 Punkt 10 (R97 (b)) und die Pflegezeile. Handfelder 14a und 14b: *Wortlaut des Baus, zur Abnahme durch den steuernden Chat*. rc ≠ 0 eines Schritts: festhalten, die Dateien dieses Schritts nicht committen, melden (kein Abbruch). Commit `TB-162 K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**.

```
git add docs/projektfuehrung/REGISTER_INDEX.md
git add docs/projektfuehrung/FABLE_DIALOG_INDEX.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil1.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil2.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil3.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil4.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil5.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil6.md
git add docs/projektfuehrung/register_kopie
git add docs/belege/TB-162/k_registerkopie.txt
git add docs/belege/TB-162/k_abschnitte.txt
git add docs/belege/TB-162/k_pruefen.txt
git add docs/belege/TB-162/k_index_zeilen.txt
git add docs/belege/TB-162/k_index.txt
git add docs/belege/TB-162/k_handfelder.txt
git add docs/belege/TB-162/k_dialog_index.txt
git add docs/belege/TB-162/k_dialog_pruefen.txt
git add docs/belege/TB-162/k_handfelder.json
```

## Schritt M — Messung (F1, F2, F4)

Zuerst die Proben, dann die Messung (die Positionen rekonstruiert `messung.py` je Bot selbst, F9; kein `positionen_holen.py`):

```
mkdir -p research/wf_kapital_dd
cp "$TMPDIR"/tb162_modul/fenster.py "$TMPDIR"/tb162_modul/messung.py "$TMPDIR"/tb162_modul/rekonstruktion.py "$TMPDIR"/tb162_modul/test_fenster.py "$TMPDIR"/tb162_modul/test_rekonstruktion.py research/wf_kapital_dd/
trading-env/bin/python3 -B research/wf_kapital_dd/test_fenster.py > docs/belege/TB-162/m_test.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/m_test.txt
trading-env/bin/python3 -B research/wf_kapital_dd/test_rekonstruktion.py > docs/belege/TB-162/m_test_rekonstruktion.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/m_test_rekonstruktion.txt
trading-env/bin/python3 -B research/wf_kapital_dd/messung.py --alle > docs/belege/TB-162/m_messung.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/m_messung.txt
```

Soll: `m_test.txt` „9 von 9 Pruefungen bestanden“ und `m_test_rekonstruktion.txt` „10 von 10 Pruefungen bestanden“, je `rc 0` — sonst **ABBRUCH** (F4). `m_messung.txt` endet mit `Sperrliste vorher = nachher: True; Bots rc 0: 9 von 9` und `rc 0` — sonst **ABBRUCH der Messung** (F7: ⟨R⟩, ⟨K⟩ bleiben; die letzte Fehlerzeile je Bot aus `ergebnisse/laufprotokoll.json` wörtlich melden; **keine** andere Positionsquelle, nicht die TB-24-Listen, nicht `positionen_holen.py`). Nicht zuordenbare Positionen je Bot (`ergebnisse/<bot>.json`, Feld `rekonstruktion.nicht_zuordenbar`) ins Ergebnis; ein Bot mit mehr als null steht als „nicht vollständig zugeordnet“ in `tabelle.md` (F9) — Befund, kein Abbruch. „M flacher als E“ in einem Abschnitt ist ein Befund (24.6), kein Abbruch. Commit `TB-162 M: Messung E und M je WF-Abschnitt`, pushen ⇒ **⟨M⟩**.

```
git add research/wf_kapital_dd/fenster.py
git add research/wf_kapital_dd/messung.py
git add research/wf_kapital_dd/rekonstruktion.py
git add research/wf_kapital_dd/test_fenster.py
git add research/wf_kapital_dd/test_rekonstruktion.py
git add research/wf_kapital_dd/daten
git add research/wf_kapital_dd/ergebnisse
git add docs/belege/TB-162/m_test.txt
git add docs/belege/TB-162/m_test_rekonstruktion.txt
git add docs/belege/TB-162/m_messung.txt
```

## Schritt E — Ergebnis, Journal, Abgabe

`trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py kennung > docs/belege/TB-162/e_kennung.txt; echo "rc $?" >> docs/belege/TB-162/e_kennung.txt` (Soll „Kennung EX …“, `rc 0`); Block nach `BEL/e_block.md` (Schreibwerkzeug; erste Zeile `## <Kennung> — TB-162: …`, Quellenzeile, `**Quelle:**`, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; keine weitere `## `-Zeile, kein `---`), dann:

```
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py journal docs/belege/TB-162/e_block.md --probe > docs/belege/TB-162/e_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/e_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-162/tb162_werkzeug.py journal docs/belege/TB-162/e_block.md > docs/belege/TB-162/e_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-162/e_journal.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: zweiten nicht ausführen, **ABBRUCH**. **Ergebnis** `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` (Schreibwerkzeug): Kopf mit Commits · „Kurz“ · **Voraussetzungen** (`v_voraussetzung.txt` wörtlich) · Register (oder: nicht eingetragen, warum) · Messung: `research/wf_kapital_dd/ergebnisse/tabelle.md` wörtlich, Rekonstruktion je Bot (zugeordnet, nicht zuordenbar, Z2/Z3-Fälle, `kursdaten_symbole` aus `ergebnisse/<bot>.json`), Grenzen-Streuung je Bot, Datenbestand, sha256 der Parameterdateien und Commit (`ergebnisse/vorher.json`), Sperrliste vorher/nachher · **Vorschlag Tatsachennotiz** (Bauart 24.6, nicht eingetragen; F3; „Rekonstruktion“ mit Regel und Toleranz, F9; mit dem Satz: „Der Aufruf von simulate_portfolio ist argumentgleich mit dem __main__ des Bots (am Code geprüft); es gibt keinen zweiten Bot-Lauf zum Abgleich.“ und je Bot `final_capital`, `num_executed`, `num_skipped` aus der Meta) · Abweichungen · **In einfacher Sprache**. Commit `TB-162 Abgabe: Ergebnis, Journal <Kennung>` (erster Block), pushen ⇒ **⟨F⟩**; dann `git status --porcelain > "$TMPDIR/tb162_f.txt"`, `cp "$TMPDIR/tb162_f.txt" docs/belege/TB-162/f_porcelain.txt`, `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-162/f_numstat.txt`, Commit `TB-162 F: porcelain und numstat` (zweiter Block), pushen.

```
git add docs/ERGEBNIS_TB-162_wf_kapital_dd.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-162/e_kennung.txt
git add docs/belege/TB-162/e_block.md
git add docs/belege/TB-162/e_journal_probe.txt
git add docs/belege/TB-162/e_journal.txt
```

```
git add docs/belege/TB-162/f_porcelain.txt
git add docs/belege/TB-162/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab; Holbefehl-Soll weicht ab; `WZ register --probe`/`register` nicht `rc 0`; `m_test.txt` nicht 9 von 9 oder `m_test_rekonstruktion.txt` nicht 10 von 10; `messung.py --alle` nicht `rc 0`; `WZ journal` nicht `rc 0`; `git push` scheitert zweimal (nicht für den Abbruch-Commit); Claude Code verlangt eine Bestätigung (melden, nicht umgehen). **Kein Abbruch:** V endet NEIN (Weg über E, s. V); ein Schritt in K mit rc ≠ 0; „M flacher als E“.
**Abbruchweg:** vor ⟨S0⟩ nichts schreiben, nur melden. Danach genau eine neue Datei `printf '%s\n' "<Schritt>: <Grund>" > docs/belege/TB-162/abbruch.txt`, `git add` dieser Datei und jeder schon entstandenen, nicht committeten Datei aus dem Anhang „Dateien“ mit Namen (nie `git add -A`, nie `-f`), Commit `TB-162 Abbruch: <Schritt>`, pushen, melden. **Scheitert Commit oder Push des Abbruch-Commits: nicht wiederholen, anhalten, melden.** Nichts zurückdrehen (kein `reset`, `revert`, `restore`, `checkout`).

## In einfacher Sprache

Der Verfahrensprüfer hat gesagt: Vor dem Stichtag darf niemand auf den Kursdaten nach besseren Parametern suchen — aber messen, wie tief das Konto der heutigen Einstellungen zwischendurch fällt, ist erlaubt, auch getrennt nach den Zeitabschnitten des Walk-Forward. Das alte Werkzeug, das die ausgeführten Positionen holte, markierte dafür die Symbole; das verbietet eine Registerregel (A9), und es verändert heute auch die Rechnung. Darum rechnet diese Sitzung die Simulation einmal ganz unverändert und ordnet die ausgeführten Positionen danach aus der Kapitalkurve zu — eine Rekonstruktion, die als solche benannt wird, mit Regel, Toleranz und der Zahl der Positionen, die sich nicht eindeutig zuordnen lassen (beim Bau: keine). Vorher trägt sie die vier Regeln R94–R97 ins Register ein, wenn die Voraussetzungen stimmen. Die Zahlen entscheiden nichts; sie sind ein Bericht.

## Anhang — Dateien und ihre Befehle

| Datei | Befehl |
|---|---|
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/UEBERGABE.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/auftraege/MAC_TB-162_wf_kapital_dd.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/belege/TB-162/0a_status.txt` | 0a, `cp` nach ⟨S0⟩ |
| `docs/belege/TB-162/tb162_werkzeug.py` | Holbefehl, `cp` nach ⟨S0⟩ |
| `docs/belege/TB-162/v_voraussetzung.txt` | Schritt V |
| `docs/VORREGISTRIERUNG_neuselektion.md` | `WZ register` (R) |
| `docs/belege/TB-162/r_probe.txt` | R |
| `docs/belege/TB-162/r_eintrag.txt` | R |
| `docs/belege/TB-162/r_daten.json` | `WZ register` (R) |
| `docs/projektfuehrung/REGISTER_INDEX.md` | Schritt K |
| `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil1.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil2.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil3.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil4.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil5.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil6.md` | Schritt K |
| `docs/projektfuehrung/register_kopie` | Schritt K |
| `docs/belege/TB-162/k_registerkopie.txt` | Schritt K |
| `docs/belege/TB-162/k_abschnitte.txt` | Schritt K |
| `docs/belege/TB-162/k_pruefen.txt` | Schritt K |
| `docs/belege/TB-162/k_index_zeilen.txt` | Schritt K |
| `docs/belege/TB-162/k_index.txt` | Schritt K |
| `docs/belege/TB-162/k_handfelder.txt` | Schritt K |
| `docs/belege/TB-162/k_dialog_index.txt` | Schritt K |
| `docs/belege/TB-162/k_dialog_pruefen.txt` | Schritt K |
| `docs/belege/TB-162/k_handfelder.json` | Schritt K |
| `research/wf_kapital_dd/fenster.py` | Schritt M |
| `research/wf_kapital_dd/messung.py` | Schritt M |
| `research/wf_kapital_dd/rekonstruktion.py` | Schritt M |
| `research/wf_kapital_dd/test_fenster.py` | Schritt M |
| `research/wf_kapital_dd/test_rekonstruktion.py` | Schritt M |
| `research/wf_kapital_dd/daten` | Schritt M |
| `research/wf_kapital_dd/ergebnisse` | Schritt M |
| `docs/belege/TB-162/m_test.txt` | Schritt M |
| `docs/belege/TB-162/m_test_rekonstruktion.txt` | Schritt M |
| `docs/belege/TB-162/m_messung.txt` | Schritt M |
| `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` | Schritt E |
| `docs/projektfuehrung/JOURNAL.md` | Schritt E |
| `docs/belege/TB-162/e_kennung.txt` | Schritt E |
| `docs/belege/TB-162/e_block.md` | Schritt E |
| `docs/belege/TB-162/e_journal_probe.txt` | Schritt E |
| `docs/belege/TB-162/e_journal.txt` | Schritt E |
| `docs/belege/TB-162/f_porcelain.txt`, `docs/belege/TB-162/f_numstat.txt` | Abgabe |
| `docs/belege/TB-162/abbruch.txt` | nur Abbruchweg |
| `$TMPDIR/tb162_*` | 0a, Holbefehl, Abgabe; bleiben liegen |

## Anhang A — Modul `research/wf_kapital_dd/` (wörtlich)

### research/wf_kapital_dd/fenster.py

```python
"""
TB-162 - Fenster des bot-eigenen Walk-Forward, ohne Rastersuche (reine Funktionen)
==============================================================================
Register R94 (b) (Fable 14.10.a): zulaessig vor dem Tag ist E und M der
heutigen Parameter, auch in den Fenstern des bot-eigenen Walk-Forward. Die
Fenster kommen aus `split_all_symbols` des Bots (importiert vom Aufrufer,
`__main__` des Bots laeuft nie; R88 (e), R95 (a)). Hier steht nur, wie aus
dessen Rueckgabe die Grenze je Symbol gelesen wird und wie daraus die drei
Abschnitte EINES durchgehenden Kapitalpfads werden (R36: Ausschnitt, kein
Neustart des Kapitals; Entscheid F2 TB-162):

  IS        vom Pfadbeginn bis zur fruehesten Symbolgrenze
  gemischt  von der fruehesten bis zur spaetesten Symbolgrenze
  OOS       ab der spaetesten Symbolgrenze bis zum Pfadende
  gesamt    der ganze Pfad

Zwei Bauarten der Rueckgabe (gelesen, nicht nachgebaut):
  zeitbasiert   train[s] = (kurse, start|None, split_time), test[s] = (kurse, split_time, None)
  zeilenbasiert train[s] = kurse.iloc[:k], test[s] = kurse.iloc[k:]  -> Grenze = open_time der Zeile k
Kein Raster, kein Score, keine Auswahl: diese Datei rechnet keine Kennzahl.
"""
import pandas as pd

ABSCHNITTE = ("gesamt", "IS", "gemischt", "OOS")


def _ts(x):
    t = pd.Timestamp(x)
    return t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t


def grenze_je_symbol(train: dict, test: dict) -> dict:
    """Grenze je Symbol aus der Rueckgabe von split_all_symbols; None, wenn das Symbol keinen OOS-Teil hat."""
    aus = {}
    for s in sorted(set(train) | set(test)):
        tr, te = train.get(s), test.get(s)
        if isinstance(tr, tuple) or isinstance(te, tuple):
            g_tr = tr[2] if isinstance(tr, tuple) and len(tr) == 3 else None
            g_te = te[1] if isinstance(te, tuple) and len(te) == 3 else None
            if tr is not None and not isinstance(tr, tuple) or te is not None and not isinstance(te, tuple):
                raise ValueError("%s: gemischte Bauart der Rueckgabe" % s)
            if g_tr is not None and g_te is not None and _ts(g_tr) != _ts(g_te):
                raise ValueError("%s: Grenze IS %s ungleich Grenze OOS %s" % (s, g_tr, g_te))
            g = g_te if g_te is not None else g_tr
        elif isinstance(te, pd.DataFrame):
            g = te["open_time"].iloc[0] if len(te) else None
        else:
            raise ValueError("%s: unbekannte Bauart %s" % (s, type(te).__name__))
        aus[s] = None if g is None else _ts(g)
    return aus


def streuung(grenzen: dict) -> dict:
    g = sorted(v for v in grenzen.values() if v is not None)
    if not g:
        raise ValueError("kein Symbol mit Grenze")
    return {"symbole": len(grenzen), "symbole_ohne_grenze": sorted(k for k, v in grenzen.items() if v is None),
            "frueheste": str(g[0]), "spaeteste": str(g[-1]), "median": str(pd.Series(g).median()),
            "spannweite_tage": round((g[-1] - g[0]).total_seconds() / 86400.0, 2)}


def abschnitte(grenzen: dict, von, bis) -> list:
    """Die vier Ausschnitte des einen Pfads [von, bis) in der Form von messe_falten (mtm_kern)."""
    st = streuung(grenzen)
    von, bis = _ts(von), _ts(bis)
    frueh, spaet = pd.Timestamp(st["frueheste"]), pd.Timestamp(st["spaeteste"])
    if not (von <= frueh <= spaet <= bis):
        raise ValueError("Grenzen %s..%s liegen nicht im Pfad %s..%s" % (frueh, spaet, von, bis))
    return [{"name": "gesamt", "rolle": "durchgehender Pfad", "von": von, "bis_ausschliesslich": bis},
            {"name": "IS", "rolle": "bis zur fruehesten Symbolgrenze", "von": von, "bis_ausschliesslich": frueh},
            {"name": "gemischt", "rolle": "zwischen fruehester und spaetester Symbolgrenze", "von": frueh, "bis_ausschliesslich": spaet},
            {"name": "OOS", "rolle": "ab der spaetesten Symbolgrenze", "von": spaet, "bis_ausschliesslich": bis}]
```

### research/wf_kapital_dd/messung.py

```python
#!/usr/bin/env python3
"""
TB-162 - Kapital-Drawdown E und M der heutigen Parameter, je Abschnitt des bot-eigenen Walk-Forward
==============================================================================
Register R94 (b) (Fable 14.10.a), Bauart 24.6 / TB-73. Fuer jeden der neun
Bots auf DENSELBEN ausgefuehrten Positionen der heutigen Parameter (R47), REKONSTRUIERT
nach R97 (b) zweiter Satz (Entscheid F9; rekonstruktion.py): EIN Lauf mit unveraenderten
Trades (bot_lauf.hole_trades; simulate_portfolio des Bots wie in dessen __main__, mit
all_data als kursdaten - Stufe 2/3 der Kaskade aktiv; bot_lauf.main() mit dem Doppellauf wird nie
aufgerufen, positionen_holen.py weder ausgefuehrt noch eingebunden; A9, R97 (a)), Zuordnung
aus Trade-Liste und equity_curve; nicht zuordenbare Positionen je Bot gemeldet:
E (ereignisindiziert) und M (MtM taeglich) mit research/mtm_drawdown/mtm_kern.py,
auf dem EINEN durchgehenden Pfad ohne Neustart (R36), ausgeschnitten in die
Abschnitte aus fenster.py (gesamt, IS, gemischt, OOS; Entscheid F2).
Die Grenzen je Symbol kommen aus split_all_symbols des Bots (importiert; __main__
des Bots laeuft nie, keine Rastersuche, kein IS-Sieger, kein Score; R94 (a), (c)).
Diese Zahl entscheidet nichts (24.3); sie dient 24.2, 24.3, R36 und 11.2 mit R43
nur als Bericht (Tatsachennotiz-Vorschlag, nicht ins Register).

Aufruf:  python3 -B research/wf_kapital_dd/messung.py <bot>      ein Bot (eigener Prozess)
         python3 -B research/wf_kapital_dd/messung.py --alle     neun Kindprozesse, Nachweise, Tabelle
"""
import glob, hashlib, importlib, importlib.util, json, os, subprocess, sys, time
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
DATEN = os.path.join(_HIER, "daten")
ERGEBNISSE = os.path.join(_HIER, "ergebnisse")
BOTS = ("elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion", "t3_supertrend",
        "turtle_soup_crypto", "turtle_soup_stocks", "volatility_breakout", "volatility_breakout_crypto")
sys.path.insert(0, _HIER)
import fenster  # noqa: E402
from rekonstruktion import REGEL  # noqa: E402


def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _mtm_messung():
    """research/mtm_drawdown/messung.py unter eigenem Namen laden (gleicher Dateiname wie hier)."""
    p = os.path.join(REPO_ROOT, "research", "mtm_drawdown", "messung.py")
    spec = importlib.util.spec_from_file_location("mtm_messung", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _kurse(w):
    """load_all_symbol_data liefert {symbol: df} oder {symbol: (df, entry_cutoff)} (shared/zuteilung.py Z. 215-217)."""
    return w[0] if isinstance(w, tuple) else w


def datenbestand(all_data: dict) -> dict:
    h = hashlib.sha256()
    for s in sorted(all_data):
        df = _kurse(all_data[s])
        h.update(("%s|%d|%s|%s\n" % (s, len(df), df["open_time"].min(), df["open_time"].max())).encode())
    return {"symbole": len(all_data), "zeilen": int(sum(len(_kurse(d)) for d in all_data.values())), "sha256_kurzbild": h.hexdigest(),
            "TB_SELEKTIONSWURZEL": os.environ.get("TB_SELEKTIONSWURZEL"), "TB_SELEKTIONSHASH": os.environ.get("TB_SELEKTIONSHASH")}


def simuliere_wie_main(es, trades, all_data) -> dict:
    """simulate_portfolio des Bots mit denselben Argumenten wie sein __main__ (Befund B1 des Gegenlesers):
    kursdaten = all_data per Keyword (elliott_wave kennt kein Limit), max_concurrent_positions = MAX_CONCURRENT_POSITIONS,
    wo die Signatur es hat. kursdaten_symbole 0 (Stufe 2/3 ruhen, zuteilung.py Z. 684-688) => Abbruch."""
    kw = {"kursdaten": all_data}
    if "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames:
        kw["max_concurrent_positions"] = es.MAX_CONCURRENT_POSITIONS
    erg = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, **kw)
    ks = (erg.get("zuteilung") or {}).get("kursdaten_symbole")
    if not ks:
        raise SystemExit("kursdaten_symbole %r - Stufe 2/3 der Zuteilungskaskade ruhen, Abbruch fuer diesen Bot" % (ks,))
    return erg


def positionen_rekonstruieren(bot, es, all_data, startkapital) -> dict:
    """F9 / R97 (b): ein Lauf mit unveraenderten Trades, Zuordnung aus Trade-Liste und equity_curve."""
    if sys.argv[1:2] != [bot]:
        raise SystemExit("bot_lauf.py liest den Bot aus sys.argv[1] - Aufruf: messung.py <bot>")
    sys.path.insert(0, os.path.join(REPO_ROOT, "research", "exposure_messung"))
    import bot_lauf as bl                               # noqa: E402  nur hole_trades; main() (Doppellauf) nie
    import rekonstruktion as rk                         # noqa: E402
    trades = bl.hole_trades(es, all_data)
    if trades is None or len(trades) == 0:
        raise SystemExit("%s: keine Trades" % bot)
    vorher = trades.copy(deep=True)
    hat_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    erg = simuliere_wie_main(es, trades, all_data)
    if not (trades.equals(vorher) and list(trades.columns) == list(vorher.columns)):
        raise SystemExit("%s: Trades nach dem Lauf veraendert - Abbruch (A9)" % bot)
    kurve = erg["equity_curve"]
    if len(kurve) != int(erg["num_executed"]):
        raise SystemExit("%s: equity_curve %d Zeilen, num_executed %d - Abbruch" % (bot, len(kurve), erg["num_executed"]))
    pos, rek = rk.zuordnen(trades, kurve, startkapital, float(es.ALLOCATION_PCT))
    rek.update({"trades_ausgefuehrt": int(erg["num_executed"]), "trades_uebersprungen": int(erg["num_skipped"]),
                "allocation_pct": float(es.ALLOCATION_PCT), "max_concurrent_positions": es.MAX_CONCURRENT_POSITIONS if hat_limit else None,
                "trades_unveraendert": True, "kursdaten_symbole": int(erg["zuteilung"]["kursdaten_symbole"]), "zuteilung": erg["zuteilung"],
                "final_capital": float(erg["final_capital"]), "num_executed": int(erg["num_executed"]), "num_skipped": int(erg["num_skipped"]),
                "aufruf": "simulate_portfolio argumentgleich mit dem __main__ des Bots (am Code geprueft); kein zweiter Bot-Lauf zum Abgleich"})
    os.makedirs(DATEN, exist_ok=True)
    pos.to_csv(os.path.join(DATEN, bot + "_positionen.csv"), index=False)
    with open(os.path.join(DATEN, bot + "_meta.json"), "w", encoding="utf-8") as f:
        json.dump(rek, f, indent=1, ensure_ascii=False, default=str)
    return rek


def ein_bot(bot: str) -> dict:
    t0 = time.time()
    mm = _mtm_messung()
    bot = mm.botenv.setup(bot)
    import equity_simulation as es                      # noqa: E402
    import multi_symbol_walk_forward as wf              # noqa: E402
    from messkette import max_drawdown_ungerundet       # noqa: E402
    import exposure_kern as ek                          # noqa: E402
    bt = importlib.import_module(mm.BACKTEST_MODUL[bot])
    mk, gl = mm.mtm_kern, mm.grundlage
    kosten_seite = float(bt.TRADING_FEE_PCT) + float(bt.SLIPPAGE_PCT)
    startkapital = float(es.STARTING_CAPITAL)

    all_data = wf.load_all_symbol_data()
    train, test = wf.split_all_symbols(all_data, wf.TRAIN_SPLIT_RATIO)
    grenzen = fenster.grenze_je_symbol(train, test)

    rek = positionen_rekonstruieren(bot, es, all_data, startkapital)
    if rek["nicht_zuordenbar"]:                         # F9: keine stille Luecke - Bot ohne E/M, als nicht vollstaendig zugeordnet
        aus = {"bot": bot, "status": "nicht vollstaendig zugeordnet", "rekonstruktion": rek, "abschnitte": [],
               "grenzen_streuung": fenster.streuung(grenzen), "datenbestand": datenbestand(all_data), "laufzeit_s": round(time.time() - t0, 1)}
        os.makedirs(ERGEBNISSE, exist_ok=True)
        with open(os.path.join(ERGEBNISSE, bot + ".json"), "w", encoding="utf-8") as f:
            json.dump(aus, f, indent=1, ensure_ascii=False, default=str)
        return aus
    gl.TB24_DIR = DATEN                                 # die eben rekonstruierte Liste dieses Laufs
    pos, meta, grund = gl.lade_positionen(bot)
    if pos is None:
        raise SystemExit("%s: keine Positionen - %s" % (bot, grund))
    ereignisse = mk.ereignisreihenfolge(pos, startkapital)
    kurve = mk.ereigniskurve(ereignisse)
    tages = gl.lade_schlusskurse(pos["symbol"].unique(), "1d")
    fehlend = sorted(set(pos["symbol"].unique()) - set(tages))
    if fehlend:
        raise SystemExit("%s: 1d-Kursdatei fehlt fuer %s" % (bot, fehlend))
    erste = min(fenster._ts(_kurse(d)["open_time"].min()) for d in all_data.values())
    letzte = max(fenster._ts(_kurse(d)["open_time"].max()) for d in all_data.values())
    von = min(erste.normalize(), ereignisse["entry_time"].min().normalize())
    bis = max(letzte.normalize(), ereignisse["exit_time"].max().normalize()) + mk.EIN_TAG
    ab = fenster.abschnitte(grenzen, von, bis)
    tage = mk.tagesraster(tages, von=von, bis=bis)
    kurse, fort = mk.kurse_auf_raster(tages, tage)
    pfad = mk.mtm_pfad(ereignisse, kurse, fort, startkapital, kosten_seite)
    zeilen = mk.messe_falten(kurve, pfad, ab, startkapital, max_drawdown_ungerundet)
    expo = mm.exposure_je_falte(pos, startkapital, ab, ek)
    for z, a in zip(zeilen, ab):
        z["von_genau"], z["bis_genau"] = str(a["von"]), str(a["bis_ausschliesslich"])
        z["exposure_mittel"] = expo.get(z["falte"])
    aus = {"bot": bot, "positionen": int(len(pos)), "erster_einstieg": str(pos["entry_time"].min()),
           "letzter_ausstieg": str(pos["exit_time"].max()), "startkapital": startkapital,
           "kosten_je_seite_pct": kosten_seite, "kosten_modul": mm.BACKTEST_MODUL[bot],
           "train_split_ratio": float(wf.TRAIN_SPLIT_RATIO), "grenzen_streuung": fenster.streuung(grenzen),
           "grenzen_je_symbol": {k: (str(v) if v is not None else None) for k, v in grenzen.items()},
           "datenbestand": datenbestand(all_data), "quelle_positionen": os.path.relpath(os.path.join(DATEN, bot + "_positionen.csv"), REPO_ROOT),
           "status": "vollstaendig zugeordnet", "rekonstruktion": rek,
           "abschnitte": zeilen,
           "M_flacher_als_E": [z["falte"] for z in zeilen if z["M_flacher_als_E"]],
           "laufzeit_s": round(time.time() - t0, 1)}
    os.makedirs(ERGEBNISSE, exist_ok=True)
    with open(os.path.join(ERGEBNISSE, bot + ".json"), "w", encoding="utf-8") as f:
        json.dump(aus, f, indent=1, ensure_ascii=False, default=str)
    return aus


def parameterdateien(bot):
    d = os.path.join(REPO_ROOT, "strategies", bot)
    return sorted([os.path.join(d, "live_params.py")] + glob.glob(os.path.join(d, "backtest_*.py")))


def sperrliste():
    muster = ["shared/messkette.py", "shared/zuteilung.py", "strategies/*/equity_simulation.py",
              "strategies/*/multi_symbol_optimise.py", "strategies/*/multi_symbol_walk_forward.py"]
    # herkunft.py Z. 102-106 (SPERRLISTE_DATEIEN); hier gelesen, nicht importiert - geprueft gegen die Datei:
    quelle = open(os.path.join(REPO_ROOT, "research", "vorregistrierung", "herkunft.py"), encoding="utf-8").read()
    if any('"%s"' % m not in quelle for m in muster):
        raise SystemExit("Sperrlisten-Muster weichen von herkunft.py ab")
    return {os.path.relpath(p, REPO_ROOT): sha256(p) for m in muster for p in sorted(glob.glob(os.path.join(REPO_ROOT, m)))}


def alle() -> int:
    os.makedirs(ERGEBNISSE, exist_ok=True)
    commit = subprocess.run(["git", "-C", REPO_ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    vorher = {"commit": commit, "parameterdateien": {b: {os.path.relpath(p, REPO_ROOT): sha256(p) for p in parameterdateien(b)} for b in BOTS},
              "sperrliste": sperrliste()}
    json.dump(vorher, open(os.path.join(ERGEBNISSE, "vorher.json"), "w", encoding="utf-8"), indent=1)
    lauf, t0 = {}, time.time()
    for b in BOTS:
        t = time.time()
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), b], capture_output=True, text=True)
        lauf[b] = {"rc": r.returncode, "s": round(time.time() - t, 1), "stderr_ende": r.stderr.strip().split("\n")[-3:]}
        print("%-28s rc %d  %.1f s" % (b, r.returncode, time.time() - t), flush=True)
    nachher = sperrliste()
    gleich = nachher == vorher["sperrliste"]
    zeilen = ["| Bot | Positionen (Rekonstruktion) | Abschnitt | von | bis (ausschl.) | Ausstiege | E % | M % | M−E pp | Exposure | Grenzen frueh/spaet (Spannweite Tage) | Datenbestand |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b in BOTS:
        p = os.path.join(ERGEBNISSE, b + ".json")
        if lauf[b]["rc"] or not os.path.exists(p):
            zeilen.append("| %s | – | – | – | – | – | – | – | – | – | Lauf rc %d | – |" % (b, lauf[b]["rc"])); continue
        e = json.load(open(p, encoding="utf-8")); s = e["grenzen_streuung"]; d = e["datenbestand"]; r = e["rekonstruktion"]
        zuo = "%d zugeordnet, %d nicht zuordenbar" % (r["zugeordnet"], r["nicht_zuordenbar"])
        if r["nicht_zuordenbar"]:
            zeilen.append("| %s | nicht vollstaendig zugeordnet: %s | – | – | – | – | – | – | – | – | %s / %s (%s) | %d Symbole, %s |" % (
                b, zuo, s["frueheste"], s["spaeteste"], s["spannweite_tage"], d["symbole"], d["sha256_kurzbild"][:12])); continue
        for z in e["abschnitte"]:
            zeilen.append("| %s | %s | %s | %s | %s | %d | %s | %s | %s | %s | %s / %s (%s) | %d Symbole, %s |" % (
                b, zuo, z["falte"], z["von_genau"], z["bis_genau"], z["n_ausstiege"], z["E"], z["M"], z["M_minus_E_pp"], z["exposure_mittel"],
                s["frueheste"], s["spaeteste"], s["spannweite_tage"], d["symbole"], d["sha256_kurzbild"][:12]))
    kopf = ("Kapital-Drawdown E und M der heutigen Parameter je Abschnitt des bot-eigenen Walk-Forward (TB-162). Bericht, kein Tor: "
            "die Zahl entscheidet nichts (24.3); kein Raster, kein Score, keine Rangfolge (R94). Commit %s. Sperrliste vorher = nachher: %s. Positionen: Rekonstruktion nach R97 (b) (kein Nachweis, R95 (b)); Regel: %s." % (commit[:7], gleich, REGEL))
    open(os.path.join(ERGEBNISSE, "tabelle.md"), "w", encoding="utf-8").write(kopf + "\n\n" + "\n".join(zeilen) + "\n")
    json.dump({"lauf": lauf, "sperrliste_gleich": gleich, "laufzeit_s": round(time.time() - t0, 1), "python": sys.version.split()[0]},
              open(os.path.join(ERGEBNISSE, "laufprotokoll.json"), "w", encoding="utf-8"), indent=1)
    ok = gleich and all(v["rc"] == 0 for v in lauf.values())
    print("Sperrliste vorher = nachher: %s; Bots rc 0: %d von %d; Laufzeit %.1f s" % (gleich, sum(v["rc"] == 0 for v in lauf.values()), len(BOTS), time.time() - t0))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--alle"]:
        sys.exit(alle())
    if len(sys.argv) != 2 or sys.argv[1] not in BOTS:
        raise SystemExit("Aufruf: messung.py <bot> | --alle")
    a = ein_bot(sys.argv[1])
    print("%s: %s, %d nicht zuordenbar, %d Abschnitte, %.1f s" % (a["bot"], a["status"], a["rekonstruktion"]["nicht_zuordenbar"], len(a["abschnitte"]), a["laufzeit_s"]))
```

### research/wf_kapital_dd/rekonstruktion.py

```python
#!/usr/bin/env python3
"""
TB-162 - Rekonstruktion der ausgefuehrten Positionen aus Trade-Liste und equity_curve
==============================================================================
Entscheid F9, Register R97 (b) zweiter Satz (Fable 14.10.b): ein Lauf mit
UNVERAENDERTEN Trades (kein Feld beschrieben, auch nicht im Speicher; A9, 41.1),
die Zuordnung aus Trade-Liste und equity_curve. Das ist eine REKONSTRUKTION,
kein Nachweis, keine Probe, keine Definition (R95 (b), (c)).
positionen_holen.py (Doppellauf, verstoesst gegen A9, R97 (a)) wird weder
ausgefuehrt noch eingebunden.

Zuordnungsregel (je Zeile der equity_curve, in ihrer Reihenfolge):
  Z1 Kandidaten: noch nicht zugeordnete Trade-Zeilen mit gleichem Symbol (als Text),
     gleichem Ausstiegszeitpunkt (exit_time = time, in UTC) und gleichem pnl_pct
     (Abweichung <= TOL_PNL).
  Z2 Mehr als ein Kandidat: Kapitalprobe - allocation der Kurvenzeile gegen
     allocation_pct x Kapital beim Einstieg (capital_after der letzten Kurvenzeile
     mit time <= entry_time, sonst Startkapital); Abweichung <= TOL_GELD.
  Z3 Bleiben mehrere, die in symbol, entry_time, exit_time, entry_price,
     exit_price und pnl_pct gleich sind: die mit der kleinsten Zeilennummer
     (inhaltsgleich; gezaehlt).
  Z4 Sonst (kein Kandidat, oder mehrere verschiedene): NICHT ZUORDENBAR - gezaehlt
     und mit Kurvenzeile gemeldet; die Position fehlt in der Liste.
Toleranz: TOL_PNL = 1e-9 Prozentpunkte (die Kurve traegt den pnl_pct der Trade-
Zeile); TOL_GELD = 0.01 (allocation und capital_after sind auf 2 Stellen gerundet).
Ausgabe in der Buchungsreihenfolge der equity_curve (Spalte kurvenzeile).
Reine Funktionen; die Trade-Liste wird nur gelesen.
"""
import numpy as np
import pandas as pd

TOL_PNL = 1e-9
TOL_GELD = 0.01
REGEL = ("Z1 gleiches Symbol, exit_time = time (UTC), |pnl_pct-Diff| <= %g; Z2 bei mehreren: Kapitalprobe "
         "|allocation - allocation_pct x Kapital beim Einstieg| <= %g; Z3 inhaltsgleiche Kandidaten: kleinste Zeile; "
         "Z4 sonst nicht zuordenbar (gemeldet)" % (TOL_PNL, TOL_GELD))
_INHALT = ("symbol", "entry_time", "exit_time", "entry_price", "exit_price", "pnl_pct")
_NULL = pd.Timestamp("1970-01-01", tz="UTC")


def ns_utc(werte) -> np.ndarray:
    """Zeitpunkte als ganze Nanosekunden seit 1970 (UTC); naive Werte gelten als UTC."""
    t = pd.Series(pd.to_datetime(pd.Series(list(werte)), utc=True))
    return ((t - _NULL) // pd.Timedelta(1, "ns")).to_numpy(dtype="int64")


def zuordnen(trades: pd.DataFrame, kurve: pd.DataFrame, startkapital: float, allocation_pct: float):
    """-> (positionen, bericht). positionen: neue Tabelle (trade_zeile = Position in trades)."""
    n = len(trades)
    sym = trades["symbol"].astype(str).to_numpy()
    ein = ns_utc(trades["entry_time"]) if n else np.zeros(0, "int64")
    aus = ns_utc(trades["exit_time"]) if n else np.zeros(0, "int64")
    pnl = trades["pnl_pct"].astype(float).to_numpy()
    nach_schluessel = {}
    for i in range(n):
        nach_schluessel.setdefault((sym[i], int(aus[i])), []).append(i)
    k_sym = kurve["symbol"].astype(str).to_numpy() if len(kurve) else np.zeros(0, object)
    k_zeit = ns_utc(kurve["time"]) if len(kurve) else np.zeros(0, "int64")
    k_pnl = kurve["pnl_pct"].astype(float).to_numpy() if len(kurve) else np.zeros(0)
    k_alloc = kurve["allocation"].astype(float).to_numpy() if len(kurve) else np.zeros(0)
    k_kap = kurve["capital_after"].astype(float).to_numpy() if len(kurve) else np.zeros(0)

    def kapital_beim_einstieg(t):
        j = int(np.searchsorted(k_zeit, t, side="right")) - 1
        return float(startkapital) if j < 0 else float(k_kap[j])

    def inhalt(i):
        return tuple(str(trades[s].iloc[i]) if s in trades.columns else None for s in _INHALT)

    benutzt, paare, fehl = set(), [], []
    zaehl = {"eindeutig": 0, "durch_kapitalprobe": 0, "inhaltsgleich": 0}
    for k in range(len(kurve)):
        kand = [i for i in nach_schluessel.get((str(k_sym[k]), int(k_zeit[k])), ())
                if i not in benutzt and abs(pnl[i] - k_pnl[k]) <= TOL_PNL]
        art = "eindeutig"
        if len(kand) > 1:
            kand = [i for i in kand if abs(k_alloc[k] - allocation_pct * kapital_beim_einstieg(ein[i])) <= TOL_GELD]
            art = "durch_kapitalprobe"
        if len(kand) > 1 and len(set(inhalt(i) for i in kand)) == 1:
            kand = [min(kand)]
            art = "inhaltsgleich"
        if len(kand) != 1:
            fehl.append({"kurvenzeile": k, "symbol": str(k_sym[k]), "time": str(pd.Timestamp(int(k_zeit[k]), tz="UTC")),
                         "kandidaten": len(kand)})
            continue
        benutzt.add(kand[0]); paare.append((k, kand[0])); zaehl[art] += 1

    spalten = [s for s in ("symbol", "entry_time", "exit_time", "result", "pnl_pct", "entry_price", "exit_price")
               if s in trades.columns]
    zeilen = [i for _, i in paare]
    pos = trades.iloc[zeilen][spalten].copy().reset_index(drop=True)
    pos.insert(0, "trade_zeile", zeilen)
    pos["allocation"] = [float(k_alloc[k]) for k, _ in paare]
    pos["capital_after"] = [float(k_kap[k]) for k, _ in paare]
    pos["kurvenzeile"] = [k for k, _ in paare]
    # Reihenfolge = Buchungsreihenfolge der Simulation (kurvenzeile). Nach entry_time sortiert waehlt
    # mtm_kern.ereignisreihenfolge bei Gleichstand im Ausstieg mit Nullschritt (pnl_pct 0) die falsche
    # Zeile und die Kette schliesst nicht (Befund TB-162 Bau, rsi2_mean_reversion an der Kopie).
    bericht = {"art": "Rekonstruktion", "regel": REGEL, "toleranz": {"pnl_pct": TOL_PNL, "geld": TOL_GELD},
               "trades_gefunden": n, "kurvenzeilen": int(len(kurve)), "zugeordnet": len(paare),
               "nicht_zuordenbar": len(fehl), "nicht_zuordenbar_zeilen": fehl[:50], **zaehl}
    return pos, bericht
```

### research/wf_kapital_dd/test_fenster.py

```python
#!/usr/bin/env python3
"""
TB-162 - Proben fuer fenster.py an synthetischen Daten (Entscheid F4; Bauart R46: keine Zahl der Kursdaten der Bots)
  F1 zeitbasierte Rueckgabe -> Grenze je Symbol        F2 zeilenbasierte Rueckgabe -> open_time der Zeile k
  F3 widerspruechliche Grenze bricht ab                F4 Abschnitte lueckenlos, ausserhalb des Pfads bricht ab
  F5 Streuung (Spannweite, ohne Grenze)                P1 durchgehender Pfad: Basis des Abschnitts = Stand davor (kein Neustart)
  P2 Intraday-Positionen: E = M in jedem Abschnitt     P3 Handposition ueber die Grenze: M zeigt den Zwischenverlust, E nicht
"""
import os, sys, time
import numpy as np
import pandas as pd
_HIER = os.path.dirname(os.path.abspath(__file__)); REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER); sys.path.insert(0, os.path.join(REPO_ROOT, "research", "mtm_drawdown")); sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))
import fenster          # noqa: E402
import mtm_kern         # noqa: E402
from messkette import max_drawdown_ungerundet   # noqa: E402
BEFUNDE = []
def pruefe(ok, text):
    BEFUNDE.append(bool(ok)); print(("ok    " if ok else "FEHL  ") + text)
def kurse(von, n, freq="D"):
    t = pd.date_range(von, periods=n, freq=freq); return pd.DataFrame({"open_time": t, "close": np.linspace(100, 120, n)})
def f_tests():
    a, b = kurse("2020-01-01", 101), kurse("2021-01-01", 11)
    st = {}
    for s, df in (("A", a), ("B", b)):
        w0, w1 = df["open_time"].min(), df["open_time"].max(); st[s] = w0 + (w1 - w0) * 0.7
    train = {s: (df, None, st[s]) for s, df in (("A", a), ("B", b))}; test = {s: (df, st[s], None) for s, df in (("A", a), ("B", b))}
    g = fenster.grenze_je_symbol(train, test)
    pruefe(g == {"A": pd.Timestamp("2020-03-11"), "B": pd.Timestamp("2021-01-08")}, "F1 zeitbasiert: Grenze je Symbol = split_time %s" % g)
    k = int(len(a) * 0.7); g2 = fenster.grenze_je_symbol({"A": a.iloc[:k]}, {"A": a.iloc[k:].reset_index(drop=True), "C": a.iloc[0:0]})
    pruefe(g2 == {"A": a["open_time"].iloc[k], "C": None}, "F2 zeilenbasiert: Grenze = open_time der Zeile %d, leerer OOS-Teil = None" % k)
    try:
        fenster.grenze_je_symbol({"A": (a, None, st["A"])}, {"A": (a, st["A"] + pd.Timedelta(days=1), None)}); pruefe(False, "F3 widerspruechliche Grenze bricht ab")
    except ValueError:
        pruefe(True, "F3 widerspruechliche Grenze bricht ab (ValueError)")
    ab = fenster.abschnitte(g, "2020-01-01", "2021-01-12")
    lueckenlos = all(ab[i]["bis_ausschliesslich"] == ab[i + 1]["von"] for i in (1, 2)) and ab[1]["von"] == ab[0]["von"] and ab[3]["bis_ausschliesslich"] == ab[0]["bis_ausschliesslich"]
    pruefe([x["name"] for x in ab] == list(fenster.ABSCHNITTE) and lueckenlos, "F4 Abschnitte gesamt/IS/gemischt/OOS lueckenlos")
    try:
        fenster.abschnitte(g, "2020-06-01", "2021-01-12"); pruefe(False, "F4 Grenze vor dem Pfadbeginn bricht ab")
    except ValueError:
        pruefe(True, "F4 Grenze vor dem Pfadbeginn bricht ab (ValueError)")
    s = fenster.streuung(dict(g, C=None))
    pruefe(s["spannweite_tage"] == 303.0 and s["symbole_ohne_grenze"] == ["C"] and s["symbole"] == 3, "F5 Streuung: Spannweite %s Tage, ohne Grenze %s" % (s["spannweite_tage"], s["symbole_ohne_grenze"]))
def pfad(pos, tage, schluss, kosten=0.0):
    e = mtm_kern.ereignisreihenfolge(pos, 10000.0); k = mtm_kern.ereigniskurve(e)
    ks, f = mtm_kern.kurse_auf_raster({"X": pd.Series(schluss, index=tage)}, tage)
    return k, mtm_kern.mtm_pfad(e, ks, f, 10000.0, kosten)
def p_tests():
    tage = pd.date_range("2020-01-01", periods=10, freq="D")
    schluss = [100, 100, 90, 80, 95, 105, 105, 105, 105, 105]
    pos = pd.DataFrame({"symbol": ["X"], "entry_time": [tage[1]], "exit_time": [tage[5]], "entry_price": [100.0], "exit_price": [105.0],
                        "allocation": [2000.0], "pnl_pct": [5.0], "capital_after": [10100.0]})
    k, p = pfad(pos, tage, schluss)
    ab = fenster.abschnitte({"X": tage[3]}, tage[0], tage[-1] + pd.Timedelta(days=1))
    m = {z["falte"]: z for z in mtm_kern.messe_falten(k, p, ab, 10000.0, max_drawdown_ungerundet)}
    pruefe(abs(m["OOS"]["basis_M"] - float(p["mtm"].iloc[2])) < 1e-9 and m["OOS"]["basis_M"] != 10000.0,
           "P1 kein Neustart: Basis M des OOS = Stand am Vortag der Grenze (%s), nicht das Startkapital" % m["OOS"]["basis_M"])
    pruefe(m["gesamt"]["E"] == 0.0 and m["gesamt"]["M"] < 0 and m["IS"]["M"] < 0, "P3 Handposition ueber die Grenze: E %s, M gesamt %s, M IS %s" % (m["gesamt"]["E"], m["gesamt"]["M"], m["IS"]["M"]))
    rows = []; kap = 10000.0
    for i, (r, d) in enumerate(zip([2.0, -3.0, 1.5, -4.0, 2.5], tage[1:6])):
        kap += 1000.0 * r / 100; rows.append({"symbol": "X", "entry_time": d, "exit_time": d + pd.Timedelta(hours=1), "entry_price": 100.0,
                                             "exit_price": 100.0 * (1 + r / 100), "allocation": 1000.0, "pnl_pct": r, "capital_after": kap})
    k, p = pfad(pd.DataFrame(rows), tage, [100.0] * 10)
    m2 = mtm_kern.messe_falten(k, p, ab, 10000.0, max_drawdown_ungerundet)
    pruefe(all(z["E"] == z["M"] for z in m2), "P2 Intraday: E = M in allen %d Abschnitten %s" % (len(m2), [(z["falte"], z["E"], z["M"]) for z in m2]))
def main():
    t0 = time.time(); f_tests(); p_tests(); n, ok = len(BEFUNDE), sum(BEFUNDE)
    print("%d von %d Pruefungen bestanden, %d gescheitert, Laufzeit %.1f s" % (ok, n, n - ok, time.time() - t0))
    return 0 if ok == n else 1
if __name__ == "__main__":
    sys.exit(main())
```

### research/wf_kapital_dd/test_rekonstruktion.py

```python
#!/usr/bin/env python3
"""
TB-162 - Proben fuer rekonstruktion.py an synthetischen Daten (Entscheid F9; R97 (b); keine Zahl der Kursdaten der Bots)
  R1 eindeutige Trades: alle Kurvenzeilen zugeordnet, Kapitalkette schliesst   R2 gleicher Schluessel, Kapitalprobe trennt
  R3 inhaltsgleiche Zeilen: kleinste Zeile, gezaehlt                          R4 NICHT ZUORDENBAR: zwei verschiedene Kandidaten, gleiches Kapital
  R5 Kurvenzeile ohne Kandidat: nicht zuordenbar, gemeldet                    R6 Zeitzone: tz-behaftete Trades gegen naive Kurve
  R7 der Lauf (simuliere_portfolio) laesst die Trades unveraendert            R8 Quelle: kein Schreibzugriff auf Trades, kein positionen_holen
  R9 Nullschritt im Gleichstand: Liste in Kurvenreihenfolge, die Kette von mtm_kern schliesst
  R10 messung.simuliere_wie_main: kursdaten per Keyword, Limit nur wo die Signatur es hat, kursdaten_symbole 0 bricht ab
"""
import os, re, sys, time
import pandas as pd
_HIER = os.path.dirname(os.path.abspath(__file__)); REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER); sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))
import rekonstruktion as rk   # noqa: E402
import zuteilung              # noqa: E402
sys.path.insert(0, os.path.join(REPO_ROOT, "research", "mtm_drawdown"))
import mtm_kern               # noqa: E402
BEFUNDE = []
def pruefe(ok, text):
    BEFUNDE.append(bool(ok)); print(("ok    " if ok else "FEHL  ") + text)
T = pd.Timestamp
def tr(rows):
    return pd.DataFrame([{"symbol": s, "entry_time": e, "exit_time": x, "entry_price": ep, "exit_price": ep * (1 + p / 100), "pnl_pct": p}
                         for s, e, x, ep, p in rows])
def lauf(trades, pct=0.1, limit=None):
    vorher = trades.copy(deep=True)
    e = zuteilung.simuliere_portfolio(trades, 10000.0, pct, limit)
    return e, trades.equals(vorher) and list(trades.columns) == list(vorher.columns)
def kette(pos, start=10000.0):
    p = pos.sort_values("kurvenzeile"); kap = start
    for a, r, c in zip(p["allocation"], p["pnl_pct"], p["capital_after"]):
        kap += a * r / 100
        if abs(kap - c) > rk.TOL_GELD: return False
    return True
def main():
    t0 = time.time()
    t1 = tr([("A", T("2021-01-01"), T("2021-01-05"), 10.0, 2.0), ("B", T("2021-01-02"), T("2021-01-04"), 20.0, -1.0),
             ("C", T("2021-01-03"), T("2021-01-09"), 30.0, 3.0), ("A", T("2021-01-06"), T("2021-01-08"), 11.0, 1.5)])
    e, unv = lauf(t1); pos, b = rk.zuordnen(t1, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["zugeordnet"] == e["num_executed"] == 4 and b["nicht_zuordenbar"] == 0 and b["eindeutig"] == 4 and kette(pos)
           and sorted(pos["trade_zeile"]) == [0, 1, 2, 3] and list(pos["kurvenzeile"]) == [0, 1, 2, 3], "R1 eindeutig: %d von %d zugeordnet, Kette schliesst" % (b["zugeordnet"], b["kurvenzeilen"]))
    t2 = tr([("X", T("2021-01-01"), T("2021-01-10"), 10.0, 5.0), ("Y", T("2021-01-02"), T("2021-01-03"), 10.0, 20.0),
             ("X", T("2021-01-04"), T("2021-01-10"), 10.0, 5.0)])
    e, unv = lauf(t2); pos, b = rk.zuordnen(t2, e["equity_curve"], 10000.0, 0.1)
    xa = dict(zip(pos["trade_zeile"], pos["allocation"]))
    pruefe(b["nicht_zuordenbar"] == 0 and b["durch_kapitalprobe"] >= 1 and xa.get(0) == 1000.0 and xa.get(2) == 1020.0 and kette(pos),
           "R2 Kapitalprobe trennt gleichen Schluessel (Einstieg vor/nach Gewinn Y): allocation je Zeile %s, %s" % (xa, {k: b[k] for k in ("eindeutig", "durch_kapitalprobe", "inhaltsgleich")}))
    t3 = tr([("X", T("2021-01-01"), T("2021-01-05"), 10.0, 1.0), ("X", T("2021-01-01"), T("2021-01-05"), 10.0, 1.0)])
    e, unv = lauf(t3); pos, b = rk.zuordnen(t3, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["nicht_zuordenbar"] == 0 and b["inhaltsgleich"] >= 1 and sorted(pos["trade_zeile"]) == [0, 1],
           "R3 inhaltsgleich: %d gezaehlt, Zeilen %s" % (b["inhaltsgleich"], sorted(pos["trade_zeile"])))
    t4 = tr([("X", T("2021-01-01"), T("2021-01-10"), 10.0, 4.0), ("X", T("2021-01-03"), T("2021-01-10"), 10.0, 4.0)])
    t4.loc[1, "entry_price"] = 10.5
    e, unv = lauf(t4, pct=0.6); pos, b = rk.zuordnen(t4, e["equity_curve"], 10000.0, 0.6)
    pruefe(e["num_executed"] == 1 and b["nicht_zuordenbar"] == 1 and len(pos) == 0 and b["nicht_zuordenbar_zeilen"][0]["kandidaten"] == 2,
           "R4 NICHT ZUORDENBAR gemeldet: %s" % b["nicht_zuordenbar_zeilen"])
    k5 = pd.DataFrame([{"time": T("2021-02-01"), "symbol": "Z", "pnl_pct": 1.0, "allocation": 1000.0, "capital_after": 10010.0}])
    pos, b = rk.zuordnen(t1, k5, 10000.0, 0.1)
    pruefe(b["nicht_zuordenbar"] == 1 and b["nicht_zuordenbar_zeilen"][0]["kandidaten"] == 0, "R5 Kurvenzeile ohne Kandidat gemeldet")
    t6 = t1.copy(); t6["entry_time"] = [str(x.tz_localize("UTC").tz_convert("Europe/Berlin")) for x in t1["entry_time"]]
    t6["exit_time"] = [str(x.tz_localize("UTC").tz_convert("Europe/Berlin")) for x in t1["exit_time"]]
    e, _ = lauf(t1); pos, b = rk.zuordnen(t6, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["zugeordnet"] == 4 and b["nicht_zuordenbar"] == 0, "R6 Zeitzone: Berlin-Text gegen naive UTC-Kurve, %d zugeordnet" % b["zugeordnet"])
    alle = all(lauf(t)[1] for t in (t1, t2, t3, t4))
    vor = t2.copy(deep=True); rk.zuordnen(t2, lauf(t2)[0]["equity_curve"], 10000.0, 0.1)
    pruefe(alle and t2.equals(vor), "R7 Lauf und Zuordnung lassen die Trades unveraendert (DataFrame.equals)")
    schreib = re.compile(r"trades(\[[^\]]*\]|\.(loc|iloc|at|iat)\[[^\]]*\])\s*=[^=]|trades\.(insert|pop|drop|sort_values|set_index|rename)\([^)]*inplace|positionen_holen\.py[\x22\x27]|(import|from)\s+positionen_holen|spec_from_file_location\([^)]*positionen_holen")
    quellen = [os.path.join(_HIER, f) for f in ("rekonstruktion.py", "messung.py") if os.path.exists(os.path.join(_HIER, f))]
    treffer = [(os.path.basename(q), z) for q in quellen for z in open(q, encoding="utf-8").read().split("\n") if schreib.search(z)]
    pruefe(len(quellen) == 2 and not treffer, "R8 Quellen ohne Schreibzugriff auf Trades und ohne positionen_holen: %s" % (treffer or "keiner"))
    t9 = tr([("P", T("2021-01-03"), T("2021-01-11"), 10.0, 0.0), ("B", T("2021-01-01"), T("2021-01-11"), 10.0, -3.55),
             ("C", T("2021-01-01"), T("2021-01-11"), 10.0, -2.5), ("D", T("2021-01-02"), T("2021-01-05"), 10.0, 1.0)])
    e, _ = lauf(t9); pos, b = rk.zuordnen(t9, e["equity_curve"], 10000.0, 0.1)
    try:
        r = mtm_kern.ereignisreihenfolge(pos, 10000.0); ok9 = list(r["kurvenzeile"]) == sorted(pos["kurvenzeile"])
    except ValueError as x:
        ok9 = False
    pruefe(ok9 and b["nicht_zuordenbar"] == 0, "R9 Nullschritt im Gleichstand: mtm_kern.ereignisreihenfolge folgt der Kurvenreihenfolge")
    import importlib.util, types
    spec = importlib.util.spec_from_file_location("wf_messung", os.path.join(_HIER, "messung.py"))   # nicht research/mtm_drawdown/messung.py
    messung = importlib.util.module_from_spec(spec); spec.loader.exec_module(messung)
    ruf = []
    def sp_ohne(trades, starting_capital, allocation_pct, kursdaten=None, signalspalte=None):
        ruf.append(("ohne", kursdaten is not None)); return zuteilung.simuliere_portfolio(trades, starting_capital, allocation_pct, None, kursdaten)
    def sp_mit(trades, starting_capital, allocation_pct, max_concurrent_positions=None, kursdaten=None, signalspalte=None):
        ruf.append(("mit", max_concurrent_positions, kursdaten is not None)); return zuteilung.simuliere_portfolio(trades, starting_capital, allocation_pct, max_concurrent_positions, kursdaten)
    kd = {s: pd.DataFrame({"open_time": pd.date_range("2020-12-01", periods=60, freq="D"), "close": [100.0 + i for i in range(60)],
                           "volume": [1000.0] * 60}) for s in ("A", "B", "C")}
    es1 = types.SimpleNamespace(simulate_portfolio=sp_ohne, STARTING_CAPITAL=10000.0, ALLOCATION_PCT=0.1)
    es2 = types.SimpleNamespace(simulate_portfolio=sp_mit, STARTING_CAPITAL=10000.0, ALLOCATION_PCT=0.1, MAX_CONCURRENT_POSITIONS=3)
    e1 = messung.simuliere_wie_main(es1, t1, kd); e2 = messung.simuliere_wie_main(es2, t1, kd)
    try:
        messung.simuliere_wie_main(es1, t1, {}); abbr = False
    except SystemExit:
        abbr = True
    pruefe(ruf[:2] == [("ohne", True), ("mit", 3, True)] and e1["zuteilung"]["kursdaten_symbole"] > 0 and e2["zuteilung"]["kursdaten_symbole"] > 0 and abbr,
           "R10 wie __main__: Aufrufe %s, kursdaten_symbole %s/%s, ohne Kursdaten Abbruch: %s" % (ruf[:2], e1["zuteilung"]["kursdaten_symbole"], e2["zuteilung"]["kursdaten_symbole"], abbr))
    n, ok = len(BEFUNDE), sum(BEFUNDE)
    print("%d von %d Pruefungen bestanden, %d gescheitert, Laufzeit %.1f s" % (ok, n, n - ok, time.time() - t0))
    return 0 if ok == n else 1
if __name__ == "__main__":
    sys.exit(main())
```

## Anhang B — Werkzeug

### Werkzeug

```python
#!/usr/bin/env python3
"""TB-162 Werkzeug (Anhang B): Voraussetzungen F5/F11, Register 58 (R94-R97) mit Marken (R96 (d), R97 (e)), Index-Eintraege, Handfelder, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                         F5/F11: Voraussetzungen aus R94-R97 messen (rc 0 = alle ja)
  register <DATUM> <S0> <BELEG> [--probe]  Abschnitt 58 (R94-R96 aus 14a, R97 aus 14b zeichengleich) und 8 Marken
  index <S0> <DATUM> [--probe]          REGISTER_INDEX.md: Kopf, Tabelle 4, Zeile 58, Abschnitt 13, Pflege (nach c2_index_zeilen.py)
  handfelder <ZIEL>                     Handfelder 14a fuer dialog_index.py
  kennung | journal <BLOCK> [--probe]   naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, subprocess, sys
REG, IDX, JO = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md"
FA = "docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md"
DREI = [FA, "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md"]
FB = "docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md"
SECHS = DREI + [FB, "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md"]
FA_MD5, FB_MD5 = "c33799567a0205f66c502dbf5aaff5c5", "4b02ae62279294f5b1df4b1472cc2435"
KOPF_A, KOPF_B = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R94)", "## Registerblock — zeichengleich kopierbar, nummeriert (ab R97)"
TITEL58 = "## 58. Fable 14a und 14b — Registerblock R94–R97 (TB-162)"
# (Ort, Bereich-Anfang, Wort, R, Unterabschnitt, Fable, Unterpunkte) - R96 (d) (14a) und R97 (e) (14b); je Ort in dieser Reihenfolge
MARKEN = [("Abschnitt 27", "## 27. ", "ERGÄNZT", "R94", "58.1", "14a", "Unterpunkte (a) und (b) (zu 27.2)"),
          ("Abschnitt 27", "## 27. ", "ERGÄNZT", "R97", "58.4", "14b", "Unterpunkt (b) (zu R94 (b) und 27.2)"),
          ("48.13 R45", "### 48.13 ", "PRÄZISIERT", "R95", "58.2", "14a", "Unterpunkte (a) und (b)"),
          ("48.13 R45", "### 48.13 ", "ERGÄNZT", "R97", "58.4", "14b", "Unterpunkt (b)"),
          ("48.14 R46", "### 48.14 ", "ERGÄNZT", "R94", "58.1", "14a", "Unterpunkte (a) und (b)"),
          ("56.1 R84", "### 56.1 ", "PRÄZISIERT", "R95", "58.2", "14a", "Unterpunkte (a) und (b)")]
# Marken in 58 selbst (R97 (e)): an R95 (58.2) und R96 (58.3), nach der Quellenzeile
MARKEN58 = [("58.2 R95", 1, "BERICHTIGT", "R97", "58.4", "14b", "Unterpunkt (a)"), ("58.3 R96", 2, "BERICHTIGT", "R97", "58.4", "14b", "Unterpunkt (d)")]
ZEICHENGLEICH = "> Eintrag und Stand oben bleiben zeichengleich."
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
def gitrc(*a): r = subprocess.run(["git"] + list(a), capture_output=True, text=True); return r.returncode, r.stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def abschnitt(txt, n):
    z = txt.split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## %d. " % n)]
    if len(a) != 1: return None
    e = next((i for i in range(a[0] + 1, len(z)) if re.match(r"## \d+\. ", z[i])), len(z)); return "\n".join(z[a[0]:e])
def bloecke_aus(datei, kopf, rr):
    z = lies(datei).split("\n"); a = z.index(kopf) + 1
    while z[a] == "": a += 1
    assert z[a] == "```"; e = z.index("```", a + 1); b = [l for l in z[a + 1:e] if l]
    soll = [x for r in rr for x in (r + " — ", "Quelle")]
    assert [l[:6] for l in b] == soll, [l[:6] for l in b]
    return [(b[i], b[i + 1], a + 2 + z[a + 1:e].index(b[i])) for i in range(0, len(b), 2)]
def bloecke():
    """[(R-Zeile, Quellenzeile, Zeile in der Fable-Datei, Datei)] fuer R94, R95, R96 (14a) und R97 (14b)."""
    return [x + (FA,) for x in bloecke_aus(FA, KOPF_A, ("R94", "R95", "R96"))] + [x + (FB,) for x in bloecke_aus(FB, KOPF_B, ("R97",))]
def voraussetzung():
    hk = lies("research/vorregistrierung/herkunft.py").split("\n")[101:106]
    for m in ("shared/messkette.py", "shared/zuteilung.py", "strategies/*/equity_simulation.py", "strategies/*/multi_symbol_optimise.py", "strategies/*/multi_symbol_walk_forward.py"):
        p(any('"%s"' % m in l for l in hk), "R94: Sperrliste herkunft.py Z. 102-106 nennt %s" % m)
    p(len(git("ls-files", "strategies/*/multi_symbol_walk_forward.py").split()) == 9, "R94: neun Walk-Forward-Rechner verfolgt (die sechs Rechner und drei Erben)")
    A, D = git("show", "3f2e97e:" + REG), git("show", "d950e03:" + REG)
    for n in (9, 11, 24, 37, 41, 51, 54):
        x, y = abschnitt(A, n), abschnitt(D, n); p(x is not None and x == y, "R94/R96 (b)/R97 (f): Abschnitt %d am Stand 3f2e97e zeichengleich mit d950e03" % n)
    rc, aus = gitrc("log", "--format=%h", "3f2e97e..HEAD", "--", REG); p(rc == 0 and aus.strip() == "", "Register seit 3f2e97e unveraendert")
    for f in ("research/tb24_haltedauern/positionen_holen.py", "shared/zuteilung.py"):
        rc, aus = gitrc("log", "--format=%h", "7b9f9ac..HEAD", "--", f); rc2, aus2 = gitrc("diff", "--name-only", "HEAD", "--", f)
        p(rc == 0 and rc2 == 0 and aus.strip() == "" and aus2.strip() == "", "F11 (3)/R97 (f): %s am HEAD unveraendert gegen 7b9f9ac (Verhalten nach der Wiedergabe in 14.10.b)" % f)
    for f in SECHS:
        p(bool(git("ls-files", "--error-unmatch", f).strip()) and git("diff", "--name-only", "HEAD", "--", f).strip() == "", "F11 (1)/R56 (b): %s verfolgt, gleich HEAD" % f)
    p(md5(lies(FA)) == FA_MD5, "Fable-Datei 14.10.a md5 %s" % FA_MD5); p(md5(lies(FB)) == FB_MD5, "Fable-Datei 14.10.b md5 %s" % FB_MD5)
    reg = lies(REG); p(not re.search(r"^## 58\. ", reg, re.M) and not re.search(r"\bR9[4567]\b", reg), "R94-R97 und Abschnitt 58 noch nicht im Register")
    ende()
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    z = lies(REG).split("\n"); bl = bloecke(); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1] == "Pruefungen: %d, NEIN: 0" % sum(1 for l in vb if l.startswith(("ja ", "NEIN"))), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    einf = []
    for ort, anfang, wort, rr, ua, fb, up in MARKEN:
        a = [i for i, l in enumerate(z) if l.startswith(anfang)]
        if not p(len(a) == 1, "Ort %s (%s): Anfang genau einmal" % (ort, rr)): continue
        tief = "## " if anfang.startswith("## ") else "### "
        e = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or (tief == "### " and z[i].startswith("### ")))
        zg = [i for i in range(a[0], e) if z[i] == ZEICHENGLEICH]
        p(bool(zg) and not any(rr in z[i] for i in range(a[0], e)), "Ort %s: letzte Marke Z. %s, %s dort noch nicht genannt" % (ort, zg[-1] + 1 if zg else "?", rr))
        if zg: einf.append((zg[-1] + 1, ["", "> ⭐ **%s %s durch %s (%s)** (Fable %s %s, %s, TB-162, %s)." % (ort, wort, rr, ua, fb, rr, up, datum), ZEICHENGLEICH]))
    titel = []
    for zeile, _, _, _ in bl:
        t = zeile.split(". (a) ")[0] if ". (a) " in zeile else zeile.split(" (a) ")[0]; t = t[:-1] if t.endswith(".") else t
        if len(t) > 140: t = t[:139].rsplit(" ", 1)[0] + "…"
        titel.append(t)
    kette = ["**Kette:** Marken: Abschnitt 27; 48.14 (R46). Indexzeilen ohne Marke (R96 (d)): 48.20 (R52); 54.3 (R76). Zu (b): R97 (b) (58.4); R94 bleibt unverändert (R97 (c)).",
             "**Kette:** Marken: 48.13 (R45); 56.1 (R84). Unterpunkt (a) BERICHTIGT durch R97 (a) (58.4).",
             "**Kette:** Marken: keine. Unterpunkt (c) BERICHTIGT durch R97 (d) (58.4): gezählt sind fünfzehn Fälle.",
             "**Kette:** Marken nach R97 (e): 58.2 (R95); 58.3 (R96); 48.13 (R45); Abschnitt 27. Indexzeilen 48.20 (R52) und 54.3 (R76): fünfzehn Fälle (R97 (d)); Abschnitt 10, Punkt 10: R97 (b). Voraussetzungen und Befunde: 58.5."]
    gr = lambda f: format(len(lies(f).encode("utf-8")), ",").replace(",", " ")
    kopf = ("Reines Eintragen von Registertext, Bauart wie 57. Quellen sind allein `%s`, md5 `%s`, %s B, Abschnitt "
            "„Registerblock — zeichengleich kopierbar, nummeriert (ab R94)“, Z. %d–%d (58.1–58.3), und `%s`, md5 `%s`, %s B, Abschnitt "
            "„Registerblock — zeichengleich kopierbar, nummeriert (ab R97)“, Z. %d–%d (58.4), beide im Repo seit Commit `%s`. Nicht eingetragen werden Leseprotokoll, Teile und „Unsicher“ der Antworten. "
            "Zum Dialog gehören die Anfragen 14.10.a und 14.10.b und die Übergaben vom 14.10.2026 (a und b; alle seit `%s`). Eingetragen am %s mit TB-162 "
            "(Entscheide F5 vom 14.10.2026, 21:58, und F10–F12 vom 15.10.2026, 08:08, des steuernden Chats).") % (
            FA, FA_MD5, gr(FA), bl[0][2], bl[2][2] + 1, FB, FB_MD5, gr(FB), bl[3][2], bl[3][2] + 1, s0, s0, datum)
    neu = ["", TITEL58, "", kopf, ""]
    m58 = {k: ["", "> ⭐ **%s %s durch %s (%s)** (Fable %s %s, %s, TB-162, %s)." % (ort, wort, rr, ua, fb, rr, up, datum), ZEICHENGLEICH] for ort, k, wort, rr, ua, fb, up in MARKEN58}
    for k, ((zeile, quelle, _, _), t) in enumerate(zip(bl, titel)):
        neu += ["### 58.%d %s" % (k + 1, t), "", "> " + zeile, "> " + quelle] + m58.get(k, []) + ["", kette[k], ""]
    neu += ["### 58.5 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `docs/belege/TB-162/v_voraussetzung.txt` (Werkzeug `voraussetzung`, Anhang B des Auftrags TB-162), Zeilen wörtlich:", ""]
    neu += ["    " + l for l in vb] + [""]
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    p(len(einf) == len(MARKEN), "%d Marken am alten Ort (R96 (d), R97 (e)), 2 in 58 (R97 (e))" % len(einf))
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    for at in sorted(set(x[0] for x in einf), reverse=True): z[at:at] = [l for a2, zz in einf if a2 == at for l in zz]
    z = z[:-1] + neu; schreibe(REG, "\n".join(z))
    r2 = lies(REG).split("\n"); mz = [(i + 1, l) for i, l in enumerate(r2) if l.startswith("> ⭐ **") and ("(Fable 14a R9" in l or "(Fable 14b R97" in l) and "TB-162" in l]
    soll = ["> ⭐ **%s %s durch %s (%s)**" % (m[0], m[2], m[3], m[4]) for m in MARKEN + MARKEN58]
    zu = {s: [n for n, l in mz if l.startswith(s)] for s in soll}
    json.dump({"marken": [[m[0], m[2], m[3], m[4], (zu[s] or [0])[0]] for m, s in zip(MARKEN + MARKEN58, soll)], "abschnitt_58": r2.index(TITEL58) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(len(mz) == 8 and all(len(v) == 1 for v in zu.values()), "nachher: 8 Marken Z. %s; Abschnitt 58 Z. %d" % ([n for n, _ in mz], r2.index(TITEL58) + 1))
    p(all(r2.count("> " + b[0]) == 1 and r2.count("> " + b[1]) == 1 for b in bl), "R94-R97 mit Quellenzeile je genau einmal zeichengleich im Register")
    ende()
def index(s0, datum, probe):
    d = json.load(open("docs/belege/TB-162/r_daten.json", encoding="utf-8")); mk = d["marken"]; mz = [m[4] for m in mk]
    p(len(mk) == 8 and all(mz), "r_daten.json: 8 Marken mit Zeile")
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 58. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 58 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    x = lies(IDX); z = x.split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–57" in z[k[0]], "Kopf genau einmal, nennt 0–57"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–57", "Abschnitte 0–58")
    zus = {"| 27 Sichtschutz |": "; Abschnitt 27 ERGÄNZT durch R94 (58.1) (Z. %d); Abschnitt 27 ERGÄNZT durch R97 (58.4) (Z. %d)" % (mz[0], mz[1]),
           "| 48 aus 29b |": "; 48.13 R45 **PRÄZISIERT durch R95 (58.2)** (Z. %d); 48.13 R45 ERGÄNZT durch R97 (58.4) (Z. %d); 48.14 R46 ERGÄNZT durch R94 (58.1) (Z. %d)" % (mz[2], mz[3], mz[4]),
           "| 56 aus 09a |": "; 56.1 R84 **PRÄZISIERT durch R95 (58.2)** (Z. %d)" % mz[5]}
    for anf, t in zus.items():
        i = [j for j, l in enumerate(z) if l.startswith(anf)]
        if p(len(i) == 1 and z[i[0]].endswith(" |"), "Index-Zeile %s genau einmal" % anf): z[i[0]] = z[i[0]][:-2] + t + " |"
    i = [j for j, l in enumerate(z) if l.startswith("| 57 aus 10a |")]
    if p(len(i) == 1, "Zeile 57 genau einmal"): z.insert(i[0] + 1, "| 58 aus 14a und 14b | %s | R94–R96 (58.1–58.3, 14a); R97 (58.4, 14b); 58.5 Voraussetzungen und Befunde | 58.2 R95 **BERICHTIGT durch R97 (58.4)** (Z. %d); 58.3 R96 **BERICHTIGT durch R97 (58.4)** (Z. %d) |" % (T, mz[6], mz[7]))
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    tab = ["## 13. Die Marken aus Fable 14a und 14b (TB-162)", "", "Alle 8 Marken, die TB-162 nach R96 (d) und R97 (e) gesetzt hat (6 am alten Ort, 2 in 58), in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-162/r_daten.json`.", "",
           "| Ort | Marke | Wort | durch | T |", "|---|---|---|---|---|"]
    for ort, wort, rr, ua, zz in sorted(mk, key=lambda m: m[4]): tab.append("| %s | Z. %d | %s | %s (%s) | %s |" % (ort, zz, wort, rr, ua, T))
    tab += ["", "### Indexzeilen aus Fable 14a und 14b", "",
            "- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R96 (c) (58.3) mit R97 (d) (58.4): fünfzehn gezählte Fälle; der fünfzehnte ist „ein solches Modul schreibt keines“ in R95 (a). In R96 (c) lies „Gezählt sind fünfzehn Fälle.“ Ohne Marke (R96 (d), R97 (e)). Der Index ist kein Registertext.",
            "- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R97 (d) (58.4): fünfzehnter Fall. Ohne Marke (R97 (e)). Der Index ist kein Registertext.",
            "- **Abschnitt 10, Punkt 10:** → R97 (b) (58.4): die ausgeführten Positionen aus der Rückgabe nach R45 mit R84 (e), nachdem Punkt 10 nach 37.3 beauftragt und freigegeben ist; bis dahin Rekonstruktion. Ohne Marke (R97 (e)). Der Index ist kein Registertext.", "", "---", ""]
    if p(len(i) == 1 and z[i[0] - 2] == "---", "Pflege-Anker genau einmal, davor '---'"): z[i[0] - 1:i[0] - 1] = [""] + tab[:-2]
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-154 (")]
    if p(len(j) == 1, "Pflegezeile TB-154 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-154 (", "In TB-154 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-162 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-162 (`index`); 58 (R94–R97) kommt zu T%s; neuer Abschnitt 13 (8 Marken)." % (datum, s0, rcm, T))
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"14a": {"frage": "Ist eine Messung des Kapital-Drawdowns im Walk-Forward mit Rastersuche und IS-Sieger vor dem signierten Tag ein Versuch, was darf vor dem Tag gemessen werden, und bindet der Satz zum zweiten Rechenweg aus R45 ein Forschungsmodul ausserhalb des Laufs?",
                       "entscheidung": "Rastersuche und faltenweise Auswahl auf den Kursdaten der Bots sind vor dem Tag Versuch und unterbleiben (R94 (a), (c)); zulässig bleibt E und M der heutigen Parameter, auch in den Fenstern des bot-eigenen Walk-Forward, als Tatsachennotiz (R94 (b)); der Satz aus R45 bindet den Lauf, nicht ein Forschungsmodul ausserhalb (R95); Tatsachennotizen und Marken in R96.",
                       "offen": "ja"},
               "14b": {"frage": "Verstösst der Doppellauf aus positionen_holen.py gegen A9, und woher nimmt eine Messung nach R94 (b) vor dem Tag die ausgeführten Positionen?",
                       "entscheidung": "Ja, der Doppellauf verstösst gegen A9 und ist historischer Stand; R95 (a) in „lies“-Form berichtigt (R97 (a)). Positionen aus der Rückgabe nach R45 mit R84 (e), sobald Punkt 10 nach 37.3 freigegeben ist; bis dahin Rekonstruktion aus Trade-Liste und equity_curve, als solche benannt (R97 (b)); fünfzehnter gezählter Fall (R97 (d)).",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 14a und 14b geschrieben: %s" % ziel)
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); print("Kennung %s%s (letzte %s)" % (h[0], chr(ord(h[1]) + 1), h))
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); neu = h[0] + chr(ord(h[1]) + 1)
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-162: " % neu), "Kopfzeile ## %s — TB-162: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(i and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b, "Teil 'Was gemessen ist'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
```
