"""
Start des Dashboards
==============================================================
    python3 dashboard/server.py

Laeuft im Vordergrund, Strg+C beendet. Kein Hintergrunddienst und kein
launchd-Eintrag - das kann spaeter eingerichtet werden, wenn das
Dashboard sich im manuellen Betrieb bewaehrt hat (dasselbe Vorgehen wie
beim Telegram-Bot).

BINDUNG AN 127.0.0.1 - BEWUSSTE GRUNDEINSTELLUNG:
Der Server lauscht standardmaessig NUR auf der lokalen Loopback-Adresse.
Damit ist das Dashboard ausschliesslich auf dem Mac selbst erreichbar,
nicht von anderen Geraeten im WLAN und erst recht nicht aus dem
Internet. Der urspruengliche Plan sah vor, die Erreichbarkeit ueber das
Tailscale-Netz zu regeln - Tailscale ist auf diesem Mac aber noch nicht
eingerichtet. Solange das so ist, waere "lauscht auf allen Interfaces"
die einzige tatsaechliche Zugriffskontrolle, und die gaebe es dann gar
nicht mehr.

Wer trotzdem vom iPhone im selben WLAN zugreifen will, kann
DASHBOARD_HOST=0.0.0.0 setzen - dann greift nur noch das Token als
Schutz, und der Server weist beim Start ausdruecklich darauf hin.

Das wiegt seit dem manuellen Schliessen schwerer als frueher: das
Dashboard ist nicht mehr rein lesend, es hat genau einen schreibenden
Endpunkt (siehe app.py und dashboard/schliessen.py). Der Start gibt
deshalb aus, fuer welche Bots das freigeschaltet ist.
"""

import logging
import os
import sys

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
if _DASHBOARD_DIR not in sys.path:
    sys.path.insert(0, _DASHBOARD_DIR)

import konfig
import schliessen
from app import erzeuge_app

LOKALE_ADRESSEN = {"127.0.0.1", "localhost", "::1"}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        # Laedt das Token und bricht ab, falls keines gesetzt ist -
        # das Dashboard startet nie ohne Zugriffsschutz.
        anwendung = erzeuge_app()
    except RuntimeError as fehler:
        print(f"\nStart abgebrochen: {fehler}\n", file=sys.stderr)
        raise SystemExit(1)

    adresse, tor = konfig.host(), konfig.port()

    print("Trading-Bot-Dashboard")
    print(f"  Adresse: http://{adresse}:{tor}/")
    # Nicht mehr "rein lesend": seit dem manuellen Schliessen gibt es
    # genau einen schreibenden Endpunkt. Wer den Server startet, soll das
    # auf der Startzeile sehen und es nicht erst im Quelltext finden.
    print(f"  Schreibend freigeschaltet: "
          f"{', '.join(schliessen.freigeschaltete_bots())}")
    print("    Positionen manuell schliessen - einzeln: 1 Tap | bot-weit: "
          "2 Klicks | alle Bots: 2 Klicks + Text")
    if adresse in LOKALE_ADRESSEN:
        print("  Bindung: nur localhost - vom iPhone/anderen Geraeten NICHT erreichbar.")
        print("           Fuer den Fernzugriff ist Tailscale (oder Gleichwertiges) noetig,")
        print("           siehe dashboard/README.md.")
    else:
        print(f"  ACHTUNG: gebunden an {adresse} - das Dashboard ist damit im Netzwerk")
        print("           erreichbar. Einziger Schutz ist jetzt das Zugriffs-Token.")
    print("  Beenden mit Strg+C.\n")

    try:
        import uvicorn
    except ImportError:
        print("uvicorn ist nicht installiert: pip3 install -r dashboard/requirements.txt",
              file=sys.stderr)
        raise SystemExit(1)

    # access_log=False ist KEIN Schoenheitsfehler, sondern Absicht: das
    # Zugriffs-Token darf einmalig als ?token=... in der URL stehen (der
    # bequeme Erstaufruf auf dem iPhone), und uvicorns Zugriffsprotokoll
    # wuerde die komplette Anfragezeile inklusive Query-String
    # mitschreiben - das Token stuende dann im Klartext im Log. Fehler,
    # Warnungen und die eigenen Log-Zeilen der App (die nur Pfade ohne
    # Query enthalten) bleiben unveraendert sichtbar.
    uvicorn.run(anwendung, host=adresse, port=tor, log_level="info", access_log=False)


if __name__ == "__main__":
    main()
