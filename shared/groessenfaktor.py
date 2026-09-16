"""
Der Quartals-Multiplikator auf die Positionsgroesse - die LESESEITE (TB-42)
==============================================================================
Das Leiter-Skript des Zellenbudgets (Registertext 6m, TB-41) rechnet einmal je
Quartal fuer jeden der neun Bots einen Multiplikator auf dessen heutige,
statische Positionsgroesse aus:

    m_b = (Zellenanteil x Klassenschluessel x Bot-Anteil in der Zelle) / (1/9)

`1/9` ist der Nenner, weil neun gleich grosse Bots heute je ein Neuntel
tragen: **m_b = 1,0 heisst "wie bisher"**. Dieses Modul LIEST diesen Wert.

    import groessenfaktor
    FAKTOR = groessenfaktor.lies(__file__)        # 1,0, wenn nichts hinterlegt

⚠️ DIE SCHREIBENDE SEITE GIBT ES NOCH NICHT. Sie entsteht erst, wenn
`research/vorregistrierung/auswertung.py` auf Verfahren B umgebaut ist. Bis
dahin fehlt `config/groessenfaktor.json` schlicht - und genau deshalb ist der
Rueckfall auf 1,0 keine Randerscheinung, sondern der Normalfall.

WO DER MULTIPLIKATOR ANGREIFT - UND DER BEFUND DAZU
------------------------------------------------------------------------------
**Befund (TB-42):** Die neun `forward_test.py` fuehren HEUTE GAR KEINE
Positionsgroesse. Ihre Trade-Tabellen halten Symbol, Zeiten, Ein- und
Ausstiegskurs, Stop und `pnl_pct` - kein Stueck, keinen Betrag, keinen Anteil.
Was eine Position "gross" macht, steht ausserhalb: `ALLOCATION_PCT` in
`strategies/*/equity_simulation.py` und `BINANCE_TESTNET_BETRAG_USDT` in
`broker/zugang.py`. Das Dashboard sagt dasselbe von der anderen Seite:
"die Bots speichern keine Positionsgroesse pro Trade"
(`dashboard/datenquelle.py`).

Der Multiplikator kann im Forward-Test also nichts multiplizieren - es gibt
keine Zahl, an der er angreifen koennte. Die Aufgabe nennt als Befund den
Fall "mehr als eine Stelle je Bot"; hier ist es **keine**.

Aufgeloest wird das so, wie es die Freigabe hergibt - und keinen Schritt
weiter: der Forward-Test **schreibt die Positionsgroesse hin**, mit der er die
Position eroeffnet, als Vielfaches der statischen Groesse dieses Bots. Das ist
die neue Spalte `groessenfaktor` in der Trade-Tabelle, gefuellt mit m_b.

  * Sie ist **genau eine Stelle je Bot** - der INSERT beim Eroeffnen.
  * Sie beruehrt **kein Signal, keine Schwelle, keine Positionszahl**: welche
    Trades entstehen und wann sie wieder zugehen, haengt an keiner Stelle von
    ihr ab. Nachgewiesen in `shared/test_groessenfaktor.py`: derselbe Lauf mit
    m_b = 1,0 und m_b = 0,5 erzeugt dieselben Ein- und Ausstiegszeitpunkte.
  * Sie macht den Wert **nachtraeglich pruefbar**: neben jedem Trade steht,
    mit welchem Multiplikator er eroeffnet wurde. Ohne sie waere spaeter nicht
    mehr feststellbar, welches Quartal welche Groesse getragen hat.
  * `pnl_pct` bleibt unberuehrt - ein Prozentsatz ist von der Groesse
    unabhaengig. Wer die Groesse einrechnen will, multipliziert beides; genau
    dafuer steht die Spalte da.

Die Seite, die diese Spalte tatsaechlich in Stuecke oder Betraege uebersetzt
(Kapitalsimulation, Broker-Bruecke), gehoert **nicht** zu dieser Aufgabe.

WO DIE DATEI LIEGT UND WARUM DORT
------------------------------------------------------------------------------
    config/groessenfaktor.json                (versioniert, nicht gitignoriert)

* **`config/` und nicht `results/`**, weil die Datei den laufenden Betrieb
  steuert und nicht ein Ergebnis beschreibt. Was neun Bots die Groesse
  vorgibt, gehoert neben `config/sp500_top150.txt` - und in die Versionierung,
  damit spaeter im Git-Verlauf nachlesbar ist, welcher Multiplikator wann galt.
  Die Bot-Datenbanken sind gitignoriert; dort waere diese Spur weg.
* **JSON und nicht Python**, obwohl `live_params.py` Python ist: diese Datei
  wird von einem Skript GESCHRIEBEN. Erzeugter Python-Quelltext, der bei jedem
  Bot-Lauf ausgefuehrt wird, ist eine viel groessere Angriffsflaeche als Daten,
  die geprueft werden koennen - und geprueft wird hier jeder einzelne Wert.
* **JSON und nicht CSV**, weil neben den neun Zahlen auch das Quartal und die
  Herkunft hineingehoeren; eine CSV haette dafuer keinen Platz.
* Selten geschrieben (quartalsweise), oft gelesen (neun Bots, bis zu sechs
  Laeufe am Tag): ein paar hundert Byte, die der Kern in Millisekunden liest.

`config/groessenfaktor.beispiel.json` zeigt das Format - nach dem Vorbild von
`.env.beispiel`, das ebenfalls nur die Form nennt und nichts Wirksames setzt.

DER ZULAESSIGE BEREICH: 0,25 bis 4,0
------------------------------------------------------------------------------
"Ein Multiplikator von 0 oder 50 ist ein Fehler, kein Befehl." Der Bereich ist
bewusst enger als das rechnerisch Moegliche (m_b kann formal zwischen 0 und 9
liegen, denn mehr als das ganze Kapital kann ein Bot nicht bekommen):

* **Untergrenze 0,25** - ein Viertel der heutigen Groesse. Darunter wird der
  Forward-Test blind: Gebuehren und Slippage (0,1 % + 0,05 % je Seite, in
  jedem der neun Bots) sind ein FESTER Prozentsatz und schrumpfen nicht mit.
  Und **0 muss aussen vor bleiben**: "dieser Bot handelt nicht mehr" ist eine
  Entscheidung des Betreibers, keine Zahl, die eine Quartalsrechnung
  nebenbei setzt. Genau das meint "ein Fehler, kein Befehl".
* **Obergrenze 4,0** - das Vierfache. Die Bots stehen heute bei 2 % bis 10 %
  je Position und 5 bis 20 gleichzeitigen Positionen; mal vier ist ein Bot
  damit voll investiert. Was darueber hinausginge, waere keine Umverteilung
  mehr, sondern eine andere Strategie - und die gehoert durch Backtest,
  Walk-Forward und Equity-Simulation (Protokoll Abschnitt 7), nicht in eine
  JSON-Datei.
* Die Grenzen sind **symmetrisch**: 4 = 1/0,25. Die Wache sitzt nach oben so
  eng wie nach unten und bevorzugt das Vergroessern nicht.

Die Grenzen stehen hier und nicht in `live_params.py`: sie sind kein
Handelsparameter, sondern die Wache um einen. `live_params.py` bleibt
unberuehrt (TB-42-Randbedingung).

WAS BEI FEHLERN GESCHIEHT - MELDEN, NICHT STOPPEN
------------------------------------------------------------------------------
In JEDEM Zweifelsfall gilt 1,0, und der Bot laeuft weiter. Ein Bot darf nicht
stehenbleiben, weil eine Quartalsrechnung fehlt oder kaputt ist.

Still wird der Rueckfall dabei nie: **jeder Lauf protokolliert genau eine
Zeile** mit dem geltenden Faktor und seiner Herkunft - auch der ganz normale
Fall "keine Datei hinterlegt". Ein stiller Rueckfall auf 1,0 waere derselbe
Fehler wie die lautlosen Loader aus Teil 1 dieser Aufgabe.
"""

import json
import math
import os

NEUTRAL = 1.0
UNTERGRENZE = 0.25
OBERGRENZE = 4.0

DATEINAME = "groessenfaktor.json"


def standardpfad():
    """config/groessenfaktor.json, von diesem Modul aus gerechnet."""
    basis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basis, "config", DATEINAME)


def botname(bot):
    """Nimmt den Bot-Namen entgegen - oder das `__file__` eines Bot-Skripts.

    `lies(__file__)` ist im Aufrufer EINE Zeile ohne weitere Konstante; der
    Ordnername unter strategies/ IST der Bot-Name (siehe strategy_paths.py).
    """
    if bot.endswith(".py") or os.sep in bot:
        return os.path.basename(os.path.dirname(os.path.abspath(bot)))
    return bot


def bestimme(bot, pfad=None):
    """Der geltende Multiplikator, ohne jede Ausgabe.

    Gibt `(wert, protokollzeile, meldungen)` zurueck. `meldungen` ist leer,
    wenn nichts zu beanstanden war - eine fehlende Datei ist nichts zu
    beanstanden, sie ist der heutige Normalfall.
    """
    name = botname(bot)
    pfad = pfad or standardpfad()
    zurueck = lambda grund: (NEUTRAL, _protokoll(name, NEUTRAL, grund))   # noqa: E731

    if not os.path.exists(pfad):
        wert, zeile = zurueck(f"keine Quartalsrechnung hinterlegt ({pfad} fehlt)")
        return wert, zeile, []

    try:
        with open(pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)
    except Exception as fehler:                                  # noqa: BLE001
        wert, zeile = zurueck("Datei unlesbar")
        return wert, zeile, [_warnung(name, f"{pfad} ist nicht lesbar ({fehler})")]

    if not isinstance(daten, dict) or not isinstance(daten.get("bots"), dict):
        wert, zeile = zurueck("Datei unvollstaendig")
        return wert, zeile, [_warnung(
            name, f"{pfad} hat keinen Abschnitt 'bots' mit Werten je Bot")]

    if name not in daten["bots"]:
        wert, zeile = zurueck("eigener Bot nicht in der Datei")
        return wert, zeile, [_warnung(
            name, f"{pfad} fuehrt diesen Bot nicht auf")]

    roh = daten["bots"][name]
    # `bool` ausdruecklich heraus: True ist in Python eine 1 und kaeme sonst
    # als gueltiger Faktor durch, ohne je eine Zahl gewesen zu sein.
    if isinstance(roh, bool) or not isinstance(roh, (int, float)):
        wert, zeile = zurueck("Wert ist keine Zahl")
        return wert, zeile, [_warnung(
            name, f"der Wert {roh!r} in {pfad} ist keine Zahl")]

    wert_roh = float(roh)
    # EINE Wache fuer den Bereich - und sie faengt NaN und Unendlich mit:
    # beide Vergleiche sind fuer NaN False, inf liegt oberhalb. Eine zweite
    # Pruefung daneben wuerde nur verdecken, wenn diese hier verschwaende.
    if not (UNTERGRENZE <= wert_roh <= OBERGRENZE):
        wert, zeile = zurueck(
            f"Wert {_zahl(wert_roh)} liegt ausserhalb von "
            f"{_zahl(UNTERGRENZE)} bis {_zahl(OBERGRENZE)}")
        return wert, zeile, [_warnung(
            name, f"der Wert {_zahl(wert_roh)} in {pfad} liegt ausserhalb des "
                  f"zulaessigen Bereichs {_zahl(UNTERGRENZE)} bis "
                  f"{_zahl(OBERGRENZE)} - er wird NICHT uebernommen")]

    quartal = daten.get("quartal")
    herkunft = f"{pfad}" + (f", Quartal {quartal}" if quartal else "")
    return wert_roh, _protokoll(name, wert_roh, herkunft), []


def lies(bot, pfad=None):
    """Der geltende Multiplikator, mit Protokollzeile und etwaiger Meldung.

    Das ist der Aufruf fuer die neun `forward_test.py`. Er wirft nie: was
    hier schiefgeht, darf einen Bot-Lauf nicht anhalten.
    """
    try:
        wert, zeile, meldungen = bestimme(bot, pfad)
    except Exception as fehler:                                  # noqa: BLE001
        # Letzte Leine. Sie soll nie greifen - wenn doch, dann laut.
        print(_warnung(botname(bot), f"unerwarteter Fehler ({fehler})"))
        print(_protokoll(botname(bot), NEUTRAL, "Rueckfall nach Fehler"))
        return NEUTRAL
    for m in meldungen:
        print(m)
    print(zeile)
    return wert


# ---------------------------------------------------------------------------
def _zahl(x):
    """Deutsche Schreibweise, so wie die Aufgabe sie fuehrt: 1,0 statt 1.0.

    Die Nachkommastelle bleibt auch bei glatten Werten stehen: "1" koennte
    eine Anzahl sein, "1,0" ist erkennbar ein Faktor.
    """
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return str(x)
    text = f"{x:.4f}".rstrip("0")
    if text.endswith("."):
        text += "0"
    return text.replace(".", ",")


def _protokoll(name, wert, herkunft):
    return f"Groessenfaktor {_zahl(wert)} fuer {name} ({herkunft})."


def _warnung(name, text):
    return f"Warnung: Groessenfaktor fuer {name} - {text}. Es gilt {_zahl(NEUTRAL)}."


def spalte_anlegen(conn, tabelle="trades", spalte="groessenfaktor"):
    """Ergaenzt die Spalte in einer BESTEHENDEN Trade-Tabelle.

    `CREATE TABLE IF NOT EXISTS` ruehrt eine Tabelle, die es schon gibt, nicht
    mehr an - die Datenbanken der neun Bots laufen aber seit Monaten. Ohne
    diesen Schritt bliebe die Spalte dort fuer immer aus, und der INSERT
    scheiterte bei jedem Trade. Ein zweiter Aufruf ist folgenlos.

    Alte Trades behalten NULL: sie wurden vor dem Zellenbudget eroeffnet, und
    ihnen nachtraeglich 1,0 einzutragen hiesse, eine Zahl zu behaupten, die
    damals niemand gefuehrt hat.
    """
    vorhanden = {z[1] for z in conn.execute(f"PRAGMA table_info({tabelle})")}
    if not vorhanden:
        return False                       # Tabelle gibt es (noch) nicht
    if spalte in vorhanden:
        return False
    conn.execute(f"ALTER TABLE {tabelle} ADD COLUMN {spalte} REAL")
    conn.commit()
    return True
