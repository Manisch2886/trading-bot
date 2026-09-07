"""
BTC-Regimefilter fuer die Vertiefungsstudie
====================================================================
Der Sync-Check (PR #24) hat belegt: `live_params.py` fuehrt
`BTC_REGIME_FILTER_ENABLED = True`, aber `equity_simulation.py` wendet den
Filter nicht an. Saemtliche Zahlen der Vorgaenger-Studien - auch die der
ersten Fassung dieser Vertiefungsstudie - sind daher OHNE Filter gerechnet,
waehrend der Live-Bot MIT laeuft.

Dieses Modul stellt den Filter fuer die Studie bereit. Es definiert ihn
NICHT neu, sondern benutzt ausschliesslich die unveraenderten Funktionen des
Bots (`strategies/volatility_breakout_crypto/regime_filter.py`) - dieselben,
die `forward_test.py` live benutzt.

--------------------------------------------------------------------
Zwei Anwendungsarten - und warum beide gerechnet werden
--------------------------------------------------------------------
Der Filter blockiert LIVE neue Einstiege (forward_test.py:158: wenn BTC im
Abwaertstrend ist, wird der komplette Lauf ohne Einstieg beendet). Das
Projekt selbst wertet ihn im Backtest jedoch NACHTRAEGLICH aus - sowohl
`regime_filter.filter_trades_by_regime` als auch das bestehende
`experiment_btc_regime_filter.py` erzeugen erst den vollen Trade-Satz und
streichen daraus die Trades mit BTC-Abwaertstrend zum Einstiegszeitpunkt.

Beides ist NICHT dasselbe, und der Unterschied ist strukturell, nicht
numerisch-zufaellig: der Bot kennt kein Pyramiding, der naechste Scan eines
Symbols startet erst NACH dem Ausstieg. Wird ein Einstieg live blockiert,
bleibt das Symbol frei und kann ein SPAETERES Signal annehmen, das im
ungefilterten Lauf gar nicht erst entstanden waere, weil dort noch eine
Position lief. Nachtraegliches Streichen kann solche Ersatz-Trades
per Konstruktion nicht erzeugen.

  * `posthoc`     - Projekt-Konvention. Referenzfaehig: reproduziert die im
                    Sync-Check veroeffentlichten Zahlen und die des
                    bestehenden Bot-Experiments. Wird als PRIMAERE Variante
                    dieser Studie verwendet.
  * `sequential`  - mechanisch getreue Nachbildung des Live-Verhaltens
                    (Blockade im Scan statt Streichung danach). Wird als
                    Robustheits-Gegenprobe gerechnet, um zu zeigen, ob die
                    Konvention das Ergebnis traegt.

Reine Backtest-Untersuchung: dieses Modul wird von keinem Live-Skript
importiert und aendert nichts an strategies/.
"""

import numpy as np
import pandas as pd

REGIME_POSTHOC = "posthoc"
REGIME_SEQUENTIAL = "sequential"
REGIME_OFF = "off"
REGIME_MODES = (REGIME_OFF, REGIME_POSTHOC, REGIME_SEQUENTIAL)

BTC_SYMBOL = "BTCUSDT"


def btc_regime_table(raw_data: dict) -> pd.DataFrame:
    """BTC-Regime-Tabelle ueber die UNVERAENDERTE Bot-Funktion.

    `compute_btc_regime` berechnet den taeglichen SuperTrend von BTC selbst
    (ATR-Laenge 22, Multiplikator 3,0 - Bot-Konstanten, hier nicht
    veraendert) und gibt je Balken die Richtung zurueck: 1 = Aufwaerts
    (Einstiege erlaubt), -1 = Abwaerts (blockiert).
    """
    from regime_filter import compute_btc_regime

    btc = raw_data.get(BTC_SYMBOL)
    if btc is None:
        raise SystemExit(
            f"{BTC_SYMBOL} fehlt in den geladenen Kursdaten - ohne BTC-Referenz "
            "laesst sich der Regimefilter nicht anwenden.")
    return compute_btc_regime(btc)


def filter_posthoc(trades: pd.DataFrame, regime: pd.DataFrame) -> pd.DataFrame:
    """Nachtraegliches Streichen ueber die UNVERAENDERTE Bot-Funktion
    `regime_filter.filter_trades_by_regime` (merge_asof rueckwaerts, es
    zaehlt also der zuletzt bekannte BTC-Zustand zum Einstiegszeitpunkt).

    Die Bot-Funktion gibt einen neu indizierten Ausschnitt zurueck; die
    uebrigen Spalten (atr_at_entry, vol_at_entry, ...) bleiben erhalten,
    was fuer die Gewichtung dieser Studie noetig ist.
    """
    from regime_filter import filter_trades_by_regime

    if trades is None or trades.empty:
        return trades
    out = filter_trades_by_regime(trades, regime)
    return out.sort_values("entry_time", kind="stable").reset_index(drop=True)


def regime_mask_for(open_times: np.ndarray, regime: pd.DataFrame) -> np.ndarray:
    """Balkenweise Erlaubnis-Maske fuer EIN Symbol.

    Bildet dieselbe Zuordnung ab wie das `merge_asof(direction="backward")`
    der Bot-Funktion: zu jedem Balken zaehlt der letzte BTC-Regime-Eintrag
    mit `open_time <= Balkenzeit`. Balken vor dem ersten BTC-Eintrag gelten
    als NICHT erlaubt (kein Regime bekannt -> live gaebe es keinen
    Einstieg); in der Praxis liegen sie vor dem Warmup.

    Wird nur fuer die `sequential`-Gegenprobe gebraucht - die primaere
    Variante laeuft ueber die Bot-Funktion selbst.
    """
    reg = regime.sort_values("open_time")
    ref_times = reg["open_time"].to_numpy(dtype="datetime64[ns]")
    ref_dir = reg["btc_regime"].to_numpy()
    bars = np.asarray(open_times, dtype="datetime64[ns]")

    idx = np.searchsorted(ref_times, bars, side="right") - 1
    allowed = np.zeros(len(bars), dtype=bool)
    valid = idx >= 0
    allowed[valid] = ref_dir[idx[valid]] == 1
    return allowed
