"""TB-124 B - Einbau des Scanbeginns in die zwei backtest_breakout.py (exakte Ersetzungen, je genau einmal).
Aufruf: python3 b_einbau.py <wurzel>   (wurzel = Repo oder Kandidatenordner)"""
import os, sys
W = sys.argv[1]
VERMERK_ALT = '''    df["vol_avg"] = df["volume"].rolling(window=VOLUME_AVG_PERIOD).mean()
    return df
'''
VERMERK_NEU = '''    df["vol_avg"] = df["volume"].rolling(window=VOLUME_AVG_PERIOD).mean()
    # TB-124 (F1): der Lookback reist mit dem Frame - run_backtest liest ihn
    # hier ab und beginnt den Scan so frueh, wie diese Indikatoren es erlauben.
    df.attrs["squeeze_lookback_days"] = squeeze_lookback_days
    return df
'''
START = {
    "volatility_breakout": ('''    start_i = WARMUP_PERIOD + 1  # +1, da Punkt 2 den Squeeze-Status von t-1 braucht
''', '''    # TB-124 (F1, Nachtrag 1 / Fable 30a R53): Der Scan beginnt am ersten Index,
    # an dem die Einstiegsbedingung definiert ist - nie davor, nicht spaeter.
    # Herleitung (0-basiert, rolling ohne min_periods): bb_width ist ab
    # BB_PERIOD - 1 definiert, squeeze_thresh (Fenster L ueber bb_width) ab
    # BB_PERIOD - 1 + L - 1, und der Einstieg bei i braucht is_squeeze[i - 1];
    # also i >= BB_PERIOD + L - 1 (bb_upper ist dann laengst definiert). vol_avg
    # (ab VOLUME_AVG_PERIOD - 1) ist nicht Teil der Einstiegsbedingung; mit
    # use_volume_filter wird ein NaN unten uebersprungen. L ist der Lookback, mit
    # dem compute_indicators die Indikatoren DIESES Frames gerechnet hat
    # (df.attrs); ohne Vermerk die Voreinstellung SQUEEZE_LOOKBACK_DAYS.
    # WARMUP_PERIOD bleibt als Voreinstellung fuer seine Leser stehen.
    squeeze_lookback_days = df.attrs.get("squeeze_lookback_days", SQUEEZE_LOOKBACK_DAYS)
    start_i = BB_PERIOD + squeeze_lookback_days - 1
'''),
    "volatility_breakout_crypto": ('''    start_i = WARMUP_PERIOD + 1
''', '''    # TB-124 (F1, Nachtrag 1 / Fable 30a R53): Der Scan beginnt am ersten Index,
    # an dem die Einstiegsbedingung definiert ist - nie davor, nicht spaeter.
    # Herleitung (0-basiert, rolling ohne min_periods): bb_width ist ab
    # BB_PERIOD - 1 definiert, squeeze_thresh (Fenster L ueber bb_width) ab
    # BB_PERIOD - 1 + L - 1, und der Einstieg bei i braucht is_squeeze[i - 1];
    # also i >= BB_PERIOD + L - 1 (bb_upper ist dann laengst definiert). vol_avg
    # (ab VOLUME_AVG_PERIOD - 1) ist nicht Teil der Einstiegsbedingung; mit
    # use_volume_filter wird ein NaN unten uebersprungen. L ist der Lookback, mit
    # dem compute_indicators die Indikatoren DIESES Frames gerechnet hat
    # (df.attrs); ohne Vermerk die Voreinstellung SQUEEZE_LOOKBACK_DAYS.
    # WARMUP_PERIOD bleibt als Voreinstellung fuer seine Leser stehen.
    squeeze_lookback_days = df.attrs.get("squeeze_lookback_days", SQUEEZE_LOOKBACK_DAYS)
    start_i = BB_PERIOD + squeeze_lookback_days - 1
'''),
}
for bot, (alt, neu) in START.items():
    p = os.path.join(W, "strategies", bot, "backtest_breakout.py")
    s = open(p, encoding="utf-8").read()
    for a, n in ((VERMERK_ALT, VERMERK_NEU), (alt, neu)):
        k = s.count(a)
        if k != 1:
            sys.exit(f"ABBRUCH {p}: Anker {k}x statt 1x: {a[:60]!r}")
        s = s.replace(a, n)
    open(p, "w", encoding="utf-8").write(s)
    print("eingebaut", p)
