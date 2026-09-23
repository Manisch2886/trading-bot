#!/usr/bin/env python3
"""TB-90 B2 - die neun Ersetzungen, mechanisch und je Datei genau einmal.

(1) Zuweisungen TRADING_FEE_PCT/SLIPPAGE_PCT (samt dem Kommentar darueber,
    wo es einen gab - er steht jetzt im Kopf von shared/handelskosten.py)
    -> from handelskosten import TRADING_FEE_PCT, SLIPPAGE_PCT
(2) wo der sys.path-Block auf Modulebene fehlt: zeichengleich nach dem
    Muster von strategies/elliott_wave/backtest_elliott.py ergaenzen
    (import os / import sys vor den Importen, der Dreizeilen-Block danach).
Jede Ersetzung muss genau einmal treffen, sonst Abbruch ohne Schreiben.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
IMPORT = "from handelskosten import TRADING_FEE_PCT, SLIPPAGE_PCT\n"
BLOCK = ('_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))\n'
         '_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")\n'
         'sys.path.insert(0, _SHARED_DIR)\n')

ELLIOTT = ("# Realistische Handelskosten (Binance Spot: ~0.1% pro Order als Standard)\n"
           "TRADING_FEE_PCT = 0.1     # pro Order (Entry und Exit je einmal)\n"
           "SLIPPAGE_PCT = 0.05       # angenommene Abweichung vom gewuenschten Preis, je Order\n")
T3 = ("# Trading-Kosten (gleiche Annahmen wie bei der Elliott-Wave-Strategie)\n"
      "TRADING_FEE_PCT = 0.1\nSLIPPAGE_PCT = 0.05\n")
SCHLICHT = "TRADING_FEE_PCT = 0.1\nSLIPPAGE_PCT = 0.05\n"

DATEIEN = {
    "elliott_wave/backtest_elliott.py": (ELLIOTT, None),
    "elliott_wave_stocks/backtest_elliott.py": (ELLIOTT, None),
    "t3_supertrend/backtest_trend.py": (T3, "import pandas as pd\n\n"),
    "rsi2_crypto/backtest_rsi2.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
    "rsi2_mean_reversion/backtest_rsi2.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
    "turtle_soup_crypto/backtest_turtle_soup.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
    "turtle_soup_stocks/backtest_turtle_soup.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
    "volatility_breakout/backtest_breakout.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
    "volatility_breakout_crypto/backtest_breakout.py": (SCHLICHT, "import numpy as np\nimport pandas as pd\n\n"),
}

neu = {}
for rel, (alt, kopf) in DATEIEN.items():
    pfad = os.path.join(REPO, "strategies", rel)
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    n = text.count(alt)
    if n != 1:
        sys.exit("ABBRUCH %s: Kostenzuweisung %dx statt 1x" % (rel, n))
    text = text.replace(alt, IMPORT)
    if kopf is not None:
        if "\n" + BLOCK in text or "\nimport sys\n" in text.split('"""', 2)[2][:400]:
            sys.exit("ABBRUCH %s: Block schon vorhanden" % rel)
        n = text.count(kopf)
        if n != 1:
            sys.exit("ABBRUCH %s: Importkopf %dx statt 1x" % (rel, n))
        text = text.replace(kopf, "import os\nimport sys\n" + kopf + BLOCK + "\n")
    neu[pfad] = text

for pfad, text in neu.items():
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)
    print("geschrieben:", os.path.relpath(pfad, REPO))
