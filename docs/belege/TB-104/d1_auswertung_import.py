"""TB-104 D1 (c): `auswertung.py` im Modus NUR als Import - es gibt noch keine Rohergebnisse,
die es auswerten koennte. Liegt im Repo, weil die Startpruefung des Selektionsmodus den
Einstiegspunkt unter derselben Git-Wurzel verlangt. Schreibt nichts."""
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_REPO, "research", "vorregistrierung"))
import auswertung  # noqa: E402,F401

print("import auswertung: ok", auswertung.__file__)
