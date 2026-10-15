# TB-163 Register 59 (Tatsachennotiz TB-162) und E-6: Horizont je Bot aus `faltenplan.HORIZONTBEGINN` (TB-30b Posten 4) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 15.10.2026, 18:52** (Helfer BAU163, per Skript aus Bausteinen, `$HOME/sc/tb163/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an einer Kopie simuliert. Urteil und Freigabe beim steuernden Chat; nach dem Bau liest ein frischer Gegenleser (F5, W1). **Gebaut am HEAD `8517c5f`.**

**Sitzungstitel:** `TB-163` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `8517c5f5eff85058730b0322b4e009be8e78301c` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu; F1) · **Start:** über den Sitzungswächter (`starte_TB-163`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-163_register59_posten4_horizont.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`; Werkzeug `docs/belege/TB-163/tb163_werkzeug.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-163/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md`. **Journal:** nächste freie Kennung (am Bau-HEAD höchste EY ⇒ EZ).
**Grundlage:** Entscheide F1–F6 des steuernden Chats vom 15.10.2026, 18:25; Bestand BESTAND30B. **Zeitgrenze:** jeder Bash-Aufruf mit dem Parameter `timeout` des Bash-Werkzeugs, 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V (Voraussetzungen) ⇒ N (Register 59, zuerst; F2) ⇒ K (Kopien, Index, Dialog-Index; F2) ⇒ E (E-6 mit Tests und R81 (d); F3, F4) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe; F6). Scheitert E, bleiben ⟨N⟩ und ⟨K⟩; nach einem Abbruch in E bleiben die vier Optimierer im Arbeitsbaum geändert und `research/posten4_horizont/` unverfolgt — das wird gemeldet.

## Freigabe — Karten des Betreibers, wörtlich (`tb30b_ENTSCHEIDE.md`)

> 15.10.2026 18:17 Karte Betreiber: Tatsachennotiz TB-162 ins Register, als Schritt im nächsten Mac-Auftrag (Ja, Recommended).
> 15.10.2026 18:17 Karte Betreiber: nächster Handelsschritt Rang 1 TB-30b formulieren (Recommended).
> 15.10.2026 18:24 Karte Betreiber: Einzelfreigabe nach 37.3 für E-6 (Posten 4, Horizont je Bot, vier Aktien-Optimierer), Auftrag mit R81 (d) und Tatsachennotiz TB-162 als Abschnitt 59 (Ja, Recommended).

Die dritte Karte ist die **Einzelfreigabe nach 37.3** für E-6 (F3). Regel 37.3 (Register Z. 7022): „Ein Befund 1 der Sperrlisten-Sonde vor dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein neues Abbild unter neuem Namen geschlossen, nie durch Anpassung des alten.“ Sperrlistenpunkt 11 (Register Z. 11213): „Hash-Übergänge nach 37.3 (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“)“ — die vier Optimierer stehen auf der Sperrliste (`research/vorregistrierung/herkunft.py` Z. 102–106, Muster `strategies/*/multi_symbol_optimise.py`); der Befund `1` ist vor dem Tag zulässig, weil beauftragt, und wird als Hash-Übergang notiert. **Vorbild des Hash-Übergangs:** `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md` Z. 17 und 136 (Entwurf der Tatsachennotiz im Ergebnis, Tabelle Datei · vorher · nachher · Commit · vollzieht), eingetragen als Register 50.3 (Z. 11198–11243). Wie dort: der Übergang steht in diesem Auftrag **nur als Entwurf im Ergebnis**, nicht im Register.

## E-6 und die Voraussetzung aus R81 (d) — wörtlich aus dem Register, per Skript

- **E-6** (`docs/belege/TB-120/d_plan.md` Z. 47): „| **E-6** Posten 4 | G8: Horizont je Bot aus `faltenplan.HORIZONTBEGINN` in den vier Aktien-Optimierern | AN-51 | `strategies/{elliott_wave_stocks,rsi2_mean_reversion,turtle_soup_stocks,volatility_breakout}/multi_symbol_optimise.py` | Punkt 11 | klein — 4 Dateien; ⚠️ Reihenfolge zu E-4 nach F-13 |“
- **55.8 Nr. 3** (Register Z. 11840): „| 3 | Posten 4: das Fenster je Bot aus dem Register statt aus der letzten Zeile der Datei (26.2, 28.5, R44), dazu die Voraussetzung aus R81 (d) | vor der Neuerzeugung der Listen (R44); Signalpfad, Einzelfreigabe nach 37.3 (Antwort 07.10.a, Frage 1 (c)) |“
- **R81 (d)** (Register Z. 11775): „(d) Fenster. Dass die vier Aktien-Bots den frühesten Einstieg, elliott_wave_stocks den Anfang der geladenen Zeilen, aus der letzten Zeile der Datei bilden, ist die Datenuhr, die 26.2 ablöst: Der Horizontbeginn ist asof minus RECENT_YEARS_ONLY (28.4), gilt für alle Symbole des Bots gleich, und der Vorlauf rechnet gegen ihn (28.6). Das ist entschieden und im Code offen (28.5; R44: Posten 4, vor der Neuerzeugung der Listen); dieser Block fügt dem nichts hinzu. [Voraussetzung, mit Posten 4 zu messen: dass danach bei keinem der vier Bots das Ende einer Datei in Fenster, Scanbeginn oder Anfang der geladenen Zeilen eingeht.]“
- **Am Code (Bau-HEAD):** `strategies/elliott_wave_stocks/multi_symbol_optimise.py` Z. 93: `cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`; `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` Z. 93: `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`; `strategies/turtle_soup_stocks/multi_symbol_optimise.py` Z. 81: `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`; `strategies/volatility_breakout/multi_symbol_optimise.py` Z. 89: `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`. Der Horizontbeginn steht in `research/vorregistrierung/faltenplan.py` Z. 228: `HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}`. Der Grenzwert folgt der Zeitzone der Spalte `open_time` (naiv bleibt naiv; tz-behaftet ⇒ `tz_localize` auf die Spaltenzone).

**Die Voraussetzung wird in Schritt E erfüllt und als Abbruchbedingung geprüft:** `WZ r81d` endet nur mit `rc 0`, wenn in keiner der vier Dateien das Fenster aus `open_time.max()` gebildet wird, der Wert aus `faltenplan.horizontbeginn(<bot>)` kommt, `elliott_wave_stocks` die geladenen Zeilen am Horizontbeginn kappt, der Scanbeginn von `volatility_breakout` (`backtest_breakout.py`, unverändert) dem `entry_cutoff` folgt und die synthetische Probe (drei Dateienden je Bot) alle Prüfungen besteht. **Befund, kein Teil von R81 (d):** ob ein Symbol aufgenommen wird (`timespan_days` gegen `MIN_HISTORY_DAYS`), hängt weiter vom Dateiende ab; `buy_and_hold_benchmark.py` (rsi2, turtle, vb) bildet seinen `cutoff` weiter aus `.max()` — beides nicht E-6, im Ergebnis nennen.

## Verboten (F4; R94 (a), (c))

Keine Rastersuche, **kein Lauf eines Optimierers, eines Walk-Forward-Rechners oder einer equity_simulation auf Kursdaten**, keine Neuerzeugung der Listen (E-4), keine Änderung am DD-Mass, `positionen_holen.py` nie. Die Tests rechnen **nur synthetisch** (Temp-Ordner, Zufallspfad); `data/` wird nicht gelesen. **Schreiben darf die Sitzung nur:** `docs/VORREGISTRIERUNG_neuselektion.md` (N, nur `WZ register`, append-only), `docs/projektfuehrung/REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), die vier Dateien `strategies/{elliott_wave_stocks,rsi2_mean_reversion,turtle_soup_stocks,volatility_breakout}/multi_symbol_optimise.py` (E, nur `WZ e6`), `research/posten4_horizont/` (E), `docs/belege/TB-163/`, `docs/projektfuehrung/BACKLOG.md` (`WZ backlog`), `docs/projektfuehrung/JOURNAL.md` (`WZ journal`), das Ergebnis. Kein Netz; kein `pip`, kein `brew`.

## Lage nach dem Auslegen

Am Bau-HEAD `8517c5f`: geändert `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/projektfuehrung/UEBERGABE.md`; unverfolgt nichts. Das Auslegen ändert dazu `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab. **Beim Start genau 4 Einträge** (Soll in 0a).

## Belegt · erschlossen · offen (am Bau)

**Belegt:** HEAD `8517c5f`; Notiz TB-162 `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` Z. 199–232 (md5 `210508624458a7287f89888a65304394`, zuletzt geändert in `16db5e3`); Register endet mit 58, 59 fehlt; sha256 vorher der vier Optimierer, `faltenplan.py` und `backtest_breakout.py` stehen im Werkzeug (`VOR`), nachher im Werkzeug (`NACH`, aus dem Bau). **An einer Kopie (Python 3.10, synthetisch):** `test_posten4_horizont.py` 34 von 34, rc 0; am unveränderten Stand 10 von 30, rc 1 (die Probe erkennt die Datenuhr); geprüft je Bot naiv und mit tz-behaftetem `open_time` (UTC). Befund ausserhalb E-6: `backtest_breakout.py` Z. 211 (`entry_time >= np.datetime64(entry_cutoff)`) wirft mit tz-behaftetem `open_time` TypeError — am unveränderten Stand ebenso; die Probe meldet das als `INFO`, zählt es nicht. **Erschlossen:** `import faltenplan` zieht beim ersten Laden registerdaten, faltenplan_neun, erste_falte_trockenlauf und deren Importe (u. a. `notifications/manual_close.py`) in den Optimierer-Prozess. **Offen, nur am Mac messbar:** ob V dort `rc 0` endet; ob Python 3.9 und trading-env (yfinance) die Probe so laufen lassen; Laufzeit; ob `registerkopie.py` 59 in die Teildatei docs/projektfuehrung/REGISTER_KOPIE_teil6.md legt.

## Schritt 0 — Ausgang

**0a. Zuerst:** `git status --porcelain > "$TMPDIR/tb163_0a.txt"`, `git rev-parse HEAD` und `git rev-parse --abbrev-ref HEAD`. Soll: Zweig `main`, HEAD `8517c5f5eff85058730b0322b4e009be8e78301c` und genau diese 4 Einträge; sonst **ABBRUCH** (vor ⟨S0⟩ und vor jedem Push). Kein späterer Schritt wechselt den Zweig.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-163_register59_posten4_horizont.md
```

Werkzeug und Probe aus den Anhängen holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-163_register59_posten4_horizont.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
for kopf, ziel in (("### Werkzeug", "tb163_werkzeug.py"), ("## Anhang A — Probe `research/posten4_horizont/test_posten4_horizont.py` (wörtlich)", "tb163_test_posten4_horizont.py")):
    a = z.index("```python", z.index(kopf))
    t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
    open(sys.argv[2] + "/" + ziel, "w", encoding="utf-8").write(t)
    print(ziel, hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll genau: `tb163_werkzeug.py 1b7f58c554a98ea9cb51a5c6aa7fcf72dc7289642e7742fb7b9c08c7571b8ee9` · `tb163_test_posten4_horizont.py ed13dd2cbbde0bed0e83f06f363da3f6c1c8d588d25f0fd71c73b4196039534c`; sonst **ABBRUCH**. Commit `TB-163 Schritt 0: Stand des steuernden Chats vor TB-163` mit genau diesen Pfaden, pushen ⇒ **⟨S0⟩** (7 Zeichen). Erst danach: `mkdir -p docs/belege/TB-163`, `cp "$TMPDIR/tb163_0a.txt" docs/belege/TB-163/0a_status.txt`, `cp "$TMPDIR/tb163_werkzeug.py" docs/belege/TB-163/tb163_werkzeug.py` (je `diff` ohne Ausgabe).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-163_register59_posten4_horizont.md
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py voraussetzung > docs/belege/TB-163/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0`, davor `Pruefungen: 18, NEIN: 0` (Sperrliste Punkt 11; sha256 vorher; HORIZONTBEGINN-Literal; Register 58 da, 59 nicht; R81 (d) genau einmal; Notiz TB-162 Z. 199–232 und md5; Anker der vier Dateien). Sonst **ABBRUCH**.

## Schritt N — Register 59 (F2; zuerst)

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ --probe > docs/belege/TB-163/n_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/n_probe.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ > docs/belege/TB-163/n_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/n_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach steht am Registerende `## 59. Tatsachennotiz TB-162 — Kapital-Drawdown E und M je Abschnitt des bot-eigenen Walk-Forward (TB-163)` mit Kopfsatz und `### 59.1` (Notiz zeichengleich aus `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` Z. 199–232). Append-only: `git diff --numstat` des Registers zeigt in Spalte 2 eine `0` (Schritt A). Commit `TB-163 N: Register 59 (Tatsachennotiz TB-162)`, pushen ⇒ **⟨N⟩**.

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-163/0a_status.txt
git add docs/belege/TB-163/tb163_werkzeug.py
git add docs/belege/TB-163/v_voraussetzung.txt
git add docs/belege/TB-163/n_probe.txt
git add docs/belege/TB-163/n_eintrag.txt
```

## Schritt K — Kopien, Index, Dialog-Index (F2; wie TB-162 Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-163/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-163/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-163/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨N⟩ > docs/belege/TB-163/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-163/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-163/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. `registerkopie.py` schreibt Teildateien und Abschnittskopien neu (59 neu); `c2_index_zeilen.py` (aus TB-154, unverändert) schreibt die Zeilenangaben von ⟨S0⟩ auf ⟨N⟩ um; `WZ index` setzt Kopf (0–59), Zeile 59 und die Pflegezeile. Kein neuer Fable-Dialog: `dialog_index.py --pruefen` allein. Entsteht eine weitere Teildatei: mit Namen anpassen, melden. rc ≠ 0 eines Schritts: festhalten, die Dateien dieses Schritts nicht committen, melden (kein Abbruch). Commit `TB-163 K: Registerkopie, Index`, pushen ⇒ **⟨K⟩**.

```
git add docs/projektfuehrung/REGISTER_INDEX.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil1.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil2.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil3.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil4.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil5.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil6.md
git add docs/projektfuehrung/register_kopie
git add docs/belege/TB-163/k_registerkopie.txt
git add docs/belege/TB-163/k_abschnitte.txt
git add docs/belege/TB-163/k_pruefen.txt
git add docs/belege/TB-163/k_index_zeilen.txt
git add docs/belege/TB-163/k_index.txt
git add docs/belege/TB-163/k_dialog_pruefen.txt
```

## Schritt E — E-6: Horizont je Bot (F3, F4)

```
mkdir -p research/posten4_horizont
cp "$TMPDIR/tb163_test_posten4_horizont.py" research/posten4_horizont/test_posten4_horizont.py
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py e6 --probe > docs/belege/TB-163/e_e6_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/e_e6_probe.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py e6 > docs/belege/TB-163/e_e6.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/e_e6.txt
trading-env/bin/python3 -B research/posten4_horizont/test_posten4_horizont.py > docs/belege/TB-163/e_test.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/e_test.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py r81d docs/belege/TB-163/e_test.txt > docs/belege/TB-163/e_r81d.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/e_r81d.txt
```

Soll: `e_e6_probe.txt` und `e_e6.txt` je `rc 0` (sha256 vorher und nachher wie im Werkzeug); `e_test.txt` „34 von 34 Pruefungen bestanden“ und `rc 0`; `e_r81d.txt` mit `R81 (d) Voraussetzung: erfuellt …` und `rc 0`. **Endet `e_e6_probe.txt`, `e_test.txt` oder `e_r81d.txt` nicht mit `rc 0`: ABBRUCH ohne Commit der vier Dateien** (Abbruchweg; die vier Dateien und `research/posten4_horizont/` werden **nicht** gestaged). Sonst Commit `TB-163 E: E-6 Horizont je Bot aus faltenplan.HORIZONTBEGINN`, pushen ⇒ **⟨E⟩**; dann `trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py uebergang ⟨E⟩ > docs/belege/TB-163/e_uebergang.md` (Entwurf des Hash-Übergangs).

```
git add strategies/elliott_wave_stocks/multi_symbol_optimise.py
git add strategies/rsi2_mean_reversion/multi_symbol_optimise.py
git add strategies/turtle_soup_stocks/multi_symbol_optimise.py
git add strategies/volatility_breakout/multi_symbol_optimise.py
git add research/posten4_horizont/test_posten4_horizont.py
git add docs/belege/TB-163/e_e6_probe.txt
git add docs/belege/TB-163/e_e6.txt
git add docs/belege/TB-163/e_test.txt
git add docs/belege/TB-163/e_r81d.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe (F6)

`trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py kennung > docs/belege/TB-163/a_kennung.txt; echo "rc $?" >> docs/belege/TB-163/a_kennung.txt` (Soll „Kennung EZ …“, `rc 0`). Dann:

```
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-163/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-163/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/a_backlog.txt
```

Block nach `BEL/a_block.md` (Schreibwerkzeug; erste Zeile `## <Kennung> — TB-163: …`, Quellenzeile, `**Quelle:**`, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; keine weitere `## `-Zeile, kein `---`), dann:

```
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py journal docs/belege/TB-163/a_block.md --probe > docs/belege/TB-163/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-163/tb163_werkzeug.py journal docs/belege/TB-163/a_block.md > docs/belege/TB-163/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-163/a_journal.txt
```

Soll je `rc 0`; endet eine Probe nicht mit `rc 0`: zweiten nicht ausführen, **ABBRUCH**. **Ergebnis** `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` (Schreibwerkzeug): Kopf mit Commits · „Kurz“ · Voraussetzungen (`v_voraussetzung.txt` wörtlich) · Register 59 (Zeile, numstat) · E-6: `e_test.txt` und `e_r81d.txt` wörtlich, **Entwurf Tatsachennotiz Hash-Übergang nach 37.3** (`e_uebergang.md` wörtlich; Freigabe = dritte Karte oben; `herkunft.register()` vorher/nachher nur, wenn ohne Lauf auf Kursdaten messbar, sonst „nicht gemessen“) · **Offen:** der Hash-Übergang nach 37.3 bleibt offen bis zum Registereintrag (Folgeauftrag, wie TB-122 → Register 50.3) und bis zum neuen Abbild unter neuem Namen (37.3); der Entwurf führt die vollen Hashes (39.5) · Befunde (MIN_HISTORY_DAYS, buy_and_hold_benchmark, Import-Kette, `backtest_breakout.py` Z. 211 mit tz-behaftetem `open_time`, die `INFO`-Zeilen aus `e_test.txt`) · Abweichungen (gab es vorher einen Abbruch in E: die vier Optimierer geändert, `research/posten4_horizont/` unverfolgt — nennen) · **In einfacher Sprache**. Commit `TB-163 Abgabe: Ergebnis, BACKLOG, Journal <Kennung>` (erster Block), pushen ⇒ **⟨F⟩**; dann `git status --porcelain > "$TMPDIR/tb163_f.txt"`, `cp "$TMPDIR/tb163_f.txt" docs/belege/TB-163/f_porcelain.txt`, `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-163/f_numstat.txt` (Soll: Register-Zeile Spalte 2 = `0`), Commit `TB-163 F: porcelain und numstat` (zweiter Block), pushen.

```
git add docs/ERGEBNIS_TB-163_register59_posten4_horizont.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-163/e_uebergang.md
git add docs/belege/TB-163/a_kennung.txt
git add docs/belege/TB-163/a_backlog_probe.txt
git add docs/belege/TB-163/a_backlog.txt
git add docs/belege/TB-163/a_block.md
git add docs/belege/TB-163/a_journal_probe.txt
git add docs/belege/TB-163/a_journal.txt
```

```
git add docs/belege/TB-163/f_porcelain.txt
git add docs/belege/TB-163/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab (Zweig, HEAD, Einträge); Holbefehl-Soll weicht ab; V nicht `rc 0`; `WZ register --probe`/`register` nicht `rc 0`; `WZ e6 --probe`/`e6` nicht `rc 0`; `e_test.txt` nicht alle bestanden; `WZ r81d` nicht `rc 0`; `WZ backlog`/`journal` nicht `rc 0`; `git push` scheitert zweimal (nicht für den Abbruch-Commit); Claude Code verlangt eine Bestätigung (melden, nicht umgehen). **Kein Abbruch:** ein Schritt in K mit rc ≠ 0.
**Abbruchweg:** vor ⟨S0⟩ nichts schreiben, nur melden. Danach genau eine neue Datei `printf '%s\n' "<Schritt>: <Grund>" > docs/belege/TB-163/abbruch.txt` — bei einem Abbruch in E nach `WZ e6` stattdessen `printf '%s\n' "E: <Grund>" "Arbeitsbaum: die vier Optimierer bleiben geändert, research/posten4_horizont/ bleibt unverfolgt (Abbruch in E nach WZ e6)." > docs/belege/TB-163/abbruch.txt` (zweite Zeile wörtlich) —, `git add` dieser Datei und jeder schon entstandenen, nicht committeten Belegdatei unter `docs/belege/TB-163/` mit Namen (nie `git add -A`, nie `-f`; **nie** eine Datei unter `strategies/` oder `research/posten4_horizont/`), Commit `TB-163 Abbruch: <Schritt>`, pushen, melden. **Abbruch in E (nach `WZ e6`):** die vier Optimierer bleiben im Arbeitsbaum geändert und `research/posten4_horizont/` unverfolgt; das steht als zweite Zeile in `abbruch.txt` und in der Meldung. **Scheitert Commit oder Push des Abbruch-Commits: nicht wiederholen, anhalten, melden.** Nichts zurückdrehen (kein `reset`, `revert`, `restore`, `checkout`).

## In einfacher Sprache

Zwei Dinge. Erstens trägt die Sitzung die Messung aus TB-162 (wie tief das Konto der heutigen Einstellungen in den Walk-Forward-Abschnitten fiel) als Tatsachennotiz ins Register ein — wortgleich, nur angehängt. Zweitens behebt sie bei den vier Aktien-Bots eine „Datenuhr“: Bisher hing das Zehnjahresfenster am letzten Kurstag jeder einzelnen Datei; eine Datei, die einen Tag länger ist, verschob das Fenster. Künftig gilt für alle Symbole das eine Datum aus dem Register (19.09.2016). Geprüft wird das nur mit erfundenen Kursreihen; kein Optimierer läuft, keine Parameter werden gesucht. Der Betreiber hat die Änderung an den gesperrten Dateien einzeln freigegeben; die alten und neuen Prüfsummen stehen als Entwurf im Ergebnis.

## Anhang — Dateien und ihre Befehle

| Datei | Befehl |
|---|---|
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/UEBERGABE.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/auftraege/MAC_TB-163_register59_posten4_horizont.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/VORREGISTRIERUNG_neuselektion.md` | Schritt N (`WZ register`) |
| `docs/belege/TB-163/0a_status.txt` | Schritt N |
| `docs/belege/TB-163/tb163_werkzeug.py` | Schritt N |
| `docs/belege/TB-163/v_voraussetzung.txt` | Schritt N |
| `docs/belege/TB-163/n_probe.txt` | Schritt N |
| `docs/belege/TB-163/n_eintrag.txt` | Schritt N |
| `docs/projektfuehrung/REGISTER_INDEX.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil1.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil2.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil3.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil4.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil5.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil6.md` | Schritt K |
| `docs/projektfuehrung/register_kopie` | Schritt K |
| `docs/belege/TB-163/k_registerkopie.txt` | Schritt K |
| `docs/belege/TB-163/k_abschnitte.txt` | Schritt K |
| `docs/belege/TB-163/k_pruefen.txt` | Schritt K |
| `docs/belege/TB-163/k_index_zeilen.txt` | Schritt K |
| `docs/belege/TB-163/k_index.txt` | Schritt K |
| `docs/belege/TB-163/k_dialog_pruefen.txt` | Schritt K |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | Schritt E (`WZ e6`) |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | Schritt E (`WZ e6`) |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | Schritt E (`WZ e6`) |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | Schritt E (`WZ e6`) |
| `research/posten4_horizont/test_posten4_horizont.py` | Schritt E |
| `docs/belege/TB-163/e_e6_probe.txt` | Schritt E |
| `docs/belege/TB-163/e_e6.txt` | Schritt E |
| `docs/belege/TB-163/e_test.txt` | Schritt E |
| `docs/belege/TB-163/e_r81d.txt` | Schritt E |
| `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` | Schritt A |
| `docs/projektfuehrung/BACKLOG.md` | Schritt A |
| `docs/projektfuehrung/JOURNAL.md` | Schritt A |
| `docs/belege/TB-163/e_uebergang.md` | Schritt A |
| `docs/belege/TB-163/a_kennung.txt` | Schritt A |
| `docs/belege/TB-163/a_backlog_probe.txt` | Schritt A |
| `docs/belege/TB-163/a_backlog.txt` | Schritt A |
| `docs/belege/TB-163/a_block.md` | Schritt A |
| `docs/belege/TB-163/a_journal_probe.txt` | Schritt A |
| `docs/belege/TB-163/a_journal.txt` | Schritt A |
| `docs/belege/TB-163/f_porcelain.txt`, `docs/belege/TB-163/f_numstat.txt` | Abgabe |
| `docs/belege/TB-163/abbruch.txt` | nur Abbruchweg |
| `$TMPDIR/tb163_*` | 0a, Holbefehl, Abgabe; bleiben liegen |

## Anhang A — Probe `research/posten4_horizont/test_posten4_horizont.py` (wörtlich)

```python
#!/usr/bin/env python3
"""TB-163 (E-6, TB-30b Posten 4): Horizont je Bot aus faltenplan.HORIZONTBEGINN in den vier
Aktien-Optimierern - Pruefung auf SYNTHETISCHEN Kursen (Zufallspfad im Temp-Ordner), keine
Kursdaten aus data/, kein Optimierer-Lauf, keine Rastersuche. R81 (d): das Ende einer Datei geht
weder in das Fenster noch in den Scanbeginn noch in den Anfang der geladenen Zeilen ein.
Aufruf aus der Repo-Wurzel: python3 -B research/posten4_horizont/test_posten4_horizont.py
(je Bot ein Kindprozess, damit sich gleichnamige Bot-Module nicht mischen). rc 0 = alle bestanden."""
import importlib.util, os, re, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = ["elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout"]
ENDE_A, ENDE_B, ENDE_C = "2026-09-30", "2025-06-30", "2026-12-31"
def kind(bot):
    import numpy as np
    import pandas as pd
    H = pd.Timestamp(2016, 9, 19); n = [0, 0]
    def pruefe(name, ok, info=""):
        n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + bot + ": " + name + (" · " + str(info) if info else ""))
    t = pd.bdate_range("2008-01-02", ENDE_C); r = np.random.default_rng(163)
    c = 50 * np.exp(np.cumsum(r.normal(0.0002, 0.018, len(t)))); o = c * (1 + r.normal(0, 0.004, len(t)))
    h = np.maximum(o, c) * (1 + np.abs(r.normal(0, 0.008, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, 0.008, len(t))))
    basis = pd.DataFrame({"open_time": t.strftime("%Y-%m-%d"), "open": o, "high": h, "low": lo, "close": c, "volume": r.integers(100000, 1000000, len(t))})
    sys.path.insert(0, os.path.join(WURZEL, "strategies", bot))
    spec = importlib.util.spec_from_file_location("opt_" + bot, os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    src = open(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), encoding="utf-8").read()
    pruefe("Quelltext: kein Fenster aus open_time.max() - DateOffset", not re.search(r'\["open_time"\]\.max\(\)\s*-\s*pd\.DateOffset', src))
    hb = getattr(m, "horizontbeginn_ts", None)
    pruefe("horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19", hb is not None and hb() == H, hb() if hb else "fehlt")
    if hb is not None:
        import faltenplan
        pruefe("Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)", os.path.samefile(faltenplan.__file__, os.path.join(WURZEL, "research", "vorregistrierung", "faltenplan.py")) and pd.Timestamp(faltenplan.HORIZONTBEGINN["aktien"]) == H)
    interval = getattr(m, "INTERVAL", "1d")
    for zone in (None, "UTC"):  # B5: naiv (heute alle Aktien-1d-Dateien) und zeitzonenbehaftet (open_time mit +00:00)
        hz = H if zone is None else H.tz_localize(zone); kz = "naiv" if zone is None else "tz " + zone
        with tempfile.TemporaryDirectory() as d:
            for s, e in (("AAA", ENDE_A), ("BBB", ENDE_B), ("CCC", ENDE_C)):
                x = basis[basis["open_time"] <= e].copy()
                if zone is not None:
                    x["open_time"] = x["open_time"] + " 00:00:00+00:00"
                x.to_csv(os.path.join(d, "%s_%s.csv" % (s, interval)), index=False)
            m.DATA_DIR = d; m.SYMBOLS = ["AAA", "BBB", "CCC"]
            try:
                data = m.load_all_symbol_data()
            except Exception as ex:
                pruefe("[%s] Laden ohne Fehler" % kz, False, repr(ex)[:200]); continue
        pruefe("[%s] alle drei synthetischen Symbole geladen" % kz, sorted(data) == ["AAA", "BBB", "CCC"], sorted(data))
        if sorted(data) != ["AAA", "BBB", "CCC"]:
            continue
        if bot == "elliott_wave_stocks":
            anf = {s: data[s]["open_time"].min() for s in data}
            pruefe("[%s] Anfang der geladenen Zeilen = Horizontbeginn, gleich fuer drei Dateienden" % kz, all(v == hz for v in anf.values()), {k: str(v) for k, v in anf.items()})
            a, c2 = data["AAA"].reset_index(drop=True), data["CCC"].reset_index(drop=True)
            pruefe("[%s] laengere Datei (CCC) beginnt zeilengleich wie AAA" % kz, a.equals(c2.iloc[:len(a)].reset_index(drop=True)))
        else:
            cut = {s: data[s][1] for s in data}
            pruefe("[%s] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden" % kz, all(v == hz and (v.tzinfo is None if zone is None else (v.tzinfo is not None and v.utcoffset() == pd.Timedelta(0))) for v in cut.values()), {k: str(v) for k, v in cut.items()})
            if bot == "volatility_breakout":
                import backtest_breakout as bb
                sc = {s: int((data[s][0]["open_time"] < data[s][1]).sum()) for s in data}
                pruefe("[%s] Scanbeginn (Zeilen vor entry_cutoff) gleich fuer drei Dateienden" % kz, len(set(sc.values())) == 1, sc)
                try:
                    ta, tc = (bb.run_backtest(data[s][0], entry_cutoff=data[s][1]) for s in ("AAA", "CCC"))
                except TypeError as ex:  # backtest_breakout.py (nicht E-6, unveraendert): np.datetime64(entry_cutoff) gegen tz-behaftetes entry_time
                    print("INFO  %s: [%s] run_backtest: %s - Befund ausserhalb E-6, nicht gezaehlt" % (bot, kz, str(ex)[:120])); continue
                ez = lambda v: pd.to_datetime(v) if zone is None else pd.to_datetime(v, utc=True)
                pruefe("[%s] kein Einstieg vor dem Horizontbeginn" % kz, len(ta) == 0 or ez(ta["entry_time"]).min() >= hz, len(ta))
                gr = pd.Timestamp(ENDE_A) - pd.Timedelta(days=60); gr = gr if zone is None else gr.tz_localize(zone)
                g = lambda y: y[ez(y["exit_time"]) < gr].reset_index(drop=True)
                pruefe("[%s] Trades bis 60 Tage vor dem Ende von AAA gleich bei laengerer Datei" % kz, len(g(ta)) > 0 and g(ta).equals(g(tc)), len(g(ta)))
    return n
if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--kind":
        n = kind(sys.argv[2]); print("KIND %d %d" % tuple(n)); sys.exit(0)
    gesamt = [0, 0]
    for b in BOTS:
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--kind", b], capture_output=True, text=True, cwd=WURZEL)
        zeilen = [l for l in r.stdout.split("\n") if l.startswith(("ja ", "NEIN", "INFO"))]; print("\n".join(zeilen))
        k = [l for l in r.stdout.split("\n") if l.startswith("KIND ")]
        if r.returncode != 0 or not k:
            print("NEIN  %s: Kindprozess rc %d: %s" % (b, r.returncode, (r.stderr.strip().split("\n") or [""])[-1][:200])); gesamt[0] += 1; continue
        a, ok = map(int, k[0].split()[1:]); gesamt[0] += a; gesamt[1] += ok
    print("%d von %d Pruefungen bestanden" % (gesamt[1], gesamt[0])); sys.exit(0 if gesamt[0] == gesamt[1] and gesamt[0] > 0 else 1)
```

## Anhang B — Werkzeug

### Werkzeug

```python
#!/usr/bin/env python3
"""TB-163 Werkzeug (Anhang B): Voraussetzungen, Register 59 (Tatsachennotiz TB-162), Index, E-6 (Horizont je Bot), R81 (d), Hash-Uebergang, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                       Voraussetzungen messen (rc 0 = alle ja)
  register <DATUM> <S0> [--probe]     Abschnitt 59 am Registerende anhaengen (Notiz zeichengleich aus ERGEBNIS_TB-162 Z. 199-232)
  index <S0> <DATUM> [--probe]        REGISTER_INDEX.md: Kopf 0-59, Zeile 59, Pflegezeile (nach c2_index_zeilen.py)
  e6 [--probe]                        E-6: Horizont je Bot aus faltenplan.HORIZONTBEGINN in den vier Aktien-Optimierern
  r81d <TESTBELEG>                    R81 (d) nach E-6 pruefen (Code und Testbeleg)
  uebergang <E>                       Entwurf Tatsachennotiz Hash-Uebergang nach 37.3 (Sperrlistenpunkt 11)
  backlog <DATUM> <KENNUNG> [--probe] BACKLOG: Rang 1 und Zeile 'Vor der Neuerzeugung der Listen' (Posten 4 erledigt)
  kennung | journal <BLOCK> [--probe] naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
ERG, ERG_MD5, ERG_COMMIT = "docs/ERGEBNIS_TB-162_wf_kapital_dd.md", "210508624458a7287f89888a65304394", "16db5e3"
FP, BB = "research/vorregistrierung/faltenplan.py", "strategies/volatility_breakout/backtest_breakout.py"
TITEL59 = "## 59. Tatsachennotiz TB-162 — Kapital-Drawdown E und M je Abschnitt des bot-eigenen Walk-Forward (TB-163)"
R81D = "[Voraussetzung, mit Posten 4 zu messen: dass danach bei keinem der vier Bots das Ende einer Datei in Fenster, Scanbeginn oder Anfang der geladenen Zeilen eingeht.]"
DEF = "def load_all_symbol_data() -> dict:"
ALT = {"elliott_wave_stocks": '            cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "rsi2_mean_reversion": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "turtle_soup_stocks": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "volatility_breakout": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)'}
VOR = {
 "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "275273776fafb2453cdb41f634b86bacffd5994f8b5508ef034400cd7c5ede9d",
 "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "777f5cb0a637bb8770d1cd4a89aac03c6b29db98d13ce47eac6de29db279c661",
 "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "e4277f013be6d0af85647f5d32d8cdb60ef086d06c6e041853c6da571c96ddd4",
 "strategies/volatility_breakout/multi_symbol_optimise.py": "f0a4ee43dca133e89272e48d80280d8a22f57d751d2ddac06751fd091198af2d",
 "research/vorregistrierung/faltenplan.py": "63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7",
 "strategies/volatility_breakout/backtest_breakout.py": "3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76"
}
NACH = {
 "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232",
 "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "61838aca901cabeace70511b71742d10cba4de6575a999aecf5a492f938ad6dc",
 "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "29e7f10c3eb79f8316c53c9a31ee3ea0dd450d44bb9904dc2ba9944df003c0cc",
 "strategies/volatility_breakout/multi_symbol_optimise.py": "24c182ae1cf7c882c9e3aec31c5088348e2fa44c5cc2e99eab54ecf29b337585"
}
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def opt(b): return "strategies/%s/multi_symbol_optimise.py" % b
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def hilfe(bot):
    return ["def horizontbeginn_ts(spalte=None) -> pd.Timestamp:",
            '    """TB-163 (E-6, TB-30b Posten 4; R44, R81 (d), Register 26.2/28.4/28.5): der',
            "    Horizontbeginn des Bots aus research/vorregistrierung/faltenplan.py",
            "    (HORIZONTBEGINN ueber faltenplan.horizontbeginn) - ein Datum fuer alle Symbole",
            "    des Bots, nicht die letzte Zeile der Datei. Import erst beim Aufruf. Mit",
            "    `spalte` (open_time) in deren Zeitzone: naiv bleibt naiv, tz-behaftet",
            '    wird der Grenzwert auf die Spaltenzone lokalisiert."""',
            '    _vr = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "research", "vorregistrierung")',
            "    if _vr not in sys.path:", "        sys.path.insert(0, _vr)",
            "    import faltenplan  # noqa: E402",
            '    h = faltenplan.horizontbeginn("%s")' % bot,
            "    if h is None:", '        raise ValueError("%s: kein Horizontbeginn im Faltenplan")' % bot,
            "    t = pd.Timestamp(h)",
            '    tz = getattr(getattr(spalte, "dt", None), "tz", None) if spalte is not None else None',
            "    return t.tz_localize(tz) if tz is not None else t", "", ""]
def neu_text(bot, t):
    z = t.split("\n"); a = [i for i, l in enumerate(z) if l == ALT[bot]]; d = [i for i, l in enumerate(z) if l == DEF]
    if len(a) != 1 or len(d) != 1 or "horizontbeginn_ts" in t: return None
    var = ALT[bot].split("=")[0].rstrip()
    z[a[0]] = var + ' = horizontbeginn_ts(df["open_time"])  # TB-163 (E-6): Horizont aus faltenplan.HORIZONTBEGINN, nicht aus dem Dateiende (R81 (d), 28.4)'
    z[d[0]:d[0]] = hilfe(bot); return "\n".join(z)
def voraussetzung():
    hk = lies("research/vorregistrierung/herkunft.py").split("\n")[101:106]
    p(any('"strategies/*/multi_symbol_optimise.py"' in l for l in hk), "Sperrliste herkunft.py Z. 102-106 nennt strategies/*/multi_symbol_optimise.py (Punkt 11, 37.3)")
    for f, h in sorted(VOR.items()): p(sha(f) == h, "sha256 vorher %s = %s…" % (f, h[:16]))
    fp = lies(FP); p(fp.count('HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}') == 1, "faltenplan.py: HORIZONTBEGINN-Literal genau einmal (aktien 2016-09-19)")
    reg = lies(REG); z = reg.split("\n")
    p(not re.search(r"^## 59\. ", reg, re.M) and sum(l.startswith("## 58. Fable 14a und 14b") for l in z) == 1, "Register: 58 genau einmal, 59 noch nicht")
    p(reg.count(R81D) == 1, "Register: Voraussetzung R81 (d) genau einmal (Z. %s)" % [i + 1 for i, l in enumerate(z) if R81D in l])
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    e = lies(ERG); ez = e.split("\n")
    p(md5(e) == ERG_MD5, "ERGEBNIS_TB-162 md5 %s" % ERG_MD5)
    p(ez[196].startswith("## Vorschlag Tatsachennotiz") and ez[198].startswith("> **Tatsachennotiz zu 24.2") and ez[232] == "" and ez[233] == "## Abweichungen" and all(l.startswith(">") for l in ez[198:232]),
      "ERGEBNIS_TB-162: Notiz Z. 199-232 (Z. 197 Kopf, Z. 233 leer, Z. 234 Abweichungen)")
    p(git("log", "--format=%h", "-1", "--", ERG).strip()[:7] == ERG_COMMIT, "ERGEBNIS_TB-162 zuletzt in Commit %s" % ERG_COMMIT)
    for b in ALT: p(neu_text(b, lies(opt(b))) is not None, "E-6 Anker in %s genau einmal (Datenuhr-Zeile, %s), horizontbeginn_ts noch nicht da" % (opt(b), DEF))
    ende()
def register(datum, s0, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    e = lies(ERG); notiz = e.split("\n")[198:232]; z = lies(REG).split("\n")
    p(md5(e) == ERG_MD5 and len(notiz) == 34, "Quelle ERGEBNIS_TB-162 md5 %s, 34 Zeilen" % ERG_MD5)
    p(not any(l.startswith("## 59. ") for l in z), "59 noch nicht im Register"); p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    kopf = ("Reines Eintragen einer Tatsachennotiz, Bauart 24.6 (Betreiberkarte 15.10.2026, 18:17: „Tatsachennotiz TB-162 ins Register, als Schritt im nächsten Mac-Auftrag“; Entscheid F2 des steuernden Chats vom 15.10.2026, 18:25). "
            "Quelle ist allein `%s`, md5 `%s`, %s B, Z. 199–232 (Abschnitt „Vorschlag Tatsachennotiz“), im Repo seit Commit `%s`; zeichengleich übernommen. "
            "Eingetragen am %s mit TB-163 (Stand `%s`). Nichts entfernt, kein bestehender Satz umgeschrieben; keine Marke (R96 (d) führt 24.x ohne Marke).") % (
            ERG, ERG_MD5, format(len(e.encode("utf-8")), ",").replace(",", " "), ERG_COMMIT, datum, s0)
    neu = ["", TITEL59, "", kopf, "", "### 59.1 Tatsachennotiz (zeichengleich aus ERGEBNIS_TB-162 Z. 199–232)", ""] + notiz + [""]
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL59 + "\n") == 1, "nachher: altes Register unverändert vorn (append-only), 59 genau einmal, Z. %d" % (r2.split("\n").index(TITEL59) + 1))
    p("\n".join(notiz) in r2, "Notiz zeichengleich im Register")
    ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 59. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 59 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–58" in z[k[0]], "Kopf genau einmal, nennt 0–58"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–58", "Abschnitte 0–59")
    i = [j for j, l in enumerate(z) if l.startswith("| 58 aus 14a und 14b |")]
    if p(len(i) == 1, "Zeile 58 genau einmal"): z.insert(i[0] + 1, "| 59 Tatsachennotiz TB-162 | %s | 59.1 Tatsachennotiz zu 24.2, 24.3, R36 und 11.2 mit R43 (Kapital-Drawdown E und M je WF-Abschnitt; aus ERGEBNIS_TB-162 Z. 199–232) | – |" % T)
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-162 (")]
    if p(len(j) == 1, "Pflegezeile TB-162 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-162 (", "In TB-162 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-163 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-163 (`index`); 59 (Tatsachennotiz TB-162) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(IDX, "\n".join(z))
    ende()
def e6(probe):
    neu = {}
    for b in ALT:
        f = opt(b); t = lies(f); p(sha(f) == VOR[f], "vorher %s sha256 %s…" % (f, VOR[f][:16]))
        n = neu_text(b, t); p(n is not None, "%s: Anker genau einmal" % f)
        if n is not None:
            neu[f] = n; h = hashlib.sha256(n.encode("utf-8")).hexdigest()
            p(NACH is None or NACH.get(f) == h, "nachher %s sha256 %s (Soll aus dem Bau)" % (f, h))
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    for f, n in neu.items(): schreibe(f, n)
    for f in neu: p(sha(f) == (NACH or {}).get(f, sha(f)), "geschrieben %s sha256 %s" % (f, sha(f)))
    ende()
def r81d(beleg):
    t = lies(beleg).rstrip("\n").split("\n")
    p(t[-1] == "rc 0" and re.fullmatch(r"(\d+) von \1 Pruefungen bestanden", t[-2] or "") is not None, "Testbeleg %s: alle bestanden, rc 0 (%s)" % (beleg, t[-2][:60] if len(t) > 1 else "?"))
    for b in ALT:
        s = lies(opt(b))
        p(not re.search(r'\["open_time"\]\.max\(\)\s*-\s*pd\.DateOffset', s), "%s: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)" % b)
        p(len(re.findall(r'^\s+(entry_)?cutoff = horizontbeginn_ts\(df\["open_time"\]\)', s, re.M)) == 1 and ('faltenplan.horizontbeginn("%s")' % b) in s, "%s: Fenster aus faltenplan.horizontbeginn(\"%s\")" % (b, b))
    s = lies(opt("elliott_wave_stocks")); p('df = df[df["open_time"] >= cutoff].reset_index(drop=True)' in s, "elliott_wave_stocks: Anfang der geladenen Zeilen = Horizontbeginn (Kappung an cutoff)")
    p(sha(BB) == VOR[BB] and "start_i = max(start_i, int((df[\"open_time\"] < entry_cutoff).sum()))" in lies(BB), "volatility_breakout: Scanbeginn folgt entry_cutoff (backtest_breakout.py unverändert)")
    p(sha(FP) == VOR[FP], "faltenplan.py unverändert")
    n = sum(l.startswith("NEIN") for l in OUT)
    OUT.append("R81 (d) Voraussetzung: %s" % ("erfuellt (Fenster, Scanbeginn, Anfang der geladenen Zeilen ohne Dateiende)" if n == 0 else "NICHT erfuellt"))
    OUT.append("INFO Befund (kein Teil von R81 (d)): die Aufnahme eines Symbols (timespan_days = max - min gegen MIN_HISTORY_DAYS) haengt weiter vom Dateiende ab; buy_and_hold_benchmark.py der drei Bots rsi2, turtle, vb bildet cutoff weiter aus .max() (nicht E-6)")
    ende()
def uebergang(e):
    if not re.fullmatch(r"[0-9a-f]{7}", e): sys.exit(2)
    zl = ["**Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“) — Entwurf, nicht eingetragen; volle Hashes (39.5):", "",
          "| Datei | vorher | nachher | Commit | vollzieht |", "|---|---|---|---|---|"]
    for b in ALT: zl.append("| `%s` | `%s` | `%s` | `%s` | E-6 (Posten 4; R44, R81 (d)) |" % (opt(b), VOR[opt(b)], sha(opt(b)), e))
    zl += ["", "Neu (kein Vorher), Commit `%s`: `research/posten4_horizont/test_posten4_horizont.py` `%s`." % (e, sha("research/posten4_horizont/test_posten4_horizont.py")),
           "Unverändert: `%s` `%s`, `%s` `%s`." % (FP, sha(FP), BB, sha(BB))]
    print("\n".join(zl))
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n")
    a = [i for i, l in enumerate(z) if l.startswith("| **1** | **TB-30b Mass-Reparatur**")]
    if p(len(a) == 1 and z[a[0]].endswith("| zu formulieren |"), "BACKLOG Rang 1 genau einmal, Stand 'zu formulieren'"):
        z[a[0]] = z[a[0]][:-2] + " · Posten 4 (E-6, Horizont je Bot) erledigt mit TB-163 (%s, Journal %s) |" % (datum, kenn)
    s = "- **Vor der Neuerzeugung der Listen:** Posten 4, das Fenster je Bot aus dem Register (R81 (d); 55.8 Nr. 3)."
    b = [i for i, l in enumerate(z) if l.startswith(s)]
    if p(len(b) == 1, "BACKLOG-Zeile 'Vor der Neuerzeugung der Listen' genau einmal"):
        z[b[0]] = s + " ✅ Erledigt mit TB-163 (%s): Horizont aus `faltenplan.HORIZONTBEGINN` in den vier Aktien-Optimierern; R81 (d) gemessen (`docs/belege/TB-163/e_r81d.txt`)." % datum + z[b[0]][len(s):]
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(BL, "\n".join(z))
    ende()
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); print("Kennung %s%s (letzte %s)" % (h[0], chr(ord(h[1]) + 1), h))
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); neu = h[0] + chr(ord(h[1]) + 1)
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-163: " % neu), "Kopfzeile ## %s — TB-163: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(i and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile 'Was gemessen ist', 'In einfacher Sprache'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 3 and a[0] == "register": register(a[1], a[2], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif a == ["e6"]: e6(pr)
    elif len(a) == 2 and a[0] == "r81d": r81d(a[1])
    elif len(a) == 2 and a[0] == "uebergang": uebergang(a[1])
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
```
