"""
Frage 2: belegen statt vermuten - laesst sich die gespeicherte
Ergebnisdatei des Bots heute Zeile fuer Zeile wiederfinden?
====================================================================
Aufruf:  python3 historie.py <bot> [--ohne-regimefilter]

Jeder Bot hat eine gespeicherte Rasterausgabe
(`results/<bot>/multi_symbol_optimisation_results.csv`, beim
Krypto-Elliott-Bot `results/multi_symbol_optimisation_results.csv`).
Das ist die Datei, auf die sich die Prototyp-Berichte und die
`live_params.py`-Kommentare berufen. Dieses Skript stellt sie Zeile
fuer Zeile gegen die heute nachgerechneten Werte aus
`results/<bot>[...]_raster.csv`.

Trifft sie, ist belegt (nicht vermutet), dass die Parameterwahl dieses
Bots ueber `multi_symbol_optimise` und ueber genau den Drawdown auf der
Symbol-Blockreihenfolge gelaufen ist. Trifft sie nicht, sagt das
Skript, welche Spalte abweicht - und dann ist der Bot-Code oder die
Datenbasis seither veraendert worden und die Datei taugt nicht als
Beleg.

Dieses Skript LIEST die Bot-Ergebnisdatei. Es schreibt sie nicht.
"""

import os
import sys

import pandas as pd

import botenv

# Spalten, ueber die die historische Zeile eindeutig identifiziert ist
SCHLUESSEL = {
    "elliott_wave": ["deviation_pct", "stop_loss_pct", "take_profit_fib"],
    "elliott_wave_stocks": ["deviation_pct", "stop_loss_pct", "take_profit_fib",
                            "use_take_profit"],
    "t3_supertrend": ["t3_fast", "t3_slow", "adx_threshold", "stop_loss_pct"],
    "rsi2_crypto": ["sma_trend_period", "rsi_threshold", "stop_loss_pct"],
    "rsi2_mean_reversion": ["rsi_threshold", "stop_loss_pct"],
    "turtle_soup_crypto": ["donchian_period", "stop_mode"],
    "turtle_soup_stocks": ["donchian_period", "stop_mode"],
    "volatility_breakout": ["stop_loss_pct"],
    "volatility_breakout_crypto": ["stop_loss_pct"],
}

# alte Spalte -> neue Spalte
VERGLEICH = [
    ("num_trades", "num_trades"),
    ("num_symbols", "num_symbols"),
    ("win_rate", "win_rate"),
    ("total_return_pct", "total_return_pct"),
    ("avg_return_pct", "avg_return_pct"),
    ("max_drawdown_pct", "dd_block"),
    ("robustness_score", "score_block"),
]


def bot_csv(bot: str) -> str:
    """Der Krypto-Elliott-Bot ist der aelteste und schreibt noch in
    results/ direkt, nicht in results/<bot>/ - get_strategy_paths kam
    spaeter. Deshalb hier die Fallunterscheidung."""
    kandidaten = [
        os.path.join(botenv.REPO_ROOT, "results", bot, "multi_symbol_optimisation_results.csv"),
        os.path.join(botenv.REPO_ROOT, "results", "multi_symbol_optimisation_results.csv"),
    ]
    for p in kandidaten:
        if os.path.exists(p):
            return p
    return None


def main():
    botenv.print_hinweis()
    if len(sys.argv) < 2:
        raise SystemExit("Nutzung: python3 historie.py <bot> [--ohne-regimefilter]")
    bot = sys.argv[1]
    if bot not in SCHLUESSEL:
        raise SystemExit(f"Unbekannter Bot: {bot}")
    suffix = "_ohne_regimefilter" if "--ohne-regimefilter" in sys.argv else ""

    alt_pfad = bot_csv(bot)
    neu_pfad = os.path.join(botenv.RESULTS_DIR, f"{bot}{suffix}_raster.csv")
    if alt_pfad is None:
        print(f"Keine gespeicherte Ergebnisdatei fuer {bot} gefunden.")
        return
    if not os.path.exists(neu_pfad):
        raise SystemExit(f"{neu_pfad} fehlt - erst 'python3 analyse.py {bot}' laufen lassen.")

    alt = pd.read_csv(alt_pfad)
    neu = pd.read_csv(neu_pfad)
    neu = neu[neu["besteht_mindestfilter"] == True]

    k = SCHLUESSEL[bot]
    for spalte in k:
        for df in (alt, neu):
            if spalte in df.columns:
                # "kein Stop"/None/NaN vereinheitlichen, damit der Merge
                # nicht an der Schreibweise scheitert
                df[spalte] = df[spalte].astype(str)
    m = alt.merge(neu, on=k, suffixes=("_alt", "_neu"))

    print(f"\n=== {bot} ===")
    print(f"gespeichert: {os.path.relpath(alt_pfad, botenv.REPO_ROOT)}  ({len(alt)} Zeilen)")
    print(f"neu:         {os.path.relpath(neu_pfad, botenv.REPO_ROOT)}  "
          f"({len(neu)} Zeilen, die die Mindestfilter bestehen)")
    print(f"ueber {k} wiedergefunden: {len(m)} von {len(alt)}\n")

    alles = len(m) == len(alt)
    for a, b in VERGLEICH:
        sa = f"{a}_alt" if f"{a}_alt" in m.columns else a
        sb = f"{b}_neu" if f"{b}_neu" in m.columns else b
        if sa not in m.columns or sb not in m.columns:
            print(f"  {a:<20} -> {b:<16}  Spalte fehlt")
            continue
        gleich = int((m[sa] == m[sb]).sum())
        alles = alles and gleich == len(m)
        marke = "==" if gleich == len(m) else "!="
        print(f"  {a:<20} {marke} {b:<16}  {gleich}/{len(m)}")
        if gleich != len(m):
            ab = m[m[sa] != m[sb]]
            for _, r in ab.head(3).iterrows():
                print(f"        {[r[x] for x in k]}: {r[sa]} gegen {r[sb]}")

    print()
    if alles:
        print("-> BELEGT: die gespeicherte Rasterausgabe dieses Bots ist heute")
        print("   Zeile fuer Zeile reproduzierbar. Seine Parameterwahl ist ueber")
        print("   multi_symbol_optimise und den Drawdown auf der Symbol-Block-")
        print("   reihenfolge gelaufen.")
    else:
        print("-> NICHT reproduzierbar: Bot-Code oder Datenbasis haben sich")
        print("   seither veraendert. Die Datei taugt dann nicht als Beleg fuer")
        print("   die heutigen Zahlen - die Herkunft muss aus den Berichten und")
        print("   live_params.py-Kommentaren belegt werden.")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
