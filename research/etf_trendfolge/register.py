#!/usr/bin/env python3
"""
S-B1 - Die eingefrorenen Festlegungen als Code (TB-39)
==============================================================================
`S-B1` ist die Multi-Asset-ETF-Trendfolge: ETFs ueber Aktien, Zinsen, Kredit,
Metalle, Rohstoffe und Waehrungen, 3/6/12-Monats-Mehrheitssignal, inverse
Volatilitaetsgewichtung, Kasse als Rest, monatliche Umschichtung.

**Sie ist noch kein Bot.** Dieser Ordner rechnet KEINEN Backtest, KEINE
Ertragszahl und KEINE Sharpe-Zahl. Er beschafft Daten, legt Rastergrenzen
fest und schreibt das Register - alles Schritte, die NICHTS auswaehlen.
Der Backtest gehoert hinter Rang 1 der Reparaturkette, und jede Zahl, die
vorher gerechnet wuerde, waere eine Beobachtung, von der hinterher niemand
belegen koennte, dass sie die Festlegung nicht beeinflusst hat.

WARUM JEDE ZAHL GENAU HIER STEHT
------------------------------------------------------------------------------
Dieses Projekt hat schon einmal eine doppelt gefuehrte Zahl leise
auseinanderlaufen lassen (CLAUDE.md). Jede Festlegung von `S-B1` steht
deshalb in diesem Modul - genau einmal - und wird ueberall sonst importiert.
Das Registerdokument `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` erzaehlt,
WARUM sie so lautet; die Zahl selbst steht hier.

REINE STANDARDBIBLIOTHEK
------------------------------------------------------------------------------
Kein pandas, kein numpy, kein yfinance. Dasselbe Werkzeug laeuft in der
Cloud (wo yfinance gesperrt ist und pandas fehlt) und auf dem Rechner des
Betreibers. Einzige Ausnahme ist `datenlauf.py`, der yfinance BRAUCHT und
deshalb nur am Mac laeuft.

WAS AUS FREMDEN MODULEN KOMMT - UND WARUM NICHT ABGESCHRIEBEN
------------------------------------------------------------------------------
  Stufungsregel        `research/vorregistrierung/registerdaten.py`
                       (geometrisch, Faktor 1,5 bis 2,0, drei bis fuenf
                       Stufen). Sie ist eine Methodikregel des Projekts,
                       keine Zahl der Neuselektion. Abschreiben hiesse, sie
                       ein zweites Mal zu fuehren; der Selbsttest haelt die
                       erzeugten Stufen zusaetzlich auf ihren Literalen fest,
                       damit eine Aenderung drueben hier ROT wird statt still
                       durchzuschlagen.
  Datenstand-Hash      `research/vorregistrierung/herkunft.py::datenstand`
  Entscheidungskerze   `shared/entscheidungskerze.py`
"""

import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB39_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

def lade_fremdes_modul(name, pfad):
    """Ein Modul aus einem ANDEREN Ordner laden, ohne dessen Ordner auf
    `sys.path` zu legen.

    Der Grund ist eine Falle, die dieses Projekt schon kennt: gleichnamige
    Dateien in verschiedenen Ordnern verdecken einander in `sys.modules`
    (CLAUDE.md, neun gleichnamige `equity_simulation.py`). Es gibt ein
    `research/vorregistrierung/beispieldaten.py` UND ein
    `research/etf_trendfolge/beispieldaten.py`; laege der fremde Ordner auf
    dem Pfad, bekaeme dieser Ordner beim Import das falsche.

    Der Name traegt deshalb ein Praefix, und der fremde Ordner bleibt
    draussen.
    """
    import importlib.util                                   # noqa: PLC0415

    voll = f"_tb39_{name}"
    if voll in sys.modules:
        return sys.modules[voll]
    spec = importlib.util.spec_from_file_location(voll, pfad)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{pfad} laesst sich nicht laden.")
    modul = importlib.util.module_from_spec(spec)
    sys.modules[voll] = modul
    spec.loader.exec_module(modul)
    return modul


VORREGISTRIERUNG_DIR = os.path.join(BASE_DIR, "research", "vorregistrierung")

registerdaten = lade_fremdes_modul(
    "registerdaten", os.path.join(VORREGISTRIERUNG_DIR, "registerdaten.py"))


# ===========================================================================
# 1. Wohin die Kursdateien gehen - und wohin NICHT
# ===========================================================================
# Die Randbedingung, an der diese Aufgabe scheitern koennte: der
# Datenstand-Hash der Vorregistrierung ist der SHA-256 ueber die Dateien in
# `data/`. EINE zusaetzliche Datei dort aendert ihn und entwertet den
# registrierten Zustand, bevor der Selektionslauf stattgefunden hat.
#
# `daten/` liegt deshalb unter DIESEM Ordner und ist gitignoriert. Das ist
# nicht Vorsicht, sondern Trennung: was nicht im Repo liegt, kann bei keinem
# Merge nach `data/` wandern. `datenstand.py` weist die Unveraenderlichkeit
# am Verhalten nach, nicht durch Zusicherung.
DATEN_DIR = os.path.join(_HIER, "daten")
ERGEBNIS_DIR = os.path.join(_HIER, "ergebnisse")
KURSDATEN_DIR_VERBOTEN = os.path.join(BASE_DIR, "data")

# Der Stand, der fuer die Neuselektion gilt (Vorregistrierung Abschnitt 10,
# Tatsachennotiz vom 15.09.2026). Vor und nach TB-39 identisch.
DATENSTAND_SOLL = ("d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7"
                   "ccfcea995f84")
DATENSTAND_DATEIEN_SOLL = 223


# ===========================================================================
# 2. Die Kandidatenliste
# ===========================================================================
# Sechs Anlageklassen. Die Reihenfolge ist die Reihenfolge des Berichts und
# hat keine Bedeutung darueber hinaus.
KLASSEN = ("Aktien", "Zinsen", "Kredit", "Metalle", "Rohstoffe", "Waehrungen")

# `erwartete_auflage` ist AUSDRUECKLICH KEINE MESSUNG. Sie steht hier, damit
# `historie.py` das gemessene erste Datum dagegenhalten und eine Abweichung
# MELDEN kann. Was zaehlt, ist immer die Messung; die Erwartung ist eine
# Wache gegen ein stillschweigend falsches Symbol (ein Tippfehler im Ticker
# liefert eine gueltige, aber falsche Reihe).
KANDIDATEN = (
    {"symbol": "SPY", "klasse": "Aktien",
     "was": "US-Standardwerte", "erwartete_auflage": "1993-01-29"},
    {"symbol": "IWM", "klasse": "Aktien",
     "was": "US-Nebenwerte", "erwartete_auflage": "2000-05-26"},
    {"symbol": "EFA", "klasse": "Aktien",
     "was": "entwickelte Maerkte ausser USA",
     "erwartete_auflage": "2001-08-21"},
    {"symbol": "EEM", "klasse": "Aktien",
     "was": "Schwellenlaender", "erwartete_auflage": "2003-04-14"},
    {"symbol": "IEF", "klasse": "Zinsen",
     "was": "US-Staatsanleihen 7-10 Jahre", "erwartete_auflage": "2002-07-26"},
    {"symbol": "TLT", "klasse": "Zinsen",
     "was": "US-Staatsanleihen 20+ Jahre", "erwartete_auflage": "2002-07-26"},
    {"symbol": "LQD", "klasse": "Kredit",
     "was": "Unternehmensanleihen guter Bonitaet",
     "erwartete_auflage": "2002-07-26"},
    {"symbol": "HYG", "klasse": "Kredit",
     "was": "Hochzinsanleihen", "erwartete_auflage": "2007-04-11"},
    {"symbol": "GLD", "klasse": "Metalle",
     "was": "Gold", "erwartete_auflage": "2004-11-18"},
    {"symbol": "SLV", "klasse": "Metalle",
     "was": "Silber", "erwartete_auflage": "2006-04-28"},
    {"symbol": "DBC", "klasse": "Rohstoffe",
     "was": "breiter Rohstoffkorb", "erwartete_auflage": "2006-02-03"},
    {"symbol": "DBA", "klasse": "Rohstoffe",
     "was": "Agrarrohstoffe", "erwartete_auflage": "2007-01-05"},
    {"symbol": "FXE", "klasse": "Waehrungen",
     "was": "Euro gegen US-Dollar", "erwartete_auflage": "2005-12-09"},
    {"symbol": "FXY", "klasse": "Waehrungen",
     "was": "japanischer Yen gegen US-Dollar",
     "erwartete_auflage": "2007-02-13"},
)

# Die Untergrenze. Darunter degeneriert S-B1 zu Aktien-Timing mit Beiwerk -
# dann wird sie NICHT gebaut, und das ist ein zulaessiges Ergebnis.
UNTERGRENZE_INSTRUMENTE = 8
UNTERGRENZE_KLASSEN = 4

# Der Zeitraum ist nicht beliebig gewaehlt: er muss die Finanzkrise 2008
# enthalten, sonst hat eine Trendfolgestrategie nie einen echten Baerenmarkt
# gesehen.
HISTORIE_AB = "2007-01-01"

# Der Vorbehalt, der ins Register gehoert - nach dem Muster von Registertext
# 3c der Neuselektion, mit VORHERGESAGTER RICHTUNG.
SURVIVORSHIP_VORBEHALT = (
    "Die Kandidatenliste ist HEUTE zusammengestellt, also mit dem Wissen, "
    "welche ETFs es heute noch gibt. Aufgeloeste und verschmolzene Fonds "
    "sind darin nicht enthalten. Erwartete Richtung: Bevorzugung von "
    "Anlageklassen, deren Produkte die Finanzkrise ueberlebt haben - also "
    "der breiten, liquiden Koerbe gegenueber engen Nischenprodukten, und "
    "damit eine ZU GUENSTIGE Einschaetzung der Diversifikationsbreite, die "
    "S-B1 im Jahr 2008 tatsaechlich haette herstellen koennen; Groesse "
    "unbekannt. Die Bestaetigungsperiode unterliegt dieser Verzerrung nicht."
)


# ===========================================================================
# 3. Die Frequenzen - woraus alle Fensterlaengen abgeleitet sind
# ===========================================================================
# 252 ist die Konvention dieses Projekts (Falten-Sharpe x Wurzel 252,
# Vorregistrierung Abschnitt 15.3). Alles andere wird daraus GERECHNET,
# nicht getippt.
HANDELSTAGE_JE_JAHR = 252
MONATE_JE_JAHR = 12
HANDELSTAGE_JE_MONAT = HANDELSTAGE_JE_JAHR // MONATE_JE_JAHR      # 21


def monate_in_handelstagen(monate: int) -> int:
    """Monate -> Handelstage. EINE Umrechnung im ganzen Ordner."""
    return int(monate) * HANDELSTAGE_JE_MONAT


# ===========================================================================
# 4. Das Signal - FEST, nicht im Raster
# ===========================================================================
# Die drei Fenster stammen aus der Literatur (Zeitreihen-Momentum ueber drei,
# sechs und zwoelf Monate, Mehrheitsentscheid). Sie ins Raster zu stellen
# haette zwei Folgen, und beide sind teuer: N waechst, und die Herkunft "aus
# der Literatur" geht verloren - eine gewaehlte Fensterlaenge ist keine
# uebernommene mehr.
SIGNALFENSTER_MONATE = (3, 6, 12)
SIGNALFENSTER_TAGE = tuple(monate_in_handelstagen(m)
                           for m in SIGNALFENSTER_MONATE)        # 63,126,252

# "Mehrheit" von drei Fenstern ist zwei. Das ist keine Wahl, sondern das,
# was das Wort bedeutet.
SIGNAL_MEHRHEIT = len(SIGNALFENSTER_MONATE) // 2 + 1             # 2

# Das Signalmass: Vorzeichen der Rendite ueber das Fenster. Die Alternative
# (Kurs ueber gleitendem Durchschnitt) ist ein ANDERES Verfahren, kein
# anderer Wert - sie steht als Robustheitsbild ohne Weg ins Urteil.
SIGNALMASS = "vorzeichen_der_fensterrendite"


# ===========================================================================
# 5. Die Gewichtung - die EINZIGE offene Zahl der Strategie
# ===========================================================================
# Inverse Volatilitaet: w_i proportional zu 1/sigma_i, ueber ALLE Kandidaten
# normiert, die an diesem Umschichtungstag im Universum sind. Ein Instrument
# ohne Signal steht mit seinem Gewicht in der Kasse - "Kasse als Rest",
# woertlich genommen.
GEWICHTUNG = "inverse_volatilitaet"
VOLATILITAETSMASS = "standardabweichung_taeglicher_renditen"

# Kein Gewichtsdeckel. Begruendung im Register: ein Deckel waere eine zweite
# freie Zahl ohne Vorbild in der Literatur, und die Konzentration ist bei
# mindestens acht Instrumenten durch die Bauart schon begrenzt.
GEWICHTSDECKEL = None

# Die Rasterachse. Grundlage `datenfrequenz`: der Rueckblick reicht vom
# Doppelten des Umschichtungsabstands bis zum laengsten Signalfenster.
# Der Satz nennt KEINE Zahl - die Werte stehen im getrennten Feld darunter,
# genau wie in Abschnitt 2.2 der Neuselektion.
VOL_RUECKBLICK_GRENZSATZ = {
    "regel": "vielfaches_des_umschichtungsabstands",
    "grundlage": "datenfrequenz",
    "satz": ("Der Volatilitaets-Rueckblick reicht vom Doppelten des "
             "Umschichtungsabstands bis zum laengsten Signalfenster. "
             "Geometrisch gestuft nach der Projektregel."),
    "unten": 2 * HANDELSTAGE_JE_MONAT,
    "oben": max(SIGNALFENSTER_TAGE),
    "stufen": 5,
}


def _ganzzahlige_stufen(unten, oben, stufen):
    """Geometrische Stufung, auf Handelstage gerundet.

    Die Stufungsregel selbst kommt aus `registerdaten.geometrische_stufen`
    (Faktor 1,5 bis 2,0, drei bis fuenf Stufen) - sie wird hier NICHT
    wiederholt, nur angewandt. Gerundet wird danach, und fallen zwei Stufen
    dabei zusammen, bricht das Modul ab: ein Raster mit einer doppelten
    Zelle zaehlt eine Zelle zweimal.
    """
    roh = registerdaten.geometrische_stufen(unten, oben, stufen)
    werte = [int(round(x)) for x in roh]
    if len(set(werte)) != len(werte):
        raise SystemExit(
            f"Die Stufen fallen nach dem Runden zusammen: {roh} -> {werte}")
    return tuple(werte)


VOL_RUECKBLICK_TAGE = _ganzzahlige_stufen(
    VOL_RUECKBLICK_GRENZSATZ["unten"],
    VOL_RUECKBLICK_GRENZSATZ["oben"],
    VOL_RUECKBLICK_GRENZSATZ["stufen"])


# Der Vorlauf, den ein Instrument braucht, bevor es ueberhaupt ein Signal
# tragen kann: das laengste Signalfenster bzw. der laengste Vol-Rueckblick,
# je nachdem, welcher laenger ist. GERECHNET aus den Achsen, nicht getippt -
# wer eine Achse verlaengert, verlaengert damit den Vorlauf.
VORLAUF_TAGE = max(max(SIGNALFENSTER_TAGE), max(VOL_RUECKBLICK_TAGE))

# Wann ein Instrument ins Universum tritt. Es fehlt vorher schlicht - es
# steht nicht mit Gewicht 0 da, sondern gar nicht; die inversen
# Volatilitaetsgewichte werden ueber die anwesenden Instrumente normiert.
UNIVERSUM_EINTRITT = (
    "Ein Instrument ist ab dem Umschichtungstag im Universum, an dem es "
    "VORLAUF_TAGE abgeschlossene Handelstage hinter sich hat. Vorher fehlt "
    "es; die Gewichte werden ueber die anwesenden Instrumente normiert."
)

# Der Stichtag, an dem die Untergrenze geprueft wird: der Beginn der ersten
# Selektionsfalte. Abgeleitet aus HISTORIE_AB - das Jahr 2007 ist die
# Datenanforderung, die erste Falte ist das Jahr darauf, weil der Vorlauf
# dazwischenliegt.
ERSTE_SELEKTIONSFALTE = int(HISTORIE_AB[:4]) + 1
UNTERGRENZE_STICHTAG = f"{ERSTE_SELEKTIONSFALTE}-01-01"



# ===========================================================================
# 6. Die Kasse
# ===========================================================================
# Das Projekt hat am 15.09.2026 entschieden, freies Kapital NICHT zu
# verzinsen. Hier gilt dieselbe Festlegung. Sie ist konservativ: eine
# Verzinsung schriebe der Strategie einen Ertrag gut, den sie nicht
# erwirtschaftet, und zwar ausgerechnet in den Zeiten, in denen sie am
# meisten Kasse haelt.
KASSE_VERZINST = False
KASSE_ZINSSATZ_PA = 0.0


# ===========================================================================
# 7. Die Umschichtung
# ===========================================================================
# Entschieden wird auf der Entscheidungskerze des LETZTEN Handelstags des
# Kalendermonats - der letzten Kerze, deren Zeitraum vor der Startzeit des
# Laufs endete (TB-38, `shared/entscheidungskerze.py`). Ausgefuehrt wird zur
# EROEFFNUNG des ersten Handelstags des Folgemonats.
#
# Warum nicht zum Schluss des Entscheidungstags: dieser Schluss IST die
# Entscheidungsgrundlage. Zu ihm zu handeln hiesse, auf einen Kurs zu
# handeln, den man im Augenblick der Entscheidung noch nicht kennt - genau
# der Vorgriff, den TB-38 fuer die neun Bots beseitigt hat.
UMSCHICHTUNG = "monatlich"
UMSCHICHTUNG_ENTSCHEIDUNGSTAG = "letzter_handelstag_des_kalendermonats"
UMSCHICHTUNG_AUSFUEHRUNG = "eroeffnung_des_ersten_handelstags_des_folgemonats"
UMSCHICHTUNGEN_JE_JAHR = MONATE_JE_JAHR


# ===========================================================================
# 8. Kosten - dieselbe Konvention wie ueberall
# ===========================================================================
# TRADING_FEE_PCT 0,1 + SLIPPAGE_PCT 0,05 je Order. Ein Round Trip sind zwei
# Orders, also 0,30 Prozentpunkte.
KOSTEN_JE_ORDER_PCT = 0.15
KOSTEN_JE_ROUNDTRIP_PCT = 2 * KOSTEN_JE_ORDER_PCT                 # 0,30


# ===========================================================================
# 9. Falten, Bootstrap, Abbruch - Verfahren B, sinngemaess
# ===========================================================================
VERFAHREN = "B"
VERFAHREN_SATZ = (
    "Eine einmalige Auswahl ueber das ganze Raster. Jeder Rasterpunkt wird "
    "auf jeder Selektionsfalte ausgewertet; Selektionsstatistik ist der "
    "Median der Falten-Sharpes; Gewinner nach Plateau-Regel. Kein "
    "Trainingsfenster, keine faltenweise Auswahl. Out-of-Sample ist allein "
    "die Bestaetigungsperiode."
)

FALTEN_ART = "kalenderjahre"
FALTEN_MINDESTTRAINING = None          # Verfahren B kennt keines
FALTEN_MINDESTZAHL = 3
SELEKTIONSFALTEN_BIS = 2025
GO_LIVE_SCHNITT = "2026-09-01"

BOOTSTRAP_VERFAHREN = "stationaerer_block_bootstrap"
BOOTSTRAP_REIHE = "taegliche_netto_mark_to_market_renditen_des_kapitalpfads"
BOOTSTRAP_ZIEHUNGEN = 2000
BOOTSTRAP_BLOCKLAENGE_SATZ = (
    "L = max(mediane Haltedauer des Parametersatzes in Handelstagen, "
    "aufgerundet T hoch ein Drittel), T = Laenge der Reihe. L wird BERECHNET "
    "und protokolliert; es ist kein Eingabewert."
)
BOOTSTRAP_MINDESTZAHL_TRADES = None    # es gibt keine

SPITZEN_SCHWELLE = 0.5                 # Plateau-Regel, wie im Hauptregister

# Embargo. S-B1 hat KEINE Zeitbremse; es gilt deshalb die zweite Haelfte der
# Regel aus Registertext 2d: 95. Perzentil der Haltedauer plus 1, aufgerundet.
# Die Zahl kann VOR dem Lauf nicht feststehen - sie wird auf den
# Selektionsfalten des Gewinners gemessen und protokolliert, BEVOR die
# Bestaetigungsperiode geoeffnet wird. Eine hier eingetragene Zahl waere
# geraten.
EMBARGO_REGEL = (
    "95. Perzentil der Haltedauer des Gewinners in Handelstagen, "
    "aufgerundet, plus 1. Gemessen auf den Selektionsfalten und "
    "protokolliert, BEVOR die Bestaetigungsperiode geoeffnet wird."
)


# ===========================================================================
# 10. Die Benchmarks - genau EINER hat einen Weg ins Urteil
# ===========================================================================
# Eine Multi-Asset-Trendfolge gegen Aktien-Buy-and-Hold zu messen, sagt
# nichts: sie soll ja gerade etwas anderes tun. Gemessen wird deshalb gegen
# DASSELBE BUCH OHNE SIGNAL - dieselben Instrumente, dieselben inversen
# Volatilitaetsgewichte, dieselbe monatliche Umschichtung, dieselben Kosten,
# nur immer voll investiert. Uebrig bleibt genau das, was S-B1 hinzufuegt:
# das Timing.
BENCHMARK_URTEIL = {
    "name": "dasselbe_buch_ohne_signal",
    "beschreibung": (
        "Dieselben Kandidaten, dieselbe inverse Volatilitaetsgewichtung, "
        "dieselbe monatliche Umschichtung, dieselben Kosten - aber ohne "
        "Signal, also immer voll investiert. Die Gewichte werden ueber "
        "dieselben Instrumente normiert, die an diesem Umschichtungstag im "
        "Universum sind."),
    "weg_ins_urteil": True,
}

BENCHMARKS_BILD = (
    {"name": "statisch_60_40",
     "beschreibung": ("60 Prozent SPY, 40 Prozent IEF, monatlich "
                      "zurueckgesetzt, dieselben Kosten - das "
                      "Vergleichsportfolio, das der Betreiber sonst haette."),
     "weg_ins_urteil": False},
    {"name": "aktien_buy_and_hold",
     "beschreibung": ("SPY, gehalten. Berichtet, damit sichtbar bleibt, "
                      "dass dieser Vergleich ueber S-B1 nichts aussagt - "
                      "und weil die KORRELATION gegen ihn der eigentliche "
                      "Grund ist, aus dem S-B1 ueberhaupt gebaut wuerde."),
     "weg_ins_urteil": False},
    {"name": "neuner_buch",
     "beschreibung": ("Die gleichgewichtete Tagesreihe der neun heutigen "
                      "Bots. Berichtet wird die Korrelation gegen S-B1 - "
                      "berichtet, NICHT bewertet: eine Schwelle dafuer "
                      "waere eine getippte Zahl."),
     "weg_ins_urteil": False},
)

# Die Abbruchkriterien, sinngemaess nach Abschnitt 7 der Neuselektion, mit
# dem Urteilsbenchmark an der Stelle des point-in-time-Universums.
ABBRUCHKRITERIEN = {
    "a": "Falten-Median des Netto-Sharpe kleiner oder gleich 0",
    "b": ("Die Untergrenze von acht Instrumenten ueber vier Anlageklassen "
          "ist in weniger als drei Selektionsfalten erfuellt"),
    "c": ("Beta-Bereinigung: Netto-Alpha gegen den Urteilsbenchmark kleiner "
          "oder gleich 0 UND Calmar unter dem des Urteilsbenchmarks. "
          "Es verlangt BEIDES."),
    "d": ("Der Gewinner ist eine Spitze UND der beste Nicht-Spitzen-Punkt "
          "erfuellt (a)"),
}


# ===========================================================================
# 11. Die Budgetstufen-Leiter
# ===========================================================================
# Sinngemaess nach der Staging-Ebene von S-E1. S-B1 bekommt Kapital NICHT
# dadurch, dass ein Backtest gut aussieht.
BUDGETSTUFEN = (
    {"stufe": "Schatten",
     "kapital": "keines",
     "bedingung": ("S-B1 erzeugt Signale, protokolliert sie und geht in "
                   "KEINE Portfolio-Zahl und in KEINEN Crash-Knopf ein.")},
    {"stufe": "Grundbudget",
     "kapital": "die kleinste Stufe, die der Betreiber vergibt",
     "bedingung": ("Rang 1 hat ueber die neun Bots entschieden UND der "
                   "Backtest hat die Abbruchkriterien ueberstanden UND die "
                   "Bestaetigungsperiode ist abgelaufen.")},
    {"stufe": "Bestaetigt",
     "kapital": "volles Gewicht",
     "bedingung": ("Die Bestaetigungsperiode hat ihrerseits bestanden. "
                   "Es gibt kein 'vorerst behalten' - faellt eine Stufe "
                   "aus, wird der Eintrag geschlossen.")},
)

# Was dieser Ordner ausdruecklich NICHT tut.
NICHT_TEIL_DIESER_AUFGABE = (
    "kein Backtest, keine Ertragsrechnung, keine Sharpe-Zahl",
    "keine Parametersuche, keine Optimierung",
    "keine Auswahl von Instrumenten nach ihrem Ergebnis",
    "kein Bot unter strategies/, keine Crontab, keine results/*.csv",
    "keine Datei unter data/ angelegt, geaendert oder geloescht",
)


def kandidaten_je_klasse():
    """{Klasse: [Symbole]} - in der Reihenfolge von KLASSEN."""
    aus = {k: [] for k in KLASSEN}
    for k in KANDIDATEN:
        aus[k["klasse"]].append(k["symbol"])
    return aus


def symbole():
    return [k["symbol"] for k in KANDIDATEN]


def klasse_von(symbol):
    for k in KANDIDATEN:
        if k["symbol"] == symbol:
            return k["klasse"]
    raise KeyError(f"{symbol} steht nicht in der Kandidatenliste")


def _selbstpruefung():
    """Was beim Import schon falsch sein koennte, faellt beim Import auf."""
    if len(set(symbole())) != len(KANDIDATEN):
        raise SystemExit("Doppeltes Symbol in der Kandidatenliste")
    unbekannt = sorted({k["klasse"] for k in KANDIDATEN} - set(KLASSEN))
    if unbekannt:
        raise SystemExit(f"Unbekannte Anlageklasse(n): {unbekannt}")
    if os.path.abspath(DATEN_DIR).startswith(
            os.path.abspath(KURSDATEN_DIR_VERBOTEN) + os.sep):
        raise SystemExit(
            "DATEN_DIR liegt unter data/. Das aendert den Datenstand-Hash "
            "der Vorregistrierung und entwertet den registrierten Zustand.")


_selbstpruefung()


if __name__ == "__main__":
    je_klasse = kandidaten_je_klasse()
    print(f"S-B1 - {len(KANDIDATEN)} Kandidaten ueber "
          f"{len([k for k, v in je_klasse.items() if v])} Anlageklassen")
    for klasse in KLASSEN:
        print(f"  {klasse:11s} {', '.join(je_klasse[klasse])}")
    print(f"\n  Untergrenze          {UNTERGRENZE_INSTRUMENTE} Instrumente "
          f"ueber {UNTERGRENZE_KLASSEN} Anlageklassen")
    print(f"  Historie ab          {HISTORIE_AB}")
    print(f"  Signalfenster (fest) {SIGNALFENSTER_MONATE} Monate = "
          f"{SIGNALFENSTER_TAGE} Handelstage, Mehrheit {SIGNAL_MEHRHEIT}")
    print(f"  Vol-Rueckblick       {VOL_RUECKBLICK_TAGE} Handelstage "
          f"(einzige Rasterachse)")
    print(f"  Kosten               {KOSTEN_JE_ROUNDTRIP_PCT} Prozentpunkte "
          f"je Round Trip")
    print("  Kasse                "
          + ("verzinst" if KASSE_VERZINST else "unverzinst"))
    print(f"  Datenordner          {DATEN_DIR}")
