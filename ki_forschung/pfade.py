"""Pfade der KI-Forschung (TB-177, BA1).

Der Ordner liegt auf oberster Ebene neben broker/ und dashboard/:
ausserhalb von strategies/ (discover_bots in notifications/monitor.py sieht
ihn nie) und ausserhalb des Laufbereichs (shared/paths.py,
ARBEITSBAUM_PFADE). Geschrieben wird nur in die zwei Datenbanken hier.
"""
import os

KI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(KI_DIR)
SHARED_DIR = os.path.join(REPO_DIR, "shared")
ABRUFE_DB = os.path.join(KI_DIR, "abrufe.db")
AUFRUFE_DB = os.path.join(KI_DIR, "aufrufe.db")
