"""
Welche Konfiguration gilt fuer welchen Bot?
====================================================================
Der Kern dieser Auswertung ist NICHT die Rechnung - die ist trivial -
sondern die Frage, mit welchen Parametern jeder Bot gerechnet wird.
Der Sync-Check (PR #24) hat gezeigt: die Konstanten in
`equity_simulation.py` sind bei mehreren Bots nicht dieselben wie die
Werte in `live_params.py`, und `live_params.py` ist die einzige Datei,
aus der `forward_test.py` tatsaechlich liest. Wer die
`equity_simulation`-Konstanten nimmt, rechnet also einen Bot nach, der
so gar nicht laeuft.

Diese Tabelle macht die Zuordnung explizit und maschinenlesbar:

  kwargs      welcher live_params-Wert in welches Argument von
              equity_simulation.collect_all_trades geht
  konstanten  welche live_params-Werte NICHT als Argument
              durchgereicht werden koennen, sondern als Modulkonstante
              gesetzt werden muessen, damit sie ueberhaupt wirken -
              mit dem Modul und dem dortigen Namen. extract.py
              vergleicht vor dem Setzen und protokolliert jede
              Abweichung, damit im Bericht steht, welche
              Sync-Korrektur tatsaechlich gegriffen hat.
  limit       der live gesetzte MAX_CONCURRENT_POSITIONS-Wert (None =
              unbegrenzt). Fuer die 1000-USD-Rechnung ohne Bedeutung,
              aber noetig, um die Reihenfolge-Frage aus PR #23 zu
              beantworten.
  regimefilter  Bots, deren Live-Code Einstiege bei baerischem
              BTC-Regime blockiert, deren collect_all_trades das aber
              NICHT selbst tut. Nur volatility_breakout_crypto - bei
              t3_supertrend filtert collect_all_trades bereits selbst.

Nicht in dieser Tabelle stehen die beiden Elliott-Wave-Bots: ihre
Parameter kommen ueber varianten.py, weil fuer den Krypto-Bot zwei
Staende gerechnet werden (alt und neu).
"""

# Bots, deren Parameter direkt aus live_params.py kommen
STANDARD = {
    "rsi2_crypto": {
        "kwargs": {"rsi_threshold": "RSI_THRESHOLD",
                    "sma_trend_period": "SMA_TREND_FILTER",
                    "stop_loss_pct": "STOP_LOSS_PCT"},
        "konstanten": [],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "rsi2_mean_reversion": {
        "kwargs": {"rsi_threshold": "RSI_THRESHOLD",
                    "stop_loss_pct": "STOP_LOSS_PCT"},
        "konstanten": [("backtest_rsi2", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS")],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "t3_supertrend": {
        # collect_all_trades wendet den BTC-Regimefilter bereits selbst an.
        "kwargs": {"t3_fast": "T3_FAST_LENGTH", "t3_slow": "T3_SLOW_LENGTH",
                    "adx_threshold": "ADX_THRESHOLD", "stop_loss_pct": "STOP_LOSS_PCT"},
        "konstanten": [],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "turtle_soup_crypto": {
        "kwargs": {"donchian_period": "DONCHIAN_PERIOD", "stop_mode": "STOP_MODE"},
        "konstanten": [("backtest_turtle_soup", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS")],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "turtle_soup_stocks": {
        "kwargs": {"donchian_period": "DONCHIAN_PERIOD", "stop_mode": "STOP_MODE"},
        "konstanten": [("backtest_turtle_soup", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS")],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "volatility_breakout": {
        "kwargs": {"stop_loss_pct": "STOP_LOSS_PCT", "max_hold_days": "MAX_HOLD_DAYS"},
        "konstanten": [("backtest_breakout", "SQUEEZE_PERCENTILE", "BB_SQUEEZE_PERCENTILE"),
                        ("backtest_breakout", "SQUEEZE_LOOKBACK_DAYS", "BB_LOOKBACK")],
        "limit": "MAX_CONCURRENT_POSITIONS",
        "regimefilter": False,
    },
    "volatility_breakout_crypto": {
        "kwargs": {"stop_loss_pct": "STOP_LOSS_PCT", "max_hold_days": "MAX_HOLD_DAYS"},
        "konstanten": [("backtest_breakout", "SQUEEZE_PERCENTILE", "BB_SQUEEZE_PERCENTILE"),
                        ("backtest_breakout", "SQUEEZE_LOOKBACK_DAYS", "BB_LOOKBACK")],
        "limit": "MAX_CONCURRENT_POSITIONS",
        # BTC_REGIME_FILTER_ENABLED = True in live_params, aber
        # collect_all_trades wendet den Filter nicht an - siehe
        # PR #22-Nachtrag. Hier wird er nachgezogen.
        "regimefilter": True,
    },
}

# Die beiden Elliott-Wave-Bots. Fuer den Krypto-Bot zwei Staende:
# "alt" ist der Stand vor der Uebernahme, "neu" der uebernommene.
# Beide auf der kausal korrigierten Backtest-Grundlage aus PR #26.
ELLIOTT = {
    "elliott_wave_alt": {
        "bot": "elliott_wave",
        "beschreibung": "Zigzag 4 % / Stop 2 % / Fib 0.236 (Stand bis 2026-09-07)",
        "kwargs": {"deviation_pct": 4.0, "stop_loss_pct": 2.0, "take_profit_fib": 0.236},
        "limit": None,
        "quelle": "fest gesetzt - der Stand VOR der Parameter-Uebernahme",
    },
    "elliott_wave_neu": {
        "bot": "elliott_wave",
        "beschreibung": "Zigzag 10 % / Stop 6 % / Fib 0.618 (uebernommen 2026-09-07)",
        "kwargs": {"deviation_pct": 10.0, "stop_loss_pct": 6.0, "take_profit_fib": 0.618},
        "limit": None,
        "quelle": "fest gesetzt - der uebernommene Stand (PR #28)",
    },
    "elliott_wave_stocks": {
        "bot": "elliott_wave_stocks",
        "beschreibung": "unveraenderte Live-Konfiguration",
        "kwargs": None,          # kommt aus live_params.py
        "limit": "MAX_CONCURRENT_POSITIONS",
        "quelle": "live_params.py, unveraendert",
    },
}

# Reihenfolge der Zeilen im Bericht
REIHENFOLGE = ["elliott_wave_alt", "elliott_wave_neu", "elliott_wave_stocks",
                "t3_supertrend", "rsi2_crypto", "rsi2_mean_reversion",
                "turtle_soup_crypto", "turtle_soup_stocks",
                "volatility_breakout", "volatility_breakout_crypto"]

JAHR = 2025
POSITIONSGROESSE_USD = 1000.0
