"""
Portfolio-Uebersicht ueber alle Bots (Beobachtungsebene, rein lesend)
==========================================================================
Ergebnis der Architektur-Entscheidung: Die Bots bleiben dauerhaft getrennt
(kein gemeinsames Kapitalkonto, kein zentrales Locking/Verguetungssystem
in shared/). Dieses Skript ersetzt das NICHT, sondern beobachtet nur: Es
rechnet eine HYPOTHETISCHE Gewichtung durch, um die Diversifikationswirkung
(siehe RSI-2-Prototyp-Analyse, Abschnitt 5/7 in
results/rsi2_mean_reversion/PROTOTYPE_FINDINGS.md) laufend im Blick zu
behalten - ohne eine einzige Zeile in einem der Bot-Ordner anzufassen.

Macht NUR:
- Liest bereits vorhandene Dateien: die Live-DB paper_trading_<bot>.db wird
  bevorzugt, SOBALD ein Bot mindestens MIN_LIVE_CLOSED_TRADES geschlossene
  Live-Trades hat - erst dann sagt die Kurve etwas ueber den tatsaechlichen
  Live-Betrieb aus, statt eine noch verrauschte Handvoll Trades zu zeigen.
  results/<bot>/equity_curve.csv (Backtest-Simulation) ist der Fallback fuer
  einen Bot, der diese Schwelle noch nicht erreicht (z.B. ein brandneuer,
  gerade erst aktivierter Bot). Sobald die Live-DB genutzt wird, laeuft
  dafuer die EIGENE, bereits validierte simulate_portfolio()-Funktion aus
  dem equity_simulation.py DIESES Bots (siehe
  build_capital_curve_from_live_trades) - inkl. echter Kapitalbindung bei
  gleichzeitig offenen Positionen und Positionslimit, mit den EIGENEN
  live_params.py-Werten (Allokation/Limit) des Bots, nicht einer fest
  codierten Naeherung. Frueher (bis inkl. der Version ohne diesen Hinweis)
  wurde equity_curve.csv IMMER bevorzugt, sobald es existierte - das machte
  die Live-DB faktisch zu totem Code, sobald ein Bot einmal ein
  Backtest-Ergebnis hatte (was nach der Validierung immer der Fall ist).
- Rechnet ZWEI getrennte, (konfigurierbar) gewichtete Portfolios durch:
  "Live-Portfolio" (nur Bots mit live_params.py, also tatsaechlich
  aktivierte/produktive Bots) und, falls vorhanden, zusaetzlich "Inkl.
  Prototypen" (alle gefundenen Bots, explizit als Forschungs-/
  Beobachtungswert gekennzeichnet - z.B. inkl. rsi2_mean_reversion, solange
  das noch kein live_params.py hat)
- Gibt Einzel- und kombinierte Drawdown-Kennzahlen je Gruppe aus
- Gibt je Bot-Paar eine Korrelationszahl aus, ABER NUR wenn mindestens
  MIN_COMMON_TRADING_DAYS gemeinsame Handelstage vorliegen - sonst
  ausdruecklich "zu wenig Datenbasis" statt einer moeglicherweise
  irrefuehrenden Zahl

Macht NICHT:
- Keine Schreibzugriffe auf eine der vier (kuenftig mehr) Bot-Datenbanken
  oder live_params.py-Dateien
- Keine echte Kapitalverwaltung/-teilung - reine Beobachtung

Bot-Erkennung ist AUTOMATISCH (scannt strategies/), nicht hart codiert -
ein neuer 5. Bot wird automatisch mit erfasst, sobald er entweder eine
Live-Datenbank oder ein Backtest-Equity-Curve-Ergebnis hat. Ein pausierter
oder noch nicht ausgefuehrter Bot wird sauber uebersprungen statt das
Skript abstuerzen zu lassen. Ob ein Bot als "live" oder "Prototyp" gilt,
wird an der bereits im Projekt etablierten Konvention festgemacht: Existenz
einer live_params.py im Strategie-Ordner.

Aufruf von ueberall im trading-bot-Ordner:
    python3 shared/portfolio_overview.py
"""

import os
import sys
import subprocess
import sqlite3
import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
RESULTS_DIR = os.path.join(BASE_DIR, "results", "portfolio_overview")

STARTING_CAPITAL = 10_000.0

MIN_LIVE_CLOSED_TRADES = 10  # Live-DB wird erst ab dieser Anzahl geschlossener
                              # Live-Trades als Quelle bevorzugt (siehe
                              # build_capital_curve_from_live_trades) - darunter
                              # waere die Kurve zu verrauscht, dann bleibt
                              # equity_curve.csv (falls vorhanden) die Quelle.

# Anzeige-Namen fuer bekannte Bots - ein unbekannter (kuenftiger) Ordnername
# faellt automatisch auf sich selbst zurueck, siehe display_name().
DISPLAY_NAMES = {
    "elliott_wave": "Elliott Wave (Krypto)",
    "t3_supertrend": "T3/SuperTrend (Krypto)",
    "elliott_wave_stocks": "Elliott Wave (Aktien)",
    "rsi2_mean_reversion": "RSI-2 Mean-Reversion (Aktien, Prototyp)",
}

# Gewichtung innerhalb jeder der beiden Gruppen (siehe run_analysis) - None/
# nicht gesetzt = automatisch gleichgewichtet. Um einzelne Bots anders zu
# gewichten, hier ueberschreiben, z.B. {"rsi2_mean_reversion": 0.10} - die
# restlichen Bots der jeweiligen Gruppe teilen sich dann automatisch den Rest
# gleichmaessig.
WEIGHT_OVERRIDES = {}

CORRELATION_ALERT_THRESHOLD = 0.3  # einfacher Schwellenwert, siehe Teil 3
MIN_COMMON_TRADING_DAYS = 30       # Mindestanzahl gemeinsamer Handelstage, bevor eine
                                    # Korrelationszahl fuer ein Bot-Paar ueberhaupt gezeigt wird

# Der Krypto-Elliott-Wave-Bot ("elliott_wave") legt sein Backtest-Ergebnis
# noch unter results/equity_curve.csv ab statt results/elliott_wave/
# equity_curve.csv wie die anderen Bots (Relikt aus der Zeit vor der
# strategy_paths.py-Konvention) - explizit hier vermerkt statt stillschweigend
# zu erraten. Ein neuer Bot braucht hier KEINEN Eintrag, solange er dem
# Standardpfad results/<name>/equity_curve.csv folgt.
LEGACY_EQUITY_CSV_PATHS = {
    "elliott_wave": os.path.join(BASE_DIR, "results", "equity_curve.csv"),
}


def display_name(bot_name: str) -> str:
    return DISPLAY_NAMES.get(bot_name, bot_name)


def discover_bots() -> dict:
    """Findet automatisch alle Bot-Ordner unter strategies/, die entweder
    eine Live-Datenbank oder ein Backtest-Equity-Curve-Ergebnis haben.
    Robust gegenueber kuenftigen (5., 6. ...) oder pausierten Bots - ein
    Ordner ohne beide Datenquellen wird einfach nicht aufgenommen.

    is_live: True, wenn der Bot eine live_params.py hat (= aktiviert,
    validiert, laeuft/liefe per Cronjob) - False fuer Prototypen wie
    rsi2_mean_reversion, die bewusst noch keine live_params.py haben.
    Dieselbe Konvention, die im Projekt ohnehin schon den Uebergang
    "Prototyp -> Live" markiert (siehe live_params.py-Muster im
    Uebergabeprotokoll)."""
    strategies_dir = os.path.join(BASE_DIR, "strategies")
    bots = {}
    if not os.path.isdir(strategies_dir):
        return bots

    for name in sorted(os.listdir(strategies_dir)):
        strategy_dir = os.path.join(strategies_dir, name)
        if not os.path.isdir(strategy_dir):
            continue
        equity_csv = os.path.join(BASE_DIR, "results", name, "equity_curve.csv")
        if not os.path.exists(equity_csv) and name in LEGACY_EQUITY_CSV_PATHS:
            equity_csv = LEGACY_EQUITY_CSV_PATHS[name]
        db_file = os.path.join(BASE_DIR, f"paper_trading_{name}.db")

        has_csv = os.path.exists(equity_csv)
        has_db = os.path.exists(db_file)
        if not has_csv and not has_db:
            continue

        bots[name] = {
            "equity_csv": equity_csv if has_csv else None,
            "db_file": db_file if has_db else None,
            "is_live": os.path.exists(os.path.join(strategy_dir, "live_params.py")),
        }
    return bots


def _load_db_exit_dates(db_file: str) -> pd.Series:
    conn = sqlite3.connect(db_file)
    try:
        closed = pd.read_sql(
            "SELECT exit_time FROM trades WHERE status='closed' AND exit_time IS NOT NULL", conn)
    finally:
        conn.close()
    if closed.empty:
        return pd.Series(dtype="datetime64[ns]")
    return pd.to_datetime(closed["exit_time"]).dt.normalize()


def count_live_closed_trades(db_file) -> int:
    """Anzahl geschlossener Live-Trades - Grundlage fuer die
    MIN_LIVE_CLOSED_TRADES-Entscheidung in load_all_curves(). 0, falls
    keine Live-DB vorhanden ist (z.B. brandneuer Bot vor dem ersten
    forward_test.py-Lauf)."""
    if not db_file:
        return 0
    return len(_load_db_exit_dates(db_file))


def load_trade_dates(sources: dict) -> pd.Series:
    """Rohe Trade-Exit-Termine (nicht forward-gefuellt) - Grundlage fuer die
    Mindestanzahl gemeinsamer Handelstage in Teil 3, analog zu
    rsi2_mean_reversion/correlation_robustness_check.py. Nutzt DIESELBE
    Quelle wie die Kapitalkurve dieses Bots (sources['using_live_data'],
    von load_all_curves() gesetzt) - sonst koennten Kurve und
    Handelstage-Zaehlung aus unterschiedlichen Datenquellen stammen."""
    if sources.get("using_live_data") and sources.get("db_file"):
        return _load_db_exit_dates(sources["db_file"])
    if sources.get("equity_csv"):
        df = pd.read_csv(sources["equity_csv"], parse_dates=["time"])
        return df["time"].dt.normalize()
    if sources.get("db_file"):
        return _load_db_exit_dates(sources["db_file"])
    return pd.Series(dtype="datetime64[ns]")


def _daily_capital_curve_from_equity_df(equity_df: pd.DataFrame) -> pd.Series:
    df = equity_df.sort_values("time").copy()
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = STARTING_CAPITAL
    return daily_last


def build_capital_curve_from_csv(csv_path: str) -> pd.Series:
    """Fallback-Quelle: equity_curve.csv aus der jeweiligen
    equity_simulation.py des Bots (Backtest-Simulation) - wird genutzt,
    solange die Live-DB dieses Bots noch unter MIN_LIVE_CLOSED_TRADES
    liegt (siehe load_all_curves)."""
    df = pd.read_csv(csv_path, parse_dates=["time"])
    return _daily_capital_curve_from_equity_df(df)


def load_live_trades(db_file: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_file)
    try:
        trades = pd.read_sql(
            "SELECT symbol, entry_time, exit_time, pnl_pct FROM trades "
            "WHERE status='closed' AND exit_time IS NOT NULL", conn)
    finally:
        conn.close()
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time"] = pd.to_datetime(trades["exit_time"])
    return trades


def build_capital_curve_from_live_trades(strategy_dir: str, live_trades: pd.DataFrame) -> pd.Series:
    """Bevorzugte Quelle, sobald genug Live-Trades vorliegen (siehe
    MIN_LIVE_CLOSED_TRADES): wendet die EIGENE, bereits validierte
    simulate_portfolio()-Funktion DIESES Bots (aus dessen
    equity_simulation.py) auf dessen echte Live-Trades an - inkl.
    Kapitalbindung bei gleichzeitig offenen Positionen und Positionslimit,
    exakt wie im Backtest. Nutzt dabei auch die EIGENEN live_params.py-Werte
    (Allokation, Limit) des Bots statt einer fest codierten Naeherung.

    Laeuft in einem EIGENEN Subprozess (siehe
    turtle_soup_stocks/experiment_volatility_breakout_overlap.py-Docstring
    fuer die ausfuehrliche Begruendung): sowohl equity_simulation.py als
    auch live_params.py heissen bei JEDEM Bot identisch - ein direkter
    Import mehrerer Bots im selben Python-Prozess wuerde denselben stillen
    sys.modules-Kollisions-Bug reproduzieren, der dort bereits einmal
    gefunden wurde (ein Bot bekommt lautlos die Funktionen/Werte eines
    ANDEREN Bots untergeschoben, ohne Fehlermeldung)."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tmp_trades_csv = os.path.join(RESULTS_DIR, "_live_trades_cache.csv")
    tmp_out_csv = os.path.join(RESULTS_DIR, "_live_equity_curve_cache.csv")
    live_trades.to_csv(tmp_trades_csv, index=False)

    script = f"""
import pandas as pd
from live_params import ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS
from equity_simulation import simulate_portfolio, STARTING_CAPITAL
trades = pd.read_csv({tmp_trades_csv!r}, parse_dates=["entry_time", "exit_time"])
result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT / 100, MAX_CONCURRENT_POSITIONS)
result["equity_curve"].to_csv({tmp_out_csv!r}, index=False)
"""
    result = subprocess.run([sys.executable, "-c", script], cwd=strategy_dir,
                             capture_output=True, text=True)
    os.remove(tmp_trades_csv)
    if result.returncode != 0:
        raise RuntimeError(f"Live-Equity-Subprozess fuer {strategy_dir} fehlgeschlagen:\n{result.stderr}")

    equity_df = pd.read_csv(tmp_out_csv, parse_dates=["time"])
    os.remove(tmp_out_csv)
    if equity_df.empty:
        return pd.Series(dtype=float)
    return _daily_capital_curve_from_equity_df(equity_df)


def load_all_curves(bots: dict) -> dict:
    """Entscheidet PRO BOT die Datenquelle und laedt die Kapitalkurve.
    Setzt zusaetzlich sources['using_live_data']/sources['live_closed_trades']
    direkt in bots[name] (Mutation in-place - bots ist dasselbe dict-Objekt,
    das run_analysis()/load_trade_dates() spaeter erneut nutzen), damit die
    Korrelations-Handelstage-Zaehlung in Teil 3 dieselbe Quelle wie die
    Kurve verwendet."""
    curves = {}
    for name, sources in bots.items():
        try:
            live_trade_count = count_live_closed_trades(sources["db_file"])
            sources["live_closed_trades"] = live_trade_count
            use_live = live_trade_count >= MIN_LIVE_CLOSED_TRADES and sources["db_file"] is not None
            sources["using_live_data"] = use_live

            if use_live:
                strategy_dir = os.path.join(BASE_DIR, "strategies", name)
                live_trades = load_live_trades(sources["db_file"])
                series = build_capital_curve_from_live_trades(strategy_dir, live_trades)
                source_label = (f"Live-DB ({live_trade_count} geschlossene Live-Trades, "
                                 f"eigene Allokation/Limit aus live_params.py)")
            elif sources["equity_csv"] is not None:
                series = build_capital_curve_from_csv(sources["equity_csv"])
                if live_trade_count > 0:
                    source_label = (f"equity_curve.csv (Backtest-Fallback, Live-DB noch zu duenn: "
                                     f"{live_trade_count}/{MIN_LIVE_CLOSED_TRADES} Trades)")
                else:
                    source_label = "equity_curve.csv (Backtest-Simulation, noch keine geschlossenen Live-Trades)"
            elif sources["db_file"] is not None:
                print(f"  Hinweis: {display_name(name)} uebersprungen (nur {live_trade_count} "
                      f"geschlossene Live-Trades, unter Schwelle {MIN_LIVE_CLOSED_TRADES}, "
                      f"kein Backtest-equity_curve.csv als Fallback vorhanden)")
                continue
            else:
                continue
        except Exception as e:
            print(f"  Warnung: {display_name(name)} uebersprungen (Lesefehler: {e})")
            continue

        if series.empty:
            print(f"  Warnung: {display_name(name)} uebersprungen (keine Trades vorhanden)")
            continue

        curves[name] = {"series": series, "source": source_label}
    return curves


def resolve_weights(bot_names: list) -> dict:
    n = len(bot_names)
    if n == 0:
        return {}
    overridden = {b: w for b, w in WEIGHT_OVERRIDES.items() if b in bot_names}
    remaining = [b for b in bot_names if b not in overridden]
    remaining_weight = 1.0 - sum(overridden.values())
    weights = dict(overridden)
    if remaining:
        each = max(remaining_weight, 0) / len(remaining)
        for b in remaining:
            weights[b] = each
    return weights


def max_drawdown_pct(normalised_series: pd.Series) -> float:
    running_max = normalised_series.cummax()
    return round(((normalised_series - running_max) / running_max * 100).min(), 2)


def run_analysis(bots: dict, curves: dict, group_label: str, output_suffix: str):
    """Fuehrt Teil 1-3 (Einzel-Drawdowns, kombiniertes Portfolio,
    Korrelations-Hinweis) fuer eine Teilmenge von Bots aus. bots: das volle
    discover_bots()-Ergebnis (fuer load_trade_dates); curves: bereits
    geladene Kapitalkurven, NUR fuer die Bots dieser Gruppe."""
    print("\n" + "#" * 70)
    print(f"# {group_label}")
    print("#" * 70)

    if len(curves) < 2:
        print(f"Weniger als 2 Bots mit verwertbaren Daten in dieser Gruppe "
              f"({', '.join(display_name(n) for n in curves) or 'keine'}) - kein Vergleich moeglich.")
        return

    print("\nDatenquelle je Bot:")
    for name, data in curves.items():
        print(f"  {display_name(name)}: {data['source']} "
              f"({data['series'].index.min().date()} bis {data['series'].index.max().date()})")

    common_start = max(d["series"].index.min() for d in curves.values())
    common_end = min(d["series"].index.max() for d in curves.values())
    print(f"\nGemeinsames Vergleichsfenster: {common_start.date()} bis {common_end.date()}")

    if common_start >= common_end:
        print("Kein ausreichend gemeinsames Zeitfenster fuer einen Vergleich.")
        return

    date_range = pd.date_range(common_start, common_end, freq="D")
    filled = {name: d["series"].reindex(date_range).ffill().bfill() for name, d in curves.items()}
    normalised = pd.DataFrame({name: s / s.iloc[0] * 100 for name, s in filled.items()})

    weights = resolve_weights(list(curves.keys()))

    print("\n" + "=" * 70)
    print("TEIL 1: EINZEL-BOT-DRAWDOWNS IM GEMEINSAMEN FENSTER")
    print("=" * 70)
    rows = []
    for name in curves:
        dd = max_drawdown_pct(normalised[name])
        total_return = round((normalised[name].iloc[-1] / normalised[name].iloc[0] - 1) * 100, 2)
        rows.append({"bot": display_name(name), "gewicht": f"{weights[name]*100:.1f}%",
                      "rendite_pct": total_return, "max_drawdown_pct": dd})
    print(pd.DataFrame(rows).to_string(index=False))

    print("\n" + "=" * 70)
    print(f"TEIL 2: KOMBINIERTES PORTFOLIO (Gewichtung: "
          f"{', '.join(f'{display_name(n)}={weights[n]*100:.0f}%' for n in curves)})")
    print("=" * 70)
    portfolio = sum(normalised[name] * weights[name] for name in curves)
    portfolio_curve = portfolio / portfolio.iloc[0] * 100
    portfolio_dd = max_drawdown_pct(portfolio_curve)
    portfolio_return = round((portfolio_curve.iloc[-1] / portfolio_curve.iloc[0] - 1) * 100, 2)
    worst_individual = min(r["max_drawdown_pct"] for r in rows)

    print(f"  Rendite im Fenster:        {portfolio_return:.2f}%")
    print(f"  Max Drawdown kombiniert:   {portfolio_dd:.2f}%")
    print(f"  Schlechtester Einzel-Bot:  {worst_individual:.2f}%  "
          f"(zum Vergleich - je naeher kombiniert an 0 liegt, desto staerker die Diversifikation)")

    print("\n" + "=" * 70)
    print(f"TEIL 3: KORRELATIONS-HINWEIS je Bot-Paar "
          f"(Schwelle {CORRELATION_ALERT_THRESHOLD}, mind. {MIN_COMMON_TRADING_DAYS} gemeinsame Handelstage)")
    print("=" * 70)
    daily_returns = normalised.pct_change().dropna()
    corr = daily_returns.corr()

    trade_dates = {name: load_trade_dates(bots[name]) for name in curves}
    any_alert = False
    bot_list = list(curves.keys())
    for i in range(len(bot_list)):
        for j in range(i + 1, len(bot_list)):
            a, b = bot_list[i], bot_list[j]
            dates_a = trade_dates[a]
            dates_b = trade_dates[b]
            active_a = date_range.isin(dates_a[(dates_a >= common_start) & (dates_a <= common_end)])
            active_b = date_range.isin(dates_b[(dates_b >= common_start) & (dates_b <= common_end)])
            common_active_days = int((active_a & active_b).sum())

            label = f"  {display_name(a)} <-> {display_name(b)}"
            if common_active_days < MIN_COMMON_TRADING_DAYS:
                print(f"{label}: zu wenig Datenbasis fuer belastbare Korrelationsaussage "
                      f"(nur {common_active_days} gemeinsame Handelstage, mind. {MIN_COMMON_TRADING_DAYS} noetig)")
                continue

            value = corr.loc[a, b]
            flag = ""
            if abs(value) >= CORRELATION_ALERT_THRESHOLD:
                flag = "  ⚠ ueber Schwelle"
                any_alert = True
            print(f"{label}: {value:.2f}  ({common_active_days} gemeinsame Handelstage){flag}")

    if any_alert:
        print("\n  Hinweis: Ein Wert ueber der Schwelle ist ein frueher Hinweis, kein endgueltiger")
        print("  Beweis fuer echte Kopplung - insbesondere bei wenigen gemeinsamen Handelstagen")
        print("  nahe der Mindestgrenze mit Vorsicht interpretieren.")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = normalised.copy()
    output["Portfolio (gewichtet)"] = portfolio_curve
    output_path = os.path.join(RESULTS_DIR, f"portfolio_overview_curve_{output_suffix}.csv")
    output.to_csv(output_path)
    print(f"\nNormierte Kurven gespeichert unter: {output_path}")


def main():
    print("=" * 70)
    print("PORTFOLIO-UEBERSICHT (Beobachtungsebene)")
    print("=" * 70)

    bots = discover_bots()
    if not bots:
        print("Keine Bots mit Ergebnisdaten gefunden.")
        return

    print(f"\nGefundene Bots: {', '.join(display_name(b) for b in bots)}")
    print("  davon aktiviert/live: " +
          (', '.join(display_name(b) for b, d in bots.items() if d["is_live"]) or "keine"))
    print("  davon Prototyp (kein live_params.py): " +
          (', '.join(display_name(b) for b, d in bots.items() if not d["is_live"]) or "keine"))

    curves = load_all_curves(bots)

    live_curves = {n: c for n, c in curves.items() if bots[n]["is_live"]}
    run_analysis(bots, live_curves, "LIVE-PORTFOLIO (nur aktivierte Bots)", "live")

    if len(curves) > len(live_curves):
        run_analysis(bots, curves,
                     "INKL. PROTOTYPEN (Forschungs-/Beobachtungswert, kein gleichwertiger Live-Partner)",
                     "inkl_prototypen")


if __name__ == "__main__":
    main()
