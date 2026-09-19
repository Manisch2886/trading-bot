#!/usr/bin/env python3
"""
TB-30a - Registerdaten: die eingefrorenen Festlegungen als Datenstruktur
==============================================================================
Dieses Modul ist die **einzige Quelle** fuer alles, was die Vorregistrierung
festschreibt: Rastergrenzen und Grenzsaetze, Faltenplan, Selektionsstatistik,
Plateau- und Kantenregel, Drawdown-Bedingung, Abbruchkriterien, N-Buchfuehrung.
`docs/VORREGISTRIERUNG_neuselektion.md` beschreibt dieselben Festlegungen in
Prosa; die Zahlen dort werden aus diesem Modul erzeugt, nicht abgetippt.

WARUM DIE GRENZEN GERECHNET UND NICHT GETIPPT WERDEN
------------------------------------------------------------------------------
Die Vorregistrierung sichert zu, dass **kein Grenzsatz einen Live-Wert
erwaehnt**. Eine Zusicherung ueber getippte Zahlen liesse sich nur durch
Hinsehen pruefen. Deshalb ist hier keine Rastergrenze eine Zahl, sondern eine
**Regel** ueber eine in `messgroessen.py` gemessene Groesse:

    {"regel": "sigma_vielfaches", "zeitrahmen": "krypto_1d", "faktor": 0.5}

`pruefe_grenzsaetze.py` rechnet jede Regel nach, vergleicht sie mit dem
ausgewiesenen Wert und prueft zusaetzlich, dass keine Zahl im Begruendungssatz
mit einem Live-Wert dieses Bots zusammenfaellt. Ein Live-Wert kann so nur noch
durch **Zufall** in einer Grenze landen - und dieser Zufall faellt auf.

DIE VIER ZULAESSIGEN GRUNDLAGEN - UND ZWEI BENANNTE AUSNAHMEN
------------------------------------------------------------------------------
Zulaessig sind `kosten`, `datenfrequenz`, `volatilitaet`, `haltedauer`.

Zwei Grenzen stuetzen sich auf keine davon, und das steht hier ausdruecklich
statt verdeckt:

  `ableitung`  Die Obergrenze des Positionslimits ist `floor(1/ALLOCATION_PCT)`.
               Sie braucht keine Begruendung, weil sie keine Wahl ist: ein
               Rasterpunkt darueber IST derselbe Punkt (es lassen sich nicht
               mehr Positionen finanzieren). Die Regel steht so in der
               Aufgabenstellung.
  `methode`    Die Stufen des Fibonacci-Ziels sind die Retracement-Verhaeltnisse
               der Elliott-Methode. Sie sind eine Eigenschaft des Verfahrens,
               keine Einstellung - dieselbe Rolle wie die Kostenkonvention.

Beide Saetze nennen **keine Zahl**; die Werte stehen in einem getrennten Feld.
So kann auch hier kein Live-Wert in einem Satz auftauchen.
"""

import json
import math
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))

# Die Wurzel des Repos. Ueberschreibbar ueber TB30A_BASE_DIR - das brauchen
# die Mutationsproben aus `test_vorregistrierung.py`: sie kopieren DIESEN
# Ordner in ein Wegwerf-Verzeichnis, aendern dort eine Zeile und starten den
# Ablauf erneut. Ohne die Umgebungsvariable laege die Repo-Wurzel dann im
# Nichts, die Probe scheiterte am Import statt an der Mutation - und eine
# Probe, die aus dem falschen Grund scheitert, belegt nichts.
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))
sys.path.insert(0, os.path.join(BASE_DIR, "notifications"))

from manual_close import allokation  # noqa: E402  (nur lesend, reine Stdlib)

MESSGROESSEN_DATEI = os.path.join(_HIER, "ergebnisse", "messgroessen.json")

# ==============================================================================
# 1. Die zwoelf Festlegungen des Betreibers (14.09.2026)
# ==============================================================================
FESTLEGUNGEN = {
    1: ("Fuehrendes Mass", "Kapital-Drawdown aus equity_simulation.py"),
    2: ("Selektionsstatistik", "Median des Netto-Sharpe ueber die Selektionsfalten"),
    3: ("Beurteilung", "Netto-Calmar, Mittelwert der drei tiefsten Drawdowns, "
                       "Netto-Sharpe"),
    4: ("Drawdown-Bedingung je Falte",
        "erlaubt(f) = min(1,25 x DD_Benchmark(f), DD_Toleranz) - beide negativ, "
        "min ist der tiefere und damit grosszuegigere Wert"),
    5: ("DD_Toleranz",
        "Median der Benchmark-Drawdowns ueber alle Selektionsfalten, je Bot"),
    6: ("Keine absolute Drawdown-Grenze",
        "Eine feste Untergrenze bindet nur, wenn der Benchmark selbst unter "
        "-28 % faellt - dann aber fuer alle Parametersaetze gleichzeitig, und "
        "sie wirft den Bot aus, bevor gewaehlt wurde"),
    7: ("Schwelle fuer Zweijahres-Falten", "30 Trades je Jahr"),
    8: ("Spitzen-Schwelle der Plateau-Regel", "50 % ueber dem Nachbarschaftsmittel"),
    9: ("Cluster-Schwelle fuer N_eff", "Korrelation 0,9"),
    10: ("DSR-Basis", "N = 653, dieser Lauf zaehlt dazu"),
    11: ("DSR ist Bericht, nicht Tor",
         "Bleibt-Geht laeuft ueber die Abbruchkriterien"),
    12: ("Das zulaessige Ergebnis",
         "Es kann sein, dass kein einziger Bot die Schwelle erreicht. Eine "
         "Aussage ueber den Backtest, nicht ueber die Bots."),
}

# ==============================================================================
# 2. Konstanten der Selektion
# ==============================================================================
DD_RELATIVER_FAKTOR = 1.25          # Festlegung 4
SPITZEN_SCHWELLE = 0.50             # Festlegung 8: 50 % ueber dem Nachbarmittel
CLUSTER_SCHWELLE = 0.90             # Festlegung 9
DSR_BASIS_N = 653                   # Festlegung 10
ZWEIJAHRES_SCHWELLE_TRADES = 30     # Festlegung 7: Trades je Jahr
GO_LIVE_SCHNITT = "2026-09-01"      # siehe Abschnitt "Faltenplan" im Register
# Die erste Falte je Bot ist KEINE Konstante mehr (TB-56, 19.09.2026): sie
# entsteht aus der Datenlage nach Registertext 4a - siehe faltenplan.py,
# erste_falte(). Die frueher hier gefuehrte Schranke 2019 stand in keinem
# Registertext; die Tatsachennotiz 15.6 Punkt 2 hatte den Code-Zustand als
# Registerregel ausgegeben (Berichtigung nach F17, TB-56b).
MINDESTTRAINING_JAHRE = 4           # vor der ersten Falte
HANDELSTAGE_JE_JAHR = 252
RISIKOFREIER_SATZ = 0.0             # Netto-Sharpe ohne Zinsabzug - eine
                                    # Zinsannahme waere eine weitere Wahl

# N je Bot aus dem Versuchsregister (research/versuchsregister/REGISTER.md,
# Stand 13.09.2026, Spalte "verschiedene Kombinationen"). Summe 653.
N_HISTORISCH_JE_BOT = {
    "elliott_wave_stocks": 264,
    "elliott_wave": 252,
    "t3_supertrend": 81,
    "rsi2_crypto": 18,
    "turtle_soup_crypto": 12,
    "turtle_soup_stocks": 12,
    "rsi2_mean_reversion": 6,
    "volatility_breakout": 4,
    "volatility_breakout_crypto": 4,
}

# ==============================================================================
# 3. Die neun Bots
# ==============================================================================
BOTS = {
    "elliott_wave":               {"markt": "krypto", "zeitrahmen": "1h"},
    "t3_supertrend":              {"markt": "krypto", "zeitrahmen": "4h"},
    "rsi2_crypto":                {"markt": "krypto", "zeitrahmen": "1d"},
    "turtle_soup_crypto":         {"markt": "krypto", "zeitrahmen": "1d"},
    "volatility_breakout_crypto": {"markt": "krypto", "zeitrahmen": "1d"},
    "elliott_wave_stocks":        {"markt": "aktien", "zeitrahmen": "1d"},
    "rsi2_mean_reversion":        {"markt": "aktien", "zeitrahmen": "1d"},
    "turtle_soup_stocks":         {"markt": "aktien", "zeitrahmen": "1d"},
    "volatility_breakout":        {"markt": "aktien", "zeitrahmen": "1d"},
}

UNIVERSUM = {
    "krypto": "config/top25_symbols.txt",
    "aktien": "config/sp500_top150.txt",
}


def zeitrahmen_schluessel(bot: str) -> str:
    b = BOTS[bot]
    return f"{b['markt']}_{b['zeitrahmen']}"


def tagesschluessel(bot: str) -> str:
    """Der TAGES-Zeitrahmen des Marktes, in dem der Bot handelt.

    Die Stop-Grenzen ruhen auf dem Tages-Sigma, nicht auf dem Sigma des
    Bot-Balkens: ein Stop wirkt ueber die Haltedauer, nicht ueber einen
    Balken, und die Haltedauern aller neun Bots liegen in Tagen. So gilt fuer
    den Stundenbot dieselbe Regel wie fuer die Tagesbots - andere Zahl,
    gleiche Regel.
    """
    return f"{BOTS[bot]['markt']}_1d"


# ==============================================================================
# 4. Die Regelsprache der Rastergrenzen
# ==============================================================================
def _mess():
    with open(MESSGROESSEN_DATEI, encoding="utf-8") as f:
        return json.load(f)


def _vola(mess, zeitrahmen, feld):
    return mess["volatilitaet"][zeitrahmen][feld]


def regel_wert(regel: dict, mess: dict) -> float:
    """Rechnet eine Rastergrenze aus den gemessenen Groessen aus.

    Jede Grenze der Vorregistrierung geht durch diese Funktion. Wer eine
    Grenze aendern will, muss die REGEL aendern - eine Zahl laesst sich hier
    nicht unterbringen.
    """
    art = regel["regel"]
    if art == "kosten_vielfaches":
        return regel["faktor"] * mess["kosten"]["round_trip_pct"]
    if art == "sigma_vielfaches":
        return regel["faktor"] * _vola(mess, regel["zeitrahmen"], "balken_sigma_pct")
    if art == "spanne20":
        return _vola(mess, regel["zeitrahmen"], "spanne20_median_pct")
    if art == "hoechstens":
        return max(regel_wert(t, mess) for t in regel["terme"])
    if art == "horizont":
        # Balken, ueber die eine typische Bewegung ausgespielt ist:
        # sigma * sqrt(n) = Median der 20-Balken-Spanne  ->  n = (Spanne/sigma)^2
        sigma = _vola(mess, regel["zeitrahmen"], "balken_sigma_pct")
        spanne = _vola(mess, regel["zeitrahmen"], "spanne20_median_pct")
        return float(math.floor((spanne / sigma) ** 2))
    if art == "balken_je_jahr":
        return float(mess["datenfrequenz"]["balken_je_jahr"][regel["zeitrahmen"]])
    if art == "balken_je_handelswoche":
        return float(mess["datenfrequenz"]["balken_je_handelswoche"][regel["zeitrahmen"]])
    if art == "zwei_balken":
        # Kleinster Horizont, der ueberhaupt einer ist: ein Balken waere der
        # Ausstieg selbst, nicht eine Bremse.
        return 2.0
    if art == "zwei_positionen":
        # Ein Buch aus einer Position ist kein Buch.
        return 2.0
    if art == "median_prozent":
        # Der Median in Prozent - definitorisch, keine Wahl.
        return 50.0
    if art == "bollinger_fenster":
        # Das Bollinger-Fenster der Methode (20 Balken) - eine Eigenschaft des
        # Verfahrens, wie die Fibonacci-Leiter.
        return 20.0
    if art == "kleinstes_quantil_im_fenster":
        # Ein Quantil unterhalb von 100/Fenster waehlt weniger als einen Balken
        # aus - unterhalb dieser Schranke ist "Verengung" keine Aussage mehr.
        return 100.0 / regel_wert({"regel": "bollinger_fenster"}, mess)
    if art == "stopweite_structural":
        # Der gemessene Median des Abstands Schluss -> Tief desselben Balkens:
        # die Weite, die der "structural"-Stop im typischen Fall hat.
        return _vola(mess, regel["zeitrahmen"], "tiefabstand_median_pct")
    if art == "positionsdeckel":
        anteil = allokation(regel["bot"])["anteil"]
        if anteil is None:
            raise SystemExit(f"{regel['bot']}: ALLOCATION_PCT nicht lesbar")
        return float(math.floor(1.0 / anteil))
    if art == "haltedauer_median_balken":
        return float(math.ceil(mess["haltedauer"][regel["bot"]]["median_balken"]))
    if art == "quantil":
        tabelle = _vola(mess, regel["zeitrahmen"], regel["kennzahl"])
        return float(tabelle[str(regel["q"])])
    raise SystemExit(f"Unbekannte Regel: {art}")


def geometrische_stufen(unten: float, oben: float, stufen: int) -> list:
    """Geometrische Stufung fuer Skalenparameter.

    Der Faktor MUSS zwischen 1,5 und 2 liegen; sonst ist die Stufenzahl
    falsch gewaehlt und das Modul bricht ab. Damit kann keine Rasterachse
    still eine Stufung bekommen, die die Vorregistrierung nicht zulaesst.
    """
    if stufen < 3 or stufen > 5:
        raise SystemExit(f"Geometrische Stufung verlangt 3 bis 5 Stufen, nicht {stufen}")
    faktor = (oben / unten) ** (1.0 / (stufen - 1))
    if not (1.5 <= faktor <= 2.0):
        raise SystemExit(
            f"Geometrischer Faktor {faktor:.3f} liegt ausserhalb 1,5 bis 2,0 "
            f"(unten={unten}, oben={oben}, stufen={stufen})")
    return [round(unten * faktor ** k, 3) for k in range(stufen)]


def lineare_stufen(unten: float, oben: float, stufen: int) -> list:
    """Lineare Stufung fuer Zaehlparameter - ganzzahlig, ohne Wiederholung."""
    if stufen < 3 or stufen > 5:
        raise SystemExit(f"Lineare Stufung verlangt 3 bis 5 Stufen, nicht {stufen}")
    roh = [unten + (oben - unten) * k / (stufen - 1) for k in range(stufen)]
    werte = sorted({int(round(x)) for x in roh})
    if len(werte) != stufen:
        raise SystemExit(
            f"Lineare Stufung faellt nach dem Runden zusammen: {roh} -> {werte}")
    return werte


# ==============================================================================
# 5. Wiederverwendete Grenzen - dieselbe Regel, andere Zahl je Markt
# ==============================================================================
def _grenze(regel, grundlage, satz):
    return {"regel": regel, "grundlage": grundlage, "satz": satz}


def stop_achse(bot: str, mit_kein_stop: bool) -> dict:
    """Die Stop-Achse. Dieselbe Regel fuer alle neun Bots.

    Untergrenze 0,5 Tages-Sigma, Obergrenze 3 Tages-Sigma - der Bereich, in
    dem ein Stop ueberhaupt ein Stop ist.
    """
    zr = tagesschluessel(bot)
    achse = {
        "art": "geometrisch",
        "stufen": 4,
        "unten": _grenze(
            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 0.5},
            "volatilitaet",
            "Ein Stop enger als ein halbes Tages-Sigma des Universums wird vom "
            "gewoehnlichen Tagesrauschen ausgeloest und misst keine "
            "Strategieannahme mehr."),
        "oben": _grenze(
            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 3.0},
            "volatilitaet",
            "Ein Stop weiter als drei Tages-Sigma des Universums wird im "
            "typischen Verlauf nicht mehr erreicht - er ist dann keine "
            "Begrenzung, sondern eine Verzierung."),
    }
    if mit_kein_stop:
        achse["zusatzstufe"] = {
            "wert": None,
            "lage": "oben",
            "satz": "Die Strategie ist in ihrer Urfassung ohne Stop "
                    "beschrieben; 'kein Stop' ist der Grenzfall der Achse nach "
                    "oben und steht deshalb als oberste Stufe, nicht als "
                    "eigene Dimension.",
        }
    return achse


def positionslimit_achse(bot: str) -> dict:
    """Das Positionslimit. Obergrenze ist eine Ableitung, keine Wahl."""
    return {
        "art": "linear",
        "stufen": 4,
        "unten": _grenze(
            {"regel": "zwei_positionen"},
            "volatilitaet",
            "Bei einem Limit von einer Position ist die Kapitalkurve die Kurve "
            "eines einzelnen Titels; die Volatilitaet des Universums geht dann "
            "ungedaempft durch, und das Limit misst die Titelauswahl statt der "
            "Streuung."),
        "oben": _grenze(
            {"regel": "positionsdeckel", "bot": bot},
            "ableitung",
            "Mehr Positionen als Kehrwert der Positionsgroesse sind nicht "
            "finanzierbar; ein Rasterpunkt darueber ist derselbe Punkt."),
    }


def fibonacci_achse() -> dict:
    return {
        "art": "aufzaehlung",
        "werte": [0.236, 0.382, 0.5, 0.618, None],
        "grundlage": "methode",
        "satz": "Die Stufen sind die Retracement-Verhaeltnisse der "
                "Elliott-Methode, aufsteigend, und als Grenzfall nach oben das "
                "Weglassen des Ziels. Sie sind eine Eigenschaft des Verfahrens, "
                "keine Einstellung.",
    }


def deviation_achse(bot: str) -> dict:
    """Die Zigzag-Deviation. Dieselbe Regel in beiden Elliott-Varianten."""
    zr = zeitrahmen_schluessel(bot)
    return {
        "art": "geometrisch",
        "stufen": 4,
        "unten": _grenze(
            {"regel": "hoechstens", "terme": [
                {"regel": "kosten_vielfaches", "faktor": 2.0},
                {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 1.0},
            ]},
            "kosten",
            "Eine Deviation unter dem Zweifachen der Round-Trip-Kosten ist "
            "Rauschen, dessen Bewegung die Kosten nicht traegt; unter einem "
            "Balken-Sigma laesst sich ein Wendepunkt ausserdem nicht vom "
            "einzelnen Balken trennen. Es gilt die hoehere der beiden Schranken."),
        "oben": _grenze(
            {"regel": "spanne20", "zeitrahmen": zr},
            "volatilitaet",
            "Eine Deviation ueber dem Median der Zwanzig-Balken-Spanne erzeugt "
            "kaum noch Muster - die Bewegung, die sie verlangt, kommt im "
            "typischen Fenster nicht vor."),
    }


def horizont_achse(bot: str, unten_regel, unten_satz, unten_grundlage="datenfrequenz",
                   stufen=4) -> dict:
    zr = zeitrahmen_schluessel(bot)
    return {
        "art": "linear",
        "stufen": stufen,
        "unten": _grenze(unten_regel, unten_grundlage, unten_satz),
        "oben": _grenze(
            {"regel": "horizont", "zeitrahmen": zr},
            "volatilitaet",
            "Ueber diesen Horizont ist eine typische Bewegung ausgespielt: so "
            "viele Balken braucht das Balken-Sigma, um auf den Median der "
            "Zwanzig-Balken-Spanne anzuwachsen. Die Zahl steht bewusst "
            "ausgeschrieben - eine Ziffer im Grenzsatz koennte mit einem "
            "Live-Wert zusammenfallen, und die maschinelle Pruefung nimmt das "
            "nicht hin."),
    }


def donchian_achse(bot: str) -> dict:
    return horizont_achse(
        bot,
        {"regel": "haltedauer_median_balken", "bot": bot},
        "Ein Rueckblick kuerzer als die gemessene Median-Haltedauer dieses "
        "Bots ueberlebt die eigene Position nicht - das Muster, das den "
        "Einstieg begruendet, ist beim Ausstieg schon nicht mehr im Fenster.",
        unten_grundlage="haltedauer")


def sma_achse(bot: str) -> dict:
    zr = zeitrahmen_schluessel(bot)
    return {
        "art": "linear",
        "stufen": 5,
        "unten": _grenze(
            {"regel": "horizont", "zeitrahmen": zr},
            "volatilitaet",
            "Ein Trendfilter kuerzer als der Horizont, ueber den eine typische "
            "Bewegung ausgespielt ist, folgt dem eigenen Trade statt dem "
            "Marktzustand."),
        "oben": _grenze(
            {"regel": "balken_je_jahr", "zeitrahmen": zr},
            "datenfrequenz",
            "Ein Trendfilter ueber mehr als ein Kalenderjahr misst kein Regime "
            "mehr, sondern die Gesamtdrift des Universums."),
    }


def rsi_achse(bot: str) -> dict:
    zr = zeitrahmen_schluessel(bot)
    return {
        "art": "quantile",
        "kennzahl": "rsi2_quantile",
        "zeitrahmen": zr,
        "quantile": [1, 2, 5, 10],
        "grundlage": "volatilitaet",
        "satz": "Die Schwelle ist als Quantil der gemessenen RSI(2)-Verteilung "
                "des Universums gesetzt: unten das Quantil, unter dem im Mittel "
                "nur jeder hundertste Balken liegt (seltener laesst sich kein "
                "Einstieg mehr bewerten), oben das Quantil, ab dem jeder zehnte "
                "Balken ein Signal waere und die Schwelle nichts mehr aussortiert.",
    }


def adx_achse(bot: str) -> dict:
    zr = zeitrahmen_schluessel(bot)
    return {
        "art": "quantile",
        "kennzahl": "adx_quantile",
        "zeitrahmen": zr,
        "quantile": [50, 60, 70, 80],
        "grundlage": "volatilitaet",
        "satz": "Die Schwelle ist als Quantil der gemessenen ADX-Verteilung des "
                "Universums gesetzt: unter dem Median verwirft der Filter "
                "nichts, ueber dem Vierfuenftel-Quantil verwirft er mehr als "
                "vier Fuenftel aller Balken und laesst zu wenige Einstiege "
                "uebrig, um ihn zu bewerten.",
    }


# ==============================================================================
# 6. Die neun Raster
# ==============================================================================
def raster_definition() -> dict:
    """Ein Raster je Bot, identisch ueber alle Falten.

    Aufgenommen sind genau die Parameter, die der jeweilige Bot heute schon
    rastert, dazu das Positionslimit - und dort, wo die Aktien- und die
    Krypto-Variante bisher verschiedene Parameter rasterten, die Vereinigung
    beider, damit ueberall DIESELBE Regel gilt. Parameter, die dieses Projekt
    noch nie ausgewaehlt hat (etwa die Zeitbremse), bleiben bewusst draussen:
    jede zusaetzliche Achse multipliziert N und damit den Abschlag der DSR.
    """
    d = {}

    d["elliott_wave"] = {
        "deviation_pct": deviation_achse("elliott_wave"),
        "stop_loss_pct": stop_achse("elliott_wave", mit_kein_stop=False),
        "take_profit_fib": fibonacci_achse(),
        # KEIN Positionslimit - und das ist eine eingetragene Ausnahme, kein
        # Vergessen. `strategies/elliott_wave/equity_simulation.py` fuehrt als
        # einziger der neun kein `max_concurrent_positions`; zwoelf Stellen im
        # Repo erkennen an genau dieser Signatur, welcher Bot keines hat
        # (Protokoll Abschnitt 8, TB-26/TB-28). Die Achse nachzuruesten waere
        # eine Aenderung an Bot-Code und damit TB-30b - und sie waere hier
        # ohnehin die Aenderung einer dokumentierten Entscheidung.
        "_ausnahme": {
            "achse": "max_concurrent_positions",
            "grund": "equity_simulation.py dieses Bots fuehrt kein "
                     "max_concurrent_positions; die Signatur ist im Protokoll "
                     "Abschnitt 8 ausdruecklich so entschieden.",
            "folge": "Das Buch dieses Bots ist allein durch Kapital begrenzt, "
                     "also durch floor(1/ALLOCATION_PCT). Der Bot wird mit "
                     "dieser Schranke gerechnet und in der Beurteilung mit der "
                     "Markierung 'ohne Limitachse' gefuehrt.",
        },
    }
    d["elliott_wave_stocks"] = {
        "deviation_pct": deviation_achse("elliott_wave_stocks"),
        "stop_loss_pct": stop_achse("elliott_wave_stocks", mit_kein_stop=False),
        "take_profit_fib": fibonacci_achse(),
        "max_concurrent_positions": positionslimit_achse("elliott_wave_stocks"),
    }
    d["t3_supertrend"] = {
        "t3_fast_length": horizont_achse(
            "t3_supertrend", {"regel": "zwei_balken"},
            "Unter zwei Balken glaettet eine Glaettung nicht mehr - sie "
            "wiederholt den Kurs."),
        "t3_slow_length": horizont_achse(
            "t3_supertrend", {"regel": "zwei_balken"},
            "Unter zwei Balken glaettet eine Glaettung nicht mehr - sie "
            "wiederholt den Kurs."),
        "adx_threshold": adx_achse("t3_supertrend"),
        "stop_loss_pct": stop_achse("t3_supertrend", mit_kein_stop=False),
        "max_concurrent_positions": positionslimit_achse("t3_supertrend"),
        "_bedingung": "t3_fast_length < t3_slow_length",
    }
    for bot in ("rsi2_crypto", "rsi2_mean_reversion"):
        d[bot] = {
            "rsi_threshold": rsi_achse(bot),
            "sma_trend_filter": sma_achse(bot),
            "stop_loss_pct": stop_achse(bot, mit_kein_stop=True),
            "max_concurrent_positions": positionslimit_achse(bot),
        }
    for bot in ("turtle_soup_crypto", "turtle_soup_stocks"):
        d[bot] = {
            "donchian_period": donchian_achse(bot),
            "stop_mode": stop_achse(bot, mit_kein_stop=True),
            "max_concurrent_positions": positionslimit_achse(bot),
        }
        d[bot]["stop_mode"]["zusatzstufe_gemessen"] = {
            "wert": "structural",
            "weite_regel": {"regel": "stopweite_structural",
                            "zeitrahmen": tagesschluessel(bot)},
            "satz": "Der Stop auf dem Tief des Setup-Balkens hat keine "
                    "eingestellte Weite; er steht auf der Achse an der Stelle, "
                    "die seiner GEMESSENEN Median-Weite entspricht - dem Median "
                    "des Abstands Schluss zu Tief desselben Balkens. Wo das "
                    "ist, rechnet das Register aus, es behauptet es nicht."}
    for bot in ("volatility_breakout", "volatility_breakout_crypto"):
        d[bot] = {
            "bb_squeeze_percentile": {
                "art": "linear", "stufen": 4,
                "unten": _grenze(
                    {"regel": "kleinstes_quantil_im_fenster"}, "datenfrequenz",
                    "Unterhalb von hundert geteilt durch das Bollinger-Fenster "
                    "waehlt das Quantil weniger als einen Balken aus - dort ist "
                    "'Verengung' keine Aussage ueber das Fenster mehr."),
                "oben": _grenze(
                    {"regel": "median_prozent"}, "ableitung",
                    "Ueber dem Median ist die Verengung keine mehr: die Haelfte "
                    "aller Balken erfuellte die Bedingung."),
            },
            "bb_lookback": {
                "art": "linear", "stufen": 4,
                "unten": _grenze(
                    {"regel": "bollinger_fenster"}, "methode",
                    "Ein Rueckblick, der kuerzer ist als das Bollinger-Fenster "
                    "selbst, vergleicht die Bandbreite mit sich selbst."),
                "oben": _grenze(
                    {"regel": "balken_je_jahr",
                     "zeitrahmen": zeitrahmen_schluessel(bot)},
                    "datenfrequenz",
                    "Ueber ein Kalenderjahr hinaus vergleicht der Rueckblick "
                    "Marktphasen, nicht Verengungen."),
            },
            "stop_loss_pct": stop_achse(bot, mit_kein_stop=True),
            "max_concurrent_positions": positionslimit_achse(bot),
        }
    return d


def achse_werte(achse: dict, mess: dict) -> list:
    """Die Stufen einer Achse - gerechnet, nie getippt."""
    art = achse["art"]
    if art == "aufzaehlung":
        return list(achse["werte"])
    if art == "quantile":
        tab = mess["volatilitaet"][achse["zeitrahmen"]][achse["kennzahl"]]
        return [round(float(tab[str(q)]), 3) for q in achse["quantile"]]
    unten = regel_wert(achse["unten"]["regel"], mess)
    oben = regel_wert(achse["oben"]["regel"], mess)
    if art == "geometrisch":
        werte = geometrische_stufen(unten, oben, achse["stufen"])
    elif art == "linear":
        werte = lineare_stufen(unten, oben, achse["stufen"])
    else:
        raise SystemExit(f"Unbekannte Achsenart: {art}")
    if "zusatzstufe_gemessen" in achse:
        # Eine Stufe ohne eingestellte Weite wird an der Stelle einsortiert,
        # die ihrer gemessenen Median-Weite entspricht. Bei Gleichstand steht
        # sie VOR der gerechneten Stufe - reproduzierbar, ohne Zufall.
        zusatz = achse["zusatzstufe_gemessen"]
        weite = regel_wert(zusatz["weite_regel"], mess)
        pos = sum(1 for w in werte if w < weite)
        werte = werte[:pos] + [zusatz["wert"]] + werte[pos:]
    if "zusatzstufe" in achse:
        werte = werte + [achse["zusatzstufe"]["wert"]]
    return werte


def raster(mess=None) -> dict:
    """Das fertige Raster je Bot: Achsenname -> Liste der Stufen."""
    mess = mess or _mess()
    aus = {}
    for bot, achsen in raster_definition().items():
        aus[bot] = {name: achse_werte(a, mess)
                    for name, a in achsen.items() if not name.startswith("_")}
    return aus


def zellen(bot: str, mess=None) -> int:
    """Die Zahl der Rasterzellen eines Bots - das N dieses Laufs."""
    mess = mess or _mess()
    r = raster(mess)[bot]
    definition = raster_definition()[bot]
    n = 1
    for name, werte in r.items():
        n *= len(werte)
    if definition.get("_bedingung") == "t3_fast_length < t3_slow_length":
        # Zellen, in denen die Strategie nicht definiert ist, existieren nicht.
        schnell = r["t3_fast_length"]
        langsam = r["t3_slow_length"]
        gueltig = sum(1 for a in schnell for b in langsam if a < b)
        n = n // (len(schnell) * len(langsam)) * gueltig
    return n


def main():
    mess = _mess()
    r = raster(mess)
    print(__doc__.strip().split("\n")[0])
    gesamt = 0
    for bot in BOTS:
        n = zellen(bot, mess)
        gesamt += n
        print(f"\n{bot}  ({BOTS[bot]['markt']}, {BOTS[bot]['zeitrahmen']}) - "
              f"{n} Zellen")
        for name, werte in r[bot].items():
            print(f"    {name:26s} {werte}")
    print(f"\nZellen dieses Laufs insgesamt: {gesamt}")
    print(f"N historisch (Versuchsregister): {DSR_BASIS_N}")
    print(f"N nominal gesamt:                {DSR_BASIS_N + gesamt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
