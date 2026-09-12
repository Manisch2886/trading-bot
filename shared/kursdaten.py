"""
Unvollstaendige Kerzen aus Kursdaten fernhalten
==============================================================================
Der Anlass ist ein gemessener Befund aus `research/elliott_wave_params/`
(Abschnitt 6): die letzte Kerze von `APH` steht ohne Kurse in den Daten - nur
das Volumen ist gefuellt. Ein Trade, der dort per Zeitausstieg endet, bekommt
`exit_price = NaN`, daraus wird `pnl_pct = NaN`.

Warum das schlimmer ist als ein Absturz
------------------------------------------------------------------------------
Ein NaN faellt nirgends auf, sondern hinterlaesst ueberall plausible Zahlen:

* `equity_simulation.simulate_portfolio` rechnet `capital += ...` mit dem NaN
  weiter. **Jeder** danach verarbeitete Trade erbt es - eine einzige Luecke am
  Anfang macht die gesamte restliche Kapitalkurve unbrauchbar (gemessen: 3 von
  3 Zeilen).
* `avg_return = combined["pnl_pct"].mean()` uebergeht NaN stillschweigend
  (pandas-Voreinstellung `skipna=True`).
* `win_rate = (combined["pnl_pct"] > 0).mean()` ist noch unangenehmer:
  `NaN > 0` ergibt `False`, der kaputte Trade zaehlt also als **Verlierer**.
  In einem Beispiel mit vier Trades sinkt die Trefferquote dadurch von 66,7 %
  auf 50,0 %, ohne jeden Hinweis.

Die Abhilfe steht im Projekt bereits an einer Stelle richtig da:
`buy_and_hold_benchmark.py` prueft auf `pd.isna`, ueberspringt das betroffene
Symbol **und zaehlt es**, mit einer Hinweiszeile in der Ausgabe. Dieses Modul
verallgemeinert genau dieses Vorgehen - es ist keine zweite Erfindung.

Der Grundsatz dahinter: **streichen UND zaehlen**. Ein stillschweigend
gestrichener Datenpunkt ist dasselbe Problem in Gruen.

Wo das greift
------------------------------------------------------------------------------
An der frueheste moeglichen Stelle, damit keine nachgelagerte Rechnung sie je
zu sehen bekommt:

* `fetch_stock_data.fetch_historical_data` - die Funktion, die yfinance-Daten
  ins Projekt holt. Sie schreibt die CSVs **und** versorgt `forward_test.py`
  live. Die Absicherung dort behebt den Live-Pfad, ohne `forward_test.py`
  anzufassen.
* `multi_symbol_optimise.load_all_symbol_data` - der Weg fuer bereits
  vorhandene CSVs, die die Luecke noch enthalten.

Nutzung als Pruefwerkzeug:
    python3 shared/kursdaten.py            # prueft data/ und meldet Befunde
    python3 shared/kursdaten.py --ordner X # anderer Ordner
"""

import argparse
import glob
import os
import sys

KURSSPALTEN = ["open", "high", "low", "close"]


def unvollstaendige_maske(df):
    """True je Zeile, in der mindestens eine der vier Kursspalten fehlt.

    Das Volumen bleibt bewusst aussen vor: eine Kerze ohne Volumen, aber mit
    Kursen ist handelbar beschreibbar, eine ohne Kurse nicht. Genau so liegt
    der APH-Fall vor - Volumen vorhanden, Kurse leer.
    """
    vorhanden = [s for s in KURSSPALTEN if s in df.columns]
    if not vorhanden:
        # Ohne Kursspalten laesst sich nichts beurteilen. Nichts streichen ist
        # hier richtiger als alles zu streichen.
        import pandas as pd                                    # noqa: PLC0415
        return pd.Series(False, index=df.index)
    return df[vorhanden].isna().any(axis=1)


def entferne_unvollstaendige(df, symbol=None, melden=True):
    """(bereinigtes df, Anzahl gestrichener Zeilen).

    Streicht und ZAEHLT. Wird `melden` gesetzt, geht zusaetzlich eine Zeile an
    die Ausgabe - der Punkt der ganzen Uebung ist, dass es auffaellt.
    """
    if df is None or len(df) == 0:
        return df, 0
    maske = unvollstaendige_maske(df)
    anzahl = int(maske.sum())
    if anzahl == 0:
        return df, 0
    bereinigt = df[~maske].reset_index(drop=True)
    if melden:
        name = f"{symbol}: " if symbol else ""
        print(f"Hinweis: {name}{anzahl} unvollstaendige Kerze(n) ohne Kurse "
              f"gestrichen (von {len(df)}). Grund: mindestens eine der Spalten "
              f"{'/'.join(KURSSPALTEN)} ist leer; ein Trade, der dort endet, "
              f"ergaebe NaN als Ergebnis.")
    return bereinigt, anzahl


class Zaehler:
    """Sammelt die Streichungen eines Ladevorgangs, damit am Ende EINE Zeile
    mit der Gesamtzahl stehen kann statt nur verstreuter Einzelhinweise."""

    def __init__(self):
        self.je_symbol = {}

    def erfasse(self, symbol, anzahl):
        if anzahl:
            self.je_symbol[symbol] = anzahl

    @property
    def gesamt(self):
        return sum(self.je_symbol.values())

    def bericht(self):
        if not self.je_symbol:
            return None
        teile = ", ".join(f"{s} ({n})" for s, n in sorted(self.je_symbol.items()))
        return (f"Datenqualitaet: insgesamt {self.gesamt} unvollstaendige "
                f"Kerze(n) in {len(self.je_symbol)} Symbol(en) gestrichen - "
                f"{teile}. Diese Kerzen gehen in KEINE Kennzahl ein.")

    def melde(self):
        text = self.bericht()
        if text:
            print(text)
        return text


# ---------------------------------------------------------------------------
def pruefe_ordner(ordner, muster="*.csv"):
    """Durchsucht einen Datenordner und gibt je Datei die Zahl unvollstaendiger
    Kerzen zurueck. Rein lesend."""
    import pandas as pd                                        # noqa: PLC0415

    befunde = []
    for pfad in sorted(glob.glob(os.path.join(ordner, muster))):
        try:
            df = pd.read_csv(pfad)
        except Exception as fehler:                            # noqa: BLE001
            befunde.append({"datei": os.path.basename(pfad), "fehler": str(fehler),
                            "anzahl": None, "letzte_betroffen": None})
            continue
        maske = unvollstaendige_maske(df)
        anzahl = int(maske.sum())
        if anzahl:
            befunde.append({
                "datei": os.path.basename(pfad),
                "anzahl": anzahl,
                "zeilen": len(df),
                "letzte_betroffen": bool(maske.iloc[-1]),
                "zeitpunkte": [str(z) for z in df.loc[maske, "open_time"].tolist()[:5]]
                              if "open_time" in df.columns else [],
                "fehler": None,
            })
    return befunde


def main(argv=None) -> int:
    _SHARED = os.path.dirname(os.path.abspath(__file__))
    standard = os.path.join(os.path.dirname(_SHARED), "data")

    zerleger = argparse.ArgumentParser(
        description="Sucht Kerzen ohne Kurse in den Kursdateien.")
    zerleger.add_argument("--ordner", default=standard)
    zerleger.add_argument("--muster", default="*.csv")
    argumente = zerleger.parse_args(argv)

    befunde = pruefe_ordner(argumente.ordner, argumente.muster)
    dateien = len(glob.glob(os.path.join(argumente.ordner, argumente.muster)))
    print(f"Geprueft: {dateien} Datei(en) in {argumente.ordner}")
    if not befunde:
        print("Keine unvollstaendigen Kerzen gefunden.")
        return 0

    print(f"\n{len(befunde)} Datei(en) mit Befund:")
    for eintrag in befunde:
        if eintrag["fehler"]:
            print(f"  {eintrag['datei']:22} nicht lesbar: {eintrag['fehler']}")
            continue
        letzte = "  <- betrifft die LETZTE Kerze" if eintrag["letzte_betroffen"] else ""
        print(f"  {eintrag['datei']:22} {eintrag['anzahl']} von {eintrag['zeilen']} "
              f"Kerze(n){letzte}")
        for zeitpunkt in eintrag["zeitpunkte"]:
            print(f"      {zeitpunkt}")
    print("\nDiese Kerzen werden beim Laden gestrichen und gezaehlt - die "
          "Dateien selbst bleiben unveraendert.")
    # Rueckgabewert 1: ein Befund ist kein Fehler des Programms, aber etwas,
    # das ein Cronjob-Aufruf sichtbar machen soll.
    return 1


if __name__ == "__main__":
    sys.exit(main())
