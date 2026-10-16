"""TB-166 (E-3a) Werkzeugteil: aendert die 20 Dateien des Plans E-3a (PLAN_E3 2a) in einem Repo-Baum.
Aufruf: python3 -B e3a_patch.py <wurzel> [--probe]   --probe: nur pruefen, nichts schreiben.
Jede Ersetzung muss genau einmal treffen, sonst rc 2 und nichts geschrieben. Ausgabe: sha256 vorher/nachher je Datei."""
import hashlib, os, sys
W = sys.argv[1]; PROBE = "--probe" in sys.argv
FEHLER, NEU, VOR = [], {}, {}
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def lies(rel):
    if rel not in NEU:
        s = open(os.path.join(W, rel), encoding="utf-8").read(); VOR[rel] = sha(s); NEU[rel] = s
    return NEU[rel]
def ers(rel, alt, neu):
    s = lies(rel); k = s.count(alt)
    if k != 1: FEHLER.append("%s: %d Treffer fuer %r" % (rel, k, alt[:70])); return
    NEU[rel] = s.replace(alt, neu)
# --- 1 gemeinsame Tag-Rechnung (R90 (e)) -------------------------------------------------------
FSM = "research/faltenplan_neun/faltenschranke_messung.py"
HB = '''def handelbar_ab(bot: str, schnitt=None) -> dict:
    """TB-166 (E-3a; R87 (a)/(c), R90 (e), R98): der Handelbar-Tag je Symbol - EINE Rechnung
    fuer Wache, Benchmark (`benchmark.je_bot` ueber `loader_lesart`) und Schranke.

    Gerechnet an der Reihe OHNE Zeilen ab dem Schnitt (`schnitt`, Voreinstellung
    `faltenplan_neun.GO_LIVE`, ausschliesslich): Zeitspannen-Bots erster Kurstag +
    MIN_HISTORY_DAYS, Kerzen-Bot Datum der N-ten Kerze vor dem Schnitt. Ein Tag am oder
    nach dem Schnitt ist None - vor dem Schnitt nie handelbar. Fehlt die Datei: None.
    """
    schnitt = fp.GO_LIVE if schnitt is None else schnitt
    eig = fp.BOTS[bot]
    name, n = _min_history(bot)
    aus = {}
    for symbol in fp.symbole(eig["markt"]):
        pfad = fp.kursdatei(symbol, eig["zeitrahmen"])
        if not os.path.exists(pfad):
            aus[symbol] = None
            continue
        erster = nte = None
        zahl = 0
        with open(pfad, encoding="utf-8") as f:
            f.readline()
            for zeile in f:
                tag = fp._zeitstempel(zeile)
                if tag is None or tag >= schnitt:
                    continue
                if erster is None:
                    erster = tag
                zahl += 1
                if zahl == n:
                    nte = tag
        if name == "MIN_HISTORY_HOURS":
            t = nte
        else:
            t = None if erster is None else erster + dt.timedelta(days=n)
        aus[symbol] = t.isoformat() if t is not None and t < schnitt else None
    return aus


def loader_lesart(bot: str) -> dict:'''
ers(FSM, "def loader_lesart(bot: str) -> dict:", HB)
s = lies(FSM); a = s.index('    if name == "MIN_HISTORY_HOURS":\n        k = kerzen_elliott_wave()')
e_txt = '        aus["fensteranker"] = anker.isoformat() if anker else None\n'; e = s.index(e_txt, a) + len(e_txt)
NEU[FSM] = s[:a] + '''    # TB-166 (E-3a, R90 (e)): dieselbe Rechnung wie Wache und Schranke - an der Reihe
    # ohne Zeilen ab dem Schnitt; bis TB-166 rechnete hier eine eigene Schleife an der
    # ganzen Datei (Kerzen-Bot ueber kerzen_elliott_wave).
    aus["handelbar_ab"] = handelbar_ab(bot)
    if name != "MIN_HISTORY_HOURS":
        anker = fp.fensteranker(eig["markt"])
        aus["fensteranker"] = anker.isoformat() if anker else None
''' + s[e:]
# --- 2 sechs Backtests: Filter nach dem Ausstieg -> Wache (R90 (d)) -----------------------------
SECHS = ["strategies/rsi2_crypto/backtest_rsi2.py", "strategies/turtle_soup_crypto/backtest_turtle_soup.py",
         "strategies/volatility_breakout_crypto/backtest_breakout.py", "strategies/rsi2_mean_reversion/backtest_rsi2.py",
         "strategies/turtle_soup_stocks/backtest_turtle_soup.py", "strategies/volatility_breakout/backtest_breakout.py"]
FILTER = "        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):"
WACHE = '''        # TB-166 (E-3a, R90 (d)): Wache statt Streichen. Der Scan beginnt am ersten Balken
        # >= entry_cutoff (start_i oben); ein Einstieg davor ist ein Fehler im Signalpfad -
        # Abbruch mit Befund, kein Trade, der nach dem Ausstieg still entfaellt.
        if entry_cutoff is not None and entry_time < np.datetime64(entry_cutoff):
            sys.stderr.write("[%s] ABBRUCH (Wache R90 (d)): Einstieg %s vor entry_cutoff %s\\n"
                             % (__name__, entry_time, entry_cutoff))
            raise SystemExit(2)'''
for rel in SECHS:
    z = lies(rel).split("\n"); i = [k for k, l in enumerate(z) if l == FILTER]
    if len(i) != 1: FEHLER.append("%s: Filterzeile %d mal" % (rel, len(i))); continue
    i = i[0]; j = i + 1
    while j < len(z) and (z[j].strip() == "" or len(z[j]) - len(z[j].lstrip()) > 8): j += 1
    while z[j - 1].strip() == "": j -= 1
    NEU[rel] = "\n".join(z[:i] + WACHE.split("\n") + [l[4:] if l.strip() else l for l in z[i + 1:j]] + z[j:])
# --- 3 Durchreichung je Symbol (R98 (b)) ------------------------------------------------------
HELFER = '''
def _cutoff_je_symbol(entry_cutoffs, symbol):
    """TB-166 (E-3a, R98 (b)): entry_cutoff des Symbols aus `entry_cutoffs` ({symbol: Zeitpunkt},
    spaeterer von Horizontbeginn und Handelbar-Tag). Ohne `entry_cutoffs` None - die alte Bahn.
    Fehlt ein geladenes Symbol oder ist sein Wert None, hat es keinen Handelbar-Tag: Abbruch
    mit 2 (R81 (c)), kein stilles Weiterrechnen ohne Schranke."""
    if entry_cutoffs is None:
        return None
    wert = entry_cutoffs.get(symbol)
    if wert is None:
        sys.stderr.write("[equity_simulation] ABBRUCH: %s ohne entry_cutoff (kein Handelbar-Tag)\\n" % symbol)
        raise SystemExit(2)
    return wert

'''
EC = "entry_cutoff=_cutoff_je_symbol(entry_cutoffs, symbol)"
for rel, paare in {
    "strategies/rsi2_crypto/equity_simulation.py": [
        ("                        stop_loss_pct: float = None) -> pd.DataFrame:\n    all_trades = []",
         "                        stop_loss_pct: float = None, entry_cutoffs: dict = None) -> pd.DataFrame:\n    all_trades = []"),
        ("        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct)",
         "        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct,\n                                       " + EC + ")")],
    "strategies/turtle_soup_crypto/equity_simulation.py": [
        ("def collect_all_trades(all_data: dict, donchian_period: int, stop_mode=None) -> pd.DataFrame:",
         "def collect_all_trades(all_data: dict, donchian_period: int, stop_mode=None,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, donchian_period, stop_mode)",
         "        trades = get_trades_for_symbol(price_df, donchian_period, stop_mode,\n                                       " + EC + ")")],
    "strategies/volatility_breakout_crypto/equity_simulation.py": [
        ("                        squeeze_percentile: float = BB_SQUEEZE_PERCENTILE) -> pd.DataFrame:\n    all_trades = []",
         "                        squeeze_percentile: float = BB_SQUEEZE_PERCENTILE,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:\n    all_trades = []"),
        ("                                       squeeze_percentile=squeeze_percentile)\n        if not trades.empty:",
         "                                       squeeze_percentile=squeeze_percentile,\n                                       " + EC + ")\n        if not trades.empty:")],
    "strategies/elliott_wave/equity_simulation.py": [
        ("                        stop_loss_pct: float, take_profit_fib: float) -> pd.DataFrame:",
         "                        stop_loss_pct: float, take_profit_fib: float,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, deviation_pct)",
         "        trades = get_trades_for_symbol(price_df, deviation_pct, " + EC + ")")],
    "strategies/elliott_wave_stocks/equity_simulation.py": [
        ("                        take_profit_fib: float, use_take_profit: bool = True) -> pd.DataFrame:",
         "                        take_profit_fib: float, use_take_profit: bool = True,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit)",
         "        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit,\n                                       " + EC + ")")],
    "strategies/t3_supertrend/equity_simulation.py": [
        ("                        adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:",
         "                        adx_threshold: float, stop_loss_pct: float,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct)",
         "        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct,\n                                       " + EC + ")")],
}.items():
    ers(rel, "\ndef collect_all_trades(", HELFER + "\ndef collect_all_trades(")
    for a, n in paare: ers(rel, a, n)
# --- 4 Schranke im Scan: Elliott (2x), T3 (R90 (c), R98 (a)) --------------------------------
for b in ("elliott_wave", "elliott_wave_stocks"):
    rel = "strategies/%s/elliott_wave_counter.py" % b
    ers(rel, '                       freshness_bars: int = None, direction: str = "bearish") -> pd.DataFrame:',
        '                       freshness_bars: int = None, direction: str = "bearish",\n                       min_entry_idx: int = None) -> pd.DataFrame:')
    ers(rel, "                continue\n            traded.add(end_time)",
        "                continue\n"
        "            # TB-166 (E-3a, R90 (c), R98 (a)): Schranke im Scan - vor dem Handelbar-Tag\n"
        "            # (min_entry_idx: erster Balken >= entry_cutoff) kein Einstieg. VOR traded.add: die\n"
        "            # gesperrte Welle hinterlaesst keinen Zustand und kann an einem spaeteren Lauf\n"
        "            # >= min_entry_idx (noch frisch) einsteigen.\n"
        "            if min_entry_idx is not None and run_bar < min_entry_idx:\n"
        "                continue\n            traded.add(end_time)")
    rel = "strategies/%s/multi_symbol_optimise.py" % b
    if b == "elliott_wave":
        ers(rel, "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float) -> pd.DataFrame:",
            "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float,\n                          entry_cutoff=None) -> pd.DataFrame:")
    else:
        ers(rel, "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float, use_take_profit: bool = True) -> pd.DataFrame:",
            "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float, use_take_profit: bool = True,\n                          entry_cutoff=None) -> pd.DataFrame:")
    ers(rel, '        direction="bearish")   # Long-only, wie zuvor festgelegt',
        '        direction="bearish",   # Long-only, wie zuvor festgelegt\n'
        '        # TB-166 (E-3a, R98 (a)/(b)): Schranke je Symbol - erster Balken >= entry_cutoff\n'
        '        min_entry_idx=(None if entry_cutoff is None\n'
        '                       else int((price_df["open_time"] < entry_cutoff).sum())))')
BT = "strategies/t3_supertrend/backtest_trend.py"
ers(BT, "stop_loss_pct=STOP_LOSS_PCT, use_t3_exit=True, use_vwap_filter=False) -> pd.DataFrame:",
    "stop_loss_pct=STOP_LOSS_PCT, use_t3_exit=True, use_vwap_filter=False,\n                  entry_cutoff=None) -> pd.DataFrame:")
ers(BT, "    trades = []\n    position = None  # None oder dict mit entry-Infos",
    "    # TB-166 (E-3a, R90 (c), R98 (a)): Schranke im Scan - ein Einstieg erst ab dem ersten\n"
    "    # Balken >= entry_cutoff; Indikatoren ueber die ganze Reihe; vor dem Tag entsteht keine\n"
    "    # Position, also kein Zustand, der ein spaeteres Signal sperrt.\n"
    "    erster_einstieg = 0 if entry_cutoff is None else int((data[\"open_time\"] < entry_cutoff).sum())\n\n"
    "    trades = []\n    position = None  # None oder dict mit entry-Infos")
ers(BT, "            if crossed_up and adx[i] > adx_threshold and vwap_ok:",
    "            if crossed_up and adx[i] > adx_threshold and vwap_ok and i >= erster_einstieg:")
MT = "strategies/t3_supertrend/multi_symbol_optimise.py"
ers(MT, "                           adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:\n    if t3_fast >= t3_slow:",
    "                           adx_threshold: float, stop_loss_pct: float,\n                           entry_cutoff=None) -> pd.DataFrame:\n    if t3_fast >= t3_slow:")
ers(MT, "        stop_loss_pct=stop_loss_pct,\n    )", "        stop_loss_pct=stop_loss_pct,\n        entry_cutoff=entry_cutoff,  # TB-166 (E-3a)\n    )")
# --- 5 Erzeuger-Seite: bot_lauf.hole_trades(..., handelbar=) ---------------------------------
BL = "research/exposure_messung/bot_lauf.py"
ers(BL, "\n\ndef hole_trades(es, all_data):", '''

def _schranke_je_symbol(all_data, handelbar):
    """TB-166 (E-3a, R90 (e), R98 (b) (i)): entry_cutoff je Symbol = spaeterer von Horizontbeginn
    und Handelbar-Tag (`handelbar`: {symbol: Tag} aus faltenschranke_messung.handelbar_ab).
    Aktien-Bots mit Tupel {symbol: (df, Horizontbeginn)}: Tupel (df, max(...)); sonst
    {symbol: df} und {"entry_cutoffs": {symbol: ...}} fuer collect_all_trades. Ein geladenes
    Symbol ohne Tag: Abbruch mit 2 (R81 (c)). Der Tag folgt der Zeitzone der Spalte open_time."""
    neu, cut = {}, {}
    for symbol, wert in all_data.items():
        df, alt = wert if isinstance(wert, tuple) else (wert, None)
        tag = handelbar.get(symbol)
        if tag is None:
            sys.stderr.write("[bot_lauf] ABBRUCH: %s (%s) geladen, aber ohne Handelbar-Tag (R81 (c))\\n" % (symbol, BOT))
            raise SystemExit(2)
        tag = pd.Timestamp(tag)
        tz = getattr(df["open_time"].dt, "tz", None)
        if tz is not None and tag.tzinfo is None:
            tag = tag.tz_localize(tz)
        if BOT == "elliott_wave_stocks":
            import multi_symbol_optimise as mso   # Zeilen am Horizontbeginn gekappt (TB-163)
            alt = mso.horizontbeginn_ts(df["open_time"])
        c = tag if alt is None else max(alt, tag)
        if isinstance(wert, tuple):
            neu[symbol] = (df, c)
        else:
            neu[symbol] = df
            cut[symbol] = c
    return neu, ({"entry_cutoffs": cut} if cut else {})


def hole_trades(es, all_data, handelbar=None):''')
ers(BL, "    anwendet (`apply_btc_regime_filter`, eigener Kommentarblock dort).\"\"\"\n",
    "    anwendet (`apply_btc_regime_filter`, eigener Kommentarblock dort).\n\n"
    "    TB-166 (E-3a): mit `handelbar` traegt jeder Bot die Schranke je Symbol\n"
    "    (`_schranke_je_symbol`); ohne `handelbar` die alte Bahn, unveraendert.\"\"\"\n"
    "    kw = {}\n    if handelbar is not None:\n        all_data, kw = _schranke_je_symbol(all_data, handelbar)\n")
for a in ["es.TAKE_PROFIT_FIB)\n    if BOT == \"elliott_wave_stocks\":", "es.TAKE_PROFIT_FIB, es.USE_TAKE_PROFIT)",
          "es.ADX_THRESHOLD, es.STOP_LOSS_PCT)", "es.SMA_TREND_PERIOD,\n                                      es.STOP_LOSS_PCT)",
          "es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)", "trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)",
          "es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)", "return es.collect_all_trades(all_data, es.STOP_LOSS_PCT)"]:
    k = a.index(")"); ers(BL, a, a[:k] + ", **kw" + a[k:])
# --- Ende ------------------------------------------------------------------------------------
if FEHLER:
    print("\n".join("FEHLER " + f for f in FEHLER)); print("rc 2"); sys.exit(2)
for rel in sorted(NEU):
    if not PROBE:
        with open(os.path.join(W, rel), "w", encoding="utf-8") as f: f.write(NEU[rel])
    print("%s  vorher %s  nachher %s" % (rel, VOR[rel], sha(NEU[rel])))
print("Dateien: %d%s" % (len(NEU), " (Probe, nichts geschrieben)" if PROBE else "")); print("rc 0")
