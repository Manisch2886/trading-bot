"""
Aktuell live genutzte Parameter - T3/ADX/SuperTrend-Strategie (Krypto)
============================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.
"""

T3_FAST_LENGTH = 16
T3_SLOW_LENGTH = 30
ADX_THRESHOLD = 20.0
STOP_LOSS_PCT = 4.0
MAX_CONCURRENT_POSITIONS = 5

# Weitere wirksame Parameter: bewusst NICHT hier definiert - reine Dokumentation.
# ------------------------------------------------------------------------
# Die folgenden Groessen bestimmen den Live-Betrieb dieses Bots mit, stehen
# aber nicht in dieser Datei. Der Eintrag hier aendert daran nichts - er macht
# nur sichtbar, was sonst nur beim Lesen der Indikator-Dateien auffaellt
# (Muster wie beim ALLOCATION_PCT-Block in elliott_wave_stocks/live_params.py).
# Erhoben mit research/backtest_defaults/ (PR #45), Werte am 2026-09-08 erneut
# geprueft.
#
# INDIKATOR-PARAMETER - und zwar DOPPELT gefuehrt:
#
#   T3_FACTOR   = 0.7   DI_LENGTH  = 14   ADX_LENGTH = 14
#   ATR_LENGTH  = 22    ATR_MULT   = 3.0
#
# Sie stehen ZWEIMAL im Bot, mit je eigener Zahl:
#   - backtest_trend.py:49-54 (Defaults von run_backtest(); der Live-Pfad
#     ueber multi_symbol_optimise.get_trades_for_symbol() uebergibt sie nicht,
#     der Default wirkt also)
#   - forward_test.py:39-43 (dort erneut gesetzt und in Zeile 194/195 an die
#     Indikatorberechnung uebergeben - das ist der Cronjob)
# Stand 2026-09-08 sind beide Saetze identisch. Sie koennen aber unbemerkt
# auseinanderlaufen: wer einen Wert anpasst und den zweiten Ort vergisst,
# bekommt einen Backtest, der eine andere Strategie beschreibt als die
# laufende - genau die Falle, die bei elliott_wave_stocks/USE_TAKE_PROFIT
# schon einmal zugeschnappt ist (PR #24/#31).
#
# EXIT- UND FILTER-SCHALTER (Literale in der Signatur von run_backtest(),
# backtest_trend.py:61):
#   use_t3_exit     = True    Ausstieg beim T3-Kreuzen - live aktiv
#   use_vwap_filter = False   zusaetzliche Bedingung "Preis > VWAP" beim
#                             Einstieg. Bewusst AUS: isolierte Tests zeigten
#                             bessere Trade-Qualitaet, die volle
#                             Equity-Simulation aber GERINGERE Gesamtrendite
#                             (weniger Trades = weniger Zinseszins). Siehe
#                             den Docstring von run_backtest() und
#                             Uebergabeprotokoll Abschnitt 5.
# Solange use_vwap_filter=False gilt, ist auch bars_per_day = 6 in
# indicators.py:128 (calculate_vwap_daily) ohne Wirkung - 6 Vier-Stunden-
# Kerzen je Tag.
#
# MARKT-REGIME-FILTER (regime_filter.py:19, Literale in der Signatur von
# compute_btc_regime()):
#   atr_length = 22   atr_mult = 3.0
# equity_simulation.py:66 ruft die Funktion ohne Argumente auf, die Literale
# wirken also direkt. Sie entsprechen ATR_LENGTH/ATR_MULT oben, sind aber eine
# dritte, unabhaengige Kopie derselben Zahlen.
#
# BEWUSST NUR DOKUMENTIERT, NICHT GEKOPPELT: ein Import dieser Werte aus
# dieser Datei waere eine strukturelle Aenderung mit echtem Risiko fuer die
# Optimierungs-Skripte und ist eine eigene Entscheidung (PR #45, Befund 7.2).

LAST_UPDATED = "2026-08-31"  # Stand der PARAMETER - der Dokumentationsblock
                              # oben aendert keinen Wert und faellt deshalb
                              # nicht darunter.
