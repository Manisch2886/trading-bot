#!/usr/bin/env python3
"""TB-140 V5 - ein eigener Aufruf von schedule je Aktien-Bot gegen den Ausschnitt
aus der einmal gerechneten Menge (R79 (b)). Liest keine Kursdatei, schreibt nur nach stdout.
Rueckgabe: 0 gleich bei allen vier Bots, 1 Abweichung, 2 nicht messbar (der Kalender laedt nicht,
schedule liefert keinen Tag, oder eine Ausnahme)."""
import argparse
import datetime as dt
import importlib.metadata as md
import platform
import sys
import traceback

KALENDER_NAME = "NYSE"                      # R74 (a); kein anderer Name
GANZ_VON = dt.date(1962, 1, 2)              # docs/belege/TB-138/m1.txt Z. 19
GANZ_BIS = dt.date(2026, 9, 1)              # ebd.
ENDE = dt.date(2026, 8, 31)                 # Register 35.1, Z. 6385-6388 (Ende ausschliesslich)
BOTS = (("elliott_wave_stocks", 2017),      # Register 33.2, Z. 6001-6004
        ("rsi2_mean_reversion", 2018),
        ("turtle_soup_stocks", 2017),
        ("volatility_breakout", 2018))
PAKETE = ("pandas_market_calendars", "pandas", "exchange_calendars", "numpy")


def tage(kal, von, bis):
    """Der Aufruf des Vorgaengers (verfahrensmessung_snapshot.py Z. 230-231)."""
    plan = kal.schedule(start_date=von.isoformat(), end_date=bis.isoformat())
    return [ts.date() for ts in plan.index]


def vergleiche(bot, ausschnitt, aufruf):
    """Druckt die Zeilen eines Bots; True, wenn beide Mengen gleich sind und der Index keinen Tag doppelt fuehrt."""
    a, b = set(ausschnitt), set(aufruf)
    nur_a, nur_b = sorted(a - b), sorted(b - a)
    for t in nur_a:
        print("FALL\tv5\tnur_im_ausschnitt\t%s\t%s" % (bot, t))
    for t in nur_b:
        print("FALL\tv5\tnur_im_aufruf\t%s\t%s" % (bot, t))
    doppelt = len(aufruf) - len(b)
    print("%s: Ausschnitt %d, Aufruf %d (doppelt im Index %d), nur im Ausschnitt %d, nur im Aufruf %d, "
          "erster Tag %s / %s, letzter Tag %s / %s"
          % (bot, len(a), len(b), doppelt, len(nur_a), len(nur_b),
             min(a) if a else "-", min(b) if b else "-", max(a) if a else "-", max(b) if b else "-"))
    return not nur_a and not nur_b and doppelt == 0


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--gegenprobe", action="store_true")
    x = p.parse_args(argv)
    print("# TB-140 V5%s" % (" GEGENPROBE" if x.gegenprobe else ""))
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("sys.version      %s" % " ".join(sys.version.split()))
    print("platform         %s" % platform.platform())
    for name in PAKETE:
        try:
            print("%-24s %s" % (name, md.version(name)))
        except md.PackageNotFoundError:
            print("%-24s nicht installiert" % name)
    try:
        import pandas_market_calendars as mcal
        kal = mcal.get_calendar(KALENDER_NAME)
    except Exception as e:  # noqa: BLE001
        print("NICHT MESSBAR: Kalender %r nicht ladbar: %s: %s" % (KALENDER_NAME, type(e).__name__, e))
        return 2
    ganz = tage(kal, GANZ_VON, GANZ_BIS)
    if not ganz:
        print("NICHT MESSBAR: schedule liefert fuer %s..%s keinen Tag" % (GANZ_VON, GANZ_BIS))
        return 2
    print("\neinmal gerechnete Menge %s..%s: %d Tage" % (GANZ_VON, GANZ_BIS, len(set(ganz))))
    alle_gleich = True
    for bot, jahr in BOTS:
        von = dt.date(jahr, 1, 1)
        ausschnitt = [t for t in ganz if von <= t <= ENDE]
        aufruf = tage(kal, von, ENDE)
        if x.gegenprobe:
            # ein Tag fehlt im Ausschnitt, ein Samstag steht zu viel darin
            samstag = von + dt.timedelta(days=(5 - von.weekday()) % 7)
            ausschnitt = ausschnitt[:100] + ausschnitt[101:] + [samstag]
        gleich = vergleiche(bot, ausschnitt, aufruf)
        alle_gleich = alle_gleich and gleich
        print("    URTEIL V5 %s, Zeitraum %s..%s: %s" % (bot, von, ENDE, "gleich" if gleich else "NICHT gleich"))
    print("\nRUECKGABE %d" % (0 if alle_gleich else 1))
    return 0 if alle_gleich else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
