"""
Aus einem Kapitalpfad wird eine Kennzahl - die Messkette an EINER Stelle
==============================================================================
Dieses Modul enthaelt die beiden Rechnungen, mit denen aus dem Ergebnis der
Kapitalsimulation (`shared/zuteilung.simuliere_portfolio()`) die beiden
ausgewiesenen Kennzahlen werden:

    from messkette import calculate_max_drawdown, rendite_pct

  * **Rendite** - `rendite_pct(endkapital, startkapital)`
  * **Max Drawdown** - `calculate_max_drawdown(equity_df, startkapital)`

Damit steht die Messkette vollstaendig an einer Stelle: die Kapitalrechnung
seit TB-26 in `shared/zuteilung.py`, die beiden Kennzahlen seit TB-28 hier.

DER ANLASS (TB-27)
------------------------------------------------------------------------------
TB-27 hat die neun `strategies/*/equity_simulation.py` Funktion fuer Funktion
verglichen. Befund fuer diese beiden Rechnungen:

  | Rechnung             | Fassungen ueber die neun Bots            |
  |----------------------|------------------------------------------|
  | calculate_max_drawdown | **1** - alle neun ZEICHENGLEICH        |
  | Renditeformel          | **1** - zeichengleich                  |

Die Messkette war also bereits einheitlich - nur stand sie **neunmal** da.
Das ist kein harmloser Zustand: genau diese Sorte Doppelfuehrung ist in
diesem Projekt schon mehrfach unbemerkt auseinandergelaufen, und sie ist es
hier bereits, nur ausserhalb der neun Dateien. TB-27, Befund U10: drei Kopien
unter `research/` behaupten im Docstring, "identisch zur Hilfsfunktion in
jedem Bot-eigenen equity_simulation.py" zu sein - zwei davon sind es nicht.
Eine Kopie, die von sich sagt, sie sei eine Kopie, ist keine Absicherung.

Dieses Modul zieht die Rechnung an eine Stelle, **ohne ihr Verhalten zu
aendern**. Die Zusicherung von TB-28 lautet ausdruecklich: keine einzige Zahl
aendert sich. Deshalb ist der Rumpf von `calculate_max_drawdown()` Zeichen
fuer Zeichen der der neun Bots, nur um die gemeinsame Kernrechnung herum
aufgeteilt.

WAS HIER BEWUSST **NICHT** ENTSCHIEDEN WIRD
------------------------------------------------------------------------------
**Welches Mass fuehrt.** TB-27 Abschnitt 4.3 haelt fest, dass die Zahl, nach
der Parameter AUSGEWAEHLT werden (`robustness_score`), gar nicht hier
entsteht, sondern in `multi_symbol_optimise.py` (neunmal), in
`multi_symbol_walk_forward.py` (sechsmal) und in den `optimise_*.py`
(dreimal) - und dort aus der naiven Summierung von Trade-Prozenten, also
genau dem, wovor Methodik-Prinzip 2 des Uebergabeprotokolls warnt.

Dieses Modul ruehrt daran nichts an. Es ist der strukturelle Vorbau: erst
steht die Messkette an einer Stelle, dann ist die Frage "welches Mass fuehrt"
eine Aenderung an einer Stelle statt an achtzehn. Die Trennung ist Absicht -
aenderte sich beides zugleich, wuesste hinterher niemand mehr, ob eine
verschobene Zahl die beabsichtigte Aenderung war oder ein Fehler beim
Zusammenlegen.

WARUM DIE RENDITE HIER **UNGERUNDET** ZURUECKKOMMT
------------------------------------------------------------------------------
Die drei Verbraucher runden heute verschieden, und das ist kein Versehen:

  * die neun `__main__`-Bloecke runden gar nicht, sie formatieren (`:.2f`);
  * `shared/ergebniskurven.py::kennzahlen()` rundet auf zwei Stellen, weil
    der Wert in eine JSON-Datei und in eine Tabelle geht;
  * `shared/determinismus_lauf.py` rundet auf zwei Stellen, weil der Wert
    ueber Laeufe hinweg verglichen wird.

Rundete diese Funktion selbst, muesste einer der drei sein heutiges Verhalten
aufgeben - und die Zusicherung "keine Zahl aendert sich" waere dahin. Die
Formel gehoert hierher, die Darstellung zum Verbraucher.

WARUM `calculate_max_drawdown()` UMGEKEHRT **RUNDET**
------------------------------------------------------------------------------
Weil sie das heute tut. Ihr Rueckgabewert ist an mehr als dreissig Stellen im
Repo die Zahl, die ausgewiesen wird (TB-27, Abschnitt 4.2); die Rundung ist
Teil dieser Zahl, nicht ihrer Darstellung. Wer den ungerundeten Tiefstwert
braucht - `shared/ergebniskurven.py` braucht ihn, weil es dort anders
gerundet wird -, nimmt `max_drawdown_ungerundet()`.

DER NAME `calculate_max_drawdown` BLEIBT
------------------------------------------------------------------------------
Englisch und `snake_case` wie bisher, obwohl die neueren gemeinsamen Module
deutsch benennen. Der Grund ist nicht Bequemlichkeit: **mehr als dreissig
Stellen** im Repo rufen sie unter genau diesem Namen als Attribut des
Bot-Moduls auf (`es.calculate_max_drawdown(...)`,
`globalen["calculate_max_drawdown"](...)`, `from equity_simulation import
calculate_max_drawdown`). Weil die neun Bots den Namen hier importieren,
bleibt er Attribut ihres Moduls und alle diese Stellen laufen unveraendert
weiter. Eine Umbenennung waere eine Aenderung an dreissig Stellen ohne jeden
Gewinn - und TB-28 aendert keine Zahl und keinen Aufrufweg.

WAS DIESES MODUL NICHT TUT
------------------------------------------------------------------------------
* Es importiert **nichts** aus `strategies/` und nichts aus `shared/`. Es
  kennt weder Bots noch Parameter noch Pfade - es bekommt Zahlen und gibt
  eine Zahl zurueck. Ein Importzyklus ist damit ausgeschlossen.
* Es liest und schreibt **keine** Datei.
* Es entscheidet nichts ueber Zuteilung, Reihenfolge oder Positionsgroessen -
  das ist `shared/zuteilung.py`.
"""

import pandas as pd


def rendite_pct(endkapital: float, startkapital: float) -> float:
    """Gesamtrendite in Prozent - die Formel der neun `__main__`-Bloecke.

    Bewusst UNGERUNDET, siehe Kopfkommentar. Die neun Bots formatieren den
    Rueckgabewert mit `:.2f`, die beiden Nachrechner in `shared/` runden ihn
    mit `round(..., 2)` - beides bleibt Sache des Verbrauchers.
    """
    return (endkapital / startkapital - 1) * 100


def max_drawdown_ungerundet(kapital_nach_trade, startkapital: float):
    """Der Kern der Drawdown-Rechnung: der tiefste prozentuale Abstand vom
    bisherigen Hoechststand, ungerundet.

    `kapital_nach_trade` ist die Spalte `capital_after` der Equity-Kurve, also
    der Kapitalstand NACH jedem abgeschlossenen Trade.

    Die Reihe beginnt beim Startkapital - sonst faellt ein Verlust im ersten
    Trade aus der Rechnung heraus: ohne diesen Anfangswert waere der erste
    Kurvenpunkt selbst das laufende Maximum, und der Ruecksetzer von 10.000
    auf 9.900 haette nie stattgefunden.

    Der Rueckgabewert ist der von pandas gelieferte `numpy.float64`, nicht
    `float`. Das ist kein Detail, sondern der Grund, warum hier nicht schon
    gerundet wird: die Verbraucher runden verschieden und wandeln verschieden
    (siehe `calculate_max_drawdown` gegen
    `shared/ergebniskurven.py::kennzahlen()`), und TB-28 aendert an keiner
    dieser beiden Fassungen etwas.
    """
    reihe = pd.concat([pd.Series([startkapital]), kapital_nach_trade],
                      ignore_index=True)
    laufendes_max = reihe.cummax()
    drawdown_pct = (reihe - laufendes_max) / laufendes_max * 100
    return drawdown_pct.min()


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    """Max Drawdown auf dem Kapitalpfad, auf zwei Stellen gerundet.

    Bis TB-28 stand diese Funktion neunmal zeichengleich in den
    `strategies/*/equity_simulation.py`. Signatur, Name, Rueckgabewert und
    Rundung sind unveraendert; die neun Bots importieren sie jetzt von hier.

    Die leere Kurve gibt `0.0` zurueck und nicht `None`: ein Bot ohne
    ausgefuehrte Trades hat keinen Rueckgang erlitten. Diese Fallunterscheidung
    stand schon vorher hier und nicht beim Aufrufer.
    """
    if equity_df.empty:
        return 0.0
    return round(max_drawdown_ungerundet(equity_df["capital_after"], starting_capital), 2)
