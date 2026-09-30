#!/usr/bin/env python3
"""TB-124 Nachtrag 1, B1 - Herleitung des Scanbeginns aus den Indikatordefinitionen, gemessen an compute_indicators.
Je Stufe von bb_lookback (registerdaten.raster()) und der Voreinstellung: ab welchem Index bb_width, squeeze_thresh
und vol_avg definiert sind und welches der erste Index i ist, an dem die Einstiegsbedingung
(is_squeeze[i-1] aus definierter Schwelle, close[i] > bb_upper[i] mit definiertem Band) definiert ist.
Synthetische Kursreihe, keine Datei aus data/. Aufruf (Repo-Wurzel):
  trading-env/bin/python3 docs/belege/TB-124/b1_herleitung.py
"""
import os, subprocess, sys
KIND = r'''
import sys, os; sys.path[:0]=[os.getcwd(), '../../shared', '../../research/vorregistrierung']
import numpy as np, pandas as pd, backtest_breakout as bt, registerdaten
b = os.path.basename(os.getcwd())
st = registerdaten.raster()[b]['bb_lookback']
c = 100*np.cumprod(1+np.random.RandomState(3).normal(0,0.01,600))
roh = pd.DataFrame({'open_time':pd.date_range('2020-01-01',periods=600,freq='D'),'open':c,'high':c,'low':c,'close':c,'volume':1e6})
for s in st + [bt.SQUEEZE_LOOKBACK_DAYS]:
    d = bt.compute_indicators(roh, s)
    erst = lambda col: int(np.argmax(d[col].notna().to_numpy()))
    ok = [i for i in range(1, len(d)) if not np.isnan(d['squeeze_thresh'].iloc[i-1]) and not np.isnan(d['bb_upper'].iloc[i])][0]
    print('%-27s L %3d | bb_width ab %d | squeeze_thresh ab %3d | vol_avg ab %d | erster Einstiegsindex %3d | BB_PERIOD+L-1 = %3d %s | woertlich L+BB_PERIOD = %3d | bisher WARMUP_PERIOD+1 = %d'
          % (b, s, erst('bb_width'), erst('squeeze_thresh'), erst('vol_avg'), ok, bt.BB_PERIOD+s-1,
             'gleich' if ok == bt.BB_PERIOD+s-1 else 'ABWEICHUNG', s+bt.BB_PERIOD, bt.WARMUP_PERIOD+1))
'''
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
print("# TB-124 Nachtrag 1 B1 - Herleitung Scanbeginn (0-basiert), BB_PERIOD = 20")
for b in ("volatility_breakout", "volatility_breakout_crypto"):
    r = subprocess.run([sys.executable, "-W", "ignore", "-c", KIND], cwd=os.path.join(R, "strategies", b), capture_output=True, text=True)
    sys.stdout.write(r.stdout + (("rc %d %s\n" % (r.returncode, r.stderr[-500:])) if r.returncode else ""))
