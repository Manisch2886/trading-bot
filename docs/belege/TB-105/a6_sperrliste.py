"""TB-105 A6 - Sperrlistenpruefung der freigegebenen Dateien (Bauart TB-104 a8_sperrliste.py). Rein lesend.
Aufruf aus der Repo-Wurzel: trading-env/bin/python3 docs/belege/TB-105/a6_sperrliste.py
Gesucht wird je Datei nach dem Pfad UND nach dem Dateinamen (Dateinamen wie equity_simulation.py sind neunfach)."""
import json, os, re, sys
from datetime import datetime
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
ABBILD = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-25.json"
FREI = """strategies/t3_supertrend/equity_simulation.py strategies/t3_supertrend/multi_symbol_optimise.py strategies/volatility_breakout_crypto/equity_simulation.py strategies/elliott_wave/equity_simulation.py strategies/rsi2_crypto/equity_simulation.py strategies/turtle_soup_crypto/equity_simulation.py strategies/elliott_wave_stocks/equity_simulation.py strategies/rsi2_mean_reversion/equity_simulation.py strategies/turtle_soup_stocks/equity_simulation.py strategies/volatility_breakout/equity_simulation.py strategies/elliott_wave/multi_symbol_optimise.py strategies/elliott_wave_stocks/multi_symbol_optimise.py strategies/rsi2_mean_reversion/multi_symbol_optimise.py strategies/volatility_breakout/multi_symbol_optimise.py shared/symbols_config.py notifications/manual_close.py shared/strategy_paths.py research/exposure_messung/bot_lauf.py""".split()
zeilen = open(REG, encoding="utf-8").read().splitlines()
start = next(i for i, z in enumerate(zeilen) if z.startswith("## 10"))
ende = next(i for i in range(start + 1, len(zeilen)) if zeilen[i].startswith("## "))
abschnitt = zeilen[start:ende]
sys.path.insert(0, "research/vorregistrierung")
import herkunft as h
abbild_text = open(ABBILD, encoding="utf-8").read()
abbild = json.loads(abbild_text)
print("# TB-105 A6 - Sperrlistenpruefung, %s, HEAD %s" % (
    datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z"),
    os.popen("git rev-parse --short HEAD").read().strip()))
print("Register Abschnitt 10: Z. %d-%d" % (start + 1, ende))
namen_gesehen = set()
for d in FREI:
    name = os.path.basename(d)
    print("== %s" % d)
    for such in (d, name):
        treffer = [(start + 1 + i, z.strip()[:140]) for i, z in enumerate(abschnitt) if such in z]
        if such == name and name in namen_gesehen:
            print("   Abschnitt 10, Treffer '%s': %d (Zeilen wie oben)" % (such, len(treffer)))
            continue
        print("   Abschnitt 10, Treffer '%s': %d" % (such, len(treffer)))
        for nr, z in treffer:
            print("      Z. %d: %s" % (nr, z))
    namen_gesehen.add(name)
    for attr in ("SPERRLISTE_DATEIEN", "EINGEFROREN"):
        wert = getattr(h, attr, None)
        drin = None if wert is None else [str(x) for x in wert if name in str(x)]
        print("   herkunft.py::%s: %s" % (attr, drin if drin else (None if wert is None else "nein")))
    print("   Abbild %s, Treffer Pfad: %d, Treffer Name: %d" % (os.path.basename(ABBILD), abbild_text.count(d), abbild_text.count(name)))
# Punkt 11 woertlich
print("\n== Punkt 11, Wortlaut (Abschnitt 10)")
for i, z in enumerate(abschnitt):
    if re.match(r"\s*11\.", z) or "Commit-Hash" in z:
        print("   Z. %d: %s" % (start + 1 + i, z.rstrip()))
