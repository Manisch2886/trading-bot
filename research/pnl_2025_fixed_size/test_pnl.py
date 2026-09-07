"""
Selbsttests der 2025er-Auswertung
====================================================================
Prueft die Behauptungen, auf denen die Tabelle steht - jede einzeln,
mit Abbruch beim ersten Fehlschlag. Laeuft ohne Bot-Import, nur auf
den erzeugten Ergebnisdateien plus einem Blick in die
live_params.py-Dateien; kann deshalb fuer alle Bots in einem Prozess
laufen.

Nutzung:  python3 test_pnl.py
"""

import ast
import json
import os
import subprocess

import pandas as pd

import konfiguration as cfg

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(DIR))
RESULTS_DIR = os.path.join(DIR, "results")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


def live_params_werte(bot: str) -> dict:
    """Liest live_params.py rein statisch aus - kein Import, kein
    Ausfuehren von Bot-Code."""
    pfad = os.path.join(REPO_ROOT, "strategies", bot, "live_params.py")
    baum = ast.parse(open(pfad).read())
    werte = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and len(knoten.targets) == 1:
            ziel = knoten.targets[0]
            if isinstance(ziel, ast.Name):
                try:
                    werte[ziel.id] = ast.literal_eval(knoten.value)
                except ValueError:
                    pass
    return werte


def main():
    print("Selbsttests der 2025er-P&L-Auswertung\n")
    zeilen = {}
    for schluessel in cfg.REIHENFOLGE:
        pfad = os.path.join(RESULTS_DIR, f"{schluessel}_pnl.json")
        check(f"Ergebnisdatei vorhanden: {schluessel}", os.path.exists(pfad))
        with open(pfad) as fh:
            zeilen[schluessel] = json.load(fh)

    check("alle neun Bots sind vertreten",
          len({z["bot"] for z in zeilen.values()}) == 9,
          str(sorted({z["bot"] for z in zeilen.values()})))

    # --- Parameter stimmen mit live_params.py ueberein ---------------
    for schluessel, eintrag in cfg.STANDARD.items():
        lp = live_params_werte(schluessel)
        verwendet = zeilen[schluessel]["verwendete_parameter"]
        for arg, lp_name in eintrag["kwargs"].items():
            soll, ist = lp[lp_name], verwendet[arg]
            check(f"{schluessel}: {arg} kommt aus live_params.{lp_name}",
                  str(soll) == str(ist), f"live={soll!r}, verwendet={ist!r}")
        check(f"{schluessel}: Positionslimit aus live_params",
              str(lp.get(eintrag["limit"])) == str(zeilen[schluessel]["positionslimit_live"]),
              f"live={lp.get(eintrag['limit'])!r}, "
              f"verwendet={zeilen[schluessel]['positionslimit_live']!r}")

    lp_stocks = live_params_werte("elliott_wave_stocks")
    verwendet = zeilen["elliott_wave_stocks"]["verwendete_parameter"]
    check("elliott_wave_stocks: unveraenderte Live-Konfiguration verwendet",
          (float(verwendet["deviation_pct"]) == float(lp_stocks["DEVIATION_PCT"])
           and float(verwendet["stop_loss_pct"]) == float(lp_stocks["STOP_LOSS_PCT"])
           and bool(verwendet["use_take_profit"]) == bool(lp_stocks["USE_TAKE_PROFIT"])),
          str(verwendet))

    for schluessel in ("elliott_wave_alt", "elliott_wave_neu"):
        soll = cfg.ELLIOTT[schluessel]["kwargs"]
        ist = zeilen[schluessel]["verwendete_parameter"]
        check(f"{schluessel}: fest gesetzte Parameter",
              all(float(ist[k]) == float(v) for k, v in soll.items()), str(ist))
    check("die beiden Elliott-Krypto-Staende unterscheiden sich",
          zeilen["elliott_wave_alt"]["verwendete_parameter"]
          != zeilen["elliott_wave_neu"]["verwendete_parameter"])

    # --- Sync-Konstanten ---------------------------------------------
    abweichungen = [(s, k) for s, z in zeilen.items()
                    for k in z["konstanten_angeglichen"] if k["abweichung"]]
    check("Sync-Abgleich der Modulkonstanten protokolliert",
          all("konstanten_angeglichen" in z for z in zeilen.values()),
          f"{len(abweichungen)} Abweichung(en) gefunden"
          + ("" if not abweichungen else f": {abweichungen}"))

    # --- BTC-Regimefilter --------------------------------------------
    vbc = zeilen["volatility_breakout_crypto"]
    check("volatility_breakout_crypto: BTC-Regimefilter nachgezogen",
          vbc["regimefilter"] is not None and vbc["regimefilter"]["live_aktiv"]
          and vbc["regimefilter"]["geblockt"] > 0,
          str(vbc["regimefilter"]))
    check("t3_supertrend: Regimefilter NICHT doppelt angewendet",
          zeilen["t3_supertrend"]["regimefilter"] is None,
          "collect_all_trades des Bots filtert dort bereits selbst")

    # --- Die Rechnung -------------------------------------------------
    for schluessel, z in zeilen.items():
        if not z["trades_2025"]:
            continue
        pfad = os.path.join(RESULTS_DIR, z["trades_datei"])
        df = pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])
        check(f"{schluessel}: Zeilenzahl der CSV passt zur Kennzahl",
              len(df) == z["trades_2025"], f"{len(df)} vs {z['trades_2025']}")
        check(f"{schluessel}: nur Einstiege im Jahr {cfg.JAHR}",
              bool((df["entry_time"].dt.year == cfg.JAHR).all()),
              f"{df['entry_time'].min()} .. {df['entry_time'].max()}")
        nach = cfg.POSITIONSGROESSE_USD * (df["exit_price"] - df["entry_price"]) / df["entry_price"]
        check(f"{schluessel}: P&L exakt 1000 x (exit-entry)/entry",
              abs(float(nach.sum()) - z["pnl_usd"]) < 0.01,
              f"nachgerechnet {nach.sum():.2f}, berichtet {z['pnl_usd']:.2f}")
        check(f"{schluessel}: keine fehlenden Kurse in der Auswertung",
              not df[["entry_price", "exit_price"]].isna().any().any())
        quote = float((nach > 0).mean() * 100)
        check(f"{schluessel}: Gewinnrate nachgerechnet",
              abs(quote - z["gewinnrate_pct"]) < 0.05,
              f"{quote:.1f} % vs {z['gewinnrate_pct']} %")

    # --- Keine Live-Datei angefasst -----------------------------------
    diff = subprocess.run(["git", "-C", REPO_ROOT, "diff", "--stat", "HEAD", "--",
                            "strategies/"], capture_output=True, text=True)
    check("kein Bot-Code veraendert (git diff auf strategies/ ist leer)",
          diff.returncode == 0 and diff.stdout.strip() == "",
          diff.stdout.strip() or "leerer Diff")

    print(f"\n{sum(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
