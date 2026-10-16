"""TB-166 Vorab-Messung (S); Aufruf: python3 -B s0_vorab.py <ausgabe.json> (aus der Repo-Wurzel)
: Handelbar-Tag je Bot und Symbol, alte Rechnung
(ganze Datei, loader_lesart) gegen neue (nur Zeilen < Schnitt, Tag >= Schnitt -> None).
Eigenes Skript, stdlib, liest nur data/ und config/ des Repos."""
import datetime as dt, json, os, sys, hashlib
R = os.getcwd()  # Aufruf aus der Repo-Wurzel
SCHNITT = dt.date(2026, 9, 1)
BOTS = {"elliott_wave": ("krypto", "1h", "H", 17520), "t3_supertrend": ("krypto", "4h", "D", 730),
        "rsi2_crypto": ("krypto", "1d", "D", 500), "turtle_soup_crypto": ("krypto", "1d", "D", 500),
        "volatility_breakout_crypto": ("krypto", "1d", "D", 500), "elliott_wave_stocks": ("aktien", "1d", "D", 1825),
        "rsi2_mean_reversion": ("aktien", "1d", "D", 1825), "turtle_soup_stocks": ("aktien", "1d", "D", 1825),
        "volatility_breakout": ("aktien", "1d", "D", 1825)}
UNI = {"krypto": "config/top25_symbols.txt", "aktien": "config/sp500_top150.txt"}
def syms(m):
    l = [z.strip() for z in open(os.path.join(R, UNI[m])) if z.strip()]
    return [s for s in l if s not in ("XAUTUSDT", "PAXGUSDT")] if m == "krypto" else l
def tage(p):
    with open(p) as f:
        f.readline()
        for z in f:
            z = z.strip()
            if z: yield dt.date.fromisoformat(z.split(",")[0][:10])
aus = {}; flips = []; zeilen_ab = {}
for bot, (m, tf, art, n) in BOTS.items():
    aus[bot] = {}
    for s in syms(m):
        p = os.path.join(R, "data", f"{s}_{tf}.csv")
        if not os.path.exists(p): aus[bot][s] = {"alt": None, "neu": None, "datei": "fehlt"}; continue
        alle = list(tage(p)); vor = [t for t in alle if t < SCHNITT]
        zeilen_ab[f"{s}_{tf}"] = len(alle) - len(vor)
        if art == "H":
            alt = alle[n - 1] if len(alle) >= n else None
            neu = vor[n - 1] if len(vor) >= n else None
        else:
            alt = (alle[0] + dt.timedelta(days=n)) if alle else None
            neu = (vor[0] + dt.timedelta(days=n)) if vor else None
        if neu is not None and neu >= SCHNITT: neu = None
        a = alt.isoformat() if alt else None; b = neu.isoformat() if neu else None
        aus[bot][s] = {"alt": a, "neu": b}
        if a != b: flips.append((bot, s, a, b))
json.dump({"schnitt": str(SCHNITT), "je_bot": aus, "zeilen_ab_schnitt": zeilen_ab}, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print("Symbole je Bot:", {b: len(v) for b, v in aus.items()})
print("Dateien mit Zeilen ab Schnitt:", sum(1 for v in zeilen_ab.values() if v), "von", len(zeilen_ab), "max", max(zeilen_ab.values()))
print("Abweichungen alt/neu:", len(flips))
for f in flips: print("FLIP", *f)
alt_ab = [(b, s, v["alt"]) for b, d in aus.items() for s, v in d.items() if v["alt"] and v["alt"] >= str(SCHNITT)]
print("alte Rechnung >= Schnitt:", len(alt_ab))
