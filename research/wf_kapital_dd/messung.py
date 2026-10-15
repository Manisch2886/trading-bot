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
