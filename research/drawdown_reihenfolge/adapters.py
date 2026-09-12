"""
Bot-Adapter: ein Bot, ein Raster, eine Trade-Menge
====================================================================
Je Bot steht hier GENAU dreierlei:

  1. welche Kombinationen sein `run_multi_optimisation` durchlaeuft -
     abgeleitet aus den RANGE-Konstanten des Bots selbst, nie
     abgeschrieben (`ein Wert, eine Quelle`, Protokoll Abschnitt 7.11);
  2. wie seine Trade-Menge entsteht - ueber seine eigene
     `get_trades_for_symbol`, nie ueber eine Nachbildung;
  3. wie seine eigene `evaluate_combination_multi` fuer denselben
     Punkt aufzurufen ist - fuer den Gleichheitsnachweis in
     test_drawdown.py.

Die Adapter fuegen der Trade-Menge zwei Spalten hinzu (`symbol`, wo der
Bot sie nicht selbst setzt, und `_block_idx`). Beide aendern weder die
Zeilenreihenfolge noch `pnl_pct` - test_drawdown.py weist das nach,
indem es die Kennzahlen des Adapters gegen den Rueckgabewert der
echten Bot-Funktion stellt.
"""

import pandas as pd


class Adapter:
    """Gemeinsames Verhalten. `mo` ist das bereits importierte
    multi_symbol_optimise des jeweiligen Bots."""

    def __init__(self, mo):
        self.mo = mo

    # -- Raster ------------------------------------------------------
    def combinations(self) -> list:
        raise NotImplementedError

    def label(self, combo) -> str:
        raise NotImplementedError

    # -- Trades ------------------------------------------------------
    def _blocks(self, data, combo) -> list:
        """Liste von (symbol, trades) in der Reihenfolge, in der der Bot
        seine Teilergebnisse aneinanderhaengt."""
        raise NotImplementedError

    def collect(self, data, combo):
        """(trades, contributing_symbols) - `trades` in der
        Zeilenreihenfolge, die der Bot tatsaechlich bewertet, mit den
        Zusatzspalten `symbol` und `_block_idx`."""
        blocks = self._blocks(data, combo)
        if not blocks:
            return None, 0
        frames = []
        for idx, (symbol, trades) in enumerate(blocks):
            t = trades.copy()
            t["symbol"] = symbol
            t["_block_idx"] = idx
            frames.append(t)
        combined = pd.concat(frames, ignore_index=True)
        return combined, len(blocks)

    # -- Mindestfilter des Bots, unveraendert ------------------------
    def besteht_mindestfilter(self, trades, contributing_symbols) -> bool:
        mo = self.mo
        if trades is None or trades.empty:
            return False
        if len(trades) < mo.MIN_TRADES:
            return False
        if contributing_symbols < mo.MIN_SYMBOLS_CONTRIBUTING:
            return False
        if float(trades["pnl_pct"].mean()) < mo.MIN_AVG_RETURN_PCT:
            return False
        return True

    # -- Gegenprobe gegen die echte Bot-Funktion ---------------------
    def bot_eval(self, data, combo) -> dict:
        raise NotImplementedError

    # -- In-Sample-Fenster des Walk-Forward --------------------------
    # Die sechs Prototyp-Bots schneiden fuer den Walk-Forward NICHT die
    # Kursreihe, sondern filtern die fertigen Trades auf
    # `entry_time < cutoff_end` (siehe
    # multi_symbol_walk_forward.evaluate_combination_multi_windowed).
    # Deshalb laesst sich ihr In-Sample-Fenster exakt so nachbilden.
    # Die drei aelteren Bots schneiden die Kursreihe selbst
    # (`df.iloc[:split_idx]`) - dort waeren die Indikatoren andere, und
    # diese Ableitung waere falsch. `unterstuetzt_is` sagt, welcher Fall
    # gilt.
    unterstuetzt_is = False

    def blocks_windowed(self, windowed_data, combo) -> list:
        raise NotImplementedError

    def collect_windowed(self, windowed_data, combo):
        blocks = self.blocks_windowed(windowed_data, combo)
        if not blocks:
            return None, 0
        frames = []
        for idx, (symbol, trades) in enumerate(blocks):
            t = trades.copy()
            t["symbol"] = symbol
            t["_block_idx"] = idx
            frames.append(t)
        return pd.concat(frames, ignore_index=True), len(blocks)

    def bot_eval_windowed(self, wf, windowed_data, combo) -> dict:
        raise NotImplementedError


# --------------------------------------------------------------------
# Elliott Wave (Krypto) - Raster dev x stop x fib
# --------------------------------------------------------------------
class ElliottWave(Adapter):
    def combinations(self):
        mo = self.mo
        return [(d, s, f)
                for d in mo.DEVIATION_RANGE
                for s in mo.STOP_LOSS_RANGE
                for f in mo.TAKE_PROFIT_FIB_RANGE]

    def label(self, combo):
        d, s, f = combo
        return f"dev {d} % / Stop {s} % / Fib {f}"

    def params(self, combo):
        d, s, f = combo
        return {"deviation_pct": d, "stop_loss_pct": s, "take_profit_fib": f}

    def _blocks(self, data, combo):
        mo = self.mo
        d, s, f = combo
        mo.backtest_elliott.STOP_LOSS_PCT = s
        mo.backtest_elliott.TAKE_PROFIT_FIB = f
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, d)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, *combo)


# --------------------------------------------------------------------
# Elliott Wave (Aktien) - zusaetzlich die Option "kein Kursziel"
# --------------------------------------------------------------------
class ElliottWaveStocks(Adapter):
    def combinations(self):
        mo = self.mo
        combos = []
        for d in mo.DEVIATION_RANGE:
            for s in mo.STOP_LOSS_RANGE:
                for f in mo.TAKE_PROFIT_FIB_RANGE:
                    combos.append((d, s, f, True))
                combos.append((d, s, None, False))
        return combos

    def label(self, combo):
        d, s, f, use_tp = combo
        ziel = f"Fib {f}" if use_tp else "kein Ziel"
        return f"dev {d} % / Stop {s} % / {ziel}"

    def params(self, combo):
        d, s, f, use_tp = combo
        return {"deviation_pct": d, "stop_loss_pct": s,
                "take_profit_fib": f, "use_take_profit": use_tp}

    def _blocks(self, data, combo):
        mo = self.mo
        d, s, f, use_tp = combo
        mo.backtest_elliott.STOP_LOSS_PCT = s
        mo.backtest_elliott.TAKE_PROFIT_FIB = f
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, d, use_tp)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, *combo)


# --------------------------------------------------------------------
# T3/ADX/SuperTrend - der Sonderfall: Regimefilter NACH dem Zusammen-
# fuegen, und der sortiert selbst nach entry_time
# --------------------------------------------------------------------
class T3SuperTrend(Adapter):
    # Der BTC-Regimefilter steht erst seit einer spaeteren Aenderung in
    # evaluate_combination_multi. Die gespeicherte Ergebnisdatei
    # results/t3_supertrend/multi_symbol_optimisation_results.csv - die,
    # die die Parameterwahl getragen hat - entstand davor. Mit
    # `regimefilter = False` laesst sich dieser aeltere Zustand
    # rekonstruieren; dass er es tut, belegt der Zeilenvergleich mit
    # jener Datei (siehe BERICHT.md, Frage 2).
    regimefilter = True

    def combinations(self):
        mo = self.mo
        return [(a, b, c, d)
                for a in mo.T3_FAST_RANGE
                for b in mo.T3_SLOW_RANGE
                for c in mo.ADX_THRESHOLD_RANGE
                for d in mo.STOP_LOSS_RANGE
                if a < b]      # wie evaluate_combination_multi des Bots

    def label(self, combo):
        a, b, c, d = combo
        return f"T3 {a}/{b} / ADX {c} / Stop {d} %"

    def params(self, combo):
        a, b, c, d = combo
        return {"t3_fast": a, "t3_slow": b, "adx_threshold": c, "stop_loss_pct": d}

    def _blocks(self, data, combo):
        mo = self.mo
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, *combo)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def collect(self, data, combo):
        combined, n = super().collect(data, combo)
        if combined is None:
            return None, 0
        # genau wie evaluate_combination_multi: Regimefilter, danach
        # Symbolzahl neu zaehlen. filter_trades_by_regime sortiert
        # intern nach entry_time - die Zeilenreihenfolge, die dieser Bot
        # bewertet, ist also bereits chronologisch. `_block_idx` laeuft
        # durch den merge_asof hindurch und haelt die Blockreihenfolge
        # fest.
        if self.regimefilter and "BTCUSDT" in data:
            btc_regime = self.mo.compute_btc_regime(data["BTCUSDT"])
            combined = self.mo.filter_trades_by_regime(combined, btc_regime)
            n = int(combined["symbol"].nunique()) if not combined.empty else 0
        if combined is None or combined.empty:
            return None, 0
        return combined, n

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, *combo)


# --------------------------------------------------------------------
# RSI-2 (Krypto) - Raster sma x rsi x stop
# --------------------------------------------------------------------
class Rsi2Crypto(Adapter):
    def combinations(self):
        mo = self.mo
        return [(sma, rsi, stop)
                for sma in mo.SMA_TREND_RANGE
                for rsi in mo.RSI_THRESHOLD_RANGE
                for stop in mo.STOP_LOSS_RANGE]

    def label(self, combo):
        sma, rsi, stop = combo
        return f"SMA {sma} / RSI {rsi} / Stop {stop if stop is not None else 'kein Stop'}"

    def params(self, combo):
        sma, rsi, stop = combo
        return {"sma_trend_period": sma, "rsi_threshold": rsi,
                "stop_loss_pct": stop if stop is not None else "kein Stop"}

    def _blocks(self, data, combo):
        mo = self.mo
        sma, rsi, stop = combo
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, rsi, sma, stop)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        sma, rsi, stop = combo
        return self.mo.evaluate_combination_multi(data, rsi, sma, stop)

    unterstuetzt_is = True

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        sma, rsi, stop = combo
        out = []
        for symbol, (price_df, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(price_df, rsi, sma, stop, cutoff_start)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval_windowed(self, wf, windowed_data, combo):
        sma, rsi, stop = combo
        return wf.evaluate_combination_multi_windowed(windowed_data, rsi, sma, stop)


# --------------------------------------------------------------------
# RSI-2 (Aktien) - Raster rsi x stop, Daten als (df_ind, entry_cutoff)
# --------------------------------------------------------------------
class Rsi2Stocks(Adapter):
    def combinations(self):
        mo = self.mo
        return [(rsi, stop) for rsi in mo.RSI_THRESHOLD_RANGE for stop in mo.STOP_LOSS_RANGE]

    def label(self, combo):
        rsi, stop = combo
        return f"RSI {rsi} / Stop {stop if stop is not None else 'kein Stop'}"

    def params(self, combo):
        rsi, stop = combo
        return {"rsi_threshold": rsi,
                "stop_loss_pct": stop if stop is not None else "kein Stop"}

    def _blocks(self, data, combo):
        mo = self.mo
        rsi, stop = combo
        out = []
        for symbol, (df_ind, entry_cutoff) in data.items():
            trades = mo.get_trades_for_symbol(df_ind, entry_cutoff, rsi, stop)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, *combo)

    unterstuetzt_is = True

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        rsi, stop = combo
        out = []
        for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(df_ind, cutoff_start, rsi, stop)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval_windowed(self, wf, windowed_data, combo):
        return wf.evaluate_combination_multi_windowed(windowed_data, *combo)


# --------------------------------------------------------------------
# Turtle Soup (Krypto) - Raster donchian x stop_mode
# --------------------------------------------------------------------
class TurtleSoupCrypto(Adapter):
    def combinations(self):
        mo = self.mo
        return [(p, m) for p in mo.DONCHIAN_PERIOD_RANGE for m in mo.STOP_MODE_RANGE]

    def label(self, combo):
        p, m = combo
        return f"Donchian {p} / Stop {m if m is not None else 'kein Stop'}"

    def params(self, combo):
        p, m = combo
        return {"donchian_period": p, "stop_mode": m if m is not None else "kein Stop"}

    def _blocks(self, data, combo):
        mo = self.mo
        p, m = combo
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, p, m)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, *combo)

    unterstuetzt_is = True

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        p, m = combo
        out = []
        for symbol, (price_df, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(price_df, p, m, cutoff_start)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval_windowed(self, wf, windowed_data, combo):
        return wf.evaluate_combination_multi_windowed(windowed_data, *combo)


# --------------------------------------------------------------------
# Turtle Soup (Aktien) - wie oben, Daten als (df, entry_cutoff)
# --------------------------------------------------------------------
class TurtleSoupStocks(TurtleSoupCrypto):
    def _blocks(self, data, combo):
        mo = self.mo
        p, m = combo
        out = []
        for symbol, (df, entry_cutoff) in data.items():
            trades = mo.get_trades_for_symbol(df, entry_cutoff, p, m)
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        p, m = combo
        out = []
        for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(df_ind, cutoff_start, p, m)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out


# --------------------------------------------------------------------
# Volatility Breakout (Krypto) - Raster nur ueber den Stop
# --------------------------------------------------------------------
class BreakoutCrypto(Adapter):
    def combinations(self):
        return [(s,) for s in self.mo.STOP_LOSS_RANGE]

    def label(self, combo):
        s = combo[0]
        return f"Stop {s if s is not None else 'kein Stop'}"

    def params(self, combo):
        s = combo[0]
        return {"stop_loss_pct": s if s is not None else "kein Stop"}

    def _blocks(self, data, combo):
        mo = self.mo
        out = []
        for symbol, price_df in data.items():
            trades = mo.get_trades_for_symbol(price_df, combo[0])
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval(self, data, combo):
        return self.mo.evaluate_combination_multi(data, combo[0])

    unterstuetzt_is = True

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        out = []
        for symbol, (price_df, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(price_df, combo[0], None, False, cutoff_start)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def bot_eval_windowed(self, wf, windowed_data, combo):
        return wf.evaluate_combination_multi_windowed(windowed_data, combo[0])


# --------------------------------------------------------------------
# Volatility Breakout (Aktien) - Daten als (df_ind, entry_cutoff)
# --------------------------------------------------------------------
class BreakoutStocks(BreakoutCrypto):
    def _blocks(self, data, combo):
        mo = self.mo
        out = []
        for symbol, (df_ind, entry_cutoff) in data.items():
            trades = mo.get_trades_for_symbol(df_ind, entry_cutoff, combo[0])
            if not trades.empty:
                out.append((symbol, trades))
        return out

    def blocks_windowed(self, windowed_data, combo):
        mo = self.mo
        out = []
        for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
            trades = mo.get_trades_for_symbol(df_ind, cutoff_start, combo[0], None, False)
            if cutoff_end is not None and not trades.empty:
                trades = trades[trades["entry_time"] < cutoff_end]
            if not trades.empty:
                out.append((symbol, trades))
        return out


ADAPTER = {
    "elliott_wave": ElliottWave,
    "elliott_wave_stocks": ElliottWaveStocks,
    "t3_supertrend": T3SuperTrend,
    "rsi2_crypto": Rsi2Crypto,
    "rsi2_mean_reversion": Rsi2Stocks,
    "turtle_soup_crypto": TurtleSoupCrypto,
    "turtle_soup_stocks": TurtleSoupStocks,
    "volatility_breakout_crypto": BreakoutCrypto,
    "volatility_breakout": BreakoutStocks,
}


def build(bot: str, mo) -> Adapter:
    return ADAPTER[bot](mo)
