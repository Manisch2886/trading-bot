# Vollständige Bestandsaufnahme aller Funktions-Defaults (9 Bots)

Erzeugt von `default_scan.py`. Zeilen ohne Aufrufstelle (tote Funktionen) sind weggelassen.

| Bot | Modul | Funktion(Parameter) | Default | im Live-Pfad überschrieben? | wirkt über Default? | von Optimierung variiert? | Einordnung |
|---|---|---|---|---|---|---|---|
| elliott_wave | `elliott_wave_counter.py` | `find_impulse_waves(min_fib_score)` | `0.3` | ja | nein | nein | - |
| elliott_wave | `elliott_wave_counter.py` | `find_causal_waves(min_fib_score)` | `0.3` | ja | nein | ja | - |
| elliott_wave | `elliott_wave_counter.py` | `find_causal_waves(freshness_bars)` | `None` | ja | nein | ja | - |
| elliott_wave | `elliott_wave_counter.py` | `find_causal_waves(direction)` | `bearish` | ja | nein | ja | - |
| elliott_wave | `quarterly_review.py` | `build_report(recommendation)` | `` | nein | nein | nein | - |
| elliott_wave | `zigzag_indicator.py` | `calculate_zigzag(deviation_pct)` | `3.0` | ja | nein | nein | - |
| elliott_wave | `zigzag_indicator.py` | `calculate_zigzag_with_confirmation(deviation_pct)` | `3.0` | ja | nein | ja | - |
| elliott_wave_stocks | `backtest_elliott.py` | `simulate_trade(use_take_profit)` | `True` | ja | nein | nein | - |
| elliott_wave_stocks | `backtest_elliott.py` | `run_backtest(use_take_profit)` | `True` | ja | nein | nein | - |
| elliott_wave_stocks | `elliott_wave_counter.py` | `find_impulse_waves(min_fib_score)` | `0.3` | ja | nein | nein | - |
| elliott_wave_stocks | `elliott_wave_counter.py` | `find_causal_waves(min_fib_score)` | `0.3` | ja | nein | ja | - |
| elliott_wave_stocks | `elliott_wave_counter.py` | `find_causal_waves(freshness_bars)` | `None` | ja | nein | ja | - |
| elliott_wave_stocks | `elliott_wave_counter.py` | `find_causal_waves(direction)` | `bearish` | ja | nein | ja | - |
| elliott_wave_stocks | `equity_simulation.py` | `collect_all_trades(use_take_profit)` | `True` | ja | nein | nein | - |
| elliott_wave_stocks | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| elliott_wave_stocks | `experiment_concurrency_stats.py` | `simulate_portfolio_instrumented(max_concurrent_positions)` | `None` | nein | nein | nein | - |
| elliott_wave_stocks | `fetch_stock_data.py` | `fetch_historical_data(period)` | `<PERIOD>` | ja | nein | nein | - |
| elliott_wave_stocks | `fetch_stock_data.py` | `fetch_historical_data(interval)` | `<INTERVAL>` | ja | nein | nein | - |
| elliott_wave_stocks | `multi_symbol_optimise.py` | `get_trades_for_symbol(use_take_profit)` | `True` | ja | nein | ja | - |
| elliott_wave_stocks | `multi_symbol_optimise.py` | `evaluate_combination_multi(use_take_profit)` | `True` | nein | nein | ja | - |
| elliott_wave_stocks | `quarterly_review.py` | `build_report(recommendation)` | `` | nein | nein | nein | - |
| elliott_wave_stocks | `zigzag_indicator.py` | `calculate_zigzag(deviation_pct)` | `3.0` | ja | nein | nein | - |
| elliott_wave_stocks | `zigzag_indicator.py` | `calculate_zigzag_with_confirmation(deviation_pct)` | `3.0` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_fast_length)` | `<T3_FAST_LENGTH>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_slow_length)` | `<T3_SLOW_LENGTH>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_factor)` | `<T3_FACTOR>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(di_length)` | `<DI_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(adx_length)` | `<ADX_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(adx_threshold)` | `<ADX_THRESHOLD>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(atr_length)` | `<ATR_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(atr_mult)` | `<ATR_MULT>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(stop_loss_pct)` | `<STOP_LOSS_PCT>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(use_t3_exit)` | `True` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(use_vwap_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| t3_supertrend | `indicators.py` | `calculate_vwap_daily(bars_per_day)` | `6` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `quarterly_review.py` | `build_report(recommendation)` | `` | nein | nein | nein | - |
| t3_supertrend | `regime_filter.py` | `compute_btc_regime(atr_length)` | `22` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `regime_filter.py` | `compute_btc_regime(atr_mult)` | `3.0` | nein | **ja** | nein | KEIN GEGENSTUECK |
| rsi2_crypto | `backtest_rsi2.py` | `run_backtest(stop_loss_pct)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `backtest_rsi2.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `equity_simulation.py` | `collect_all_trades(stop_loss_pct)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `indicators.py` | `rsi(period)` | `2` | ja | nein | nein | - |
| rsi2_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(stop_loss_pct)` | `None` | ja | nein | ja | - |
| rsi2_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| rsi2_crypto | `multi_symbol_optimise.py` | `evaluate_combination_multi(stop_loss_pct)` | `None` | nein | nein | ja | - |
| rsi2_crypto | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(stop_loss_pct)` | `None` | nein | nein | nein | - |
| rsi2_crypto | `pipeline_report.py` | `collect_trades_windowed(stop_loss_pct)` | `None` | nein | nein | nein | - |
| rsi2_crypto | `regime_filter.py` | `compute_btc_regime(atr_length)` | `<BTC_ATR_LENGTH>` | nein | nein | nein | - |
| rsi2_crypto | `regime_filter.py` | `compute_btc_regime(atr_mult)` | `<BTC_ATR_MULT>` | nein | nein | nein | - |
| rsi2_mean_reversion | `backtest_rsi2.py` | `run_backtest(stop_loss_pct)` | `None` | ja | nein | nein | - |
| rsi2_mean_reversion | `backtest_rsi2.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| rsi2_mean_reversion | `correlation_robustness_check.py` | `build_daily_capital_curve(starting_capital)` | `10000.0` | nein | nein | nein | - |
| rsi2_mean_reversion | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| rsi2_mean_reversion | `fetch_stock_data.py` | `fetch_historical_data(period)` | `<PERIOD>` | ja | nein | nein | - |
| rsi2_mean_reversion | `fetch_stock_data.py` | `fetch_historical_data(interval)` | `<INTERVAL>` | ja | nein | nein | - |
| rsi2_mean_reversion | `indicators.py` | `rsi(period)` | `2` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `compute_indicators(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_crypto | `equity_simulation.py` | `collect_all_trades(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `experiment_volatility_breakout_overlap.py` | `test_temporal_proximity(n_shuffles)` | `20` | nein | nein | nein | - |
| turtle_soup_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(stop_mode)` | `None` | ja | nein | ja | - |
| turtle_soup_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| turtle_soup_crypto | `multi_symbol_optimise.py` | `evaluate_combination_multi(stop_mode)` | `None` | nein | nein | ja | - |
| turtle_soup_crypto | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(stop_mode)` | `None` | nein | nein | nein | - |
| turtle_soup_crypto | `pipeline_report.py` | `collect_trades_windowed(stop_mode)` | `None` | nein | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `compute_indicators(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_stocks | `equity_simulation.py` | `collect_all_trades(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `experiment_volatility_breakout_overlap.py` | `test_temporal_proximity(n_shuffles)` | `20` | nein | nein | nein | - |
| turtle_soup_stocks | `fetch_stock_data.py` | `fetch_historical_data(period)` | `<PERIOD>` | ja | nein | nein | - |
| turtle_soup_stocks | `fetch_stock_data.py` | `fetch_historical_data(interval)` | `<INTERVAL>` | ja | nein | nein | - |
| turtle_soup_stocks | `multi_symbol_optimise.py` | `get_trades_for_symbol(stop_mode)` | `None` | ja | nein | ja | - |
| turtle_soup_stocks | `multi_symbol_optimise.py` | `evaluate_combination_multi(stop_mode)` | `None` | nein | nein | ja | - |
| turtle_soup_stocks | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(stop_mode)` | `None` | nein | nein | nein | - |
| turtle_soup_stocks | `pipeline_report.py` | `collect_trades_windowed(stop_mode)` | `None` | nein | nein | nein | - |
| volatility_breakout | `analysis_2022_drawdown_dynamics.py` | `build_daily_capital_curve(starting_capital)` | `10000.0` | nein | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `compute_indicators(squeeze_lookback_days)` | `<SQUEEZE_LOOKBACK_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `compute_indicators(squeeze_percentile)` | `<SQUEEZE_PERCENTILE>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(stop_loss_pct)` | `5.0` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(use_volume_filter)` | `False` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(volume_filter_multiplier)` | `<VOLUME_FILTER_MULTIPLIER>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout | `equity_simulation.py` | `collect_all_trades(max_hold_days)` | `None` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout | `equity_simulation.py` | `collect_all_trades(use_volume_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| volatility_breakout | `experiment_trailing_stop.py` | `run_backtest_trailing(entry_cutoff)` | `None` | nein | nein | nein | - |
| volatility_breakout | `experiment_trailing_stop.py` | `run_backtest_trailing(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | nein | nein | - |
| volatility_breakout | `fetch_stock_data.py` | `fetch_historical_data(period)` | `<PERIOD>` | ja | nein | nein | - |
| volatility_breakout | `fetch_stock_data.py` | `fetch_historical_data(interval)` | `<INTERVAL>` | ja | nein | nein | - |
| volatility_breakout | `indicators.py` | `bollinger_bands(period)` | `20` | ja | nein | nein | - |
| volatility_breakout | `indicators.py` | `bollinger_bands(num_std)` | `2.0` | ja | nein | nein | - |
| volatility_breakout | `multi_symbol_optimise.py` | `get_trades_for_symbol(max_hold_days)` | `None` | ja | nein | ja | - |
| volatility_breakout | `multi_symbol_optimise.py` | `get_trades_for_symbol(use_volume_filter)` | `False` | ja | nein | ja | - |
| volatility_breakout | `multi_symbol_optimise.py` | `evaluate_combination_multi(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout | `multi_symbol_optimise.py` | `evaluate_combination_multi(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout | `pipeline_report.py` | `collect_trades_windowed(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout | `pipeline_report.py` | `collect_trades_windowed(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout | `stress_period_2020_covid.py` | `build_daily_capital_curve(starting_capital)` | `10000.0` | nein | nein | nein | - |
| volatility_breakout | `stress_period_comparison.py` | `build_daily_capital_curve(starting_capital)` | `10000.0` | nein | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `compute_indicators(squeeze_lookback_days)` | `<SQUEEZE_LOOKBACK_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `compute_indicators(squeeze_percentile)` | `<SQUEEZE_PERCENTILE>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(stop_loss_pct)` | `8.0` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(use_volume_filter)` | `False` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(volume_filter_multiplier)` | `<VOLUME_FILTER_MULTIPLIER>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `equity_simulation.py` | `collect_all_trades(stop_loss_pct)` | `None` | ja | nein | nein | - |
| volatility_breakout_crypto | `equity_simulation.py` | `collect_all_trades(max_hold_days)` | `None` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `equity_simulation.py` | `collect_all_trades(use_volume_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `equity_simulation.py` | `simulate_portfolio(max_concurrent_positions)` | `None` | ja | nein | nein | - |
| volatility_breakout_crypto | `indicators.py` | `bollinger_bands(period)` | `20` | ja | nein | nein | - |
| volatility_breakout_crypto | `indicators.py` | `bollinger_bands(num_std)` | `2.0` | ja | nein | nein | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(stop_loss_pct)` | `None` | ja | nein | ja | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(max_hold_days)` | `None` | ja | nein | ja | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(use_volume_filter)` | `False` | ja | nein | ja | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `evaluate_combination_multi(stop_loss_pct)` | `None` | nein | nein | ja | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `evaluate_combination_multi(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `evaluate_combination_multi(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout_crypto | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(stop_loss_pct)` | `None` | nein | nein | nein | - |
| volatility_breakout_crypto | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout_crypto | `multi_symbol_walk_forward.py` | `evaluate_combination_multi_windowed(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout_crypto | `pipeline_report.py` | `collect_trades_windowed(stop_loss_pct)` | `None` | nein | nein | nein | - |
| volatility_breakout_crypto | `pipeline_report.py` | `collect_trades_windowed(max_hold_days)` | `None` | nein | nein | nein | - |
| volatility_breakout_crypto | `pipeline_report.py` | `collect_trades_windowed(use_volume_filter)` | `False` | nein | nein | nein | - |
| volatility_breakout_crypto | `regime_filter.py` | `compute_btc_regime(atr_length)` | `<BTC_ATR_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `regime_filter.py` | `compute_btc_regime(atr_mult)` | `<BTC_ATR_MULT>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `stress_period_2022_crypto_family.py` | `build_daily_capital_curve(starting_capital)` | `10000.0` | nein | nein | nein | - |

141 Zeilen.
