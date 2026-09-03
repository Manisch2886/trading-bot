"""
Portfolio-Uebersicht ueber alle Bots (Beobachtungsebene, rein lesend)
==========================================================================
Ergebnis der Architektur-Entscheidung: Die Bots bleiben dauerhaft getrennt
(kein gemeinsames Kapitalkonto, kein zentrales Locking/Verguetungssystem
in shared/). Dieses Skript ersetzt das NICHT, sondern beobachtet nur: Es
rechnet eine HYPOTHETISCHE Gleichgewichtung aller Bots durch, um die
Diversifikationswirkung (siehe RSI-2-Prototyp-Analyse, Abschnitt 5/7 in
results/rsi2_mean_reversion/PROTOTYPE_FINDINGS.md) laufend im Blick zu
behalten - ohne eine einzige Zeile in einem der Bot-Ordner anzufassen.

Macht NUR:
- Liest bereits vorhandene Dateien (results/<bot>/equity_curve.csv bevorzugt,
  sonst Fallback auf die Live-DB paper_trading_<bot>.db)
- Rechnet eine (konfigurierbare) Portfolio-Gewichtung durch
- Gibt Einzel- und kombinierte Drawdown-Kennzahlen aus
- Warnt einfach, wenn zwei Bots ungewoehnlich stark korrelieren

Macht NICHT:
- Keine Schreibzugriffe auf eine der vier (kuenftig mehr) Bot-Datenbanken
  oder live_params.py-Dateien
- Keine echte Kapitalverwaltung/-teilung - reine Beobachtung

Bot-Erkennung ist AUTOMATISCH (scannt strategies/), nicht hart codiert -
ein neuer 5. Bot wird automatisch mit erfasst, sobald er entweder eine
Live-Datenbank oder ein Backtest-Equity-Curve-Ergebnis hat. Ein pausierter
oder noch nicht ausgefuehrter Bot wird sauber uebersprungen statt das
Skript abstuerzen zu lassen.

Aufruf von ueberall im trading-bot-Ordner:
    python3 shared/portfolio_overview.py

WICHTIG: Noch kein Cronjob dafuer eingerichtet (auf Wunsch) - erst
manuell ein paar Mal testen.
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

# Gewichtung im hypothetischen Vergleichsportfolio - None = automatisch
# gleichgewichtet ueber alle gefundenen, aktiven Bots. Um einzelne Bots
# anders zu gewichten (z.B. einen Prototyp niedriger), hier ueberschreiben,
# z.B. {"rsi2_mean_reversion": 0.10} - die restlichen Bots teilen sich dann
# automatisch den Rest gleichmaessig.
WEIGHT_OVERRIDES = {}

CORRELATION_ALERT_THRESHOLD = 0.3  # einfacher Schwellenwert, siehe Teil 3

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
    Ordner ohne beide Datenquellen wird einfach nicht aufgenommen."""
    strategies_dir = os.path.join(BASE_DIR, "strategies")
    bots = {}
    if not os.path.isdir(strategies_dir):
        return bots

    for name in sorted(os.listdir(strategies_dir)):
        if not os.path.isdir(os.path.join(strategies_dir, name)):
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
        }
    return bots


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


def main():
    print("=" * 70)
    print("PORTFOLIO-UEBERSICHT (Beobachtungsebene, hypothetische Gewichtung)")
    print("=" * 70)

    bots = discover_bots()
    if not bots:
        print("Keine Bots mit Ergebnisdaten gefunden.")
        return

    print(f"\nGefundene Bots: {', '.join(display_name(b) for b in bots)}\n")
    curves = load_all_curves(bots)

    if len(curves) < 2:
        print("Weniger als 2 Bots mit verwertbaren Daten - kein Portfolio-Vergleich moeglich.")
        return

    print("Datenquelle je Bot:")
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
    normalised = pd.DataFrame({
        name: d["series"].reindex(date_range).ffill().bfill() / d["series"].reindex(date_range).ffill().bfill().iloc[0] * 100
        for name, d in curves.items()
    })

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
    print(f"TEIL 3: KORRELATIONS-HINWEIS (Schwelle: {CORRELATION_ALERT_THRESHOLD})")
    print("=" * 70)
    daily_returns = normalised.pct_change().dropna()
    corr = daily_returns.corr()
    print(corr.round(2).to_string())

    alerts = []
    bot_list = list(curves.keys())
    for i in range(len(bot_list)):
        for j in range(i + 1, len(bot_list)):
            a, b = bot_list[i], bot_list[j]
            value = corr.loc[a, b]
            if abs(value) >= CORRELATION_ALERT_THRESHOLD:
                alerts.append((display_name(a), display_name(b), value))

    if alerts:
        print(f"\n⚠ Achtung - folgende Bot-Paare liegen ueber der Korrelations-Schwelle "
              f"({CORRELATION_ALERT_THRESHOLD}):")
        for a, b, value in alerts:
            print(f"  {a} <-> {b}: {value:.2f}")
        print("  Hinweis: Bei seltener Handelsaktivitaet kann die gemessene Korrelation stark")
        print("  schwanken (siehe rsi2_mean_reversion/correlation_robustness_check.py) - als")
        print("  frueher Hinweis lesen, nicht als endgueltigen Beweis fuer echte Kopplung.")
    else:
        print(f"\nKeine Bot-Paare ueber der Korrelations-Schwelle ({CORRELATION_ALERT_THRESHOLD}).")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = normalised.copy()
    output["Portfolio (gewichtet)"] = portfolio_curve
    output_path = os.path.join(RESULTS_DIR, "portfolio_overview_curve.csv")
    output.to_csv(output_path)
    print(f"\nVollstaendige normierte Kurven (fuer spaeteres Plotten) gespeichert unter: {output_path}")


if __name__ == "__main__":
    main()
