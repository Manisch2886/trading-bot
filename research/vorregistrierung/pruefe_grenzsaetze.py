#!/usr/bin/env python3
"""
TB-30a - Maschinelle Pruefung der Rastergrenzen
==============================================================================
Die Vorregistrierung sichert zu:

  > **Der heutige Live-Wert ist kein Bezugspunkt.**
  > Maschinell pruefen: kein Grenzsatz erwaehnt einen Live-Wert.

Dieses Programm prueft das - und zwar DOPPELT, aus einem Grund, der in diesem
Projekt teuer gelernt wurde: eine zweite Wache darf das Fehlen der ersten
nicht verdecken. Die beiden Wachen pruefen deshalb VERSCHIEDENE Dinge und
scheitern unabhaengig voneinander:

  Wache 1 - DIE GRENZE IST GERECHNET.
      Jede Rastergrenze wird aus ihrer Regel neu ausgerechnet und mit dem
      ausgewiesenen Wert verglichen. Eine getippte Zahl kann es damit nicht
      geben; ein Live-Wert koennte nur noch durch Zufall in eine Grenze
      geraten.

  Wache 2 - DER SATZ NENNT KEINEN LIVE-WERT.
      Aus jedem Begruendungssatz werden alle Zahlen gezogen und gegen die
      Live-Werte DIESES Bots gehalten (`live_params.py` und, wo der Wert nur
      dort steht, `equity_simulation.py`). Eine Uebereinstimmung ist ein
      Fehlschlag - auch dann, wenn sie unschuldig ist. Ein Grenzsatz, der
      eine Live-Zahl nennt, laedt zum Rueckschluss ein, und genau der soll
      nicht moeglich sein.

  Wache 3 - JEDE GRENZE HAT EINE ZUGELASSENE GRUNDLAGE.
      `kosten`, `datenfrequenz`, `volatilitaet`, `haltedauer` - dazu die
      beiden im Register benannten Ausnahmen `ableitung` (die abgeleitete
      Obergrenze des Positionslimits) und `methode` (die Fibonacci-Leiter und
      das Bollinger-Fenster). Eine Grenze mit einer anderen Grundlage faellt
      durch.

  Wache 4 - DIE STUFUNG IST DIE VERSPROCHENE.
      Geometrisch mit Faktor 1,5 bis 2,0 und drei bis fuenf Stufen fuer
      Skalenparameter, ganzzahlig-linear fuer Zaehlparameter.

Rueckgabewert 0, wenn alle Wachen halten, sonst 1.
"""

import ast
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

import registerdaten as rd  # noqa: E402

ZUGELASSENE_GRUNDLAGEN = {"kosten", "datenfrequenz", "volatilitaet", "haltedauer"}
BENANNTE_AUSNAHMEN = {"ableitung", "methode"}

ZAHL = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)(?![\w])")

bestanden = 0
gescheitert = []


def pruefe(name: str, bedingung: bool, zusatz: str = ""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def live_werte(bot: str) -> dict:
    """Alle Zahlenkonstanten aus live_params.py und equity_simulation.py.

    Gelesen ueber den Syntaxbaum, NICHT importiert: ein Import wuerde
    Bot-Abhaengigkeiten ziehen, und diese Pruefung soll ueberall laufen.
    """
    werte = {}
    for datei in ("live_params.py", "equity_simulation.py"):
        pfad = os.path.join(BASE_DIR, "strategies", bot, datei)
        if not os.path.exists(pfad):
            continue
        with open(pfad, encoding="utf-8") as f:
            baum = ast.parse(f.read())
        for knoten in baum.body:
            if not isinstance(knoten, ast.Assign):
                continue
            for ziel in knoten.targets:
                if not isinstance(ziel, ast.Name) or not ziel.id.isupper():
                    continue
                try:
                    wert = ast.literal_eval(knoten.value)
                except Exception:
                    continue
                if isinstance(wert, bool) or not isinstance(wert, (int, float)):
                    continue
                werte.setdefault(ziel.id, set()).add(float(wert))
    return werte


def zahlen_im_satz(satz: str) -> set:
    return {float(t.replace(",", ".")) for t in ZAHL.findall(satz or "")}


def grenzen(achse: dict):
    """Alle (Rolle, Grenze)-Paare einer Achse - auch die Aufzaehlungsformen."""
    for rolle in ("unten", "oben"):
        if rolle in achse:
            yield rolle, achse[rolle]
    if achse.get("art") in ("aufzaehlung", "quantile"):
        yield "achse", {"grundlage": achse["grundlage"], "satz": achse["satz"],
                        "regel": None}
    for schluessel in ("zusatzstufe", "zusatzstufe_gemessen"):
        if schluessel in achse:
            z = achse[schluessel]
            yield schluessel, {"grundlage": "methode" if schluessel == "zusatzstufe"
                               else "volatilitaet",
                               "satz": z["satz"],
                               "regel": z.get("weite_regel")}


def main():
    mess = rd._mess()
    definition = rd.raster_definition()
    raster = rd.raster(mess)

    print(__doc__.strip().split("\n")[0])
    print()

    for bot, achsen in definition.items():
        lw = live_werte(bot)
        alle_live = {w for menge in lw.values() for w in menge}
        for name, achse in achsen.items():
            if name.startswith("_"):
                continue
            marke = f"{bot}/{name}"

            for rolle, g in grenzen(achse):
                # --- Wache 3: zugelassene Grundlage ---------------------
                pruefe(f"{marke}[{rolle}]: Grundlage zugelassen",
                       g["grundlage"] in ZUGELASSENE_GRUNDLAGEN | BENANNTE_AUSNAHMEN,
                       f"'{g['grundlage']}'")
                # --- Wache 2: kein Live-Wert im Satz --------------------
                pruefe(f"{marke}[{rolle}]: Begruendungssatz vorhanden",
                       bool((g.get("satz") or "").strip()))
                treffer = zahlen_im_satz(g.get("satz")) & alle_live
                pruefe(f"{marke}[{rolle}]: Satz nennt keinen Live-Wert",
                       not treffer, f"nennt {sorted(treffer)}")
                # --- Wache 1: die Grenze ist gerechnet ------------------
                if g.get("regel") is not None:
                    try:
                        rd.regel_wert(g["regel"], mess)
                        ok = True
                    except SystemExit as e:
                        ok, marke_zusatz = False, str(e)
                    pruefe(f"{marke}[{rolle}]: Regel laesst sich ausrechnen", ok)

            # --- Wache 1 (Fortsetzung): die Stufen folgen den Grenzen ----
            werte = raster[bot][name]
            if achse["art"] in ("geometrisch", "linear"):
                unten = rd.regel_wert(achse["unten"]["regel"], mess)
                oben = rd.regel_wert(achse["oben"]["regel"], mess)
                gerechnet = (rd.geometrische_stufen(unten, oben, achse["stufen"])
                             if achse["art"] == "geometrisch"
                             else rd.lineare_stufen(unten, oben, achse["stufen"]))
                zahlen = [w for w in werte if isinstance(w, (int, float))
                          and not isinstance(w, bool)]
                pruefe(f"{marke}: Stufen sind die gerechneten",
                       all(g in zahlen for g in gerechnet),
                       f"{gerechnet} nicht in {zahlen}")
                # --- Wache 4: die versprochene Stufung ------------------
                if achse["art"] == "geometrisch":
                    faktor = (oben / unten) ** (1.0 / (achse["stufen"] - 1))
                    pruefe(f"{marke}: geometrischer Faktor 1,5 bis 2,0",
                           1.5 <= faktor <= 2.0, f"{faktor:.3f}")
                else:
                    pruefe(f"{marke}: Zaehlparameter sind ganzzahlig",
                           all(float(x).is_integer() for x in gerechnet))
                pruefe(f"{marke}: drei bis fuenf Stufen",
                       3 <= achse["stufen"] <= 5, str(achse["stufen"]))

            # --- Die Stufen selbst sind nicht Gegenstand von Wache 2 ----
            # Ein STUFENWERT darf mit einem Live-Wert zusammenfallen; er ist
            # gerechnet, nicht gewaehlt. Verboten ist nur, ihn im SATZ zu
            # nennen. Diese Zeile haelt den Unterschied fest, damit er nicht
            # spaeter versehentlich verschaerft wird.
            pruefe(f"{marke}: Stufen vorhanden", len(werte) >= 2, str(werte))

        # --- Ausnahmen muessen begruendet sein ---------------------------
        if "_ausnahme" in achsen:
            a = achsen["_ausnahme"]
            pruefe(f"{bot}: eingetragene Ausnahme hat Grund und Folge",
                   bool(a.get("grund")) and bool(a.get("folge")))

    print("=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    print("\nKein Grenzsatz erwaehnt einen Live-Wert; jede Grenze ist gerechnet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
