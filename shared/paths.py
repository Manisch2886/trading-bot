"""
Pfad-Konfiguration fuer gemeinsam genutzte Skripte
======================================================
Fuer Skripte, die in shared/ liegen und von JEDER Strategie genutzt
werden koennen (Datenabruf, Symbol-Liste). Diese Skripte kennen keine
einzelne Strategie, daher gibt es hier nur die projektweiten,
gemeinsamen Ordner - keine strategie-spezifischen Pfade.
"""

import os

SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SHARED_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")      # Kursdaten - von allen Strategien nutzbar
CONFIG_DIR = os.path.join(BASE_DIR, "config")  # Symbol-Liste, E-Mail-Zugangsdaten

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
