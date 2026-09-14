"""
Die Wache vor dem BTC-Regimefilter (TB-30a, Befund AB2/U5)
==============================================================================
Zwei der fuenf Krypto-Bots haben einen BTC-Marktregime-Filter, und sie gehen
mit einem fehlenden `BTCUSDT` verschieden um:

  `volatility_breakout_crypto`  bricht ab
  `t3_supertrend`               UEBERSPRINGT DEN FILTER STILLSCHWEIGEND
                                (`equity_simulation.py`, `multi_symbol_optimise.py`:
                                 jeweils `if "BTCUSDT" in all_data:` ohne `else`)

**Entschieden ist: abbrechen.** Ein Lauf, in dem ein Bot still ohne seinen
Filter rechnet, ist nicht deterministisch - dieselben Parameter liefern je
nach Inhalt von `data/` verschiedene Ergebnisse, und nichts in der Ausgabe
sagt, welcher Fall vorlag. Fuer einen vorregistrierten Selektionslauf ist das
ausgeschlossen: die Herkunft einer Ergebniszeile muss den Lauf bestimmen.

Der Regimefilter ist zudem keine Nebensache. Beim T3-Bot senkte er den Max
Drawdown von -31,2 % auf -22,2 % und hob die Rendite von 102,7 % auf 129,6 %
(Uebergabeprotokoll 3.2). Ein Lauf ohne ihn beschreibt eine ANDERE Strategie
als die laufende - er ist nicht "etwas ungenauer", er ist ein anderer Bot.

WARUM DIE WACHE IN `shared/` STEHT
------------------------------------------------------------------------------
Dieselbe Bedingung an drei Stellen gepflegt ist das Muster, das in diesem
Projekt schon mehrfach auseinandergelaufen ist (Protokoll Abschnitt 8, TB-26
und TB-28). Sie steht deshalb hier einmal und wird importiert.

WAS TB-30a ANFASST - UND WAS NICHT
------------------------------------------------------------------------------
TB-30a darf `strategies/*/equity_simulation.py` und
`strategies/*/multi_symbol_optimise.py` **nicht** aendern; das ist TB-30b.
Diese Datei ist deshalb die fertige, gepruefte Wache; einzubauen ist sie in
TB-30b, und zwar an genau drei Stellen (die Zeilennummern stehen im
Register, Abschnitt "Voraussetzungen des Laufs"):

    from regimewache import btc_daten                      # Kopfzeile
    ...
    btc = btc_daten(all_data, bot="t3_supertrend",
                    holen="python3 fetch_4h_data.py")
    combined = filter_trades_by_regime(combined, compute_btc_regime(btc))

**Bis dieser Einbau erfolgt ist, darf der Selektionslauf nicht starten.** Das
steht so auf der Sperrliste; `pruefe_einbau()` beantwortet die Frage
maschinell.
"""

import os

SYMBOL = "BTCUSDT"

# Die Stellen, an denen die Wache stehen muss, bevor ein Lauf beginnen darf.
# Datei -> der Hinweis, mit dem der Nutzer die Kursdaten nachholt.
EINBAUSTELLEN = {
    os.path.join("strategies", "t3_supertrend", "equity_simulation.py"):
        "python3 fetch_4h_data.py",
    os.path.join("strategies", "t3_supertrend", "multi_symbol_optimise.py"):
        "python3 fetch_4h_data.py",
    os.path.join("strategies", "volatility_breakout_crypto", "equity_simulation.py"):
        "python3 fetch_1d_data.py",
}


class RegimefilterFehlt(SystemExit):
    """Der Filter ist aktiv, seine Daten fehlen. Kein Rueckfallweg.

    Von `SystemExit` abgeleitet, damit ein Bot-Skript ohne weiteres Zutun mit
    Rueckgabewert != 0 endet - dieselbe Form, die
    `volatility_breakout_crypto/equity_simulation.py` heute schon benutzt.
    """


def btc_daten(all_data: dict, bot: str, holen: str, aktiv: bool = True):
    """Die BTC-Kursdaten - oder ein Abbruch. Nie ein stilles Ueberspringen.

    all_data  die geladenen Kursdaten je Symbol
    bot       Name des Bots, fuer die Fehlermeldung
    holen     der Befehl, mit dem der Nutzer die fehlenden Daten nachholt
    aktiv     ob der Filter ueberhaupt eingeschaltet ist. Ist er es nicht,
              gibt die Wache `None` zurueck: ein ABGESCHALTETER Filter ist
              eine Einstellung, ein FEHLENDER ist ein Datenproblem, und die
              beiden duerfen nicht dasselbe Ergebnis haben.
    """
    if not aktiv:
        return None
    btc = all_data.get(SYMBOL) if hasattr(all_data, "get") else None
    if btc is None:
        raise RegimefilterFehlt(
            f"{bot}: Der BTC-Regimefilter ist aktiv, aber {SYMBOL} fehlt in "
            f"den geladenen Kursdaten. Der Lauf bricht ab statt ohne Filter "
            f"weiterzurechnen - ein Lauf ohne den Filter beschreibt eine "
            f"andere Strategie als die laufende und waere von einem "
            f"gewoehnlichen Lauf nicht zu unterscheiden. "
            f"Kursdaten nachholen mit: {holen}")
    leer = getattr(btc, "empty", False)
    if leer:
        raise RegimefilterFehlt(
            f"{bot}: {SYMBOL} ist in den Kursdaten vorhanden, aber leer. "
            f"Dasselbe Problem, eine Stufe weiter innen - der Lauf bricht ab. "
            f"Kursdaten nachholen mit: {holen}")
    return btc


def pruefe_einbau(basis: str = None) -> dict:
    """Ist die Wache an allen drei Stellen eingebaut?

    Liest Quelltext, importiert nichts, veraendert nichts. Rueckgabe:
    {"vollstaendig": bool, "offen": [...], "eingebaut": [...]}.
    """
    basis = basis or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eingebaut, offen = [], []
    for rel in sorted(EINBAUSTELLEN):
        pfad = os.path.join(basis, rel)
        if not os.path.exists(pfad):
            offen.append(f"{rel} (Datei fehlt)")
            continue
        with open(pfad, encoding="utf-8") as f:
            text = f.read()
        if "btc_daten(" in text and "regimewache" in text:
            eingebaut.append(rel)
        else:
            offen.append(rel)
    return {"vollstaendig": not offen, "offen": offen, "eingebaut": eingebaut}
