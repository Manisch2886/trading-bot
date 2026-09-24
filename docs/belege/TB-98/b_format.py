"""TB-98 B3, Ausgabeformat: schreibt die neue Schreibstelle (`_schreibe_einmal`
mit `to_csv(index=False)` bzw. `json.dumps(...)`) dasselbe Byte fuer Byte wie
die alte (`to_csv(pfad, index=False)` bzw. `json.dump(meta, f, ...)`)?

Da der Erzeuger heute nicht bis zur Schreibstelle kommt (Befund 2, a1), wird
die Schreibstelle allein geprueft: je Bot wird die alte `_alle_trades.csv` und
`_positionen.csv` mit den Typen des Erzeugers eingelesen (Zeiten als datetime,
`kerzen` als Int64, `ausgefuehrt` als bool) und in einen Scratchpad-Ordner
geschrieben - einmal auf dem alten Weg, einmal ueber `_schreibe_einmal`.
Verglichen wird (a) alt gegen neu und (b) neu gegen die Originaldatei.
`meta.json` ebenso (json.load -> alter/neuer Weg).

Nichts unter research/ wird geschrieben; `--ziel` zeigt in den Scratchpad.
Aufruf (Repo-Wurzel):  python3 b_format.py <leerer_scratch_ordner>
"""
import filecmp
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
ziel = os.path.abspath(sys.argv[1])
assert os.path.isdir(ziel) and not os.listdir(ziel), "leerer Ordner verlangt"
alt_dir = os.path.join(ziel, "alt")
neu_dir = os.path.join(ziel, "neu")
os.mkdir(alt_dir)
os.mkdir(neu_dir)
sys.argv = [os.path.join(_REPO, "research", "tb24_haltedauern", "positionen_holen.py"),
            "rsi2_crypto", "--ziel", neu_dir]
sys.path.insert(0, os.path.join(_REPO, "research", "tb24_haltedauern"))
import positionen_holen as ph   # noqa: E402
import pandas as pd              # noqa: E402

DATEN = os.path.join(_REPO, "research", "tb24_haltedauern", "daten")
BOTS = ["elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
        "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion",
        "turtle_soup_stocks", "volatility_breakout"]
gesamt = 0
for bot in BOTS:
    for art in ("alle_trades", "positionen"):
        name = f"{bot}_{art}.csv"
        orig = os.path.join(DATEN, name)
        df = pd.read_csv(orig, parse_dates=["entry_time", "exit_time"])
        if "kerzen" in df.columns:
            df["kerzen"] = df["kerzen"].astype("Int64")
        df.to_csv(os.path.join(alt_dir, name), index=False)          # alter Weg
        ph._schreibe_einmal(name, df.to_csv(index=False))             # neuer Weg
        a = filecmp.cmp(os.path.join(alt_dir, name), os.path.join(neu_dir, name), shallow=False)
        b = filecmp.cmp(orig, os.path.join(neu_dir, name), shallow=False)
        gesamt += a
        print(f"{name:45s} alt==neu {'JA  ' if a else 'NEIN'}  neu==Original {'JA' if b else 'NEIN'}")
    name = f"{bot}_meta.json"
    meta = json.load(open(os.path.join(DATEN, name)))
    with open(os.path.join(alt_dir, name), "w") as f:                 # alter Weg
        json.dump(meta, f, indent=2, default=str)
    ph._schreibe_einmal(name, json.dumps(meta, indent=2, default=str))  # neuer Weg
    a = filecmp.cmp(os.path.join(alt_dir, name), os.path.join(neu_dir, name), shallow=False)
    b = filecmp.cmp(os.path.join(DATEN, name), os.path.join(neu_dir, name), shallow=False)
    gesamt += a
    print(f"{name:45s} alt==neu {'JA  ' if a else 'NEIN'}  neu==Original {'JA' if b else 'NEIN'}")
print(f"\nalt==neu: {gesamt} von {3 * len(BOTS)}")
