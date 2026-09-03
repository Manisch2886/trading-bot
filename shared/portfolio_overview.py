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
- Liest bereits vorhandene Dateien (results/<bot>/equity_curve.csv bevorzugt,
  sonst Fallback auf die Live-DB paper_trading_<bot>.db)
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
import sqlite3
import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
RESULTS_DIR = os.path.join(BASE_DIR, "results", "portfolio_overview")

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10  # nur fuer den DB-Fallback (siehe build_capital_curve_from_db) -
                        # muss zum Konzept der jeweiligen equity_simulation.py passen

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


def load_trade_dates(sources: dict) -> pd.Series:
    """Rohe Trade-Exit-Termine (nicht forward-gefuellt) - Grundlage fuer die
    Mindestanzahl gemeinsamer Handelstage in Teil 3, analog zu
    rsi2_mean_reversion/correlation_robustness_check.py."""
    if sources.get("equity_csv"):
        df = pd.read_csv(sources["equity_csv"], parse_dates=["time"])
        return df["time"].dt.normalize()
    if sources.get("db_file"):
        conn = sqlite3.connect(sources["db_file"])
        try:
            closed = pd.read_sql(
                "SELECT exit_time FROM trades WHERE status='closed' AND exit_time IS NOT NULL", conn)
        finally:
            conn.close()
        if closed.empty:
            return pd.Series(dtype="datetime64[ns]")
        return pd.to_datetime(closed["exit_time"]).dt.normalize()
    return pd.Series(dtype="datetime64[ns]")


def build_capital_curve_from_csv(csv_path: str) -> pd.Series:
    """Bevorzugte Quelle: equity_curve.csv aus der jeweiligen
    equity_simulation.py des Bots (bereits mit Positionslimit/Allokation
    simuliert, wie im Backtest validiert)."""
    df = pd.read_csv(csv_path, parse_dates=["time"]).sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = STARTING_CAPITAL
    return daily_last


def build_capital_curve_from_db(db_file: str) -> pd.Series:
    """Fallback, falls (noch) kein equity_curve.csv vorliegt: rekonstruiert
    eine VEREINFACHTE Kapitalkurve direkt aus den geschlossenen Live-Trades.
    WICHTIG - Naeherung: Die Live-DBs tracken kein echtes Kapital/keine
    Positionsgroessen (siehe Architektur-Diskussion), daher wird hier
    ersatzweise sequentiell mit fester ALLOCATION_PCT pro Trade gerechnet,
    OHNE Beruecksichtigung von echter Nebenlaeufigkeit/Positionslimit -
    weniger praezise als die CSV-Quelle, aber besser als der Bot fehlt
    komplett in der Uebersicht."""
    conn = sqlite3.connect(db_file)
    try:
        closed = pd.read_sql(
            "SELECT exit_time, pnl_pct FROM trades WHERE status='closed' AND exit_time IS NOT NULL "
            "ORDER BY exit_time", conn)
    finally:
        conn.close()

    if closed.empty:
        return pd.Series(dtype=float)

    closed["exit_time"] = pd.to_datetime(closed["exit_time"])
    capital = STARTING_CAPITAL
    records = []
    for _, row in closed.iterrows():
        allocation = capital * ALLOCATION_PCT
        capital += allocation * (row["pnl_pct"] / 100)
        records.append((row["exit_time"].normalize(), capital))

    series = pd.Series(dict(records)).sort_index()
    series = series[~series.index.duplicated(keep="last")]
    full_range = pd.date_range(series.index.min(), series.index.max(), freq="D")
    series = series.reindex(full_range).ffill()
    if pd.isna(series.iloc[0]):
        series.iloc[0] = STARTING_CAPITAL
    return series


def load_all_curves(bots: dict) -> dict:
    curves = {}
    for name, sources in bots.items():
        try:
            if sources["equity_csv"] is not None:
                series = build_capital_curve_from_csv(sources["equity_csv"])
                source_label = "equity_curve.csv (Backtest-Simulation)"
            elif sources["db_file"] is not None:
                series = build_capital_curve_from_db(sources["db_file"])
                source_label = "Live-DB (vereinfacht rekonstruiert)"
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
