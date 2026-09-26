#!/bin/bash
# TB-115 M2 (c), B2 - Stufe 3 der Zuteilungskaskade: Dollar-Volumen aus close * volume.
# Rein lesend. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-115/m2c_zuteilung.sh
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
echo "# TB-115 B2 - shared/zuteilung.py, sha256 $(shasum -a 256 shared/zuteilung.py | cut -c1-16)..."
echo "## Stufen und Dollar-Volumen (Fundstellen)"
grep -nE "3\. \*\*Liquiditaet\*\*|Bei leerem Buch|umsatz = \(close \* menge\)|# Stufe [1-4]|if len\(gruppe\) > 1 and buch and self.vorrat" shared/zuteilung.py
echo "## SIGNALSPALTE der vier Aktien-Bots (None = Stufe 1 entfaellt)"
grep -nE "^SIGNALSPALTE *=" strategies/elliott_wave_stocks/equity_simulation.py strategies/rsi2_mean_reversion/equity_simulation.py strategies/turtle_soup_stocks/equity_simulation.py strategies/volatility_breakout/equity_simulation.py
echo "## Volumen an Split-Tagen im Snapshot (open_time, close, volume) - split-bereinigt, wenn ohne Sprung um den Faktor"
for x in "AAPL 2020-08-2[78]|2020-08-31|2020-09-01" "TSLA 2022-08-2[3-6]" "NVDA 2024-06-(0[67]|1[01])"; do
  set -- $x; echo "  $1:"; grep -E "^($2)" $S/$1_1d.csv | cut -d, -f1,5,6 | sed 's/^/    /'
done
