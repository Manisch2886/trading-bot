"""TB-103 Block D: EIN Trockenlauf EINES Bots - Laden, Signalpfad, eine Simulation.

Was laeuft (unveraenderter Bot-Code, ueber dieselben Aufrufe wie
`research/exposure_messung/bot_lauf.py` / `research/tb24_haltedauern/
positionen_holen.py`):

  1. `equity_simulation.load_all_symbol_data()`  - Symbolliste + Kursdaten,
     mit dem Ladeprotokoll des Bots
  2. `bot_lauf.hole_trades(es, all_data)`        - der Signalpfad
     (`collect_all_trades` mit den Argumenten des Bots)
  3. `bot_lauf.simuliere(...)` EINMAL            - der Ausfuehrungspfad
     (Zuteilung), OHNE die Kennzeichnung aus positionen_holen (TB-98 Befund 2)

Was NICHT geschieht: nichts wird geschrieben ausser in den Scratchpad-Ordner
aus TB103_ZIEL; `bot_lauf.main()` und die `__main__`-Bloecke laufen nie.

Sichtschutz 27.1: die Zusammenfassung (JSON) enthaelt nur Mengen, Quellen und
Dateinamen - KEINE Trade-Zahl, keine Kennzahl. Alles, was der Bot in den
Schritten 2 und 3 auf stdout schreibt, geht in `rechnung_stdout.txt` im
Scratchpad (Rohprotokoll), nicht in die Zusammenfassung.

Er liegt im Repo, weil die Startpruefung des Selektionsmodus (shared/paths.py,
TB-58 Bedingung 1) den Einstiegspunkt unter derselben Git-Wurzel verlangt.

Aufruf (Repo-Wurzel; Modus-Variablen und Lesehaken per Umgebung):
    TB103_ZIEL=<leerer scratch-ordner> python3 docs/belege/TB-103/d_trockenlauf.py <bot>
"""
import contextlib
import io
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
ziel = os.environ["TB103_ZIEL"]
if not os.path.isdir(ziel) or os.listdir(ziel):
    raise SystemExit("TB103_ZIEL muss ein vorhandener, LEERER Ordner sein: %s" % ziel)
bot = sys.argv[1]
zusammenfassung = {"bot": bot}


def _schreibe():
    with open(os.path.join(ziel, "zusammenfassung.json"), "w", encoding="utf-8") as f:
        json.dump(zusammenfassung, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


# bot_lauf liest sys.argv[1] beim Import (Bot-Name) und setzt sys.path.
sys.argv = [os.path.join(_REPO, "research", "exposure_messung", "bot_lauf.py"), bot]
sys.path.insert(0, os.path.join(_REPO, "research", "exposure_messung"))
import bot_lauf as basis          # noqa: E402  (Stubs fuer binance/yfinance/fetch)
import equity_simulation as es    # noqa: E402

# --- Welche Symbolliste hat der Bot bekommen, und woher? ---------------------
quelle = None
for name in ("symbols_config", "stocks_symbols_config"):
    modul = sys.modules.get(name)
    if modul is not None and hasattr(modul, "SYMBOLS_FILE"):
        quelle = modul
        zusammenfassung["symbolliste_modul"] = os.path.relpath(modul.__file__, _REPO)
        break
if quelle is None:
    zusammenfassung["symbolliste_modul"] = None
    _schreibe()
    raise SystemExit("%s: kein symbols_config/stocks_symbols_config geladen" % bot)

datei = quelle.SYMBOLS_FILE
ausschluss = sorted(getattr(quelle, "EXCLUDE_SYMBOLS", set()))
zusammenfassung["symbolliste_datei"] = datei
zusammenfassung["symbolliste_datei_existiert"] = os.path.isfile(datei)
if os.path.isfile(datei):
    with open(datei, encoding="utf-8") as f:
        zeilen = [z.strip() for z in f if z.strip()]
else:
    zeilen = []
erwartet = [s for s in zeilen if s not in set(ausschluss)]
liste = list(quelle.SYMBOLS)
zusammenfassung.update({
    "universum_zeilen": len(zeilen),
    "exclude_symbols": ausschluss,
    "erwartet_nach_exclude": len(erwartet),
    "symbolliste_n": len(liste),
    "symbolliste_gleich_universum": liste == erwartet,
    "symbolliste_ist_standardliste": liste == list(getattr(quelle, "DEFAULT_SYMBOLS", [])),
})

# --- 1. Laden, mit Ladeprotokoll -------------------------------------------
puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    all_data = es.load_all_symbol_data()
ladeausgabe = puffer.getvalue()
sys.stdout.write(ladeausgabe)
geladen = sorted(all_data.keys()) if all_data else []
zusammenfassung.update({
    "geladen_n": len(geladen),
    "geladen_gleich_liste": geladen == sorted(liste),
    "nicht_geladen": sorted(set(liste) - set(geladen)),
    "geladen_nicht_in_liste": sorted(set(geladen) - set(liste)),
    "ladeprotokoll": [z for z in ladeausgabe.splitlines() if z.strip()],
    "summenzeile": [z for z in ladeausgabe.splitlines() if z.startswith("Geladen:")],
})
_schreibe()
if not all_data:
    raise SystemExit("%s: keine Kursdaten geladen" % bot)

# --- 2./3. Signalpfad und eine Simulation, Ausgabe nur ins Rohprotokoll -----
with open(os.path.join(ziel, "rechnung_stdout.txt"), "w", encoding="utf-8") as roh:
    with contextlib.redirect_stdout(roh):
        trades = basis.hole_trades(es, all_data)
        signalpfad = trades is not None and not trades.empty
        if signalpfad:
            hat_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
            limit = (getattr(es, "MAX_CONCURRENT_POSITIONS", None) if hat_limit
                     else basis._KEIN_LIMIT_PARAMETER)
            basis.simuliere(es, trades, es.ALLOCATION_PCT, limit)
zusammenfassung["signalpfad_gelaufen"] = True
zusammenfassung["simulation_gelaufen"] = bool(signalpfad)
_schreibe()
print("%s: Trockenlauf fertig (Laden, Signalpfad, %s)" % (
    bot, "eine Simulation" if signalpfad else "keine Simulation - Signalpfad leer"))
