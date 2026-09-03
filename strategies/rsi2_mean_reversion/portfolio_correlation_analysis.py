"""
Grobe erste Einschaetzung: Korrelation der vier Bots als kombiniertes Portfolio
====================================================================================
Beantwortet die Frage: Gleichen sich Verlustphasen zwischen den vier Bots
tatsaechlich aus, oder korrelieren sie (z.B. weil alle vier in einem breiten
Markt-Abverkauf gleichzeitig verlieren)?

METHODIK (bewusst einfach gehalten, "grobe erste Einschaetzung" wie
angefragt - keine neue Infrastruktur, keine Aenderung an den bestehenden
Bots):
1. Liest die bereits vorhandenen equity_curve.csv der drei bestehenden Bots
   (results/equity_curve.csv [Elliott Wave Krypto],
   results/t3_supertrend/equity_curve.csv,
   results/elliott_wave_stocks/equity_curve.csv) sowie die frisch erzeugte
   equity_curve.csv des RSI-2-Bots.
2. Baut aus jeder Datei eine TAEGLICHE Kapitalkurve (Forward-Fill zwischen
   Trade-Exit-Ereignissen - zwischen zwei Exits aendert sich das Kapital
   einer Strategie definitionsgemaess nicht).
3. Beschraenkt den Vergleich auf das ZEITFENSTER, in dem ALLE VIER Kurven
   bereits echte Trades hatten (sonst wuerde eine noch "flache" Anfangsphase
   kuenstlich als unkorreliert erscheinen).
4. Berechnet daraus taegliche Renditen je Strategie, eine
   Korrelationsmatrix, sowie eine gleichgewichtete 25/25/25/25-Kombination
   aller vier als einfaches Vier-Bot-Portfolio (nur zur Einordnung - keine
   echte Kapitalallokation zwischen Bots, die Bots bleiben unabhaengig).

WICHTIG - Einschraenkungen dieser groben Analyse:
- Die Krypto-Bots haben deutlich kuerzere Historie (~2021+) als der
  Aktien-Bot (~2016+) - der Vergleich beschraenkt sich zwangslaeufig auf
  die kuerzeste gemeinsame Historie.
- Elliott Wave (Krypto) laeuft auf Stundenkerzen, T3/SuperTrend auf
  4-Stunden-Kerzen, beide Aktien-Bots auf Tageskerzen - hier wird fuer den
  Vergleich einheitlich auf Tagesbasis (letzter Kapitalstand des Tages)
  aggregiert.
- Das ist eine Analyse auf BACKTEST-Daten (keine echten Forward-Test-Trades),
  daher mit der ueblichen Vorsicht zu interpretieren - dient nur einer
  ersten, groben Einordnung, keiner belastbaren Entscheidungsgrundlage.
"""

import os
import pandas as pd

BASE_DIR = "/home/user/trading-bot"
STARTING_CAPITAL = 10_000.0

CURVES = {
    "Elliott Wave (Krypto)": os.path.join(BASE_DIR, "results", "equity_curve.csv"),
    "T3/SuperTrend (Krypto)": os.path.join(BASE_DIR, "results", "t3_supertrend", "equity_curve.csv"),
    "Elliott Wave (Aktien)": os.path.join(BASE_DIR, "results", "elliott_wave_stocks", "equity_curve.csv"),
    "RSI-2 Mean-Reversion (Aktien, neu)": os.path.join(BASE_DIR, "results", "rsi2_mean_reversion", "equity_curve.csv"),
}


def build_daily_capital_curve(csv_path: str) -> pd.Series:
    df = pd.read_csv(csv_path, parse_dates=["time"])
    df = df.sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    daily_last.iloc[0] = daily_last.iloc[0] if pd.notna(daily_last.iloc[0]) else STARTING_CAPITAL
    return daily_last


def main():
    curves = {}
    for label, path in CURVES.items():
        if not os.path.exists(path):
            print(f"Uebersprungen (Datei fehlt, erst Equity-Simulation ausfuehren): {label} -> {path}")
            continue
        curves[label] = build_daily_capital_curve(path)

    if len(curves) < 2:
        print("Nicht genug Kapitalkurven gefunden fuer einen Vergleich.")
        return

    print("Verfuegbare Zeitraeume je Bot:")
    for label, series in curves.items():
        print(f"  {label}: {series.index.min().date()} bis {series.index.max().date()}")

    common_start = max(s.index.min() for s in curves.values())
    common_end = min(s.index.max() for s in curves.values())
    print(f"\nGemeinsames Vergleichsfenster (alle Bots aktiv): {common_start.date()} bis {common_end.date()}\n")

    if common_start >= common_end:
        print("Kein gemeinsames Zeitfenster - Bots ueberlappen sich zeitlich nicht ausreichend.")
        return

    combined = pd.DataFrame({
        label: series.reindex(pd.date_range(common_start, common_end, freq="D")).ffill().bfill()
        for label, series in curves.items()
    })

    # Normierte Kapitalkurven (jede Strategie startet im Vergleichsfenster
    # bei 100), damit die 25/25/25/25-Kombination und die Renditen fair
    # vergleichbar sind, unabhaengig vom absoluten Kapitalstand zu Fensterbeginn.
    normalised = combined / combined.iloc[0] * 100
    daily_returns = normalised.pct_change().dropna()

    print("=" * 70)
    print("KORRELATIONSMATRIX (taegliche Renditen im gemeinsamen Fenster)")
    print("=" * 70)
    corr = daily_returns.corr()
    print(corr.round(2).to_string())

    print("\n" + "=" * 70)
    print("MAX DRAWDOWN JE BOT IM GEMEINSAMEN FENSTER")
    print("=" * 70)
    for label in normalised.columns:
        running_max = normalised[label].cummax()
        dd = ((normalised[label] - running_max) / running_max * 100).min()
        print(f"  {label}: {dd:.2f}%")

    print("\n" + "=" * 70)
    print("GLEICHGEWICHTETE 4-BOT-KOMBINATION (25% je Bot, nur zur Einordnung)")
    print("=" * 70)
    portfolio = normalised.mean(axis=1)
    portfolio_running_max = portfolio.cummax()
    portfolio_dd = ((portfolio - portfolio_running_max) / portfolio_running_max * 100).min()
    portfolio_return = (portfolio.iloc[-1] / portfolio.iloc[0] - 1) * 100
    print(f"  Gesamtrendite im Fenster: {portfolio_return:.2f}%")
    print(f"  Max Drawdown kombiniert:  {portfolio_dd:.2f}%")
    print(f"  (zum Vergleich: schlechtester Einzel-Bot-Drawdown im selben Fenster, siehe oben)")


if __name__ == "__main__":
    main()
