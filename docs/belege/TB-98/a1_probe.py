"""TB-98 A1, dynamisch: EIN Probelauf des UNVERAENDERTEN Erzeugers fuer EINEN
Bot, Ausgabe in den Scratchpad statt nach research/tb24_haltedauern/daten/.

Warum ein Umschlag: `positionen_holen.py` (Stand e87b06f) schreibt fest nach
`DATEN_DIR` (Z. 78/257/258/286) - ein direkter Aufruf ueberschriebe die
historischen Listen. Der Umschlag importiert das Modul (nicht als __main__),
setzt NUR die Modulvariable `DATEN_DIR` auf den Scratchpad und ruft `main()`.
Rechenweg und Lesewege bleiben damit genau die des Erzeugers.

Er liegt im Repo (docs/belege/TB-98/), weil die Startpruefung des
Selektionsmodus (shared/paths.py, TB-58 Bedingung 1) verlangt, dass der
Einstiegspunkt unter derselben Git-Wurzel liegt wie shared/paths.py.

Aufruf (Repo-Wurzel, Modus-Variablen und Lesehaken per Umgebung):
    TB98_ZIEL=<scratch> python3 docs/belege/TB-98/a1_probe.py <bot>
"""
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
ziel = os.environ["TB98_ZIEL"]
if not os.path.isdir(ziel) or os.listdir(ziel):
    raise SystemExit("TB98_ZIEL muss ein vorhandener, LEERER Ordner sein: %s" % ziel)
bot = sys.argv[1]
sys.argv = [os.path.join(_REPO, "research", "tb24_haltedauern", "positionen_holen.py"), bot]
sys.path.insert(0, os.path.join(_REPO, "research", "tb24_haltedauern"))
import positionen_holen as ph   # noqa: E402

ph.DATEN_DIR = ziel
ph.main()
